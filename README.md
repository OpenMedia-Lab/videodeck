<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="videodeck: a source-grounded workflow from an idea to a reviewed explanatory film" width="100%">
</p>

# videodeck

**Turn technical writing into an explanatory video with your coding agent.**

Keep the mechanism, equations and examples. Choose a voice, build deliberate
motion, and review the actual film before delivery. Works with Agent Skills-compatible
hosts; HyperFrames renders and [caption-cli](https://github.com/OpenMedia-Lab/caption-cli)
prepares local review evidence.

[Quick start](#quick-start) · [See it move](#see-it-move) · [Workflow](docs/workflow.md) · [Guide](docs/usage.md) · [中文](README_ZH.md)

[![CI](https://github.com/OpenMedia-Lab/videodeck/actions/workflows/validate.yml/badge.svg)](https://github.com/OpenMedia-Lab/videodeck/actions/workflows/validate.yml)
[![MIT](https://img.shields.io/badge/license-MIT-172321)](LICENSE)

## See it move

![Actual render: weighted Expert outputs travel into the equation](docs/assets/readme-demo.gif)

A six-second excerpt from the included [12.4-second runnable example](videodeck/assets/example/README.md).
The same weighted outputs become the terms in the equation. This fixture uses a
synthetic continuity tone; it is not a voiceover sample. [Reproduce the demo](docs/assets/README.md).

## Quick start

Install the inner skill directory in your host. For Codex:

```sh
git clone https://github.com/OpenMedia-Lab/videodeck.git
cd videodeck
mkdir -p "$HOME/.codex/skills"
videodeck_target="$HOME/.codex/skills/videodeck"
test ! -e "$videodeck_target" && test ! -L "$videodeck_target" &&
  ln -s "$PWD/videodeck" "$videodeck_target"
```

Already installed? Update the existing checkout. Other hosts use the same inner
`videodeck/` folder in their skill directory. [Installation and requirements](docs/usage.md#install).

Then give your agent a source and a destination:

> Use $videodeck to turn this article into a 90-second portrait explainer for
> engineers. Keep the equations and worked example. Reuse our accepted voice and
> transitions, and deliver a local video, cover and captions for review.

For your first film, supply the article, intended audience and platform or aspect
ratio. The skill resolves meaningful missing choices through concrete voice
samples, keyframes and motion proofs.

## From source to film

| Stage | What you get |
| --- | --- |
| Understand | Source-grounded outline, locked claims and an explanatory thread |
| Hear | An auditioned or reused voice, contextual pronunciation checks and one complete master |
| Design | Typeset math, clear 2D construction, justified local 3D and an independent cover |
| Animate | Audio-timed actions, preserved transitions and a seekable composition |
| Review | Actual encoded video, timestamped visual evidence and explicit listening limits |
| Deliver | MP4, cover, subtitles, editable sources and a review record |

No model API or paid video account is required by the skill. Your agent host and
chosen voice tools have their own requirements. Publication is optional and uses
confirmed final copy and settings. [Full workflow](docs/workflow.md).

## Choose your next step

| I want to… | Start here |
| --- | --- |
| Make or revise a film | [Skill entrypoint](videodeck/SKILL.md) |
| Try the renderer without a voice model | [Runnable HyperFrames example](videodeck/assets/example/README.md) |
| Keep a series' voice and style | [Project preferences](docs/usage.md) |
| Review generated media locally | [caption-cli](https://github.com/OpenMedia-Lab/caption-cli) |
| Publish after review | [Bilibili](videodeck/references/platforms/bilibili.md) · [Xiaohongshu](videodeck/references/platforms/xiaohongshu.md) |
| Check what was actually validated | [Validation record](docs/validation.md) |

## Contribute

Open an [issue](https://github.com/OpenMedia-Lab/videodeck/issues) with the source
context, expected behavior and a minimal reproducible case. Run
`python3 -m unittest discover -s tests -v` before submitting changes. Keep private
voice references, account state and source media outside the repository.

Part of [OpenMedia-Lab](https://github.com/OpenMedia-Lab), alongside
[postdeck](https://github.com/OpenMedia-Lab/postdeck) for social image cards.
[MIT](LICENSE); external runtimes, fonts and source media keep their own terms.
