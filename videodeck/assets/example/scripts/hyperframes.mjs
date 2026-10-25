import { spawnSync } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync } from 'node:fs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
// Keep every invocation on the installed version. Never npx-fetch at render.
const bin = resolve(root, 'node_modules/hyperframes/bin/hyperframes.mjs');
const browser = process.env.HYPERFRAMES_BROWSER_PATH
  || (existsSync('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : undefined);
const result = spawnSync(process.execPath, ['--import', resolve(root, 'scripts/offline-guard.mjs'), bin, ...process.argv.slice(2)], {
  cwd: root,
  stdio: 'inherit',
  env: {
    ...process.env,
    HYPERFRAMES_NO_UPDATE_CHECK: '1',
    HYPERFRAMES_NO_TELEMETRY: '1',
    DO_NOT_TRACK: '1',
    HYPERFRAMES_HISTORY_ROOT: resolve(root, '.hyperframes/history'),
    HYPERFRAMES_FONT_CACHE_DIR: resolve(root, '.hyperframes/fonts'),
    ...(browser ? { HYPERFRAMES_BROWSER_PATH: browser } : {}),
  },
});
if (result.error) throw result.error;
process.exit(result.status ?? 1);
