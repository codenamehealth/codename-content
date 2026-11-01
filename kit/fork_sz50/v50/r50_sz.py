import sys; sys.path.insert(0, '../../fork1'); sys.path.insert(0, '../../pixellab/safezone')
import os; os.chdir('../../fork_b5/v50'); OUT='../../fork_sz50/v50/'
from hook import hook_layer
from common import *
import numpy as np
from PIL import ImageFilter
random.seed(4)
DUR = 19.5; NF = int(DUR * FPS)
BG = bg_frames('recov_hd.gif', (W, H), box=(690, 0, 1297, 1080), step=2, bright=0.42)
# lines on a low-res grid (4x) for chunky pixels
LS = 4; LW, LH = W // LS, H // LS
Y0, Y1 = 1440 // LS, 860 // LS              # bottom start, top end (low-res)
SX = [170 / LS, 370 / LS, 570 / LS]
TX = [230 / LS, 500 / LS, 770 / LS]
CX, HW = 470 / LS, 380 / LS
PERM = [2, 0, 1]                             # A->C slot, B->A slot, C->B slot (never shown)
COL = [(255, 206, 70), (80, 220, 255), (255, 100, 210)]
DARK = [(110, 70, 10), (10, 70, 110), (110, 20, 80)]
rng = np.random.RandomState(7)
PAR = []
for i in range(3):
    PAR.append([(rng.uniform(40, 70), rng.uniform(0.6, 2.4), rng.uniform(0, 6.3), rng.uniform(0.4, 1.1) * rng.choice([-1, 1])) for _ in range(3)])
T_GROW, T_SETTLE, T_PRIZE = 2.2, 13.5, 14.2
def path(i, t):
    us = np.linspace(0, 1, 260); s, e = SX[i], TX[PERM[i]]
    tt = min(t, T_SETTLE) + (0 if t < T_SETTLE else (1 - math.exp(-(t - T_SETTLE) * 2)) * 0.4)
    x = s + (e - s) * (3 * us ** 2 - 2 * us ** 3)
    env = np.sin(np.pi * us) ** 0.8
    for a, f, ph, w in PAR[i]:
        x = x + a * env * np.sin(2 * np.pi * f * us + ph + w * tt)
    x = CX + HW * np.tanh((x - CX) / HW)
    y = Y0 + (Y1 - Y0) * us
    return x, y
def draw_lines(t, grow):
    L = Image.new('RGBA', (LW, LH), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = []
    for i in range(3):
        x, y = path(i, t); n = max(2, int(len(x) * grow)); P = list(zip(x[:n], y[:n])); pts.append(P)
    order = [(int(t * 0.7) + k) % 3 for k in range(3)]
    for i in order:
        d.line(pts[i], fill=DARK[i] + (255,), width=7, joint='curve')
        d.line(pts[i], fill=COL[i] + (255,), width=4, joint='curve')
        d.line([(px, py - 1) for px, py in pts[i]], fill=tuple(min(255, c + 80) for c in COL[i]) + (255,), width=1)
    big = up(L, LS)
    glow = big.filter(ImageFilter.GaussianBlur(18))
    return big, glow, pts
RAY = idle('ray', 4)
PR_DRAGON = up(Image.open('../dragon128L.png').convert('RGBA'), 2)
cr = crop(Image.open('../../pixellab/ref/crown_cands/01.png').convert('RGBA')); PR_CROWN = up(cr, max(1, 200 // cr.width))
PR_GUM = gummy('mel', 5)
PRIZES = [(PR_DRAGON, 'DRAGON'), (PR_CROWN, 'CROWN'), (PR_GUM, 'GUMMY')]
LBL = ['A', 'B', 'C']
stars = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0.5, 2), random.uniform(0, 6)) for _ in range(90)]
HK1, HB1 = hook_layer(['CHOOSE YOUR', 'PATH'], accent=1, sub='A, B OR C?')
HK2, HB2 = hook_layer(['WHAT DID', 'YOU GET?'], accent=1, sub='COMMENT YOUR PRIZE')
print('hook bottoms', HB1, HB2)
wr = Writer(OUT + 'v50_noaudio.mp4'); ev = []
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, (y + t * 20 * s) % H, x + 4 * s, (y + t * 20 * s) % H + 4 * s], fill=(255, 240, 200, int(120 + 100 * math.sin(t * 3 + p)))) for x, y, s, p in stars])
    grow = min(1, max(0, (t - 0.6) / (T_GROW - 0.6)))
    if grow > 0:
        big, glow, pts = draw_lines(t, grow)
        ga = glow.getchannel('A').point(lambda v: int(v * 0.9)); glow.putalpha(ga)
        img.alpha_composite(glow); img.alpha_composite(big)
        # light pulses travelling up each path
        if grow >= 1:
            def pulses(d):
                for i in range(3):
                    P = pts[i]
                    for k in range(3):
                        u = ((t * 0.22 + k / 3 + i * 0.1) % 1)
                        px, py = P[int(u * (len(P) - 1))]
                        X, Y = px * LS, py * LS
                        d.ellipse([X - 11, Y - 11, X + 11, Y + 11], fill=(255, 255, 255, 220)); d.ellipse([X - 20, Y - 20, X + 20, Y + 20], outline=COL[i] + (150,), width=4)
            layer(img, pulses)
    # start orbs + Rayleigh
    def orbs(d):
        for i in range(3):
            X, Y = SX[i] * LS, Y0 * LS
            d.ellipse([X - 34, Y - 34, X + 34, Y + 34], fill=(20, 14, 34, 235), outline=COL[i] + (255,), width=6)
    layer(img, orbs)
    text_layer(img, [(SX[i] * LS, Y0 * LS - 16, LBL[i], 34, COL[i], 5, 255) for i in range(3)])
    rf = RAY[int(t * 8) % len(RAY)]; img.alpha_composite(rf, (564, 1495 - 312))
    # top slots: question marks until prizes pop
    for k in range(3):
        X = TX[k] * LS; Y = Y1 * LS
        if t < T_PRIZE:
            layer(img, lambda d, X=X, Y=Y: d.ellipse([X - 70, Y - 150, X + 70, Y - 10], fill=(20, 14, 34, 200), outline=(255, 214, 60, 220), width=5))
            text_layer(img, [(X, Y - 104, '?', 60, (255, 214, 60), 6, 255)])
        else:
            u = min(1, (t - T_PRIZE - k * 0.25) / 0.35)
            if u > 0:
                im, nm = PRIZES[k]; s = 0.4 + 0.6 * u + (0.08 * math.sin((t - T_PRIZE) * 12) * max(0, 1 - (t - T_PRIZE - k * 0.25)) if u >= 1 else 0)
                pim = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
                layer(img, lambda d, X=X, Y=Y: d.ellipse([X - 140, Y - 250, X + 140, Y + 10], fill=(255, 214, 60, int(50 * u))))
                img.alpha_composite(pim, (int(X - pim.width / 2), int(Y - 20 - pim.height)))
                text_layer(img, [(X, Y + 14, nm, 28, (255, 255, 255), 5, int(255 * u))])
                if not any(e[1] == 'chime' and abs(e[0] - (T_PRIZE + k * 0.25)) < 0.05 for e in ev) and u > 0: ev.append((round(T_PRIZE + k * 0.25, 3), 'chime'))
    if 0.6 < t < 2.4:
        text_layer(img, [(760, 1130, 'START!', 44, (255, 214, 60), 6, int(255 * min(1, (2.4 - t) / 0.3)))])
    img.alpha_composite(HK2 if t >= T_PRIZE + 0.6 else HK1)
    wr.write(img)
    if f % 45 == 0: img.convert('RGB').save(OUT + f'p_{f:04d}.png')
wr.close()
ev += [(0.6, 'whoosh_8bit'), (T_PRIZE + 0.9, 'twinkle')]
json.dump(ev, open(OUT + 'ev50.json', 'w')); print('done')
