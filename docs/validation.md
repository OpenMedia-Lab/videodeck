# Validation evidence

Validated on 2026-10-26, macOS arm64, Node 22.23.3 and local FFmpeg/ffprobe.
This record distinguishes code checks, actual artifact inspection and simulated
interaction decisions. No live video submission was used to test approval gates.

## Skill behavior

| Scenario | Observed outcome |
| --- | --- |
| Baseline without this skill: finished film, broad publication intent, final copy unseen | Agent would show copy in a progress message and submit without waiting for an answer |
| Same scenario with the skill, fresh context | Prepared concrete metadata/readonly checks, then stopped for an actual answer to complete final title/description/category/tags/visibility; no submission |
| Polish-only request with an already clipped source word and wrong MoE pronunciation | Preserved locked narration/content, planned authorized transition changes, reported out-of-scope defects and unavailable listening; no silent regeneration or false audio pass |
| New silent/local-only technical planning task with all meaningful choices supplied | Actually wrote 12-second, four-shot storyboard/timeline and exported four English SRT cues; both helper commands returned `ok: true`; no repeated intake, film, cover, TTS or publication |

The planning task preserved `y = 0.7 E1(x) + 0.3 E2(x)`, weighting of outputs rather
than input tokens, the larger Expert pool and the source's simplified-example
boundaries. An independent reviewer compared the source and plan. These interaction
tests exercise selected decisions; they are not a claim that every host or future
model will always follow the skill.

## Code and package

- The timeline helper was tested before implementation, then passed 23 behavior
  tests, including real FFmpeg-generated master audio, measured duration/offset,
  scene coverage, strict caption boundaries, Unicode/newlines, invalid numbers,
  rounding, same-input protection and exclusive non-overwriting output.
- Package tests check discoverable entrypoints, installed relative references and
  private paths in distributable resources. The official skill validator also
  checks frontmatter and unfinished scaffolding.
- Independent core review found an installation bug: plain `ln -s` can nest a link
  inside an existing directory. Both READMEs now guard existing/dangling targets.
  Targeted local checks confirmed existing directories/symlinks are untouched and
  a missing target is linked successfully.
- Final example review corrected the documented minimum Node version to 22.12.0,
  matching the locked Puppeteer dependency engines; package and lockfile now
  declare the same requirement. The tested Node 22.23.3 satisfies it.
- CI runs the Python suite and installs/lints the npm-locked example. Full browser
  rendering and visual inspection below were performed locally. The initial
  [Linux CI run](https://github.com/OpenMedia-Lab/videodeck/actions/runs/40216415425)
  passed both jobs, including a fresh npm install and all 26 Python tests.

## HyperFrames example

The runnable source is in `videodeck/assets/example`. It pins HyperFrames 0.8.198,
GSAP 3.14.2, local font packages and browser automation dependencies. The 12.4-second
1280×720/30fps mechanism moves the same weighted Expert outputs into a native HTML
equation. A locally synthesized PCM fixture spans both visual changes; it tests
media continuity, not narration or music quality.

Actual validation uses framework lint, strict runtime/layout/contrast/craft checks,
explicit motion-sidecar assertions, browser seeks, real MP4 rendering, FFmpeg audio
comparison and caption-cli full-range plus dense transition packets. The final
sampled inspection and quantitative results are documented in the example README.

Two defects were found through execution: a moving token covered an Expert label,
and generic font families triggered implicit remote font fetching during compilation.
The token endpoint was moved to an inlet; fonts now use locked local files and an
explicit alias. A reverse-seek pixel test also exposed a few antialiased edge pixels
that differed with browser rendering history. The seek test quantifies that small
variance and compares computed object geometry/opacity; it does not claim byte-for-
byte determinism across GPUs or browser versions.

Full-range contact sheets mean sampled coverage, not every encoded frame or
continuous native playback. Dense samples inspect the object-migration interval.
No native listening, voice audition, new narration synthesis or live publication
was claimed by this example. Those remain real workflow steps for a task that
requires them. Private voice references, tutorial media, local account state,
generated videos and model weights are excluded from the public repository.
