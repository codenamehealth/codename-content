"""Standard Code Name hook band (Bennett: the hook makes or breaks the video).
usage:
    import sys; sys.path.insert(0, '<scratchpad>/pixellab/safezone'); from hook import hook_layer
    HOOK, HOOK_BOTTOM = hook_layer(['WHICH JAR IS', "CYRUS'S?"], accent=1, color=(255,214,60))
    frame.alpha_composite(HOOK)      # draw LAST (on top of everything) every frame
    # put content below HOOK_BOTTOM (typically ~450-470) and above y=1500
lines: 1-2 short lines of the original hook. accent: index of the line drawn in `color` (others white), or None.
sub: optional small secondary line (>=34px), drawn under the main lines.
"""
from PIL import Image, ImageDraw, ImageFont
import os
FONT = os.path.join(os.path.dirname(__file__), '../../npmfont/ps/package/files/PressStart2P.ttf')
W, H = 1080, 1920
X0, X1, Y0 = 70, 1025, 262
def _fit(lines, maxw, hi=80, lo=48):
    for s in range(hi, lo - 1, -2):
        f = ImageFont.truetype(FONT, s); d = ImageDraw.Draw(Image.new('L', (1, 1)))
        if all(d.textlength(l, font=f) + 2 * 9 <= maxw for l in lines): return f, s
    return ImageFont.truetype(FONT, lo), lo
def hook_layer(lines, accent=None, color=(255, 214, 60), sub=None, sub_color=(235, 235, 235), border=None):
    lines = [l.upper() for l in lines][:2]
    f, s = _fit(lines, X1 - X0 - 40)
    gap = int(s * 0.38); pad = 26
    h = len(lines) * s + (len(lines) - 1) * gap + 2 * pad
    fs = None
    if sub:
        fs, ss = _fit([sub], X1 - X0 - 40, 36, 30); h += ss + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([X0, Y0, X1, Y0 + h], 22, fill=(14, 10, 24, 225), outline=border or color, width=6)
    y = Y0 + pad
    for i, l in enumerate(lines):
        c = color if accent == i else (255, 255, 255)
        w = d.textlength(l, font=f)
        d.text(((X0 + X1) / 2 - w / 2, y), l, font=f, fill=c, stroke_width=9, stroke_fill=(10, 6, 18))
        y += s + gap
    if sub:
        w = d.textlength(sub, font=fs)
        d.text(((X0 + X1) / 2 - w / 2, y), sub, font=fs, fill=sub_color, stroke_width=6, stroke_fill=(10, 6, 18))
    return L, Y0 + h
if __name__ == '__main__':
    im = Image.open('/tmp/_a.png').convert('RGBA') if os.path.exists('/tmp/_a.png') else Image.new('RGBA', (W, H), (60, 90, 60, 255))
    L, b = hook_layer(['Which jar is', "Cyrus's?"], accent=1, sub='Follow the line')
    im.alpha_composite(L); im.convert('RGB').resize((540, 960)).save('hook_demo.jpg'); print('bottom', b)


# ---- Oct 29: approved hook style ("soft fade", Bennett). No box. Dark fade from the top edge, text over it.
def hook_fade(lines, accent=None, color=(255, 214, 60), size=64, y=286, fade_to=None, strength=190):
    """lines: as many as the video needs (usually 1-2). accent: index (or list of indexes) of lines drawn in `color`.
    Returns (RGBA layer, bottom_y). Composite LAST each frame. Content may start right under bottom_y."""
    lines = [l.upper() for l in lines]
    acc = set(accent if isinstance(accent, (list, tuple, set)) else ([] if accent is None else [accent]))
    f, s = _fit(lines, X1 - X0 - 20, size, 40)
    lh = int(s * 1.32)
    bottom = y + len(lines) * lh
    fe = fade_to or bottom + 110
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = Image.new('L', (1, H), 0)
    for yy in range(H): g.putpixel((0, yy), int(strength * max(0.0, min(1.0, (fe - yy) / max(1, fe - 230)))))
    sh = Image.new('RGBA', (W, H), (8, 6, 16, 255)); sh.putalpha(g.resize((W, H))); L.alpha_composite(sh)
    d = ImageDraw.Draw(L)
    for i, l in enumerate(lines):
        c = color if i in acc else (255, 255, 255)
        w = d.textlength(l, font=f)
        d.text((W / 2 - w / 2, y + i * lh), l, font=f, fill=c, stroke_width=6, stroke_fill=(12, 8, 20))
    return L, bottom


def hook_band(lines, accent=None, color=(255, 214, 60), size=72, y=262, alpha=170, pad=24):
    """Second approved style: full-width dark translucent strip edge to edge (no corners, no border), text centred on it."""
    lines = [l.upper() for l in lines]
    acc = set(accent if isinstance(accent, (list, tuple, set)) else ([] if accent is None else [accent]))
    f, s = _fit(lines, X1 - X0 - 20, size, 40)
    lh = int(s * 1.3)
    h = len(lines) * lh - (lh - s) + 2 * pad
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, y, W, y + h], fill=(10, 8, 20, alpha))
    for i, l in enumerate(lines):
        c = color if i in acc else (255, 255, 255)
        w = d.textlength(l, font=f)
        d.text((W / 2 - w / 2, y + pad + i * lh), l, font=f, fill=c, stroke_width=7, stroke_fill=(12, 8, 20))
    return L, y + h
