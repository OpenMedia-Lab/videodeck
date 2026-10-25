import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const video = resolve(root, 'renders/expert-routing.mp4');
const fixture = await readFile(resolve(root, 'assets/continuity.wav'));
const rate = fixture.readUInt32LE(24), count = fixture.readUInt32LE(40) / 2;
const decoded = spawnSync('ffmpeg', ['-v', 'error', '-i', video, '-map', '0:a:0', '-ac', '1', '-ar', String(rate), '-f', 'f32le', 'pipe:1'], { maxBuffer: 8 * 1024 * 1024 });
if (decoded.status !== 0) throw new Error(decoded.stderr.toString());
const actual = decoded.stdout;
if (actual.length / 4 < count) throw new Error('Decoded audio is shorter than the complete generated fixture.');
function compare(label, start, end) {
  const a = Math.round(start * rate), b = Math.round(end * rate);
  let xx = 0, yy = 0, xy = 0, zeroSamples = 0;
  for (let i = a; i < b; i++) {
    const x = fixture.readInt16LE(44 + i * 2) / 32768, y = actual.readFloatLE(i * 4);
    xx += x * x; yy += y * y; xy += x * y;
    if (y === 0) zeroSamples++;
  }
  return { label, start, end, samples: b - a, sourceRms: Math.sqrt(xx / (b - a)), decodedRms: Math.sqrt(yy / (b - a)), correlation: xy / Math.sqrt(xx * yy), fittedGain: xy / xx, zeroSamples };
}
const comparisons = [compare('head', 0, .5), compare('transition-1', 3.55, 4.05), compare('transition-2', 7.45, 7.95), compare('tail', 11.9, 12.4), compare('whole-fixture', 0, 12.4)];
if (comparisons.some(x => x.correlation < .999 || x.decodedRms < .005)) throw new Error(`Audio fixture mismatch: ${JSON.stringify(comparisons)}`);
const report = { ok: true, signalOnlyNotListeningReview: true, sampleRate: rate, fixtureSamples: count, decodedSamplesIncludingAacPadding: actual.length / 4, paddingSamples: actual.length / 4 - count, comparisons, fixtureSha256: createHash('sha256').update(fixture).digest('hex'), renderSha256: createHash('sha256').update(await readFile(video)).digest('hex') };
await mkdir(resolve(root, '.hyperframes'), { recursive: true });
await writeFile(resolve(root, '.hyperframes/audio-verification.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
