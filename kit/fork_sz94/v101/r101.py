import numpy as np, math, random, subprocess, json, os, sys, glob
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; OUTD = SP + 'fork_sz94/v101/'
os.chdir(SP + 'pixellab/maze')
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['WHO ESCAPES', 'THE LAVA?'], accent=1, color=(255, 140, 40)); print('hook bottom', HB)
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'; A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
C = 52                                   # cell size (was 64; must be a multiple of 4 for the sim's fine grid) so the 15-col board fits x88-868; sim speeds scale with C/64
KC = C / 64
MAP = [
    "###############",
    "#.............#",
    "#....o...o....#",
    "#.............#",
    "###########...#",
    "#.............#",
    "#..o...#...o..#",
    "#.............#",
    "#...###########",
    "#.............#",
    "#....o...o....#",
    "#.............#",
    "###########...#",
    "#.............#",
    "#..o...#...o..#",
    "#.............#",
    "#...###########",
    "#...########EE#",
    "#.............#",
    "#....o...o....#",
    "#.............#",
    "###############"]
ROWS, COLS = len(MAP), len(MAP[0])
OX = 88; WIN_Y0, WIN_Y1 = HB + 100, 1496; BOARD_Y0 = WIN_Y0 + 56; PADT = 140
CAM_MAX = BOARD_Y0 + ROWS * C - WIN_Y1 + 8
def is_wall(r, c): return MAP[r][c] in '#o'
# ---------------- textures
wm = json.load(open('../../fork_b10/volc_meta.json')); wsh = Image.open('../../fork_b10/volc_sheet.png').convert('RGBA')
def tile(sh, b, s=2): return sh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32)).resize((C, C), Image.NEAREST)
TILES = wm['tileset_data']['tiles']
FLOOR = tile(wsh, TILES[0]['bounding_box']); TOP = tile(wsh, TILES[6]['bounding_box'])
BRICK = tile(wsh, TILES[12]['bounding_box'])          # obsidian cliff face over floor
sm = json.load(open('../../fork_b10/lava_meta.json')); ssh = Image.open('../../fork_b10/lava_sheet.png').convert('RGBA')
SLIME = tile(ssh, sm['tileset_data']['tiles'][6]['bounding_box'])
RIM = (120, 60, 40, 255); RIM2 = (70, 40, 30, 255)
board = Image.new('RGBA', (COLS * C, ROWS * C), (0, 0, 0, 255))
bd = ImageDraw.Draw(board)
for r in range(ROWS):
    for c in range(COLS):
        x, y = c * C, r * C
        if not is_wall(r, c) and MAP[r][c] != 'E':
            t = FLOOR
            if (r + c) % 2: t = t.transpose(Image.FLIP_LEFT_RIGHT)
            if r % 2: t = t.transpose(Image.FLIP_TOP_BOTTOM)
            board.alpha_composite(t, (x, y))
for r in range(ROWS):
    for c in range(COLS):
        if not is_wall(r, c) and MAP[r][c] != 'E': continue
        x, y = c * C, r * C
        board.alpha_composite(TOP, (x, y))
        south_open = r + 1 < ROWS and not is_wall(r + 1, c) and MAP[r + 1][c] != 'E'
        if south_open:
            FH = int(46 * KC); face = BRICK.crop((0, 0, C, FH)); board.alpha_composite(face, (x, y + C - FH))
            bd.rectangle([x, y + C - FH - 4, x + C - 1, y + C - FH], fill=RIM)
        def open_(rr, cc): return 0 <= rr < ROWS and 0 <= cc < COLS and not is_wall(rr, cc) and MAP[rr][cc] != 'E'
        top = y; bot = y + C - (int(46 * KC) if south_open else 0)
        if open_(r - 1, c): bd.rectangle([x, y, x + C - 1, y + 5], fill=RIM)
        if open_(r, c - 1): bd.rectangle([x, top, x + 5, bot - 1], fill=RIM)
        if open_(r, c + 1): bd.rectangle([x + C - 6, top, x + C - 1, bot - 1], fill=RIM)
# exit door (PixelLab) set into the wall at the end of the last corridor
DOOR = Image.open('../../fork_b10/portal/00.png').convert('RGBA'); DOOR = DOOR.crop(DOOR.getbbox())
k = (2 * C) / DOOR.height; DOOR = DOOR.resize((int(DOOR.width * k), 2 * C), Image.NEAREST)
er = [r for r in range(ROWS) if 'E' in MAP[r]]; ec = [c for c in range(COLS) if 'E' in MAP[er[0]]]
ec = [c for c, ch in enumerate(MAP[er[0]]) if ch == 'E']
DOOR_XY = (ec[0] * C + C - DOOR.width // 2, (er[0] - 1) * C + 20)
board.alpha_composite(DOOR, DOOR_XY)
# torches (PixelLab, animated flame) on wall rows
TORCH = [f.resize((int(f.width * 2 * KC), int(f.height * 2 * KC)), Image.NEAREST) for f in [Image.open(p).convert('RGBA') for p in sorted(glob.glob('torch_anim/*.png'))]]
TORCH_POS = [(4, 4), (4, 9), (8, 7), (8, 12), (12, 4), (12, 9), (16, 7), (16, 11)]
# ---------------- graph: exit flows (to door) and slime spread (from start)
FINE = 4; FC = C // FINE
def passable(r, c): return 0 <= r < ROWS and 0 <= c < COLS and (not is_wall(r, c))
def bfs(starts):
    d = np.full((ROWS * FINE, COLS * FINE), np.inf); q = deque()
    for (fr, fc) in starts: d[fr, fc] = 0; q.append((fr, fc))
    while q:
        fr, fc = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = fr + dr, fc + dc
            if 0 <= nr < ROWS * FINE and 0 <= nc < COLS * FINE and passable(nr // FINE, nc // FINE) and d[nr, nc] == np.inf:
                d[nr, nc] = d[fr, fc] + 1; q.append((nr, nc))
    return d
exit_cells = [(r * FINE + i, c * FINE + j) for r in er for c in ec for i in range(FINE) for j in range(FINE) if r == er[0]]
DEX = bfs(exit_cells)
start_cells = [(r * FINE + i, 1 * FINE + j) for r in (1, 2, 3) for i in range(FINE) for j in range(FINE)]
import heapq
def dijk(starts):
    d = np.full((ROWS * FINE, COLS * FINE), np.inf); h = []
    for p in starts: d[p] = 0; heapq.heappush(h, (0.0, p))
    while h:
        dist, (fr, fc) = heapq.heappop(h)
        if dist > d[fr, fc]: continue
        for dr, dc, w in ((1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,1.414),(1,-1,1.414),(-1,1,1.414),(-1,-1,1.414)):
            nr, nc = fr + dr, fc + dc
            if 0 <= nr < ROWS * FINE and 0 <= nc < COLS * FINE and passable(nr // FINE, nc // FINE):
                if dr and dc and not (passable((fr + dr) // FINE, fc // FINE) and passable(fr // FINE, (fc + dc) // FINE)): continue
                nd = dist + w
                if nd < d[nr, nc]: d[nr, nc] = nd; heapq.heappush(h, (nd, (nr, nc)))
    return d
DSL = dijk(start_cells)
GY, GX = np.gradient(np.where(np.isinf(DEX), 9999, DEX))

# ---------------- racers (the guides themselves, PixelLab animations from Syeda's sprites)
NAMES = ['joy', 'cyrus', 'cleo', 'ray']   # Hollow racer removed (Hollow rule)
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (120, 110, 150)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
SS = 2; FOOT = 78 * SS
def seq(d, lo=1, hi=9):
    fr = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(d + '/*.png'))][lo:hi]
    return [f.resize((f.width * SS, f.height * SS), Image.NEAREST) for f in fr]
SRUN = {g: seq(f'../race/{g}_run') for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq('anim/hollow_srun')
FRUN = {g: seq(f'anim/{g}_frun') for g in NAMES}
PANIC = {g: seq(f'anim/{g}_panic') for g in NAMES}
SLIDE = {g: seq(f'anim/{g}_slide', 1, 8) for g in NAMES}
STAND = {g: seq(f'anim/{g}_frun', 0, 1)[0] for g in NAMES}
def flip(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
SRUNL = {g: [flip(f) for f in v] for g, v in SRUN.items()}; SLIDEL = {g: [flip(f) for f in v] for g, v in SLIDE.items()}
R = 22 * KC                              # feet collision radius
def face(name, rad):
    im = Image.open('../../syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 34) for n in NAMES}
GUM = Image.open('../gummies/pick_mush.png').convert('RGBA'); GUM = GUM.resize((GUM.width * 3, GUM.height * 3), Image.NEAREST)
GUM_CELL = tuple(int(v) for v in os.environ.get("GC", "6,9").split(",")); GUM_XY = (GUM_CELL[1] * C + C / 2, GUM_CELL[0] * C + C / 2 + 10 * KC)
BOOST_T, BOOST_K = float(os.environ.get("BT", "4.0")), float(os.environ.get("BK", "1.8"))
def cell_of(x, y): return int(y // FC), int(x // FC)
def wall_at(x, y, ghost=False):
    r, c = int(y // C), int(x // C)
    if ghost and 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] == 'o': return False
    return not passable(r, c)
def pillar_at(x, y):
    r, c = int(y // C), int(x // C)
    return 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] == 'o'
SL = 0.5
T_START, T_SLIME = 2.4, 3.6
SA, SB = float(os.environ.get('SA', '6.0')), float(os.environ.get('SB', '0.45'))
T_ERUPT, ERUPT_K = 9.0, float(os.environ.get('EK', '7'))
def prog(s):
    fr, fc = cell_of(s['x'], s['y']); return DEX[fr, fc]
def sim(seed, dur=30.0):
    rnd = random.Random(seed)
    racers = {}; slots = list(range(len(NAMES))); rnd.shuffle(slots)
    for i, n in enumerate(NAMES):
        racers[n] = dict(x=2.4 * C + slots[i] * 2.6 * C, y=2.0 * C + rnd.uniform(0, 1.2) * C, vx=0.0, vy=0.0, base=rnd.uniform(240, 285) * KC,
                         ph=rnd.uniform(0, 6.28), caught=None, out=None, mode='side', slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, behind=None, dist=0.0)
    gum_taken = None; frames = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        front = 0 if t < T_SLIME else (t - T_SLIME) * (SA + SB * (t - T_SLIME)) + ERUPT_K * min(1, max(0, (t - T_ERUPT) / 1.2))
        for n, s in racers.items():
            if s['caught'] is not None or s['out'] is not None or t < T_START: continue
            sliding = t - s['slide'] < SL or (s['slide'] > 0 and pillar_at(s['x'], s['y']))
            sp = s['base'] * (1 + 0.30 * math.sin(0.9 * t + s['ph']) + 0.16 * math.sin(2.3 * t + 2 * s['ph']))
            if s['boost'] is not None and t - s['boost'] < BOOST_T: sp *= BOOST_K
            if sliding:
                # locked straight-line slide, passes through guides and pillars
                sp *= 1.2; s['vx'] += (s['sdx'] * sp - s['vx']) * 0.3; s['vy'] += (s['sdy'] * sp - s['vy']) * 0.3
            else:
                fr, fc = cell_of(s['x'], s['y'])
                gx, gy = -GX[fr, fc], -GY[fr, fc]; L = math.hypot(gx, gy) or 1
                wob = 0.45 * math.sin(3.7 * t + s['ph'] * 3)
                dx, dy = gx / L, gy / L
                tx, ty = dx - dy * wob, dy + dx * wob
                s['vx'] += (tx * sp - s['vx']) * 0.12; s['vy'] += (ty * sp - s['vy']) * 0.12
            v = math.hypot(s['vx'], s['vy']) or 1
            # pillar dead ahead -> slide through it
            if not sliding and t - s['slide'] > 1.0 and t > T_START + 0.8:
                ux, uy = s['vx'] / v, s['vy'] / v
                if any(pillar_at(s['x'] + ux * d, s['y'] + uy * d) for d in (R + 10 * KC, R + 26 * KC)):
                    s['slide'] = t; s['sdx'], s['sdy'] = ux, uy; sliding = True
            nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
            for _ in range(2):
                for ax, ay in ((R, 0), (-R, 0), (0, R), (0, -R), (R * .7, R * .7), (-R * .7, R * .7), (R * .7, -R * .7), (-R * .7, -R * .7)):
                    if wall_at(nx + ax, ny + ay, sliding):
                        if ax: nx -= ax * 0.18; s['vx'] *= -0.4
                        if ay: ny -= ay * 0.18; s['vy'] *= -0.4
            s['dist'] += math.hypot(nx - s['x'], ny - s['y'])
            s['x'], s['y'] = nx, ny
            for m, o in racers.items():
                if m == n or o['caught'] is not None or o['out'] is not None: continue
                if sliding or t - o['slide'] < SL: continue          # no collision while sliding
                ddx, ddy = (s['x'] - o['x']) / 1.0, (s['y'] - o['y']) * 1.6; dd = math.hypot(ddx, ddy)
                if 0 < dd < 2 * R + 8 * KC:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and t - s['slide'] > 1.0 and t > T_START + 0.8:
                        v2 = math.hypot(s['vx'], s['vy']) or 1
                        s['slide'] = t; s['sdx'], s['sdy'] = s['vx'] / v2, s['vy'] / v2; sliding = True; continue
                    push = (2 * R + 8 * KC - dd) / 2; s['x'] += ddx / dd * push * 0.8; s['y'] += ddy / dd * push * 0.5
            v = math.hypot(s['vx'], s['vy']) or 1
            s['mode'] = 'down' if s['vy'] > 0.72 * v else 'side'
            s['sliding'] = sliding
            if gum_taken is None and math.hypot(s['x'] - GUM_XY[0], s['y'] - GUM_XY[1]) < 46 * KC:
                gum_taken = (n, t); s['boost'] = t
                s['behind'] = sum(1 for m, o in racers.items() if m != n and o['caught'] is None and prog(o) < prog(s))
            fr, fc = cell_of(s['x'], s['y'])
            if int(s['y'] // C) == er[0] and int(s['x'] // C) in ec: s['out'] = t
            elif DSL[fr, fc] < front - 1.5: s['caught'] = t
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], caught=s['caught'] is not None and s['caught'] <= t, ct=s['caught'],
                               out=s['out'] is not None and s['out'] <= t, mode=s['mode'], slide=s['slide'], sliding=s['sliding'], boost=s['boost'], dist=s['dist']) for n, s in racers.items()}, front, gum_taken))
        if any(s['out'] is not None for s in racers.values()) and all(s['out'] is not None or s['caught'] is not None for s in racers.values()):
            break
    return racers, frames, gum_taken
def score(seed):
    rc, fr, gt = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in rc.values() if s['caught'] is not None)
    if len(outs) != 1 or len(caught) != 3 or gt is None: return None
    tw, win = outs[0]
    if not (16 < tw < 22): return None
    if max(caught) < tw - 2.5 or min(caught) < 7: return None
    if gt[0] != win or rc[win]['behind'] < 2: return None
    if os.environ.get('WANT') and win != os.environ['WANT']: return None          # comeback powered by the gummy
    return round(tw, 2), win, round(gt[1], 1), rc[win]['behind'], [round(c, 1) for c in caught]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for seed in range(lo, hi):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
rc, FR, GT = sim(SEED)
win = [n for n, s in rc.items() if s['out'] is not None][0]; T_OUT = rc[win]['out']
print('winner', win, round(T_OUT, 2), 'gum', GT, {n: (round(s['caught'], 1) if s['caught'] else None) for n, s in rc.items()})
BG = Image.new('RGBA', (W, H), (12, 10, 18, 255))
for y in range(0, H, C):
    for x in range(0, W, C): BG.alpha_composite(BRICK if (y // C) % 3 else TOP, (x, y))
BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (30, 8, 4, 165)))
_g = np.zeros((H, W, 4), np.uint8); _g[..., 0] = 255; _g[..., 1] = 90; _g[..., 3] = (np.clip((np.arange(H) - 1200) / 720, 0, 1) * 90).astype(np.uint8)[:, None]
BG = Image.alpha_composite(BG, Image.fromarray(_g, 'RGBA'))
MSL = Image.open(sorted(glob.glob('../../fork_b10/mslime/*.png'))[4]).convert('RGBA'); MSL = MSL.crop(MSL.getbbox()); MSL = MSL.resize((MSL.width * 2, MSL.height * 2), Image.NEAREST)
MSPOTS = [(4, 2), (8, 9), (12, 2), (16, 8), (0, 6), (0, 11)]
VIC = {'joy': 'vic_Victory_Pose.gif', 'cyrus': 'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', 'cleo': 'vic_victoryPose.gif', 'ray': 'vic_victoryPose_1.gif', 'hollow': 'hollow-victory.gif'}
def gif(p, h):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
VICF = gif(VIC[win], 330)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
# slime texture tile big enough for the board, scrolled per frame
STEX = Image.new('RGBA', (COLS * C + 2 * C, ROWS * C + 2 * C))
for yy in range(0, STEX.height, C):
    for xx in range(0, STEX.width, C): STEX.alpha_composite(SLIME, (xx, yy))
ISLE = None
def stuck(spr, t_in, t, tex_off):
    """lava cools under the guide: they stand safe on a cooled stone island, waving for help, little steam puffs"""
    k = min(1, (t - t_in) / 0.35)
    out = Image.new('RGBA', spr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(out)
    cx = spr.width // 2; rx, ry = int(40 + 18 * k), int(16 + 7 * k)
    d.ellipse([cx - rx - 4, FOOT - ry - 2, cx + rx + 4, FOOT + ry + 6], fill=(255, 200, 90, 255))
    d.ellipse([cx - rx, FOOT - ry, cx + rx, FOOT + ry + 2], fill=(92, 86, 92, 255))
    d.ellipse([cx - rx + 8, FOOT - ry + 2, cx + rx - 14, FOOT + ry - 6], fill=(128, 122, 128, 255))
    out.alpha_composite(spr)
    for q in range(3):
        u = ((t - t_in) * 0.9 + q / 3) % 1
        sx = cx + (q - 1) * 34 + 6 * math.sin(t * 3 + q); sy = FOOT - 20 - u * 90; a = int(170 * (1 - u))
        d2 = ImageDraw.Draw(out)
        d2.ellipse([sx - 10 - u * 8, sy - 8 - u * 6, sx + 10 + u * 8, sy + 8 + u * 6], fill=(235, 235, 240, a))
    return out
def stuck_old(spr, t_in, t, tex_off):
    """sprite sunk waist-deep in a slime mound"""
    k = min(1, (t - t_in) / 0.35)
    cut = int(FOOT - 30 - 28 * k)                         # sinks from knees to waist
    s2 = spr.copy(); a = s2.getchannel('A'); ImageDraw.Draw(a).rectangle([0, cut, s2.width, s2.height], fill=0); s2.putalpha(a)
    cx = spr.width // 2; box = [cx - 54, cut - 16, cx + 54, cut + 30]
    mound = Image.new('L', spr.size, 0); ImageDraw.Draw(mound).ellipse(box, fill=255)
    tex = STEX.crop((tex_off[0], tex_off[1], tex_off[0] + spr.width, tex_off[1] + spr.height))
    out = Image.new('RGBA', spr.size, (0, 0, 0, 0))
    out.paste(tex, (0, 0), mound)
    rim = Image.new('L', spr.size, 0); ImageDraw.Draw(rim).ellipse(box, outline=255, width=4)
    out.paste(Image.new('RGBA', spr.size, (190, 255, 130, 255)), (0, 0), rim)
    out.alpha_composite(s2)
    lip = Image.new('L', spr.size, 0); ImageDraw.Draw(lip).arc([cx - 30, cut - 8, cx + 30, cut + 12], 0, 180, fill=255, width=5)
    out.paste(Image.new('RGBA', spr.size, (120, 230, 80, 255)), (0, 0), lip)
    drip = ImageDraw.Draw(out)
    for q in range(3):
        dx = (q - 1) * 18; dy = int(6 + 6 * math.sin(t * 6 + q))
        drip.rectangle([cx + dx - 3, cut - 2, cx + dx + 3, cut + dy], fill=(120, 230, 80, 255))
    return out
END = T_OUT + 3.0
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + 'noaudio.mp4'], stdin=subprocess.PIPE)
events = []; caught_seen = set(); slides_seen = set(); ghosts = {n: [] for n in NAMES}
NF = int(END * FPS); F16 = F(30); cam = 0.0
for f in range(NF):
    t = f / FPS; st, front, gt = FR[min(f, len(FR) - 1)]
    b = board.copy()
    off = int(t * 18) % C
    if front > 0:
        mi = Image.fromarray((DSL < front).astype(np.uint8) * 255, 'L').resize((COLS * C, ROWS * C), Image.NEAREST)
        tex = STEX.crop((C - off // 2, C - off, C - off // 2 + COLS * C, C - off + ROWS * C))
        edge = Image.fromarray(((DSL < front) & (DSL > front - 2.2)).astype(np.uint8) * 255, 'L').resize(mi.size, Image.NEAREST)
        b.paste(tex, (0, 0), mi)
        b.paste(Image.new('RGBA', mi.size, (255, 236, 140, 255)), (0, 0), edge.point(lambda p: p // 2))
        for r in range(ROWS):
            for c in range(COLS):
                if is_wall(r, c) or MAP[r][c] == 'E':
                    b.alpha_composite(board.crop((c * C, r * C, c * C + C, r * C + C)), (c * C, r * C))
    for (r, c) in TORCH_POS:
        fr_ = TORCH[(int(t * 10) + r + c) % len(TORCH)]; b.alpha_composite(fr_, (c * C + C // 2 - fr_.width // 2, r * C + C - fr_.height - 20))
    big = Image.new('RGBA', (COLS * C, ROWS * C + PADT), (0, 0, 0, 0)); big.alpha_composite(b, (0, PADT)); b = big
    bd2 = ImageDraw.Draw(b)
    # mushroom gummy pickup
    if gt is None or t < gt[1]:
        bob = int(6 * math.sin(t * 4)); gx_, gy_ = GUM_XY[0], GUM_XY[1] + PADT
        for rr, al in ((46, 40), (34, 70), (24, 90)):
            bd2.ellipse([gx_ - rr, gy_ - rr + bob - 10, gx_ + rr, gy_ + rr + bob - 10], fill=(255, 200, 120, al))
        bd2.ellipse([gx_ - 26, gy_ + 18, gx_ + 26, gy_ + 28], fill=(0, 0, 0, 90))
        b.alpha_composite(GUM, (int(gx_ - GUM.width / 2), int(gy_ - GUM.height / 2 + bob - 10)))
        for k in range(3):
            a = t * 2.5 + k * 2.09; sx, sy = gx_ + 40 * math.cos(a), gy_ - 10 + 30 * math.sin(a) + bob
            bd2.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 245, 190, 230))
    elif t - gt[1] < 0.6:
        u = (t - gt[1]) / 0.6; gx_, gy_ = GUM_XY[0], GUM_XY[1] + PADT
        for k in range(10):
            a = k * 0.628; rr = 20 + 90 * u; sx, sy = gx_ + rr * math.cos(a), gy_ - 20 + rr * math.sin(a)
            bd2.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 220, 120, int(255 * (1 - u))))
        if not any(e[1] == 'powerup_8bit' for e in events): events.append((round(gt[1], 3), 'powerup_8bit'))
    # characters, y-sorted by feet
    order = sorted([n for n in NAMES if not st[n]['out']], key=lambda n: st[n]['y'])
    for n in order:
        s = st[n]; x, y = s['x'], s['y'] + PADT
        boosted = s['boost'] is not None and 0 <= t - s['boost'] < BOOST_T
        if s['caught']:
            spr = PANIC[n][int(t * 12) % 8]
            spr = stuck(spr, s['ct'], t, (int(x) % C, int(y) % C))
            if n not in caught_seen: caught_seen.add(n); events.append((round(t, 3), 'poof'))
        elif t < T_START:
            spr = STAND[n]
        elif s['sliding']:
            k = min(6, int((t - s['slide']) / SL * 7)); spr = (SLIDEL if s['vx'] < 0 else SLIDE)[n][k]
            if (n, s['slide']) not in slides_seen: slides_seen.add((n, s['slide'])); events.append((round(t, 3), 'jump'))
            for q in range(3):
                dxp = -math.copysign(1, s['vx']) * (20 + q * 22 + (t - s['slide']) * 60); a = int(180 * max(0, 1 - (t - s['slide']) / SL))
                bd2.ellipse([x + dxp - 12 - q * 3, y - 14 - q * 4, x + dxp + 12 + q * 3, y + 6], fill=(200, 190, 170, max(0, a - q * 40)))
        else:
            ph = int(s['dist'] / 22) % 8
            if s['mode'] == 'down': spr = FRUN[n][ph]
            else: spr = (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        # boost: amber afterimages and sparkles
        if boosted and not s['caught']:
            ghosts[n] = (ghosts[n] + [(spr, x, y)])[-5:]
            for i, (gs, gx2, gy2) in enumerate(ghosts[n][:-1]):
                gimg = gs.copy(); al = gimg.getchannel('A').point(lambda p, i=i: int(p * (0.12 + 0.08 * i)))
                tint = Image.new('RGBA', gimg.size, (255, 180, 60, 255)); tint.putalpha(al)
                b.alpha_composite(tint, (int(gx2 - gimg.width / 2), int(gy2 - FOOT)))
        else: ghosts[n] = []
        if not s['caught']: bd2.ellipse([x - 26, y - 8, x + 26, y + 8], fill=(0, 0, 0, 80))
        b.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if boosted and not s['caught']:
            for k in range(4):
                a = t * 9 + k * 1.57; sx, sy = x + 34 * math.cos(a), y - 70 + 50 * math.sin(a * 1.3)
                bd2.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 230, 140, 230))
            u = t - s['boost']
            if u < 1.4:
                for q in range(4):     # SPEED: dust trail + speed lines behind
                    du = (t * 6 + q * 0.25) % 1.0; ddx = -math.copysign(1, s['vx'] or 1) * (24 + du * 50)
                    bd2.ellipse([x + ddx - 10 - du * 8, y - 12 - du * 6, x + ddx + 10 + du * 8, y + 4], fill=(230, 200, 150, int(170 * (1 - du))))
                    bd2.line([x + ddx - 30, y - 40 - q * 22, x + ddx - 80, y - 40 - q * 22], fill=(255, 220, 140, 200), width=4)
                al = int(255 * min(1, (1.4 - u) / 0.4)); txt = 'SPEED!'
                tw = bd2.textlength(txt, font=F16); ty_ = y - FOOT - 10 - u * 40
                bd2.text((x - tw / 2, ty_), txt, font=F16, fill=(255, 200, 70, al), stroke_width=5, stroke_fill=(40, 20, 10, al))
    # magma slime spectators bouncing on the obsidian walls
    for k_, (r_, c_) in enumerate(MSPOTS):
        ms = MSL; hop = int(abs(math.sin(t * 5 + k_)) * 14)
        b.alpha_composite(ms, (c_ * C + C // 2 - ms.width // 2, PADT + r_ * C + C - ms.height - 8 - hop))
    shx = shy = 0
    if T_ERUPT <= t < T_ERUPT + 1.3:
        amp = 14 * (1 - (t - T_ERUPT) / 1.3); shx = int(amp * math.sin(t * 90)); shy = int(amp * math.cos(t * 77))
        if not any(e[1] == 'boom' for e in events): events.append((T_ERUPT, 'boom'))
    alive = [st[n]['y'] for n in NAMES if not st[n]['out'] and not st[n]['caught']] or [st[n]['y'] for n in NAMES]
    tgt = max(0, min(CAM_MAX, BOARD_Y0 + sum(alive) / len(alive) - 1060)) if t >= T_START else 0
    cam += (tgt - cam) * 0.06; OY = BOARD_Y0 - int(cam)
    img = BG.copy(); img.alpha_composite(b, (OX + shx, OY - PADT + shy))
    img.paste(BG.crop((0, 0, W, WIN_Y0)), (0, 0)); img.paste(BG.crop((0, WIN_Y1, W, H)), (0, WIN_Y1))
    def embers(dd):
        rr_ = random.Random(7)
        for q in range(46):
            ex = rr_.uniform(0, W); sp_ = rr_.uniform(60, 160); ph_ = rr_.uniform(0, 30)
            ey = H - ((t * sp_ + ph_ * 60) % (H - 300)); sz = rr_.choice([3, 4, 5])
            dd.rectangle([ex + 8 * math.sin(t * 2 + q), ey, ex + sz + 8 * math.sin(t * 2 + q), ey + sz], fill=(255, rr_.randint(120, 200), 60, 200))
        if T_ERUPT - 0.2 <= t < T_ERUPT + 2.2:
            for q in range(10):
                u = (t - T_ERUPT + 0.2 - q * 0.12)
                if u < 0 or u > 1.2: continue
                rx_ = OX + 80 + (q * 197) % (COLS * C - 160); ry_ = WIN_Y0 - 40 + u * u * 900
                dd.ellipse([rx_ - 16, ry_ - 16, rx_ + 16, ry_ + 16], fill=(255, 150, 40, 255)); dd.ellipse([rx_ - 9, ry_ - 9, rx_ + 7, ry_ + 7], fill=(255, 230, 120, 255))
    L_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); embers(ImageDraw.Draw(L_)); img.alpha_composite(L_)
    if T_ERUPT <= t < T_ERUPT + 1.6:
        a_ = int(255 * min(1, (T_ERUPT + 1.6 - t) / 0.4)); L_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L_)
        w_ = dd.textlength('ERUPTION!', font=F(80)); dd.text((478 - w_ / 2, 980), 'ERUPTION!', font=F(80), fill=(255, 120, 40, a_), stroke_width=9, stroke_fill=(40, 10, 5, a_))
        img.alpha_composite(L_)
    d = ImageDraw.Draw(img)
    d.rectangle([OX - 8, WIN_Y0 - 8, OX + COLS * C + 7, WIN_Y1 + 7], outline=(30, 26, 40), width=8)
    for i, n in enumerate(NAMES):
        ix = 478 + (i - 1.5) * 180; iy = HB + 48
        ic = ICON[n]; s = st[n]
        if s['caught']: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55)
        img.alpha_composite(ic, (int(ix - ic.width / 2), int(iy - ic.height / 2)))
        d = ImageDraw.Draw(img)
        if s['caught']:
            d.line([ix - 26, iy - 26, ix + 26, iy + 26], fill=(230, 50, 50), width=9); d.line([ix - 26, iy + 26, ix + 26, iy - 26], fill=(230, 50, 50), width=9)
        if s['out']: d.ellipse([ix - 42, iy - 42, ix + 42, iy + 42], outline=(255, 214, 60), width=6)
        if s['boost'] is not None and t >= s['boost'] and not s['caught']:
            img.alpha_composite(GUM.resize((GUM.width // 2, GUM.height // 2), Image.NEAREST), (int(ix + 14), int(iy + 10)))
    d = ImageDraw.Draw(img)
    if t < T_START + 0.6: ctext(d, 478, 1010, 'PICK ONE!', F(60), (255, 255, 255), 8)
    if t >= T_OUT:
        u = t - T_OUT; a = min(1, u / 0.3)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(150 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1060 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, 478, 1090, LABEL[win] + ' ESCAPED!', F(56), (255, 214, 60), 8)
        if not any(e[1] == 'vg02' for e in events): events.append((round(t, 3), 'vg02'))
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(OUTD + f'prev/v_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump(events, open(OUTD + 'ev.json', 'w'))
print('done', round(END, 2))
