# n03 box maze, rebuild 2 (Bennett: "the point of the box race is that they bounce, the characters don't control where they go;
# the door shouldn't open, they should have to break it; same format as the posted video").
# Format of viral_dl/1118_2000_outrun_the_shadow.mp4: 3-2-1-GO, four face boxes each in a top chamber behind a guild-coloured brick wall,
# at GO they are launched and bounce passively (constant speed, reflecting off walls, motion trail), they break their brick walls by hitting
# them, the shadow floods in from the top (stepped edge, eyes), any box it touches is OUT (roster card crossed), one pickup on the floor
# (here a STRENGTH gummy: bricks break in one hit), the exit by the dragon is blocked by a brick wall the boxes must break, first box
# through the checkered exit wins, winner card (Syeda victory pose, NAME WINS!, DID YOUR GUIDE WIN?).
# New maze layout and seed (Bennett: same format, the run plays out differently). Clean physics: axis-separated, sub-stepped AABB
# collision against wall tiles and brick walls (no tunnelling), equal-mass elastic box-box contacts resolved on the least-penetration
# axis (never overlapping), constant speed, bricks crack then shatter into debris that slides and settles on the floor.
import sys, os
S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S_ + 'fork1'); from common import *
sys.path.insert(0, S_ + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
from collections import deque
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (100, 200, 70), 'cleo': (70, 135, 255), 'cyrus': (255, 145, 30), 'ray': (180, 95, 235)}
HOOK, HB = hook_fade(['WHO ESCAPES', 'THE SHADOW?'], accent=1)
C = 48
MAP = [
    "##################",
    "#111#222#333#444##",
    "#111#222#333#444##",
    "#111#222#333#444##",
    "#ggg#ggg#ggg#ggg##",
    "#................#",
    "#................#",
    "#...##########...#",
    "#...#........#...#",
    "#...#........#...#",
    "#...#..####..#...#",
    "#...#..####..#...#",
    "#......####......#",
    "#......####......#",
    "####...####...####",
    "#......####......#",
    "#................#",
    "#......bbbb......#",
    "#######EEEE#######",
    "#######EEEE#######",
    "#######EEEE#######",
    "##################"]
ROWS, COLS = len(MAP), len(MAP[0])
OX = (W - COLS * C) // 2; OY = int(os.environ.get('OY', '468'))
CH = {'joy': 1, 'cleo': 5, 'cyrus': 9, 'ray': 13}          # chamber left column per guide (set per seed below)
def is_wall(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or MAP[r][c] == '#'
# breakable walls: four gates (row 4) + the exit wall (row 17)
BRK0 = {}
for k, c0 in enumerate([1, 5, 9, 13]): BRK0['gate%d' % k] = dict(rect=(OX + c0 * C, OY + 4 * C, OX + (c0 + 3) * C, OY + 5 * C), hp=3)
BRK0['exit'] = dict(rect=(OX + 7 * C, OY + 17 * C, OX + 11 * C, OY + 18 * C), hp=int(os.environ.get('EXHP', '5')))
EXIT_Y = OY + 18 * C                                        # crossing into the checkered exit
GUM_POS = (OX + 2.0 * C, OY + 15.5 * C) if os.environ.get('GUMPOS', 'L') == 'L' else (OX + 16.0 * C, OY + 15.5 * C)
HS = 26
SPD = float(os.environ.get('SPD', '360'))
SUB = 8
T_GO = 2.1
def solids_near(x, y, B):
    out = []
    r0, r1 = int((y - HS - OY) // C) - 1, int((y + HS - OY) // C) + 1
    c0, c1 = int((x - HS - OX) // C) - 1, int((x + HS - OX) // C) + 1
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if is_wall(r, c): out.append((OX + c * C, OY + r * C, OX + c * C + C, OY + r * C + C, None))
    for k, b in B.items():
        if b['hp'] > 0:
            x0, y0, x1, y1 = b['rect']
            if x1 > x - HS - 60 and x0 < x + HS + 60 and y1 > y - HS - 60 and y0 < y + HS + 60: out.append((x0, y0, x1, y1, k))
    return out
def sim(seed, dur=float(os.environ.get('SIMDUR', '26'))):
    rnd = random.Random(seed)
    order = G[:]; rnd.shuffle(order)
    for i, g in enumerate(order): CH[g] = [1, 5, 9, 13][i]
    B = {k: dict(v) for k, v in BRK0.items()}
    for k in B: B[k]['hits'] = []; B[k]['broke'] = None
    X = {}
    for g in G:
        cx = OX + (CH[g] + 1.5) * C; cy = OY + 2.5 * C
        a = rnd.uniform(0.25, 1.32) * (1 if rnd.random() < 0.5 else -1) + (math.pi if rnd.random() < 0.35 else 0)
        X[g] = dict(x=cx + rnd.uniform(-30, 30), y=cy + rnd.uniform(-25, 25), vx=SPD * math.cos(a + math.pi / 2), vy=SPD * math.sin(a + math.pi / 2),
                    out=None, won=None, strong=False, last={})
    gum = dict(x=GUM_POS[0], y=GUM_POS[1], t=None, who=None)
    sh0, shv, sha = float(os.environ.get('SH0', '4.6')), float(os.environ.get('SHV', '3.4')), float(os.environ.get('SHA', '0.62'))
    ev = []; frames = []; wallhits = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS / SUB
        for _ in range(SUB if t >= T_GO else 0):
            for g in G:
                p = X[g]
                if p['out'] is not None or p['won'] is not None: continue
                for axis in ('x', 'y'):
                    p[axis] += p['v' + axis] * dt
                    for (x0, y0, x1, y1, k) in solids_near(p['x'], p['y'], B):
                        if p['x'] + HS <= x0 or p['x'] - HS >= x1 or p['y'] + HS <= y0 or p['y'] - HS >= y1: continue
                        if k is not None and B[k]['hp'] <= 0: continue
                        v = p['v' + axis]
                        if axis == 'x':
                            if v > 0: p['x'] = x0 - HS
                            elif v < 0: p['x'] = x1 + HS
                        else:
                            if v > 0: p['y'] = y0 - HS
                            elif v < 0: p['y'] = y1 + HS
                        if v != 0:
                            p['v' + axis] = -v
                            # tiny surface imperfection (+-2.5 deg) so no box locks into a perfectly periodic orbit
                            ang = rnd.uniform(-0.044, 0.044); vx, vy = p['vx'], p['vy']
                            p['vx'], p['vy'] = vx * math.cos(ang) - vy * math.sin(ang), vx * math.sin(ang) + vy * math.cos(ang)
                            wallhits.append((t, g))
                            if k is not None and t - p['last'].get(k, -9) > 0.12:
                                p['last'][k] = t; B[k]['hp'] -= (99 if p['strong'] else 1); B[k]['hits'].append((t, g))
                                if B[k]['hp'] <= 0: B[k]['broke'] = (t, g, p['vx'], p['vy']); ev.append((t, 'break', g, k))
                                else: ev.append((t, 'crack', g, k))
            # box-box contacts: equal masses, elastic, resolved along the least-penetration axis (never overlapping)
            live = [g for g in G if X[g]['out'] is None and X[g]['won'] is None]
            for i in range(len(live)):
                for j in range(i + 1, len(live)):
                    a_, b_ = X[live[i]], X[live[j]]
                    px, py = 2 * HS - abs(a_['x'] - b_['x']), 2 * HS - abs(a_['y'] - b_['y'])
                    if px <= 0 or py <= 0: continue
                    if px < py:
                        s = 1 if a_['x'] < b_['x'] else -1; a_['x'] -= s * px / 2; b_['x'] += s * px / 2
                        if (b_['vx'] - a_['vx']) * s < 0: a_['vx'], b_['vx'] = b_['vx'], a_['vx']; ev.append((t, 'bump', live[i], live[j]))
                    else:
                        s = 1 if a_['y'] < b_['y'] else -1; a_['y'] -= s * py / 2; b_['y'] += s * py / 2
                        if (b_['vy'] - a_['vy']) * s < 0: a_['vy'], b_['vy'] = b_['vy'], a_['vy']; ev.append((t, 'bump', live[i], live[j]))
            for g in live:                                      # passive bouncing at constant speed
                p = X[g]; v = math.hypot(p['vx'], p['vy']) or 1; p['vx'] *= SPD / v; p['vy'] *= SPD / v
        front = 0.0 if t < sh0 else shv * (t - sh0) + 0.5 * sha * (t - sh0) ** 2
        for g in G:
            p = X[g]
            if p['out'] is not None or p['won'] is not None or t < T_GO: continue
            if gum['t'] is None and abs(p['x'] - gum['x']) < HS + 16 and abs(p['y'] - gum['y']) < HS + 16:
                gum['t'] = t; gum['who'] = g; p['strong'] = True; ev.append((t, 'pick', g, 'cre'))
            if p['y'] - HS > EXIT_Y - 4 and OX + 7 * C <= p['x'] <= OX + 11 * C:
                p['won'] = t; ev.append((t, 'win', g))
            elif shadow_touch(p['x'], p['y'], front):
                p['out'] = t; ev.append((t, 'out', g))
        frames.append(({g: (X[g]['x'], X[g]['y'], X[g]['vx'], X[g]['vy'], X[g]['out'], X[g]['won'], X[g]['strong']) for g in G}, front,
                       {k: B[k]['hp'] for k in B}))
        if any(X[g]['won'] is not None for g in G):
            if 'tend' not in B['exit']: B['exit']['tend'] = t
            if t > B['exit']['tend'] + float(os.environ.get('TAILSIM', '0')): break
        if all(X[g]['out'] is not None for g in G): break
    return X, frames, ev, gum, B, wallhits
# ---------------- shadow: flood fill on half cells from the tops of the four chambers
H2 = C // 2
SUBR, SUBC = ROWS * 2, COLS * 2
def sub_open(r, c):
    R, Cc = r // 2, c // 2
    return not is_wall(R, Cc)
SRC = [(2, c) for c in range(SUBC) if sub_open(2, c)]
DIST = {s: 0 for s in SRC}; q = deque(SRC)
while q:
    r, c = q.popleft()
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (r + dr, c + dc)
        if 0 <= n[0] < SUBR and 0 <= n[1] < SUBC and sub_open(*n) and n not in DIST: DIST[n] = DIST[(r, c)] + 1; q.append(n)
def shadow_touch(x, y, front):
    r0, r1 = int((y - HS - OY) // H2), int((y + HS - 1 - OY) // H2)
    c0, c1 = int((x - HS - OX) // H2), int((x + HS - 1 - OX) // H2)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            d = DIST.get((r, c))
            if d is not None and d < front: return True
    return False
WANT = os.environ.get('WANT', 'cyrus')
def score(seed):
    X, fr, ev, gum, B, wh = sim(seed)
    won = [e for e in ev if e[1] == 'win']
    if not won or won[0][2] != WANT: return None
    tw = won[0][0]
    if not (12.0 < tw < 18.0): return None
    outs = sorted(e[0] for e in ev if e[1] == 'out' and e[0] < tw)
    if len(outs) < 2: return None
    if any(b - a < 0.9 for a, b in zip(outs, outs[1:])): return None
    if outs[0] < 5.0: return None
    if gum['t'] is None or gum['t'] > tw - 0.8: return None
    gates = [B['gate%d' % k]['broke'] for k in range(4)]
    sh0, shv, sha = float(os.environ.get('SH0', '4.6')), float(os.environ.get('SHV', '3.4')), float(os.environ.get('SHA', '0.62'))
    t6 = sh0 + (-shv + math.sqrt(shv * shv + 2 * sha * 6)) / sha if sha > 0 else sh0 + 6 / shv   # shadow reaches the gate row
    if any(gb is None or gb[0] > t6 - 0.3 for gb in gates): return None
    # close finish: someone else still alive near the exit wall, or the last catch just before the win
    st = fr[min(len(fr) - 1, int(tw * FPS))][0]
    near = [g for g in G if g != WANT and st[g][4] is None and st[g][1] > OY + 12 * C]
    close = bool(near) or (tw - outs[-1] < 1.8)
    if not close: return None
    hits_exit = [h for h in B['exit']['hits']]
    who = sorted(set(h[1] for h in hits_exit))
    return round(tw, 2), [round(o, 1) for o in outs], (round(gum['t'], 1), gum['who']), who, [g for g in near]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
os.environ.setdefault('TAILSIM', '6')
XX, FR, EV, GUM, BB, WH = sim(SEED)
T_WIN = [e for e in EV if e[1] == 'win'][0][0]
print('win', round(T_WIN, 2), {g: XX[g]['out'] for g in G}, 'gum', GUM['t'], GUM['who'], 'chambers', CH)
for e in EV:
    if e[1] != 'bump': print('  ', round(e[0], 2), e[1:])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()
