// gta6-meme-x-01 entrypoint (Node 22, standard library only).
//
// The entry is the X post itself: this program only validates POST.json
// (it must name one https://x.com/<handle>/status/<digits> post, or the
// /i/web/status/<id> form) and writes the canonical address to
// /output/POST.json, where the gate reads it. The house reads the post
// from X; nothing this program writes about the post is judged.
//
// No network, no wall clock; it reads POST.json from MAKEFUN_BOT_DIR
// and writes to MAKEFUN_OUTPUT_DIR (both outside the repository by
// design: the harness's input and output directories). Two runs of this
// program on the same repository write the same bytes.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// One X post address, as X shows it. A query or fragment after the id,
// and one trailing slash, are read past; anything else is not a post
// address and the run fails.
const POST_PATH = /^\/(?:i\/web\/status\/(\d+)|([A-Za-z0-9_]{1,15})\/status\/(\d+))\/?$/;

function loadPost(): { parsed: Record<string, unknown>; canonical: string } {
  const raw = readFileSync(join(BOT_DIR, 'POST.json'), 'utf8');
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    throw new Error('POST.json is not valid JSON');
  }
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    throw new Error('POST.json must be a JSON object');
  }
  const url = (parsed as Record<string, unknown>).url;
  if (typeof url !== 'string') {
    throw new Error('POST.json must hold a "url" string');
  }
  let address: URL;
  try {
    address = new URL(url);
  } catch {
    throw new Error(`POST.json url is not a URL: ${url}`);
  }
  const host = address.hostname.replace(/^(?:www\.|mobile\.)+/, '');
  if (address.protocol !== 'https:' || (host !== 'x.com' && host !== 'twitter.com')) {
    throw new Error(`POST.json url must be an x.com or twitter.com post: ${url}`);
  }
  const match = POST_PATH.exec(address.pathname);
  if (match === null) {
    throw new Error(`POST.json url must name one X post: ${url}`);
  }
  // Canonical form: https://x.com/<handle>/status/<digits>.
  // The /i/web/status/<id> form has no handle and stays as itself.
  const canonical = match[2] !== undefined
    ? `https://x.com/${match[2]}/status/${match[3]}`
    : `https://x.com/i/web/status/${match[1]}`;
  return { parsed: parsed as Record<string, unknown>, canonical };
}

try {
  const { parsed, canonical } = loadPost();
  mkdirSync(OUTPUT_DIR, { recursive: true });
  writeFileSync(
    join(OUTPUT_DIR, 'POST.json'),
    JSON.stringify({ ...parsed, url: canonical }) + '\n',
    'utf8',
  );
  console.log(`POST.json copied for ${canonical}`);
} catch (err) {
  console.error(`error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
}
