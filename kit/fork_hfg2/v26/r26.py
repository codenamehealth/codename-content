# #26 Put the gummy in the bottle -- review recut (fork_rc4). One-frame puzzle: exactly one frame has the gummy in the mouth.
import sys, json, math, random, os
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP_ + 'fork1'); from common import *
sys.path.insert(0, SP_ + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1
MODE = sys.argv[2] if len(sys.argv) > 2 else 'render'          # 'search' | 'preview:t,t' | 'render'
DUR = 10.0; NF = int(DUR * FPS); TEND = 8.6; LAUNCH = 0.6
# Oct 29 hookfade pass: boxed band + 'PAUSE WHEN IT'S IN' sub + 'COMMENT YOUR TIME' plate -> one 2-line soft-fade hook that is the instruction
HOOK, HB = hook_fade(["PAUSE WHEN IT'S", 'IN THE BOTTLE'], accent=1, size=64)
PY0 = 557 + 10; PY1 = PY0 + 74                         # pinned to the batch_review layout: the trajectory search uses PY1, so the one valid frame stays put
JAR = Image.open(A + 'jar_melatonin.png').convert('RGBA')
BOT = JAR.copy(); ImageDraw.Draw(BOT).rectangle([0, 0, 540, 67], fill=(0, 0, 0, 0))
S = 1.4; BOT = BOT.resize((int(540 * S), int(540 * S)), Image.NEAREST)          # bottle 1.2 -> 1.4
BX, BY = 300, 1490 - int(520 * S)
TX, TY = BX + int(270 * S), BY + int(78 * S)            # mouth centre
K = 7                                                    # Rayleigh 6x -> 7x
RAY = seq(SP_ + 'fork3/ray_cast', K, 1, 9)
FX0, FY0 = -124, 1490 - 78 * K
OX, OY = FX0 + 59 * K, FY0 + 35 * K                      # staff orb
GUM = gummy('mel', 3)
LX, LY = OX + 70, OY - 150                              # launch point just above the staff (clear of Rayleigh's face)                                    # 2x -> 3x
print('HB', HB, 'mouth', TX, TY, 'orb', OX, OY)
ts = np.arange(NF) / FPS
tau = ts + 0.05 * np.maximum(0, ts - 6.0) ** 2           # speed ramp from 6s (~1.4x by the end)
def allowed(xs, ys):
    gr = GUM.width / 2
    if xs.min() < 70 + gr + 10 or xs.max() > 1025 - gr - 10: return False
    if ys.min() < PY1 + gr + 20 or ys.max() > 1000: return False
    col = (xs > BX + int(150 * S)) & (xs < BX + int(430 * S))
    return not np.any(col & (ys > TY + 4))               # never below the mouth over the bottle (never "inside")
best = None
rng = random.Random(SEED)
for trial in range(20000 if MODE == 'search' or MODE == 'render' or MODE.startswith('preview') else 0):
    fx = rng.uniform(0.35, 0.8); fx2 = rng.uniform(0.9, 1.6); fy = rng.uniform(0.45, 1.0); fy2 = rng.uniform(1.0, 1.9)
    ax, ax2 = rng.uniform(170, 250), rng.uniform(30, 90); ay, ay2 = rng.uniform(50, 85), rng.uniform(12, 35)
    p = [rng.uniform(0, 6.28) for _ in range(4)]
    cx0, cy0 = rng.uniform(540, 640), rng.uniform(770, 805)
    xs = cx0 + ax * np.sin(2 * np.pi * fx * tau + p[0]) + ax2 * np.sin(2 * np.pi * fx2 * tau + p[1])
    ys = cy0 + ay * np.sin(2 * np.pi * fy * tau + p[2]) + ay2 * np.sin(2 * np.pi * fy2 * tau + p[3])
    valid = (ts < TEND) & (ts > 2.2)
    d = np.hypot(xs - TX, ys - TY); dv = np.where(valid, d, 9e9)
    k = int(np.argmin(dv))
    if dv[k] > 55: continue
    g = np.exp(-((ts - ts[k]) / 0.12) ** 2); xs = xs + (TX - xs[k]) * g; ys = ys + (TY - ys[k]) * g
    # launch from the staff orb on frame 0
    w = np.clip(ts / LAUNCH, 0, 1); w = w * w * (3 - 2 * w)
    xs = LX + (xs - LX) * w; ys = LY + (ys - LY) * w
    xs[ts >= TEND] = xs[ts < TEND][-1]; ys[ts >= TEND] = ys[ts < TEND][-1]
    if not allowed(xs[ts > LAUNCH], ys[ts > LAUNCH]): continue
    d = np.hypot(xs - TX, ys - TY); d2 = d.copy(); d2[k] = 9e9
    miss = d2.min()
    if miss < 45: continue
    # near-miss passes: local minima of distance under 130px, at speed, outside +-0.4s of the hit
    sp = np.hypot(np.diff(xs, prepend=xs[0]), np.diff(ys, prepend=ys[0]))
    mins = [i for i in range(1, int(TEND * FPS) - 1) if d[i] <= d[i - 1] and d[i] <= d[i + 1] and d[i] < 130 and abs(i - k) > 12 and sp[i] > 9]
    passes = []
    for i in mins:
        if not passes or i - passes[-1] > 24: passes.append(i)
    if len(passes) < 3: continue
    late = any(p_ / FPS > 6.0 for p_ in passes)
    sc = miss + 10 * min(len(passes), 5) + (15 if late else 0)
    if best is None or sc > best[0]: best = (sc, k, xs.copy(), ys.copy(), miss, passes)
sc, KM, XS, YS, MISS, PASSES = best
print('match frame', KM, round(KM / FPS, 2), 'nearest other', round(MISS), 'near passes', [(round(p_ / FPS, 2), round(float(np.hypot(XS[p_] - TX, YS[p_] - TY)))) for p_ in PASSES])
if MODE == 'search': sys.exit()
BG = bg_frames('recov_hd.gif', (3413, 1920), step=2, bright=0.85)
BG = [b.crop((1166, 0, 1166 + W, H)) for b in BG]
PLATE = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PLATE)
pd.rounded_rectangle([200, PY0, 880, PY1], 18, fill=(14, 10, 24, 225), outline=(190, 120, 255, 255), width=4)
ctext(pd, 540, PY0 + 15, 'COMMENT YOUR TIME', F(44), (255, 255, 255), 6)
frames = [int(round(float(x) * FPS)) for x in MODE.split(':')[1].split(',')] if MODE.startswith('preview') else range(NF)
w = None if MODE.startswith('preview') else Writer('v26_noaudio.mp4'); ev = [(0.0, 'sword_swish')]
trail = []
def pos(f): return XS[min(f, NF - 1)], YS[min(f, NF - 1)]
for f in frames:
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: d.ellipse([BX + 120, BY + int(520 * S) - 60, BX + int(430 * S) + 40, BY + int(520 * S) + 50], fill=(140, 90, 255, 70)))
    img.alpha_composite(BOT, (BX, BY))
    rf = RAY[int(t * 8) % len(RAY)]
    img.alpha_composite(rf, (FX0, FY0))
    gx, gy = pos(f)
    hold = t >= TEND
    end_fade = max(0.0, (t - (DUR - 0.3)) / 0.3)            # gummy dissolves at the end; frame 0 starts at the orb
    tr = [pos(max(0, f - i)) for i in range(1, 9)] if not hold else []
    def magic(d):
        if not hold:
            for i in range(24):
                u = i / 23; mx = OX + (gx - OX) * u + 26 * math.sin(t * 9 + u * 9) * math.sin(math.pi * u); my = OY + (gy - OY) * u + 26 * math.cos(t * 7 + u * 8) * math.sin(math.pi * u)
                r = 6 + 3 * math.sin(t * 12 + i); d.ellipse([mx - r - 3, my - r - 3, mx + r + 3, my + r + 3], fill=(190, 110, 255, 70)); d.ellipse([mx - r / 2, my - r / 2, mx + r / 2, my + r / 2], fill=(255, 235, 255, 200))
        d.ellipse([OX - 30, OY - 30, OX + 30, OY + 30], fill=(220, 150, 255, 110 + int(100 * end_fade)))
        # glowing comet trail behind the gummy so the eye can follow it
        for i, (tx_, ty_) in enumerate(tr):
            r = 34 - i * 3.2; a = int(150 * (1 - i / 9))
            d.ellipse([tx_ - r, ty_ - r, tx_ + r, ty_ + r], fill=(255, 190, 120, a // 2))
            d.ellipse([tx_ - r * 0.45, ty_ - r * 0.45, tx_ + r * 0.45, ty_ + r * 0.45], fill=(255, 240, 210, a))
        d.ellipse([gx - 66, gy - 66, gx + 66, gy + 66], fill=(255, 170, 90, 45))
    layer(img, magic)
    g = GUM
    if end_fade > 0:
        g = GUM.copy(); g.putalpha(g.getchannel('A').point(lambda p: int(p * (1 - end_fade))))
    img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    if hold:
        u = t - TEND; sc = 1 + 0.3 * max(0, 1 - u / 0.12); a = 255 if end_fade == 0 else int(255 * (1 - end_fade))
        text_layer(img, [(540, HB + 70 - int(60 * sc) // 2, 'DID YOU GET IT?', int(60 * sc), (255, 214, 60), 9, a)])
    img.alpha_composite(HOOK)
    if MODE.startswith('preview'): img.convert('RGB').save(f'p_{f:03d}.png')
    else: w.write(img)
if not MODE.startswith('preview'):
    ev += [(round(TEND, 3), 'ding_8bit'), (round(DUR - 0.3, 3), 'twinkle')]
    w.close(); json.dump({'events': ev}, open('v26_events.json', 'w'))
    json.dump({'match_frame': KM, 'nearest_other_px': float(MISS)}, open('v26_match.json', 'w')); print('done')
