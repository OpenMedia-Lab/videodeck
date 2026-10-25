# videodeck implementation plan

The user approved the workflow on 2026-10-26 and asked to implement and publish
`OpenMedia-Lab/videodeck` with `master` as its default branch.

## Scope

An independently installable Agent Skill for source-grounded video production.
HyperFrames is the default animation renderer; caption-cli prepares local evidence
for agent review. Neither a paid model service nor a particular voice vendor is
required. Creative choices remain task-specific.

## Work and validation

- [ ] Observe baseline agent behavior for publishing and audio/polish pressure cases.
- [ ] Write a concise `videodeck/SKILL.md` and `agents/openai.yaml`, with stage-specific
  references for intake, storyboard, art direction, audio, HyperFrames, review and
  publishing. Preserve meaningful interactive answers and the separate final
  publication metadata confirmation.
- [ ] Implement one Python standard-library helper at
  `videodeck/scripts/timeline.py`: validate real timeline/caption intervals against
  the full master audio, and export canonical captions to SRT. Its JSON interface
  and behavior tests live alongside the helper/reference. It must not infer
  semantic correctness or manufacture approval.
- [ ] Supply one small, deterministic, runnable HyperFrames mechanism example,
  pinned dependencies, and a configurable monochrome technical profile.
- [ ] Test actual HyperFrames check/render → caption-cli evidence, inspect the
  output and record sampled coverage and unverified listening explicitly.
- [ ] Forward-test the finished skill with fresh agents on realistic scenarios;
  inspect their actual decisions and artifacts, correct demonstrated gaps.
- [ ] Validate packaging, relative references, script behavior and example build.
  Review the complete result independently, focusing on missing gates, audio loss,
  source fidelity, public portability and claims that exceed evidence.
- [ ] Publish MIT repository to the requested organization, verify CI/default
  branch/license, and install the discoverable skill without replacing other skills.

## File boundaries

Root agent owns skill instructions, documentation, packaging, CI and integration.
Tooling agent owns only `videodeck/scripts/timeline.py` and `tests/test_timeline.py`.
Rendering agent first works in `/private/tmp/videodeck-hyperframes-test`, then
provides the example under `videodeck/assets/example/` after interface alignment.
Tests and review records contain neutral scenarios, never private transcripts,
account state, reference voice recordings or third-party tutorial media.

## Reviewable invariants

Source terminology/formulas and accepted content survive adaptation. Voice choice
precedes final timing. New visual direction is reviewed through actual static
frames before full production. Master audio spans visual cuts intact. Captions
use canonical text; pronunciation aliases belong only to synthesis. Full-range
evidence preparation is distinguished from actual sampled agent review and
continuous listening. Final publishing metadata is displayed in full and actually
answered. Local output remains useful when credentials or model capabilities are
unavailable.
