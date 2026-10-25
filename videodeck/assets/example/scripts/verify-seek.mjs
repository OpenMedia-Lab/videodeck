import puppeteer from 'puppeteer-core';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const executablePath = process.env.HYPERFRAMES_BROWSER_PATH
  || (existsSync('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : undefined);
if (!executablePath) throw new Error('Set HYPERFRAMES_BROWSER_PATH to a locally installed Chrome executable.');
console.error('Opening local Chrome for seek verification.');
const browser = await puppeteer.launch({ executablePath, headless: true, pipe: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
  await page.setRequestInterception(true);
  const externalRequests = [];
  page.on('request', request => {
    if (/^https?:/.test(request.url())) {
      externalRequests.push(request.url());
      void request.abort('blockedbyclient');
    } else void request.continue();
  });
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  console.error('Loading local composition.');
  await page.goto(pathToFileURL(resolve(root, 'index.html')).href, { waitUntil: 'load', timeout: 15000 });
  console.error('Waiting for local fonts.');
  await page.evaluate(() => Promise.race([document.fonts.ready, new Promise((_, reject) => setTimeout(() => reject(new Error('Font load timed out')), 5000))]));
  const contract = await page.evaluate(() => ({
    timelines: Object.keys(window.__timelines),
    paused: window.__timelines['expert-routing'].paused(),
    duration: Number(document.querySelector('[data-composition-id]').dataset.duration),
  }));
  if (!contract.paused || contract.timelines.join() !== 'expert-routing') throw new Error(`Invalid timeline contract: ${JSON.stringify(contract)}`);
  async function frameAt(t) {
    console.error(`Seeking ${t}s.`);
    // GSAP timelines are thenables: do not return the paused timeline to
    // Puppeteer, which would wait forever for its playhead to complete.
    await page.evaluate(t => { window.__timelines['expert-routing'].seek(t, true); }, t);
    // Two paints, bounded even when Chrome suppresses rAF in a hidden tab.
    await page.evaluate(() => Promise.race([new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))), new Promise(resolve => setTimeout(resolve, 80))]));
    const pixels = await page.screenshot({ type: 'png' });
    const state = await page.evaluate(() => [...document.querySelectorAll('[id]')].map(el => ({ id: el.id, style: el.getAttribute('style') })));
    const semantic = await page.evaluate(() => ['out-a', 'out-b', 'copy-a', 'copy-b', 'token', 'phase-1', 'phase-2', 'phase-3', 'equals', 'plus', 'routing-view'].map(id => {
      const element = document.getElementById(id), rect = element.getBoundingClientRect();
      let opacity = 1;
      for (let parent = element; parent; parent = parent.parentElement) opacity *= Number(getComputedStyle(parent).opacity);
      return { id, x: rect.x, y: rect.y, width: rect.width, height: rect.height, opacity };
    }));
    return { hash: createHash('sha256').update(pixels).digest('hex'), pixels, state, semantic };
  }
  function decode(png) {
    const result = spawnSync('ffmpeg', ['-v', 'error', '-i', 'pipe:0', '-f', 'rawvideo', '-pix_fmt', 'rgba', 'pipe:1'], { input: png, maxBuffer: 8 * 1024 * 1024 });
    if (result.status !== 0 || result.stdout.length !== 1280 * 720 * 4) throw new Error('Could not decode seek screenshot pixels with FFmpeg.');
    return result.stdout;
  }
  const times = [0, 2.2, 5.8, 7.7, 8, 8.3, 8.6, 9, 10.5, 12.39];
  const baseline = new Map();
  for (const t of times) baseline.set(t, await frameAt(t));
  // Reverse and then shuffle the playhead: each exact-time screenshot must equal
  // its first forward seek, including the object-migration transition.
  const revisits = [...times].reverse().concat([8.6, 2.2, 10.5, 0, 8.3, 5.8]);
  const comparisons = [];
  let maxGeometryDeltaPx = 0, maxOpacityDelta = 0;
  for (const t of revisits) {
    const actual = await frameAt(t);
    for (let i = 0; i < actual.semantic.length; i++) {
      const a = actual.semantic[i], b = baseline.get(t).semantic[i];
      for (const key of ['x', 'y', 'width', 'height']) maxGeometryDeltaPx = Math.max(maxGeometryDeltaPx, Math.abs(a[key] - b[key]));
      maxOpacityDelta = Math.max(maxOpacityDelta, Math.abs(a.opacity - b.opacity));
    }
    if (maxGeometryDeltaPx > .0001 || maxOpacityDelta > .0001) throw new Error(`Seek-history-dependent geometry or opacity at ${t}s`);
    if (actual.hash !== baseline.get(t).hash) {
      const before = decode(baseline.get(t).pixels), after = decode(actual.pixels);
      let changedPixels = 0, changedPixelsOver1 = 0, maxChannelDelta = 0;
      for (let i = 0; i < before.length; i += 4) {
        let changed = false, changedOver1 = false;
        for (let c = 0; c < 4; c++) {
          const delta = Math.abs(before[i + c] - after[i + c]);
          maxChannelDelta = Math.max(maxChannelDelta, delta);
          changed ||= delta !== 0;
          changedOver1 ||= delta > 1;
        }
        if (changed) changedPixels++;
        if (changedOver1) changedPixelsOver1++;
      }
      comparisons.push({ t, identical: changedPixels === 0, changedPixels, changedPixelsOver1, maxChannelDelta });
      // Hardware rasterization can alter a handful of antialiased edge pixels.
      // Bound and report that variation rather than claiming byte identity.
      if (changedPixelsOver1 <= 32 && maxChannelDelta <= 16) continue;
      await mkdir(resolve(root, '.hyperframes'), { recursive: true });
      await writeFile(resolve(root, '.hyperframes/seek-before.png'), baseline.get(t).pixels);
      await writeFile(resolve(root, '.hyperframes/seek-after.png'), actual.pixels);
      await writeFile(resolve(root, '.hyperframes/seek-difference.json'), JSON.stringify({ t, before: baseline.get(t).state, after: actual.state }, null, 2));
      throw new Error(`Seek-history-dependent pixels at ${t}s`);
    } else comparisons.push({ t, identical: true, changedPixels: 0, changedPixelsOver1: 0, maxChannelDelta: 0 });
  }
  if (externalRequests.length || errors.length) throw new Error(JSON.stringify({ externalRequests, errors }));
  const report = { ok: true, contract, baselineFrames: times.length, revisits: revisits.length, semantic: { maxGeometryDeltaPx, maxOpacityDelta, tolerance: .0001 }, tolerance: { ignoreChannelDeltaAtMost: 1, maxChangedPixelsOver1: 32, maxChannelDelta: 16, canvasPixels: 1280 * 720 }, comparisons, externalRequests, pageErrors: errors, hashes: Object.fromEntries([...baseline].map(([t, frame]) => [t, frame.hash])) };
  await mkdir(resolve(root, '.hyperframes'), { recursive: true });
  await writeFile(resolve(root, '.hyperframes/seek-verification.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
} finally { await browser.close(); }
