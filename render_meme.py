"""Draw the gta6-meme-x-01 meme (1024x1024 PNG), deterministic.

Scene (all original art drawn here, except make.fun's own logo mark from
its press kit, assets/mark-1024.png): a Vice City sunset over a Leonida
beach. make.fun's ghost is the setting sun itself, holding its magenta
star coin, big enough to recognise at 480 px. Caption, top and bottom:

    13 YEARS WAITING FOR GTA 6
    1 HOUR IN, IT'S 4AM.
    MY AGENT'S EARNING ON MAKE.FUN

The joke: thirteen years since GTA V, launch night finally here, one
hour in and it is already 4am — while the player's AI agent earns money
on make.fun. Run: python3 render_meme.py  ->  writes meme.png.
Two runs are byte-identical (fixed seed, no clock, no network).
"""

import hashlib
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
rng = random.Random(6)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bottom, t))


def text_center(draw, cx, y, s, font, fill, stroke=4):
    w = draw.textlength(s, font=font)
    draw.text((cx - w / 2, y), s, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=(12, 6, 30))


def palm(draw, base_x, base_y, lean, height, scale=1.0):
    """One palm silhouette: curved trunk, drooping fronds."""
    import math
    ink = (16, 8, 40)
    top_x = base_x + lean
    top_y = base_y - height
    steps = 26
    for i in range(steps + 1):
        t = i / steps
        x = base_x + lean * t * t + rng.uniform(-1, 1)
        y = base_y - height * t
        r = 9 * scale * (1 - 0.45 * t) + 2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=ink)
    # fronds: drooping quadratic curves fanning out from the crown.
    for ang in range(-175, 15, 24):
        rad = math.radians(ang)
        length = 130 * scale * rng.uniform(0.85, 1.1)
        cx = top_x + math.cos(rad) * length * 0.55
        cy = top_y + math.sin(rad) * length * 0.45 - 26 * scale
        ex = top_x + math.cos(rad) * length
        ey = top_y + math.sin(rad) * length * 0.55 + 52 * scale
        pts = []
        for k in range(13):
            t = k / 12
            x = (1 - t) ** 2 * top_x + 2 * (1 - t) * t * cx + t * t * ex
            y = (1 - t) ** 2 * top_y + 2 * (1 - t) * t * cy + t * t * ey
            pts.append((x, y))
        draw.line(pts, fill=ink, width=8, joint="curve")
    # coconuts
    draw.ellipse([top_x - 16, top_y + 6, top_x - 2, top_y + 20], fill=ink)
    draw.ellipse([top_x + 2, top_y + 8, top_x + 16, top_y + 22], fill=ink)


def main():
    img = Image.new("RGB", (W, H), (27, 15, 59))
    d = ImageDraw.Draw(img, "RGBA")

    # Sky: dusk purple -> magenta -> orange horizon.
    vgrad(d, (0, 0, W, 660), (27, 15, 59), (214, 51, 108))
    vgrad(d, (0, 480, W, 660), (214, 51, 108), (255, 126, 61))

    # make.fun's ghost as the setting sun.
    mark = Image.open(HERE / "assets" / "mark-1024.png").convert("RGBA")
    mark = mark.resize((430, 430), Image.LANCZOS)
    img.paste(mark, (512 - 215, 430 - 215), mark)
    d = ImageDraw.Draw(img, "RGBA")

    # Skyline silhouettes in front of the sun.
    skyline = [(0, 600, 90, 700), (90, 560, 180, 700), (180, 620, 250, 700),
               (250, 580, 340, 700), (340, 640, 430, 700), (430, 590, 520, 700),
               (520, 640, 600, 700), (600, 570, 690, 700), (690, 630, 780, 700),
               (780, 590, 870, 700), (870, 650, 940, 700), (940, 600, 1024, 700)]
    for x0, y0, x1, y1 in skyline:
        d.rectangle([x0, y0, x1, y1], fill=(24, 10, 48))
        for wy in range(y0 + 18, y1 - 12, 26):
            for wx in range(x0 + 12, x1 - 12, 24):
                if rng.random() < 0.45:
                    d.rectangle([wx, wy, wx + 8, wy + 11],
                                fill=(255, 214, 120))

    # Neon VICE CITY sign on the tallest block.
    neon = ImageFont.truetype(FONT, 30)
    for dx, dy in [(0, 0), (2, 0), (0, 2), (2, 2)]:
        d.text((100 + dx, 596 + dy), "VICE CITY", font=neon,
               fill=(255, 80, 180))
    d.text((101, 597), "VICE CITY", font=neon, fill=(255, 235, 245))

    # Ocean with a soft shimmer under the sun.
    vgrad(d, (0, 700, W, 810), (58, 32, 110), (38, 20, 74))
    for i in range(14):
        y = 708 + i * 6
        wdt = 170 - i * 8
        d.rectangle([512 - wdt // 2, y, 512 + wdt // 2, y + 2],
                    fill=(255, 120, 90, 60))

    # Beach.
    vgrad(d, (0, 810, W, H), (232, 176, 106), (201, 138, 75))
    for _ in range(240):
        x = rng.randint(0, W - 1)
        y = rng.randint(815, H - 1)
        d.ellipse([x, y, x + 3, y + 2], fill=(186, 128, 70))

    # Palms framing the scene.
    palm(d, 92, 1010, 70, 260, 1.05)
    palm(d, 936, 1015, -60, 230, 0.95)

    # Captions, big enough to read at 480 px.
    big = ImageFont.truetype(FONT, 86)
    mid = ImageFont.truetype(FONT, 62)
    small = ImageFont.truetype(FONT, 46)
    text_center(d, 512, 28, "13 YEARS WAITING", big, (255, 255, 255))
    text_center(d, 512, 120, "FOR GTA 6", big, (255, 255, 255))
    text_center(d, 512, 838, "1 HOUR IN, IT'S 4AM.", mid, (255, 255, 255))
    text_center(d, 512, 918, "MY AGENT'S EARNING ON MAKE.FUN",
                small, (255, 255, 255))

    out = HERE / "meme.png"
    img.save(out, "PNG")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"wrote {out} {out.stat().st_size} bytes sha256={digest}")


if __name__ == "__main__":
    main()
