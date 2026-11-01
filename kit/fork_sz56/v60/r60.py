import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
import numpy as np
os.chdir(SP + 'fork_b6'); OUT = SP + 'fork_sz56/v60/'
HOOK, HB = hook_layer(['ONLY 1', 'DIFFERENCE'], accent=1)
PX0, PX1, PY0, PY1 = 70, 1010, HB + 18, 1106
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
FOOT = 78 * 7; FY = 1066; XL, XR = 305, 775
T0, T1 = 1.0, 8.0
ev = [(0.9, 'ding_8bit')] + [(T0 + k, 'tick_8bit') for k in range(1, 7)] + [(T1, 'buzz_8bit')]
w = Writer(OUT + 'v60_noaudio.mp4'); rng = random.Random(3)
SP_ = [(rng.uniform(85, 525), rng.uniform(PY0 + 20, PY1 - 20), rng.uniform(0, 6.3)) for _ in range(14)]
for f in range(N):
    t = f / FPS; img = BG[int(t * 8) % len(BG)].copy()
    img.paste(img.crop((PX0, PY0, 540, PY1)), (540, PY0))
    def panel(d):
        d.rounded_rectangle([PX0, PY0, PX1, PY1], 28, fill=(12, 10, 26, 175))
        for x in (XL, XR):
            d.ellipse([x - 150, FY - 34, x + 150, FY + 34], fill=(46, 93, 168, 90), outline=(123, 157, 209, 200), width=4)
            d.ellipse([x - 110, FY - 20, x + 110, FY + 20], fill=(0, 0, 0, 70))
        for sx, sy, ph in SP_:
            a = int(140 + 110 * math.sin(t * 3 + ph))
            if a > 150:
                for ox in (0, 470): d.rectangle([sx + ox - 3, sy - 3, sx + ox + 3, sy + 3], fill=(200, 220, 255, a - 100))
    layer(img, panel)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([PX0, PY0, PX1, PY1], 28, outline=(232, 182, 76), width=6)
    d.line([540, PY0 + 30, 540, PY1 - 30], fill=(232, 182, 76), width=4)
    k = int(t * 6) % len(L5)
    img.alpha_composite(L5[k], (XL - 322, FY - FOOT)); img.alpha_composite(R5[k], (XR - 322, FY - FOOT))
    bob = int(10 * math.sin(t * 3))
    for x in (XL, XR): img.alpha_composite(GUM, (x - GUM.width // 2, PY0 + 14 + bob))
    # timer
    if t >= T0 - 0.2:
        u = max(0.0, min(1.0, (t - T0) / (T1 - T0))); rem = max(0, math.ceil(T1 - t))
        col = (90, 200, 80) if rem > 3 else (240, 80, 70)
        layer(img, lambda dd: dd.rounded_rectangle([80, 1124, 870, 1170], 16, fill=(12, 10, 26, 200)))
        d = ImageDraw.Draw(img)
        if u < 1: d.rounded_rectangle([88, 1132, 88 + int(774 * (1 - u)), 1162], 12, fill=col)
        d.rounded_rectangle([80, 1124, 870, 1170], 16, outline=(232, 182, 76), width=4)
        if t < T1: ctext(d, 475, 1186, f'{rem} SECONDS', F(36), col, 6)
    # hollow thinking
    th = THINK[int(t * 7) % len(THINK)]
    img.alpha_composite(th, (190 - th.width // 2, 1496 - 78 * 3))
    def bub(dd):
        dd.ellipse([300, 1240, 500, 1380], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=5)
        dd.ellipse([268, 1372, 298, 1400], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=4)
        dd.ellipse([246, 1406, 264, 1424], fill=(250, 246, 232, 235), outline=(20, 15, 35, 255), width=3)
    layer(img, bub); d = ImageDraw.Draw(img)
    ctext(d, 400, 1268 + int(4 * math.sin(t * 5)), '?', F(80), (232, 182, 76), 6)
    ctext(d, 680, 1300, 'CAN YOU', F(44), (255, 255, 255), 6); ctext(d, 680, 1370, 'SPOT IT?', F(44), (255, 255, 255), 6)
    if t >= T1:
        u = min(1, (t - T1) / 0.3)
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(120 * u))))
        layer(img, lambda dd: dd.rounded_rectangle([110, 700, 970, 1010], 28, fill=(12, 10, 26, int(235 * u))))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([110, 700, 970, 1010], 28, outline=(232, 182, 76), width=6)
        ctext(d, W / 2, 745, "TIME'S UP!", F(64), (232, 182, 76), 7)
        ctext(d, W / 2, 860, 'What is different?', F(36), (255, 255, 255), 5)
        ctext(d, W / 2, 920, 'Comment below', F(36), (255, 255, 255), 5)
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (60, 200, 270): img.convert('RGB').save(OUT + f'k60_{f}.png')
w.close(); json.dump({'events': ev}, open(OUT + 'v60_ev.json', 'w')); print('ok')
