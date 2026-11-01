import sys, math, json
sys.path.insert(0, '../fork1')
from common import *
OUT = SP + 'fork2/iq_noaudio.mp4'
DUR = 9.5; N = int(DUR * FPS)
# Liza's moonlit temple, cover-cropped
BGF = bg_frames('bg_moon.gif', (int(1600 * H / 900), H), step=1, bright=0.9)
BGF = [f.crop(((f.width - W) // 2, 0, (f.width - W) // 2 + W, H)) for f in BGF]
SCROLL = up(Image.open(SP + 'fork2/scroll/00.png').convert('RGBA'), 4)
SX, SY = (W - SCROLL.width) // 2, 300
G = {}
for k in ['mush', 'acv', 'mel']:
    g0 = gummy(k, 1); G[k] = g0.resize((int(g0.width * 84 / g0.height), 84), Image.NEAREST)
HOL = seq(SP + 'fork2/hollow_think', 4, 1, None)
INK = (74, 42, 22)
ROWS = [(['mush', 'mush', 'mush'], ['+', '+'], '30'), (['acv', 'acv', 'mush'], ['+', '+'], '20'), (['mel', 'mel', 'acv'], ['+', '+'], '13'), (['mush', 'acv', 'mel'], ['+', 'x'], '?')]
ROW_Y = [SY + 300, SY + 480, SY + 660, SY + 840]
T_ROW = [0.55, 0.95, 1.35, 1.75]
events = [(0.05, 'whoosh_8bit')] + [(t, 'coin_8bit') for t in T_ROW] + [(2.3, 'ding_8bit')]
rng = random.Random(3); STARS = [(rng.uniform(0, W), rng.uniform(0, 700), rng.uniform(0, 6.28)) for _ in range(40)]
wr = Writer(OUT)
for f in range(N):
    t = f / FPS
    img = BGF[int(t * 6) % len(BGF)].copy()
    layer(img, lambda d: [d.rectangle([x - 2, y - 2, x + 2, y + 2], fill=(230, 240, 255, int(120 + 120 * math.sin(t * 3 + p)))) for x, y, p in STARS])
    # scroll slides up
    u = min(1, t / 0.45); e = 1 - (1 - u) ** 3; sy = int(SY + (1 - e) * 1300)
    img.alpha_composite(SCROLL, (SX, sy)); dy = sy - SY
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, sy + 150, 'SOLVE IT', F(30), (240, 220, 170), 4)
    for r, ((gs, ops, res), y0, t0) in enumerate(zip(ROWS, ROW_Y, T_ROW)):
        if t < t0: continue
        k = min(1, (t - t0) / 0.18); pop = 1 + 0.25 * math.sin(math.pi * k) if k < 1 else 1
        y = y0 + dy
        GX = [262, 432, 602]; OPX = [347, 517]
        for i, g in enumerate(gs):
            im = G[g]
            if pop != 1: im = up(im, pop)
            bob = int(4 * math.sin(t * 3 + i + r * 1.3))
            img.alpha_composite(im, (int(GX[i] - im.width / 2), int(y - im.height / 2 + bob)))
            if i < 2: ctext(d, OPX[i], y - 22, ops[i], F(44), INK, 0)
        ctext(d, 692, y - 22, '=', F(44), INK, 0)
        if res == '?':
            pz = 1 + 0.12 * math.sin(t * 6)
            ctext(d, 800, y - 34 * pz, '?', F(int(68 * pz)), (200, 40, 40), 0)
        else:
            ctext(d, 800, y - 22, res, F(44), INK, 0)
    if t > 2.1:
        ctext(d, W / 2, sy + 1005, "What's your final answer?", F(22), INK, 0)
    # the Hollow thinking + tag
    hf = HOL[int(t * 8) % len(HOL)]
    img.alpha_composite(hf, (-30, H - 10 - hf.height))
    if t > 2.3:
        k = min(1, (t - 2.3) / 0.2); a = int(255 * k)
        text_layer(img, [(660, 1700, 'ONLY 1%', 56, (255, 214, 60), 8, a), (660, 1780, 'GET THIS', 56, (255, 214, 60), 8, a)])
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 110, 'IQ TEST', F(96), (255, 255, 255), 9)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(SP + f'fork2/prev16/p_{f:03d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in events]}, open(SP + 'fork2/iq_events.json', 'w'))
print('done')
