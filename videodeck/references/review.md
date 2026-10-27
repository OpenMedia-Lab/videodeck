# Review the rendered artifact

Use the actual final MP4, not only the HTML preview or screenshots. Verify decode,
streams, dimensions and duration with ffprobe/FFmpeg. When audio exists, check its
start/end and compare the decoded track with the complete master, allowing known
codec padding. For narration, follow the
[pronunciation record](audio.md#pronunciation-before-the-master) for risky spans;
ASR text equality does not verify their phonetic reading.

## Evidence preparation

Locate [caption-cli](https://github.com/OpenMedia-Lab/caption-cli), check installed
help and run `doctor`; install only if missing and setup is permitted. If unavailable,
use equivalent local timestamped evidence and name the substituted tools and limits.
It uses local FFmpeg and no model API. Example (paths are project-local):

```bash
caption-cli video-read --file output/final.mp4 --out review/full --transcript captions.srt
caption-cli video-read --file output/final.mp4 --out review/transition --start 4 --end 6 --fps 8 --frame-width 720
```

Omit transcript options for silent work without subtitles.

SRT timestamps use original source time, including focused ranges. Canonical
captions are expected text, not independent recognition. Label transcript provenance;
optional local ASR can use `caption-cli transcribe` with a local whisper.cpp binary
and model, or another trusted tool. Use `--transcript-provenance local_asr` for its
output. Follow the [audio evidence limits](audio.md#listening-capability); ASR does
not prove pronunciation.

Read `packet.json` and assign its `tasks.jsonl` ranges to yourself/subagents. Open
the actual contact sheets, compare canonical text and source, and inspect audio
evidence with the host's real capabilities. Mark a task reviewed only after its
evidence was consumed. A prepared packet or subagent dispatch is not a completed
review. Inspect every assigned sheet; ensure the reviewed ranges cover the film.

At ordinary sampling rates, inspect all-time-range story continuity; sample more
densely around fast effects, boundaries, formulas and suspect cues. Derive focused
ranges from actual timeline anchors: begin before the first actor/label moves and
end after the last actor settles and labels appear. Read packet timestamps; a
range starting with an already assembled result does not inspect its assembly.
Include every scene boundary and the full sweep of moving objects near text.
Check native-size crops for the [complete notation inventory](storyboard.md#visible-mathematics),
not only prominent equations, and inspect the cover at thumbnail size. Distinguish
sampled visual coverage from continuous playback or frame-by-frame verification.

For motion quality, compare the accepted sample and changed passages at matched
playback speed when supported, including outgoing/incoming states. Check focus,
identity, acceleration, settling, readable holds and planned occlusion against the
[motion specification](art-direction.md#preserve-transitions). Log concrete defects
with times. If playback is unavailable, leave smoothness unverified; contact sheets
and passing validators do not establish it.

## Release criteria

| Check | Required evidence / failure condition |
| --- | --- |
| Notation | Reconcile every inventory occurrence with actual encoded pixels and source meaning. Unrendered or wrong notation fails, including a small dimension label. |
| Motion | Cover each boundary and complete demanding action arcs against the accepted motion specification. Lost transitions, clipped exits, unrelated text occlusion or missing readable holds fail. |
| Dimensionality | Check the brief's scoped reason for 3D. Unjustified extrusion or an unapproved departure from accepted dimensionality fails the design contract. |

Known failures MUST be repaired within scope and rechecked before calling the
artifact ready. Unavailable capabilities require targeted human review and MUST
remain unverified, not passed.

## Review contract

Record artifact hash/version, reviewer, ranges/sheets actually opened, sample
rates, checks, findings, repairs and unverified capabilities. Review source fidelity,
technical meaning, narrative flow, geometry, text, effects, caption timing and sound.
Compare final encoded geometry with the accepted [layout measurements](art-direction.md),
including closing cards and covers at phone size. For sound, record actual listening
coverage and unverified pronunciation/music judgments using the audio guide's limits.

Fix the earliest bad layer, rerender affected artifacts and update the review to
the new version. Recheck affected intervals and boundaries; full decode/metadata
checks remain inexpensive. Preserve accepted core material during polish-only
feedback. Report an out-of-scope defect and its consequence instead of claiming
the entire film passed. Show the human the same film version the review describes.

Deliver a usable local bundle even if publishing credentials are unavailable.
Never label known unchecked sound or unresolved defects as verified quality.
