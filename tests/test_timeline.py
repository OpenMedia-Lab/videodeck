"""Exercise the portable timeline CLI, including real local master audio."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "videodeck/scripts/timeline.py"


class TimelineCase(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.input = self.root / "timeline.json"
        self.out = self.root / "captions.srt"
        self.timeline = {
            "version": 1,
            "duration": 2,
            "fps": 30,
            "scenes": [
                {"id": "intro", "start": 0, "end": 1, "source": "opening.png", "action": "Hold"},
                {"id": "detail", "start": 1, "end": 2, "source": "detail.png", "action": "Zoom"},
            ],
            "captions": [
                {"start": 0, "end": 0.8, "text": "中文 API\n保留多行"},
                {"start": 1, "end": 2, "text": r"literal \n stays"},
            ],
            "notes": {"owner": "local"},
        }

    def run_cli(self, command="check", data=None, out=None, *, raw=None, cwd=None):
        if raw is None:
            raw = json.dumps(self.timeline if data is None else data, ensure_ascii=False)
        self.input.write_text(raw, encoding="utf-8")
        arguments = [sys.executable, str(SCRIPT), command, str(self.input)]
        if command == "srt":
            arguments += ["--out", str(self.out if out is None else out)]
        result = subprocess.run(arguments, capture_output=True, text=True, cwd=cwd, timeout=20)
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError:
            self.fail(f"CLI did not emit a JSON report: {result.stdout!r}; stderr={result.stderr!r}")
        return result, report

    def assert_rejected(self, data=None, *, code=None, raw=None):
        result, report = self.run_cli("srt", data, raw=raw)
        self.assertNotEqual(result.returncode, 0, report)
        self.assertFalse(report["ok"])
        self.assertTrue(report["errors"])
        if code:
            self.assertEqual(report["errors"][0]["code"], code)
        self.assertFalse(self.out.exists(), "invalid input must not create an output")
        return report


class TimelineTest(TimelineCase):
    def test_check_accepts_a_silent_timeline_and_extra_metadata(self):
        result, report = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(report["ok"])
        self.assertEqual(report["scenes"], 2)
        self.assertEqual(report["captions"], 2)
        self.assertIsNone(report["audio"])
        self.assertFalse(self.out.exists())

    def test_srt_preserves_multiline_unicode_and_literal_backslash_n(self):
        result, report = self.run_cli("srt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(report["ok"])
        self.assertEqual(
            self.out.read_text(encoding="utf-8"),
            "1\n00:00:00,000 --> 00:00:00,800\n中文 API\n保留多行\n\n"
            "2\n00:00:01,000 --> 00:00:02,000\nliteral \\n stays\n\n",
        )

    def test_empty_captions_are_valid_for_a_video_without_subtitles(self):
        self.timeline["captions"] = []
        result, report = self.run_cli("srt")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["captions"], 0)
        self.assertEqual(self.out.read_bytes(), b"")

    def test_scene_gaps_and_overlaps_beyond_one_frame_prevent_export(self):
        for start, code in [(1.1, "scene_gap"), (0.9, "scene_overlap")]:
            with self.subTest(start=start):
                data = copy.deepcopy(self.timeline)
                data["scenes"][1]["start"] = start
                self.assert_rejected(data, code=code)

    def test_scene_boundaries_accept_one_frame_tolerance(self):
        self.timeline["scenes"][0]["start"] = 0.02
        self.timeline["scenes"][1]["start"] = 1.02
        self.timeline["scenes"][1]["end"] = 1.98
        result, report = self.run_cli()
        self.assertEqual(result.returncode, 0, report)

    def test_scene_ids_are_unique_and_scenes_cover_the_full_duration(self):
        cases = [
            ("duplicate_scene_id", lambda data: data["scenes"][1].update(id="intro")),
            ("scene_gap", lambda data: data["scenes"][0].update(start=0.1)),
            ("scene_gap", lambda data: data["scenes"][1].update(end=1.8)),
            ("scene_overlap", lambda data: data["scenes"][1].update(end=2.1)),
        ]
        for code, mutate in cases:
            with self.subTest(code=code):
                data = copy.deepcopy(self.timeline)
                mutate(data)
                self.assert_rejected(data, code=code)

    def test_invalid_numbers_prevent_export(self):
        for field in ["duration", "fps"]:
            for value in [True, False, None, "30", 0, -1, float("nan"), float("inf"), -float("inf")]:
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.timeline)
                    data[field] = value
                    self.assert_rejected(data)
        for value in [0.00001, 1000000000]:
            with self.subTest(fps=value):
                data = copy.deepcopy(self.timeline)
                data["fps"] = value
                self.assert_rejected(data, code="invalid_number")
        for section in ["scenes", "captions"]:
            for field in ["start", "end"]:
                for value in [True, "1", float("nan"), float("inf")]:
                    with self.subTest(section=section, field=field, value=value):
                        data = copy.deepcopy(self.timeline)
                        data[section][0][field] = value
                        self.assert_rejected(data)

    def test_invalid_json_also_emits_json_and_never_writes(self):
        for raw in ["{", "[]", '{"version": 1, "duration": 1e999}', '{"version": 1, "version": 2}']:
            with self.subTest(raw=raw):
                self.assert_rejected(raw=raw)

    def test_bad_required_fields_prevent_export(self):
        for field in ["version", "duration", "fps", "scenes", "captions"]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.timeline)
                del data[field]
                self.assert_rejected(data)
        for field in ["id", "source", "action"]:
            for value in [None, "", [], True]:
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.timeline)
                    data["scenes"][0][field] = value
                    self.assert_rejected(data)
        for value in [True, 1.0, 2]:
            data = copy.deepcopy(self.timeline)
            data["version"] = value
            self.assert_rejected(data)

    def test_captions_must_be_ordered_nonoverlapping_and_in_bounds(self):
        cases = [
            ("caption_overlap", [{"start": 0, "end": 1.2, "text": "A"}, {"start": 1, "end": 2, "text": "B"}]),
            ("caption_order", [{"start": 1, "end": 2, "text": "A"}, {"start": 0, "end": 0.8, "text": "B"}]),
            ("invalid_number", [{"start": -0.001, "end": 1, "text": "A"}]),
            ("invalid_number", [{"start": 0, "end": 2.001, "text": "A"}]),
            ("invalid_number", [{"start": 1, "end": 1, "text": "A"}]),
        ]
        for code, captions in cases:
            with self.subTest(code=code):
                data = copy.deepcopy(self.timeline)
                data["captions"] = captions
                self.assert_rejected(data, code=code)

    def test_caption_text_cannot_break_the_srt_format(self):
        for value in ["", " \t", "line\n\nline", "line\n \nline", "\nline", "line\n", "A --> B", "a\x00b", "a\rb", "a\x1bb", "a\x85b", "a\u2028b", None]:
            with self.subTest(value=value):
                data = copy.deepcopy(self.timeline)
                data["captions"][0]["text"] = value
                self.assert_rejected(data, code="caption_text")

    def test_srt_rejects_a_caption_that_collapses_after_millisecond_rounding(self):
        self.timeline["captions"] = [{"start": 0.0001, "end": 0.0004, "text": "too short"}]
        result, report = self.run_cli()
        self.assertEqual(result.returncode, 0, report)
        self.assert_rejected(code="srt_timing")

    def test_srt_rounds_to_the_nearest_millisecond(self):
        self.timeline["captions"] = [{"start": 0.0005, "end": 1.2345, "text": "半毫秒"}]
        result, report = self.run_cli("srt")
        self.assertEqual(result.returncode, 0, report)
        self.assertIn("00:00:00,001 --> 00:00:01,235", self.out.read_text(encoding="utf-8"))

    def test_existing_output_is_never_overwritten(self):
        self.out.write_text("keep existing", encoding="utf-8")
        result, report = self.run_cli("srt")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["errors"][0]["code"], "output_exists")
        self.assertEqual(self.out.read_text(encoding="utf-8"), "keep existing")
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ["captions.srt", "timeline.json"])

    def test_input_and_output_must_be_different_even_through_a_symlink(self):
        for use_symlink in [False, True]:
            with self.subTest(symlink=use_symlink):
                target = self.input
                if use_symlink:
                    target = self.root / "alias.srt"
                    target.symlink_to(self.input)
                result, report = self.run_cli("srt", out=target)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(report["errors"][0]["code"], "output_input_same")
                self.assertEqual(json.loads(self.input.read_text(encoding="utf-8")), self.timeline)

    def test_cli_usage_errors_are_machine_readable(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "srt", str(self.input)], capture_output=True, text=True, timeout=20)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["errors"][0]["code"], "usage")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "real audio tests require ffmpeg and ffprobe")
class MasterAudioTest(TimelineCase):
    @classmethod
    def setUpClass(cls):
        cls.audio_workspace = tempfile.TemporaryDirectory()
        cls.master = Path(cls.audio_workspace.name) / "master.wav"
        subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=16000:duration=1.5", "-c:a", "pcm_s16le", str(cls.master)],
            check=True, capture_output=True, timeout=20,
        )

    @classmethod
    def tearDownClass(cls):
        cls.audio_workspace.cleanup()

    def setUp(self):
        super().setUp()
        media = self.root / "media"
        media.mkdir()
        shutil.copyfile(self.master, media / "主音轨.wav")
        self.timeline["audio"] = {"path": "media/主音轨.wav"}

    def test_audio_path_is_resolved_relative_to_json_instead_of_cwd(self):
        result, report = self.run_cli(cwd=self.audio_workspace.name)
        self.assertEqual(result.returncode, 0, report)
        self.assertAlmostEqual(report["audio"]["duration"], 1.5, places=3)
        self.assertEqual(report["audio"]["offset"], 0)

    def test_actual_full_audio_duration_cannot_be_shortened_by_metadata(self):
        self.timeline["duration"] = 1
        self.timeline["scenes"] = self.timeline["scenes"][:1]
        self.timeline["captions"] = self.timeline["captions"][:1]
        self.timeline["audio"]["duration"] = 0.8
        self.assert_rejected()
        del self.timeline["audio"]["duration"]
        self.assert_rejected(code="audio_truncated")

    def test_audio_offset_plus_actual_duration_must_fit_timeline(self):
        self.timeline["audio"]["offset"] = 0.6
        self.assert_rejected(code="audio_truncated")

    def test_matching_audio_duration_is_checked_against_ffprobe(self):
        self.timeline["audio"].update(duration=1.5, offset=0.5)
        result, report = self.run_cli("srt")
        self.assertEqual(result.returncode, 0, report)
        self.assertTrue(self.out.is_file())

    def test_audio_allows_one_frame_of_container_rounding(self):
        self.timeline["audio"]["offset"] = 0.52
        result, report = self.run_cli()
        self.assertEqual(result.returncode, 0, report)

    def test_audio_declared_duration_is_not_used_as_a_trim_instruction(self):
        self.timeline["audio"]["duration"] = 1
        self.assert_rejected(code="audio_duration_mismatch")

    def test_audio_fields_and_remote_paths_are_rejected(self):
        for audio in [None, [], {}, {"path": "https://example.com/master.wav"}, {"path": str(self.master)}, {"path": "missing.wav"}, {"path": "media/主音轨.wav", "offset": -0.1}, {"path": "media/主音轨.wav", "offset": True}, {"path": "media/主音轨.wav", "duration": False}]:
            with self.subTest(audio=audio):
                data = copy.deepcopy(self.timeline)
                data["audio"] = audio
                self.assert_rejected(data)


if __name__ == "__main__":
    unittest.main()
