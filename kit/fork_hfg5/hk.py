# fork_hfg5 helpers: approved soft-fade hook (safezone/hook.py) with per-segment colours.
import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone')
from hook import hook_fade, hook_band, _fit, X0 as HX0, X1 as HX1
from PIL import ImageDraw
W = 1080
WHITE = (255, 255, 255)


def hook_fade_segs(lines, size=64, y=286, strength=190, band=False, alpha=170):
    """lines: list of lines, each a list of (text, colour) segments. Fade (or full-width strip when band=True), no box.
    Returns (layer, bottom_y)."""
    plain = [''.join(t for t, _ in l) for l in lines]
    if band:
        L, b = hook_band(plain, accent=None, size=size, y=y, alpha=alpha)
        f, s = _fit([p.upper() for p in plain], HX1 - HX0 - 20, size, 40); lh = int(s * 1.3); y0 = y + 24
    else:
        L, b = hook_fade(plain, accent=None, size=size, y=y, strength=strength)
        f, s = _fit([p.upper() for p in plain], HX1 - HX0 - 20, size, 40); lh = int(s * 1.32); y0 = y
    d = ImageDraw.Draw(L)
    for i, segs in enumerate(lines):
        full = ''.join(t for t, _ in segs).upper()
        x = W / 2 - d.textlength(full, font=f) / 2
        for t, c in segs:
            t = t.upper()
            d.text((x, y0 + i * lh), t, font=f, fill=c, stroke_width=7 if band else 6, stroke_fill=(12, 8, 20))
            x += d.textlength(t, font=f)
    return L, b


def hook_fade_tint(lines, accent=None, color=(255, 214, 60), size=64, y=286, strength=190, tint=(8, 6, 16)):
    """hook_fade with the fade colour as a parameter (e.g. warm dark brown over parchment)."""
    from PIL import Image
    L, b = hook_fade(lines, accent=accent, color=color, size=size, y=y, strength=strength)
    import numpy as np
    a = np.asarray(L).copy()
    # pixels that are pure fade (no text) carry the fade colour; recolour them, keep alpha
    fade = (a[..., 0] == 8) & (a[..., 1] == 6) & (a[..., 2] == 16)
    a[fade, 0], a[fade, 1], a[fade, 2] = tint
    return Image.fromarray(a, 'RGBA'), b
