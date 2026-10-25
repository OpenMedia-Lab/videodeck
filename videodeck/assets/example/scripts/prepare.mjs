import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

// A reproducible, quiet synthetic continuity fixture. This is NOT speech,
// music, or an auditioned voiceover. No model, API, network or private recording.
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const seconds = 12.4;
const rate = 48000;
const count = Math.round(seconds * rate);
const data = Buffer.alloc(count * 2);
for (let i = 0; i < count; i++) {
  const t = i / rate;
  const envelope = Math.min(1, t / .2, (seconds - t) / .2);
  const sample = .025 * envelope * (Math.sin(2 * Math.PI * 220 * t) + .35 * Math.sin(2 * Math.PI * 330 * t));
  data.writeInt16LE(Math.round(32767 * sample), i * 2);
}
const header = Buffer.alloc(44);
header.write('RIFF'); header.writeUInt32LE(36 + data.length, 4); header.write('WAVE', 8);
header.write('fmt ', 12); header.writeUInt32LE(16, 16); header.writeUInt16LE(1, 20);
header.writeUInt16LE(1, 22); header.writeUInt32LE(rate, 24); header.writeUInt32LE(rate * 2, 28);
header.writeUInt16LE(2, 32); header.writeUInt16LE(16, 34);
header.write('data', 36); header.writeUInt32LE(data.length, 40);
await mkdir(resolve(root, 'assets'), { recursive: true });
await writeFile(resolve(root, 'assets/continuity.wav'), Buffer.concat([header, data]));
console.log(`Generated assets/continuity.wav: ${seconds}s, ${rate}Hz mono PCM; synthetic continuity test only.`);
