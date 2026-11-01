# n03 box maze (Oct 30 post): remake of the posted "Outrun the Shadow" box maze (viral_dl/1118_2000_outrun_the_shadow.mp4)
# Same format: checkered maze, four guild-coloured brick gates at the top, face boxes, a shadow flooding in behind them,
# a dragon on its treasure at the checkered exit, face roster at the bottom.  Upgraded graphics (PixelLab marble hall floor,
# dungeon brick walls with lit rims and brick faces, glowing shadow with eyes, polished boxes, cleaner HUD) and clean physics:
# rigid square boxes, sub-stepped integration, restitution bounces off walls and corners, box-box elastic contacts
# (equal masses, never overlapping), continuous thrust along the maze (no snapping, no teleports, no speed jumps).
import sys, os
S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S_ + 'fork1'); from common import *
sys.path.insert(0, S_ + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
from collections import deque
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (110, 200, 80), 'cleo': (90, 150, 255), 'cyrus': (255, 150, 40), 'ray': (185, 105, 240)}
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
HOOK, HB = hook_fade(['WHO ESCAPES', 'THE SHADOW?'], accent=1)
HOOK_END, _ = hook_fade(['DID YOU', 'CALL IT?'], accent=1)
# ---------------- maze (cell 60px)
C = 60
MAP = [
    "#################",
    "#11#22#33#44#####",
    "#11#22#33#44#####",
    "#gg#gg#gg#gg#####",
    "#...........#####",
    "#...........#####",
    "#..#########XXXX#",
    "#..#.....#..XXXX#",
    "#..#.....#..XXXX#",
    "#..#..#..#..XXXX#",
    "#..#..#..#..#####",
    "#..#..#..#..#####",
    "#..#..#..#..#####",
    "#.....#.....#####",
    "#.....#.....#####",
    "#################"]
# exit room: cols 12-14 rows 6-9 opens on the corridor at rows 7-8 col 11 (see MAP); dragon at its right end, facing left
ROWS, COLS = len(MAP), len(MAP[0])
OX = (W - COLS * C) // 2; OY = int(os.environ.get('OY', '470'))
def wall(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or MAP[r][c] == '#'
GATE_ROW = 3
GATE_COL = {'joy': 1, 'cleo': 4, 'cyrus': 7, 'ray': 10}
EXIT = [(r, c) for r in range(ROWS) for c in range(COLS) if MAP[r][c] == 'X']
def bfs(srcs):
    d = {s: 0 for s in srcs}; q = deque(srcs)
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (r + dr, c + dc)
            if not wall(*n) and n not in d: d[n] = d[(r, c)] + 1; q.append(n)
    return d
DEXIT = bfs(EXIT)
SRC = [(r, c) for r in (1, 2) for c in range(COLS) if MAP[r][c] in '1234']
DSRC = bfs(SRC)
def cell_of(x, y): return int((y - OY) // C), int((x - OX) // C)
def ccenter(r, c): return OX + c * C + C / 2, OY + r * C + C / 2
# ---------------- physics
HS = 28                     # box half-size (56px boxes)
THR, DRAG = float(os.environ.get('THR', '1000')), 2.9     # thrust / linear drag -> cruise ~345 px/s
E_WALL, E_BOX = 0.72, 0.9
SUB = 10
T_GO = 1.2
SPEED_T, SLEEP_T = 2.2, 1.1
def solid_overlap(x, y):
    """wall cells overlapped by the box at centre (x, y)"""
    out = []
    r0, c0 = cell_of(x - HS + 0.01, y - HS + 0.01); r1, c1 = cell_of(x + HS - 0.01, y + HS - 0.01)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if wall(r, c) or (r == GATE_ROW and MAP[r][c] == 'g' and not GATES_OPEN[0]): out.append((r, c))
    return out
GATES_OPEN = [False]
def flow_dir(x, y):
    r, c = cell_of(x, y)
    if (r, c) not in DEXIT: return 0.0, 0.0
    d0 = DEXIT[(r, c)]
    if d0 == 0:                                   # inside the exit room: settle toward the dragon's side
        tx, ty = OX + 12.75 * C, OY + 8.0 * C; vx, vy = tx - x, ty - y; n = math.hypot(vx, vy)
        return (vx / n * min(1, n / 80), vy / n * min(1, n / 80)) if n > 1 else (0.0, 0.0)
    best = None
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (r + dr, c + dc)
        if n in DEXIT and DEXIT[n] < d0 and (best is None or DEXIT[n] < DEXIT[best]): best = n
    tx, ty = ccenter(*best)
    # aim at the next cell, but keep the box's own lane across a 2-wide corridor (no zig-zag toward cell centres)
    if best[0] != r: tx = x
    else: ty = y
    vx, vy = tx - x, ty - y; n = math.hypot(vx, vy) or 1
    return vx / n, vy / n
def sim(seed, dur=22.0):
    rnd = random.Random(seed)
    GATES_OPEN[0] = False
    B = {}
    order = G[:]; rnd.shuffle(order)
    for i, g in enumerate(order): GATE_COL[g] = [1, 4, 7, 10][i]          # which chamber each guide starts in (seeded)
    for g in G:
        cx, cy = ccenter(1, GATE_COL[g]); cx += C / 2                 # chamber centre (2x2 cells)
        B[g] = dict(x=cx + rnd.uniform(-20, 20), y=cy + C / 2 + rnd.uniform(-10, 10), vx=0.0, vy=0.0, thr=THR * rnd.uniform(0.86, 1.12),
                    caught=None, done=None, boost=-9, sleep=-9, sleep0=-9, shield=False, grace=-9)
    gum = {}
    cells = [k for k, v in DEXIT.items() if MAP[k[0]][k[1]] == '.' and 8 < v < 40]
    picks_kinds = ['mush', 'acv', 'mel']; rnd.shuffle(picks_kinds)
    used = []
    for k in picks_kinds:
        while True:
            cc = rnd.choice(cells)
            if all(abs(DEXIT[cc] - DEXIT[u]) > 7 for u in used): break
        used.append(cc); x, y = ccenter(*cc); gum[k] = dict(x=x + rnd.uniform(-12, 12), y=y + rnd.uniform(-12, 12), t=None, who=None)
    sh_t0, sh_v, sh_a = float(os.environ.get('SH0', '2.2')), float(os.environ.get('SHV', '2.2')), float(os.environ.get('SHA', '0.32'))
    ev = []; frames = []; hits = []
    for f in range(int(dur * FPS)):
        t = f / FPS
        if t >= T_GO and not GATES_OPEN[0]: GATES_OPEN[0] = True; ev.append((t, 'gates', None))
        front = 0.0 if t < sh_t0 else sh_v * (t - sh_t0) + 0.5 * sh_a * (t - sh_t0) ** 2
        dt = 1 / FPS / SUB
        for _ in range(SUB):
            for g in G:
                b = B[g]
                if b['caught'] is not None: continue
                fx, fy = (flow_dir(b['x'], b['y']) if t >= T_GO else (0.0, 0.0))
                k = b['thr'] * (1.7 if t - b['boost'] < SPEED_T else 1.0)
                drag = DRAG * (1.7 if t - b['boost'] < SPEED_T else 1.0) ** 0 * (1 / 1.0)
                if t < b['sleep']: fx = fy = 0.0; drag = 9.0                   # asleep: no thrust, skids to a stop
                if b['done'] is not None: drag = 6.0
                b['vx'] += (fx * k - DRAG * b['vx'] * (drag / DRAG)) * dt
                b['vy'] += (fy * k - DRAG * b['vy'] * (drag / DRAG)) * dt
                # move x, resolve walls
                b['x'] += b['vx'] * dt
                for (r, c) in solid_overlap(b['x'], b['y']):
                    wl, wr = OX + c * C, OX + c * C + C
                    if b['vx'] > 0 and b['x'] + HS > wl and b['x'] < wl: b['x'] = wl - HS; hits.append((t, abs(b['vx']))); b['vx'] = -E_WALL * b['vx']
                    elif b['vx'] < 0 and b['x'] - HS < wr and b['x'] > wr: b['x'] = wr + HS; hits.append((t, abs(b['vx']))); b['vx'] = -E_WALL * b['vx']
                b['y'] += b['vy'] * dt
                for (r, c) in solid_overlap(b['x'], b['y']):
                    wt, wb = OY + r * C, OY + r * C + C
                    if b['vy'] > 0 and b['y'] + HS > wt and b['y'] < wt: b['y'] = wt - HS; hits.append((t, abs(b['vy']))); b['vy'] = -E_WALL * b['vy']
                    elif b['vy'] < 0 and b['y'] - HS < wb and b['y'] > wb: b['y'] = wb + HS; hits.append((t, abs(b['vy']))); b['vy'] = -E_WALL * b['vy']
            # box-box contacts (equal masses, restitution E_BOX), resolved along the axis of least penetration
            live = [g for g in G if B[g]['caught'] is None]
            for i in range(len(live)):
                for j in range(i + 1, len(live)):
                    a, c_ = B[live[i]], B[live[j]]
                    px, py = 2 * HS - abs(a['x'] - c_['x']), 2 * HS - abs(a['y'] - c_['y'])
                    if px <= 0 or py <= 0: continue
                    if px < py:
                        s = 1 if a['x'] < c_['x'] else -1; a['x'] -= s * px / 2; c_['x'] += s * px / 2
                        rv = (c_['vx'] - a['vx']) * s
                        if rv < 0:
                            imp = -(1 + E_BOX) * rv / 2; a['vx'] -= s * imp; c_['vx'] += s * imp; hits.append((t, abs(rv)))
                    else:
                        s = 1 if a['y'] < c_['y'] else -1; a['y'] -= s * py / 2; c_['y'] += s * py / 2
                        rv = (c_['vy'] - a['vy']) * s
                        if rv < 0:
                            imp = -(1 + E_BOX) * rv / 2; a['vy'] -= s * imp; c_['vy'] += s * imp; hits.append((t, abs(rv)))
        for g in G:
            b = B[g]
            if b['caught'] is not None: continue
            # pickups
            for k, gm in gum.items():
                if gm['t'] is None and abs(b['x'] - gm['x']) < HS + 14 and abs(b['y'] - gm['y']) < HS + 14:
                    gm['t'] = t; gm['who'] = g; ev.append((t, 'pick', g, k))
                    if k == 'mush': b['boost'] = t
                    elif k == 'acv': b['shield'] = True
                    else:
                        vic = []
                        for m in G:
                            o = B[m]
                            if m == g or o['caught'] is not None or o['done'] is not None: continue
                            if o['shield']: o['shield'] = False; ev.append((t, 'block', m, 'sleep'))
                            else: o['sleep0'] = t; o['sleep'] = t + SLEEP_T; vic.append(m)
                        ev.append((t, 'sleepwave', g, vic))
            r, c = cell_of(b['x'], b['y'])
            if b['done'] is None and (r, c) in DEXIT and DEXIT[(r, c)] == 0 and b['x'] - HS > OX + 12 * C: b['done'] = t; ev.append((t, 'done', g))
            # shadow: a cell is swallowed once the front passes it; the box goes when the cell under its centre is fully dark
            dsc = DSRC.get((r, c), 999)
            if b['done'] is None and front > dsc + 0.85 and t > b['grace']:
                if b['shield']:
                    b['shield'] = False; b['grace'] = t + 0.9; ev.append((t, 'block', g, 'shadow'))
                    fx, fy = flow_dir(b['x'], b['y']); b['vx'] += fx * 420; b['vy'] += fy * 420      # the bubble bounces off the dark (one impulse, not a jump)
                else:
                    b['caught'] = t; ev.append((t, 'caught', g))
        frames.append(({g: (B[g]['x'], B[g]['y'], B[g]['vx'], B[g]['vy'], B[g]['caught'], B[g]['done'], B[g]['boost'], B[g]['sleep'], B[g]['sleep0'], B[g]['shield']) for g in G}, front))
        if all(B[g]['caught'] is not None or B[g]['done'] is not None for g in G) and t > 3:
            if 'tend' not in B[G[0]]: B[G[0]]['tend'] = t
            if t > B[G[0]]['tend'] + float(os.environ.get('TAILSIM', '0')): break
    return B, frames, ev, gum, hits
WANT = os.environ.get('WANT', 'cyrus')
def score(seed):
    B, fr, ev, gum, hits = sim(seed)
    done = [g for g in G if B[g]['done'] is not None]; caught = sorted(B[g]['caught'] for g in G if B[g]['caught'] is not None)
    if done != [WANT] or len(caught) != 3: return None
    if GATE_COL[WANT] == 1 and not os.environ.get('ANYCH'): return None          # more fun if the winner doesn't just start in front
    tw = B[WANT]['done']
    if not (10.0 < tw < 15.5) or caught[0] < 3.5: return None
    gaps = [b - a for a, b in zip(caught, caught[1:])]
    if min(gaps) < float(os.environ.get('MING', '0.9')) or tw - caught[-1] < 0.6 or tw - caught[-1] > 3.5: return None
    picks = [e for e in ev if e[1] == 'pick' and e[0] < tw]
    if len(picks) < int(os.environ.get('NPICK', '3')): return None
    bt = sorted(e[0] for e in ev if e[1] in ('pick', 'block', 'caught') and e[0] <= tw)
    if any(b - a < float(os.environ.get('SEP', '0.8')) for a, b in zip(bt, bt[1:])): return None
    pk = {e[3]: e for e in picks}
    if 'acv' in pk and not any(e[1] == 'block' and e[3] == 'shadow' for e in ev): return None      # the shield has to save someone
    if any(e[0] < T_GO + 1.0 for e in picks): return None
    return round(tw, 2), [round(c, 1) for c in caught], [(round(e[0], 1), e[1], e[2], e[3] if len(e) > 3 and isinstance(e[3], str) else '') for e in ev if e[1] in ('pick', 'block', 'caught')]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
os.environ.setdefault('TAILSIM', '7')
BB, FR, EV, GUM, HITS = sim(SEED)
T_WIN = BB[WANT]['done']
print('win', T_WIN, {g: BB[g]['caught'] for g in G})
for e in EV: print('  ', round(e[0], 2), e[1:])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()

# =====================================================================  RENDER
T_FIRE = T_WIN + 1.1                       # the shadow keeps coming... the dragon rears up and breathes fire down the corridor
FIRE_FPS = 10
T_REC0 = T_FIRE + 0.25; REC_D = 1.4        # the fire burns the shadow back out of the maze
T_CARD = T_REC0 + REC_D + 0.55             # winner reveal
T_LOOP = T_CARD + 2.6; NF = int(round(T_LOOP * FPS))
print('beats: win', round(T_WIN, 2), 'fire', round(T_FIRE, 2), 'card', round(T_CARD, 2), 'end', round(T_LOOP, 2))
def frame_at(t): return FR[min(int(round(t * FPS)), len(FR) - 1)]
F_PEAK = min(frame_at(T_REC0)[1], min(DSRC[x] for x in EXIT) - 0.02)
FMAX = min(DSRC[x] for x in EXIT) - 0.02          # the dark never crosses into the dragon's room: it stalls at the doorway
def front_at(t):
    if t < T_REC0: return min(frame_at(t)[1], FMAX)
    u = min(1.0, (t - T_REC0) / REC_D); return F_PEAK * (1 - u) ** 2 - 1.5 * u
# ---------------- assets
hall_m = json.load(open(S_ + 'fork_a8/gen/hall_meta.json')); hall_s = Image.open(S_ + 'fork_a8/gen/hall_sheet.png').convert('RGBA')
def tl_(m, sh, name):
    for t_ in m['tileset_data']['tiles']:
        if t_['name'] == name:
            b = t_['bounding_box']; return sh.crop((b['x'], b['y'], b['x'] + b['width'], b['y'] + b['height']))
FLOOR_T = up(tl_(hall_m, hall_s, 'wang_0'), 2)                      # polished cream/grey marble checker (PixelLab)
wsheet = Image.open(S_ + 'pixellab/maze/walls_sheet.png').convert('RGBA')
BRICK = up(wsheet.crop((77, 13, 128, 56)), 2)                       # PixelLab dungeon stone bricks
def tint(im, col, k=0.75):
    a = np.array(im).astype(float); g_ = a[..., :3].mean(2, keepdims=True) / 255.0
    a[..., :3] = a[..., :3] * (1 - k) + (np.array(col)[None, None, :] * (0.35 + 0.95 * g_)) * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
FACE = {}
for g, fn in [('joy', 'idle_0.gif'), ('cyrus', 'idle_1.gif'), ('ray', 'idle_2.gif'), ('cleo', 'idle_3.gif')]:
    im = Image.open(A + fn); im.seek(0); im = im.convert('RGBA').resize((92, 92), Image.NEAREST); bb = im.getbbox()
    cx = 46 if g != 'cleo' else 47
    FACE[g] = im.crop((cx - 12, 15, cx + 12, 39))                   # 24x24 head crop of Syeda's idle
ROSTER_FACE = {g: up(FACE[g], 3) for g in G}
VICF = {g: [up(f, 3) for f in [Image.open(A + VIC[g]).convert('RGBA')]] for g in G}
def vic_frames(g):
    im = Image.open(A + VIC[g]); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), 5))
    return out
VIC_W = vic_frames(WANT)
GUMI = {k: up(Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA'), 2 if k == 'mush' else 1 if False else 2) for k in ('mush', 'acv', 'mel')}
GUMI = {k: (v if v.width <= 60 else v.resize((int(v.width * 52 / v.height), 52), Image.NEAREST)) for k, v in GUMI.items()}
DRG = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(S_ + 'fork_b5/dragon_fire/*.png'))]
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
        if not wall(r, c): fd.rectangle([c * C, r * C, c * C + C - 1, r * C + C - 1], fill=255)
fl2 = Image.new('RGBA', floor.size, (0, 0, 0, 0)); fl2.paste(floor, (0, 0), fmask); MZ.alpha_composite(fl2, (mx0, my0))
d = ImageDraw.Draw(MZ)
# checkered exit room (the finish)
for r, c in EXIT:
    for i in range(2):
        for j in range(2):
            col_ = (238, 238, 238, 255) if (i + j + r + c) % 2 == 0 else (28, 28, 34, 255)
            d.rectangle([OX + c * C + j * 30, OY + r * C + i * 30, OX + c * C + j * 30 + 29, OY + r * C + i * 30 + 29], fill=col_)
# walls: dark slate top with a lit stone rim, brick face where a wall drops onto the floor below
rnd_ = random.Random(7)
for r in range(ROWS):
    for c in range(COLS):
        if not wall(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        d.rectangle([x0, y0, x0 + C - 1, y0 + C - 1], fill=(38, 34, 52, 255))
        for k in range(6):
            px_, py_ = x0 + rnd_.randint(2, C - 10), y0 + rnd_.randint(2, C - 10)
            d.rectangle([px_, py_, px_ + 6, py_ + 4], fill=(48, 44, 64, 255))
for r in range(ROWS):
    for c in range(COLS):
        if not wall(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        if not wall(r + 1, c) and r + 1 < ROWS:              # brick face (3/4 view lip) on the wall's south side
            MZ.alpha_composite(BRICK.crop((0, 0, C, 26)), (x0, y0 + C - 26))
            d.rectangle([x0, y0 + C - 28, x0 + C - 1, y0 + C - 27], fill=(150, 146, 168, 255))
        rim = (122, 118, 142, 255)
        if not wall(r - 1, c) and r > 0: d.rectangle([x0, y0, x0 + C - 1, y0 + 3], fill=rim)
        if not wall(r, c - 1) and c > 0: d.rectangle([x0, y0, x0 + 3, y0 + C - 1], fill=rim)
        if not wall(r, c + 1) and c + 1 < COLS: d.rectangle([x0 + C - 4, y0, x0 + C - 1, y0 + C - 1], fill=rim)
# soft contact shadow on the floor under each wall lip
ao = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ao)
for r in range(ROWS):
    for c in range(COLS):
        if not wall(r, c) and wall(r - 1, c):
            for k in range(10): ad.rectangle([OX + c * C, OY + r * C + k, OX + c * C + C - 1, OY + r * C + k], fill=(10, 6, 20, 90 - k * 9))
MZ.alpha_composite(ao)
def gate_img(g):
    im = tint(BRICK.crop((0, 0, 2 * C, C)) if BRICK.width >= 2 * C else BRICK.resize((2 * C, C), Image.NEAREST), COL[g], 0.8)
    im2 = Image.new('RGBA', (2 * C, C)); im2.alpha_composite(BRICK.resize((2 * C, BRICK.height), Image.NEAREST).crop((0, 0, 2 * C, C)) if BRICK.height >= C else im)
    t2 = tint(BRICK.resize((2 * C, C), Image.NEAREST), COL[g], 0.8); dd = ImageDraw.Draw(t2)
    dd.rectangle([0, 0, 2 * C - 1, 3], fill=tuple(min(255, int(v * 1.25)) for v in COL[g]) + (255,)); dd.rectangle([0, C - 4, 2 * C - 1, C - 1], fill=(20, 14, 26, 255))
    return t2
GATE = {g: gate_img(g) for g in G}
# roster plates (HUD)
RY0 = my1 + 34
def roster(img, t):
    d_ = ImageDraw.Draw(img)
    for i, g in enumerate(G):
        x0 = 36 + i * 254; x1 = x0 + 238
        caught = BB[g]['caught'] is not None and BB[g]['caught'] <= t and not (t >= T_REC0 and front_at(t) < DSRC.get(cell_of(*frame_at(BB[g]['caught'])[0][g][:2]), 0))
        win = t >= T_WIN and g == WANT
        layer(img, lambda dd, x0=x0, x1=x1: dd.rounded_rectangle([x0, RY0, x1, RY0 + 100], 14, fill=(14, 10, 22, 225), outline=COL[g] + (255,) if not win else (255, 214, 60, 255), width=4 if not win else 6))
        fc = ROSTER_FACE[g]
        if caught: fc = ImageEnhance.Brightness(ImageEnhance.Color(fc).enhance(0.15)).enhance(0.45)
        img.alpha_composite(fc, (x0 + 10, RY0 + 14))
        nm = NAME[g] if g != 'ray' else 'RAY'
        d_ = ImageDraw.Draw(img); d_.text((x0 + 92, RY0 + 30), nm, font=F(30 if len(nm) < 5 else 26), fill=(120, 110, 130) if caught else COL[g], stroke_width=4, stroke_fill=(10, 6, 16))
        if caught:
            d_.line([x0 + 12, RY0 + 16, x0 + 82, RY0 + 86], fill=(230, 50, 60), width=7); d_.line([x0 + 12, RY0 + 86, x0 + 82, RY0 + 16], fill=(230, 50, 60), width=7)
# shadow texture: deep purple with slow swirls
NZ = Image.effect_noise((COLS * C // 4, ROWS * C // 4), 60).resize((COLS * C, ROWS * C), Image.BICUBIC).filter(ImageFilter.GaussianBlur(5))
NZa = np.array(NZ).astype(float) / 255.0
SHC = np.zeros((ROWS * C, COLS * C, 4), np.uint8)
SHC[..., 0] = (22 + 30 * NZa).astype(np.uint8); SHC[..., 1] = (10 + 12 * NZa).astype(np.uint8); SHC[..., 2] = (40 + 50 * NZa).astype(np.uint8); SHC[..., 3] = 246
SHADOW_TEX = Image.fromarray(SHC)
CELLS = [(r, c) for r in range(ROWS) for c in range(COLS) if not wall(r, c)]
def shadow_layer(t, fr_):
    m = Image.new('L', (COLS * C, ROWS * C), 0); md = ImageDraw.Draw(m); rim = []
    for (r, c) in CELLS:
        ds = DSRC.get((r, c))
        if ds is None: continue
        cov = fr_ - ds
        if cov <= 0: continue
        if cov >= 1: md.rectangle([c * C, r * C, c * C + C - 1, r * C + C - 1], fill=255)
        else:
            # the dark creeps across the cell from the side it came from (no popping)
            best = min(((DSRC.get((r + dr, c + dc), 999), dr, dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))))
            _, dr, dc = best; k = max(1, int(C * cov))
            if dr == -1: box_ = [c * C, r * C, c * C + C - 1, r * C + k]; edge = [c * C, r * C + k - 3, c * C + C - 1, r * C + k]
            elif dr == 1: box_ = [c * C, r * C + C - k, c * C + C - 1, r * C + C - 1]; edge = [c * C, r * C + C - k, c * C + C - 1, r * C + C - k + 3]
            elif dc == -1: box_ = [c * C, r * C, c * C + k, r * C + C - 1]; edge = [c * C + k - 3, r * C, c * C + k, r * C + C - 1]
            else: box_ = [c * C + C - k, r * C, c * C + C - 1, r * C + C - 1]; edge = [c * C + C - k, r * C, c * C + C - k + 3, r * C + C - 1]
            md.rectangle(box_, fill=255); rim.append(edge)
    L = Image.new('RGBA', (COLS * C, ROWS * C), (0, 0, 0, 0)); L.paste(SHADOW_TEX, (int(6 * math.sin(t)), 0), m)
    dd = ImageDraw.Draw(L)
    for b_ in rim: dd.rectangle(b_, fill=(170, 110, 250, 220) if t < T_REC0 else (255, 160, 60, 240))   # glowing leading edge (burning while it retreats)
    # eyes in the dark
    for (r, c) in CELLS:
        ds = DSRC.get((r, c))
        if ds is None or fr_ - ds < 1.5 or (r * 7 + c * 13) % 6: continue
        ex, ey = c * C + 18 + (r * 11) % 14, r * C + 22 + (c * 5) % 12
        if (int(t * 1.6 + r + c) % 7) == 0: dd.rectangle([ex, ey + 4, ex + 22, ey + 6], fill=(230, 220, 255, 230))
        else: dd.ellipse([ex, ey, ex + 7, ey + 9], fill=(240, 235, 255, 240)); dd.ellipse([ex + 15, ey, ex + 22, ey + 9], fill=(240, 235, 255, 240))
    return L
def box_img(g, k=1.0, dark=0.0):
    b = Image.new('RGBA', (2 * HS, 2 * HS), (0, 0, 0, 0)); dd = ImageDraw.Draw(b)
    dd.rectangle([0, 0, 2 * HS - 1, 2 * HS - 1], fill=(14, 10, 20, 255))
    dd.rectangle([2, 2, 2 * HS - 3, 2 * HS - 3], fill=COL[g] + (255,))
    b.alpha_composite(up(FACE[g], 2), (4, 4))
    dd.rectangle([4, 4, 2 * HS - 5, 2 * HS - 5], outline=(255, 255, 255, 70), width=2)
    dd.rectangle([6, 6, 14, 8], fill=(255, 255, 255, 170))
    if dark > 0: b = Image.blend(b, Image.new('RGBA', b.size, (30, 16, 50, 255)), dark).copy(); b.putalpha(Image.new('L', b.size, 255))
    if k != 1.0: b = b.resize((max(2, int(b.width * k)), max(2, int(b.height * k))), Image.NEAREST)
    return b
BOXI = {g: box_img(g) for g in G}
def SN(g): return NAME[g]
RAWS = []
for e in EV:
    if e[1] == 'pick': RAWS.append((e[0], ('pop', e[2], SN(e[2]) + ': ' + POWER[e[3]][0], POWER[e[3]][1])))
    elif e[1] == 'block': RAWS.append((e[0], ('pop', e[2], SN(e[2]) + ': BLOCKED!', (130, 240, 100))))
    elif e[1] == 'caught': RAWS.append((e[0], ('caught', e[2], SN(e[2]) + ' CAUGHT!', (255, 120, 120))))
RAWS.append((T_WIN, ('win', WANT, SN(WANT) + ' ESCAPED!', (255, 214, 60))))
RAWS.sort(key=lambda z: z[0]); SCHED = []
for i, (t0, it) in enumerate(RAWS):
    st0 = max(t0, SCHED[-1][1] + 0.1) if SCHED else t0
    nxt = RAWS[i + 1][0] if i + 1 < len(RAWS) else 1e9
    en = min(st0 + 0.95, max(st0 + 0.6, nxt - 0.1)) if it[0] != 'win' else T_FIRE - 0.1
    SCHED.append((st0, en, it))
print('stamps', [(round(a, 2), round(b, 2), it[2]) for a, b, it in SCHED])
# trails: recent positions
def pos_at(g, t):
    s_ = frame_at(t)[0][g]; return s_[0], s_[1]
STILLS = [float(x) for x in os.environ.get('STILLS', '').split(',') if x]
wr = None if STILLS else Writer('n03_noaudio.mp4')
SW_X = {}
for f in range(NF):
    t = f / FPS
    if STILLS and not any(abs(t - x) < 0.5 / FPS for x in STILLS): continue
    st, _fr = frame_at(t); fr_ = front_at(t)
    img = BG[int(t * 5) % len(BG)].copy()
    img.alpha_composite(MZ)
    # gates slide sideways into the wall (clipped to the doorway)
    for g in G:
        c0 = GATE_COL[g]; gx, gy = OX + c0 * C, OY + GATE_ROW * C
        u = 0.0 if t < T_GO else min(1.0, (t - T_GO) / 0.35); off = int(2 * C * u * u)
        if off < 2 * C:
            gi = GATE[g].crop((0, 0, 2 * C - off, C)); img.alpha_composite(gi, (gx + off, gy))
    # gummies on the floor (bob in place, soft glow)
    for k, gm in GUM.items():
        if gm['t'] is not None and t >= gm['t']: continue
        gi = GUMI[k]; bob = 4 * math.sin(t * 4 + gm['x'])
        layer(img, lambda dd, gm=gm, k=k: [dd.ellipse([gm['x'] - 30 + q * 8, gm['y'] - 30 + q * 8, gm['x'] + 30 - q * 8, gm['y'] + 30 - q * 8], fill=POWER[k][1] + (35 + q * 25,)) for q in range(3)])
        img.alpha_composite(gi, (int(gm['x'] - gi.width / 2), int(gm['y'] - gi.height / 2 + bob)))
    # trails + boxes (live), shadow over everything on the floor, then swallowed boxes inside it
    live_draw = []
    for g in G:
        x, y, vx, vy, ca, dn, boost, sleep, sleep0, shield = st[g]
        if ca is not None and ca <= t: continue
        if t >= T_CARD and g == WANT: continue
        sp = math.hypot(vx, vy)
        for q in range(1, 6):
            px_, py_ = pos_at(g, max(0, t - q * 0.04))
            a_ = int(min(1, sp / 350) * (110 - q * 18)); s_ = int(HS * (1 - q * 0.1))
            if a_ > 0: layer(img, lambda dd, px_=px_, py_=py_, a_=a_, s_=s_, g=g: dd.rectangle([px_ - s_, py_ - s_, px_ + s_, py_ + s_], fill=COL[g] + (a_,)))
        live_draw.append(g)
    img.alpha_composite(shadow_layer(t, fr_), (OX, OY))
    for g in G:                                               # swallowed: sinks into the dark; freed when the fire burns it back
        x, y, vx, vy, ca, dn, boost, sleep, sleep0, shield = st[g]
        if ca is None or ca > t: continue
        cx_, cy_ = frame_at(ca)[0][g][:2]
        cellc = DSRC.get(cell_of(cx_, cy_), 0)
        if t >= T_REC0 and fr_ < cellc + 0.2:                  # freed
            u = min(1.0, (t - (T_REC0 + REC_D * (1 - math.sqrt(max(0, (cellc + 0.2 + 1.5) / (F_PEAK + 1.5)))))) / 0.3) if F_PEAK > 0 else 1
            k = 0.6 + 0.4 * max(0, min(1, u)) + 0.12 * math.sin(max(0, min(1, u)) * math.pi)
            bi = box_img(g, k); img.alpha_composite(bi, (int(cx_ - bi.width / 2), int(cy_ - bi.height / 2)))
            if t >= T_CARD - 0.4: pass
            continue
        u = (t - ca) / 0.45
        if u < 1:
            bi = box_img(g, 1 - 0.55 * u, dark=min(1, u * 1.2)); img.alpha_composite(bi, (int(cx_ - bi.width / 2), int(cy_ - bi.height / 2)))
    for g in live_draw:
        x, y, vx, vy, ca, dn, boost, sleep, sleep0, shield = st[g]
        boosted = t - boost < SPEED_T; asleep = t < sleep
        if boosted: layer(img, lambda dd, x=x, y=y: dd.rectangle([x - HS - 8, y - HS - 8, x + HS + 8, y + HS + 8], outline=(255, 170, 50, 200), width=5))
        bi = BOXI[g] if not asleep else box_img(g, dark=0.45)
        img.alpha_composite(bi, (int(x - HS), int(y - HS)))
        if shield: layer(img, lambda dd, x=x, y=y: (dd.ellipse([x - 46, y - 46, x + 46, y + 46], fill=(110, 230, 90, 40), outline=(150, 255, 120, 230), width=5), dd.arc([x - 34, y - 36, x - 8, y - 10], 190, 260, fill=(230, 255, 220, 230), width=4)))
        if asleep:
            u = t - sleep0
            text_layer(img, [(x + 24 + 16 * kz, y - 50 - ((u * 1.4 + kz * 0.33) % 1) * 40 - kz * 12, 'Z', 26 + 8 * kz, (225, 205, 255), 5, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
    # pickup bursts / sleep wave / block flashes
    for e in EV:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.5:
            px_, py_ = frame_at(e[0])[0][e[2]][:2]; u = (t - e[0]) / 0.5; col = POWER[e[3]][1]
            layer(img, lambda dd, px_=px_, py_=py_, u=u, col=col: [dd.rectangle([px_ + (20 + 90 * u) * math.cos(q * 0.785) - 6, py_ + (20 + 90 * u) * math.sin(q * 0.785) - 6, px_ + (20 + 90 * u) * math.cos(q * 0.785) + 6, py_ + (20 + 90 * u) * math.sin(q * 0.785) + 6], fill=col + (int(255 * (1 - u)),)) for q in range(8)])
        if e[1] == 'sleepwave' and 0 <= t - e[0] < 0.7:
            px_, py_ = frame_at(e[0])[0][e[2]][:2]; u = (t - e[0]) / 0.7
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.ellipse([px_ - r_, py_ - r_, px_ + r_, py_ + r_], outline=(190, 120, 255, int(230 * (1 - u))), width=10) for r_ in (40 + 1100 * u, 10 + 800 * u)])
    # dragon on its treasure at the exit; rears up and breathes fire down the corridor at the shadow
    k = 0 if t < T_FIRE else min(len(DRG) - 1, int((t - T_FIRE) * FIRE_FPS))
    if t < T_FIRE: k = int(t * 2) % 2
    dfr = DRG[k]; dx0 = OX + 16 * C - dfr.width - 6; dy0 = OY + 9 * C + 50 - dfr.height
    img.alpha_composite(dfr, (dx0, dy0))
    if T_FIRE + 0.2 <= t < T_FIRE + 1.1:                      # fire stream from the mouth down the corridor, splashing on the far wall
        def flames(dd):
            rs = random.Random(int(t * 30))
            for q in range(40):
                age = (q / 40) * 0.5 + ((t * 7 + q * 0.37) % 1) * 0.05
                x_ = dx0 + 30 - 900 * age; y_ = dy0 + 52 + rs.uniform(-1, 1) * (8 + 60 * age)
                x_ = max(x_, OX + 10 * C + 10 + rs.uniform(0, 30))
                rr = 10 + 26 * age; col = (255, 240, 160) if age < 0.12 else (255, 170, 50) if age < 0.3 else (230, 80, 30)
                dd.ellipse([x_ - rr, y_ - rr, x_ + rr, y_ + rr], fill=col + (int(230 * (1 - age * 1.4)),))
        layer(img, flames)
    if T_FIRE + 0.2 <= t < T_REC0 + REC_D:                    # the fire's glow sweeps back along the corridor
        u = (t - T_FIRE - 0.2) / (T_REC0 + REC_D - T_FIRE - 0.2)
        layer(img, lambda dd, u=u: dd.rectangle([OX, OY, OX + COLS * C, OY + ROWS * C], fill=(255, 150, 40, int(70 * math.sin(u * math.pi)))))
    # stamps (one at a time, dark plate)
    for st0, en, it in SCHED:
        if st0 <= t < en:
            kind, g, text, col = it; u = t - st0; al = int(255 * min(1, (en - t) / 0.2))
            fs_ = min(60, int(880 / len(text))); sc = 1 + 0.2 * max(0, 1 - u / 0.12); fs2 = int(fs_ * sc)
            tw_ = len(text) * fs2; yy = OY + int(1.1 * C)
            layer(img, lambda dd, tw_=tw_, fs2=fs2, al=al, yy=yy: dd.rounded_rectangle([540 - tw_ / 2 - 22, yy - 18, 540 + tw_ / 2 + 22, yy + fs2 + 18], 16, fill=(14, 8, 22, int(225 * al / 255))))
            text_layer(img, [(540, yy, text, fs2, col, 8, al)])
    # countdown
    if t < T_GO + 0.5:
        n = 3 - int(t / 0.4); txt = str(n) if t < T_GO else 'GO!'
        u = (t % 0.4) / 0.4 if t < T_GO else (t - T_GO) / 0.5
        fs = int((190 if t < T_GO else 150) * (1.2 - 0.2 * min(1, u * 3)))
        text_layer(img, [(540, OY + 7 * C, txt, fs, (255, 214, 60) if t < T_GO else (120, 230, 90), 12, int(255 * (1 if t < T_GO else max(0, 1 - u))))])
    roster(img, t)
    # winner reveal: Syeda's victory pose replaces Cyrus's box
    if t >= T_CARD:
        u = t - T_CARD; a_ = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([OX - 14, OY - 14, OX + COLS * C + 14, OY + ROWS * C + 14], fill=(8, 6, 16, int(170 * a_))))
        vf = VIC_W[int(u * 8) % len(VIC_W)]; sc = min(1, 0.6 + u / 0.25 * 0.4) if u < 0.25 else 1
        vf2 = vf if sc >= 1 else vf.resize((int(vf.width * sc), int(vf.height * sc)), Image.NEAREST)
        img.alpha_composite(vf2, (int(540 - vf2.width / 2), int(OY + 12.4 * C - vf2.height * (78 / 92))))
        text_layer(img, [(540, OY + int(1.4 * C), NAME[WANT] + ' WINS!', 84, COL[WANT], 10, int(255 * a_))])
    img.alpha_composite(HOOK_END if t >= T_CARD else HOOK)
    if STILLS: img.convert('RGB').save(f'st_{t:.2f}.png')
    else: wr.write(img)
if wr: wr.close()
if STILLS: sys.exit()
out_ev = [(0.0, 'tick_8bit'), (0.4, 'tick_8bit'), (0.8, 'tick_8bit'), (T_GO, 'go_8bit'), (T_GO, 'whoosh_8bit')]
last = -9
for th, v in HITS:
    if v > 160 and th - last > 0.25 and th < T_WIN + 1: out_ev.append((round(th, 3), 'tick_8bit')); last = th
PS = {'mush': 'powerup_8bit', 'acv': 'twinkle', 'mel': 'poof'}
for e in EV:
    if e[1] == 'pick': out_ev.append((round(e[0], 3), PS[e[3]]))
    elif e[1] == 'block': out_ev.append((round(e[0], 3), 'boing'))
    elif e[1] == 'caught': out_ev.append((round(e[0], 3), 'squish')); out_ev.append((round(e[0] + 0.05, 3), 'buzz_8bit'))
out_ev += [(round(T_WIN, 3), 'ding_8bit'), (round(T_FIRE, 3), 'whoosh_8bit'), (round(T_FIRE + 0.2, 3), 'boom'), (round(T_REC0 + 0.6, 3), 'twinkle'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(e for e in out_ev if e[0] < T_LOOP - 0.1)
json.dump({'events': out_ev, 'end': T_LOOP, 'beats': {'win': T_WIN, 'fire': T_FIRE, 'recede': T_REC0, 'card': T_CARD, 'loop': T_LOOP}}, open('n03_events.json', 'w'), indent=1)
print('done', round(T_LOOP, 2), NF)
