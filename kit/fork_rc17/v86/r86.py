import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #86 Which path saves Joy: safe zone + hook + Bennett note "too zoomed out, make it EASIER" (source fork_a9/path/render_path.py)
# maze 15x19 cells of 32px -> 7x8 cells with 64px corridors and 32px walls (zoomed in, findable at phone size)
from collections import deque
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = SP0 + 'fork_a9/gen/'
# #86 follow-up (5:41pm) 'now TOO EASY after the zoom-in, a little harder (middle ground)': 7x8 cells (64px corridors,
# 32px walls) -> 9x10 cells with 56px corridors and 24px walls (90 cells, was 56; original was 15x19 at 32px)
NX, NY = 9, 10; GW, GH = 2 * NX + 1, 2 * NY + 1; CW, WW = 56, 24
def gx(i): return (i // 2) * (CW + WW) + (WW if i % 2 else 0)
def gw(i): return CW if i % 2 else WW
BW, BH = gx(GW - 1) + WW, gx(GH - 1) + WW
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rnd = random.Random(SEED)
open_ = [[False] * GW for _ in range(GH)]
for cy in range(NY):
    for cx in range(NX): open_[2 * cy + 1][2 * cx + 1] = True
seen = {(0, 0)}; st = [(0, 0)]; adj = {}
while st:
    cx, cy = st[-1]; nb = [(cx + dx, cy + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= cx + dx < NX and 0 <= cy + dy < NY and (cx + dx, cy + dy) not in seen]
    if nb:
        n = rnd.choice(nb); seen.add(n); st.append(n)
        open_[cy + n[1] + 1][cx + n[0] + 1] = True
        adj.setdefault((cx, cy), set()).add(n); adj.setdefault(n, set()).add((cx, cy))
    else: st.pop()
CC = (NX // 2, NY // 2)
ENT = {'A': 0, 'B': NX // 2, 'C': NX - 1}
def path(a, b):
    prev = {a: None}; q = deque([a])
    while q:
        u = q.popleft()
        if u == b: break
        for v in adj.get(u, ()):
            if v not in prev: prev[v] = u; q.append(v)
    if b not in prev: return None
    p = [b]
    while prev[p[-1]] is not None: p.append(prev[p[-1]])
    return p[::-1]
paths = {k: path((x, 0), CC) for k, x in ENT.items()}
ans = rnd.choice('ABC'); good = paths[ans]; goodE = set(frozenset(e) for e in zip(good, good[1:]))
for k in 'ABC':
    if k == ans: continue
    p = path((ENT[k], 0), CC)
    if p is None: continue
    cand = [i for i in range(int(len(p) * 0.6), len(p) - 3) if frozenset((p[i], p[i + 1])) not in goodE]
    if not cand: cand = [i for i in range(len(p) - 1) if frozenset((p[i], p[i + 1])) not in goodE]
    if not cand: print('BAD'); sys.exit(1)
    i = rnd.choice(cand); a, b = p[i], p[i + 1]
    adj[a].discard(b); adj[b].discard(a); open_[a[1] + b[1] + 1][a[0] + b[0] + 1] = False
ok = all((path((ENT[k], 0), CC) is not None) == (k == ans) for k in 'ABC')
print('answer', ans, 'ok', ok, 'goodlen', len(good), 'lens', {k: len(paths[k] or []) for k in 'ABC'})
gx0, gy0 = 2 * CC[0] + 1, 2 * CC[1] + 1
for y in range(gy0 - 1, gy0 + 2):
    for x in range(gx0 - 1, gx0 + 2): open_[y][x] = True
for k, x in ENT.items(): open_[0][2 * x + 1] = True
def gridreach(sx):
    q = deque([(0, sx)]); seen = {(0, sx)}
    while q:
        y, x = q.popleft()
        if (y, x) == (gy0, gx0): return True
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < GH and 0 <= xx < GW and open_[yy][xx] and (yy, xx) not in seen: seen.add((yy, xx)); q.append((yy, xx))
    return False
reach = [k for k, x in ENT.items() if gridreach(2 * x + 1)]
print('grid reach', reach)
if not ok or reach != [ans]: print('REJECT'); sys.exit(1)
if len(sys.argv) > 2 and sys.argv[2] == 'check': sys.exit()
# ---- layout
import hook as _hk; _fit0 = _hk._fit
_hk._fit = lambda lines, maxw, hi=80, lo=48: _fit0(lines, maxw, min(hi, 72), lo)   # recut: hook 80 -> 72px to make room for the comment line
HOOK, HB = hook_layer(['WHICH PATH', 'SAVES JOY?'], accent=1, color=(140, 220, 90))
_hk._fit = _fit0
# end title box: same band, "TIME'S UP! / COMMENT A, B OR C" (the maze stays visible, never dimmed)
HOOK_END = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(HOOK_END)
_d.rounded_rectangle([70, 262, 1025, HB], 22, fill=(14, 10, 24, 225), outline=(140, 220, 90), width=6)
ctext(_d, 547, 262 + 34, "TIME'S UP!", F(72), (255, 214, 60), 9, 255, (10, 6, 18)); ctext(_d, 547, 262 + 34 + 72 + 30, 'COMMENT A, B OR C', F(48), (255, 255, 255), 7, 255, (10, 6, 18))
PLY = HB + 8                        # comment line under the hook (from 0.5s)
OX = 478 - BW // 2; OY = HB + 170
print('hook bottom', HB, 'board', OX, OY, OX + BW, OY + BH)
# ---- textures
meta = json.load(open(G + 'sand_meta.json')); sh = Image.open(G + 'sand_sheet.png').convert('RGBA'); TL = meta['tileset_data']['tiles']
def tile(i):
    b = TL[i]['bounding_box']; return sh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
FLOOR, TOP, BRICK = tile(0), tile(6), tile(15)
RIM = (120, 90, 40, 255)
board = Image.new('RGBA', (BW, BH), (0, 0, 0, 255)); bd = ImageDraw.Draw(board)
def op(yy, xx): return 0 <= yy < GH and 0 <= xx < GW and open_[yy][xx]
for y in range(GH):
    for x in range(GW):
        X0, Y0, w, h = gx(x), gx(y), gw(x), gw(y)
        for yy in range(0, h, 32):
            for xx in range(0, w, 32):
                cw_, ch_ = min(32, w - xx), min(32, h - yy)
                if open_[y][x]:
                    t = FLOOR
                    if ((X0 + xx) // 32 + (Y0 + yy) // 32) % 2: t = t.transpose(Image.FLIP_LEFT_RIGHT)
                    board.alpha_composite(t.crop((0, 0, cw_, ch_)), (X0 + xx, Y0 + yy))
                else: board.alpha_composite(TOP.crop((0, 0, cw_, ch_)), (X0 + xx, Y0 + yy))
for y in range(GH):
    for x in range(GW):
        if open_[y][x]: continue
        X0, Y0, w, h = gx(x), gx(y), gw(x), gw(y)
        so = op(y + 1, x)
        if so:
            for xx in range(0, w, 32): board.alpha_composite(BRICK.crop((0, 0, min(32, w - xx), 17)), (X0 + xx, Y0 + h - 17))
        bot = Y0 + h - (17 if so else 0)
        if op(y - 1, x): bd.rectangle([X0, Y0, X0 + w - 1, Y0 + 2], fill=RIM)
        if op(y, x - 1): bd.rectangle([X0, Y0, X0 + 2, bot - 1], fill=RIM)
        if op(y, x + 1): bd.rectangle([X0 + w - 3, Y0, X0 + w - 1, bot - 1], fill=RIM)
JCX, JCY = gx(gx0) + CW // 2, gx(gy0) + CW // 2
bd.ellipse([JCX - 50, JCY - 50, JCX + 50, JCY + 50], outline=(255, 214, 90, 255), width=4)
dead = [(cx, cy) for cx in range(NX) for cy in range(NY) if len(adj.get((cx, cy), ())) == 1 and abs(cx - CC[0]) + abs(cy - CC[1]) > 1 and cy > 0]
rnd.shuffle(dead); GSPOT = [(d, ['mush', 'acv', 'mel', 'cre'][i % 4]) for i, d in enumerate(dead[:8])]
TORCH = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(PL + 'maze/torch_anim/*.png'))]
# torches mounted on horizontal wall faces (wall above an open corridor), never floating
walls_with_face = [(x, y) for y in range(2, GH - 1) for x in range(1, GW - 1, 2) if not open_[y][x] and open_[y + 1][x] and abs(x - gx0) + abs(y - gy0) > 3]
rnd.shuffle(walls_with_face)
gcells = {(2 * cx + 1, 2 * cy + 1) for (cx, cy), k in GSPOT}
TPOS = []
for (x, y) in walls_with_face:   # spread out: never two close together, never hanging over a gummy
    if any(abs(x - X) <= 2 and abs(y + 1 - Y) <= 1 for (X, Y) in gcells): continue
    if any(abs(x - X) + abs(y - Y) < 7 for (X, Y) in TPOS): continue
    TPOS.append((x, y))
    if len(TPOS) == 6: break
print('torches', TPOS)
JOYP = seq(PL + 'maze/anim/joy_panic', 2, 1, 9)        # 1x -> 2x (zoomed in)
GUM = {k: gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre']}
BGF = bg_frames('sun_hd.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.5, blur=3)
DUR = 9.2; T_END = 7.5; T_LOOP = 9.0;   # recut: end hold 1.5s, last 0.2s = opening state
wr = Writer('v86_noaudio.mp4'); ev = []
LBLX = {k: OX + gx(2 * x + 1) + CW // 2 for k, x in ENT.items()}
MEDY = OY - 46; MR = 50                       # A/B/C badges 36 -> 50px radius
for f in range(int(DUR * FPS)):
    t = f / FPS
    if t >= T_LOOP: t = 0.0
    img = BGF[int(t * 6) % len(BGF)].copy()
    layer(img, lambda d: d.rounded_rectangle([OX - 22, OY - 60, OX + BW + 21, OY + BH + 18], 20, fill=(20, 12, 6, 200), outline=(232, 180, 60, 255), width=6))
    b = board.copy()
    for (x, y) in TPOS:
        fr = TORCH[(int(t * 10) + x + y) % len(TORCH)]; b.alpha_composite(fr, (gx(x) + gw(x) // 2 - fr.width // 2, gx(y) + gw(y) + 6 - 62))   # sconce on the brick face
    for (cx, cy), k in GSPOT:
        g = GUM[k]; bob = int(3 * math.sin(t * 4 + cx + cy))
        b.alpha_composite(g, (gx(2 * cx + 1) + CW // 2 - g.width // 2, gx(2 * cy + 1) + CW // 2 - g.height // 2 + bob))
    img.alpha_composite(b, (OX, OY))
    def glow(d):
        p = 0.5 + 0.5 * math.sin(t * 4)
        d.ellipse([OX + JCX - 64, OY + JCY - 64, OX + JCX + 64, OY + JCY + 64], fill=(255, 220, 120, int(30 + 30 * p)))
        for k, x in LBLX.items():
            d.ellipse([x - MR, MEDY - MR, x + MR, MEDY + MR], fill=(232, 180, 60, 255), outline=(60, 30, 10, 255), width=6)
    layer(img, glow)
    jf = JOYP[int(t * 10) % len(JOYP)]
    img.alpha_composite(jf, (OX + JCX - jf.width // 2, OY + JCY + 40 - 78 * 2))   # Joy 2x stands in the centre room (feet on its floor)
    items = [(x, MEDY - 27, k, 56, (60, 30, 10), 0, 255) for k, x in LBLX.items()]
    if int(t * 2) % 2 == 0: items.append((OX + JCX, OY + JCY - 150, 'HELP!', 44, (255, 255, 255), 7, 255))
    text_layer(img, items)
    rem = max(0, T_END - t)
    def bar(d):   # recut: vertical timer right of the maze, 50px wide (was an 18px-tall strip), red pulse in the last 2s
        x0, x1, y0, y1 = 892, 944, OY, OY + 430
        pulse = rem <= 2.0 and rem > 0 and int(rem * 6) % 2 == 0
        d.rounded_rectangle([x0, y0, x1, y1], 14, fill=(20, 12, 30, 225), outline=(255, 255, 255, 255) if pulse else (232, 180, 60, 255), width=5)
        fy = y1 - 7 - (y1 - y0 - 14) * rem / T_END
        col = (140, 220, 90, 255) if rem > 3.5 else ((255, 170, 60, 255) if rem > 2.0 else ((255, 60, 50, 255) if pulse else (200, 40, 40, 255)))
        if rem > 0.02: d.rounded_rectangle([x0 + 7, fy, x1 - 7, y1 - 7], 10, fill=col)
    if t < T_END: layer(img, bar)
    if t < T_END:
        if f < int(T_LOOP * FPS):
            for k in (3, 2, 1):
                if abs((T_END - t) - k) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
        a = int(255 * min(1, max(0, (t - 0.5) / 0.2)))
        if a > 0:
            layer(img, lambda d: d.rounded_rectangle([86, PLY, 870, PLY + 62], 16, fill=(14, 10, 24, int(a * 0.9)), outline=(255, 214, 60, a), width=4))
            text_layer(img, [(478, PLY + 9, 'COMMENT A, B OR C', 44, (255, 255, 255), 7, a)])
    else:
        if not any(e[1] == 'buzz_8bit' for e in ev): ev.append((round(T_END, 3), 'buzz_8bit'))
    img.alpha_composite(HOOK_END if t >= T_END else HOOK)
    wr.write(img)
    if f in (0, 60, 200, 240, 275): img.convert('RGB').save(f'f86_{f}.png')
wr.close(); json.dump({'events': ev}, open('v86_ev.json', 'w')); print('done', ev)
