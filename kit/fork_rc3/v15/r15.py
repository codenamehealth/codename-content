import numpy as np, math, random, subprocess, json, os, sys, glob
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/maze')
OUTD = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc3/v15/'
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'; A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
C = 64                                   # cell size on screen (32px tiles at 2x)
MAP = [
    "#############",
    "##########EE#",
    "#...........#",
    "#..o...o..o.#",
    "#...........#",
    "#...#########",
    "#...........#",
    "#..o...o..o.#",
    "#...........#",
    "#########...#",
    "#...........#",
    "#..o...o..o.#",
    "#...........#",
    "#############"]
ROWS, COLS = len(MAP), len(MAP[0])
import sys as _s; _s.path.insert(0, '../safezone'); from hook import hook_layer
def hook3():
    from hook import FONT as HF, X0, X1, Y0
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    f1, f2, f3 = ImageFont.truetype(HF, 80), ImageFont.truetype(HF, 36), ImageFont.truetype(HF, 46)
    h = 26 + 80 + 26 + 36 + 22 + 18 + 46 + 26
    d.rounded_rectangle([X0, Y0, X1, Y0 + h], 22, fill=(14, 10, 24, 232), outline=(255, 214, 60), width=6)
    y = Y0 + 26
    for txt, f, col, sw, yy in (('PICK A GUIDE', f1, (255, 214, 60), 9, 80 + 26), ('BEFORE THE MAZE STARTS', f2, (190, 150, 255), 6, 36 + 22)):
        w = d.textlength(txt, font=f); d.text(((X0 + X1) / 2 - w / 2, y), txt, font=f, fill=col, stroke_width=sw, stroke_fill=(10, 6, 18)); y += yy
    d.line([(X0 + 60, y - 6), (X1 - 60, y - 6)], fill=(255, 214, 60, 120), width=3); y += 12
    txt = 'COMMENT YOUR PICK'; w = d.textlength(txt, font=f3)
    d.text(((X0 + X1) / 2 - w / 2, y), txt, font=f3, fill=(245, 245, 245), stroke_width=6, stroke_fill=(10, 6, 18))
    return L, Y0 + h
HOOK, HB = hook3()
OX = 70; OY = HB + 96
VW, VH = 816, 1500 - OY; VWW, VHW = VW * 2 // 3, (VH * 2 // 3) // 2 * 2; VH = VHW * 3 // 2   # camera window in world px, shown 1.5x (sprites 2x -> 3x)
def is_wall(r, c): return MAP[r][c] in '#o'
# ---------------- textures
FK = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork2/'
wm = json.load(open(FK + 'hedge_meta.json')); wsh = Image.open(FK + 'hedge_sheet.png').convert('RGBA')
def tile(sh, b, s=2): return sh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32)).resize((32 * s, 32 * s), Image.NEAREST)
TILES = wm['tileset_data']['tiles']
FLOOR = tile(wsh, TILES[0]['bounding_box']); TOP = tile(wsh, TILES[6]['bounding_box'])
BRICK = tile(wsh, TILES[15]['bounding_box'])          # brick face over floor
RIM = (34, 66, 38, 255); RIM2 = (20, 40, 24, 255)
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
            face = BRICK.crop((0, 0, C, 46)); board.alpha_composite(face, (x, y + C - 46))
            bd.rectangle([x, y + C - 50, x + C - 1, y + C - 46], fill=RIM)
        def open_(rr, cc): return 0 <= rr < ROWS and 0 <= cc < COLS and not is_wall(rr, cc) and MAP[rr][cc] != 'E'
        top = y; bot = y + C - (46 if south_open else 0)
        if open_(r - 1, c): bd.rectangle([x, y, x + C - 1, y + 5], fill=RIM)
        if open_(r, c - 1): bd.rectangle([x, top, x + 5, bot - 1], fill=RIM)
        if open_(r, c + 1): bd.rectangle([x + C - 6, top, x + C - 1, bot - 1], fill=RIM)
# exit door (PixelLab) set into the wall at the end of the last corridor
DOOR = Image.open(FK + 'moongate/01.png').convert('RGBA'); DOOR = DOOR.crop(DOOR.getbbox())
k = (2 * C) / DOOR.height; DOOR = DOOR.resize((int(DOOR.width * k), 2 * C), Image.NEAREST)
er = [r for r in range(ROWS) if 'E' in MAP[r]]; ec = [c for c in range(COLS) if 'E' in MAP[er[0]]]
ec = [c for c, ch in enumerate(MAP[er[0]]) if ch == 'E']
DOOR_XY = (ec[0] * C + C - DOOR.width // 2, er[0] * C + C - DOOR.height + 30)
board.alpha_composite(DOOR, DOOR_XY)
# torches (PixelLab, animated flame) on wall rows
LANT = Image.open(FK + 'lantern/09.png').convert('RGBA'); LANT = LANT.crop(LANT.getbbox()); LANT = LANT.resize((LANT.width * 2, LANT.height * 2), Image.NEAREST)
TORCH_POS = [(5, 6), (5, 10), (9, 3), (9, 7)]
SPIRIT = Image.open(FK + 'spirit/09.png').convert('RGBA'); SPIRIT = SPIRIT.crop(SPIRIT.getbbox()); SPIRIT = SPIRIT.resize((SPIRIT.width * 2, SPIRIT.height * 2), Image.NEAREST)
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
start_cells = [(r * FINE + i, 1 * FINE + j) for r in (10, 11, 12) for i in range(FINE) for j in range(FINE)]
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
NAMES = ['joy', 'cleo', 'cyrus', 'ray']
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
R = 22                                   # feet collision radius
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
GUM = Image.open('../gummies/pick_mush.png').convert('RGBA'); GUM = GUM.resize((GUM.width * 3, GUM.height * 3), Image.NEAREST)   # mushroom gummy = SPEED
GUM_CELL = tuple(int(v) for v in os.environ.get("GC", "6,9").split(",")); GUM_XY = (GUM_CELL[1] * C + C / 2, GUM_CELL[0] * C + C / 2 + 10)
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
STUN, KB = float(os.environ.get('STUN', '0.85')), float(os.environ.get('KB', '430'))   # shove: target stunned STUN s, knocked back KB px/s
T_START, T_SLIME = float(os.environ.get('TS','2.4')), float(os.environ.get('TSL','3.6'))
SA, SB = float(os.environ.get("SA", "6.0")), float(os.environ.get("SB", "0.45"))
def prog(s):
    fr, fc = cell_of(s['x'], s['y']); return DEX[fr, fc]
def sim(seed, dur=30.0):
    rnd = random.Random(seed)
    racers = {}; slots = list(range(len(NAMES))); rnd.shuffle(slots)
    for i, n in enumerate(NAMES):
        racers[n] = dict(x=2.2 * C + slots[i] * 2.4 * C, y=10.6 * C + rnd.uniform(0, 1.2) * C, vx=0.0, vy=0.0, base=rnd.uniform(240, 285) * float(os.environ.get("SPD", "1")),
                         ph=rnd.uniform(0, 6.28), caught=None, out=None, mode='side', slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, behind=None, dist=0.0, stun=-9.0, scd=-9.0)
    gum_taken = None; frames = []; shoves = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        front = 0 if t < T_SLIME else (t - T_SLIME) * (SA + SB * (t - T_SLIME))
        for n, s in racers.items():
            if s['caught'] is not None or s['out'] is not None or t < T_START: continue
            stunned = t < s['stun']
            sliding = (t - s['slide'] < SL or (s['slide'] > 0 and pillar_at(s['x'], s['y']))) and not stunned
            sp = s['base'] * (1 + 0.30 * math.sin(0.9 * t + s['ph']) + 0.16 * math.sin(2.3 * t + 2 * s['ph']))
            if s['boost'] is not None and t - s['boost'] < BOOST_T: sp *= BOOST_K
            if stunned:
                s['vx'] *= 0.86; s['vy'] *= 0.86          # knocked back, dazed: no steering
            elif sliding:
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
            if not sliding and not stunned and t - s['slide'] > 1.0 and t > T_START + 0.8:
                ux, uy = s['vx'] / v, s['vy'] / v
                if any(pillar_at(s['x'] + ux * d, s['y'] + uy * d) for d in (R + 10, R + 26)):
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
                if 0 < dd < 2 * R + 8:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and not stunned and t >= o['stun'] and t - s['scd'] > 1.2 and t > T_START + 0.6:
                        # SHOVE: bump the one in the way, they get knocked back and stunned
                        ux, uy = o['x'] - s['x'], o['y'] - s['y']; L2 = math.hypot(ux, uy) or 1
                        o['stun'] = t + STUN; o['vx'], o['vy'] = ux / L2 * KB, uy / L2 * KB
                        s['scd'] = t; s['vx'] *= 0.6; s['vy'] *= 0.6
                        shoves.append((round(t, 3), n, m, (s['x'] + o['x']) / 2, (s['y'] + o['y']) / 2)); continue
                    push = (2 * R + 8 - dd) / 2; s['x'] += ddx / dd * push * 0.8; s['y'] += ddy / dd * push * 0.5
            v = math.hypot(s['vx'], s['vy']) or 1
            s['mode'] = 'down' if s['vy'] > 0.72 * v else 'side'
            s['sliding'] = sliding
            if gum_taken is None and math.hypot(s['x'] - GUM_XY[0], s['y'] - GUM_XY[1]) < 46:
                gum_taken = (n, t); s['boost'] = t
                s['behind'] = sum(1 for m, o in racers.items() if m != n and o['caught'] is None and prog(o) < prog(s))
            fr, fc = cell_of(s['x'], s['y'])
            if int(s['y'] // C) == er[0] and int(s['x'] // C) in ec: s['out'] = t
            elif DSL[fr, fc] < front - 1.5: s['caught'] = t
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], caught=s['caught'] is not None and s['caught'] <= t, ct=s['caught'],
                               out=s['out'] is not None and s['out'] <= t, mode=s['mode'], slide=s['slide'], sliding=s['sliding'], boost=s['boost'], dist=s['dist'],
                               stun=t < s['stun'], st0=s['stun'] - STUN) for n, s in racers.items()}, front, gum_taken))
        if any(s['out'] is not None for s in racers.values()) and all(s['out'] is not None or s['caught'] is not None for s in racers.values()):
            break
    return racers, frames, gum_taken, shoves
def score(seed):
    rc, fr, gt, sv = sim(seed)
    if len(sv) < int(os.environ.get('NSH', '3')) or len(set(x[2] for x in sv)) < 2: return None
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in rc.values() if s['caught'] is not None)
    if len(outs) != 1 or len(caught) != len(NAMES) - 1 or gt is None: return None
    tw, win = outs[0]
    if not (float(os.environ.get('TLO','11')) < tw < float(os.environ.get('THI','17'))): return None
    if max(caught) < tw - 2.5 or min(caught) < float(os.environ.get('MC','6')): return None
    if os.environ.get('WIN') and win != os.environ['WIN']: return None
    if gt[0] != win or rc[win]['behind'] < int(os.environ.get('BH', '2')): return None          # comeback powered by the gummy
    return round(tw, 2), win, round(gt[1], 1), rc[win]['behind'], [round(c, 1) for c in caught], [(x[0], x[1][:2] + '>' + x[2][:2]) for x in sv]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for seed in range(lo, hi):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
rc, FR, GT, SHV = sim(SEED)
print('shoves', [(x[0], x[1], x[2]) for x in SHV])
win = [n for n, s in rc.items() if s['out'] is not None][0]; T_OUT = rc[win]['out']
print('winner', win, round(T_OUT, 2), 'gum', GT, {n: (round(s['caught'], 1) if s['caught'] else None) for n, s in rc.items()})
BG = Image.new('RGBA', (W, H), (12, 10, 18, 255))
for y in range(0, H, C):
    for x in range(0, W, C): BG.alpha_composite(BRICK if (y // C) % 3 else TOP, (x, y))
BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (8, 6, 14, 170)))
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
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=tuple(fill[:3]) + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
# slime texture tile big enough for the board, scrolled per frame
_r = np.random.default_rng(7); _w, _h = (COLS * C + 2 * C) // 8, (ROWS * C + 2 * C) // 8
_n = _r.random((_h, _w))
for _ in range(3): _n = (_n + np.roll(_n, 1, 0) + np.roll(_n, -1, 0) + np.roll(_n, 1, 1) + np.roll(_n, -1, 1)) / 5
_n = (_n - _n.min()) / (_n.max() - _n.min())
_q = np.digitize(_n, [0.35, 0.55, 0.72, 0.86])
PAL = np.array([(14, 8, 26), (24, 12, 42), (38, 20, 64), (62, 34, 98), (104, 62, 150)], np.uint8)
_rgb = PAL[_q]; _sp = _r.random((_h, _w)) > 0.985; _rgb[_sp] = (200, 170, 255)
STEX = Image.fromarray(_rgb, 'RGB').resize((_w * 8, _h * 8), Image.NEAREST).convert('RGBA')
def stuck(spr, t_in, t, tex_off):
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
    out.paste(Image.new('RGBA', spr.size, (170, 120, 255, 255)), (0, 0), rim)
    out.alpha_composite(s2)
    lip = Image.new('L', spr.size, 0); ImageDraw.Draw(lip).arc([cx - 30, cut - 8, cx + 30, cut + 12], 0, 180, fill=255, width=5)
    out.paste(Image.new('RGBA', spr.size, (120, 80, 200, 255)), (0, 0), lip)
    drip = ImageDraw.Draw(out)
    for q in range(3):
        dx = (q - 1) * 18; dy = int(6 + 6 * math.sin(t * 6 + q))
        drip.rectangle([cx + dx - 3, cut - 2, cx + dx + 3, cut + dy], fill=(60, 30, 100, 255))
    return out
mb = Image.open(A + 'bg_moon.gif'); mb.seek(0); _m = mb.convert('RGB'); _k = H / _m.height
_m = _m.resize((int(_m.width * _k), H), Image.NEAREST); _m = _m.crop(((_m.width - W) // 2, 0, (_m.width - W) // 2 + W, H))
BG = ImageEnhance.Brightness(_m).enhance(0.55).convert('RGBA')
LIGHT = Image.new('RGBA', (COLS * C, ROWS * C), (8, 10, 40, 70)); _ld = ImageDraw.Draw(LIGHT)
_glow = Image.new('RGBA', LIGHT.size, (0, 0, 0, 0)); _gd = ImageDraw.Draw(_glow)
for (r, c) in TORCH_POS + [(er[0], ec[0] + 0.5)]:
    cx_, cy_ = c * C + C / 2, r * C + C / 2
    for rr_ in range(150, 0, -15):
        _ld.ellipse([cx_ - rr_, cy_ - rr_, cx_ + rr_, cy_ + rr_], fill=(8, 10, 40, int(70 * rr_ / 150)))
        _gd.ellipse([cx_ - rr_, cy_ - rr_, cx_ + rr_, cy_ + rr_], fill=(255, 200, 110, int(6 * (150 - rr_) / 15)))
LIGHT.alpha_composite(_glow)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
fxL = [None]
def flush(bb):
    bb.alpha_composite(fxL[0]); fxL[0] = Image.new('RGBA', bb.size, (0, 0, 0, 0)); return ImageDraw.Draw(fxL[0])
HOLD = float(os.environ.get('HOLD', '1.35')); NOPEN = 6
END = T_OUT + HOLD
# ---- camera: follows the pack (alive guides + guides caught in the last 0.8s), zero-lag smoothing, clamped to the board
_tx, _ty = [], []
for _f in range(int(END * FPS)):
    _st, _, _ = FR[min(_f, len(FR) - 1)]; _t = _f / FPS
    pts = [(v['x'], v['y']) for v in _st.values() if not v['out'] and (not v['caught'] or _t - v['ct'] < 0.8)]
    if not pts: pts = [(_tx[-1] + VWW / 2, _ty[-1] + VHW / 2 + 40)] if _tx else [(COLS * C / 2, ROWS * C / 2)]
    if _f / FPS >= T_OUT - 0.2: pts = [(DOOR_XY[0] + DOOR.width / 2, DOOR_XY[1] + DOOR.height)]
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    _tx.append((min(xs) + max(xs)) / 2 - VWW / 2); _ty.append((min(ys) + max(ys)) / 2 - 40 - VHW / 2)
def _smooth(a, sig):
    a = np.array(a, float); k = np.exp(-0.5 * (np.arange(-3 * sig, 3 * sig + 1) / sig) ** 2); k /= k.sum()
    pad = np.concatenate([np.full(3 * sig, a[0]), a, np.full(3 * sig, a[-1])]); return np.convolve(pad, k, 'valid')
CAMX = np.clip(_smooth(_tx, 12), 0, COLS * C - VWW); CAMY = np.clip(_smooth(_ty, 12), 0, ROWS * C - VHW)
print('cam x', int(CAMX.min()), int(CAMX.max()), 'y', int(CAMY.min()), int(CAMY.max()), 'view', VWW, VHW, VW, VH, 'OY', OY)
STAMPS = []   # (t0, dur, kind, text, colour, icon)
for n, s_ in rc.items():
    if s_['caught'] is not None: STAMPS.append((s_['caught'], 0.75, 'out', LABEL[n] + ' OUT!', (255, 70, 70), n))
STAMPS.append((GT[1], 1.0, 'pow', 'SPEED!', (255, 160, 40), GT[0]))
STAMPS.sort()
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + 'v15_noaudio.mp4'], stdin=subprocess.PIPE)
events = []; caught_seen = set(); slides_seen = set(); ghosts = {n: [] for n in NAMES}; stun_seen = []
for (t_s, a_s, b_s, _x, _y) in SHV: events.append((round(t_s, 3), 'punch'))
def star(dd, x, y, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    dd.polygon(pts, fill=col, outline=(60, 40, 10, 255))
PREV = [int(v) for v in os.environ.get('PREV', '').split(',') if v]
NFM = int(END * FPS); NF = NFM + NOPEN; F16 = F(30)
for f in range(NF):
    OPEN = f >= NFM
    t = f / FPS if not OPEN else 0.0; st, front, gt = FR[min(f, len(FR) - 1) if not OPEN else 0]
    cx_cam, cy_cam = (int(CAMX[f]), int(CAMY[f])) if not OPEN else (int(CAMX[0]), int(CAMY[0]))
    b = board.copy()
    off = int(t * 18) % C
    if front > 0:
        mi = Image.fromarray((DSL < front).astype(np.uint8) * 255, 'L').resize((COLS * C, ROWS * C), Image.NEAREST)
        tex = STEX.crop((C - off // 2, C - off, C - off // 2 + COLS * C, C - off + ROWS * C))
        edge = Image.fromarray(((DSL < front) & (DSL > front - 2.2)).astype(np.uint8) * 255, 'L').resize(mi.size, Image.NEAREST)
        b.paste(tex, (0, 0), mi)
        b.paste(Image.new('RGBA', mi.size, (170, 110, 255, 255)), (0, 0), edge.point(lambda p: p // 2))
        for r in range(ROWS):
            for c in range(COLS):
                if is_wall(r, c) or MAP[r][c] == 'E':
                    b.alpha_composite(board.crop((c * C, r * C, c * C + C, r * C + C)), (c * C, r * C))
    for (r, c) in TORCH_POS:
        b.alpha_composite(LANT, (c * C + C // 2 - LANT.width // 2, r * C + C - LANT.height - 14))
    b.alpha_composite(LIGHT)
    if front > 0:
        ys, xs = np.nonzero(((DSL < front) & (DSL > front - 2.2)))
        if len(xs):
            order_ = np.argsort(xs * 1000 + ys)
            for k in range(3):
                j = order_[int((k + 0.5) / 3 * len(order_))]; sx_, sy_ = xs[j] * FC, ys[j] * FC
                bob_ = int(6 * math.sin(t * 5 + k * 2))
                b.alpha_composite(SPIRIT, (int(sx_ - SPIRIT.width / 2), int(sy_ - SPIRIT.height + bob_)))
    fxL[0] = Image.new('RGBA', b.size, (0, 0, 0, 0)); bd2 = ImageDraw.Draw(fxL[0]); LABELS = []
    # mushroom gummy pickup
    if gt is None or t < gt[1]:
        bob = int(6 * math.sin(t * 4)); gx_, gy_ = GUM_XY
        for rr, al in ((62, 40), (50, 70), (40, 90)):
            bd2.ellipse([gx_ - rr, gy_ - rr + bob - 10, gx_ + rr, gy_ + rr + bob - 10], fill=(255, 200, 120, al))
        bd2.ellipse([gx_ - 26, gy_ + 18, gx_ + 26, gy_ + 28], fill=(0, 0, 0, 90))
        bd2 = flush(b); b.alpha_composite(GUM, (int(gx_ - GUM.width / 2), int(gy_ - GUM.height / 2 + bob - 10)))
        for k in range(3):
            a = t * 2.5 + k * 2.09; sx, sy = gx_ + 40 * math.cos(a), gy_ - 10 + 30 * math.sin(a) + bob
            bd2.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 245, 190, 230))
    elif t - gt[1] < 0.6:
        u = (t - gt[1]) / 0.6; gx_, gy_ = GUM_XY
        for k in range(10):
            a = k * 0.628; rr = 20 + 90 * u; sx, sy = gx_ + rr * math.cos(a), gy_ - 20 + rr * math.sin(a)
            bd2.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 220, 120, int(255 * (1 - u))))
        if not any(e[1] == 'powerup_8bit' for e in events): events.append((round(gt[1], 3), 'powerup_8bit'))
    # characters, y-sorted by feet
    order = sorted([n for n in NAMES if not st[n]['out']], key=lambda n: st[n]['y'])
    for n in order:
        s = st[n]; x, y = s['x'], s['y']
        boosted = s['boost'] is not None and 0 <= t - s['boost'] < BOOST_T
        if s['caught']:
            spr = PANIC[n][int(t * 12) % 8]
            spr = stuck(spr, s['ct'], t, (int(x) % C, int(y) % C))
            if n not in caught_seen: caught_seen.add(n); events.append((round(t, 3), 'poof'))
        elif t < T_START or OPEN or f == 0:
            spr = STAND[n]
        elif s['stun']:
            spr = PANIC[n][int(t * 14) % 8]   # dazed after a shove
            if s['st0'] not in [e2[2] for e2 in stun_seen if e2[0] == n]: stun_seen.append((n, t, s['st0']))
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
                tint = Image.new('RGBA', gimg.size, (255, 160, 40, 255)); tint.putalpha(al)
                b.alpha_composite(tint, (int(gx2 - gimg.width / 2), int(gy2 - FOOT)))
        else: ghosts[n] = []
        if not s['caught']: bd2.ellipse([x - 26, y - 8, x + 26, y + 8], fill=(0, 0, 0, 80))
        if boosted and not s['caught']:
            vv = math.hypot(s['vx'], s['vy']) or 1; ux_, uy_ = s['vx'] / vv, s['vy'] / vv
            for q in range(5):   # speed lines trailing behind
                ph_ = (t * 7 + q * 0.37) % 1; off_ = 30 + 70 * ph_; lat_ = (q - 2) * 16
                x0_ = x - ux_ * off_ - uy_ * lat_; y0_ = y - 60 - uy_ * off_ + ux_ * lat_
                bd2.line([x0_, y0_, x0_ - ux_ * 46, y0_ - uy_ * 46], fill=(255, 245, 220, int(230 * (1 - ph_))), width=5)
            for q in range(3):   # dust kicked up at the feet
                ph_ = (t * 5 + q / 3) % 1; dx_ = x - ux_ * (20 + 50 * ph_); dy_ = y - uy_ * (20 + 50 * ph_) - 6
                r_ = 8 + 14 * ph_; bd2.ellipse([dx_ - r_, dy_ - r_ * 0.7, dx_ + r_, dy_ + r_ * 0.7], fill=(215, 195, 160, int(170 * (1 - ph_))))
        bd2 = flush(b); b.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['stun'] and not s['caught']:
            for k in range(3):
                a = t * 7 + k * 2.09; star(bd2, x + 30 * math.cos(a), y - FOOT + 18 + 9 * math.sin(a), 11, (255, 220, 70, 255))
        if boosted and not s['caught']:
            for k in range(4):
                a = t * 9 + k * 1.57; sx, sy = x + 34 * math.cos(a), y - 70 + 50 * math.sin(a * 1.3)
                bd2.rectangle([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 230, 140, 230))
    for (t_s, a_s, b_s, sx_s, sy_s) in SHV:
        u = t - t_s
        if 0 <= u < 0.3:   # impact burst at the contact point
            for k in range(8):
                an = k * math.pi / 4; r0, r1 = 14 + 40 * u / 0.3, 30 + 70 * u / 0.3
                bd2.line([sx_s + r0 * math.cos(an), sy_s - 50 + r0 * math.sin(an), sx_s + r1 * math.cos(an), sy_s - 50 + r1 * math.sin(an)], fill=(255, 255, 230, int(255 * (1 - u / 0.3))), width=6)
        if 0 <= u < 0.9 and not st[b_s]['caught']:
            al = int(255 * min(1, (0.9 - u) / 0.3))
            LABELS.append((t_s, st[b_s]['x'], st[b_s]['y'] - FOOT - 18 - u * 40, 'BUMP!', (255, 255, 255), al))
    placed = []   # pop labels: newest keeps its spot, older ones stack above it so they never overlap
    for (t0_, lx, ly, txt, col, al) in sorted(LABELS, key=lambda e: -e[0]):
        tw = bd2.textlength(txt, font=F16); box = [lx - tw / 2 - 6, ly - 4, lx + tw / 2 + 6, ly + 36]
        moved = True
        while moved:
            moved = False
            for pb in placed:
                if box[0] < pb[2] and pb[0] < box[2] and box[1] < pb[3] and pb[1] < box[3]:
                    dy = box[3] - pb[1] + 2; box[1] -= dy; box[3] -= dy; moved = True
        placed.append(box)
        bd2.text((box[0] + 6, box[1] + 4), txt, font=F16, fill=col + (al,), stroke_width=5, stroke_fill=(40, 20, 10, al))
    for k in range(26):
        fx_ = (k * 137.5 + 40 * math.sin(t * 0.7 + k)) % (COLS * C); fy_ = (k * 211.3 + 30 * math.cos(t * 0.9 + k * 1.7)) % (ROWS * C)
        al_ = int(140 + 110 * math.sin(t * 3 + k))
        bd2.rectangle([fx_ - 6, fy_ - 6, fx_ + 6, fy_ + 6], fill=(220, 255, 140, al_ // 4)); bd2.rectangle([fx_ - 2, fy_ - 2, fx_ + 2, fy_ + 2], fill=(240, 255, 170, al_))
    bd2 = flush(b)
    img = BG.copy()
    view = b.crop((cx_cam, cy_cam, cx_cam + VWW, cy_cam + VHW)).resize((VW, VH), Image.NEAREST)
    img.alpha_composite(view, (OX, OY))
    d = ImageDraw.Draw(img)
    d.rectangle([OX - 8, OY - 8, OX + VW + 7, OY + VH + 7], outline=(30, 26, 40), width=8)
    for i, n in enumerate(NAMES):
        ix = W / 2 + (i - 1.5) * 200; iy = HB + 46
        ic = ICON[n]; s = st[n]
        if s['caught']: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55)
        img.alpha_composite(ic, (int(ix - ic.width / 2), int(iy - ic.height / 2)))
        d = ImageDraw.Draw(img)
        if s['caught']:
            for sg in (-1, 1):
                d.line([ix - 30, iy - 30 * sg, ix + 30, iy + 30 * sg], fill=(20, 10, 10), width=16)
                d.line([ix - 30, iy - 30 * sg, ix + 30, iy + 30 * sg], fill=(255, 60, 60), width=9)
        if s['out']: d.ellipse([ix - 42, iy - 42, ix + 42, iy + 42], outline=(255, 214, 60), width=6)
        if s['boost'] is not None and t >= s['boost'] and not s['caught']:
            img.alpha_composite(GUM.resize((GUM.width * 2 // 3, GUM.height * 2 // 3), Image.NEAREST), (int(ix + 12), int(iy + 2)))
    VCX = OX + VW / 2
    if (t < 1.6 and not OPEN) or OPEN:
        a_ = 255 if OPEN or t < 1.3 else int(255 * (1.6 - t) / 0.3)
        L_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L_)
        dl.rounded_rectangle([VCX - 352, OY + 40, VCX + 352, OY + 152], 16, fill=(14, 10, 24, int(a_ * 0.8)))
        ctext(dl, VCX, OY + 60, 'PICK ONE!', F(72), (255, 255, 255), 9, a_); img.alpha_composite(L_)
    # big stamps: OUT per elimination + the gummy power; placed in the half of the view away from the leader, never overlapping
    if not OPEN and t < T_OUT:
        lead = min((n for n in NAMES if not st[n]['caught']), key=lambda n: prog(st[n]))
        live = []
        for (t0, du, kind, txt, col, who) in STAMPS:
            u = t - t0
            if 0 <= u < du: live.append((t0, du, kind, txt, col, who, u))
        for k_, (t0, du, kind, txt, col, who, u) in enumerate(live):
            ly = (st[lead]['y'] - cy_cam) * 1.5 + OY
            top = ly > OY + VH * 0.5
            sy = (OY + 40 + k_ * 150) if top else (OY + VH - 150 - k_ * 150)
            sc = 1.25 - 0.25 * min(1, u / 0.12); a_ = int(255 * min(1, (du - u) / 0.2))
            icw = 96 if kind == 'pow' else 0; fs = int(min(72, (VW - 70 - icw) / len(txt)) * sc); fnt = F(fs)
            L_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L_)
            tw = dl.textlength(txt, font=fnt)
            x0 = VCX - (tw + icw) / 2
            dl.rounded_rectangle([x0 - 22, sy - 18, x0 + tw + icw + 22, sy + fs + 18], 18, fill=(14, 8, 18, int(a_ * 0.88)), outline=col + (a_,), width=6)
            dl.text((x0 + icw, sy), txt, font=fnt, fill=col + (a_,), stroke_width=9, stroke_fill=(20, 10, 10, a_))
            if kind == 'pow':
                gi = GUM.copy(); gi.putalpha(gi.getchannel('A').point(lambda p: p * a_ // 255)); L_.alpha_composite(gi, (int(x0), int(sy + fs / 2 - gi.height / 2)))
            img.alpha_composite(L_)
    d = ImageDraw.Draw(img)
    if t >= T_OUT and not OPEN:
        u = t - T_OUT; a = min(1, u / 0.15)
        img.alpha_composite(Image.new('RGBA', (VW, VH), (8, 6, 14, int(160 * a))), (OX, OY))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (int(VCX - vf.width / 2), OY + 330 - vf.height + 120))
        d = ImageDraw.Draw(img); ctext(d, VCX, OY + 470, LABEL[win] + ' ESCAPED!', F(56 if len(LABEL[win]) < 8 else 48), (255, 214, 60), 9)
        if u > 0.25:
            ctext(d, VCX, OY + 580, 'DID YOUR', F(64), (255, 255, 255), 9); ctext(d, VCX, OY + 672, 'GUIDE WIN?', F(64), (255, 255, 255), 9)
        if not any(e[1] == 'victory' for e in events): events.append((round(t, 3), 'victory'))
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in PREV: img.convert('RGB').save(OUTD + f'p_{f:03d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open(OUTD + 'v15_events.json', 'w'))
print('done', round(END, 2))
