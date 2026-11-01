import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
OUT = SP + 'fork_sz14/d16/iq_sz_noaudio.mp4'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['IQ TEST'], accent=0, sub='ONLY 1% GET THIS')
DUR = 9.5; N = int(DUR * FPS)
# Liza's moonlit temple, cover-cropped
BGF = bg_frames('bg_moon.gif', (int(1600 * H / 900), H), step=1, bright=0.9)
BGF = [f.crop(((f.width - W) // 2, 0, (f.width - W) // 2 + W, H)) for f in BGF]
SCROLL = up(Image.open(SP + 'fork2/scroll/00.png').convert('RGBA'), 3)
SX, SY = 118, HB + 22
Q = 0.75
G = {}
for k in ['mush', 'acv', 'mel']:
    g0 = gummy(k, 1); G[k] = g0.resize((int(g0.width * 66 / g0.height), 66), Image.NEAREST)
HOL = seq(SP + 'fork2/hollow_think', 3, 1, None)
INK = (74, 42, 22)
ROWS = [(['mush', 'mush', 'mush'], ['+', '+'], '30'), (['acv', 'acv', 'mush'], ['+', '+'], '20'), (['mel', 'mel', 'acv'], ['+', '+'], '13'), (['mush', 'acv', 'mel'], ['+', 'x'], '?')]
ROW_Y = [SY + 225, SY + 360, SY + 495, SY + 630]
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
    ctext(d, SX + 360, sy + 104, 'SOLVE IT', F(26), (240, 220, 170), 4)
    for r, ((gs, ops, res), y0, t0) in enumerate(zip(ROWS, ROW_Y, T_ROW)):
        if t < t0: continue
        k = min(1, (t - t0) / 0.18); pop = 1 + 0.25 * math.sin(math.pi * k) if k < 1 else 1
        y = y0 + dy
        GX = [SX + 151, SX + 279, SX + 406]; OPX = [SX + 215, SX + 343]
        for i, g in enumerate(gs):
            im = G[g]
            if pop != 1: im = up(im, pop)
            bob = int(4 * math.sin(t * 3 + i + r * 1.3))
            img.alpha_composite(im, (int(GX[i] - im.width / 2), int(y - im.height / 2 + bob)))
            if i < 2: ctext(d, OPX[i], y - 17, ops[i], F(34), INK, 0)
        ctext(d, SX + 474, y - 17, '=', F(34), INK, 0)
        if res == '?':
            pz = 1 + 0.12 * math.sin(t * 6)
            ctext(d, SX + 562, y - 27 * pz, '?', F(int(54 * pz)), (200, 40, 40), 0)
        else:
            ctext(d, SX + 562, y - 17, res, F(34), INK, 0)
    if t > 2.1:
        ctext(d, SX + 360, sy + 740, "What's your final answer?", F(20), INK, 0)
    # the Hollow thinking + tag
    hf = HOL[int(t * 8) % len(HOL)]
    img.alpha_composite(hf, (70 - 25 * 3, 1496 - 78 * 3))
    d = ImageDraw.Draw(img)
    img.alpha_composite(HOOK)
    wr.write(img)
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': [(round(a, 3), b) for a, b in events]}, open(SP + 'fork_sz14/d16/iq_sz_events.json', 'w'))
print('done')
