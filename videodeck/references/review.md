# Review the rendered artifact

Use the actual final MP4, not only the HTML preview or screenshots. Verify decode,
streams, dimensions, duration and audio start/end with ffprobe/FFmpeg. Compare final
decoded audio against the complete master, allowing known codec padding. No universal
fixed padding frame count guarantees an intact spoken tail.

## Evidence preparation

Install [caption-cli](https://github.com/OpenMedia-Lab/caption-cli), run `doctor`,
and check command help for the installed version. It uses local FFmpeg and no model
API. Example (paths are project-local):

```bash
caption-cli video-read --file output/final.mp4 --out review/full --transcript captions.srt
caption-cli video-read --file output/final.mp4 --out review/transition --start 4 --end 6 --fps 8 --frame-width 720
```

SRT timestamps refer to original source time even for focused ranges. Canonical
script captions are expected text, not independent recognition. Label their origin
in the review record; don't claim they prove the speech matches. For independent
local ASR, `caption-cli transcribe` accepts a local whisper.cpp binary/model; use
its output with `--transcript-provenance local_asr`. Models are optional downloads,
not bundled dependencies. Other trusted local ASR is equally usable.

Read `packet.json` and assign its `tasks.jsonl` ranges to yourself/subagents. Open
the actual contact sheets, compare canonical text and source, and inspect audio
evidence with the host's real capabilities. Mark a task reviewed only after its
evidence was consumed. A prepared packet or subagent dispatch is not a completed
review. Inspect every assigned sheet; ensure the reviewed ranges cover the film.

At ordinary sampling rates, inspect all-time-range story continuity; sample more
densely around fast effects, boundaries, formulas and suspect cues. Check selected
frames at full size for math/subtitles and the cover at thumbnail size. Distinguish
sampled visual coverage from continuous playback or frame-by-frame verification.

## Review contract

Record artifact hash/version, reviewer, ranges/sheets actually opened, sample
rates, checks, findings, repairs and unverified capabilities. Review source fidelity,
technical meaning, narrative flow, geometry, text, effects, caption timing and sound.
ASR/alignment are supporting evidence; explicitly record unavailable listening,
music/timbre judgment or continuous motion review.

Fix the earliest bad layer, rerender affected artifacts and update the review to
the new version. Recheck affected intervals and boundaries; full decode/metadata
checks remain inexpensive. Preserve accepted core material during polish-only
feedback. Report an out-of-scope defect and its consequence instead of claiming
the entire film passed. Show the human the same film version the review describes.

Deliver a usable local bundle even if publishing credentials are unavailable.
Never label known unchecked sound or unresolved defects as verified quality.
