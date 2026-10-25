// Fail on accidental compiler-side CDN, font, API, telemetry or update requests.
// Loopback HTTP/WebSocket communication with local Chrome remains available.
import http from 'node:http';
import https from 'node:https';
import { syncBuiltinESMExports } from 'node:module';

const local = new Set(['localhost', '127.0.0.1', '::1', '[::1]']);
function assertLocal(input) {
  if (input?.socketPath) return;
  let host;
  if (typeof input === 'string' || input instanceof URL) {
    const url = new URL(input);
    if (!['http:', 'https:'].includes(url.protocol)) return;
    host = url.hostname;
  } else {
    host = input?.hostname ?? (input?.host ? new URL(`http://${input.host}`).hostname : 'localhost');
  }
  if (!local.has(host)) throw new Error(`Offline example blocked remote request to ${host}. Install dependencies/browser before rendering.`);
}
const fetchOriginal = globalThis.fetch;
globalThis.fetch = function (input, ...rest) {
  assertLocal(input instanceof Request ? input.url : input);
  return fetchOriginal.call(this, input, ...rest);
};
for (const transport of [http, https]) {
  for (const name of ['request', 'get']) {
    const original = transport[name];
    transport[name] = function (input, ...rest) {
      assertLocal(input);
      return original.call(this, input, ...rest);
    };
  }
}
syncBuiltinESMExports();
