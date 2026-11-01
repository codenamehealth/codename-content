import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #86 Which path saves Joy: safe zone + hook + Bennett note "too zoomed out, make it EASIER" (source fork_a9/path/render_path.py)
# maze 15x19 cells of 32px -> 7x8 cells with 64px corridors and 32px walls (zoomed in, findable at phone size)
from collections import deque
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = SP0 + 'fork_a9/gen/'
NX, NY = 7, 8; GW, GH = 2 * NX + 1, 2 * NY + 1
def gx(i): return (i // 2) * 96 + (32 if i % 2 else 0)
def gw(i): return 64 if i % 2 else 32
BW, BH = gx(GW - 1) + 32, gx(GH - 1) + 32
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
HOOK, HB = hook_layer(['WHICH PATH', 'SAVES JOY?'], accent=1, color=(140, 220, 90))
BARY = HB + 14                      # timer bar under the hook
OX = 478 - BW // 2; OY = BARY + 34 + 100
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
                if open_[y][x]:
                    t = FLOOR
                    if ((X0 + xx) // 32 + (Y0 + yy) // 32) % 2: t = t.transpose(Image.FLIP_LEFT_RIGHT)
                    board.alpha_composite(t, (X0 + xx, Y0 + yy))
                else: board.alpha_composite(TOP, (X0 + xx, Y0 + yy))
for y in range(GH):
    for x in range(GW):
        if open_[y][x]: continue
        X0, Y0, w, h = gx(x), gx(y), gw(x), gw(y)
        so = op(y + 1, x)
        if so:
            for xx in range(0, w, 32): board.alpha_composite(BRICK.crop((0, 0, 32, 23)), (X0 + xx, Y0 + h - 23))
        bot = Y0 + h - (23 if so else 0)
        if op(y - 1, x): bd.rectangle([X0, Y0, X0 + w - 1, Y0 + 2], fill=RIM)
        if op(y, x - 1): bd.rectangle([X0, Y0, X0 + 2, bot - 1], fill=RIM)
        if op(y, x + 1): bd.rectangle([X0 + w - 3, Y0, X0 + w - 1, bot - 1], fill=RIM)
JCX, JCY = gx(gx0) + 32, gx(gy0) + 32
bd.ellipse([JCX - 62, JCY - 62, JCX + 62, JCY + 62], outline=(255, 214, 90, 255), width=4)
dead = [(cx, cy) for cx in range(NX) for cy in range(NY) if len(adj.get((cx, cy), ())) == 1 and abs(cx - CC[0]) + abs(cy - CC[1]) > 1 and cy > 0]
rnd.shuffle(dead); GSPOT = [(d, ['mush', 'acv', 'mel', 'cre'][i % 4]) for i, d in enumerate(dead[:8])]
TORCH = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(PL + 'maze/torch_anim/*.png'))]
# torches mounted on horizontal wall faces (wall above an open corridor), never floating
walls_with_face = [(x, y) for y in range(2, GH - 1) for x in range(1, GW - 1, 2) if not open_[y][x] and open_[y + 1][x] and abs(x - gx0) + abs(y - gy0) > 3]
rnd.shuffle(walls_with_face); TPOS = walls_with_face[:6]
JOYP = seq(PL + 'maze/anim/joy_panic', 2, 1, 9)        # 1x -> 2x (zoomed in)
GUM = {k: gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre']}
BGF = bg_frames('sun_hd.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.5, blur=3)
DUR = 10.0; T_END = 7.5; wr = Writer('v86_noaudio.mp4'); ev = []
LBLX = {k: OX + gx(2 * x + 1) + 32 for k, x in ENT.items()}
MEDY = OY - 70
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BGF[int(t * 6) % len(BGF)].copy()
    layer(img, lambda d: d.rounded_rectangle([OX - 22, OY - 100, OX + BW + 21, OY + BH + 21], 20, fill=(20, 12, 6, 200), outline=(232, 180, 60, 255), width=6))
    b = board.copy()
    for (x, y) in TPOS:
        fr = TORCH[(int(t * 10) + x + y) % len(TORCH)]; b.alpha_composite(fr, (gx(x) + 32 - fr.width // 2, gx(y) + 32 - 62 + 4))
    for (cx, cy), k in GSPOT:
        g = GUM[k]; bob = int(3 * math.sin(t * 4 + cx + cy))
        b.alpha_composite(g, (gx(2 * cx + 1) + 32 - g.width // 2, gx(2 * cy + 1) + 32 - g.height // 2 + bob))
    img.alpha_composite(b, (OX, OY))
    def glow(d):
        p = 0.5 + 0.5 * math.sin(t * 4)
        d.ellipse([OX + JCX - 80, OY + JCY - 80, OX + JCX + 80, OY + JCY + 80], fill=(255, 220, 120, int(30 + 30 * p)))
        for k, x in LBLX.items():
            d.ellipse([x - 36, MEDY - 36, x + 36, MEDY + 36], fill=(232, 180, 60, 255), outline=(60, 30, 10, 255), width=5)
    layer(img, glow)
    jf = JOYP[int(t * 10) % len(JOYP)]
    img.alpha_composite(jf, (OX + JCX - jf.width // 2, OY + JCY + 30 - 78 * 2 + 20))   # Joy 2x stands in the centre room
    items = [(x, MEDY - 20, k, 40, (60, 30, 10), 0, 255) for k, x in LBLX.items()]
    if int(t * 2) % 2 == 0: items.append((OX + JCX, OY + JCY - 150, 'HELP!', 30, (255, 255, 255), 6, 255))
    text_layer(img, items)
    rem = max(0, T_END - t)
    def bar(d):
        x0, x1, y = OX - 22, OX + BW + 21, BARY
        d.rounded_rectangle([x0, y, x1, y + 34], 12, fill=(20, 12, 30, 225), outline=(232, 180, 60, 255), width=4)
        fx = x0 + 6 + (x1 - x0 - 12) * rem / T_END
        if rem > 0: d.rounded_rectangle([x0 + 6, y + 6, fx, y + 28], 8, fill=(140, 220, 90, 255) if rem > 2.5 else (255, 120, 80, 255))
    layer(img, bar)
    if t < T_END:
        if f % 30 == 0 and t > 0.2: ev.append((round(t, 3), 'tick_8bit'))
    else:
        u = t - T_END
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 14, int(150 * min(1, u / 0.3)))))
        layer(img, lambda d: d.rounded_rectangle([OX - 10, 820, OX + BW + 9, 1080], 22, fill=(14, 10, 24, 230), outline=(255, 214, 60, 255), width=6))
        text_layer(img, [(478, 860, "TIME'S UP!", 76, (255, 214, 60), 9, 255), (478, 980, 'Comment A, B or C', 40, (255, 255, 255), 7, 255)])
        if not any(e[1] == 'buzz_8bit' for e in ev): ev.append((round(T_END, 3), 'buzz_8bit'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (60, 200, 270): img.convert('RGB').save(f'f86_{f}.png')
wr.close(); json.dump(ev, open('v86_ev.json', 'w')); print('done', ev)
