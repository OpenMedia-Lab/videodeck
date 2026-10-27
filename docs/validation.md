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

## Portrait publication feedback

A real publication task exposed two gaps after user acceptance: asymmetric
interface-safe margins displaced the main diagrams by roughly 40–54 pixels in a
1080-pixel portrait frame, and a readable public video was later restricted for
an outbound article URL in its body. Creator detail still showed enabled/public;
the creator list exposed the punishment and edit advice. Public readability and
activity association had therefore not established recommendation eligibility.

The installed guidance now calls for measured content-center checks in keyframes,
closing cards and covers; destination-specific review of body, visible sources,
subtitles and narration; and separate reporting of moderation and public-read
state. The Xiaohongshu reference routes to official rules and actual account
notices, keeps full provenance locally, and distinguishes neutral attribution from
outbound instructions. Replacing a video's media must be verified independently
from editing its text; neither an edit nor a prior successful post proves that a
restriction is lifted. The task's revised films and platform correction remain
separate work with their own review and confirmation.

A fresh-context application check with the revised installed skill correctly
calculated x540 versus x500 and caption center502.5, retained intentional left
alignment inside centered regions, reviewed outbound wording across text/visuals/
speech, preserved original note IDs, and required complete changed-version review
before an edit. It distinguished public readability from recommendation limits
and did not infer permission to repost or appeal. The 26 package/timeline tests
and official skill validator passed after the reference changes. This is selected
decision coverage, not a guarantee of platform moderation outcomes.

## Pronunciation, motion craft and disclosure

A fresh-context application check exercised three new cases:

| Case | Observed decision |
| --- | --- |
| “按行处理矩阵，可以并行运行。Router 为 MoE 选路。” with an accepted voice and acronym convention | Distinguished háng from xíng per occurrence, reused the voice and `M O E` convention, and treated identical ASR text as insufficient phonetic evidence; proposed real contextual clips without inventing listening or timestamps |
| New dimensional motion after flat keyframes had been accepted | Required spatial/material decisions and an encoded mechanism plus complete transition before full production; checked object identity, settling, protected text and planned occlusion |
| Silent, local-only film | Read the production references needed for that task, skipped audio and publication, and did not introduce a model API requirement |

Reference research covered three public henryz videos:
[KV cache](https://www.xiaohongshu.com/explore/6ade18130000000025006227),
[GPU execution](https://www.xiaohongshu.com/explore/6ad61594000000002803f2f7) and
[Groq](https://www.xiaohongshu.com/explore/6ad8b9b80000000031037691).
Searching the supplied rednote number matched this author; the profile endpoint
returned HTTP 406, so its redId field was not directly verified. Local inspection
consumed full-range 1 fps evidence and nine focused dense sequences: 89 contact
sheets, 1,020 sampled frames in total. Dense requests were 8 or 12 fps; actual
timestamps, rather than requested rates, define the evidence. This was sampled
visual inspection, without continuous native playback or audio listening.

The design guidance now distinguishes a restrained palette from flat construction:
depth must explain structure, transformations preserve object identity, effects
have a state/path consequence, and actions include readable settled states.
Inspection also found brief text overlaps in the references; their presence was
not adopted as a quality target. Exact easing curves or a universal spring style
were not inferred from samples. The small bundled 2D example remains a runtime
fixture rather than the production craft standard.

A separate disclosure audit kept pronunciation in the existing audio guide,
design decisions in art direction, and destination rules in their platform
adapter. The entrypoint was reduced from 490 to 309 whitespace-delimited words,
including frontmatter. These checks exercise routing and decisions, not a claim
that instruction changes alone establish the quality of a future film.

## Notation, preserved transitions and dimensionality

On 2026-10-27, user feedback identified unrendered small mathematical labels,
regressed transitions and unnecessary 3D in real films. This revision changes
instructions and adopted local preferences only; no film was regenerated or edited.

An independent review found and corrected overbroad wording that would have
forbidden intentional cuts or user-authorized dimensionality changes. Requirements
now have one owner: notation in storyboard, construction/motion in art direction,
runtime behavior in HyperFrames, and evidence/failure criteria in review.

Fresh-context bounded applications used a 12-second silent source, a bare
`d_model` SVG label, a separate `config.d_model` code panel, and an accepted token
path spanning a four-second scene boundary. The final portable-skill application,
without personal configuration, produced these observable decisions:

- Typeset the dimension label, preserve the literal code, and inventory every
  mathematical occurrence rather than trusting the correct large equation.
- Keep the accepted path, timing and easing across the scene boundary; leave
  actual smoothness unverified without the encoded sample and playback.
- Use 2D for data flow and for GPU/memory adjacency, since a top view preserves
  the required relationship; reserve 3D for a necessary unresolved spatial relation.
- Skip audio/publication references and operations for this silent local plan.

The baseline skill also produced several correct decisions; this is not a claimed
before/after failure-rate improvement. These were planning applications, not
rendering or playback tests. The 26 package/timeline tests, official skill validator
and Markdown diff checks passed; no new image, listening or motion-quality pass is
inferred from those checks.
