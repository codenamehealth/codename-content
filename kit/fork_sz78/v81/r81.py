import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #81 safe-zone + hook pass (source: fork_b8/r83.py). HOLLOW RULE: the Hollow runner is removed (4 guides).
# Maze narrowed 15 -> 13 columns (central wall block 7 -> 5 wide; cols 5 and 9 removed) so it fits the zone width; vertical camera follows the pack.
import numpy as np, heapq
from collections import deque
os.chdir(os.path.dirname(os.path.abspath(__file__)))
HOOK, HB = hook_layer(['OUTRUN', 'THE SHADOW'], accent=1, color=(200, 150, 255))
ROSTER_Y = HB + 52; VY0 = HB + 100; VY1 = 1500; VH = VY1 - VY0
print('hook bottom', HB, 'view', VY0, VY1)
C = 64
MAP0 = ["###############",
       "#.............#",
       "#.............#",
       "#.............#",
       "#...#######...#",
       "#...#######...#",
       "#.o.#######.o.#",
       "#...#######...#",
       "#...#######...#",
       "#.............#",
       "#......o......#",
       "#.............#",
       "##########....#",
       "#.............#",
       "#..o......o...#",
       "#.............#",
       "#....##########",
       "#.............#",
       "#......o......#",
       "######...######",
       "######EEE######",
       "###############"]
MAP = [r[:5] + r[6:9] + r[10:] for r in MAP0]
ROWS, COLS = len(MAP), len(MAP[0]); OX = 478 - COLS * C // 2; OY = VY0
def is_wall(r, c): return MAP[r][c] == '#'
def is_pil(r, c): return MAP[r][c] == 'o'
def passable(r, c): return 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] != '#' and MAP[r][c] != 'o'
meta = json.load(open(B8 + 'snow_meta.json')); sh = Image.open(B8 + 'snow_sheet.png').convert('RGBA')
TL = meta['tileset_data']['tiles']
def tile(i):
    b = TL[i]['bounding_box']; return up(sh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32)), 2)
FLOOR, TOP, FACE = tile(0), tile(6), tile(15)
LAMP = up(crop(Image.open(B8 + 'lamppost/01.png').convert('RGBA')), 2)
PINE = up(crop(Image.open(B8 + 'pine/01.png').convert('RGBA')), 2)
PINE1 = crop(Image.open(B8 + 'pine/05.png').convert('RGBA'))
STX = Image.open(B8 + 'shadowtex/06.png').convert('RGBA')
board = Image.new('RGBA', (COLS * C, ROWS * C), (0, 0, 0, 255))
for r in range(ROWS):
    for c in range(COLS):
        if not is_wall(r, c):
            t_ = FLOOR
            if (r + c) % 2: t_ = t_.transpose(Image.FLIP_LEFT_RIGHT)
            board.alpha_composite(t_, (c * C, r * C))
bd = ImageDraw.Draw(board)
for r in range(ROWS):
    for c in range(COLS):
        if not is_wall(r, c): continue
        x, y = c * C, r * C; board.alpha_composite(TOP, (x, y))
        if r + 1 < ROWS and not is_wall(r + 1, c):
            board.alpha_composite(FACE.crop((0, 0, C, 46)), (x, y + C - 46))
# exit glow lane
for c in range(COLS):
    for r in range(ROWS):
        if MAP[r][c] == 'E': board.alpha_composite(FLOOR, (c * C, r * C))
STATIC_PROPS = []
for (r, c) in [(5, 5), (5, 8), (7, 6), (4, 9), (13, 0)]: pass
PINES = [(4.6, 4.71), (4.6, 7.0), (6.8, 5.86), (7.2, 7.3), (6.2, 4.29)]  # same pines, mapped onto the narrower block
SMALLP = [(12, 1), (12, 4), (12, 6), (16, 6), (16, 8), (16, 11), (19, 2), (19, 10), (0, 3), (0, 9), (21, 4), (21, 8)]
LAMPS = [(r, c) for r in range(ROWS) for c in range(COLS) if is_pil(r, c)]
EX_R = 20; EX_C = [c for c in range(COLS) if MAP[EX_R][c] == 'E']
FIRE_XY = (OX + (EX_C[1] * C + C // 2), OY + EX_R * C + C // 2)
# --- graph
FINE = 4; FC = C // FINE
def dijk(starts):
    d = np.full((ROWS * FINE, COLS * FINE), np.inf); h = []
    for p in starts: d[p] = 0; heapq.heappush(h, (0.0, p))
    while h:
        dist, (fr, fc) = heapq.heappop(h)
        if dist > d[fr, fc]: continue
        for dr, dc, w in ((1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)):
            nr, nc = fr + dr, fc + dc
            if 0 <= nr < ROWS * FINE and 0 <= nc < COLS * FINE and passable(nr // FINE, nc // FINE):
                if dr and dc and not (passable((fr + dr) // FINE, fc // FINE) and passable(fr // FINE, (fc + dc) // FINE)): continue
                nd = dist + w
                if nd < d[nr, nc]: d[nr, nc] = nd; heapq.heappush(h, (nd, (nr, nc)))
    return d
DEX = dijk([(EX_R * FINE + i, c * FINE + j) for c in EX_C for i in range(FINE) for j in range(FINE)])
DSL = dijk([(1 * FINE + i, c * FINE + j) for c in range(1, COLS - 1) for i in range(2) for j in range(FINE)])
GY, GX = np.gradient(np.where(np.isinf(DEX), 9999, DEX))
DSLV = DSL.copy()
for _r in range(ROWS):
    for _c in range(COLS):
        if MAP[_r][_c] == 'o':
            blk = DSL[max(0, (_r - 1) * FINE):(_r + 2) * FINE, max(0, (_c - 1) * FINE):(_c + 2) * FINE]
            DSLV[_r * FINE:(_r + 1) * FINE, _c * FINE:(_c + 1) * FINE] = np.min(blk[np.isfinite(blk)]) + 6
# --- guides
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GUMOF = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
SS = 2; FOOT = 78 * SS; MZ = SP0 + 'pixellab/maze/anim/'
SRUN = {g: seq(SP0 + f'pixellab/race/{g}_run', 2) for g in ['joy', 'cyrus', 'cleo', 'ray']}
FRUN = {g: seq(MZ + f'{g}_frun', 2) for g in NAMES}
PANIC = {g: seq(MZ + f'{g}_panic', 2) for g in NAMES}
SLIDE = {g: seq(MZ + f'{g}_slide', 2, 1, 8) for g in NAMES}
STAND = {g: seq(MZ + f'{g}_frun', 2, 0, 1)[0] for g in NAMES}
fl = lambda im: im.transpose(Image.FLIP_LEFT_RIGHT)
SRUNL = {g: [fl(f) for f in v] for g, v in SRUN.items()}; SLIDEL = {g: [fl(f) for f in v] for g, v in SLIDE.items()}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
def face(name, rad):
    im = Image.open(SP0 + 'syeda_src/' + SRC[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 34) for n in NAMES}
R = 22; SL = 0.5
SPOTS = [((9, 3), 'acv'), ((12, 9), 'mush'), ((16, 3), 'mel'), ((9, 9), 'cre')]  # same spots, cols mapped
def spot_xy(rc): return (rc[1] * C + C / 2, rc[0] * C + C / 2 + 8)
def cell_of(x, y): return int(y // FC), int(x // FC)
def wall_at(x, y, ghost=False):
    r, c = int(y // C), int(x // C)
    if ghost and 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] == 'o': return False
    return not passable(r, c)
def pillar_at(x, y):
    r, c = int(y // C), int(x // C); return 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] == 'o'
T_START, T_SH = 3.0, 4.2
SA = float(os.environ.get('SA', '4.4')); SB = float(os.environ.get('SB', '0.30')); VB = float(os.environ.get('VB', '165'))
PUSH = 9.0; BT, BK = 2.5, 1.45
def prog(s):
    fr, fc = cell_of(s['x'], s['y']); return DEX[fr, fc]
def sim(seed, dur=34.0):
    rnd = random.Random(seed)
    racers = {}; slots = list(range(5)); rnd.shuffle(slots)
    for i, n in enumerate(NAMES):
        racers[n] = dict(x=2.3 * C + slots[i] * 2.1 * C, y=2.2 * C + rnd.uniform(0, 1.0) * C, vx=0.0, vy=0.0, base=rnd.uniform(VB, VB * 1.13),
                         ph=rnd.uniform(0, 6.28), caught=None, out=None, mode='down', slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, dist=0.0)
    taken = {}; frames = []; front = 0.0; bursts = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t > T_SH: front += dt * (SA + 2 * SB * (t - T_SH))
        for n, s in racers.items():
            if s['caught'] is not None or s['out'] is not None or t < T_START: continue
            sliding = t - s['slide'] < SL or (s['slide'] > 0 and pillar_at(s['x'], s['y']))
            sp = s['base'] * (1 + 0.22 * math.sin(0.9 * t + s['ph']) + 0.12 * math.sin(2.3 * t + 2 * s['ph']))
            if s['boost'] is not None and t - s['boost'] < BT: sp *= BK
            if sliding:
                sp *= 1.2; s['vx'] += (s['sdx'] * sp - s['vx']) * 0.3; s['vy'] += (s['sdy'] * sp - s['vy']) * 0.3
            else:
                fr, fc = cell_of(s['x'], s['y'])
                gx, gy = -GX[fr, fc], -GY[fr, fc]; L = math.hypot(gx, gy) or 1
                wob = 0.4 * math.sin(3.7 * t + s['ph'] * 3); dx, dy = gx / L, gy / L
                tx, ty = dx - dy * wob, dy + dx * wob
                s['vx'] += (tx * sp - s['vx']) * 0.12; s['vy'] += (ty * sp - s['vy']) * 0.12
            v = math.hypot(s['vx'], s['vy']) or 1
            if not sliding and t - s['slide'] > 1.0 and t > T_START + 0.8:
                ux, uy = s['vx'] / v, s['vy'] / v
                if any(pillar_at(s['x'] + ux * d, s['y'] + uy * d) for d in (R + 10, R + 26)):
                    s['slide'] = t; s['sdx'], s['sdy'] = ux, uy; sliding = True
            nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
            for _ in range(2):
                for ax, ay in ((R, 0), (-R, 0), (0, R), (0, -R), (R * .7, R * .7), (-R * .7, R * .7), (R * .7, -R * .7), (-R * .7, -R * .7)):
                    if wall_at(nx + ax, ny + ay, sliding):
                        if ax: nx -= ax * 0.18; s['vx'] *= -0.4
                        if ay: ny -= ay * 0.18; s['vy'] *= -0.4
            s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
            for m, o in racers.items():
                if m == n or o['caught'] is not None or o['out'] is not None: continue
                if sliding or t - o['slide'] < SL: continue
                ddx, ddy = (s['x'] - o['x']), (s['y'] - o['y']) * 1.6; dd = math.hypot(ddx, ddy)
                if 0 < dd < 2 * R + 8:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and t - s['slide'] > 1.0 and t > T_START + 0.8:
                        v2 = math.hypot(s['vx'], s['vy']) or 1
                        s['slide'] = t; s['sdx'], s['sdy'] = s['vx'] / v2, s['vy'] / v2; sliding = True; continue
                    push = (2 * R + 8 - dd) / 2; s['x'] += ddx / dd * push * 0.8; s['y'] += ddy / dd * push * 0.5
            v = math.hypot(s['vx'], s['vy']) or 1
            s['mode'] = 'down' if s['vy'] > 0.72 * v else 'side'; s['sliding'] = sliding
            for k, (rc, kind) in enumerate(SPOTS):
                if k in taken: continue
                gx_, gy_ = spot_xy(rc)
                if math.hypot(s['x'] - gx_, s['y'] - gy_) < 50:
                    taken[k] = (n, t); s['boost'] = t; front = max(0.0, front - PUSH); bursts.append((t, n, s['x'], s['y'], kind))
            fr, fc = cell_of(s['x'], s['y'])
            if int(s['y'] // C) == EX_R and int(s['x'] // C) in EX_C: s['out'] = t
            elif DSL[fr, fc] < front - 1.5: s['caught'] = t
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], caught=s['caught'] is not None and s['caught'] <= t, ct=s['caught'],
                               out=s['out'] is not None and s['out'] <= t, mode=s['mode'], slide=s['slide'], sliding=s['sliding'], boost=s['boost'], dist=s['dist']) for n, s in racers.items()}, front, dict(taken)))
        if any(s['out'] is not None for s in racers.values()) and all(s['out'] is not None or s['caught'] is not None for s in racers.values()): break
    return racers, frames, bursts
def score(seed):
    rc, fr, bu = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in rc.values() if s['caught'] is not None)
    if len(outs) != 1 or len(caught) != 3 or len(bu) < 2: return None
    tw, win = outs[0]
    if not (14 < tw < 21) or max(caught) < tw - 2.5 or min(caught) < 7: return None
    return round(tw, 2), win, len(bu), [round(c, 1) for c in caught]
if sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(os.environ.get('SA'), os.environ.get('SB'), os.environ.get('VB'), seed, r, flush=True)
    sys.exit()
if sys.argv[1] == 'diag':
    for seed in range(8):
        rc, fr, bu = sim(seed)
        print(seed, {n: (round(s['out'], 1) if s['out'] else None, round(s['caught'], 1) if s['caught'] else None) for n, s in rc.items()}, len(bu))
    sys.exit()
SEED = int(sys.argv[1]); RC, FR, BURSTS = sim(SEED)
win = [n for n, s in RC.items() if s['out'] is not None][0]; T_OUT = RC[win]['out']
print('winner', win, round(T_OUT, 2), {n: (round(s['caught'], 1) if s['caught'] else None) for n, s in RC.items()}, [(round(b[0], 1), b[1], b[4]) for b in BURSTS])
# ---- static assets for render
BGF = [b.crop((594, 6, 594 + 540, 6 + 960)).resize((W, H), Image.NEAREST) for b in bg_frames('recov_hd.gif', (int(1920 * 0.9), int(1080 * 0.9)), step=2, bright=0.45)]
VICF = vic(win, 330)
def shade(t, w=COLS * C // 4, h=ROWS * C // 4):
    xs = np.arange(w)[None, :]; ys = np.arange(h)[:, None]
    v = np.sin(xs / 9.0 + t * 0.9 + ys / 15.0) + np.sin(ys / 7.0 - t * 0.7 + xs / 13.0) + np.sin((xs + ys) / 11.0 + t * 1.3)
    img = np.zeros((h, w, 3)) + np.array([38, 18, 66])
    img[v > 0.6] = [62, 30, 104]; img[v > 1.7] = [104, 62, 168]; img[v > 2.5] = [150, 110, 220]
    return Image.fromarray(img.astype(np.uint8), 'RGB').resize((w * 4, h * 4), Image.NEAREST).convert('RGBA')
STEX = shade(0.0)
FIRE = [up(crop(Image.open(p).convert('RGBA')), 2) for p in sorted(glob.glob(B8 + 'fire_anim/*.png'))[1:]] or [up(crop(Image.open(B8 + 'bonfire/00.png').convert('RGBA')), 2)]
GUMS = {k: gummy(k, 3) for k in GUMK}
rr = random.Random(3)
FLOORPTS = [(r * FINE + rr.randrange(FINE), c * FINE + rr.randrange(FINE)) for r in range(ROWS) for c in range(COLS) if passable(r, c) for _ in range(1)]
SNOW = [(rr.uniform(0, W), rr.uniform(0, H), rr.uniform(40, 110), rr.choice([3, 4, 6]), rr.uniform(0, 6)) for _ in range(140)]
def shadowed(spr, t_in, t):
    k = min(1, (t - t_in) / 0.5)
    a = np.array(spr).astype(float); m = a[..., 3] > 0
    tgt = np.array([50, 25, 80], float)
    a[m, :3] = a[m, :3] * (1 - 0.6 * k) + tgt * 0.6 * k
    out = Image.fromarray(a.astype(np.uint8)); cx = spr.width // 2
    mist = Image.new('L', spr.size, 0); md = ImageDraw.Draw(mist)
    for q in range(5):
        ang = t * 2 + q * 1.25; ex = cx + 34 * math.cos(ang); ey = FOOT - 40 + 50 * math.sin(ang * 0.7) * 0.5
        md.ellipse([ex - 22, ey - 16, ex + 22, ey + 16], fill=int(170 * k))
    tex = STEX.crop((0, 0, spr.width, spr.height)); res = Image.new('RGBA', spr.size, (0, 0, 0, 0))
    res.alpha_composite(out); res.paste(tex, (0, 0), mist)
    return res
END = T_OUT + 3.2; NF = int(END * FPS)
# vertical camera: keep the leader low in the view and the pack in frame
BH = ROWS * C; CAM = []; cy = 0.0
for f in range(NF):
    st_ = FR[min(f, len(FR) - 1)][0]; t = f / FPS
    alive = [n for n in NAMES if not st_[n]['caught'] and not st_[n]['out']]
    if t >= T_START and alive:
        ys = [st_[n]['y'] for n in alive]; lead, last = max(ys), min(ys)
        tgt = max(lead - VH + 250, min((lead + last) / 2 - VH * 0.5, lead - 330))
    elif t >= T_START: tgt = cy
    else: tgt = 0
    tgt = min(max(0, tgt), BH - VH); cy += (tgt - cy) * 0.06; CAM.append(cy)
print('camera range', round(min(CAM)), round(max(CAM)))
wr = Writer('v81_noaudio.mp4'); events = []; caught_seen = set(); slides_seen = set(); ghosts = {n: [] for n in NAMES}
for f in range(NF):
    t = f / FPS; st, front, taken = FR[min(f, len(FR) - 1)]
    img = BGF[int(t * 5) % len(BGF)].copy(); camy = int(round(CAM[f]))
    b = board.copy()
    if front > 0:
        mask = (DSLV < front)
        mi = Image.fromarray(mask.astype(np.uint8) * 230, 'L').resize((COLS * C, ROWS * C), Image.NEAREST)
        tex = shade(t)
        edge = Image.fromarray(((DSLV < front) & (DSLV > front - 2.4)).astype(np.uint8) * 150, 'L').resize(mi.size, Image.NEAREST)
        b.paste(tex, (0, 0), mi)
        b.paste(Image.new('RGBA', mi.size, (190, 120, 255, 255)), (0, 0), edge)
        for r in range(ROWS):
            for c in range(COLS):
                if is_wall(r, c): b.alpha_composite(board.crop((c * C, r * C, c * C + C, r * C + C)), (c * C, r * C))
        # eyes in the dark
        bd2 = ImageDraw.Draw(b)
        for i, (fr_, fc_) in enumerate(FLOORPTS):
            dd = DSL[fr_, fc_]
            if front - 9 < dd < front - 2.5 and (i * 7 + int(t * 1.3)) % 5 == 0:
                if (int(t * 4) + i) % 9 == 0: continue
                ex, ey = fc_ * FC + 8, fr_ * FC + 8
                bd2.rectangle([ex - 9, ey - 3, ex - 3, ey + 3], fill=(240, 235, 255)); bd2.rectangle([ex + 3, ey - 3, ex + 9, ey + 3], fill=(240, 235, 255))
    # pines on wall tops
    for (pr, pc) in PINES: b.alpha_composite(PINE, (int(pc * C), int(pr * C)))
    for (pr, pc) in SMALLP: b.alpha_composite(PINE1, (pc * C + 2, pr * C + 2))
    # gummies
    bd2 = ImageDraw.Draw(b)
    for k, (rc, kind) in enumerate(SPOTS):
        gx_, gy_ = spot_xy(rc)
        if k not in taken or t < taken[k][1]:
            bob = int(6 * math.sin(t * 4 + k))
            layer(b, lambda dd: [dd.ellipse([gx_ - r_, gy_ - r_ + bob - 12, gx_ + r_, gy_ + r_ + bob - 12], fill=(255, 210, 120, a_)) for r_, a_ in ((48, 45), (34, 70), (22, 90))])
            g = GUMS[kind]; b.alpha_composite(g, (int(gx_ - g.width / 2), int(gy_ - g.height / 2 + bob - 12)))
    # lamps
    for (r, c) in LAMPS:
        lx, ly = c * C + C / 2, r * C + C - 6
        layer(b, lambda dd: [dd.ellipse([lx - r_, ly - 30 - r_ * 0.7, lx + r_, ly - 30 + r_ * 0.7], fill=(255, 190, 90, a_)) for r_, a_ in ((80, 18), (52, 26), (30, 34))])
        b.alpha_composite(LAMP, (int(lx - LAMP.width / 2), int(ly - LAMP.height)))
    # bonfire at the exit
    fx, fy = EX_C[1] * C + C / 2, EX_R * C + 8
    layer(b, lambda dd: [dd.ellipse([fx - r_, fy - r_ * 0.75, fx + r_, fy + r_ * 0.75], fill=(255, 170, 80, a_)) for r_, a_ in ((200 + 10 * math.sin(t * 7), 30), (130, 45), (80, 60))])
    fi = FIRE[int(t * 10) % len(FIRE)]; b.alpha_composite(fi, (int(fx - fi.width / 2), int(fy - fi.height / 2 + 10)))
    # characters
    order = sorted([n for n in NAMES if not st[n]['out']], key=lambda n: st[n]['y'])
    for n in order:
        s = st[n]; x, y = s['x'], s['y']
        boosted = s['boost'] is not None and 0 <= t - s['boost'] < BT
        if s['caught']:
            spr = shadowed(PANIC[n][int(t * 12) % 8], s['ct'], t)
            if n not in caught_seen: caught_seen.add(n); events.append((round(t, 3), 'whoosh_8bit'))
        elif t < T_START: spr = STAND[n]
        elif s['sliding']:
            k = min(6, int((t - s['slide']) / SL * 7)); spr = (SLIDEL if s['vx'] < 0 else SLIDE)[n][k]
            if (n, s['slide']) not in slides_seen: slides_seen.add((n, s['slide'])); events.append((round(t, 3), 'jump'))
            layer(b, lambda dd: [dd.ellipse([x - math.copysign(1, s['vx']) * (20 + q * 22) - 12, y - 14 - q * 4, x - math.copysign(1, s['vx']) * (20 + q * 22) + 12, y + 6], fill=(240, 245, 255, 170 - q * 45)) for q in range(3)])
        else:
            ph = int(s['dist'] / 22) % 8
            spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        if boosted and not s['caught']:
            ghosts[n] = (ghosts[n] + [(spr, x, y)])[-5:]
            for i, (gs, gx2, gy2) in enumerate(ghosts[n][:-1]):
                al = gs.getchannel('A').point(lambda p, i=i: int(p * (0.12 + 0.08 * i)))
                tint = Image.new('RGBA', gs.size, (255, 200, 90, 255)); tint.putalpha(al); b.alpha_composite(tint, (int(gx2 - gs.width / 2), int(gy2 - FOOT)))
        else: ghosts[n] = []
        if not s['caught']: layer(b, lambda dd: dd.ellipse([x - 26, y - 8, x + 26, y + 8], fill=(20, 30, 60, 90)))
        b.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    # light bursts
    for (tb, n, bx, by, kind) in BURSTS:
        u = t - tb
        if 0 <= u < 1.0:
            rad = 40 + 520 * u; al = int(220 * (1 - u))
            layer(b, lambda dd: (dd.ellipse([bx - rad, by - 60 - rad, bx + rad, by - 60 + rad], outline=(255, 230, 150, al), width=14), dd.ellipse([bx - rad * 0.6, by - 60 - rad * 0.6, bx + rad * 0.6, by - 60 + rad * 0.6], fill=(255, 240, 200, int(al * 0.35)))))
            text_layer(b, [(min(max(bx, 182), 650), by - FOOT - 40 - u * 50, 'LIGHT BURST!', 28, (255, 220, 110), 5, int(255 * min(1, (1 - u) / 0.3)))])
        if abs(t - tb) < 0.5 / FPS: events.append((round(tb, 3), 'powerup_8bit')); events.append((round(tb + 0.05, 3), 'chime'))
    img.alpha_composite(b.crop((0, camy, COLS * C, camy + VH)), (OX, VY0))
    d = ImageDraw.Draw(img); d.rectangle([OX - 8, VY0 - 8, OX + COLS * C + 7, VY1 + 7], outline=(30, 28, 50), width=8)
    # snow
    layer(img, lambda dd: [dd.rectangle([(sx + 30 * math.sin(t * 0.8 + ph)) % W, (sy + t * vy) % H, (sx + 30 * math.sin(t * 0.8 + ph)) % W + sz, (sy + t * vy) % H + sz], fill=(240, 245, 255, 200)) for sx, sy, vy, sz, ph in SNOW])
    # header
    layer(img, lambda dd: dd.rounded_rectangle([118, ROSTER_Y - 46, 838, ROSTER_Y + 46], 20, fill=(12, 10, 26, 210)))
    for i, n in enumerate(NAMES):
        ix = 478 + (i - 1.5) * 170; iy = ROSTER_Y; ic = ICON[n]; s = st[n]
        if s['caught']: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(ix - ic.width / 2), int(iy - ic.height / 2)))
        d = ImageDraw.Draw(img)
        if s['caught']: d.line([ix - 26, iy - 26, ix + 26, iy + 26], fill=(150, 90, 230), width=9); d.line([ix - 26, iy + 26, ix + 26, iy - 26], fill=(150, 90, 230), width=9)
        if s['out']: d.ellipse([ix - 42, iy - 42, ix + 42, iy + 42], outline=(255, 214, 60), width=6)
    if t < T_START:
        text_layer(img, [(478, 1020, 'PICK ONE!', 64, (255, 255, 255), 8, 255), (478, 1110, str(3 - int(t)), 110, (255, 214, 60), 10, 255)])
        if abs(t - int(t)) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
    elif t < T_START + 0.7:
        text_layer(img, [(478, 1060, 'RUN!', 110, (255, 214, 60), 10, int(255 * (T_START + 0.7 - t) / 0.7))])
        if abs(t - T_START) < 0.5 / FPS: events.append((round(t, 3), 'go_8bit'))
    if t >= T_OUT:
        u = t - T_OUT
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 14, int(150 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1080 - vf.height))
        text_layer(img, [(478, 1130, LABEL[win] + ' MADE IT!', 46, (255, 214, 60), 8, 255), (478, 1230, 'DID YOUR GUIDE WIN?', 36, (255, 255, 255), 6, int(255 * min(1, max(0, u - 0.6) / 0.4)))])
        if not any(e[1] == 'victory' for e in events): events.append((round(T_OUT, 3), 'victory'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p81_{f:04d}.png')
wr.close(); json.dump(events, open('v81_ev.json', 'w')); print('done', END)
