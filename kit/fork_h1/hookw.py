"""Oct 29 hook-only pass (fork_h1): same soft fade as safezone/hook.py hook_fade (same gradient, font, 6px stroke),
but the accent colour goes on single WORDS, and the text can be placed by its glyph bottom so the hook's bottom edge
stays where the old hook's was (layout below is untouched: scripts keep their old HB value)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone')
from hook import _fit, X0, X1, W, H
from PIL import Image, ImageDraw

def hook_fade_w(lines, accent_words=(), color=(255, 214, 60), size=64, y=286, glyph_bottom=None, lh_k=1.32,
                fade_to=None, strength=190):
    lines = [l.upper() for l in lines]
    acc = set(a.upper() for a in accent_words)
    f, s = _fit(lines, X1 - X0 - 20, size, 40)
    lh = int(s * lh_k)
    if glyph_bottom is not None: y = glyph_bottom - (len(lines) - 1) * lh - s
    bottom = y + len(lines) * lh
    fe = fade_to or bottom + 110
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = Image.new('L', (1, H), 0)
    for yy in range(H): g.putpixel((0, yy), int(strength * max(0.0, min(1.0, (fe - yy) / max(1, fe - 230)))))
    sh = Image.new('RGBA', (W, H), (8, 6, 16, 255)); sh.putalpha(g.resize((W, H))); L.alpha_composite(sh)
    d = ImageDraw.Draw(L)
    for i, l in enumerate(lines):
        x0 = W / 2 - d.textlength(l, font=f) / 2; yy = y + i * lh
        words = l.split(' ')
        for j, wd in enumerate(words):
            x = x0 + d.textlength(' '.join(words[:j]) + (' ' if j else ''), font=f)
            d.text((x, yy), wd, font=f, fill=color if wd in acc else (255, 255, 255), stroke_width=6, stroke_fill=(12, 8, 20))
    return L, dict(y=y, size=s, lh=lh, glyph_bottom=y + (len(lines) - 1) * lh + s, fade_to=fe)
