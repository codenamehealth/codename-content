import numpy as np, math, random, subprocess, json, os, sys, glob
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'; A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
C = 64                                   # cell size on screen (32px tiles at 2x)
MAP = [
    "###############",
    "#.............#",
    "#..o...o...o..#",
    "#.............#",
    "###########...#",
    "#.............#",
    "#..o...o...o..#",
    "#.............#",
    "#...###########",
    "#.............#",
    "#..o...o...o..#",
    "#.............#",
    "###########...#",
    "#.............#",
    "#..o...o...o..#",
    "#.............#",
    "#...########EE#",
    "############EE#",
    "#.............#",
    "#..o...o...o..#",
    "#.............#",
    "###############"]
# corridor E is reached via the left gap of row 16? -> re-route: gap row 16 cols 1-3 leads down into E
MAP[16] = "#...###########"; MAP[17] = "#...########EE#"
ROWS, COLS = len(MAP), len(MAP[0])
OX = (W - COLS * C) // 2; OY = 360
def is_wall(r, c): return MAP[r][c] in '#o'
# ---------------- textures
wm = json.load(open('walls_meta.json')); wsh = Image.open('walls_sheet.png').convert('RGBA')
def tile(sh, b, s=2): return sh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32)).resize((32 * s, 32 * s), Image.NEAREST)
TILES = wm['tileset_data']['tiles']
FLOOR = tile(wsh, TILES[0]['bounding_box']); TOP = tile(wsh, TILES[6]['bounding_box'])
BRICK = tile(wsh, TILES[15]['bounding_box'])          # brick face over floor
sm = json.load(open('slime_meta.json')); ssh = Image.open('slime_sheet.png').convert('RGBA')
SLIME = tile(ssh, sm['tileset_data']['tiles'][12]['bounding_box'])
RIM = (104, 104, 112, 255); RIM2 = (70, 70, 80, 255)
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
DOOR = Image.open('exit_cands/07.png').convert('RGBA'); DOOR = DOOR.crop(DOOR.getbbox())
k = (2 * C) / DOOR.height; DOOR = DOOR.resize((int(DOOR.width * k), 2 * C), Image.NEAREST)
er = [r for r in range(ROWS) if 'E' in MAP[r]]; ec = [c for c in range(COLS) if 'E' in MAP[er[0]]]
ec = [c for c, ch in enumerate(MAP[er[0]]) if ch == 'E']
DOOR_XY = (ec[0] * C + C - DOOR.width // 2, (er[0] - 1) * C + 20)
board.alpha_composite(DOOR, DOOR_XY)
# torches (PixelLab, animated flame) on wall rows
TORCH = [f.resize((f.width * 2, f.height * 2), Image.NEAREST) for f in [Image.open(p).convert('RGBA') for p in sorted(glob.glob('torch_anim/*.png'))]]
TORCH_POS = [(4, 3), (4, 8), (8, 6), (8, 11), (12, 3), (12, 8), (16, 6), (16, 10)]
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
# ---------------- racers
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (120, 110, 150)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
R = 30
def face(name, rad):
    im = Image.open('../../syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    d.ellipse([12, 9, 20, 15], fill=(255, 255, 255, 170))
    return b
BALL = {n: face(n, R) for n in NAMES}
ICON = {n: face(n, 34) for n in NAMES}
def cell_of(x, y): return int(y // FC), int(x // FC)
def wall_at(x, y):
    r, c = int(y // C), int(x // C)
    return not passable(r, c)
T_START, T_SLIME = 2.4, 3.6
SA, SB = 6.0, 0.45
def sim(seed, dur=30.0):
    rnd = random.Random(seed)
    racers = {}; slots = list(range(len(NAMES))); rnd.shuffle(slots)
    for i, n in enumerate(NAMES):
        racers[n] = dict(x=2.2 * C + slots[i] * 1.9 * C, y=1.5 * C + rnd.uniform(0, 1.0) * C, vx=0.0, vy=0.0, base=rnd.uniform(255, 300),
                         ph=rnd.uniform(0, 6.28), caught=None, out=None, trail=[])
    front0 = 0.0; frames = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        front = 0 if t < T_SLIME else (t - T_SLIME) * (SA + SB * (t - T_SLIME))      # fine cells
        for n, s in racers.items():
            if s['caught'] is not None or s['out'] is not None or t < T_START: continue
            fr, fc = cell_of(s['x'], s['y'])
            gx, gy = -GX[fr, fc], -GY[fr, fc]; L = math.hypot(gx, gy) or 1
            sp = s['base'] * (1 + 0.32 * math.sin(0.9 * t + s['ph']) + 0.18 * math.sin(2.3 * t + 2 * s['ph']))
            wob = 0.55 * math.sin(3.7 * t + s['ph'] * 3)
            dx, dy = gx / L, gy / L
            tx, ty = dx - dy * wob, dy + dx * wob
            s['vx'] += (tx * sp - s['vx']) * 0.12; s['vy'] += (ty * sp - s['vy']) * 0.12
            nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
            # collide with walls (circle vs grid)
            for _ in range(2):
                for ax, ay in ((R, 0), (-R, 0), (0, R), (0, -R), (R * .7, R * .7), (-R * .7, R * .7), (R * .7, -R * .7), (-R * .7, -R * .7)):
                    if wall_at(nx + ax, ny + ay):
                        if ax: nx -= ax * 0.18; s['vx'] *= -0.4
                        if ay: ny -= ay * 0.18; s['vy'] *= -0.4
            s['x'], s['y'] = nx, ny
            # racer collisions
            for m, o in racers.items():
                if m == n or o['caught'] is not None or o['out'] is not None: continue
                ddx, ddy = s['x'] - o['x'], s['y'] - o['y']; dd = math.hypot(ddx, ddy)
                if 0 < dd < 2 * R:
                    push = (2 * R - dd) / 2; s['x'] += ddx / dd * push; s['y'] += ddy / dd * push
            fr, fc = cell_of(s['x'], s['y'])
            if int(s['y'] // C) == er[0] and int(s['x'] // C) in ec: s['out'] = t
            elif DSL[fr, fc] < front - 1.5: s['caught'] = t
            s['trail'] = (s['trail'] + [(s['x'], s['y'])])[-8:]
        frames.append(({n: (s['x'], s['y'], s['caught'] is not None and s['caught'] <= t, s['out'] is not None and s['out'] <= t, list(s['trail'])) for n, s in racers.items()}, front))
        if any(s['out'] is not None for s in racers.values()) and all(s['out'] is not None or s['caught'] is not None for s in racers.values()):
            break
    return racers, frames
def score(seed):
    rc, fr = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in rc.values() if s['caught'] is not None)
    if len(outs) != 1 or len(caught) != 4: return None
    tw = outs[0][0]
    if not (16 < tw < 22): return None
    if max(caught) < tw - 2.5: return None             # someone still alive near the end
    if min(caught) < 7: return None
    return round(tw, 2), outs[0][1], [round(c, 1) for c in caught]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(300):
        r = score(seed)
        if r: print(seed, r)
    sys.exit()
SEED = int(sys.argv[1]); WIN_OVERRIDE = None
rc, FR = sim(SEED)
win = [n for n, s in rc.items() if s['out'] is not None][0]; T_OUT = rc[win]['out']
print('winner', win, round(T_OUT, 2), {n: (round(s['caught'], 1) if s['caught'] else None) for n, s in rc.items()})
# ---------------- background (dark dungeon stone around the board)
bgt = TOP.copy(); BG = Image.new('RGBA', (W, H), (12, 10, 18, 255))
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
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
END = T_OUT + 3.0
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'maze_noaudio.mp4'], stdin=subprocess.PIPE)
events = []; caught_seen = set()
NF = int(END * FPS)
for f in range(NF):
    t = f / FPS; st, front = FR[min(f, len(FR) - 1)]
    img = BG.copy(); b = board.copy()
    # slime mask at fine resolution
    if front > 0:
        mask = (DSL < front).astype(np.uint8) * 255
        mi = Image.fromarray(mask, 'L').resize((COLS * C, ROWS * C), Image.NEAREST)
        wallm = Image.new('L', mi.size, 0); wd = ImageDraw.Draw(wallm)
        tex = Image.new('RGBA', mi.size)
        off = int(t * 18) % C
        for yy in range(-C, ROWS * C, C):
            for xx in range(-C, COLS * C, C): tex.alpha_composite(SLIME, (xx + off // 2, yy + off))
        edge = Image.fromarray(((DSL < front) & (DSL > front - 2.2)).astype(np.uint8) * 255, 'L').resize(mi.size, Image.NEAREST)
        b.paste(tex, (0, 0), mi)
        b.paste(Image.new('RGBA', mi.size, (190, 255, 120, 255)), (0, 0), edge.point(lambda p: p // 3))
        # re-draw wall faces over slime so walls stay on top
        for r in range(ROWS):
            for c in range(COLS):
                if is_wall(r, c) or MAP[r][c] == 'E':
                    b.alpha_composite(board.crop((c * C, r * C, c * C + C, r * C + C)), (c * C, r * C))
    for (r, c) in TORCH_POS:
        fr_ = TORCH[(int(t * 10) + r + c) % len(TORCH)]; b.alpha_composite(fr_, (c * C + C // 2 - fr_.width // 2, r * C + C - fr_.height - 20))
    bd2 = ImageDraw.Draw(b)
    for n in NAMES:
        x, y, caught, out, trail = st[n]
        if out: continue
        if not caught:
            for i, (tx, ty) in enumerate(trail[:-1]):
                a = int(60 + 140 * i / max(1, len(trail))); rr = 4 + i
                bd2.rectangle([tx - rr // 2, ty - rr // 2, tx + rr // 2, ty + rr // 2], fill=RING[n] + (a,))
        ball = BALL[n]
        if caught:
            g = ImageEnhance.Color(ball).enhance(0.25); g = ImageEnhance.Brightness(g).enhance(0.7)
            b.alpha_composite(g, (int(x - ball.width / 2), int(y - ball.height / 2)))
            bd2.ellipse([x - R - 4, y - R - 4, x + R + 4, y + R + 4], outline=(160, 255, 110, 200), width=4)
            if n not in caught_seen: caught_seen.add(n); events.append((round(t, 3), 'squish'))
        else:
            b.alpha_composite(ball, (int(x - ball.width / 2), int(y - ball.height / 2)))
    img.alpha_composite(b, (OX, OY))
    d = ImageDraw.Draw(img)
    d.rectangle([OX - 8, OY - 8, OX + COLS * C + 7, OY + ROWS * C + 7], outline=(30, 26, 40), width=8)
    # header
    d.rectangle([0, 0, W, 350], fill=(14, 10, 24, 235))
    ctext(d, W / 2, 50, 'WHO ESCAPES', F(68)); ctext(d, W / 2, 140, 'THE SLIME?', F(68), (140, 240, 90))
    for i, n in enumerate(NAMES):
        ix = W / 2 + (i - 2) * 170; iy = 245
        ic = ICON[n]; x, y, caught, out, _ = st[n]
        if caught: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55)
        img.alpha_composite(ic, (int(ix - ic.width / 2), int(iy - ic.height / 2)))
        if caught:
            d = ImageDraw.Draw(img); d.line([ix - 26, iy - 26, ix + 26, iy + 26], fill=(230, 50, 50), width=9); d.line([ix - 26, iy + 26, ix + 26, iy - 26], fill=(230, 50, 50), width=9)
        if out:
            d = ImageDraw.Draw(img); d.ellipse([ix - 42, iy - 42, ix + 42, iy + 42], outline=(255, 214, 60), width=6)
    d = ImageDraw.Draw(img)
    if t < T_START + 0.6:
        ctext(d, W / 2, OY + ROWS * C + 40, 'PICK ONE!', F(60), (255, 255, 255), 8)
    if t >= T_OUT:
        u = t - T_OUT; a = min(1, u / 0.3)
        ov = Image.new('RGBA', (W, H), (8, 6, 14, int(150 * a))); img.alpha_composite(ov)
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1060 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, W / 2, 1110, LABEL[win] + ' ESCAPED!', F(56), (255, 214, 60), 8)
        if u < 0.04: events.append((round(t, 3), 'vg02'))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('maze_events.json', 'w'))
print('done', round(END, 2))
