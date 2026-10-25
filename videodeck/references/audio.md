# Audio and timing

## Select, then generate

For a new voice, show comparable same-text audio auditions and wait for the user's
selection through the host's interactive question tool. Reuse a confirmed voice
without a fresh audition. Persist the exact
reference, reference transcript/hash, model/version, parameters and seeds that
actually affect that model's generation path. A requested timbre is not an audition.
Do not silently replace the chosen voice with a framework's convenient stock voice.

Narration, music and effects can come from different local or user-selected tools.
No cloud provider or API key is required by this skill. Tool unavailability should
yield a concrete local alternative for selection, not an unannounced voice change.
Use original/licensed references according to the project's permissions.

Generate continuous candidate tracks for continuity before final shot timing.
For long narration, synthesize coherent chapters with the same frozen recipe, then
assemble one complete master; preserve pauses and check boundaries. Music, when
requested, gets its own coherent track and deliberate relation to the narration.

## Preserve the waveform

Measure actual source duration and sample count. Never clip audio at a scene's
visual endpoint. Visual transitions and narration use independent tracks.
The final timeline contains the complete master, including intended lead-in/tail.

If a word is cut off, locate the earliest bad artifact: generation/decoder output,
reference removal, chapter join, timeline trim, render or encode. Compare raw and
packaged samples and decoded final audio. Missing decoded speech must be recovered
from a complete source or regenerated; padding silence cannot restore it. Use exact
sample slicing when removing a reference, and verify the model's valid-length
contract instead of assuming zero codec IDs are padding. Fade music deliberately;
do not fade away the last phoneme to hide a defect.

## Align canonical words

Keep canonical display/subtitle text unchanged; only synthesis uses aliases such
as `MoE` → `M O E`. Maintain a reversible mapping to display terms. Build captions
from the canonical script, with acoustic word/sentence anchors from the real audio.
Forced alignment estimates positions; independent unprompted ASR audits missing
words and pronunciation. Neither proves phonetic accuracy. Record doubtful or
zero-length spans and inspect/listen where possible.

Re-time dependent captions, actions and transitions whenever audio changes. Do not
solve a changed voice length by squeezing audio into stale fixed scene durations.
Export canonical captions through the [timeline helper](timeline.md) when useful.

## Listening capability

Use native playback/audio understanding when the host supports it. Otherwise use
local ASR, waveform/sample checks and explicit review limits. A subagent with the
same input limits does not magically hear the audio. Distinguish measured integrity,
ASR evidence, actual listening and human audition of voice/music/synchronization.
