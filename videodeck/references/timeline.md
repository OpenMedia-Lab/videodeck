# Timeline helper contract

Optional Python 3.10+ standard-library helper; ffprobe is needed only when `audio`
is present. Invoke through the interpreter, with paths relative to your working
directory (replace `SKILL` with the installed skill folder):

```bash
python3 SKILL/scripts/timeline.py check project/timeline.json
python3 SKILL/scripts/timeline.py srt project/timeline.json --out project/captions.srt
```

Minimal silent example (seconds, canonical display text):

```json
{
  "version": 1,
  "duration": 4,
  "fps": 30,
  "scenes": [
    {"id": "route", "start": 0, "end": 2, "source": "article.md#routing", "action": "Follow the same token into two selected Experts"},
    {"id": "merge", "start": 2, "end": 4, "source": "article.md#weighted-sum", "action": "Weight the outputs, then add them"}
  ],
  "captions": [
    {"start": 0.2, "end": 1.8, "text": "MoE: select Experts"},
    {"start": 2.1, "end": 3.8, "text": "Weight each output.\nThen add them."}
  ]
}
```

For sound add `"audio": {"path": "master.wav", "offset": 0}`. The path is local,
relative to the JSON; the complete file duration is measured, not inferred from
captions. Optional `audio.duration` is checked against that measurement. Sound may
end before the video. Its offset plus complete duration must fit inside the video,
allowing one frame of tolerance; exact sample-level waveform verification remains
a separate audio check.

Scene intervals must cover the timeline in order, with at most one frame of
boundary tolerance. IDs are unique; source and action are required, narration and
transition optional. FPS supports 1–240, including fractional rates. Extra metadata
can retain source hashes, cue provenance or locked decisions. Empty caption arrays
are valid. Captions use strict bounds and no overlaps; empty text, blank paragraphs,
SRT arrows and format-breaking controls are rejected.

Both commands emit one JSON success/error report and fail nonzero on invalid input.
SRT export validates the entire input before writing, uses half-up millisecond
rounding, preserves Unicode and real text newlines, and refuses to overwrite an
existing output. Literal backslash-n is not converted. Intervals that collapse or
overlap after rounding fail rather than producing broken cues.

This is a timing/format check. A contiguous timeline does not prove the audio is
complete at source, the picture explains the math, the words were pronounced
correctly, or the human approved anything.
