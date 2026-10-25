# HyperFrames mechanism example

A 12.4-second, 1280×720 explanation: one token is routed to two experts, then the
**same two weighted output objects** move into the equation
`y = 0.7 E₁(x) + 0.3 E₂(x)`. These are illustrative normalized weights, not a
claim that every mixture-of-experts implementation uses this exact router.
Mathematics uses rendered native HTML with subscripts, not raw TeX.

The source has one synchronously constructed, paused GSAP timeline registered as
`window.__timelines['expert-routing']`. No animation callback, timer, random
number, autoplay, remote image, or cloud generation drives the composition.

## Reproduce

Requires Node.js >=22.12.0, npm, FFmpeg/FFprobe, and local Chrome. Exact dependencies
are pinned in `package-lock.json`: HyperFrames 0.8.198, GSAP 3.14.2, two Fontsource
5.3.0 packages, and Puppeteer Core 25.16.0 for seek verification.

```sh
npm ci
npm run prepare
npm run lint
npm run check -- --strict
npm run verify:seek
npm run snapshot
npm run render
npm run verify:audio
```

`npm ci` also runs the `prepare` lifecycle; the explicit prepare command is safe
to repeat. It generates `assets/continuity.wav` from a fixed mathematical signal.
The quiet synthetic tone tests audio continuity only. It is not speech or an
auditioned voiceover. No ASR, TTS model, API key, or third-party service is needed.

Set `HYPERFRAMES_BROWSER_PATH` to your Chrome executable if needed. The wrapper
detects a standard macOS Chrome installation. On Linux, for example:

```sh
export HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome
npm run check -- --strict
npm run verify:seek
npm run render
```

If Chrome is absent, install it during preparation, before the offline commands:

```sh
HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 node node_modules/hyperframes/bin/hyperframes.mjs browser ensure
HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 node node_modules/hyperframes/bin/hyperframes.mjs browser path
```

Use the printed path as `HYPERFRAMES_BROWSER_PATH`. Preparation may need network
access for npm and the browser download. The render wrapper uses the installed
CLI, disables updates/telemetry, stores history/fonts within `.hyperframes/`, and
rejects Node-side non-loopback HTTP/fetch requests. The seek test also rejects
page-level HTTP/HTTPS resources. This is not a system-wide network firewall.

## Local fonts matter in 0.8.198

During the actual first render, generic primary `sans-serif` and `serif` families
were silently rewritten to Inter and the compiler fetched Google Fonts. This
example avoids that behavior: explicit `Video Sans`/`Video Math` aliases have
local `@font-face` sources under the locked Fontsource packages. GSAP is also
loaded from `node_modules`; no CDN is involved. IBM Plex Sans and Libre
Baskerville are open fonts; their licenses are included in the npm packages.

The current CLI uses **lint + check**. `validate`, `inspect`, and `layout` are
deprecated aliases. `check` only runs the motion gate when a `*.motion.json`
sidecar exists. This example includes 11 assertions in `index.motion.json` for
arrival times, order, staying within the frame, and diagram liveness.

## Verification and limits

The example was really rendered on macOS arm64 using Node 22.23.3, FFmpeg 7.1.1,
Chrome 155.0.8059.86, and HyperFrames 0.8.198. The final strict check passed:
104 layout samples, 249 motion samples, 53/53 contrast checks, and 100 craft
samples, with no errors or warnings. Initial checks caught and fixed token boxes
covering expert labels, overlapping transition text, and an empty first frame.

`verify:seek` compares ten forward positions with sixteen reverse/shuffled
revisits, including the object migration. It verifies key object geometry and
effective opacity within 0.0001, rejects JS errors/remote page requests, and
quantifies screenshot differences. Hardware antialiasing can change a few edge
pixels: the test ignores channel differences <=1, permits at most 32 pixels with
a larger difference, and caps every channel difference at 16/255. It records
actual comparisons in `.hyperframes/seek-verification.json`; it does not claim
byte-identical output across browsers, GPUs, operating systems, or FFmpeg builds.

For machine-readable check output without npm's banner:

```sh
node scripts/hyperframes.mjs check --samples 15 --at-transitions --strict --json > check.json
```

Actual MP4 review used `caption-cli 0.1.0` at 1 fps over the full video and 6 fps
over 7.5–9.5 seconds. All prepared contact sheets were visually opened. AAC audio
was present for the full 12.4 seconds; signal comparisons around both transitions
correlated >0.9999 with the continuous generated fixture, with no zero samples
in those windows. `verify:audio` also compares the first and final 0.5 seconds and
the whole fixture, reports source/decoded energy and fitted gain, and checks that
all 595,200 source samples are retained. Decoding may expose 768 extra samples
(16 ms) of AAC padding beyond the container's 12.4-second duration. This is
signal validation, not listening or speech review. The measured fitted gain was
about 1.413 in this pipeline; waveform correlation does not claim lossless
amplitude preservation.
The preparation packet itself retains `prepared` status; it does not certify a
semantic review or every rendered frame.

```sh
caption-cli video-read --file renders/expert-routing.mp4 --out review --fps 1 --frame-width 640
caption-cli video-read --file renders/expert-routing.mp4 --out review-transition --fps 6 --start 7.5 --end 9.5 --frame-width 640
```

Generated audio/video, dependency folders, caches, snapshots, and review packets
are excluded from the repository. Run the commands to create your own artifacts.
