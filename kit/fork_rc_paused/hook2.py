"""hook_layer with the comment prompt as a real second line of the band, at least 44px (RECUT_BRIEF rule).
Same look as safezone/hook.py; sub line is 44-52px, white, thinner stroke, separated by a thin divider."""
import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone')
from hook import _fit, FONT, W, H, X0, X1, Y0
from PIL import Image, ImageDraw, ImageFont
def hook_layer2(lines, accent=None, color=(255, 214, 60), sub=None, sub_color=(240, 240, 240), border=None, sub_max=52):
    lines = [l.upper() for l in lines][:2]
    f, s = _fit(lines, X1 - X0 - 40)
    gap = int(s * 0.38); pad = 26
    h = len(lines) * s + (len(lines) - 1) * gap + 2 * pad
    if sub:
        fs, ss = _fit([sub], X1 - X0 - 40, sub_max, 44)
        d0 = ImageDraw.Draw(Image.new('L', (1, 1)))
        assert d0.textlength(sub, font=fs) + 12 <= X1 - X0 - 30, ('sub too long for 44px', sub)
        h += ss + 34
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([X0, Y0, X1, Y0 + h], 22, fill=(14, 10, 24, 232), outline=border or color, width=6)
    y = Y0 + pad
    for i, l in enumerate(lines):
        c = color if accent == i else (255, 255, 255)
        w = d.textlength(l, font=f)
        d.text(((X0 + X1) / 2 - w / 2, y), l, font=f, fill=c, stroke_width=9, stroke_fill=(10, 6, 18))
        y += s + gap
    if sub:
        y = y - gap + 14
        d.line([(X0 + 60, y), (X1 - 60, y)], fill=(color if border is None else border)[:3] + (120,), width=3)
        y += 18
        w = d.textlength(sub, font=fs)
        d.text(((X0 + X1) / 2 - w / 2, y), sub, font=fs, fill=sub_color, stroke_width=6, stroke_fill=(10, 6, 18))
    return L, Y0 + h
if __name__ == '__main__':
    L, b = hook_layer2(['Which jar is', "Cyrus's?"], accent=1, color=(255, 160, 40), sub='Comment A, B, C or D')
    im = Image.new('RGBA', (W, H), (60, 90, 60, 255)); im.alpha_composite(L); im.convert('RGB').crop((0, 200, 1080, 700)).save(sys.argv[1] if len(sys.argv) > 1 else 'hook2_demo.png'); print('bottom', b)
