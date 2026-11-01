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
C = 44
MAP = [
    "##################",
    "#111#222#333#444##",
    "#111#222#333#444##",
    "#111#222#333#444##",
    "#ggg#ggg#ggg#ggg##",
    "#................#",
    "#................#",
    "#................#",
    "###########......#",
    "#................#",
    "#................#",
    "#................#",
    "#......###########",
    "#................#",
    "#................#",
    "#................#",
    "#######bbbb#######",
    "####EEEEEEEEEE####",
    "####EEEEEEEEEE####",
    "####EEEEEEEEEE####"]
ROWS, COLS = len(MAP), len(MAP[0])
OX = (W - COLS * C) // 2; OY = int(os.environ.get('OY', '476'))
CH = {'joy': 1, 'cleo': 5, 'cyrus': 9, 'ray': 13}          # chamber left column per guide (set per seed below)
def is_wall(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or MAP[r][c] == '#'
# breakable walls: four gates (row 4) + the exit wall (row 17)
BRK0 = {}
for k, c0 in enumerate([1, 5, 9, 13]): BRK0['gate%d' % k] = dict(rect=(OX + c0 * C, OY + 4 * C, OX + (c0 + 3) * C, OY + 5 * C), hp=3)
BRK0['exit'] = dict(rect=(OX + 7 * C, OY + 16 * C, OX + 11 * C, OY + 17 * C), hp=int(os.environ.get('EXHP', '3')))
EXIT_Y = OY + 17 * C                                        # crossing into the checkered exit
GUM_POS = (OX + float(os.environ.get('GUMX', '8.5')) * C, OY + float(os.environ.get('GUMY', '10.5')) * C)
HS = int(os.environ.get('HS', '22'))
SPD = float(os.environ.get('SPD', '422'))
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
                if p['out'] is not None: continue
                if p['won'] is not None:                       # through the exit: friction brings it to rest inside the room (still solid)
                    dmp = math.exp(-dt / 0.07); p['vx'] *= dmp; p['vy'] *= dmp
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
                            broke = False
                            if k is not None and t - p['last'].get(k, -9) > 0.12:
                                p['last'][k] = t; B[k]['hp'] -= (99 if p['strong'] else 1); B[k]['hits'].append((t, g, p['x'], p['y']))
                                if B[k]['hp'] <= 0: B[k]['broke'] = (t, g, p['vx'], p['vy']); ev.append((t, 'break', g, k)); broke = True
                                else: ev.append((t, 'crack', g, k))
                            if broke: continue                       # the breaking hit carries straight through the wall
                            p['v' + axis] = -v
                            # tiny surface imperfection (+-2.5 deg) so no box locks into a perfectly periodic orbit
                            ang = rnd.uniform(-0.044, 0.044); vx, vy = p['vx'], p['vy']
                            p['vx'], p['vy'] = vx * math.cos(ang) - vy * math.sin(ang), vx * math.sin(ang) + vy * math.cos(ang)
                            wallhits.append((t, g, k, abs(v)))
            # box-box contacts: equal masses, elastic, resolved along the least-penetration axis (never overlapping)
            live = [g for g in G if X[g]['out'] is None]
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
            for g in [g_ for g_ in live if X[g_]['won'] is None]:      # passive bouncing at constant speed
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
WANT = os.environ.get('WANT', 'cyrus'); TW0, TW1 = float(os.environ.get('TW0', '15')), float(os.environ.get('TW1', '20'))
def score(seed):
    X, fr, ev, gum, B, wh = sim(seed)
    won = [e for e in ev if e[1] == 'win']
    if not won or won[0][2] != WANT: return None
    tw = won[0][0]
    if not (TW0 < tw < TW1): return None
    outs = sorted(e[0] for e in ev if e[1] == 'out' and e[0] < tw)
    if len(outs) < 2: return None
    if any(b - a < 0.9 for a, b in zip(outs, outs[1:])): return None
    if outs[0] < 5.0: return None
    if gum['t'] is None or gum['t'] > tw - 0.8: return None
    if any(abs(gum['t'] - o) < 1.0 for o in outs): return None
    gates = [B['gate%d' % k]['broke'] for k in range(4)]
    sh0, shv, sha = float(os.environ.get('SH0', '4.6')), float(os.environ.get('SHV', '3.4')), float(os.environ.get('SHA', '0.62'))
    t6 = sh0 + (-shv + math.sqrt(shv * shv + 2 * sha * 6)) / sha if sha > 0 else sh0 + 6 / shv   # shadow reaches the gate row
    if any(gb is None or gb[0] > t6 - 0.3 for gb in gates): return None
    # close finish: someone else still alive near the exit wall, or the last catch just before the win
    st = fr[min(len(fr) - 1, int(tw * FPS))][0]
    near = [g for g in G if g != WANT and st[g][4] is None and st[g][1] > OY + 12 * C]
    # how far behind the winner the dark is when he crosses (half cells along the maze; smaller = closer)
    wx, wy = st[WANT][0], st[WANT][1]; fw = fr[min(len(fr) - 1, int(tw * FPS))][1]
    dw = min((DIST.get((int((wy - OY) // H2) + dr, int((wx - OX) // H2) + dc), 999) for dr in (-3, -2, -1) for dc in (-1, 0, 1)), default=999)
    gap = round(dw - fw, 1)
    close = (bool(near) or (tw - outs[-1] < 1.8)) and gap < float(os.environ.get('GAPMAX', '99'))
    if not close: return None
    hits_exit = [h for h in B['exit']['hits']]
    who = sorted(set(h[1] for h in hits_exit))
    eb = B['exit']['broke']; steal = eb is not None and eb[1] != WANT and eb[1] == gum['who']
    return round(tw, 2), [round(o, 1) for o in outs], (round(gum['t'], 1), gum['who']), who, [g for g in near], 'gap', gap, 'STEAL' if steal else '', 'exitbreak', eb and round(eb[0], 1)
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
# =====================================================================  RENDER
from PIL import ImageFilter, ImageEnhance
OWNER = {[1, 5, 9, 13].index(CH[g]): g for g in G}                   # gate index -> guide whose chamber it closes
T_CARD = T_WIN + float(os.environ.get('CARDDLY', '1.25'))           # box slides into the checkered room, beat, then the winner card
T_END = T_CARD + float(os.environ.get('HOLD', '2.6')); NF = int(round(T_END * FPS))
def fidx(t): return min(max(0, int(round(t * FPS))), len(FR) - 1)
def frame_at(t): return FR[fidx(t)]
BDIST = min(DIST[(r, c)] for (r, c) in DIST if r // 2 == 16)        # the exit wall row: the dark never seeps past it
def front_at(t): return min(frame_at(t)[1], BDIST - 0.01)
# ---------------- assets
hall_m = json.load(open(S_ + 'fork_a8/gen/hall_meta.json')); hall_s = Image.open(S_ + 'fork_a8/gen/hall_sheet.png').convert('RGBA')
def tl_(m, sh, name):
    for t_ in m['tileset_data']['tiles']:
        if t_['name'] == name:
            b = t_['bounding_box']; return sh.crop((b['x'], b['y'], b['x'] + b['width'], b['y'] + b['height']))
FLOOR_T = up(tl_(hall_m, hall_s, 'wang_0'), 2)
wsheet = Image.open(S_ + 'pixellab/maze/walls_sheet.png').convert('RGBA')
BRICK = up(wsheet.crop((77, 13, 128, 56)), 2)
def tint(im, col, k=0.75):
    a = np.array(im).astype(float); g_ = a[..., :3].mean(2, keepdims=True) / 255.0
    a[..., :3] = a[..., :3] * (1 - k) + (np.array(col)[None, None, :] * (0.35 + 0.95 * g_)) * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
FACE = {}; FACE24 = {}
for g, fn in [('joy', 'idle_0.gif'), ('cyrus', 'idle_1.gif'), ('ray', 'idle_2.gif'), ('cleo', 'idle_3.gif')]:
    im = Image.open(A + fn); im.seek(0); im = im.convert('RGBA').resize((92, 92), Image.NEAREST)
    cx = 46 if g != 'cleo' else 47
    FACE[g] = im.crop((cx - 10, 16, cx + 10, 36)); FACE24[g] = im.crop((cx - 12, 15, cx + 12, 39))
ROSTER_FACE = {g: up(FACE24[g], 3) for g in G}
def vic_frames(g):
    im = Image.open(A + VIC[g]); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), 5))
    return out
VIC_W = vic_frames(WANT)
GUMI = up(Image.open(PL + 'gummies/pick_cre.png').convert('RGBA'), 2)
STR_COL = (255, 92, 70)
DRG = [Image.open(S_ + 'fork_b5/dragon_fire/%02d.png' % i).convert('RGBA').crop((97, 0, 224, 126)) for i in (0, 1)]
moon = Image.open(A + 'bg_moon.gif'); BG = []
for i in range(0, moon.n_frames, 2):
    moon.seek(i); f_ = moon.convert('RGB').resize((3413, 1920), Image.LANCZOS).crop((1166, 0, 1166 + W, H)).filter(ImageFilter.GaussianBlur(6))
    BG.append(ImageEnhance.Brightness(f_).enhance(0.42).convert('RGBA'))
# ---------------- static maze layer
MZ = Image.new('RGBA', (W, H), (0, 0, 0, 0))
mx0, my0, mx1, my1 = OX, OY, OX + COLS * C, OY + ROWS * C
d = ImageDraw.Draw(MZ)
d.rounded_rectangle([mx0 - 14, my0 - 14, mx1 + 14, my1 + 14], 12, fill=(16, 12, 24, 255), outline=(232, 186, 70, 255), width=6)
floor = Image.new('RGBA', (COLS * C, ROWS * C), (0, 0, 0, 0))
for yy in range(0, ROWS * C, FLOOR_T.height):
    for xx in range(0, COLS * C, FLOOR_T.width): floor.alpha_composite(FLOOR_T, (xx, yy))
fmask = Image.new('L', (COLS * C, ROWS * C), 0); fd = ImageDraw.Draw(fmask)
for r in range(ROWS):
    for c in range(COLS):
        if not is_wall(r, c): fd.rectangle([c * C, r * C, c * C + C - 1, r * C + C - 1], fill=255)
fl2 = Image.new('RGBA', floor.size, (0, 0, 0, 0)); fl2.paste(floor, (0, 0), fmask); MZ.alpha_composite(fl2, (mx0, my0))
d = ImageDraw.Draw(MZ)
for r in range(ROWS):                                                 # checkered exit room (the finish)
    for c in range(COLS):
        if MAP[r][c] != 'E': continue
        for i in range(2):
            for j in range(2):
                col_ = (238, 238, 238, 255) if (i + j + r + c) % 2 == 0 else (28, 28, 34, 255)
                d.rectangle([OX + c * C + j * 22, OY + r * C + i * 22, OX + c * C + j * 22 + 21, OY + r * C + i * 22 + 21], fill=col_)
rnd_ = random.Random(7)
for r in range(ROWS):
    for c in range(COLS):
        if not is_wall(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        d.rectangle([x0, y0, x0 + C - 1, y0 + C - 1], fill=(38, 34, 52, 255))
        for k in range(5):
            px_, py_ = x0 + rnd_.randint(2, C - 10), y0 + rnd_.randint(2, C - 10)
            d.rectangle([px_, py_, px_ + 6, py_ + 4], fill=(48, 44, 64, 255))
for r in range(ROWS):
    for c in range(COLS):
        if not is_wall(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        if r + 1 < ROWS and not is_wall(r + 1, c):                   # brick face (3/4 view lip) on the wall's south side
            MZ.alpha_composite(BRICK.crop((0, 0, C, 22)), (x0, y0 + C - 22))
            d.rectangle([x0, y0 + C - 24, x0 + C - 1, y0 + C - 23], fill=(150, 146, 168, 255))
        rim = (122, 118, 142, 255)
        if r > 0 and not is_wall(r - 1, c): d.rectangle([x0, y0, x0 + C - 1, y0 + 3], fill=rim)
        if c > 0 and not is_wall(r, c - 1): d.rectangle([x0, y0, x0 + 3, y0 + C - 1], fill=rim)
        if c + 1 < COLS and not is_wall(r, c + 1): d.rectangle([x0 + C - 4, y0, x0 + C - 1, y0 + C - 1], fill=rim)
ao = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ao)
for r in range(ROWS):
    for c in range(COLS):
        if not is_wall(r, c) and is_wall(r - 1, c):
            for k in range(9): ad.rectangle([OX + c * C, OY + r * C + k, OX + c * C + C - 1, OY + r * C + k], fill=(10, 6, 20, 85 - k * 9))
MZ.alpha_composite(ao)
# ---------------- breakable brick walls: guild-coloured gates, a dark exit wall; cracks grow with each hit
BCOL = {('gate%d' % k): COL[OWNER[k]] for k in range(4)}; BCOL['exit'] = (120, 96, 150)
HP0 = {k: BRK0[k]['hp'] for k in BRK0}
def brick_img(k):
    x0, y0, x1, y1 = BRK0[k]['rect']; w, h = int(x1 - x0), int(y1 - y0)
    base = Image.new('RGBA', (w, h)); bt = tint(BRICK, BCOL[k], 0.8)
    for xx in range(0, w, bt.width):
        for yy in range(0, h, bt.height): base.alpha_composite(bt, (xx, yy))
    dd = ImageDraw.Draw(base)
    dd.rectangle([0, 0, w - 1, 3], fill=tuple(min(255, int(v * 1.3)) for v in BCOL[k]) + (255,)); dd.rectangle([0, h - 4, w - 1, h - 1], fill=(20, 14, 26, 255))
    dd.rectangle([0, 0, w - 1, h - 1], outline=(18, 12, 24, 255), width=2)
    return base
BIMG = {k: brick_img(k) for k in BRK0}
def crack_at(k, hx, top, seed):
    """jagged pixel crack starting where the box struck the face, with a branch"""
    x0, y0, x1, y1 = BRK0[k]['rect']; w, h = int(x1 - x0), int(y1 - y0); rr = random.Random(seed)
    px = max(6, min(w - 7, hx - x0)); py = 0 if top else h - 1; dy = 4 if top else -4; pts = [(px, py)]; br = []
    while 0 <= py + dy < h:
        py += dy; px = max(3, min(w - 4, px + rr.choice([-4, -2, 0, 2, 4]))); pts.append((px, py))
        if len(pts) == 4: br = [(px, py)] + [(px + s_ * 4 * n, py + dy * n // 2) for n, s_ in zip(range(1, 4), [rr.choice([-1, 1])] * 3)]
    return [[(a // 2 * 2, b // 2 * 2) for a, b in pts], [(a // 2 * 2, max(0, min(h - 1, b)) // 2 * 2) for a, b in br]]
def wall_img(k, stage):
    im = BIMG[k].copy(); dd = ImageDraw.Draw(im); x0, y0, x1, y1 = BRK0[k]['rect']; wy = (y0 + y1) / 2
    for j, (th, g, bx, by) in enumerate(BB[k]['hits'][:stage]):
        top = by < wy
        for path in crack_at(k, bx, top, 31 + j * 17 + len(k)):
            if len(path) < 2: continue
            dd.line(path, fill=(14, 8, 20, 255), width=3); dd.line([(a + 2, b) for a, b in path], fill=(255, 255, 255, 55), width=1)
        if j == 1:                                                     # second hit knocks a chip out of the face
            cx_ = int(max(8, min(x1 - x0 - 9, bx - x0))); cy_ = 0 if top else int(y1 - y0) - 10
            dd.rectangle([cx_ - 6, cy_, cx_ + 5, cy_ + 9], fill=(22, 16, 30, 255))
    return im
WIMG = {k: [wall_img(k, s_) for s_ in range(3)] for k in BRK0}
# ---------------- debris: chips on every hit, chunks when a wall shatters; they slide on the floor and settle (never over a wall)
def solid_at(x, y, t):
    r, c = int((y - OY) // C), int((x - OX) // C)
    if is_wall(r, c): return True
    hp = frame_at(t)[2]
    for k, b in BRK0.items():
        x0, y0, x1, y1 = b['rect']
        if hp[k] > 0 and x0 <= x < x1 and y0 <= y < y1: return True
    return False
PARTS = []
prr = random.Random(5)
for k in BRK0:
    x0, y0, x1, y1 = BRK0[k]['rect']; wy = (y0 + y1) / 2
    for (th, g, bx, by) in BB[k]['hits']:
        side = -1 if by < wy else 1                                    # chips spall back toward the hitter's side
        brk = BB[k]['broke'] is not None and abs(BB[k]['broke'][0] - th) < 1e-6
        if brk:
            dirn = 1 if by < wy else -1                                # chunks carry on in the box's direction
            for n in range(18):
                px = prr.uniform(x0 + 4, x1 - 4); py = prr.uniform(y0 + 4, y1 - 4)
                sp = prr.uniform(110, 380); ang = prr.uniform(-0.8, 0.8) + (math.pi / 2 if dirn > 0 else -math.pi / 2)
                pull = max(0.0, 1 - abs(px - bx) / 90)
                PARTS.append(dict(t0=th, x=px, y=py, vx=sp * math.cos(ang) + (px - bx) * 0.6, vy=sp * math.sin(ang) * (1 + 0.6 * pull), sz=prr.choice([8, 10, 10, 12, 14]),
                                  col=tuple(int(v * prr.uniform(0.55, 1.05)) for v in BCOL[k]), ok=True))
        else:
            cx_ = max(x0 + 6, min(x1 - 6, bx)); cy_ = y0 if side < 0 else y1
            for n in range(5):
                ang = prr.uniform(-1.1, 1.1) + (-math.pi / 2 if side < 0 else math.pi / 2)
                sp = prr.uniform(50, 150)
                PARTS.append(dict(t0=th, x=cx_ + prr.uniform(-10, 10), y=cy_ + side * 3, vx=sp * math.cos(ang), vy=sp * math.sin(ang), sz=prr.choice([4, 4, 6]),
                                  col=tuple(int(v * prr.uniform(0.55, 1.0)) for v in BCOL[k]), ok=True))
PPOS = [[None] * len(PARTS) for _ in range(NF)]
for f in range(NF):
    t = f / FPS
    for i, p in enumerate(PARTS):
        if t < p['t0']: continue
        if 'cur' not in p: p['cur'] = (p['x'], p['y'])
        x, y = p['cur']
        for _ in range(4):
            dtp = 1 / FPS / 4; dmp = math.exp(-dtp / 0.13)
            p['vx'] *= dmp; p['vy'] *= dmp
            nx = x + p['vx'] * dtp
            if solid_at(nx, y, t): p['vx'] *= -0.3; nx = x
            ny = y + p['vy'] * dtp
            if solid_at(nx, ny, t): p['vy'] *= -0.3; ny = y
            x, y = nx, ny
        if solid_at(x, y, t): p['ok'] = False                          # spawned inside something solid: drop it
        p['cur'] = (x, y); PPOS[f][i] = (x, y)
# ---------------- shadow on the half-cell grid (stepped edge), creeping in from the cell it came from
SUBS = sorted(DIST.items(), key=lambda z: z[1])
SUBDIR = {}
for (r, c), dv in SUBS:
    best = min(((DIST.get((r + dr, c + dc), 999), dr, dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))))
    SUBDIR[(r, c)] = (best[1], best[2]) if best[0] < dv else (-1, 0)
NZ = Image.effect_noise((COLS * C // 4, ROWS * C // 4), 60).resize((COLS * C, ROWS * C), Image.BICUBIC).filter(ImageFilter.GaussianBlur(5))
NZa = np.array(NZ).astype(float) / 255.0
SHC = np.zeros((ROWS * C, COLS * C, 4), np.uint8)
SHC[..., 0] = (20 + 30 * NZa).astype(np.uint8); SHC[..., 1] = (9 + 12 * NZa).astype(np.uint8); SHC[..., 2] = (38 + 50 * NZa).astype(np.uint8); SHC[..., 3] = 248
SHADOW_TEX = Image.fromarray(SHC)
EYES = [(r, c) for (r, c) in DIST if (r * 7 + c * 13) % 23 == 0 and DIST.get((r, c + 1)) is not None]
def shadow_layer(t, fr_):
    m = Image.new('L', (COLS * C, ROWS * C), 0); md = ImageDraw.Draw(m); rim = []
    for (r, c), dv in SUBS:
        cov = fr_ - dv
        if cov <= 0: break
        x0, y0 = c * H2, r * H2
        if cov >= 1: md.rectangle([x0, y0, x0 + H2 - 1, y0 + H2 - 1], fill=255); continue
        dr, dc = SUBDIR[(r, c)]; k = max(2, int(H2 * cov) // 2 * 2)
        if dr == -1: bx_ = [x0, y0, x0 + H2 - 1, y0 + k - 1]; ed = [x0, y0 + k - 3, x0 + H2 - 1, y0 + k - 1]
        elif dr == 1: bx_ = [x0, y0 + H2 - k, x0 + H2 - 1, y0 + H2 - 1]; ed = [x0, y0 + H2 - k, x0 + H2 - 1, y0 + H2 - k + 2]
        elif dc == -1: bx_ = [x0, y0, x0 + k - 1, y0 + H2 - 1]; ed = [x0 + k - 3, y0, x0 + k - 1, y0 + H2 - 1]
        else: bx_ = [x0 + H2 - k, y0, x0 + H2 - 1, y0 + H2 - 1]; ed = [x0 + H2 - k, y0, x0 + H2 - k + 2, y0 + H2 - 1]
        md.rectangle(bx_, fill=255); rim.append(ed)
    L = Image.new('RGBA', (COLS * C, ROWS * C), (0, 0, 0, 0)); L.paste(SHADOW_TEX, (int(6 * math.sin(t)), 0), m)
    dd = ImageDraw.Draw(L)
    for b_ in rim: dd.rectangle(b_, fill=(175, 115, 255, 225))
    for (r, c) in EYES:
        if fr_ - DIST[(r, c)] < 3 or fr_ - DIST[(r, c + 1)] < 3: continue
        ex, ey = c * H2 + 8, r * H2 + 6
        if (int(t * 1.7 + r * 3 + c) % 9) == 0: dd.rectangle([ex, ey + 4, ex + 24, ey + 6], fill=(230, 220, 255, 230))
        else: dd.rectangle([ex, ey, ex + 6, ey + 9], fill=(240, 235, 255, 245)); dd.rectangle([ex + 18, ey, ex + 24, ey + 9], fill=(240, 235, 255, 245))
    return L
# ---------------- boxes
def box_img(g, k=1.0, dark=0.0):
    b = Image.new('RGBA', (2 * HS, 2 * HS), (0, 0, 0, 0)); dd = ImageDraw.Draw(b)
    dd.rectangle([0, 0, 2 * HS - 1, 2 * HS - 1], fill=(14, 10, 20, 255))
    dd.rectangle([2, 2, 2 * HS - 3, 2 * HS - 3], fill=COL[g] + (255,))
    fc = up(FACE[g], 2); bg_ = Image.new('RGBA', fc.size, tuple(int(v * 0.55) for v in COL[g]) + (255,)); bg_.alpha_composite(fc)
    b.alpha_composite(bg_, (HS - fc.width // 2, HS - fc.height // 2))
    dd = ImageDraw.Draw(b); dd.rectangle([2, 2, 2 * HS - 3, 2 * HS - 3], outline=COL[g] + (255,), width=2)
    dd.rectangle([4, 4, 10, 6], fill=(255, 255, 255, 190))
    if dark > 0: b = Image.blend(b, Image.new('RGBA', b.size, (30, 16, 50, 255)), dark).copy(); b.putalpha(Image.new('L', b.size, 255))
    if k != 1.0: b = b.resize((max(2, int(b.width * k)), max(2, int(b.height * k))), Image.NEAREST)
    return b
BOXI = {g: box_img(g) for g in G}
# ---------------- HUD
RY0 = my1 + 30
def roster(img, t):
    tt = min(t, T_CARD)
    for i, g in enumerate(G):
        x0 = 36 + i * 254; x1 = x0 + 238
        out = XX[g]['out'] is not None and XX[g]['out'] <= tt
        win = t >= T_WIN and g == WANT
        layer(img, lambda dd, x0=x0, x1=x1, win=win, g=g: dd.rounded_rectangle([x0, RY0, x1, RY0 + 90], 14, fill=(14, 10, 22, 230), outline=(255, 214, 60, 255) if win else COL[g] + (255,), width=6 if win else 4))
        fc = ROSTER_FACE[g]
        if out: fc = ImageEnhance.Brightness(ImageEnhance.Color(fc).enhance(0.15)).enhance(0.45)
        img.alpha_composite(fc, (x0 + 9, RY0 + 9))
        nm = NAME[g] if g != 'ray' else 'RAY'
        d_ = ImageDraw.Draw(img); d_.text((x0 + 90, RY0 + 22), nm, font=F(28 if len(nm) < 5 else 24), fill=(120, 110, 130) if out else COL[g], stroke_width=4, stroke_fill=(10, 6, 16))
        if out:
            d_.line([x0 + 10, RY0 + 10, x0 + 80, RY0 + 80], fill=(230, 50, 60), width=7); d_.line([x0 + 10, RY0 + 80, x0 + 80, RY0 + 10], fill=(230, 50, 60), width=7)
            d_.text((x0 + 92, RY0 + 56), 'OUT', font=F(20), fill=(240, 70, 70), stroke_width=3, stroke_fill=(10, 6, 16))
RAWS = []
for e in EV:
    if e[1] == 'pick': RAWS.append((e[0], (NAME[e[2]] + ': STRENGTH!', STR_COL, frame_at(e[0])[0][e[2]][1])))
    elif e[1] == 'out' and e[0] < T_CARD: RAWS.append((e[0], (NAME[e[2]] + ' OUT!', (255, 110, 110), frame_at(e[0])[0][e[2]][1])))
RAWS.sort(key=lambda z: z[0]); SCHED = []
for i, (t0, it) in enumerate(RAWS):
    st0 = max(t0, SCHED[-1][1] + 0.08) if SCHED else t0
    nxt = RAWS[i + 1][0] if i + 1 < len(RAWS) else 1e9
    en = min(st0 + 1.1, max(st0 + 0.7, nxt - 0.08))
    en = min(en, T_WIN - 0.05) if st0 < T_WIN - 0.5 else en
    SCHED.append((st0, en, it))
print('stamps', [(round(a, 2), round(b, 2), it[0]) for a, b, it in SCHED])
print('beats: go', T_GO, 'win', round(T_WIN, 2), 'card', round(T_CARD, 2), 'end', round(T_END, 2))
STILLS = [float(x) for x in os.environ.get('STILLS', '').split(',') if x]
EVONLY = bool(os.environ.get('EVONLY'))
wr = None if (STILLS or EVONLY) else Writer('n03_noaudio.mp4')
WINXY = None
for f in range(NF):
    t = f / FPS
    if EVONLY: break
    if STILLS and not any(abs(t - x) < 0.5 / FPS for x in STILLS): continue
    st, _f, hp = frame_at(t); fr_ = front_at(t)
    img = BG[int(t * 5) % len(BG)].copy()
    img.alpha_composite(MZ)
    # dragon on its treasure in the checkered exit room (idle breathing, as in the posted cut)
    dfr = DRG[int(t * 2) % 2]; dx0 = OX + 14 * C - 6 - dfr.width; dy0 = OY + 20 * C - 4 - dfr.height
    img.alpha_composite(dfr, (dx0, dy0))
    # rubble on the floor
    for i, p in enumerate(PARTS):
        pp = PPOS[f][i]
        if pp is None or not p['ok']: continue
        x, y = pp; s_ = p['sz']
        layer(img, lambda dd, x=x, y=y, s_=s_, p=p: (dd.rectangle([x - s_ / 2 + 2, y - s_ / 2 + 2, x + s_ / 2 + 2, y + s_ / 2 + 2], fill=(10, 6, 18, 120)),
                                                    dd.rectangle([x - s_ / 2, y - s_ / 2, x + s_ / 2 - 1, y + s_ / 2 - 1], fill=p['col'] + (255,)),
                                                    dd.rectangle([x - s_ / 2, y + s_ / 2 - 2, x + s_ / 2 - 1, y + s_ / 2 - 1], fill=tuple(int(v * 0.6) for v in p['col']) + (255,))))
    # brick walls (shake on a hit, crack stages)
    for k in BRK0:
        if hp[k] <= 0: continue
        x0, y0, x1, y1 = BRK0[k]['rect']; stage = min(2, HP0[k] - hp[k])
        lastk = [h[0] for h in BB[k]['hits'] if h[0] <= t]
        sh_ = int(3 * math.sin((t - lastk[-1]) * 90)) if lastk and t - lastk[-1] < 0.12 else 0
        img.alpha_composite(WIMG[k][stage], (int(x0) + sh_, int(y0)))
    # the STRENGTH gummy on the floor
    if GUM['t'] is None or t < GUM['t']:
        bob = 3 * math.sin(t * 4); gx, gy = GUM_POS
        layer(img, lambda dd: [dd.ellipse([gx - 34 + q * 9, gy - 34 + q * 9, gx + 34 - q * 9, gy + 34 - q * 9], fill=STR_COL + (30 + q * 22,)) for q in range(3)])
        img.alpha_composite(GUMI, (int(gx - GUMI.width / 2), int(gy - GUMI.height / 2 + bob)))
    # trails + live boxes
    live = []
    for g in G:
        x, y, vx, vy, out, won, strong = st[g]
        if out is not None and out <= t: continue
        if t >= T_CARD and g == WANT: continue
        if t >= T_GO and (won is None or t < won + 0.3):
            for q in range(1, 6):
                s0 = frame_at(max(0, t - q * 0.033))[0][g]
                if s0[4] is not None and s0[4] <= t: break
                a_ = 100 - q * 17; s_ = int(HS * (1 - q * 0.1))
                layer(img, lambda dd, px_=s0[0], py_=s0[1], a_=a_, s_=s_, g=g, strong=strong: dd.rectangle([px_ - s_, py_ - s_, px_ + s_, py_ + s_], fill=(STR_COL if strong else COL[g]) + (a_,)))
        live.append(g)
    img.alpha_composite(shadow_layer(t, fr_), (OX, OY))
    for g in G:                                                       # caught: sinks into the dark
        x, y, vx, vy, out, won, strong = st[g]
        if out is None or out > t: continue
        u = (t - out) / 0.45
        if u < 1:
            bi = box_img(g, 1 - 0.55 * u, dark=min(1, u * 1.2)); img.alpha_composite(bi, (int(x - bi.width / 2), int(y - bi.height / 2)))
        if t - out < 1.0:
            a_ = int(255 * min(1, (1.0 - (t - out)) / 0.25))
            ly = y - 64 - 10 * min(1, (t - out) / 0.2)
            if ly < OY + 1.2 * C + 90: ly = y + 34
            text_layer(img, [(x, ly, 'OUT', 30, (255, 90, 90), 6, a_)])
    for g in live:
        x, y, vx, vy, out, won, strong = st[g]
        if strong:
            pul = 0.5 + 0.5 * math.sin(t * 14)
            layer(img, lambda dd, x=x, y=y, pul=pul: dd.rectangle([x - HS - 6, y - HS - 6, x + HS + 5, y + HS + 5], outline=STR_COL + (int(140 + 100 * pul),), width=4))
        img.alpha_composite(BOXI[g], (int(x - HS), int(y - HS)))
        if g == WANT: WINXY = (x, y)
    # bursts: pickup, wall break dust
    for e in EV:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.5:
            px_, py_ = frame_at(e[0])[0][e[2]][:2]; u = (t - e[0]) / 0.5
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.rectangle([px_ + (20 + 90 * u) * math.cos(q * 0.785) - 6, py_ + (20 + 90 * u) * math.sin(q * 0.785) - 6, px_ + (20 + 90 * u) * math.cos(q * 0.785) + 6, py_ + (20 + 90 * u) * math.sin(q * 0.785) + 6], fill=STR_COL + (int(255 * (1 - u)),)) for q in range(8)])
        if e[1] == 'break' and 0 <= t - e[0] < 0.4:
            x0, y0, x1, y1 = BRK0[e[3]]['rect']; u = (t - e[0]) / 0.4; rr = random.Random(int(e[0] * 1000))
            pts = [(rr.uniform(x0, x1), rr.uniform(y0, y1)) for _ in range(8)]
            layer(img, lambda dd, u=u, pts=pts: [dd.rectangle([px - 8 - 14 * u, py - 8 - 14 * u, px + 8 + 14 * u, py + 8 + 14 * u], fill=(225, 215, 235, int(150 * (1 - u)))) for px, py in pts])
    # stamps (one at a time, dark plate, top of the maze)
    for st0, en, it in SCHED:
        if st0 <= t < en and t < T_CARD:
            text, col, _y = it; u = t - st0; al = int(255 * min(1, (en - t) / 0.2))
            fs_ = min(48, int(700 / len(text))); sc = 1 + 0.2 * max(0, 1 - u / 0.12); fs2 = int(fs_ * sc)
            tw_ = len(text) * fs2; yy = OY + int(1.2 * C) if it[2] > OY + 4.5 * C else OY + int(8.5 * C) - fs2 // 2
            layer(img, lambda dd, tw_=tw_, fs2=fs2, al=al, yy=yy: dd.rounded_rectangle([540 - tw_ / 2 - 22, yy - 18, 540 + tw_ / 2 + 22, yy + fs2 + 18], 16, fill=(14, 8, 22, int(230 * al / 255))))
            text_layer(img, [(540, yy, text, fs2, col, 8, al)])
    # countdown 3-2-1-GO
    if t < T_GO + 0.5:
        n = 3 - int(t / 0.7); txt = str(n) if t < T_GO else 'GO!'
        u = (t % 0.7) / 0.7 if t < T_GO else (t - T_GO) / 0.5
        fs = int((190 if t < T_GO else 150) * (1.2 - 0.2 * min(1, u * 3)))
        text_layer(img, [(540, OY + int(9.3 * C) - fs // 2, txt, fs, (255, 214, 60) if t < T_GO else (120, 230, 90), 12, int(255 * (1 if t < T_GO else max(0, 1 - u))))])
    roster(img, t)
    # winner card: Syeda's victory pose replaces Cyrus's box
    if t >= T_CARD:
        u = t - T_CARD; a_ = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([OX - 14, OY - 14, OX + COLS * C + 14, OY + ROWS * C + 14], fill=(8, 6, 16, int(175 * a_))))
        vf = VIC_W[int(u * 8) % len(VIC_W)]; q = min(1.0, u / 0.25)
        sc = 0.35 + 0.65 * (1 - (1 - q) ** 3)
        vf2 = vf if sc >= 0.999 else vf.resize((max(2, int(vf.width * sc)), max(2, int(vf.height * sc))), Image.NEAREST)
        cxp = WINXY[0] + (540 - WINXY[0]) * q; cyp = WINXY[1] + (OY + 12.6 * C - WINXY[1]) * q
        img.alpha_composite(vf2, (int(cxp - vf2.width / 2), int(cyp - vf2.height * (78 / 92))))
        text_layer(img, [(540, OY + int(1.6 * C), NAME[WANT] + ' WINS!', 72, COL[WANT], 10, int(255 * a_)),
                         (540, OY + int(15.2 * C), 'DID YOUR GUIDE WIN?', 40, (255, 255, 255), 8, int(255 * min(1, max(0, u - 0.12) / 0.2)))])
    img.alpha_composite(HOOK)
    if STILLS: img.convert('RGB').save(f'st_{t:.2f}.png')
    else: wr.write(img)
if wr: wr.close()
if STILLS: sys.exit()
out_ev = [(0.0, 'tick_8bit'), (0.7, 'tick_8bit'), (1.4, 'tick_8bit'), (T_GO, 'go_8bit')]
last = -9
for (th, g, k, v) in sorted(WH, key=lambda z: z[0]):
    if k is None and th - last > 0.3 and th < T_WIN: out_ev.append((round(th, 3), 'reeltick_8bit')); last = th
for e in EV:
    if e[0] > T_CARD: continue
    if e[1] == 'crack': out_ev.append((round(e[0], 3), 'brick_8bit'))
    elif e[1] == 'break': out_ev.append((round(e[0], 3), 'crunch_8bit')); out_ev.append((round(e[0] + 0.02, 3), 'brick_8bit'))
    elif e[1] == 'pick': out_ev.append((round(e[0], 3), 'powerup_8bit'))
    elif e[1] == 'out': out_ev.append((round(e[0], 3), 'squish')); out_ev.append((round(e[0] + 0.05, 3), 'buzz_8bit'))
out_ev += [(round(T_WIN, 3), 'ding_8bit'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(e for e in out_ev if e[0] < T_END - 0.1)
json.dump({'events': out_ev, 'end': T_END, 'beats': {'go': T_GO, 'win': T_WIN, 'card': T_CARD, 'loop': T_END, 'outs': {g: XX[g]['out'] for g in G}, 'gummy': GUM['t']}}, open('n03_events.json', 'w'), indent=1)
print('done', round(T_END, 2), NF)
