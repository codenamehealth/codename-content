import sys, os; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
import numpy as np
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import math, random
Q = 4; QW, QH = W // Q, H // Q          # quarter-res canvas, upscaled 4x at the end
rng = random.Random(11)
BG = bg_frames('vit_hd.gif', (QW, QH), box=(656, 0, 1264, 1080), step=4, bright=0.32, blur=1)
GUM = up(crop(Image.open(PL + 'gummies/pick_cre.png').convert('RGBA')), 2)
PED = crop(Image.open(SP + 'fork2/pedestal/08.png').convert('RGBA'))
FLOOR = 375          # was 452: floor now at y1500 so the gummy + pedestal (unchanged size) sit in the safe zone
PX = QW // 2; PED_Y = FLOOR - PED.height; GUM_Y = PED_Y - GUM.height + 3
# support surface S(x): top of gummy, pedestal, floor
occ = Image.new('L', (QW, QH), 0)
occ.paste(255, (PX - PED.width // 2, PED_Y), PED.getchannel('A'))
occ.paste(255, (PX - GUM.width // 2, GUM_Y), GUM.getchannel('A'))
oa = np.array(occ)
S = np.full(QW, float(FLOOR))
for x in range(QW):
    ys = np.nonzero(oa[:, x] > 0)[0]
    if len(ys): S[x] = min(S[x], ys.min())
TH = 2               # was 3: thinner bars so the pile still fills the (smaller) zone near the end, like before
PAL = [((255, 120, 150), (255, 190, 205), (190, 60, 95)), ((255, 160, 60), (255, 210, 130), (200, 100, 30)), ((250, 225, 70), (255, 245, 170), (190, 160, 30)),
       ((110, 215, 90), (180, 245, 160), (60, 150, 50)), ((80, 210, 230), (170, 240, 250), (40, 140, 170)), ((90, 130, 240), (170, 195, 255), (50, 80, 180)), ((170, 100, 235), (215, 175, 250), (110, 60, 170))]
N = 150
# drop schedule: accelerating
times = []; t = 1.8; gap = 0.62
for i in range(N):
    times.append(t); t += gap; gap = max(0.09, gap * 0.972)
T_LAST = times[-1] + 0.35
print('last drop', round(times[-1], 2))
WEIGHT = [1.1 * 1.047 ** i for i in range(N)]
CUM = np.cumsum(WEIGHT)
FALL = 0.32
# precompute each bar's draped shape in landing order
shapes = []; surf = S.copy(); xs = np.arange(QW)
for i in range(N):
    base = surf - TH
    # lower envelope: min over x' of base(x') + SLOPE*|x-x'|  (bar can't sag steeper than SLOPE)
    SLOPE = 0.9 + 1.3 * (i / N)
    B = base.copy()
    for x in range(1, QW): B[x] = min(B[x], B[x - 1] + SLOPE)
    for x in range(QW - 2, -1, -1): B[x] = min(B[x], B[x + 1] + SLOPE)
    k = np.ones(21) / 21; Bp = np.pad(B, 10, mode='edge'); B = np.convolve(Bp, k, mode='valid')
    B = np.minimum(B, base)
    shapes.append(B.copy()); surf = B.copy()
def draw_bar(dd, B, col, y_off=0.0):
    c, hi, lo = col; prev = None
    for x in range(QW):
        y = int(round(B[x] + y_off))
        y0 = min(y, prev) if prev is not None else y
        y1 = max(y, prev) if prev is not None else y
        dd.rectangle([x, y0, x, y1 + TH - 1], fill=c + (255,))
        dd.point((x, y), fill=hi + (255,)); dd.point((x, y + TH - 1), fill=lo + (255,)) if TH > 1 else None
        prev = y
PILE = Image.new('RGBA', (QW, QH), (0, 0, 0, 0)); pd = ImageDraw.Draw(PILE); settled = 0
CLEO = vic('cleo', 520)
DUR = T_LAST + 4.6
_hk = {}
def HOOK(sub):
    if sub not in _hk: _hk.clear(); _hk[sub] = hook_layer(['THE GUMMY VS', '150 JELLY BARS'], accent=1, sub=sub)
    return _hk[sub]
HB = HOOK('0 / 150')[1]
wr = Writer('v74_noaudio.mp4'); ev = []
FB = F(16); FS = F(10)
def qtext(d, x, y, t, f, fill, sw=2):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BG[int(t * 3) % len(BG)].copy()
    d = ImageDraw.Draw(img); d.rectangle([0, FLOOR, QW, QH], fill=(40, 30, 40, 255)); d.line([(0, FLOOR), (QW, FLOOR)], fill=(90, 70, 80, 255))
    while settled < N and t >= times[settled] + FALL:
        draw_bar(pd, shapes[settled], PAL[settled % 7]); settled += 1
    n_on = settled
    w = CUM[n_on - 1] if n_on else 0.0
    # gummy squish under load
    load = min(1, math.log10(1 + w) / 4.4) if t < T_LAST + 0.5 else 0
    sq = 1 - 0.14 * load + (0.03 * math.sin(t * 40) * load if t < T_LAST else 0)
    end = t >= T_LAST + 0.5
    img.alpha_composite(PED, (PX - PED.width // 2, PED_Y))
    g = GUM.resize((GUM.width, max(1, int(GUM.height * sq))), Image.NEAREST)
    if end:
        u = t - T_LAST - 0.5; bounce = abs(math.sin(u * 6)) * 12 * math.exp(-u * 1.5)
        img.alpha_composite(g, (PX - g.width // 2, int(PED_Y - g.height + 3 - bounce)))
    else:
        img.alpha_composite(g, (PX - g.width // 2, PED_Y - g.height + 3))
    if not end:
        img.alpha_composite(PILE)
        dd = ImageDraw.Draw(img)
        for i in range(settled, N):
            if times[i] <= t < times[i] + FALL:
                u = (t - times[i]) / FALL; B = shapes[i]; top = B.min()
                # falls straight, then drapes in the last 30%
                if u < 0.7:
                    yy = -10 + (top + 10) * (u / 0.7) ** 2; flat = np.full(QW, yy)
                    draw_bar(dd, flat, PAL[i % 7])
                else:
                    k = (u - 0.7) / 0.3; draw_bar(dd, top + (B - top) * k, PAL[i % 7])
            if times[i] > t: break
    else:
        # the gummy pops: the pile bursts into jelly bits
        u = t - T_LAST - 0.5
        if u < 1.8:
            dd = ImageDraw.Draw(img); rr = random.Random(5)
            for q in range(220):
                ang = rr.uniform(-math.pi, 0); sp = rr.uniform(80, 260); x0 = rr.uniform(0, QW); y0 = rr.uniform(60, FLOOR)
                x = x0 + math.cos(ang) * sp * u; y = y0 + math.sin(ang) * sp * u + 160 * u * u
                c = PAL[q % 7][0]; dd.rectangle([x, y, x + 2, y + 1], fill=c + (255,))
    # header / counters
    d = ImageDraw.Draw(img)
    kg = f'{w:,.0f} KG' if w >= 10 else f'{w:.1f} KG'
    sub = f'{n_on} / 150   ' + (kg if not end else f'{CUM[-1]:,.0f} KG')
    big = img.resize((W, H), Image.NEAREST)
    if end:
        u = t - T_LAST - 0.5; a = int(255 * min(1, u / 0.3))
        if u > 0.6:
            vf = CLEO[int(u * 8) % len(CLEO)]; big.alpha_composite(vf, (80, 1500 - vf.height))
        if u < 0.2: big.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(255 * (1 - u / 0.2)))))
        text_layer(big, [(478, HB + 70, 'ALL 150!', 96, (255, 214, 60), 11, a), (478, HB + 220, 'The gummy held.', 44, (255, 255, 255), 6, a)])
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'boom')); ev.append((round(t + 0.15, 3), 'victory')); ev.append((round(t + 0.3, 3), 'cheer'))
    big.alpha_composite(HOOK(sub)[0])
    wr.write(big)
for i in range(N):
    if i < 40 or i % 3 == 0: ev.append((round(times[i] + FALL, 3), 'squish' if i % 2 else 'stomp_8bit'))
wr.close(); json.dump(ev, open('v74_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
