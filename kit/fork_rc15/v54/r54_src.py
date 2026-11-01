import sys, os; os.chdir('../../fork_b5/v54'); OUT='../../fork_c4/v54/'; sys.path.insert(0, '../../fork1'); sys.path.insert(0, '../../pixellab/safezone')
from hook import hook_layer
HK, HB = hook_layer(['PUT THE GUMMY', 'IN THE BOTTLE'], accent=1, color=(140, 230, 90), sub='PAUSE WHEN IT DROPS IN'); print('HB', HB)
from common import *
import numpy as np
JS = 12
nat = Image.open('../jar_native.png').convert('RGBA'); a = np.array(nat)
cork = Image.fromarray(a[0:5].copy()); cork = crop(cork)
b = a.copy(); b[0:5] = 0
for x in range(11, 17): b[5, x] = (20, 60, 16, 255)
OPEN = up(Image.fromarray(b), JS)
# glass-ish neck: make neck rows semi transparent so a gummy inside reads as inside
nk = np.array(OPEN); nk[5 * JS:19 * JS, 9 * JS:19 * JS, 3] = (nk[5 * JS:19 * JS, 9 * JS:19 * JS, 3] * 0.55).astype(np.uint8); OPEN_GLASS = Image.fromarray(nk)
CORK = up(cork, JS); CLOSED = up(nat, JS)
BX, BB = 640, 1495                       # bottle centre x, bottom y
BT = BB - OPEN.height                     # bottle top (row 0)
M = (BX - OPEN.width / 2 + 14 * JS, BT + 5 * JS)   # mouth centre
GUM = gummy('acv', 3); GW = GUM.width
BG = [up(Image.open('../orchard2/00.png').convert('RGBA'), 3)]
JK = 6; JX = 268
def _nt(p, box=(43, 33, 49, 38)):
    im = Image.open(p).convert('RGBA'); px = im.load()
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            r, g, b_, al = px[x, y]
            if al and r > 235 and g > 225 and b_ > 215: px[x, y] = (106, 38, 9, 255)   # no teeth: Syeda-style dark open mouth
    return up(im, JK)
JOY = [_nt(p) for p in sorted(glob.glob(SP + 'fork_a3/joy_cast/*.png'))[1:]]; JOYI = idle('joy', JK)
DUR = 10.0; NF = int(DUR * FPS); T_GO = 1.8; T_END = 9.0; T_LOOP = 9.75
ts = np.arange(NF) / FPS
rng = np.random.RandomState(11); best = None
FSTAR = int(6.3 * FPS)
for trial in range(120000):
    A1, A2 = rng.uniform(150, 300), rng.uniform(40, 120); w1, w2 = rng.uniform(1.8, 3.6), rng.uniform(3.5, 6.5)
    C1, w3 = rng.uniform(180, 420), rng.uniform(2.0, 4.0); p = rng.uniform(0, 6.3, 3)
    gx = A1 * np.sin(w1 * ts + p[0]) + A2 * np.sin(w2 * ts + p[1])
    gy = -np.abs(C1 * np.sin(w3 * ts + p[2])) + 30 * np.sin(5.1 * ts)
    gx = gx - gx[FSTAR]; gy = gy - gy[FSTAR]
    act = (ts >= T_GO) & (ts <= T_END)
    X, Y = M[0] + gx, M[1] + gy
    if X[act].min() < 360 or X[act].max() > 985 or Y[act].min() < HB + 60 or Y[act].max() > M[1] + 80: continue
    if (X[act & (Y > 1074)] > 850).any(): continue
    d = np.hypot(X - M[0], Y - M[1]); d[~act] = 1e9; d[FSTAR] = 1e9
    near = ((d < 140) & act).sum()
    mn = d.min()
    if near < 6 or d[FSTAR - 1] < 48 or d[FSTAR + 1] < 48: continue
    sc = mn
    if best is None or sc > best[0]: best = (sc, X.copy(), Y.copy(), near)
print('min miss px', round(best[0], 1), 'near frames', best[3])
_, PX, PY, _ = best
ev = [(0.7, 'poof'), (T_GO - 0.3, 'twinkle')]
print('bottle', BX - OPEN.width / 2, BT, BX + OPEN.width / 2, BB, 'mouth', M)
wr = Writer(OUT + 'v54_noaudio.mp4')
for F_ in range(NF):
    f = F_; t = f / FPS
    img = BG[0].copy()
    # Joy
    if t >= T_LOOP: t = 0.0; f = 0
    fr = JOY[(f // 3) % len(JOY)] if t > 0.4 else JOYI[(f // 3) % len(JOYI)]
    img.alpha_composite(fr, (int(JX - fr.width / 2), int(BB - 78 * JK)))
    staff = (JX + 13 * JK, BB - 45 * JK)
    # gummy position
    if t < T_GO:
        u = max(0, (t - 1.2) / (T_GO - 1.2)); gx, gy = staff[0] + (PX[int(T_GO * FPS)] - staff[0]) * u, staff[1] + (PY[int(T_GO * FPS)] - staff[1]) * u - 120 * math.sin(math.pi * u)
    else:
        k = min(f, int(T_END * FPS)); gx, gy = PX[k], PY[k]
    inside = (f == FSTAR)
    show_g = t > 1.2
    if inside and show_g:
        g = GUM; img.alpha_composite(g, (int(gx - g.width / 2), int(gy + 36 - g.height / 2)))
        img.alpha_composite(OPEN_GLASS, (int(BX - OPEN.width / 2), BT))
    else:
        img.alpha_composite(CLOSED if t < 0.7 else OPEN, (int(BX - OPEN.width / 2), BT))
    if 0.7 <= t < 2.2:
        u = t - 0.7; cx, cy = M[0] + 260 * u, BT - 900 * u + 1500 * u * u
        c = CORK.rotate(-u * 720, expand=True); img.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))
        if u < 0.5: text_layer(img, [(M[0] - 40, BT - 140, 'POP!', 56, (255, 255, 255), 7, int(255 * (1 - u / 0.5)))])
    if show_g and not inside:
        # magic tether sparkles from Joy's staff to the gummy
        def tether(d):
            for q in range(10):
                u = (q / 10 + t * 0.8) % 1; sx, sy = staff[0] + (gx - staff[0]) * u, staff[1] + (gy - staff[1]) * u - 60 * math.sin(math.pi * u)
                d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(160, 255, 120, int(200 * (1 - abs(u - 0.5)))))
            d.ellipse([gx - 50, gy - 50, gx + 50, gy + 50], fill=(255, 120, 90, 50))
        layer(img, tether)
        g = GUM.rotate(10 * math.sin(t * 7), resample=Image.NEAREST, expand=True); img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    # header
    if T_END <= t:
        u = t - T_END
        text_layer(img, [(W / 2, 700, 'DID YOU GET IT?', 62, (255, 214, 60), 8, int(255 * min(1, u / 0.2)))])
    img.alpha_composite(HK)
    wr.write(img)
    if F_ in (FSTAR - 1, FSTAR, FSTAR + 1): img.convert('RGB').crop((300, 500, 1000, 1500)).save(OUT + f'm_{f - FSTAR:+d}.png')
    if F_ % 60 == 0 or F_ in (NF - 1, 0): img.convert('RGB').save(OUT + f'p_{F_:04d}.png')
wr.close()
json.dump(ev + [(T_END, 'chime')], open(OUT + 'ev54.json', 'w')); print('done, match frame', FSTAR, round(FSTAR / FPS, 2))
