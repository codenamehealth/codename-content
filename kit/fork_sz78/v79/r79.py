import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #79 safe-zone + hook pass (source: fork_a8/v81/render.py)
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
HOOK, HB = hook_layer(['FIND 6 MOVING', 'HOLLOWS'], accent=0, sub="I BET YOU CAN'T")
BAR_Y = HB + 14; DY = 52  # whole statue field shifted down 52px
print('hook bottom', HB)
DUR = 13.0; N = int(DUR * FPS); T_GO, T_UP = 1.6, 11.0
SS = 2; FOOT = 78 * SS
def stone(im):
    a = np.array(im).astype(float); m = a[..., 3] > 0
    L = a[..., :3].mean(-1); lo, hi = 10, 200; v = np.clip((L - lo) / (hi - lo), 0, 1) ** 0.8
    out = a.copy(); out[..., 0] = 78 + 125 * v; out[..., 1] = 82 + 122 * v; out[..., 2] = 92 + 118 * v
    out[~m] = 0; out[..., 3] = a[..., 3]; return Image.fromarray(out.astype('uint8'), 'RGBA')
def load(d, lo=0, hi=None): return [stone(up(Image.open(p).convert('RGBA'), SS)) for p in sorted(glob.glob(d + '/*.png'))[lo:hi]]
POSES = [stone(up(Image.open(SP + f'syeda_src/hollow/{n}').convert('RGBA'), SS)) for n in ['char1.png', 'char2.png', 'char3.png', 'char26.png', 'char27.png', 'char28.png']]
POSES = [p for p in POSES if p.size == (184, 184)]
POSES += [p.transpose(Image.FLIP_LEFT_RIGHT) for p in POSES[1:3]]
POSES += [load(SP + 'fork_a4/hollow_sit')[-1], load(SP + 'fork_b5/hollow_nod')[0]]
MOV = [load(SP + 'fork_b5/hollow_nod', 1), load(SP + 'fork3/hollow_eat', 1), load(SP + 'pixellab/maze/anim/hollow_panic', 1),
       load(SP + 'fork_a3/hollow_chomp', 1), load(SP + 'pixellab/maze/anim/hollow_frun', 1), load(SP + 'fork_a4/hollow_sit', 1)]
# ground: PixelLab plaza (cobble + grass) at night
T = wang(PL + 'steal/plaza_meta.json', PL + 'steal/plaza_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
AY0 = 430; TS = 64; GC, GR = 17, 24
def low(i, j):
    x, y = i * TS, AY0 + j * TS
    return (abs(x - 540) < 200 + 40 * math.sin(j * 0.7)) or (abs(y - 1180) < 120 + 30 * math.sin(i * 0.9))
CORN = [[low(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (20, 30, 20, 255))
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1]); GROUND.alpha_composite(T[key], (i * TS, AY0 + DY + j * TS))
# header sky: Liza's moon realm
SKY = bg_frames('bg_moon.gif', (1920, 1080), step=1, bright=0.85)
SKY = [s.crop((420, 0, 1500, 470)) for s in SKY]
# place statues on a jittered grid
rng = random.Random(21); spots = []
for r in range(12):
    for c in range(8):
        x = 70 + c * 134 + (67 if r % 2 else 0) + rng.uniform(-18, 18); y = AY0 + 150 + r * 108 + rng.uniform(-14, 14)
        if x < 60 or x > W - 60: continue
        spots.append([x, y])
movers = rng.sample(range(len(spots)), 6)
STAT = {i: rng.choice(POSES) for i in range(len(spots))}
MV = {i: (MOV[k], rng.uniform(0, 3)) for k, i in enumerate(movers)}
print('orig statues', len(spots), 'movers at', [tuple(int(v) for v in spots[i]) for i in movers])
for sp in spots: sp[1] += DY
def inzone(spr, x, y):
    bb = spr.getbbox(); x0 = int(x - spr.width / 2); y0 = int(y - FOOT)
    X0, Y0, X1, Y1 = x0 + bb[0], y0 + bb[1], x0 + bb[2], y0 + bb[3]
    if X0 < 76 or Y0 < BAR_Y + 46 or Y1 > 1500 or X1 > 1019: return False
    if Y1 > 1110 and X1 > 881: return False
    return True
def ok(i):
    x, y = spots[i]
    frs = MV[i][0] if i in MV else [STAT[i]]
    return all(inzone(f, x, y) for f in frs)
keep = [i for i in range(len(spots)) if i not in MV and ok(i)]
for i in list(MV):
    if not ok(i):  # relocate this mover to the nearest statue spot inside the zone that fits its animation
        ox, oy = spots[i]; fr = MV.pop(i)
        cand = sorted(keep, key=lambda j: (spots[j][0] - ox) ** 2 + (spots[j][1] - oy) ** 2)
        for j in cand:
            MV[j] = fr
            if ok(j): keep.remove(j); print('mover moved', (int(ox), int(oy - DY)), '->', tuple(int(v) for v in spots[j])); break
            del MV[j]
assert len(MV) == 6 and all(ok(i) for i in MV)
spots_all = spots; ACTIVE = sorted(keep + list(MV))
print('statues kept', len(ACTIVE), 'movers at', [tuple(int(v) for v in spots[i]) for i in MV])
rr = random.Random(3); FIRE = [(rr.uniform(0, W), rr.uniform(AY0, H), rr.uniform(0, 6.3), rr.uniform(0.3, 0.8)) for _ in range(28)]
NIGHT = Image.new('RGBA', (W, H), (20, 30, 80, 95))
w = Writer('v79_noaudio.mp4'); ev = [(0.2, 'chime'), (T_GO, 'go_8bit'), (T_UP, 'buzz_8bit')]
for s_ in range(int(T_UP - T_GO) - 3, int(T_UP - T_GO)): ev.append((round(T_GO + s_ + 1, 3), 'tick_8bit'))
for f in range(N):
    t = f / FPS; img = GROUND.copy()
    layer(img, lambda d: [d.ellipse([spots[i][0] - 30, spots[i][1] - 9, spots[i][0] + 30, spots[i][1] + 9], fill=(0, 0, 0, 90)) for i in ACTIVE])
    for i in sorted(ACTIVE, key=lambda i: spots[i][1]):
        x, y = spots[i]
        if i in MV:
            fr, ph = MV[i]; u = (t * 0.9 + ph) % 3.0
            k = int(u / 3.0 * len(fr) * 2) % len(fr) if t > T_GO - 0.6 else 0
            spr = fr[k]
        else: spr = STAT[i]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    img.alpha_composite(NIGHT)
    layer(img, lambda d: [d.ellipse([W / 2 - r, 700 - r * 0.5, W / 2 + r, 700 + r * 0.5], fill=(200, 220, 255, 10)) for r in (700, 560, 420)])
    layer(img, lambda d: [d.rectangle([x + 20 * math.sin(t * sp + p), y + 14 * math.cos(t * sp * 1.3 + p), x + 20 * math.sin(t * sp + p) + 5, y + 14 * math.cos(t * sp * 1.3 + p) + 5],
                                       fill=(220, 255, 140, int(110 + 110 * math.sin(t * 3 + p)))) for x, y, p, sp in FIRE])
    img.alpha_composite(SKY[int(t * 6) % len(SKY)], (0, 0))
    layer(img, lambda d: d.rectangle([0, 0, W, 470], fill=(10, 10, 30, 70)))
    its = []
    if T_GO <= t < T_UP:
        u = (t - T_GO) / (T_UP - T_GO)
        layer(img, lambda d: (d.rounded_rectangle([90, BAR_Y, 1005, BAR_Y + 36], 16, fill=(20, 16, 34, 220), outline=(255, 214, 60, 255), width=4),
                              d.rounded_rectangle([98, BAR_Y + 7, 98 + int(899 * (1 - u)), BAR_Y + 29], 10, fill=(120, 220, 120, 255) if u < 0.6 else (255, 180, 60, 255) if u < 0.85 else (255, 80, 80, 255))))
    if t < T_GO + 0.3:
        its.append((547, 1010, 'They look like statues...', 36, (255, 255, 255), 7, 255))
    if t >= T_UP:
        a = int(255 * min(1, (t - T_UP) / 0.3))
        layer(img, lambda d: d.rounded_rectangle([108, 880, 848, 1090], 24, fill=(20, 16, 34, int(225 * a / 255)), outline=(255, 214, 60, a), width=5))
        its += [(478, 912, "TIME'S UP!", 60, (255, 214, 60), 7, a), (478, 1012, 'How many did you find?', 32, (255, 255, 255), 5, a)]
    text_layer(img, its)
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (0, int(5 * FPS), 370): img.convert('RGB').save(f'f79_{f}.png')
w.close(); print('done')
