"""Oct 29 hook-only swaps (fork_h2). Same look as safezone/hook.py hook_fade / hook_band, plus:
- word-level accent: a line may be a list of (text, colour_or_None) segments; None = white.
- keep_bottom: the new hook is placed so its bottom edge equals the OLD hook's bottom edge (nothing else moves),
  and the fade gradient ends exactly where the old one did.
"""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone')
import hook as H
from PIL import Image, ImageDraw, ImageFont
W, HH = 1080, 1920
GOLD = (255, 214, 60)


def _norm(lines, accent, color):
    out = []
    acc = set(accent if isinstance(accent, (list, tuple, set)) else ([] if accent is None else [accent]))
    for i, l in enumerate(lines):
        if isinstance(l, (list, tuple)):
            out.append([(t.upper(), c) for t, c in l])
        else:
            out.append([(l.upper(), color if i in acc else None)])
    return out


def _draw_line(d, f, segs, y, stroke):
    full = ''.join(t for t, _ in segs)
    x = W / 2 - d.textlength(full, font=f) / 2
    pre = ''
    for t, c in segs:
        d.text((x + d.textlength(pre, font=f), y), t, font=f, fill=c or (255, 255, 255), stroke_width=stroke, stroke_fill=(12, 8, 20))
        pre += t


def fade(lines, accent=None, color=GOLD, size=64, y=286, fade_to=None, strength=190, tint=(8, 6, 16)):
    """Exact hook_fade look with word accents. Returns (layer, bottom)."""
    segs = _norm(lines, accent, color)
    plain = [''.join(t for t, _ in s) for s in segs]
    f, s = H._fit(plain, H.X1 - H.X0 - 20, size, 40)
    lh = int(s * 1.32)
    bottom = y + len(plain) * lh
    fe = fade_to or bottom + 110
    L = Image.new('RGBA', (W, HH), (0, 0, 0, 0))
    g = Image.new('L', (1, HH), 0)
    for yy in range(HH): g.putpixel((0, yy), int(strength * max(0.0, min(1.0, (fe - yy) / max(1, fe - 230)))))
    sh = Image.new('RGBA', (W, HH), tuple(tint) + (255,)); sh.putalpha(g.resize((W, HH))); L.alpha_composite(sh)
    d = ImageDraw.Draw(L)
    for i, sg in enumerate(segs): _draw_line(d, f, sg, y + i * lh, 6)
    return L, bottom, s


def fade_keep(old_lines, new_lines, accent=None, color=GOLD, size=64, y=286, fade_to=None, strength=190, old_accent=None, tint=(8, 6, 16)):
    """New hook whose bottom edge (and fade end) match the old hook_fade(old_lines, size=size, y=y, fade_to=fade_to)."""
    _, ob = H.hook_fade(old_lines, accent=old_accent, size=size, y=y, fade_to=fade_to, strength=strength)
    ofe = fade_to or ob + 110
    plain = [''.join(t for t, _ in s) for s in _norm(new_lines, accent, color)]
    _, s = H._fit(plain, H.X1 - H.X0 - 20, size, 40)
    ny = ob - len(plain) * int(s * 1.32)
    L, nb, s = fade(new_lines, accent, color, size, ny, ofe, strength, tint)
    assert nb == ob, (nb, ob)
    print(f'fade_keep: old bottom {ob}, new y {ny}, new size {s}px', flush=True)
    return L, ob


def band(lines, accent=None, color=GOLD, size=72, y=262, alpha=170, pad=24):
    segs = _norm(lines, accent, color)
    plain = [''.join(t for t, _ in s) for s in segs]
    f, s = H._fit(plain, H.X1 - H.X0 - 20, size, 40)
    lh = int(s * 1.3)
    h = len(plain) * lh - (lh - s) + 2 * pad
    L = Image.new('RGBA', (W, HH), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, y, W, y + h], fill=(10, 8, 20, alpha))
    for i, sg in enumerate(segs): _draw_line(d, f, sg, y + pad + i * lh, 7)
    return L, y + h, s


def band_keep(old_lines, new_lines, accent=None, color=GOLD, size=72, y=262, alpha=170, pad=24):
    _, ob = H.hook_band(old_lines, size=size, y=y, alpha=alpha, pad=pad)
    plain = [''.join(t for t, _ in s) for s in _norm(new_lines, accent, color)]
    _, s = H._fit(plain, H.X1 - H.X0 - 20, size, 40)
    lh = int(s * 1.3); h = len(plain) * lh - (lh - s) + 2 * pad
    ny = ob - h
    L, nb, s = band(new_lines, accent, color, size, ny, alpha, pad)
    assert nb == ob, (nb, ob)
    print(f'band_keep: old bottom {ob}, new y {ny}, new size {s}px', flush=True)
    return L, ob


def band_tight(lines, accent=None, color=GOLD, size=56, y_text=262, lh=70, top=250, bottom=398, alpha=170):
    """hook_band look (stroke 7, full-width strip, no border) with explicit strip top/bottom and line height, for a reel where
    the normal 2-line strip would cover a character (020: Cyrus's hair top is at y407)."""
    segs = _norm(lines, accent, color)
    plain = [''.join(t for t, _ in s) for s in segs]
    f, s = H._fit(plain, H.X1 - H.X0 - 20, size, 40)
    L = Image.new('RGBA', (W, HH), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, top, W, bottom], fill=(10, 8, 20, alpha))
    for i, sg in enumerate(segs): _draw_line(d, f, sg, y_text + i * lh, 7)
    print(f'band_tight: strip {top}-{bottom}, text {y_text}-{y_text + (len(segs) - 1) * lh + s}, {s}px', flush=True)
    return L, bottom
