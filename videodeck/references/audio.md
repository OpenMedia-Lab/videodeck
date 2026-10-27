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

Before a full narration take, use the pronunciation pass below. Generate continuous
candidate tracks for continuity before final shot timing.
For long narration, synthesize coherent chapters with the same frozen recipe, then
assemble one complete master; preserve pauses and check boundaries. Music, when
requested, gets its own coherent track and deliberate relation to the narration.

## Pronunciation before the master

Before full synthesis, the agent MUST scan the complete canonical narration and
its source for technical terms: acronyms, product/model names, units, mixed-language
phrases, numbers/formulas and Chinese polyphones. Cover every spoken occurrence,
including compounds and case variants; a few handpicked test words are insufficient.
Automate matching against the lexicon, then make a contextual pass for missed or
ambiguous terms. Regex and ASR alone are not a complete terminology scan.

Maintain one reusable project/domain pronunciation lexicon. Each entry records
**canonical term, occurrence contexts/IDs, intended reading, active synthesis
control, and evidence/status**. Merge confirmed series choices first; a current
explicit override wins. Resolve ordinary readings from the source and reliable
term references; ask only when a consequential convention remains ambiguous.
Newly detected terms are candidates, not automatically approved pronunciations.

| Context | Decision |
| --- | --- |
| 一行矩阵 / 并行计算、运行时 | Context selects háng / xíng; never globally replace 行. |
| MoE / DeepSeekMoE | Reuse the confirmed convention; if letter-by-letter was selected, test `M O E` / `DeepSeek M O E` in the actual sentence. |
| RAM, MiB or ambiguous shorthand | Establish the source term and intended word/letter/expanded reading. Do not infer a reading from capitalization or a viewer's shorthand. |

Generate a separate, inspectable TTS input from the lexicon BEFORE synthesis.
Apply reversible aliases or verified dictionary/phoneme/SSML controls to each
context; preserve canonical subtitles, screen text and units. Check occurrence
coverage and the canonical-to-synthesis diff: no missed risky term, unrelated
replacement or changed meaning. Never silently convert every acronym to letters.

Verify that the model's active generation path actually consumes the control.
Unsupported markup or an instruction prompt is not a pronunciation fix. With the
frozen voice recipe, test each new, changed or unverified entry in its complete
sentence; retain the take/time and update the lexicon for reuse. Recipe/engine
changes require rechecking affected controls. Keep detected, annotated and
listening-verified states distinct; unresolved readings cannot be marked passed.

Inspect risky spans again in the encoded deliverable. Unprompted ASR detects
omitted/changed words; identical Chinese characters do not verify a polyphone's
sound, and normalized acronyms do not verify letters versus a word. Alignment
supplies positions, not phonetic proof. Verify through actual listening; otherwise
provide timestamped clips for human review and leave pronunciation unverified.

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

For an authorized pronunciation repair, regenerate a coherent sentence/scene with
the accepted voice. Preserve unrelated audio and compare the untouched regions,
joins and timing; do not assemble individual syllables to hide a bad take.

## Align canonical words

Build canonical captions with acoustic word/sentence anchors from the real audio.
Record doubtful or zero-length spans and inspect their audio; use the pronunciation
record above for phonetic checks.

Re-time dependent captions, actions and transitions whenever audio changes. Do not
solve a changed voice length by squeezing audio into stale fixed scene durations.
Export canonical captions through the [timeline helper](timeline.md) when useful.

## Listening capability

Use native audio understanding when available. Otherwise record local ASR/sample
evidence and explicit listening limits; delegating to an equally limited host adds
no hearing capability. Distinguish signal integrity, ASR, actual listening and
human voice/music/synchronization review.
