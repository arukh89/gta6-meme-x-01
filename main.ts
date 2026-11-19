// gta6-meme-x-01 entrypoint (Node 22, standard library only).
//
// The entry is the X post itself: this program only validates POST.json
// (it must name one https://x.com/<handle>/status/<digits> post, or the
// /i/web/status/<id> form) and copies it to /output/POST.json, where the
// gate reads it. The house reads the post from X; nothing this program
// writes about the post is judged.
//
// No network, no wall clock, no files outside the repository; two runs
// of this program on the same repository write the same bytes.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// One X post address, as X shows it. A query or fragment after the id is
// read past; anything else is not a post address and the run fails.
const POST_PATH = /^\/(?:i\/web\/status\/\d+|[A-Za-z0-9_]{1,15}\/status\/\d+)$/;

function loadPostUrl(): string {
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
  const host = address.hostname.replace(/^(www\.|mobile\.)/, '');
  if (address.protocol !== 'https:' || (host !== 'x.com' && host !== 'twitter.com')) {
    throw new Error(`POST.json url must be an x.com or twitter.com post: ${url}`);
  }
  if (!POST_PATH.test(address.pathname)) {
    throw new Error(`POST.json url must name one X post: ${url}`);
  }
  return url;
}

const url = loadPostUrl();
mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
console.log(`POST.json copied for ${url}`);
