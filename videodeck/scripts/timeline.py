#!/usr/bin/env python3
"""Validate a version 1 timeline and exclusively export its canonical captions.

Times are seconds. Supported fps: 1 through 240. Scene boundaries and master
audio duration allow one frame of tolerance; captions use strict boundaries.
Audio paths are local and relative to the input JSON. ffprobe is needed only
when audio is present. Validation checks structure and timing, not meaning or
consent. Every command emits one JSON report; failures exit nonzero.
"""

import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata


class TimelineError(Exception):
    def __init__(self, code, message, field=None):
        super().__init__(message)
        self.detail = {"code": code, "message": message}
        if field is not None:
            self.detail["field"] = field


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise TimelineError("usage", message)


def number(value, field, *, minimum=None, maximum=None, positive=False):
    if type(value) not in (int, float):
        raise TimelineError("invalid_number", "must be a finite number", field)
    try:
        value = float(value)
    except (OverflowError, ValueError):
        raise TimelineError("invalid_number", "must be a finite number", field)
    if not math.isfinite(value):
        raise TimelineError("invalid_number", "must be a finite number", field)
    if positive and value <= 0:
        raise TimelineError("invalid_number", "must be greater than zero", field)
    if minimum is not None and value < minimum:
        raise TimelineError("invalid_number", f"must be at least {minimum}", field)
    if maximum is not None and value > maximum:
        raise TimelineError("invalid_number", f"must be at most {maximum}", field)
    return value


def text(value, field, *, allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise TimelineError("invalid_field", "must be a nonempty string", field)
    return value


def object_value(value, field):
    if not isinstance(value, dict):
        raise TimelineError("invalid_field", "must be an object", field)
    return value


def list_value(value, field):
    if not isinstance(value, list):
        raise TimelineError("invalid_field", "must be an array", field)
    return value


def reject_constant(value):
    raise ValueError(f"nonfinite JSON number: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def finite_json(value):
    """Reject overflowed JSON numbers even when they appear in extra metadata."""
    if isinstance(value, dict):
        for child in value.values():
            finite_json(child)
    elif isinstance(value, list):
        for child in value:
            finite_json(child)
    elif isinstance(value, float) and not math.isfinite(value):
        raise ValueError("nonfinite JSON number")


def load_timeline(path):
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_constant,
            object_pairs_hook=unique_object,
        )
        finite_json(value)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise TimelineError("invalid_json", "input must be valid finite UTF-8 JSON") from error
    except OSError as error:
        raise TimelineError("input_error", "cannot read timeline JSON") from error
    return object_value(value, "timeline")


def caption_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise TimelineError("caption_text", "caption text must be nonempty", field)
    if "-->" in value or any(not line.strip() for line in value.split("\n")):
        raise TimelineError("caption_text", "caption text cannot contain arrows or blank lines", field)
    for character in value:
        if character == "\n":
            continue
        if unicodedata.category(character) in {"Cc", "Cs", "Zl", "Zp"}:
            raise TimelineError("caption_text", "caption text contains a format-breaking character", field)
    return value


def probe_audio(audio, timeline_path, duration, tolerance):
    object_value(audio, "audio")
    raw_path = text(audio.get("path"), "audio.path")
    path = Path(raw_path)
    if path.is_absolute() or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", raw_path) or "\x00" in raw_path:
        raise TimelineError("audio_path", "audio path must be local and relative to the JSON", "audio.path")
    try:
        path = (timeline_path.parent / path).resolve()
        if not path.is_file():
            raise TimelineError("audio_path", "audio path must name a local file", "audio.path")
    except (OSError, ValueError, RuntimeError) as error:
        raise TimelineError("audio_path", "cannot resolve local audio file", "audio.path") from error
    offset = number(audio.get("offset", 0), "audio.offset", minimum=0)
    declared = None
    if "duration" in audio:
        declared = number(audio["duration"], "audio.duration", positive=True)
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error", "-protocol_whitelist", "file",
                "-i", str(path), "-show_entries", "format=duration:stream=codec_type,duration",
                "-of", "json",
            ],
            capture_output=True, text=True, encoding="utf-8", timeout=15, check=False,
        )
        if result.returncode:
            raise ValueError("ffprobe could not inspect audio")
        probed = json.loads(result.stdout, parse_constant=reject_constant)
        streams = [stream for stream in probed.get("streams", []) if stream.get("codec_type") == "audio"]
        if not streams:
            raise ValueError("file has no audio stream")
        candidates = [probed.get("format", {}).get("duration")]
        candidates.extend(stream.get("duration") for stream in streams)
        lengths = []
        for candidate in candidates:
            if candidate is None or candidate == "N/A":
                continue
            length = float(candidate)
            if not math.isfinite(length) or length <= 0:
                raise ValueError("invalid probed duration")
            lengths.append(length)
        if not lengths:
            raise ValueError("duration unavailable")
        actual = max(lengths)
    except (OSError, subprocess.TimeoutExpired, ValueError, TypeError, AttributeError) as error:
        raise TimelineError("audio_probe", "ffprobe could not determine complete local audio duration", "audio.path") from error
    if declared is not None and abs(declared - actual) > tolerance + 1e-9:
        raise TimelineError("audio_duration_mismatch", "declared duration differs from the complete audio file", "audio.duration")
    if offset + actual > duration + tolerance + 1e-9:
        raise TimelineError("audio_truncated", "timeline would cut off the master audio", "audio")
    return {"path": str(path), "offset": offset, "duration": actual}


def validate(timeline, path):
    if type(timeline.get("version")) is not int or timeline["version"] != 1:
        raise TimelineError("invalid_field", "version must be the integer 1", "version")
    duration = number(timeline.get("duration"), "duration", positive=True)
    fps = number(timeline.get("fps"), "fps", minimum=1, maximum=240)
    tolerance = 1 / fps
    scenes = list_value(timeline.get("scenes"), "scenes")
    if not scenes:
        raise TimelineError("invalid_field", "at least one scene is required", "scenes")
    previous_end = 0
    identifiers = set()
    for index, scene in enumerate(scenes):
        field = f"scenes[{index}]"
        object_value(scene, field)
        identifier = text(scene.get("id"), f"{field}.id")
        if identifier in identifiers:
            raise TimelineError("duplicate_scene_id", "scene ids must be unique", f"{field}.id")
        identifiers.add(identifier)
        text(scene.get("source"), f"{field}.source")
        text(scene.get("action"), f"{field}.action")
        if "narration" in scene:
            text(scene["narration"], f"{field}.narration", allow_empty=True)
        if "transition" in scene:
            text(scene["transition"], f"{field}.transition")
        start = number(scene.get("start"), f"{field}.start", minimum=0)
        end = number(scene.get("end"), f"{field}.end", positive=True)
        if end <= start:
            raise TimelineError("invalid_number", "scene end must follow its start", field)
        if start - previous_end > tolerance + 1e-9:
            raise TimelineError("scene_gap", "scenes must cover the timeline without gaps", field)
        if previous_end - start > tolerance + 1e-9:
            raise TimelineError("scene_overlap", "scenes must not overlap", field)
        if end > duration + tolerance + 1e-9:
            raise TimelineError("scene_overlap", "scene extends beyond timeline duration", field)
        previous_end = end
    if duration - previous_end > tolerance + 1e-9:
        raise TimelineError("scene_gap", "scenes must reach timeline duration", "scenes")
    captions = list_value(timeline.get("captions"), "captions")
    previous_start = previous_end = 0
    for index, caption in enumerate(captions):
        field = f"captions[{index}]"
        object_value(caption, field)
        start = number(caption.get("start"), f"{field}.start", minimum=0, maximum=duration)
        end = number(caption.get("end"), f"{field}.end", minimum=0, maximum=duration)
        if end <= start:
            raise TimelineError("invalid_number", "caption end must follow its start", field)
        if start < previous_start:
            raise TimelineError("caption_order", "captions must be in chronological order", field)
        if start < previous_end:
            raise TimelineError("caption_overlap", "captions must not overlap", field)
        caption_text(caption.get("text"), f"{field}.text")
        previous_start, previous_end = start, end
    audio = None
    if "audio" in timeline:
        audio = probe_audio(timeline["audio"], path, duration, tolerance)
    return {"duration": duration, "fps": fps, "scenes": len(scenes), "captions": len(captions), "audio": audio}


def milliseconds(seconds):
    # Decimal(str(...)) preserves the authored half millisecond instead of
    # depending on binary float representation or Python's ties-to-even round.
    return int((Decimal(str(seconds)) * 1000).to_integral_value(rounding=ROUND_HALF_UP))


def timestamp(value):
    seconds, millis = divmod(value, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def render_srt(timeline):
    result = []
    previous_end = 0
    final_end = milliseconds(timeline["duration"])
    for index, caption in enumerate(timeline["captions"], 1):
        start, end = milliseconds(caption["start"]), milliseconds(caption["end"])
        if start < previous_end or start >= end or end > final_end:
            raise TimelineError("srt_timing", "caption becomes invalid after millisecond rounding", f"captions[{index - 1}]")
        result.append(f"{index}\n{timestamp(start)} --> {timestamp(end)}\n{caption['text']}\n\n")
        previous_end = end
    return "".join(result)


def write_exclusive(output, source, content):
    """Publish a complete file with an atomic hard link that never replaces one."""
    temporary = None
    try:
        if output.resolve() == source.resolve() or (output.exists() and os.path.samefile(output, source)):
            raise TimelineError("output_input_same", "output must differ from input JSON")
        descriptor, temporary = tempfile.mkstemp(prefix=".timeline-", suffix=".tmp", dir=output.parent)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, output)
    except FileExistsError as error:
        raise TimelineError("output_exists", "output already exists; choose a new path") from error
    except (OSError, ValueError, RuntimeError, UnicodeError) as error:
        raise TimelineError("output_error", "cannot create the output file") from error
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass


def main(argv=None):
    parser = Parser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check_parser = commands.add_parser("check", help="check structure and timing")
    check_parser.add_argument("timeline", type=Path)
    srt_parser = commands.add_parser("srt", help="check fully, then create a new UTF-8 SRT")
    srt_parser.add_argument("timeline", type=Path)
    srt_parser.add_argument("--out", required=True, type=Path)
    command = None
    try:
        args = parser.parse_args(argv)
        command = args.command
        timeline = load_timeline(args.timeline)
        report = validate(timeline, args.timeline)
        if command == "srt":
            write_exclusive(args.out, args.timeline, render_srt(timeline))
            report["output"] = str(args.out.resolve())
        print(json.dumps({"ok": True, "command": command, **report}, ensure_ascii=False, allow_nan=False))
        return 0
    except TimelineError as error:
        print(json.dumps({"ok": False, "command": command, "errors": [error.detail]}, ensure_ascii=False, allow_nan=False))
        print(f"timeline: {error.detail['message']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
