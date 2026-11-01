"""#54 Put the gummy in the bottle: review recut (fork_rc15). Source fork_c4/v54/r54.py.
Starts on the cork pop (frame 1), rule as a 44px band line, DID YOU GET IT? on its own dark plate under the band from 5.0s (off the
gummy's path), white outline + gloss on Syeda's ACV gummy + ACV GUMMY tag on first appearance, Joy stays 6x. Exactly one in-bottle frame."""
import sys, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
OUT = SP0 + 'fork_rc15/v54/'
os.chdir(SP0 + 'fork_b5/v54'); sys.path.insert(0, SP0 + 'fork1'); sys.path.insert(0, SP0 + 'pixellab/safezone'); sys.path.insert(0, SP0 + 'fork_rc2')
from rc2 import hook_layer2, acv_gloss, acv_tag
HK, HB = hook_layer2(['PUT THE GUMMY', 'IN THE BOTTLE'], accent=1, color=(140, 230, 90), sub="PAUSE WHEN IT'S IN"); print('HB', HB)
from common import *
from PIL import ImageFilter
import numpy as np
JS = 12
nat = Image.open('../jar_native.png').convert('RGBA'); a = np.array(nat)
cork = Image.fromarray(a[0:5].copy()); cork = crop(cork)
b = a.copy(); b[0:5] = 0
for x in range(11, 17): b[5, x] = (20, 60, 16, 255)
OPEN = up(Image.fromarray(b), JS)
nk = np.array(OPEN); nk[5 * JS:19 * JS, 9 * JS:19 * JS, 3] = (nk[5 * JS:19 * JS, 9 * JS:19 * JS, 3] * 0.55).astype(np.uint8); OPEN_GLASS = Image.fromarray(nk)
CORK = up(cork, JS); CLOSED = up(nat, JS)
BX, BB = 640, 1495
BT = BB - OPEN.height
M = (BX - OPEN.width / 2 + 14 * JS, BT + 5 * JS)
# Syeda's ACV gummy + gloss (reads as a gummy) at 3x; white outline so it reads against the red apples in the tree
GUM = up(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')), 3)
def outlined(g, r=6, col=(255, 255, 255, 255)):
    pad = r + 2; c = Image.new('RGBA', (g.width + 2 * pad, g.height + 2 * pad), (0, 0, 0, 0)); c.alpha_composite(g, (pad, pad))
    m = c.getchannel('A').point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(2 * r + 1))
    o = Image.new('RGBA', c.size, col); o.putalpha(m)
    dk = Image.new('RGBA', c.size, (20, 40, 10, 255)); dk.putalpha(c.getchannel('A').point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.MaxFilter(5)))
    o.alpha_composite(dk); o.alpha_composite(c); return o
GUMO = outlined(GUM)
BG = [up(Image.open('../orchard2/00.png').convert('RGBA'), 3)]
JK = 6; JX = 268
def _nt(p, box=(43, 33, 49, 38)):
    im = Image.open(p).convert('RGBA'); px = im.load()
    for x in range(box[0], box[2]):
        for y in range(box[1], box[3]):
            r, g, b_, al = px[x, y]
            if al and r > 235 and g > 225 and b_ > 215: px[x, y] = (106, 38, 9, 255)
    return up(im, JK)
JOY = [_nt(p) for p in sorted(glob.glob(SP + 'fork_a3/joy_cast/*.png'))[1:]]; JOYI = idle('joy', JK)
DUR = 10.0; NF = int(DUR * FPS); T_GO = 1.8; T_END = 9.0; T_LOOP = 9.75
SKIP = 20                      # output frame 0 = source frame 20 (0.667s): cork pops on output frame 1
T_ASK = 1.0 + SKIP / FPS       # DID YOU GET IT? plate in at 1.0s output time (well before any neck pass, so it cues nothing)
PL0, PL1 = HB + 10, HB + 88    # prompt plate
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
    if X[act].min() < 360 or X[act].max() > 985 or Y[act].min() < 536 + 60 or Y[act].max() > M[1] + 80: continue
    if (X[act & (Y > 1074)] > 850).any(): continue
    d = np.hypot(X - M[0], Y - M[1]); d[~act] = 1e9; d[FSTAR] = 1e9
    near = ((d < 140) & act).sum()
    mn = d.min()
    if near < 6 or d[FSTAR - 1] < 48 or d[FSTAR + 1] < 48: continue
    sc = mn
    if best is None or sc > best[0]: best = (sc, X.copy(), Y.copy(), near)
print('min miss px', round(best[0], 1), 'near frames', best[3])
_, PX, PY, _ = best
print('path min Y', round(PY[(ts >= T_GO) & (ts <= T_END)].min()), 'times above 700:', [round(i/FPS,2) for i in range(NF) if T_GO<=i/FPS<=T_END and PY[i]<700][:1], sum(1 for i in range(NF) if T_GO<=i/FPS<=T_END and PY[i]<700))
dd = np.hypot(PX - M[0], PY - M[1]); act = (ts >= T_GO) & (ts <= T_END)
print('near-neck passes (src s):', [round(i / FPS, 2) for i in range(1, NF - 1) if act[i] and dd[i] < 140 and dd[i] <= dd[i - 1] and dd[i] <= dd[i + 1]])
ev = [(0.7 - SKIP / FPS, 'poof'), (T_GO - 0.3 - SKIP / FPS, 'twinkle'), (round(T_ASK - SKIP / FPS, 3), 'ding_8bit'), (T_END - SKIP / FPS, 'chime')]
NOUT = NF - SKIP
wr = Writer(OUT + 'v54_noaudio.mp4')
for F_ in range(NOUT):
    f = F_ + SKIP; t = f / FPS
    img = BG[0].copy()
    if t >= T_LOOP: t = SKIP / FPS; f = SKIP          # cut back to the opening state (corked, Joy idle)
    fr = JOY[(f // 3) % len(JOY)] if t > 0.4 else JOYI[(f // 3) % len(JOYI)]
    img.alpha_composite(fr, (int(JX - fr.width / 2), int(BB - 78 * JK)))
    staff = (JX + 13 * JK, BB - 45 * JK)
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
        if u < 0.5: text_layer(img, [(M[0] - 40, BT - 140, 'POP!', 64, (255, 255, 255), 8, int(255 * (1 - u / 0.5)))])
    if T_ASK <= t:
        aa = int(255 * min(1, (t - T_ASK) / 0.15)); s = 1 + 0.25 * max(0, 1 - (t - T_ASK) / 0.15)
        layer(img, lambda d: d.rounded_rectangle([70, PL0, 1025, PL1], 18, fill=(14, 10, 24, int(232 * aa / 255)), outline=(255, 214, 60, aa), width=5))
        text_layer(img, [(W / 2, PL0 + 16, 'DID YOU GET IT?', 52, (255, 214, 60), 7, aa)])
    if show_g and not inside:
        def tether(d):
            for q in range(10):
                u = (q / 10 + t * 0.8) % 1; sx, sy = staff[0] + (gx - staff[0]) * u, staff[1] + (gy - staff[1]) * u - 60 * math.sin(math.pi * u)
                d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(160, 255, 120, int(200 * (1 - abs(u - 0.5)))))
            d.ellipse([gx - 56, gy - 56, gx + 56, gy + 56], fill=(255, 255, 255, 46))
        layer(img, tether)
        g = GUMO.rotate(10 * math.sin(t * 7), resample=Image.NEAREST, expand=True); img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
        if t < 2.7:   # first appearance: ACV GUMMY tag rides above it
            aa = int(255 * min(1, (t - 1.2) / 0.15, (2.7 - t) / 0.25))
            acv_tag(img, int(gx), int(gy - 40), a=aa)
    img.alpha_composite(HK)
    wr.write(img)
    if f in (FSTAR - 1, FSTAR, FSTAR + 1) and t > 2: img.convert('RGB').crop((300, 500, 1000, 1500)).save(OUT + f'm_{f - FSTAR:+d}.png')
    if F_ % 30 == 0 or F_ in (NOUT - 1, 0, 1, 2): img.convert('RGB').save(OUT + f'p_{F_:04d}.png')
wr.close()
json.dump({'events': ev}, open(OUT + 'ev54.json', 'w')); print('done, match frame src', FSTAR, 'out', FSTAR - SKIP, round((FSTAR - SKIP) / FPS, 2), 'dur', NOUT / FPS)
