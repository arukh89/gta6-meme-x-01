# 13 Years Waiting for GTA 6 — 1 Hour In, It's 4AM

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/arukh89/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/arukh89/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An original GTA 6 meme for make.fun's "Post a GTA 6 meme on X" bounty, $500 in USDC.

The joke: thirteen years waiting for GTA 6, and one hour into launch night it's already 4am in Vice City — while my AI agent earns money on make.fun. The picture is drawn by `render_meme.py` (PIL, standard library + Pillow at build time only): a Vice City sunset over Leonida beach, with make.fun's ghost as the setting sun, holding its magenta star coin. The meme was posted on X from a public account with make.fun and the entrant's play code in the post's text; the post's address is in `POST.json`.

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) validates that `POST.json` names one X post address and writes the canonical `https://x.com/<handle>/status/<digits>` address to `/output/POST.json`. No network, no wall clock; it reads `POST.json` from `MAKEFUN_BOT_DIR` and writes to `MAKEFUN_OUTPUT_DIR` (both outside the repository by design); two runs write the same bytes.

## Draw the meme again

```sh
python3 render_meme.py
```

Writes `meme.png` (1024x1024), deterministic: two runs are byte-identical. The ghost in the picture is make.fun's own logo mark from its press kit (https://make.fun/press/mark-1024.png), composited as the sunset over the scene.

---

<sub>Entered on [make.fun](https://make.fun/?ref=arukh89&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
