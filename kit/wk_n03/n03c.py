# n03 box maze, rebuild 3 (review: pixellab/review2/n03_box_maze/review.md).
# Format of viral_dl/1118_2000_outrun_the_shadow.mp4: four face boxes in start cells behind guild-coloured brick walls (Joy, Cleo,
# Cyrus, Rayleigh, same order as the roster), 3-2-1-GO, the boxes bounce passively (constant speed, no steering) and break their
# walls by hitting them, the shadow floods in from the top and chases them down a winding corridor maze, a box it overlaps is OUT
# (OUT tag + roster card crossed), one STRENGTH gummy (bricks break in one hit), the dragon sits on its hoard (gummies) in the
# checkered exit room mid-maze on the right behind a brick wall the boxes must break, the first box across the finish line wins:
# everything freezes on that frame, winner card (Syeda victory pose, NAME WINS!, DID YOUR GUIDE WIN?).
# World units = screen pixels (32px cells); clean physics: sub-stepped axis-separated exact AABB collisions, equal-mass elastic
# box-box contacts on the least-penetration axis, constant speed; the dragon and hoard are solid.
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
C = 32
# ---------------- maze: start cells + corridor on top, then a serpentine of four long columns; the exit room sits mid-maze on the
# right at the top of the last column, above the caption zone
MAP = []
def row(s): assert len(s) == 32, s; MAP.append(s)
row('#' * 32)
for r in range(4): row('#' + '111111' + '##' + '222222' + '##' + '333333' + '##' + '444444' + '#')
for r in range(2): row('#' + 'gggggg' + '##' + 'gggggg' + '##' + 'gggggg' + '##' + 'gggggg' + '#')
for r in range(4): row('#' + '.' * 30 + '#')                                    # rows 7-10: corridor under the start cells
row('#' + '......' + '#' * 25)                                                   # row 11
for r in range(12, 28):
    s = ['#'] * 32
    for c in range(1, 7): s[c] = '.'                                             # column 1 (down)
    if r >= 23: s[7] = s[8] = '.'                                                # gap col1 -> col2 at the bottom
    for c in range(9, 15): s[c] = '.'                                            # column 2 (up)
    if r <= 15: s[15] = s[16] = '.'                                              # gap col2 -> col3 at the top
    for c in range(17, 23): s[c] = '.'                                           # column 3 (down)
    if r >= 23: s[23] = s[24] = '.'                                              # gap col3 -> col4 at the bottom
    for c in range(25, 31):
        if r <= 16: s[c] = 'D' if (13 <= r <= 15 and c >= 27) else 'E'          # exit room (dragon + hoard solid, finish strip free)
        elif r <= 18: s[c] = 'b'                                                 # exit brick wall
        else: s[c] = '.'                                                         # column 4 (up)
    row(''.join(s))
row('#' * 32)
ROWS, COLS = len(MAP), len(MAP[0])
OX = (W - COLS * C) // 2; OY = int(os.environ.get('OY', '466'))
def is_wall(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or MAP[r][c] in '#D'
CH = {'joy': 1, 'cleo': 9, 'cyrus': 17, 'ray': 25}
BRK0 = {}
for k, c0 in enumerate([1, 9, 17, 25]): BRK0['gate%d' % k] = dict(rect=(OX + c0 * C, OY + 5 * C, OX + (c0 + 6) * C, OY + 7 * C), hp=3)
BRK0['exit'] = dict(rect=(OX + 25 * C, OY + 17 * C, OX + 31 * C, OY + 19 * C), hp=int(os.environ.get('EXHP', '3')))
EXIT_Y = OY + 17 * C                                                             # the finish line (room edge)
EXX0, EXX1 = OX + 25 * C, OX + 31 * C
GUM_POS = (OX + float(os.environ.get('GUMX', '20')) * C, OY + float(os.environ.get('GUMY', '19.5')) * C)
HS = 28
SPD = float(os.environ.get('SPD', '440'))
SUB = 8
T_GO = float(os.environ.get('TGO', '1.8')); CD = T_GO / 3
H2 = C // 2
# ---------------- shadow: flood fill on half cells from the tops of the start cells (shared geometry for physics and drawing)
SUBR, SUBC = ROWS * 2, COLS * 2
def sub_open(r, c): return not is_wall(r // 2, c // 2)
SRC = [(2, c) for c in range(SUBC) if sub_open(2, c)]
DIST = {s: 0 for s in SRC}; q = deque(SRC)
while q:
    r, c = q.popleft()
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (r + dr, c + dc)
        if 0 <= n[0] < SUBR and 0 <= n[1] < SUBC and sub_open(*n) and n not in DIST: DIST[n] = DIST[(r, c)] + 1; q.append(n)
BDIST = min(DIST[(r, c)] for (r, c) in DIST if MAP[r // 2][c // 2] == 'b')      # the dark stops at the exit wall
SUBDIR = {}
for (r, c), dv in DIST.items():
    best = min(((DIST.get((r + dr, c + dc), 999), dr, dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))))
    SUBDIR[(r, c)] = (best[1], best[2]) if best[0] < dv else (-1, 0)
def sub_rect(r, c, cov):
    """the part of half-cell (r, c) the dark covers, in world px; it creeps in from the neighbour it came from"""
    x0, y0 = OX + c * H2, OY + r * H2
    if cov >= 1: return (x0, y0, x0 + H2, y0 + H2)
    k = H2 * cov; dr, dc = SUBDIR[(r, c)]
    if dr == -1: return (x0, y0, x0 + H2, y0 + k)
    if dr == 1: return (x0, y0 + H2 - k, x0 + H2, y0 + H2)
    if dc == -1: return (x0, y0, x0 + k, y0 + H2)
    return (x0 + H2 - k, y0, x0 + H2, y0 + H2)
VIS_DEPTH = float(os.environ.get("VISD", "6"))                                                                  # OUT only once the dark visibly overlaps the box
def shadow_hits(x, y, front):
    r0, r1 = int((y - HS - OY) // H2), int((y + HS - 1 - OY) // H2)
    c0, c1 = int((x - HS - OX) // H2), int((x + HS - 1 - OX) // H2)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            d = DIST.get((r, c))
            if d is None or d >= front: continue
            a0, b0, a1, b1 = sub_rect(r, c, min(1.0, front - d))
            ox_ = min(a1, x + HS) - max(a0, x - HS); oy_ = min(b1, y + HS) - max(b0, y - HS)
            if ox_ >= VIS_DEPTH and oy_ >= VIS_DEPTH: return True
    return False
def front_of(t, sh0, shv, sha):
    f = 0.0 if t < sh0 else shv * (t - sh0) + 0.5 * sha * (t - sh0) ** 2
    return min(f, BDIST - 0.01)
# ---------------- physics
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
            if x1 > x - HS - 40 and x0 < x + HS + 40 and y1 > y - HS - 40 and y0 < y + HS + 40: out.append((x0, y0, x1, y1, k))
    return out
CFLAGS = []                                                                      # per frame: which boxes touched a wall/brick/box
def sim(seed, dur=float(os.environ.get('SIMDUR', '24'))):
    rnd = random.Random(seed)
    sh0, shv, sha = float(os.environ.get('SH0', '6')), float(os.environ.get('SHV', '2')), float(os.environ.get('SHA', '0.2'))
    B = {k: dict(v) for k, v in BRK0.items()}
    for k in B: B[k]['hits'] = []; B[k]['broke'] = None
    X = {}
    for g in G:
        cx = OX + (CH[g] + 3) * C; cy = OY + 2.5 * C
        a = rnd.uniform(0.3, 1.27) * (1 if rnd.random() < 0.5 else -1) + (math.pi if rnd.random() < 0.3 else 0)
        X[g] = dict(x=cx + rnd.uniform(-30, 30), y=cy + rnd.uniform(-20, 20), vx=SPD * math.sin(a), vy=SPD * math.cos(a), out=None, strong=False, last={})
    gum = dict(x=GUM_POS[0], y=GUM_POS[1], t=None, who=None)
    ev = []; frames = []; wallhits = []; win = None
    CFLAGS.clear()
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS / SUB; CF = {g: False for g in G}
        for _ in range(SUB if t >= T_GO else 0):
            for g in G:
                p = X[g]
                if p['out'] is not None: continue
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
                                if B[k]['hp'] <= 0: B[k]['broke'] = (t, g, p['vx'], p['vy'], p['strong']); ev.append((t, 'break', g, k)); broke = True
                                else: ev.append((t, 'crack', g, k))
                            if broke: continue                       # the breaking hit carries straight through the wall
                            p['v' + axis] = -v
                            ang = rnd.uniform(-0.044, 0.044); vx, vy = p['vx'], p['vy']   # +-2.5 deg surface imperfection
                            p['vx'], p['vy'] = vx * math.cos(ang) - vy * math.sin(ang), vx * math.sin(ang) + vy * math.cos(ang)
                            wallhits.append((t, g, k)); CF[g] = True
            live = [g for g in G if X[g]['out'] is None]
            for i in range(len(live)):
                for j in range(i + 1, len(live)):
                    a_, b_ = X[live[i]], X[live[j]]
                    px, py = 2 * HS - abs(a_['x'] - b_['x']), 2 * HS - abs(a_['y'] - b_['y'])
                    if px <= 0 or py <= 0: continue
                    if px < py:
                        s = 1 if a_['x'] < b_['x'] else -1; a_['x'] -= s * px / 2; b_['x'] += s * px / 2
                        if (b_['vx'] - a_['vx']) * s < 0:                # each box bounces off the other like off a wall: own speed, own angle
                            a_['vx'] = -s * abs(a_['vx']); b_['vx'] = s * abs(b_['vx']); ev.append((t, 'bump', live[i], live[j])); CF[live[i]] = CF[live[j]] = True
                    else:
                        s = 1 if a_['y'] < b_['y'] else -1; a_['y'] -= s * py / 2; b_['y'] += s * py / 2
                        if (b_['vy'] - a_['vy']) * s < 0:
                            a_['vy'] = -s * abs(a_['vy']); b_['vy'] = s * abs(b_['vy']); ev.append((t, 'bump', live[i], live[j])); CF[live[i]] = CF[live[j]] = True
            for g in live:
                p = X[g]; v = math.hypot(p['vx'], p['vy']) or 1; p['vx'] *= SPD / v; p['vy'] *= SPD / v
        front = front_of(t, sh0, shv, sha)
        for g in G:
            p = X[g]
            if p['out'] is not None or t < T_GO: continue
            if gum['t'] is None and abs(p['x'] - gum['x']) < HS + 14 and abs(p['y'] - gum['y']) < HS + 14:
                gum['t'] = t; gum['who'] = g; p['strong'] = True; ev.append((t, 'pick', g, 'cre'))
            if p['y'] - HS < EXIT_Y and p['y'] > OY + 14 * C and EXX0 <= p['x'] <= EXX1:
                win = (t, g); ev.append((t, 'win', g)); break
            if shadow_hits(p['x'], p['y'], front):
                p['out'] = t; ev.append((t, 'out', g))
        CFLAGS.append(CF)
        frames.append(({g: (X[g]['x'], X[g]['y'], X[g]['vx'], X[g]['vy'], X[g]['out'], X[g]['strong']) for g in G}, front, {k: B[k]['hp'] for k in B}))
        if win or all(X[g]['out'] is not None for g in G): break           # the win freezes everyone on this frame
    return X, frames, ev, gum, B, wallhits, win
WANT = os.environ.get('WANT', 'cyrus'); TW0, TW1 = float(os.environ.get('TW0', '13.5')), float(os.environ.get('TW1', '17.0'))
def score(seed):
    X, fr, ev, gum, B, wh, win = sim(seed)
    if not win or win[1] != WANT: return None
    tw = win[0]
    if not (TW0 < tw < TW1): return None
    outs = sorted(e[0] for e in ev if e[1] == 'out')
    if len(outs) < 2 or not (4.3 <= outs[0] <= 6.8): return None
    if any(b - a < 1.2 for a, b in zip(outs, outs[1:])): return None
    if gum['t'] is None or gum['t'] > tw - 1.0 or any(abs(gum['t'] - o) < 1.0 for o in outs): return None
    gates = [B['gate%d' % k]['broke'] for k in range(4)]
    sh0 = float(os.environ.get('SH0', '6'))
    if any(gb is None or gb[0] > sh0 + 0.5 for gb in gates): return None   # every start cell open before the dark reaches it
    st = fr[-1][0]; fw = fr[-1][1]
    alive = [g for g in G if g != WANT and st[g][4] is None]
    wx, wy = st[WANT][0], st[WANT][1]
    dw = min((DIST.get((int((wy - OY) // H2) + dr, int((wx - OX) // H2) + dc), 999) for dr in (1, 2, 3) for dc in (-1, 0, 1)), default=999)
    gap = round(dw - fw, 1)
    t4 = next((i / FPS for i, (s_, f_, h_) in enumerate(fr) if s_[WANT][0] > OX + 25 * C and s_[WANT][1] > OY + 19 * C), None)
    if t4 is None or t4 > float(os.environ.get('T4MAX', '12.5')): return None
    eb = B['exit']['broke']
    return dict(t4=round(t4, 1), tw=round(tw, 2), outs=[round(o, 1) for o in outs], gum=(round(gum['t'], 1), gum['who']), alive=alive, gap=gap,
                exit=(round(eb[0], 1), eb[1], eb[4]) if eb else None, exhits=[h[1] for h in B['exit']['hits']])
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
XX, FR, EV, GUM, BB, WH, WIN = sim(SEED)
T_WIN = WIN[0] if WIN else None
print('win', WIN, {g: XX[g]['out'] for g in G}, 'gum', GUM['t'], GUM['who'])
for e in EV:
    if e[1] != 'bump': print('  ', round(e[0], 2), e[1:])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()
# =====================================================================  RENDER
from PIL import ImageFilter, ImageEnhance, ImageChops
T_CARD = T_WIN + float(os.environ.get('CARDDLY', '0.6'))            # the win freezes everything; a beat, then the winner card
T_END = T_CARD + float(os.environ.get('HOLD', '3.3')); XF = 0.35; NF = int(round(T_END * FPS))
def fidx(t): return min(max(0, int(round(t * FPS))), len(FR) - 1)
def frame_at(t): return FR[fidx(t)]
OWNER = {[1, 9, 17, 25].index(CH[g]): g for g in G}
MX0, MY0, MX1, MY1 = OX, OY, OX + COLS * C, OY + ROWS * C
# ---------------- assets
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
    FACE24[g] = im.crop((cx - 12, 15, cx + 12, 39))
ROSTER_FACE = {g: up(FACE24[g], 3) for g in G}
def vic_frames(g, k):
    im = Image.open(A + VIC[g]); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), k))
    return out
VIC_W = vic_frames(WANT, 6)
GUMI = up(Image.open(PL + 'gummies/pick_cre.png').convert('RGBA'), 2)
STR_COL = (255, 92, 70)
DRAGON = Image.open('dragon_gummies.png').convert('RGBA')               # same dragon, hoard swapped for Code Name gummies (hoard.py)
moon = Image.open(A + 'bg_moon.gif'); BG = []
for i in range(0, moon.n_frames, 2):
    moon.seek(i); f_ = moon.convert('RGB').resize((3413, 1920), Image.LANCZOS).crop((1166, 0, 1166 + W, H)).filter(ImageFilter.GaussianBlur(6))
    BG.append(ImageEnhance.Brightness(f_).enhance(0.42).convert('RGBA'))
# ---------------- floor: warm sandstone tiles (2x pixels), low contrast, subtle alternating tone like the reference's sand
def stone_tile(tone, seed):
    rr = random.Random(seed); t_ = Image.new('RGBA', (32, 32), tone + (255,)); px = t_.load()
    gr = tuple(int(v * 0.84) for v in tone); hi = tuple(min(255, int(v * 1.06)) for v in tone)
    for i in range(32):
        px[i, 31] = gr + (255,); px[31, i] = gr + (255,); px[i, 0] = hi + (255,); px[0, i] = hi + (255,)
    for n in range(26):
        x, y = rr.randint(2, 29), rr.randint(2, 29); px[x, y] = (tuple(int(v * 0.92) for v in tone) if n % 2 else tuple(min(255, int(v * 1.04)) for v in tone)) + (255,)
    for n in range(3):                                                   # a few tiny pits
        x, y = rr.randint(3, 27), rr.randint(3, 27); px[x, y] = tuple(int(v * 0.86) for v in tone) + (255,); px[x + 1, y] = tuple(int(v * 0.9) for v in tone) + (255,)
    return up(t_, 2)
TONES = [(226, 199, 152), (216, 187, 141)]
# ---------------- static maze layer
MZ = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(MZ)
d.rounded_rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], 8, fill=(22, 18, 32, 255), outline=(74, 66, 96, 255), width=4)
for r0 in range(0, ROWS, 2):
    for c0 in range(0, COLS, 2):
        tl = stone_tile(TONES[(r0 // 2 + c0 // 2) % 2], r0 * 97 + c0)
        for dr in range(2):
            for dc in range(2):
                r, c = r0 + dr, c0 + dc
                if r < ROWS and c < COLS and not is_wall(r, c) or (r < ROWS and c < COLS and MAP[r][c] == 'D'):
                    MZ.alpha_composite(tl.crop((dc * C, dr * C, dc * C + C, dr * C + C)), (OX + c * C, OY + r * C))
d = ImageDraw.Draw(MZ)
for r in range(ROWS):                                                    # checkered exit room: the finish
    for c in range(COLS):
        if MAP[r][c] not in 'ED': continue
        for i in range(2):
            for j in range(2):
                col_ = (236, 236, 236, 255) if (i + j + r * 2 + c * 2) % 2 == 0 else (30, 30, 36, 255)
                d.rectangle([OX + c * C + j * 16, OY + r * C + i * 16, OX + c * C + j * 16 + 15, OY + r * C + i * 16 + 15], fill=col_)
rnd_ = random.Random(7)
for r in range(ROWS):
    for c in range(COLS):
        if MAP[r][c] != '#': continue
        x0, y0 = OX + c * C, OY + r * C
        d.rectangle([x0, y0, x0 + C - 1, y0 + C - 1], fill=(40, 36, 54, 255))
        for k in range(2):
            px_, py_ = x0 + rnd_.randint(1, 6) * 4, y0 + rnd_.randint(1, 6) * 4
            d.rectangle([px_, py_, px_ + 5, py_ + 3], fill=(50, 46, 66, 255))
for r in range(ROWS):
    for c in range(COLS):
        if MAP[r][c] != '#': continue
        x0, y0 = OX + c * C, OY + r * C
        if r + 1 < ROWS and MAP[r + 1][c] != '#':                         # brick face (3/4 view lip) on the wall's south side
            MZ.alpha_composite(BRICK.crop(((c % 3) * 32, 0, (c % 3) * 32 + C, 16)), (x0, y0 + C - 16))
            d.rectangle([x0, y0 + C - 18, x0 + C - 1, y0 + C - 17], fill=(150, 146, 168, 255))
        rim = (118, 114, 140, 255)
        if r > 0 and MAP[r - 1][c] != '#': d.rectangle([x0, y0, x0 + C - 1, y0 + 2], fill=rim)
        if c > 0 and MAP[r][c - 1] != '#': d.rectangle([x0, y0, x0 + 2, y0 + C - 1], fill=rim)
        if c + 1 < COLS and MAP[r][c + 1] != '#': d.rectangle([x0 + C - 3, y0, x0 + C - 1, y0 + C - 1], fill=rim)
ao = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ao)
for r in range(1, ROWS):
    for c in range(COLS):
        if MAP[r][c] != '#' and MAP[r - 1][c] == '#':
            for k in range(4): ad.rectangle([OX + c * C, OY + r * C + 2 * k, OX + c * C + C - 1, OY + r * C + 2 * k + 1], fill=(10, 6, 20, 80 - k * 18))
MZ.alpha_composite(ao)
DRX = OX + 31 * C - 2 - DRAGON.width; DRY = OY + 16 * C + 2 - DRAGON.height     # rests on the solid cells, finish strip free below
MZ.alpha_composite(DRAGON, (DRX, DRY))
# ---------------- breakable brick walls: guild-coloured start walls, a dark exit wall; cracks grow with each hit
BCOL = {('gate%d' % k): COL[OWNER[k]] for k in range(4)}; BCOL['exit'] = (120, 96, 150)
HP0 = {k: BRK0[k]['hp'] for k in BRK0}
def irect(k): return tuple(int(v) for v in BRK0[k]['rect'])
def brick_img(k):
    x0, y0, x1, y1 = irect(k); w, h = x1 - x0, y1 - y0
    base = Image.new('RGBA', (w, h)); bt = tint(BRICK, BCOL[k], 0.8)
    for xx in range(0, w, bt.width):
        for yy in range(0, h, bt.height): base.alpha_composite(bt, (xx, yy))
    dd = ImageDraw.Draw(base)
    dd.rectangle([0, 0, w - 1, 3], fill=tuple(min(255, int(v * 1.3)) for v in BCOL[k]) + (255,)); dd.rectangle([0, h - 4, w - 1, h - 1], fill=(20, 14, 26, 255))
    dd.rectangle([0, 0, w - 1, h - 1], outline=(18, 12, 24, 255), width=2)
    return base
BIMG = {k: brick_img(k) for k in BRK0}
def crack_at(k, hx, top, seed):
    x0, y0, x1, y1 = irect(k); w, h = x1 - x0, y1 - y0; rr = random.Random(seed)
    px = max(8, min(w - 9, int(hx) - x0)); py = 0 if top else h - 1; dy = 4 if top else -4; pts = [(px, py)]; br = []
    while 0 <= py + dy < h:
        py += dy; px = max(3, min(w - 4, px + rr.choice([-4, -2, 0, 2, 4]))); pts.append((px, py))
        if len(pts) == 5: br = [(px, py)] + [(px + s_ * 4 * n, py + dy * n // 2) for n, s_ in zip(range(1, 4), [rr.choice([-1, 1])] * 3)]
    return [[(a // 2 * 2, b // 2 * 2) for a, b in pts], [(a // 2 * 2, max(0, min(h - 1, b)) // 2 * 2) for a, b in br]]
def wall_img(k, stage):
    im = BIMG[k].copy(); dd = ImageDraw.Draw(im); x0, y0, x1, y1 = irect(k); wy = (y0 + y1) / 2
    for j, (th, g, bx, by) in enumerate(BB[k]['hits'][:stage]):
        top = by < wy
        for path in crack_at(k, bx, top, 31 + j * 17 + len(k)):
            if len(path) < 2: continue
            dd.line(path, fill=(14, 8, 20, 255), width=3); dd.line([(a + 2, b) for a, b in path], fill=(255, 255, 255, 55), width=1)
        if j == 1:
            cx_ = int(max(9, min(x1 - x0 - 10, bx - x0))); cy_ = 0 if top else (y1 - y0) - 10
            dd.rectangle([cx_ - 7, cy_, cx_ + 6, cy_ + 9], fill=(22, 16, 30, 255))
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
        side = -1 if by < wy else 1
        brk = BB[k]['broke'] is not None and abs(BB[k]['broke'][0] - th) < 1e-6
        if brk:
            dirn = 1 if by < wy else -1
            for n in range(20):
                px = prr.uniform(x0 + 4, x1 - 4); py = prr.uniform(y0 + 4, y1 - 4)
                sp = prr.uniform(110, 380); ang = prr.uniform(-0.8, 0.8) + (math.pi / 2 if dirn > 0 else -math.pi / 2)
                pull = max(0.0, 1 - abs(px - bx) / 90)
                PARTS.append(dict(t0=th, x=px, y=py, vx=sp * math.cos(ang) + (px - bx) * 0.6, vy=sp * math.sin(ang) * (1 + 0.6 * pull), sz=prr.choice([8, 10, 10, 12, 14]),
                                  col=tuple(int(v * prr.uniform(0.55, 1.05)) for v in BCOL[k]), ok=True))
        else:
            cx_ = max(x0 + 6, min(x1 - 6, bx)); cy_ = y0 if side < 0 else y1
            for n in range(5):
                ang = prr.uniform(-1.1, 1.1) + (-math.pi / 2 if side < 0 else math.pi / 2); sp = prr.uniform(50, 150)
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
        if solid_at(x, y, t): p['ok'] = False
        p['cur'] = (x, y); PPOS[f][i] = (x, y)
# ---------------- shadow (same half-cell geometry the physics uses)
SUBS = sorted(DIST.items(), key=lambda z: z[1])
SW_, SH_ = COLS * C, ROWS * C
NZ = Image.effect_noise((SW_ // 4, SH_ // 4), 60).resize((SW_, SH_), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
NZa = np.array(NZ).astype(float) / 255.0
SHC = np.zeros((SH_, SW_, 4), np.uint8)
SHC[..., 0] = (20 + 30 * NZa).astype(np.uint8); SHC[..., 1] = (9 + 12 * NZa).astype(np.uint8); SHC[..., 2] = (38 + 50 * NZa).astype(np.uint8); SHC[..., 3] = 248
SHADOW_TEX = Image.fromarray(SHC)
EYES = [(r, c) for (r, c) in DIST if (r * 7 + c * 13) % 29 == 0 and DIST.get((r, c + 1)) is not None]
def shadow_layer(t, fr_):
    m = Image.new('L', (SW_, SH_), 0); md = ImageDraw.Draw(m); rim = []
    for (r, c), dv in SUBS:
        cov = fr_ - dv
        if cov <= 0: break
        a0, b0, a1, b1 = sub_rect(r, c, min(1.0, cov)); a0 -= OX; a1 -= OX; b0 -= OY; b1 -= OY
        if a1 - a0 < 1 or b1 - b0 < 1: continue
        md.rectangle([a0, b0, a1 - 1, b1 - 1], fill=255)
        if cov < 1:
            dr, dc = SUBDIR[(r, c)]
            if dr == -1: rim.append([a0, b1 - 3, a1 - 1, b1 - 1])
            elif dr == 1: rim.append([a0, b0, a1 - 1, b0 + 2])
            elif dc == -1: rim.append([a1 - 3, b0, a1 - 1, b1 - 1])
            else: rim.append([a0, b0, a0 + 2, b1 - 1])
    L = Image.new('RGBA', (SW_, SH_), (0, 0, 0, 0)); L.paste(SHADOW_TEX, (int(6 * math.sin(t)), 0), m)
    dd = ImageDraw.Draw(L)
    for b_ in rim: dd.rectangle(b_, fill=(175, 115, 255, 225))
    for (r, c) in EYES:
        if fr_ - DIST[(r, c)] < 3 or fr_ - DIST[(r, c + 1)] < 3: continue
        ex, ey = c * H2 + 6, r * H2 + 4
        if (int(t * 1.7 + r * 3 + c) % 9) == 0: dd.rectangle([ex, ey + 4, ex + 20, ey + 6], fill=(230, 220, 255, 230))
        else: dd.rectangle([ex, ey, ex + 5, ey + 8], fill=(240, 235, 255, 245)); dd.rectangle([ex + 15, ey, ex + 20, ey + 8], fill=(240, 235, 255, 245))
    return L
# ---------------- boxes (56px: 24x24 face crop at 2x)
def box_img(g, k=1.0, dark=0.0):
    n = 2 * HS; b = Image.new('RGBA', (n, n), (0, 0, 0, 0)); dd = ImageDraw.Draw(b)
    dd.rectangle([0, 0, n - 1, n - 1], fill=(14, 10, 20, 255))
    fc = up(FACE24[g], 2); bg_ = Image.new('RGBA', fc.size, tuple(int(v * 0.55) for v in COL[g]) + (255,)); bg_.alpha_composite(fc)
    b.alpha_composite(bg_, ((n - fc.width) // 2, (n - fc.height) // 2))
    dd = ImageDraw.Draw(b); dd.rectangle([2, 2, n - 3, n - 3], outline=COL[g] + (255,), width=3)
    dd.rectangle([5, 5, 12, 7], fill=(255, 255, 255, 190))
    if dark > 0: b = Image.blend(b, Image.new('RGBA', b.size, (30, 16, 50, 255)), dark).copy(); b.putalpha(Image.new('L', b.size, 255))
    if k != 1.0: b = b.resize((max(2, int(b.width * k)), max(2, int(b.height * k))), Image.NEAREST)
    return b
BOXI = {g: box_img(g) for g in G}
# ---------------- HUD: roster (crossed with OUT on a catch, as in the reference)
RY0 = MY1 + 12                                                         # name bar fully above the bottom caption zone
def roster(img, t):
    tt = min(t, T_WIN)
    for i, g in enumerate(G):
        x0 = 30 + i * 257; x1 = x0 + 247
        out = XX[g]['out'] is not None and XX[g]['out'] <= tt
        win = t >= T_WIN and g == WANT
        layer(img, lambda dd, x0=x0, x1=x1, win=win, g=g: dd.rounded_rectangle([x0, RY0, x1, RY0 + 90], 14, fill=(14, 10, 22, 230), outline=(255, 214, 60, 255) if win else COL[g] + (255,), width=6 if win else 4))
        fc = ROSTER_FACE[g]
        if out: fc = ImageEnhance.Brightness(ImageEnhance.Color(fc).enhance(0.15)).enhance(0.45)
        img.alpha_composite(fc, (x0 + 9, RY0 + 9))
        nm = NAME[g]; fs_ = 26 if len(nm) <= 5 else 18
        d_ = ImageDraw.Draw(img); d_.text((x0 + 88, RY0 + 24 + (26 - fs_) // 2), nm, font=F(fs_), fill=(120, 110, 130) if out else COL[g], stroke_width=4, stroke_fill=(10, 6, 16))
        if out:
            d_.line([x0 + 10, RY0 + 10, x0 + 80, RY0 + 80], fill=(230, 50, 60), width=7); d_.line([x0 + 10, RY0 + 80, x0 + 80, RY0 + 10], fill=(230, 50, 60), width=7)
            d_.text((x0 + 90, RY0 + 58), 'OUT', font=F(20), fill=(240, 70, 70), stroke_width=3, stroke_fill=(10, 6, 16))
SCHED = [(e[0], e[0] + 1.1, (NAME[e[2]] + ': STRENGTH!', STR_COL)) for e in EV if e[1] == 'pick']   # the power stamp names the guide
SMASH = BB['exit']['broke'] if (BB['exit']['broke'] is not None and BB['exit']['broke'][4]) else None
print('beats: go', T_GO, 'win', round(T_WIN, 2), 'card', round(T_CARD, 2), 'end', round(T_END, 2), 'smash', SMASH and round(SMASH[0], 2))
STILLS = [float(x) for x in os.environ.get('STILLS', '').split(',') if x]
EVONLY = bool(os.environ.get('EVONLY'))
OUTV = os.environ.get('OUTV', 'n03_noaudio_tmp.mp4')
wr = None if (STILLS or EVONLY) else Writer(OUTV)
WINXY = (frame_at(T_WIN)[0][WANT][0], frame_at(T_WIN)[0][WANT][1])
def clampx(x, half): return max(MX0 + 8 + half, min(MX1 - 8 - half, x))
POSE_FEET = 1236
HAND = {'joy': (30, 47), 'ray': (25, 47), 'cyrus': (27, 22), 'cleo': (30, 40)}     # free hand in each 92px victory pose
FIST = (540 - 276 + HAND[WANT][0] * 6, POSE_FEET - int(552 * 78 / 92) + HAND[WANT][1] * 6)
TOSS0, TOSS1 = T_CARD + 0.85, T_CARD + 1.45                           # the dragon tosses him a gummy, he catches it
TOSS_G = up(Image.open(PL + 'gummies/pick_mel.png').convert('RGBA'), 2)
DIGITS = [0.0, CD, 2 * CD, T_GO]
def grab_dir(g):
    out = XX[g]['out']; st_, front, _ = frame_at(out); x, y = st_[g][0], st_[g][1]; sxs = []; sys_ = []
    r0, r1 = int((y - HS - OY) // H2), int((y + HS - 1 - OY) // H2); c0, c1 = int((x - HS - OX) // H2), int((x + HS - 1 - OX) // H2)
    for r in range(r0 - 1, r1 + 2):
        for c in range(c0 - 1, c1 + 2):
            dv = DIST.get((r, c))
            if dv is not None and dv < front: sxs.append(OX + c * H2 + H2 / 2 - x); sys_.append(OY + r * H2 + H2 / 2 - y)
    mx, my = (sum(sxs) / len(sxs), sum(sys_) / len(sys_)) if sxs else (0, -1)
    return (0, -1 if my < 0 else 1) if abs(my) >= abs(mx) else (-1 if mx < 0 else 1, 0)
GRAB = {g: grab_dir(g) for g in G if XX[g]['out'] is not None}
T_EYES = next((i / FPS for i, (s_, f_, h_) in enumerate(FR) if any(f_ - DIST[(r, c)] >= 3 and f_ - DIST[(r, c + 1)] >= 3 for (r, c) in EYES)), None)
def bounce(f):
    for td in DIGITS:
        k = f - int(round(td * FPS))
        if 0 <= k < 2: return (1.18, 1.08)[k]
    return 1.0
def sparkle(dd, x, y, s_, a_):
    col = (255, 236, 150, a_); dd.rectangle([x - s_, y - 1, x + s_, y + 1], fill=col); dd.rectangle([x - 1, y - s_, x + 1, y + s_], fill=col); dd.rectangle([x - 1, y - 1, x + 1, y + 1], fill=(255, 255, 255, a_))
def draw(f):
    t = f / FPS
    st, fr_, hp = frame_at(t)
    img = BG[int(t * 5) % len(BG)].copy()
    img.alpha_composite(MZ)
    for i, p in enumerate(PARTS):                                       # rubble on the floor
        pp = PPOS[f][i]
        if pp is None or not p['ok']: continue
        x, y = pp; s_ = p['sz']
        layer(img, lambda dd, x=x, y=y, s_=s_, p=p: (dd.rectangle([x - s_ / 2 + 2, y - s_ / 2 + 2, x + s_ / 2 + 1, y + s_ / 2 + 1], fill=(10, 6, 18, 120)),
                                                    dd.rectangle([x - s_ / 2, y - s_ / 2, x + s_ / 2 - 1, y + s_ / 2 - 1], fill=p['col'] + (255,)),
                                                    dd.rectangle([x - s_ / 2, y + s_ / 2 - 2, x + s_ / 2 - 1, y + s_ / 2 - 1], fill=tuple(int(v * 0.6) for v in p['col']) + (255,))))
    for k in BRK0:                                                      # brick walls (shake on a hit, crack stages)
        if hp[k] <= 0: continue
        x0, y0, x1, y1 = irect(k); stage = min(2, HP0[k] - hp[k])
        lastk = [h[0] for h in BB[k]['hits'] if h[0] <= t]
        sh_ = int(3 * math.sin((t - lastk[-1]) * 90)) if lastk and t - lastk[-1] < 0.12 else 0
        img.alpha_composite(WIMG[k][stage], (x0 + sh_, y0))
        if k.startswith('gate'):                                       # countdown: each digit pulses the guide's wall
            for td in DIGITS:
                if 0 <= t - td < 0.3:
                    u = (t - td) / 0.3; colg = BCOL[k]
                    layer(img, lambda dd, x0=x0, y0=y0, x1=x1, y1=y1, u=u, colg=colg: (dd.rectangle([x0, y0, x1 - 1, y1 - 1], fill=tuple(min(255, v + 90) for v in colg) + (int(120 * (1 - u)),)),
                                                                                    dd.rectangle([x0 - 4, y0 - 4, x1 + 3, y1 + 3], outline=colg + (int(230 * (1 - u)),), width=4)))
    if GUM['t'] is None or t < GUM['t']:                                # the STRENGTH gummy on the floor
        bob = 3 * math.sin(t * 4); gx, gy = GUM_POS
        layer(img, lambda dd: [dd.ellipse([gx - 40 + q * 10, gy - 40 + q * 10, gx + 40 - q * 10, gy + 40 - q * 10], fill=STR_COL + (30 + q * 22,)) for q in range(3)])
        img.alpha_composite(GUMI, (int(gx - GUMI.width / 2), int(gy - GUMI.height / 2 + bob)))
    live = []                                                           # trails + live boxes
    for g in G:
        x, y, vx, vy, out, strong = st[g]
        if out is not None and out <= t: continue
        if t >= T_CARD and g == WANT: continue
        if T_GO <= t <= T_WIN:
            for q in range(1, 6):
                s0 = frame_at(max(0, t - q * 0.033))[0][g]
                a_ = 100 - q * 17; s_ = int(HS * (1 - q * 0.1))
                layer(img, lambda dd, px_=s0[0], py_=s0[1], a_=a_, s_=s_, g=g, strong=strong: dd.rectangle([px_ - s_, py_ - s_, px_ + s_, py_ + s_], fill=(STR_COL if strong else COL[g]) + (a_,)))
        live.append(g)
    for g in G:                                                         # caught boxes go under the dark, so its edge visibly covers them
        x, y, vx, vy, out, strong = st[g]
        if out is None or out > t: continue
        u = (t - out) / 0.45
        if u < 1:
            bi = box_img(g, 1 - 0.55 * u, dark=min(1, u * 1.2)); img.alpha_composite(bi, (int(x - bi.width / 2), int(y - bi.height / 2)))
    img.alpha_composite(shadow_layer(t, fr_), (OX, OY))
    for g in G:                                                         # caught: the dark swallows the box, burst, one OUT tag
        x, y, vx, vy, out, strong = st[g]
        if out is None or out > t: continue
        if t - out < 0.3:
            dx_, dy_ = GRAB[g]; u3 = min(1.0, (t - out) / 0.25 + 0.15); n = 2 * HS + 4
            if dy_ < 0: rc = [x - HS - 2, y - HS - 2, x + HS + 2, y - HS - 2 + n * u3]
            elif dy_ > 0: rc = [x - HS - 2, y + HS + 2 - n * u3, x + HS + 2, y + HS + 2]
            elif dx_ < 0: rc = [x - HS - 2, y - HS - 2, x - HS - 2 + n * u3, y + HS + 2]
            else: rc = [x + HS + 2 - n * u3, y - HS - 2, x + HS + 2, y + HS + 2]
            layer(img, lambda dd, rc=rc: (dd.rectangle(rc, fill=(26, 12, 46, 240)), dd.rectangle(rc, outline=(175, 115, 255, 225), width=3)))
        if t - out < 0.45:                                             # capture burst in the guide's colour
            u2 = (t - out) / 0.45; rr = random.Random(hash(g) % 1000)
            pts = [(rr.uniform(0, 6.283), rr.uniform(0.6, 1.0)) for _ in range(14)]
            layer(img, lambda dd, u2=u2, pts=pts, x=x, y=y, g=g: [dd.rectangle([x + (40 + 110 * u2 * sp) * math.cos(a) - 5 + int(3 * u2), y + (40 + 110 * u2 * sp) * math.sin(a) - 5 + int(3 * u2),
                                                                                 x + (40 + 110 * u2 * sp) * math.cos(a) + 5 - int(3 * u2), y + (40 + 110 * u2 * sp) * math.sin(a) + 5 - int(3 * u2)],
                                                                                fill=tuple(min(255, v + 40) for v in COL[g]) + (int(255 * (1 - u2)),)) for a, sp in pts])
        if t - out < 1.1 and t < T_CARD:
            a_ = int(255 * min(1, (1.1 - (t - out)) / 0.25)); ly = y - HS - 46 - 8 * min(1, (t - out) / 0.2)
            if ly < MY0 + 12: ly = y + HS + 10
            text_layer(img, [(clampx(x, 60), ly, 'OUT', 34, (255, 90, 90), 7, a_)])
    for g in live:
        x, y, vx, vy, out, strong = st[g]
        if strong:
            pul = 0.5 + 0.5 * math.sin(t * 14)
            layer(img, lambda dd, x=x, y=y, pul=pul: dd.rectangle([x - HS - 6, y - HS - 6, x + HS + 5, y + HS + 5], outline=STR_COL + (int(140 + 100 * pul),), width=4))
        bs = bounce(f)
        if bs != 1.0:
            bi = BOXI[g].resize((int(2 * HS * bs), int(2 * HS * bs)), Image.NEAREST); img.alpha_composite(bi, (int(x - bi.width / 2), int(y - bi.height / 2)))
        else: img.alpha_composite(BOXI[g], (int(x - HS), int(y - HS)))
    for e in EV:                                                        # bursts: pickup, wall break dust, the STRENGTH smash
        if e[1] == 'pick' and 0 <= t - e[0] < 0.5:
            px_, py_ = frame_at(e[0])[0][e[2]][:2]; u = (t - e[0]) / 0.5
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.rectangle([px_ + (24 + 100 * u) * math.cos(q * 0.785) - 6, py_ + (24 + 100 * u) * math.sin(q * 0.785) - 6, px_ + (24 + 100 * u) * math.cos(q * 0.785) + 6, py_ + (24 + 100 * u) * math.sin(q * 0.785) + 6], fill=STR_COL + (int(255 * (1 - u)),)) for q in range(8)])
        if e[1] == 'break' and 0 <= t - e[0] < 0.4:
            x0, y0, x1, y1 = irect(e[3]); u = (t - e[0]) / 0.4; rr = random.Random(int(e[0] * 1000))
            pts = [(rr.uniform(x0, x1), rr.uniform(y0, y1)) for _ in range(8)]
            layer(img, lambda dd, u=u, pts=pts: [dd.rectangle([px - 8 - 14 * u, py - 8 - 14 * u, px + 8 + 14 * u, py + 8 + 14 * u], fill=(225, 215, 235, int(150 * (1 - u)))) for px, py in pts])
    if SMASH and 0 <= t - SMASH[0] < 0.35:                              # impact flash on Cyrus's STRENGTH smash through the exit
        u = (t - SMASH[0]) / 0.35; x0, y0, x1, y1 = irect('exit'); hx = max(x0, min(x1, BB['exit']['hits'][-1][2])); hy = y1
        layer(img, lambda dd, u=u: (dd.ellipse([hx - 30 - 160 * u, hy - 30 - 160 * u, hx + 30 + 160 * u, hy + 30 + 160 * u], outline=(255, 240, 200, int(255 * (1 - u))), width=int(10 * (1 - u)) + 2),
                                    dd.ellipse([hx - 70 * (1 - u), hy - 70 * (1 - u), hx + 70 * (1 - u), hy + 70 * (1 - u)], fill=(255, 250, 230, int(230 * (1 - u)))),
                                    [dd.line([hx, hy, hx + (60 + 200 * u) * math.cos(a), hy + (60 + 200 * u) * math.sin(a)], fill=(255, 200, 120, int(220 * (1 - u))), width=6) for a in [i * 0.785 + 0.3 for i in range(8)]]))
        if u < 0.3: layer(img, lambda dd, u=u: dd.rectangle([MX0, MY0, MX1, MY1], fill=(255, 245, 225, int(110 * (1 - u / 0.3)))))
    if T_WIN <= t < T_CARD:                                             # first across the line: a ring at the finish
        u = (t - T_WIN) / (T_CARD - T_WIN); wx, wy = WINXY
        layer(img, lambda dd, u=u: dd.rectangle([wx - HS - 6 - 40 * u, wy - HS - 6 - 40 * u, wx + HS + 6 + 40 * u, wy + HS + 6 + 40 * u], outline=(255, 214, 60, int(255 * (1 - u))), width=6))
    for st0, en, (text, col) in SCHED:                                  # the power stamp (one at a time)
        if st0 <= t < en and t < T_CARD:
            u = t - st0; al = int(255 * min(1, (en - t) / 0.2))
            fs_ = min(52, int(800 / len(text))); sc = 1 + 0.15 * max(0, 1 - u / 0.12); fs2 = int(fs_ * sc)
            tw_ = len(text) * fs2; yy = OY + int(7.6 * C)
            layer(img, lambda dd, tw_=tw_, fs2=fs2, al=al, yy=yy: dd.rounded_rectangle([540 - tw_ / 2 - 22, yy - 18, 540 + tw_ / 2 + 22, yy + fs2 + 18], 16, fill=(14, 8, 22, int(230 * al / 255))))
            text_layer(img, [(540, yy, text, fs2, col, 8, al)])
    if t < T_GO + 0.5:                                                  # countdown 3-2-1-GO
        n = 3 - int(t / CD); txt = str(n) if t < T_GO else 'GO!'
        u = (t % CD) / CD if t < T_GO else (t - T_GO) / 0.5
        fs = int((200 if t < T_GO else 160) * (1.2 - 0.2 * min(1, u * 3)))
        text_layer(img, [(540, OY + int(19 * C) - fs // 2, txt, fs, (255, 214, 60) if t < T_GO else (120, 230, 90), 12, int(255 * (1 if t < T_GO else max(0, 1 - u))))])
    roster(img, t)
    if t >= T_CARD:                                                     # winner card: Syeda's victory pose replaces the box
        u = t - T_CARD; a_ = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], fill=(8, 6, 16, int(175 * a_))))
        vf = VIC_W[int(u * 8) % len(VIC_W)]; q = min(1.0, u / 0.25)
        sc = 0.3 + 0.7 * (1 - (1 - q) ** 3)
        vf2 = vf if sc >= 0.999 else vf.resize((max(2, int(vf.width * sc)), max(2, int(vf.height * sc))), Image.NEAREST)
        cxp = WINXY[0] + (540 - WINXY[0]) * q; cyp = WINXY[1] + (POSE_FEET - WINXY[1]) * q
        img.alpha_composite(vf2, (int(cxp - vf2.width / 2), int(cyp - vf2.height * (78 / 92))))
        dh = 0
        if TOSS0 - 0.15 <= t < TOSS0 + 0.1: dh = -int(10 * math.sin((t - TOSS0 + 0.15) / 0.25 * math.pi))     # little hop as it tosses
        img.alpha_composite(DRAGON, (DRX, DRY + dh))                       # the dragon stays lit over the dimmed maze
        if TOSS0 <= t < TOSS1:
            v = (t - TOSS0) / (TOSS1 - TOSS0); sx_, sy_ = DRX + 22, DRY + 40; ex_, ey_ = FIST
            gx_ = sx_ + (ex_ - sx_) * v; gy_ = sy_ + (ey_ - sy_) * v - 150 * math.sin(v * math.pi)
            gi = TOSS_G.rotate(-int(v * 540) // 90 * 90); img.alpha_composite(gi, (int(gx_ - gi.width / 2), int(gy_ - gi.height / 2)))
        if TOSS1 <= t < TOSS1 + 0.4:
            v = (t - TOSS1) / 0.4
            layer(img, lambda dd, v=v: [sparkle(dd, FIST[0] + (10 + 70 * v) * math.cos(a), FIST[1] + (10 + 70 * v) * math.sin(a), 7, int(255 * (1 - v))) for a in [i * 0.785 for i in range(8)]])
        rs = random.Random(int(t * 6))
        layer(img, lambda dd: [sparkle(dd, 540 + rs.uniform(-230, 230), POSE_FEET - rs.uniform(60, 470), rs.choice([4, 6, 8]), int(255 * (0.5 + 0.5 * math.sin(t * 9 + i)))) for i in range(7)])
        text_layer(img, [(540, OY + int(2.2 * C) + (86 - min(86, int(880 / (len(NAME[WANT]) + 6)))) // 2, NAME[WANT] + ' WINS!', min(86, int(880 / (len(NAME[WANT]) + 6))), COL[WANT], 11, int(255 * a_)),
                         (540, POSE_FEET + 56, 'DID YOUR GUIDE WIN?', 34, (255, 255, 255), 7, int(255 * min(1, max(0, u - 0.12) / 0.2)))])
    if SMASH and 0 <= t - SMASH[0] < 0.25:                              # the smash shakes the frame
        a_ = 6 * (1 - (t - SMASH[0]) / 0.25); img = ImageChops.offset(img, int(a_ * math.sin(t * 120)), int(a_ * math.cos(t * 97)))
    img.alpha_composite(HOOK)
    return img
FRAME0 = draw(0) if not EVONLY else None
for f in range(NF):
    t = f / FPS
    if EVONLY: break
    if STILLS and not any(abs(t - x) < 0.5 / FPS for x in STILLS): continue
    if f < int(os.environ.get('FROMF', '0')): continue                  # partial re-render (end card only)
    img = draw(f)
    if t > T_END - XF:                                                  # the tail flows back into frame 0
        img = Image.blend(img, FRAME0, min(1.0, (t - (T_END - XF)) / (XF - 1.5 / FPS)))   # fully frame 0 on the last frame
    if STILLS: img.convert('RGB').save(f'st_{t:.2f}.png')
    else: wr.write(img)
if wr: wr.close()
if STILLS: sys.exit()
out_ev = [(0.0, 'tick_8bit'), (round(CD, 3), 'tick_8bit'), (round(2 * CD, 3), 'tick_8bit'), (T_GO, 'go_8bit')]
last = -9
brk_t = [e[0] for e in EV if e[1] in ('crack', 'break')]
for (th, g, k) in sorted(WH, key=lambda z: z[0]):
    if k is None and th - last > 0.3 and th < T_WIN and all(abs(th - b) > 0.15 for b in brk_t): out_ev.append((round(th, 3), 'reeltick_8bit')); last = th
for e in EV:
    if e[1] == 'crack': out_ev.append((round(e[0], 3), 'exitcrack' if e[3] == 'exit' else 'brick_8bit'))
    elif e[1] == 'break':
        out_ev.append((round(e[0], 3), 'crunch_8bit')); out_ev.append((round(e[0] + 0.02, 3), 'brick_8bit'))
        if SMASH and abs(e[0] - SMASH[0]) < 1e-6 and e[3] == 'exit': out_ev += [(round(e[0], 3), 'boom_short'), (round(e[0], 3), 'punch'), (round(e[0], 3), 'exitcrack')]
    elif e[1] == 'pick': out_ev.append((round(e[0], 3), 'powerup_8bit'))
    elif e[1] == 'out': out_ev.append((round(e[0], 3), 'squish')); out_ev.append((round(e[0] + 0.03, 3), 'buzz_loud'))
out_ev += [(round(T_WIN, 3), 'win_sting'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer'),
           (round(TOSS0, 3), 'whoosh_8bit'), (round(TOSS1, 3), 'powerup_8bit')]
if T_EYES: out_ev += [(round(T_EYES, 3), 'low_sting'), (round(T_EYES, 3), 'low_sting')]          # doubled: +6 dB over the bed
out_ev = sorted(e for e in out_ev if e[0] < T_END - 0.1)
json.dump({'events': out_ev, 'end': T_END, 'beats': {'go': T_GO, 'win': T_WIN, 'card': T_CARD, 'loop': T_END, 'outs': {g: XX[g]['out'] for g in G}, 'gummy': GUM['t']}}, open('n03_events.json', 'w'), indent=1)
print('done', round(T_END, 2), NF)
