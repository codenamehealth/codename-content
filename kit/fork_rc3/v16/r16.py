import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
# rc3 recut of #16 (approved by Bennett: legibility + universal fixes only). Source: fork_sz14/d16/r16.py
D16 = SP + 'fork_rc3/v16/'
OUT = D16 + 'v16_noaudio.mp4'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import FONT as HF, X0, X1, Y0
def hook3():
    """IQ TEST (80, gold) + ONLY 1% GET THIS (36) + COMMENT YOUR ANSWER (44) as a real third row of the band"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    f1, f2, f3 = ImageFont.truetype(HF, 80), ImageFont.truetype(HF, 36), ImageFont.truetype(HF, 44)
    h = 26 + 80 + 26 + 36 + 22 + 18 + 44 + 26
    d.rounded_rectangle([X0, Y0, X1, Y0 + h], 22, fill=(14, 10, 24, 232), outline=(255, 214, 60), width=6)
    y = Y0 + 26
    for txt, f, col, sw, yy in (('IQ TEST', f1, (255, 214, 60), 9, 80 + 26), ('ONLY 1% GET THIS', f2, (235, 235, 235), 6, 36 + 22)):
        w = d.textlength(txt, font=f); d.text(((X0 + X1) / 2 - w / 2, y), txt, font=f, fill=col, stroke_width=sw, stroke_fill=(10, 6, 18)); y += yy
    d.line([(X0 + 60, y - 6), (X1 - 60, y - 6)], fill=(255, 214, 60, 120), width=3); y += 12
    txt = 'COMMENT YOUR ANSWER'; w = d.textlength(txt, font=f3)
    d.text(((X0 + X1) / 2 - w / 2, y), txt, font=f3, fill=(245, 245, 245), stroke_width=6, stroke_fill=(10, 6, 18))
    return L, Y0 + h
HOOK, HB = hook3()
T_UP, T_RESET, DUR = 6.0, 7.3, 7.6; N = int(round(DUR * FPS))
BGF = bg_frames('bg_moon.gif', (int(1600 * H / 900), H), step=1, bright=0.9)
BGF = [f.crop(((f.width - W) // 2, 0, (f.width - W) // 2 + W, H)) for f in BGF]
SCROLL = up(Image.open(SP + 'fork2/scroll/00.png').convert('RGBA'), 3)
SX, SY = 118, HB + 22
RISE = 290            # scroll starts only 290px low so it always covers the far-bank figure in Liza's background
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong   # Syeda's ACV gummy + a clearer gummy shine
G = {}
for k in ['mush', 'acv', 'mel']:   # all 78px tall (mushroom exactly 3x; was 66px): 3x for all would make the melatonin gummy 102px wide and crowd the signs
    g0 = gummy(k, 1) if k != 'acv' else acv_gummy_strong(); G[k] = g0.resize((int(round(g0.width * 78 / g0.height)), 78), Image.NEAREST)
HOL = seq(SP + 'fork2/hollow_think', 3, 1, None)
INK = (74, 42, 22)
ROWS = [(['mush', 'mush', 'mush'], ['+', '+'], '30'), (['acv', 'acv', 'mush'], ['+', '+'], '20'), (['mel', 'mel', 'acv'], ['+', '+'], '13'), (['mush', 'acv', 'mel'], ['+', 'x'], '?')]
ROW_Y = [SY + 225, SY + 360, SY + 495, SY + 630]
T_ROW = [0.55, 0.95, 1.6, 2.0]; T_TAG = (0.95, 1.55); T_BAR0 = 2.25
GX = [SX + 134, SX + 278, SX + 422]; OPX = [SX + 206, SX + 350]; EQX, RX = SX + 492, SX + 572
BAR = (SX + 112, SY + 722, SX + 608, SY + 752)
events = [(0.05, 'whoosh_8bit')] + [(t, 'coin_8bit') for t in T_ROW] + [(2.3, 'ding_8bit'), (T_UP, 'buzz_8bit'), (T_RESET, 'swish')]
rng = random.Random(3); STARS = [(rng.uniform(0, W), rng.uniform(0, 700), rng.uniform(0, 6.28)) for _ in range(40)]
PREV = [int(v) for v in os.environ.get('PREV', '').split(',') if v]
wr = Writer(OUT)
for f in range(N):
    t = f / FPS
    img = BGF[int(t * 6) % len(BGF)].copy()
    layer(img, lambda d: [d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=(230, 240, 255, int(120 + 120 * math.sin(t * 3 + p)))) for x, y, p in STARS])
    if t < T_RESET:
        u = min(1, t / 0.45); e = 1 - (1 - u) ** 3; sy = int(SY + (1 - e) * RISE); fade = 255
    else:   # loop: everything clears and the scroll drops back to its frame-0 spot
        u = min(1, (t - T_RESET) / (DUR - T_RESET - 1 / FPS)); sy = int(SY + u * u * RISE); fade = int(255 * max(0, 1 - u * 1.6))
    img.alpha_composite(SCROLL, (SX, sy)); dy = sy - SY
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for r, ((gs, ops, res), y0, t0) in enumerate(zip(ROWS, ROW_Y, T_ROW)):
        if t < t0: continue
        k = min(1, (t - t0) / 0.18); pop = 1 + 0.25 * math.sin(math.pi * k) if k < 1 else 1
        y = y0 + dy
        for i, g in enumerate(gs):
            im = G[g]
            if pop != 1: im = up(im, pop)
            bob = int(4 * math.sin(t * 3 + i + r * 1.3))
            L.alpha_composite(im, (int(GX[i] - im.width / 2), int(y - im.height / 2 + bob)))
            if i < 2: ctext(d, OPX[i], y - 22, ops[i], F(44), INK, 0)
        ctext(d, EQX, y - 22, '=', F(44), INK, 0)
        if res == '?':
            pz = 1 + 0.14 * math.sin(t * 6)
            ctext(d, RX, y - 32 * pz, '?', F(int(64 * pz)), (200, 40, 40), 0)
        else:
            ctext(d, RX, y - 22, res, F(44), INK, 0)
    if T_TAG[0] <= t < T_TAG[1]:   # 'ACV GUMMY' tag on the first ACV gummies (row 2), in row 3's slot before row 3 pops in
        a_ = int(255 * min(1, (T_TAG[1] - t) / 0.12)); cy = ROW_Y[2] + dy - 30; tw = d.textlength('ACV GUMMY', font=F(44))
        d.polygon([(GX[0] - 18, cy - 4), (GX[0] + 18, cy - 4), (GX[0], cy - 30)], fill=(30, 60, 24, a_))
        d.rounded_rectangle([GX[0] - 50, cy - 6, GX[0] - 50 + tw + 58, cy + 66], 12, fill=(30, 60, 24, a_), outline=(150, 230, 110, a_), width=4)
        d.text((GX[0] - 32, cy + 8), 'ACV GUMMY', font=F(44), fill=(235, 255, 220, a_), stroke_width=5, stroke_fill=(14, 30, 10, a_))
    # think timer: a bar on the parchment that drains 2.0 -> 6.0s, red in the last second
    if t >= T_ROW[3]:
        x0, y0, x1, y1 = BAR; y0 += dy; y1 += dy
        frac = 1 - min(1, max(0, (t - T_BAR0) / (T_UP - T_BAR0)))
        d.rounded_rectangle([x0 - 5, y0 - 5, x1 + 5, y1 + 5], 10, fill=(60, 34, 16, 255))
        col = (90, 200, 80) if t < T_UP - 1.0 else ((230, 50, 40) if int(t * 6) % 2 == 0 else (255, 120, 90))
        if frac > 0: d.rounded_rectangle([x0, y0, x0 + (x1 - x0) * frac, y1], 6, fill=col + (255,))
    if fade < 255:
        a = L.getchannel('A').point(lambda p: p * fade // 255); L.putalpha(a)
    img.alpha_composite(L)
    if T_UP <= t < T_RESET + 0.15:   # TIME'S UP! hard pop over the bar
        u = t - T_UP; sc = 1.3 - 0.3 * min(1, u / 0.1); a = 255 if t < T_RESET else int(255 * (1 - (t - T_RESET) / 0.15))
        fs = int(60 * sc); L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(L2)
        tw = d2.textlength("TIME'S UP!", font=F(fs)); cx, cy = SX + 360, SY + 737 + dy
        d2.rounded_rectangle([cx - tw / 2 - 26, cy - fs / 2 - 20, cx + tw / 2 + 26, cy + fs / 2 + 20], 16, fill=(20, 10, 14, int(a * 0.92)), outline=(255, 70, 60, a), width=6)
        ctext(d2, cx, cy - fs / 2, "TIME'S UP!", F(fs), (255, 80, 70), 9, a)
        img.alpha_composite(L2)
    hf = HOL[int(t * 8) % len(HOL)]
    img.alpha_composite(hf, (70 - 25 * 3, 1496 - 78 * 3))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in PREV: img.convert('RGB').save(D16 + f'p_{f:03d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in events]}, open(D16 + 'v16_events.json', 'w'))
print('done', N)
