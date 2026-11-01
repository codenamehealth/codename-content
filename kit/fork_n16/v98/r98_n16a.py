# #98 Will he get squished (file 098_the_cleanest_trap_ever) -- fork_n16 Oct 29 notes2 (Bennett: "love it, but have some more
# suspense, like his foot gets stuck or something. everyone knows whats going to happen here").
# Source fork_hfg11/v98/r98.py. Same board, route, hook, MADE IT! and end question. New:
#  - a green goo splat (pixellab/race/slime_splat_c/04, the slime-splat art) sits on his route at (4,2), visible from frame 0;
#    he steps in it and his foot sticks: he stops, '!' pops, he tugs three times (walk cycle in place, body springs forward and
#    is pulled back by stretching goo strands, damped spring), the tile behind him slams shut (no way back) and a block's
#    shadow grows on HIS tile; the block falls from high above with the same gravity as every other block; on the last tug
#    he pops free (goo snaps), lurches one tile and the block slams the goo tile a hair behind him (brief 0.4x slow-mo
#    around the pop, CLOSE!). Then the route continues as before to PERFECT GAP and MADE IT!.
#  - every block falls with one gravity (z = g u^2 / 2, g = 8490 px/s^2, same curve the old 0.35s / 520px drop used);
#    draw order is now by board row (a falling block is drawn over the rows behind it and the Hollow on its own row),
#    fixing falling blocks that slid behind landed ones.
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['WILL HE GET', 'SQUISHED?'], accent=1, size=72); HOOK2, _ = hook_fade(['WOULD YOU HAVE', 'SURVIVED?'], accent=1, size=72); print('hook bottom', HB)
OUT = SP + 'fork_n16/v98/'
G = SP + 'fork_a10/gen/'
CC, RR, S = 6, 7, 128
BX, BY = 94, 566
court = wang(G + 'court_meta.json', G + 'court_sheet.png')
FLAG = up(court[(True, True, True, True)], 3)
BASE = Image.new('RGBA', (W, H), (30, 60, 30, 255))
ox_, oy_ = BX % FLAG.width - FLAG.width, BY % FLAG.height - FLAG.height
for y in range(oy_, H, FLAG.height):
    for x in range(ox_, W, FLAG.width):
        fl = FLAG if ((x - BX) // 96 + (y - BY) // 96) % 2 else FLAG.transpose(Image.FLIP_LEFT_RIGHT); BASE.alpha_composite(fl, (x, y))
def frame_board(d):
    for c in range(1, CC): d.line([BX + c * S, BY, BX + c * S, BY + RR * S], fill=(255, 255, 255, 45), width=2)
    for r in range(1, RR): d.line([BX, BY + r * S, BX + CC * S, BY + r * S], fill=(255, 255, 255, 45), width=2)
layer(BASE, frame_board)
def make_block():
    n = S // 4; lip = 5; im = Image.new('RGBA', (n, n + lip), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, n - 1, n + lip - 1], fill=(36, 34, 48, 255))
    d.rectangle([1, 1, n - 2, n - 2], fill=(132, 136, 156, 255))
    d.rectangle([1, n - 1, n - 2, n + lip - 2], fill=(84, 86, 106, 255))
    d.line([1, 1, n - 2, 1], fill=(186, 190, 206, 255)); d.line([1, 1, 1, n - 2], fill=(170, 174, 192, 255))
    for (x0, y0, x1, y1) in ((4, 5, 13, 11), (17, 4, 27, 10), (6, 16, 16, 23), (20, 15, 27, 24), (9, 26, 24, 28)):
        d.rectangle([x0, y0, x1, y1], outline=(108, 110, 132, 255))
    d.rectangle([n // 2 - 3, n // 2 - 3, n // 2 + 2, n // 2 + 2], fill=(70, 130, 232, 255)); d.point((n // 2 - 2, n // 2 - 2), fill=(170, 210, 255, 255))
    d.rectangle([n // 2 - 4, n // 2 - 4, n // 2 + 3, n // 2 + 3], outline=(255, 214, 60, 255))
    return up(im, 4)
BLOCK = make_block(); LIP = BLOCK.height - S
def cell_xy(p): return (BX + p[1] * S + S / 2, BY + p[0] * S + S / 2)
HH = 190
HF = gif_frames(A + 'hollow-walk-front.gif', h=HH); HS = gif_frames(A + 'hollow-walk-side.gif', h=HH)
HSL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in HS]; HVIC = vic('hollow', 210)
GUM = gummy('cre', 4)
GOO = up(nored(Image.open(PL + 'race/slime_splat_c/04.png').convert('RGBA')).crop((6, 8, 58, 60)), 2)
GRAV = 8490.0                         # px/s^2 in screen space: z(u) = 0.5 g u^2 (identical to the old 520px in 0.35s curve)
def z_of(u): return 0.5 * GRAV * u * u
# ---- route and timing (sim time)
P = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)]
GOAL = P[-1]; NS = len(P) - 1
T0, TURN = 0.2, 0.56
KS = 10                              # stuck on P[10] = (4,2), the goo tile
D = float(os.environ.get('STUCK', '1.35'))
LURCH = 0.14                         # pop-free burst to the next tile
def at(i): return T0 + i * TURN + (D if i >= KS else 0.0)     # departure time from P[i]
T_IN = at(KS - 1) + 0.85 * TURN      # foot lands in the goo
T_FREE = at(KS)                      # pops free
T_SUS = T_FREE + 0.35                # suspense block lands on the goo tile: its underside passes his head height (190px) just as his back clears the tile
T_ARR = at(NS - 1) + 0.85 * TURN; END = T_ARR + 1.6
def adj(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
pathset = set(P); DROP = {}
T_PERF = at(NS - 1) + 0.2
for r in range(RR):
    for c in range(CC):
        q = (r, c)
        if q in pathset: continue
        near = [i for i, p in enumerate(P) if adj(p, q)]
        DROP[q] = (at(near[0]) + 0.22) if near else None
far = sorted([q for q, v in DROP.items() if v is None], key=lambda q: (q[0], q[1]))
for k, q in enumerate(far): DROP[q] = T0 + 0.1 + k * 0.33
for q in list(DROP):
    if DROP[q] > at(NS - 2) + 0.1: DROP[q] = T_PERF
for q in [(5, 3), (5, 5), (6, 3), (6, 5)]: DROP[q] = T_PERF
for i, p in enumerate(P[:-1]): DROP[p] = min(at(i + 2) + 0.25, T_PERF + 0.5) if i + 2 <= NS else T_PERF + 0.5
DROP[P[KS - 1]] = T_IN + 0.45        # the tile he came from slams while he is stuck: no way back
DROP[P[KS]] = T_SUS                  # the goo tile: the suspense block
# no other block lands within 0.5s of the suspense block (one beat at a time)
for q in DROP:
    if q != P[KS] and abs(DROP[q] - T_SUS) < 0.5 and DROP[q] < T_PERF: DROP[q] = T_SUS + 0.5 if DROP[q] > T_SUS else T_SUS - 0.5
DROP[(5, 2)] = T_SUS + 0.5         # the tile in front of the goo waits until he has moved on (a block falling there would pass in front of him while he is stuck)
assert GOAL not in DROP
for q in DROP:
    if q in pathset: assert DROP[q] > at(P.index(q)) + 0.15, (q, DROP[q], at(P.index(q)))
EVENTS = sorted((t, q) for q, t in DROP.items())
SUS_FALL = T_SUS - (T_IN + 0.3)      # suspense block: shadow from 0.3s after the foot sticks
print('steps', NS, 'stuck', round(T_IN, 2), '->', round(T_FREE, 2), 'sus lands', round(T_SUS, 2), 'perfect', round(T_PERF, 2), 'arrive', round(T_ARR, 2), 'end', round(END, 2), 'blocks', len(DROP))
TUGS = [(T_IN + 0.25, 12), (T_IN + 0.68, 16), (T_IN + 1.08, 20)]
def tug_off(t):
    o = 0.0
    for t0, a in TUGS:
        u = t - t0
        if u >= 0: o += a * math.exp(-5.5 * u) * math.sin(2 * math.pi * u / 0.34)   # pulled forward, goo springs him back (damped)
    return o
def hollow_state(t):
    """(x, y), move dir, stuck flag"""
    if t < T0: return cell_xy(P[0]), None, False
    for k in range(NS):
        if at(k) <= t < at(k + 1):
            a, b = cell_xy(P[k]), cell_xy(P[k + 1]); d = (P[k + 1][0] - P[k][0], P[k + 1][1] - P[k][1])
            dur = LURCH if k == KS else 0.85 * TURN
            u = min(1.0, (t - at(k)) / dur)
            if k == KS: u = 1 - (1 - u) ** 2          # burst out of the goo, then he's walking again
            pos = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
            if k == KS - 1 and t >= T_IN: return (cell_xy(P[KS])[0] + tug_off(t), cell_xy(P[KS])[1]), (0, 1), True
            return pos, d, False
    return cell_xy(P[-1]), None, False
# ---- time warp: brief 0.4x slow-mo around the pop-free (sim time ts per video frame)
SA, SB, RSM, RMP = T_FREE - 0.45, T_SUS + 0.1, 0.4, 0.12
def rate(ts):
    if ts < SA - RMP or ts > SB + RMP: return 1.0
    if ts < SA: return 1 - (1 - RSM) * (ts - (SA - RMP)) / RMP
    if ts <= SB: return RSM
    return RSM + (1 - RSM) * (ts - SB) / RMP
TS = [0.0]
while TS[-1] < END: TS.append(TS[-1] + rate(TS[-1]) / FPS)
NF = len(TS) - 1
def vtime(ts):   # sim time -> video time
    for f in range(len(TS) - 1):
        if TS[f + 1] > ts: return (f + (ts - TS[f]) / (TS[f + 1] - TS[f])) / FPS
    return NF / FPS
print('frames', NF, 'video s', round(NF / FPS, 2))
w = Writer(OUT + 'noaudio.mp4'); ev = []
last_pop = -9; pops = []
for td, q in EVENTS:
    if q == P[KS]: pops.append((td + 0.04, 'CLOSE!')); last_pop = td; continue
    if q in pathset and q != P[KS - 1] and td < T_PERF and td - last_pop > 1.3 and abs(td - T_SUS) > 1.0:
        pops.append((td + 0.1, 'CLOSE!')); last_pop = td
gx, gy = cell_xy(GOAL); kx, ky = cell_xy(P[KS])
FRS = [int(x) for x in os.environ['ONLY'].split(',')] if os.environ.get('ONLY') else range(NF)
KEEP = set(int(x) for x in os.environ.get('KEYS', '').split(',') if x)
for f in FRS:
    t = TS[f]; vt = f / FPS
    img = BASE.copy()
    # goo on the tile until the suspense block covers it
    if t < T_SUS:
        img.alpha_composite(GOO, (int(kx - GOO.width / 2), int(ky - GOO.height / 2 + 6)))
    if t < T_ARR:
        layer(img, lambda d2: d2.ellipse([gx - 58, gy - 58, gx + 58, gy + 58], fill=(120, 190, 255, int(70 + 30 * math.sin(t * 6)))))
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy + 40 - GUM.height)))
    (hx, hy), mv, stuck = hollow_state(t)
    # shadows (grow as the block comes down; the suspense block's shadow starts early because it falls from much higher)
    def shadows(d2):
        for td, q in EVENTS:
            lead = SUS_FALL if q == P[KS] else 0.35
            u = t - td
            if -lead <= u < 0:
                x, y = cell_xy(q); p_ = 1 - (-u) / lead
                if q == P[KS]:   # the big one: a block-sized shadow darkening around him as it comes down
                    hs = 20 + 44 * p_ ** 1.2
                    d2.rounded_rectangle([x - hs, y - hs * 0.8 + 10, x + hs, y + hs * 0.8 + 10], 10, fill=(0, 0, 0, int(40 + 150 * p_)))
                else:
                    s = 14 + 46 * p_ ** 1.5
                    d2.ellipse([x - s, y - s * 0.6, x + s, y + s * 0.6], fill=(0, 0, 0, int(50 + 140 * p_)))
    layer(img, shadows)
    shake = 0
    items = []   # (sort key, kind, payload)
    for td, q in EVENTS:
        u = t - td; x, y = cell_xy(q)
        if u < 0:
            zz = z_of(-u)
            if y - S / 2 - LIP - zz + BLOCK.height > HB: items.append((y, 1, (q, td, zz)))
        else: items.append((y, 0, (q, td, 0.0)))
    items.append((hy, 0.5, None))
    items.sort(key=lambda it: (it[0], it[1]))
    for key, kind, pl in items:
        if pl is None:
            if t >= T_ARR:
                fr = HVIC[int((t - T_ARR) * 8) % len(HVIC)]
                img.alpha_composite(fr, (int(hx - fr.width / 2), int(hy + 50 - fr.height)))
            else:
                if stuck: fr = HS[int(t * 12) % 6]
                elif mv is None: fr = HF[0]
                elif mv[0] > 0: fr = HF[int(t * 10) % 6]
                elif mv[1] > 0: fr = HS[int(t * 10) % 6]
                else: fr = HSL[int(t * 10) % 6]
                layer(img, lambda d2: d2.ellipse([hx - 40, hy + 38, hx + 40, hy + 56], fill=(0, 0, 0, 90)))
                # goo strands from the splat to his trailing foot while stuck, snapping just after he pops free
                if T_IN <= t < T_FREE + 0.05:
                    def strands(d2):
                        fx = hx - 18; fy = hy + 44
                        for k_, dy_ in enumerate((-6, 2, 10)):
                            d2.line([kx - 30 + k_ * 8, ky + 34 + dy_, fx, fy + dy_ * 0.5], fill=(20, 70, 20, 255), width=9 if t < T_FREE else 5)
                            d2.line([kx - 30 + k_ * 8, ky + 34 + dy_, fx, fy + dy_ * 0.5], fill=(140, 235, 110, 255), width=5 if t < T_FREE else 2)
                    layer(img, strands)
                img.alpha_composite(fr, (int(hx - fr.width / 2), int(hy + 50 - fr.height)))
                if T_IN + 0.05 <= t < T_IN + 0.6:   # '!' emote
                    text_layer(img, [(hx, hy - HH + 10 - 70, '!', 72, (255, 255, 255), 9, 255)])
                if T_IN + 0.65 <= t < T_FREE:       # sweat drop
                    sx_, sy_ = hx + 52, hy - HH + 70 + 30 * ((t - T_IN - 0.65) % 0.5)
                    layer(img, lambda d2: (d2.ellipse([sx_ - 9, sy_ - 4, sx_ + 9, sy_ + 18], fill=(150, 210, 255, 230), outline=(30, 40, 70, 255), width=3), d2.polygon([(sx_, sy_ - 16), (sx_ - 8, sy_ + 2), (sx_ + 8, sy_ + 2)], fill=(150, 210, 255, 230))))
            continue
        q, td, zz = pl; x, y = cell_xy(q); x0, y0 = int(x - S / 2), int(y - S / 2 - LIP)
        if kind == 1:
            yy_ = int(y0 - zz)
            cut_ = max(0, HB - yy_)
            img.alpha_composite(BLOCK.crop((0, cut_, BLOCK.width, BLOCK.height)), (x0, yy_ + cut_))
        else:
            u = t - td
            img.alpha_composite(BLOCK, (x0, y0))
            if u < 0.45:
                goo = q == P[KS]
                def dust(d2, x=x, y=y, u=u, goo=goo):
                    for k in range(8):
                        a = k * 0.785; rr = 60 + 70 * u
                        col = (100, 210, 80, int(230 * (1 - u / 0.45))) if goo and k % 2 else (220, 210, 190, int(190 * (1 - u / 0.45)))
                        d2.rectangle([x + rr * math.cos(a) - 9, y + S / 2 - 10 + rr * 0.35 * math.sin(a) - 9, x + rr * math.cos(a) + 9, y + S / 2 - 10 + rr * 0.35 * math.sin(a) + 9], fill=col)
                layer(img, dust)
            if u < 0.12: shake = max(shake, 9 if (abs(td - T_PERF) < 0.01 or q == P[KS]) else 4)
    # sound events (video time)
    if f == 0: pass
    for tp, txt in pops:
        u = t - tp
        if 0 <= u < 0.75:
            a = int(255 * min(1, (0.75 - u) / 0.25)); k_ = 1.2 - 0.2 * min(1, u / 0.1); fs = int(60 * k_)
            px_ = min(max(hx, 120 + 190), 850 - 190); py_ = hy - 260 if hy > 900 else hy + 90
            layer(img, lambda d2, px_=px_, py_=py_, a=a, fs=fs, txt=txt: ctext(d2, px_, py_, txt, F(fs), (255, 90, 90), 9, a))
    if T_PERF <= t < T_ARR + 0.3:
        u = t - T_PERF; s = 1.3 - 0.3 * min(1, u / 0.12); a = int(255 * min(1, u / 0.06)); fs = int(64 * s)
        layer(img, lambda d2, fs=fs, a=a: ctext(d2, 478, 742, 'PERFECT GAP!', F(fs), (255, 214, 60), 10, a))
    if t >= T_ARR:
        u = t - T_ARR; a = int(255 * min(1, max(0, u - 0.4) / 0.2))
        def sparks(d2):
            rr = random.Random(f)
            for _ in range(16):
                an = rr.uniform(0, 6.28); rad = 40 + 150 * min(1, u / 0.6) * rr.uniform(0.5, 1)
                d2.rectangle([gx + rad * math.cos(an) - 6, gy - 70 + rad * 0.8 * math.sin(an) - 6, gx + rad * math.cos(an) + 6, gy - 70 + rad * 0.8 * math.sin(an) + 6], fill=(150, 210, 255, int(230 * max(0, 1 - u / 1.2))))
        layer(img, sparks)
        if u < 1.0: img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - 250 - 50 * u)))
        text_layer(img, [(478, 724, 'MADE IT!', 80, (255, 214, 60), 10, a)])
    if shake: img = img.transform(img.size, Image.AFFINE, (1, 0, random.Random(f).choice([-shake, shake]), 0, 1, 0))
    img.alpha_composite(HOOK2 if t >= T_ARR + 0.4 else HOOK)
    w.write(img)
    if f in KEEP or os.environ.get('ONLY'): img.convert('RGB').save(OUT + f'k_{f:04d}.png')
w.close()
for td, q in EVENTS:
    if abs(td - T_PERF) < 0.01: continue
    ev.append((round(vtime(td), 3), 'stomp_8bit' if q == P[KS] else 'brick_8bit'))
ev += [(round(vtime(T_PERF), 3), 'boom'), (round(vtime(T_IN), 3), 'squish'), (round(vtime(T_FREE), 3), 'boing'),
       (round(vtime(T_ARR), 3), 'powerup_8bit'), (round(vtime(T_ARR + 0.4), 3), 'victory')]
json.dump({'events': sorted(ev)}, open(OUT + 'ev.json', 'w'))
print('done', NF, 'T_IN', round(vtime(T_IN), 2), 'T_FREE', round(vtime(T_FREE), 2), 'sus', round(vtime(T_SUS), 2))
# clearance check: Hollow body (half width 55) vs the goo tile edge when the block lands
tz = T_SUS - math.sqrt(2 * 200 / GRAV)   # moment the block's underside is 200px up (his head height)
(hx, hy), _, _ = hollow_state(tz); print('when the block underside reaches head height the Hollow back is', round(hx - 55 - (kx + S / 2), 1), 'px past the tile edge')
for tt in [T_SUS - 0.5 + k * 0.05 for k in range(12)]:
    (hx, hy), _, _ = hollow_state(tt); zz = z_of(max(0, T_SUS - tt)); print(' t', round(tt - T_SUS, 2), 'z', round(zz), 'back edge vs tile edge', round(hx - 55 - (kx + S / 2), 1))
