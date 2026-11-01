import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #79 safe-zone + hook pass (source: fork_a8/v81/render.py)
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# rc9 review recut: band with a 46px sub line (comment bait) built like hook.py
import hook as HK
def band(lines, accent, sub, subsize=46, color=(255, 214, 60)):
    f, s = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=(255, 255, 255), stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h, s
# hfg8: soft fade, no box. The post hook as one sentence over 3 short lines (the dare was a small sub line under the box);
# at TIME'S UP the hook text becomes TIME'S UP! / HOW MANY? in the same fade; COMMENT YOUR COUNT cut (caption asks)
_, HB = HK.hook_fade(["I BET YOU CAN'T", 'FIND 6 MOVING', 'HOLLOWS'], accent=[1, 2])
HOOK, _ = HK.hook_fade(["I BET YOU CAN'T", 'FIND 6 MOVING', 'HOLLOWS'], accent=[1, 2], fade_to=HB + 140)
UPB, UB = HK.hook_fade(["TIME'S UP!", 'HOW MANY', 'DID YOU FIND?'], accent=0, size=72, fade_to=HB + 140); HS = US = 0   # n12 review: 'HOW MANY?' contradicted the hook's 6
print('band', HB, HS, 'up band', UB, US)
BAR_Y = HB + 12; DY = 52  # whole statue field shifted down 52px
BAR_Y0 = 536 + 14  # statue filter keeps the batch_v2 field exactly (same 46 statues, same movers)
print('hook bottom', HB)
T_GO, T_UP, HOLD = 0.3, 9.3, 1.4; DUR = T_UP + HOLD; N = int(round(DUR * FPS)); PER = 1.25
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
# n12 (Bennett Oct 29: "the eating hollow needs to go. i dont like seeing his teeth"): both eating movers are gone, the teeth-baring
# chomp (fork_a3/hollow_chomp) and the gummy-eating one (fork3/hollow_eat); they are replaced, at the same two statue spots, by
# subtle no-teeth movers already used in approved reels: head scratch (fork2/hollow_think) and a small arm sway (fork2/hollow_dance)
MOV = [load(SP + 'fork_b5/hollow_nod', 1), load(SP + 'fork2/hollow_think', 1), load(SP + 'pixellab/maze/anim/hollow_panic', 1),
       load(SP + 'fork2/hollow_dance', 1), load(SP + 'pixellab/maze/anim/hollow_frun', 1), load(SP + 'fork_a4/hollow_sit', 1)]
# ground: PixelLab plaza (cobble + grass) at night
T = wang(PL + 'steal/plaza_meta.json', PL + 'steal/plaza_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
AY0 = 430; TS = 64; GC, GR = 17, 24
def low(i, j):
    x, y = i * TS, AY0 + j * TS
    return (abs(x - 540) < 200 + 40 * math.sin(j * 0.7)) or (abs(y - 1180) < 120 + 30 * math.sin(i * 0.9))
CORN = [[low(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (20, 30, 20, 255))
# hfg8: plaza tiles extended 9 rows up so the plaza runs to the frame top (the moon-sky header strip is gone); same pattern below
EXT = 9; CORN = [[low(i, j - EXT) for i in range(GC + 1)] for j in range(GR + EXT + 1)]
for j in range(GR + EXT):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1]); GROUND.alpha_composite(T[key], (i * TS, AY0 + DY + (j - EXT) * TS))
# header sky: Liza's moon realm
#SKY = bg_frames('bg_moon.gif', (1920, 1080), step=1, bright=0.85)
#SKY = [s.crop((420, 0, 1500, 470)) for s in SKY]
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
FLIP = {id(f): f.transpose(Image.FLIP_LEFT_RIGHT) for fr in MOV for f in fr}
print('orig statues', len(spots), 'movers at', [tuple(int(v) for v in spots[i]) for i in movers])
for sp in spots: sp[1] += DY
def inzone(spr, x, y):
    bb = spr.getbbox(); x0 = int(x - spr.width / 2); y0 = int(y - FOOT)
    X0, Y0, X1, Y1 = x0 + bb[0], y0 + bb[1], x0 + bb[2], y0 + bb[3]
    if X0 < 76 or Y0 < BAR_Y0 + 46 or Y1 > 1500 or X1 > 1019: return False
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
T_MID = (T_GO + T_UP) / 2
w = Writer('v79_noaudio.mp4'); ev = [(0.2, 'chime'), (T_GO, 'go_8bit'), (T_UP, 'buzz_8bit')]
for s_ in range(int(T_UP - T_GO) - 3, int(T_UP - T_GO)): ev.append((round(T_GO + s_ + 1, 3), 'tick_8bit'))
for f in range(N):
    t = f / FPS; img = GROUND.copy()
    layer(img, lambda d: [d.ellipse([spots[i][0] - 30, spots[i][1] - 9, spots[i][0] + 30, spots[i][1] + 9], fill=(0, 0, 0, 90)) for i in ACTIVE])
    for i in sorted(ACTIVE, key=lambda i: spots[i][1]):
        x, y = spots[i]
        if i in MV:
            fr, ph = MV[i]; tb = t + ph * PER / 3.0; nb = int(tb // PER); u = (tb % PER) / PER
            n = len(fr); pp = u / 0.62 if u < 0.62 else 0.0  # anim plays out and back in the first 62% of each beat
            k = int(round((1 - abs(1 - 2 * pp)) * (n - 1))) if u < 0.62 else 0
            spr = fr[k]
            if nb % 2: spr = FLIP[id(spr)]
        else: spr = STAT[i]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    img.alpha_composite(NIGHT)
    layer(img, lambda d: [d.ellipse([W / 2 - r, 700 - r * 0.5, W / 2 + r, 700 + r * 0.5], fill=(200, 220, 255, 10)) for r in (700, 560, 420)])
    layer(img, lambda d: [d.rectangle([x + 20 * math.sin(t * sp + p), y + 14 * math.cos(t * sp * 1.3 + p), x + 20 * math.sin(t * sp + p) + 5, y + 14 * math.cos(t * sp * 1.3 + p) + 5],
                                       fill=(220, 255, 140, int(110 + 110 * math.sin(t * 3 + p)))) for x, y, p, sp in FIRE])
    its = []
    if t < T_UP:
        u = max(0.0, (t - T_GO) / (T_UP - T_GO)); hf = 0 <= t - T_MID < 0.35
        col = (120, 220, 120, 255) if u < 0.5 else (255, 180, 60, 255) if u < 0.8 else (255, 80, 80, 255)
        if hf: col = (255, 255, 255, 255)
        layer(img, lambda d: (d.rounded_rectangle([90, BAR_Y, 1005, BAR_Y + 36], 16, fill=(20, 16, 34, 220), outline=(255, 255, 255, 255) if hf else (255, 214, 60, 255), width=6 if hf else 4),
                              d.rounded_rectangle([98, BAR_Y + 7, 98 + int(899 * (1 - u)), BAR_Y + 29], 10, fill=col)))
    img.alpha_composite(UPB if t >= T_UP else HOOK)
    w.write(img)
    if f in (0, int(T_MID * FPS) + 3, N - 1): img.convert('RGB').save(f'f79_{f}.png')
w.close(); json.dump({'events': ev}, open('v79_ev.json', 'w')); print('done', DUR, ev)
