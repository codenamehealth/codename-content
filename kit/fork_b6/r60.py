import sys; sys.path.insert(0, '../fork1'); from common import *
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 10.0; N = int(DUR * FPS)
BG = bg_frames('vit_hd.gif', (W, H), box=(846, 0, 1454, 1080), step=1, bright=0.62)
src = gif_frames(A + 'idle_3.gif')
def native(f): return f.resize((92, 92), Image.NEAREST)
L5 = [up(native(f), 7) for f in src]
def silver(f):
    a = np.array(native(f)); m = np.zeros(a.shape[:2], bool)
    for y in range(54, 70):
        for x in range(55, 70):
            c = tuple(a[y, x][:3])
            if c == (214, 141, 33): a[y, x, :3] = (120, 126, 148)
            elif c == (255, 213, 0): a[y, x, :3] = (214, 218, 232)
    return up(Image.fromarray(a), 7)
R5 = [silver(f) for f in src]
GUM = gummy('cre', 4)
THINK = seq(PL + '../fork2/hollow_think', 3, 1)
FOOT = 78 * 7; FY = 1185; XL, XR = 292, 788
T0, T1 = 1.0, 8.0
ev = [(0.9, 'ding_8bit')] + [(T0 + k, 'tick_8bit') for k in range(1, 7)] + [(T1, 'buzz_8bit')]
w = Writer('v60_noaudio.mp4'); rng = random.Random(3)
SP_ = [(rng.uniform(60, 520), rng.uniform(450, 1230), rng.uniform(0, 6.3)) for _ in range(14)]
for f in range(N):
    t = f / FPS; img = BG[int(t * 8) % len(BG)].copy()
    img.paste(img.crop((44, 434, 540, 1246)), (540, 434))
    def panel(d):
        d.rounded_rectangle([40, 430, 1040, 1250], 28, fill=(12, 10, 26, 175))
        for x in (XL, XR):
            d.ellipse([x - 150, FY - 34, x + 150, FY + 34], fill=(46, 93, 168, 90), outline=(123, 157, 209, 200), width=4)
            d.ellipse([x - 110, FY - 20, x + 110, FY + 20], fill=(0, 0, 0, 70))
        for sx, sy, ph in SP_:
            a = int(140 + 110 * math.sin(t * 3 + ph))
            if a > 150:
                for ox in (0, 496): d.rectangle([sx + ox - 3, sy - 3, sx + ox + 3, sy + 3], fill=(200, 220, 255, a - 100))
    layer(img, panel)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 430, 1040, 1250], 28, outline=(232, 182, 76), width=6)
    d.line([540, 470, 540, 1210], fill=(232, 182, 76), width=4)
    k = int(t * 6) % len(L5)
    img.alpha_composite(L5[k], (XL - 322, FY - FOOT)); img.alpha_composite(R5[k], (XR - 322, FY - FOOT))
    bob = int(10 * math.sin(t * 3))
    for x in (XL, XR): img.alpha_composite(GUM, (x - GUM.width // 2, 520 + bob))
    # header
    layer(img, lambda dd: dd.rectangle([0, 110, W, 360], fill=(12, 10, 26, 200)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 150, 'ONLY 1', F(70), (255, 255, 255), 7)
    ctext(d, W / 2, 245, 'DIFFERENCE', F(70), (232, 182, 76), 7)
    # timer
    if t >= T0 - 0.2:
        u = max(0.0, min(1.0, (t - T0) / (T1 - T0))); rem = max(0, math.ceil(T1 - t))
        col = (90, 200, 80) if rem > 3 else (240, 80, 70)
        layer(img, lambda dd: dd.rounded_rectangle([90, 1300, 990, 1350], 16, fill=(12, 10, 26, 200)))
        d = ImageDraw.Draw(img)
        if u < 1: d.rounded_rectangle([98, 1308, 98 + int(884 * (1 - u)), 1342], 12, fill=col)
        d.rounded_rectangle([90, 1300, 990, 1350], 16, outline=(232, 182, 76), width=4)
        if t < T1: ctext(d, W / 2, 1385, f'{rem} SECONDS', F(40), col, 6)
    # hollow thinking
    th = THINK[int(t * 7) % len(THINK)]
    img.alpha_composite(th, (200 - th.width // 2, 1840 - 78 * 3))
    def bub(dd):
        dd.ellipse([300, 1470, 560, 1650], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=5)
        dd.ellipse([262, 1640, 298, 1672], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=4)
        dd.ellipse([238, 1680, 258, 1700], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=3)
    layer(img, bub); d = ImageDraw.Draw(img)
    ctext(d, 430, 1510 + int(4 * math.sin(t * 5)), '?', F(84), (232, 182, 76), 6)
    ctext(d, 760, 1560, 'Can you', F(46), (255, 255, 255), 6); ctext(d, 760, 1630, 'spot it?', F(46), (255, 255, 255), 6)
    if t >= T1:
        u = min(1, (t - T1) / 0.3)
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(120 * u))))
        layer(img, lambda dd: dd.rounded_rectangle([110, 700, 970, 1010], 28, fill=(12, 10, 26, int(235 * u))))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([110, 700, 970, 1010], 28, outline=(232, 182, 76), width=6)
        ctext(d, W / 2, 745, "TIME'S UP!", F(64), (232, 182, 76), 7)
        ctext(d, W / 2, 860, 'What is different?', F(36), (255, 255, 255), 5)
        ctext(d, W / 2, 920, 'Comment below', F(36), (255, 255, 255), 5)
    w.write(img)
    if f in (60, 200, 270): img.convert('RGB').save(f'k60_{f}.png')
w.close(); json.dump(ev, open('v60_ev.json', 'w')); print('ok')
