import sys; sys.path.insert(0, '../fork1'); sys.path.insert(0, '../pixellab/safezone')
from hook import hook_layer
from common import *
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 10.0; NF = int(DUR * FPS); TEND = 8.6
JAR = Image.open(A + 'jar_melatonin.png').convert('RGBA')
CORK = JAR.crop((200, 0, 340, 68)); BOT = JAR.copy(); ImageDraw.Draw(BOT).rectangle([0, 0, 540, 67], fill=(0, 0, 0, 0))
S = 1.2; BOT = BOT.resize((648, 648), Image.NEAREST); CORK = CORK.resize((int(CORK.width * S), int(CORK.height * S)), Image.NEAREST)
BX, BY = 388, 866
TX, TY = BX + 324, BY + int(78 * S)
HOOK, HB = hook_layer(['PUT THE GUMMY', 'IN THE BOTTLE'], accent=1, sub='PAUSE WHEN IT DROPS IN')
print('hook bottom', HB)
GUM = gummy('mel', 2)
# motion search: exactly one frame the gummy sits in the bottle mouth
ts = np.arange(NF) / FPS
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1); best = None
for trial in range(6000):
    fx = rng.uniform(0.35, 0.8); fx2 = rng.uniform(0.9, 1.6); fy = rng.uniform(0.4, 0.9); fy2 = rng.uniform(1.0, 1.8)
    ax, ax2 = rng.uniform(150, 230), rng.uniform(30, 90); ay, ay2 = rng.uniform(120, 170), rng.uniform(30, 70)
    p = [rng.uniform(0, 6.28) for _ in range(4)]
    xs = 600 + ax * np.sin(2 * np.pi * fx * ts + p[0]) + ax2 * np.sin(2 * np.pi * fx2 * ts + p[1])
    ys = 770 + ay * np.sin(2 * np.pi * fy * ts + p[2]) + ay2 * np.sin(2 * np.pi * fy2 * ts + p[3])
    valid = ts < TEND
    d = np.hypot(xs - TX, ys - TY); d[~valid] = 9e9
    k = int(np.argmin(d))
    if d[k] > 60 or ts[k] < 2.5: continue
    ys = ys + (TY - ys[k]) * np.exp(-((ts - ts[k]) / 0.12) ** 2); xs = xs + (TX - xs[k]) * np.exp(-((ts - ts[k]) / 0.12) ** 2)
    d = np.hypot(xs - TX, ys - TY); d2 = d.copy(); d2[k] = 9e9; d2[~valid] = 9e9
    if xs.min() < 150 or xs.max() > 930 or ys.min() < HB + 70: continue
    if ys.max() > TY + 2: continue
    miss = d2.min()
    if best is None or miss > best[0]: best = (miss, k, xs.copy(), ys.copy())
miss, KM, XS, YS = best
print('match frame', KM, round(KM / FPS, 2), 'next nearest', round(miss))
if len(sys.argv) > 2: sys.exit()
BG = bg_frames('recov_hd.gif', (3413, 1920), step=2, bright=0.85)
BG = [b.crop((1166, 0, 1166 + W, H)) for b in BG]
RAY = seq('../fork3/ray_cast', 6, 1, 9)
w = Writer('v26_noaudio.mp4'); ev = []; trail = []
for f in range(NF):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    # header
    # glow under bottle
    layer(img, lambda d: d.ellipse([BX + 100, BY + 560, BX + 548, BY + 680], fill=(140, 90, 255, 70)))
    img.alpha_composite(BOT, (BX, BY))
    # Ray channeling
    rf = RAY[int(t * 8) % len(RAY)]; fx0, fy0 = -84, 1490 - 78 * 6
    img.alpha_composite(rf, (fx0, fy0))
    gx, gy = XS[min(f, NF - 1)], YS[min(f, NF - 1)]
    if t > DUR - 1.4: gx, gy = XS[NF - 1], YS[NF - 1]
    sx, sy = fx0 + 59 * 6, fy0 + 35 * 6        # staff orb
    def magic(d):
        for i in range(28):
            u = i / 27; mx = sx + (gx - sx) * u + 30 * math.sin(t * 9 + u * 9) * math.sin(math.pi * u); my = sy + (gy - sy) * u + 30 * math.cos(t * 7 + u * 8) * math.sin(math.pi * u)
            r = 7 + 4 * math.sin(t * 12 + i); d.ellipse([mx - r - 4, my - r - 4, mx + r + 4, my + r + 4], fill=(190, 110, 255, 90)); d.ellipse([mx - r / 2, my - r / 2, mx + r / 2, my + r / 2], fill=(255, 235, 255, 230))
        d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(220, 150, 255, 110))
        for (tx_, ty_, a) in trail: d.ellipse([tx_ - 8, ty_ - 8, tx_ + 8, ty_ + 8], fill=(255, 220, 160, a))
        d.ellipse([gx - 50, gy - 50, gx + 50, gy + 50], fill=(255, 170, 90, 40))
    trail = [(x_, y_, int(a * 0.8)) for (x_, y_, a) in trail if a > 20] + [(gx, gy, 140)]
    layer(img, magic)
    img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
    if t > DUR - 1.4:
        a = int(255 * min(1, (t - (DUR - 1.4)) / 0.25))
        text_layer(img, [(W / 2, HB + 40, 'Did you get it?', 46, (255, 255, 255), 6, a)])
    img.alpha_composite(HOOK)
    if f % 45 == 0: ev.append((round(t, 3), 'whoosh_8bit'))
    w.write(img)
    if f in (KM - 1, KM, KM + 1): img.convert('RGB').crop((300, 700, 1000, 1200)).save(f'm26_{f - KM:+d}.png')
w.close(); json.dump(ev, open('v26_ev.json', 'w')); print('done')
