#!/usr/bin/env python3
"""news-image-20261121: one image summing up the world's news of
Saturday 21 November 2026. Python 3.13 standard library only.
Writes /output/entry.png (1024x1024, deterministic)."""
import os
import struct
import zlib

W, H = 1024, 1024

# --- 5x5 bitmap font: each glyph is 5 rows, each row a 5-bit int ---
FONT = {
    'A': (0x0E, 0x11, 0x1F, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x1E, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x1E, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x1E, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x13, 0x0F),
    'H': (0x11, 0x11, 0x1F, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x1C, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x11, 0x11),
}
FONT.update({
    'N': (0x11, 0x19, 0x15, 0x13, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x1E, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x1E, 0x12, 0x11),
    'S': (0x0F, 0x10, 0x0E, 0x01, 0x1E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x15, 0x1B, 0x11),
    'X': (0x11, 0x0A, 0x04, 0x0A, 0x11),
    'Y': (0x11, 0x0A, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x02, 0x04, 0x08, 0x1F),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x02, 0x04, 0x1F),
    '3': (0x1F, 0x02, 0x0E, 0x02, 0x1F),
    '4': (0x02, 0x06, 0x0A, 0x1F, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x1E),
    '6': (0x0E, 0x10, 0x1E, 0x11, 0x0E),
    '7': (0x1F, 0x02, 0x04, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x0E, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x0F, 0x01, 0x0E),
    ' ': (0, 0, 0, 0, 0),
    '.': (0, 0, 0, 0, 0x04),
    ',': (0, 0, 0, 0x04, 0x08),
    ':': (0, 0x04, 0, 0x04, 0),
    ';': (0, 0x04, 0, 0x04, 0x08),
    "'": (0x04, 0x04, 0, 0, 0),
    '-': (0, 0, 0x1F, 0, 0),
    '/': (0x01, 0x02, 0x04, 0x08, 0x10),
    '(': (0x02, 0x04, 0x04, 0x04, 0x02),
    ')': (0x08, 0x04, 0x04, 0x04, 0x08),
    '%': (0x19, 0x02, 0x04, 0x08, 0x13),
    '$': (0x04, 0x0F, 0x14, 0x1E, 0x04),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15),
    '!': (0x04, 0x04, 0x04, 0, 0x04),
    '?': (0x0E, 0x11, 0x02, 0, 0x04),
    '+': (0, 0x04, 0x0E, 0x04, 0),
    '=': (0, 0x1F, 0, 0x1F, 0),
    '"': (0x0A, 0x0A, 0, 0, 0),
})

# --- pixel buffer (RGB) ---
buf = bytearray(W * H * 3)


def px(x, y, rgb):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = rgb


def fill_rect(x, y, w, h, rgb):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        base = yy * W * 3
        for xx in range(x0, x1):
            i = base + xx * 3
            buf[i], buf[i + 1], buf[i + 2] = rgb


def rect_outline(x, y, w, h, rgb, t=1):
    fill_rect(x, y, w, t, rgb)
    fill_rect(x, y + h - t, w, t, rgb)
    fill_rect(x, y, t, h, rgb)
    fill_rect(x + w - t, y, t, h, rgb)


def line(x0, y0, x1, y1, rgb, t=1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        fill_rect(x0, y0, t, t, rgb)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def circle(cx, cy, r, rgb):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                px(xx, yy, rgb)


def triangle(x0, y0, x1, y1, x2, y2, rgb):
    # filled triangle via scanline fill
    pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts
    for y in range(ay, cy + 1):
        if y < by:
            t = (y - ay) / max(1, by - ay)
            xa = ax + (bx - ax) * t
        else:
            t = (y - by) / max(1, cy - by)
            xa = bx + (cx - bx) * t
        t2 = (y - ay) / max(1, cy - ay)
        xb = ax + (cx - ax) * t2
        for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
            px(x, y, rgb)

# --- text ---
def char_w(scale):
    return 6 * scale


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_char(ch, x, y, scale, rgb):
    g = FONT.get(ch.upper(), FONT['?'])
    for r in range(5):
        row = g[r]
        for c in range(5):
            if row & (1 << (4 - c)):
                fill_rect(x + c * scale, y + r * scale, scale, scale, rgb)


def draw_text(s, x, y, scale, rgb):
    for ch in s:
        draw_char(ch, x, y, scale, rgb)
        x += 6 * scale


def wrap_text(s, scale, max_w):
    """Greedy word wrap; returns list of lines fitting max_w pixels."""
    words = s.split(' ')
    lines, cur = [], ''
    for wd in words:
        cand = wd if not cur else cur + ' ' + wd
        if text_w(cand, scale) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_lines(lines, x, y, scale, rgb, leading):
    for ln in lines:
        draw_text(ln, x, y, scale, rgb)
        y += leading
    return y

# --- PNG encoder (filter 0, zlib) ---
def chunk(typ, data):
    out = struct.pack('>I', len(data)) + typ + data
    out += struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 6))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)

# --- palette ---
INK = (26, 26, 26)
PAPER = (245, 240, 230)
NAVY = (20, 38, 63)
RED = (178, 34, 34)
CARD = (255, 255, 255)
BORDER = (216, 208, 192)
GRAY = (90, 90, 90)
WHITE = (255, 255, 255)

# --- stories: all verified as Saturday 21 November 2026 news ---
# Sources: oneturn.news/day/2026-11-21, virginiatimesnow.com daily recap,
# medium.com strategic brief 21 Nov 2026, ubstandard.com world.
STORIES = [
    ("CONFLICT", "BAHRAIN", (178, 34, 34),
     "IRAN STRIKES US BASES IN BAHRAIN",
     "Tehran says it hit two US bases; Bahrain reports a fire at a civilian site, no injuries."),
    ("WAR", "UKRAINE", (120, 40, 20),
     "RUSSIAN MISSILE HITS KRYVYI RIH",
     "Strike on Zelensky's hometown kills two, a paramedic and a boy of 7; missiles also land in Poland."),
    ("JUSTICE", "MEXICO", (30, 80, 140),
     "MEXICO CAPTURES CARTEL BOSS",
     "FBI most-wanted Fausto Isidro Meza Flores seized in Sinaloa; clashes leave at least 11 dead."),
    ("MARKETS", "NEW YORK", (20, 100, 60),
     "NASDAQ PLUNGES 5.3% IN AI SELLOFF",
     "US stocks fall into correction as the AI sell-off caps the worst week since 2020."),
    ("CLIMATE", "TURKEY", (40, 120, 110),
     "COP31 TALKS PAST DEADLINE",
     "UN climate summit in Antalya goes into overtime with no agreement on fossil fuels."),
    ("CULTURE", "GAMES", (140, 40, 140),
     "GTA VI SELLS $2.36 BILLION ON DAY ONE",
     "An estimated 24.6 million copies sold on launch day, a record for the games industry."),
]


def draw_icon(kind, x, y, s, fg):
    """Small pictogram inside a s x s box at (x, y), drawn in fg."""
    if kind == "CONFLICT":  # burst + missile
        cx, cy = x + s // 2, y + s // 2
        for ang in range(0, 360, 45):
            import math
            r1 = s // 5
            r2 = s // 2 - 2
            a = math.radians(ang)
            line(cx + int(r1 * math.cos(a)), cy + int(r1 * math.sin(a)),
                 cx + int(r2 * math.cos(a)), cy + int(r2 * math.sin(a)), fg, 3)
        circle(cx, cy, s // 6, fg)
    elif kind == "WAR":  # building with a crack
        fill_rect(x + s // 4, y + s // 5, s // 2, s * 3 // 5, fg)
        fill_rect(x + s // 4, y + s // 5 - 4, s // 2, 6, fg)
        line(x + s // 2, y + s // 5, x + s // 2 - 6, y + s // 2,
             PAPER, 2)
        line(x + s // 2 - 6, y + s // 2, x + s // 2 + 6, y + s * 3 // 4,
             PAPER, 2)
    elif kind == "JUSTICE":  # shield
        fill_rect(x + s // 4, y + s // 6, s // 2, s // 2, fg)
        triangle(x + s // 4, y + s // 6 + s // 2, x + s * 3 // 4,
                 y + s // 6 + s // 2, x + s // 2, y + s - s // 8, fg)
        circle(x + s // 2, y + s // 3, s // 8, PAPER)
    elif kind == "MARKETS":  # falling chart
        pts = [(x + 4, y + s // 4), (x + s // 3, y + s // 3),
               (x + s // 2, y + s // 2), (x + s * 2 // 3, y + s * 2 // 3),
               (x + s - 6, y + s - 8)]
        for a, b in zip(pts, pts[1:]):
            line(a[0], a[1], b[0], b[1], fg, 4)
        triangle(x + s - 14, y + s - 14, x + s - 4, y + s - 14,
                 x + s - 9, y + s - 4, fg)
    elif kind == "CLIMATE":  # globe
        circle(x + s // 2, y + s // 2, s // 2 - 3, fg)
        line(x + 4, y + s // 2, x + s - 4, y + s // 2, PAPER, 2)
        line(x + 4, y + s // 3, x + s - 4, y + s // 3, PAPER, 2)
        line(x + 4, y + s * 2 // 3, x + s - 4, y + s * 2 // 3, PAPER, 2)
    else:  # CULTURE: game controller
        fill_rect(x + s // 6, y + s // 3, s * 2 // 3, s // 3, fg)
        circle(x + s // 6, y + s // 2, s // 8, fg)
        circle(x + s * 5 // 6, y + s // 2, s // 8, fg)
        circle(x + s * 2 // 3, y + s // 3 + 6, 3, PAPER)
        circle(x + s * 2 // 3 + 10, y + s // 3 + 12, 3, PAPER)

# --- layout ---
def draw_card(x, y, w, h, story):
    tag, place, color, headline, deck = story
    fill_rect(x, y, w, h, CARD)
    rect_outline(x, y, w, h, BORDER, 2)
    # tag chip
    chip = tag + " - " + place
    cw = text_w(chip, 2) + 16
    fill_rect(x + 18, y + 16, cw, 26, color)
    draw_text(chip, x + 26, y + 21, 2, WHITE)
    # icon box top-right
    ib = 56
    fill_rect(x + w - 18 - ib, y + 16, ib, ib, color)
    draw_icon(tag, x + w - 18 - ib, y + 16, ib, WHITE)
    # headline (2 lines max)
    hl = wrap_text(headline, 4, w - 36)[:2]
    yy = draw_lines(hl, x + 18, y + 92, 4, INK, 26)
    # deck (3 lines max)
    dk = wrap_text(deck, 2, w - 36)[:3]
    draw_lines(dk, x + 18, yy + 10, 2, GRAY, 16)


def draw():
    fill_rect(0, 0, W, H, PAPER)
    # header band
    fill_rect(0, 0, W, 150, NAVY)
    draw_text("SATURDAY", 24, 18, 3, (200, 210, 225))
    draw_text("21 NOVEMBER 2026", 24, 48, 6, WHITE)
    draw_text("THE WORLD IN ONE DAY", 24, 112, 3, (200, 210, 225))
    fill_rect(0, 150, W, 6, RED)
    # grid 2x3
    gx, gy = 24, 172
    cw, chh, gap = 480, 253, 16
    for i, st in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (chh + gap)
        draw_card(cx, cy, cw, chh, st)
    # footer
    fill_rect(0, H - 44, W, 44, NAVY)
    foot = "WORLD NEWS - 21 NOVEMBER 2026 - MAKE.FUN"
    draw_text(foot, (W - text_w(foot, 2)) // 2, H - 34, 2, WHITE)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    draw()
    path = os.path.join(out_dir, "entry.png")
    n = write_png(path)
    print(f"wrote {path} ({n} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
