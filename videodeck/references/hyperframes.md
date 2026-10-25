# HyperFrames production

Check `hyperframes --version` and `--help` (or a project-local pinned executable)
before choosing commands. Verify current official docs when extending a composition:
[CLI](https://hyperframes.heygen.com/packages/cli),
[determinism](https://hyperframes.heygen.com/concepts/determinism),
[source](https://github.com/heygen-com/hyperframes).
Prefer a lockfile and project-local runtime over a rolling global install.

The small [runnable example](../assets/example/README.md) demonstrates a seekable
mechanism and an audio track crossing visual changes. Adapt its technical contract;
its layout is not a mandatory visual template.

Use a composition root with explicit id, duration and dimensions. Register a paused
GSAP timeline in `window.__timelines[compositionId]`; motion must be a deterministic
function of composition time and support seeking backward as well as forward.
Use stable assets and seed any procedural randomness. Load local bundled assets;
avoid runtime network, wall clocks and uncontrolled event loops. Canvas/WebGL is
acceptable when equally deterministic and seekable.

The composition's media timing and animation timeline must agree. Put the complete
master audio on its own track with explicit start/duration. Never inherit a shot's
cropping window for continuous narration. Keep text/subtitle cues tied to acoustic
anchors. Pre-render math to SVG or finish math DOM layout before capture.

Run supported structural/layout/motion checks, then render the actual deliverable.
Some versions offer unified `check --json`; others expose `lint`, `validate` and
`inspect`. Check installed help; do not invent a command or assume old validators
are equivalent. Read and resolve findings; checks cannot certify narrative,
pronunciation, audio tails or visual quality. Continue with [review](review.md).

Framework TTS is optional. A built-in voice model does not supersede an accepted
external/local voice. No vendored full framework docs or paid service is needed.

Tested example: HyperFrames 0.8.198, GSAP 3.14.2, Node 22.12.0+. Use `lint` plus `check`
for this version. Its compiler can rewrite generic `sans-serif`/`serif` to a web
font and fetch it during compilation. The example uses npm-locked local font files
under an explicit `@font-face` alias and rejects outbound HTTP during commands;
dependency/browser preparation is a separate, potentially networked step.
In 0.8.198 motion assertions come from an `index.motion.json` sidecar, not a
`--motion` switch. The example supplies one. A disabled motion section with empty
findings is untested; inspect `enabled` and sample counts in the actual report.
