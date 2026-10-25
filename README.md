# videodeck

[中文](README_ZH.md) · [Workflow](docs/workflow.md) · [Validation](docs/validation.md)

An Agent Skill for making explanatory videos from articles, project materials and
scripts. It combines source-grounded storytelling, deliberate motion, consistent
audio and evidence-based agent review. Companion to
[postdeck](https://github.com/OpenMedia-Lab/postdeck).

**HyperFrames renders. caption-cli prepares local evidence. The agent reviews.**
The skill requires no third-party model API, cloud account or paid video service.
Voice generation and optional local ASR use the tools you choose. Agent hosting,
optional models and destination services have their own requirements.

## Install

Clone the repository, then link the inner skill folder into Codex's skills directory
(the link command deliberately fails if an installation already exists):

```bash
git clone https://github.com/OpenMedia-Lab/videodeck.git
mkdir -p "$HOME/.codex/skills"
videodeck_target="$HOME/.codex/skills/videodeck"
test ! -e "$videodeck_target" && test ! -L "$videodeck_target" &&
  ln -s "$PWD/videodeck/videodeck" "$videodeck_target"
```

For other Agent Skills-compatible hosts, install the same inner `videodeck/` folder
in that host's skill directory. Cross-runtime hosts may support `~/.agents/skills`.
No other skill is required. Automatic discovery is enabled by default.

Example request:

> Use $videodeck to explain this article to engineers in a landscape video.
> Reuse our accepted visual direction and voice, keep the equations, and deliver locally.

The skill asks only for consequential missing choices. New voices get actual
auditions; a new visual direction gets coded static frames before full production.
Requested platform publication has a separate confirmation of complete final copy.

Record adopted series/voice preferences in project or installed-skill
`videodeck.local.json`; these ignored files can hold private reference paths.
Task answers take priority over standing settings.

## Tools

| Tool | Role |
| --- | --- |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Deterministic HTML/SVG/GSAP composition and rendering |
| [caption-cli](https://github.com/OpenMedia-Lab/caption-cli) | Local timestamped sheets, audio and review tasks; no inference API |
| FFmpeg / ffprobe | Media preparation, decoding and integrity checks |
| User-selected voice tools | Auditions, stable narration, optional music/effects |
| Source/platform CLI | Acquire references or perform confirmed publication |

Python 3.10+ runs the bundled timeline helper without Python dependencies. The
[small example](videodeck/assets/example/README.md) pins a tested HyperFrames runtime
and Node requirement; it is a technical starting point, not a universal style.

```bash
python3 -m unittest discover -s tests -v
python3 videodeck/scripts/timeline.py check /path/to/timeline.json
python3 videodeck/scripts/timeline.py srt /path/to/timeline.json --out /path/to/captions.srt
```

## What is included

The [concise entrypoint](videodeck/SKILL.md) routes to focused references for intake,
storyboarding, art direction, sound, rendering, review and publication. A small
timeline validator protects interval/audio boundaries and exports canonical SRT;
it does not certify technical accuracy, aesthetics, listening quality or consent.
An opt-in profile demonstrates monochrome technical art direction without imposing
private series settings or a particular voice model on other users.

Full-range contact sheets are sampled evidence, not continuous video understanding.
Review records distinguish actual inspection, ASR, waveform checks and listening
limitations. See the [test evidence](docs/validation.md) for the current boundaries.

MIT. Third-party runtimes, fonts, voice references and source media retain their
own terms; they are not bundled into this skill.
