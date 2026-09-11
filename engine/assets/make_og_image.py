# -*- coding: utf-8 -*-
"""Generate docs/og-image.png (1200x630) with zero dependencies.

Ocean-blue gradient + layered waves + pixel wordmark, rendered at 3x
supersampling and box-downsampled for smooth edges. Run once, commit the
resulting PNG; build.py just copies it into the site root.

Usage:  python engine/assets/make_og_image.py
"""

import math
import os
import struct
import zlib

W, H, SS = 1200, 630, 3  # final size and supersample factor
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og-image.png")

# 5x7 pixel font, one string per glyph row ('X' = ink)
FONT = {
    "T": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "..X.."],
    "o": [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "l": ["..X..", "..X..", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "i": [".X...", ".....", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "d": ["....X", "....X", "X...X", "X...X", "X...X", "X...X", ".XXXX"],
    "e": [".XXX.", "X...X", "X...X", "XXXXX", "X....", "X....", ".XXXX"],
    "t": ["...X.", "...X.", "XXXXX", "...X.", "...X.", "...X.", "..XX."],
    "F": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "X...."],
    "r": [".....", "X.XX.", "XX..X", "X....", "X....", "X....", "X...."],
    "n": [".....", "X.XX.", "XX..X", "X...X", "X...X", "X...X", "X...X"],
    "s": [".XXXX", "X....", "X....", ".XXX.", "....X", "....X", "XXXX."],
}
GW, GH = 5, 7  # glyph cell in font pixels


def hexc(s):
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


TOP, BOT = hexc("0e7490"), hexc("164e63")          # cyan-700 -> cyan-900
WAVES = [(hexc("67e8f9"), 0.22), (hexc("22d3ee"), 0.30), (hexc("155e75"), 0.45)]

big = bytearray(3 * W * SS * H * SS)               # supersampled canvas


def put(x, y, rgb):
    i = 3 * (y * W * SS + x)
    big[i:i + 3] = bytes(rgb)


def blend(x, y, rgb, a):
    i = 3 * (y * W * SS + x)
    for k in range(3):
        big[i + k] = int(big[i + k] * (1 - a) + rgb[k] * a)


for y in range(H * SS):                            # gradient backdrop
    t = y / (H * SS - 1)
    row = tuple(int(TOP[k] + (BOT[k] - TOP[k]) * t) for k in range(3))
    for x in range(W * SS):
        put(x, y, row)

for idx, (col, op) in enumerate(WAVES):            # layered sine waves, bottom third
    base = int(H * SS * (0.74 + 0.07 * idx))
    amp = (H * SS) * (0.020 - 0.004 * idx)
    freq = 2 * math.pi / (W * SS) * (1.6 + 0.5 * idx)
    phase = idx * 2.1
    cols = [col if (x // 2) % 2 == 0 else tuple(min(255, c + 14) for c in col)
            for x in range(0, W * SS, 2)]          # cheap two-tone stripe texture
    for x in range(W * SS):
        wy = base + int(amp * math.sin(x * freq + phase) + amp * 0.5 * math.sin(x * freq * 2.7 + phase * 1.3))
        cc = cols[x // 2 if x // 2 < len(cols) else -1]
        for y in range(wy, H * SS):
            blend(x, y, cc, op)


def draw_text(text, scale, left, top):
    for ci, ch in enumerate(text):
        glyph = FONT.get(ch)
        if not glyph:
            continue
        for ry, rowbits in enumerate(glyph):
            for rx, cell in enumerate(rowbits):
                if cell != "X":
                    continue
                for dy in range(scale):
                    yy = top + (ry * scale + dy)
                    for dx in range(scale):
                        blend(left + (ci * (GW + 1) * scale) + rx * scale + dx, yy,
                              (255, 255, 255), 1.0)


def text_w(text, scale):
    return len(text) * (GW + 1) * scale - scale


word, wtag = "ToolTide", "Free online tools"
sw = SS * 13                                       # wordmark scale (supersampled px)
tw = SS * 4                                        # tagline scale
draw_text(word, sw, (W * SS - text_w(word, sw)) // 2, int(H * SS * 0.16))
draw_text(wtag, tw, (W * SS - text_w(wtag, tw)) // 2, int(H * SS * 0.16) + GH * sw + SS * 14)

# box-downsample SSxSS -> one pixel
out = bytearray()
for y in range(H):
    out.append(0)                                  # PNG filter type 0
    for x in range(W):
        acc = [0, 0, 0]
        for dy in range(SS):
            for dx in range(SS):
                i = 3 * ((y * SS + dy) * W * SS + x * SS + dx)
                for k in range(3):
                    acc[k] += big[i + k]
        out += bytes(a // (SS * SS) for a in acc)


def png_chunk(tag, data):
    c = struct.pack(">I", len(data)) + tag + data
    return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)  # 8-bit RGB
body = b"".join(png_chunk(t, d) for t, d in [
    (b"IHDR", ihdr),
    (b"IDAT", zlib.compress(bytes(out), 9)),
    (b"IEND", b""),
])
with open(OUT, "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n" + body)
print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes, {W}x{H})")
