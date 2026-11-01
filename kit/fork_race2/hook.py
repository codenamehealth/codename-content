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
