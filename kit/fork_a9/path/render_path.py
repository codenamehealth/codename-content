import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
from collections import deque
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = '../gen/'
NX, NY = 15, 19; GW, GH = 2 * NX + 1, 2 * NY + 1; C = 32
OX = (W - GW * C) // 2; OY = 430
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rnd = random.Random(SEED)
# perfect maze on cells (cx, cy) -> grid (2cx+1, 2cy+1)
open_ = [[False] * GW for _ in range(GH)]
for cy in range(NY):
    for cx in range(NX): open_[2 * cy + 1][2 * cx + 1] = True
seen = {(0, 0)}; st = [(0, 0)]; edges = {}
adj = {}
while st:
    cx, cy = st[-1]; nb = [(cx + dx, cy + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= cx + dx < NX and 0 <= cy + dy < NY and (cx + dx, cy + dy) not in seen]
    if nb:
        n = rnd.choice(nb); seen.add(n); st.append(n)
        open_[cy + n[1] + 1][cx + n[0] + 1] = True
        adj.setdefault((cx, cy), set()).add(n); adj.setdefault(n, set()).add((cx, cy))
    else: st.pop()
CC = (NX // 2, NY // 2)
ENT = {'A': 2, 'B': NX // 2, 'C': NX - 3}
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
    if not cand: print('BAD'); sys.exit()
    i = rnd.choice(cand); a, b = p[i], p[i + 1]
    adj[a].discard(b); adj[b].discard(a); open_[a[1] + b[1] + 1][a[0] + b[0] + 1] = False
ok = all((path((ENT[k], 0), CC) is not None) == (k == ans) for k in 'ABC')
wl = {k: len(path((ENT[k], 0), CC) or []) for k in 'ABC'}
print('answer', ans, 'ok', ok, 'goodlen', len(good), 'onlygood', [k for k in 'ABC' if path((ENT[k],0),CC)])
# center room 3x3 grid cells and entrance openings in top wall
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
if len(sys.argv) > 2 and sys.argv[2] == 'check': sys.exit()
# ---- textures
meta = json.load(open(G + 'sand_meta.json')); sh = Image.open(G + 'sand_sheet.png').convert('RGBA'); TL = meta['tileset_data']['tiles']
def tile(i):
    b = TL[i]['bounding_box']; return sh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32))
FLOOR, TOP, BRICK = tile(0), tile(6), tile(15)
RIM = (120, 90, 40, 255)
board = Image.new('RGBA', (GW * C, GH * C), (0, 0, 0, 255)); bd = ImageDraw.Draw(board)
for y in range(GH):
    for x in range(GW):
        if open_[y][x]:
            t = FLOOR
            if (x + y) % 2: t = t.transpose(Image.FLIP_LEFT_RIGHT)
            board.alpha_composite(t, (x * C, y * C))
for y in range(GH):
    for x in range(GW):
        if open_[y][x]: continue
        board.alpha_composite(TOP, (x * C, y * C))
        so = y + 1 < GH and open_[y + 1][x]
        if so: board.alpha_composite(BRICK.crop((0, 0, C, 23)), (x * C, y * C + C - 23))
        def op(yy, xx): return 0 <= yy < GH and 0 <= xx < GW and open_[yy][xx]
        bot = y * C + C - (23 if so else 0)
        if op(y - 1, x): bd.rectangle([x * C, y * C, x * C + C - 1, y * C + 2], fill=RIM)
        if op(y, x - 1): bd.rectangle([x * C, y * C, x * C + 2, bot - 1], fill=RIM)
        if op(y, x + 1): bd.rectangle([x * C + C - 3, y * C, x * C + C - 1, bot - 1], fill=RIM)
# rune circle in the center room
bd.ellipse([gx0 * C - 40 + C // 2, gy0 * C - 40 + C // 2, gx0 * C + 40 + C // 2, gy0 * C + 40 + C // 2], outline=(255, 214, 90, 255), width=3)
# dead ends -> gummies
dead = [(cx, cy) for (cx, cy) in [(a, b) for a in range(NX) for b in range(NY)] if len(adj.get((cx, cy), ())) == 1 and abs(cx - CC[0]) + abs(cy - CC[1]) > 2 and cy > 0]
rnd.shuffle(dead); GSPOT = [(d, rnd.choice(['mush', 'acv', 'mel', 'cre'])) for d in dead[:14]]
TORCH = [up(Image.open(p).convert('RGBA'), 1) for p in sorted(glob.glob(PL + 'maze/torch_anim/*.png'))]
walls_with_face = [(x, y) for y in range(2, GH - 1) for x in range(1, GW - 1) if not open_[y][x] and open_[y + 1][x] and not open_[y][x - 1] and not open_[y][x + 1]]
rnd.shuffle(walls_with_face); TPOS = walls_with_face[:10]
JOYP = seq(PL + 'maze/anim/joy_panic', 1, 1, 9)
GUM = {k: gummy(k, 1) for k in ['mush', 'acv', 'mel', 'cre']}
BGF = bg_frames('sun_hd.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.5, blur=3)
DUR = 10.0; T_END = 7.5; wr = Writer('path_noaudio.mp4'); ev = []
LBLX = {k: OX + (2 * x + 1) * C + C // 2 for k, x in ENT.items()}
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BGF[int(t * 6) % len(BGF)].copy()
    layer(img, lambda d: d.rounded_rectangle([OX - 22, OY - 90, OX + GW * C + 21, OY + GH * C + 21], 20, fill=(20, 12, 6, 200), outline=(232, 180, 60, 255), width=6))
    b = board.copy()
    for (x, y) in TPOS:
        fr = TORCH[(int(t * 10) + x + y) % len(TORCH)]; b.alpha_composite(fr, (x * C + C // 2 - fr.width // 2, y * C + C - fr.height - 8))
    for (cx, cy), k in GSPOT:
        g = GUM[k]; bob = int(2 * math.sin(t * 4 + cx + cy))
        b.alpha_composite(g, ((2 * cx + 1) * C + C // 2 - g.width // 2, (2 * cy + 1) * C + C // 2 - g.height // 2 + bob))
    jf = JOYP[int(t * 10) % len(JOYP)]
    b.alpha_composite(jf, (gx0 * C + C // 2 - jf.width // 2, gy0 * C + C // 2 + 20 - 78))
    img.alpha_composite(b, (OX, OY))
    def glow(d):
        p = 0.5 + 0.5 * math.sin(t * 4)
        d.ellipse([OX + gx0 * C + C // 2 - 70, OY + gy0 * C + C // 2 - 70, OX + gx0 * C + C // 2 + 70, OY + gy0 * C + C // 2 + 70], fill=(255, 220, 120, int(30 + 30 * p)))
        for k, x in LBLX.items():
            d.ellipse([x - 30, OY - 78, x + 30, OY - 18], fill=(232, 180, 60, 255), outline=(60, 30, 10, 255), width=4)
    layer(img, glow)
    items = [(x, OY - 64, k, 32, (60, 30, 10), 0, 255) for k, x in LBLX.items()]
    items += [(W / 2, 90, 'WHICH PATH', 76, (255, 255, 255), 8, 255), (W / 2, 190, 'SAVES JOY?', 76, (140, 220, 90), 8, 255)]
    hp = 'HELP!' if int(t * 2) % 2 == 0 else ''
    if hp: items.append((OX + gx0 * C + C // 2, OY + gy0 * C - 70, hp, 22, (255, 255, 255), 5, 255))
    # timer bar
    rem = max(0, T_END - t)
    text_layer(img, items)
    def bar(d):
        x0, x1, y = 90, W - 90, OY + GH * C + 70
        d.rounded_rectangle([x0, y, x1, y + 34], 12, fill=(20, 12, 30, 220), outline=(232, 180, 60, 255), width=4)
        fx = x0 + 6 + (x1 - x0 - 12) * rem / T_END
        if rem > 0: d.rounded_rectangle([x0 + 6, y + 6, fx, y + 28], 8, fill=(140, 220, 90, 255) if rem > 2.5 else (255, 120, 80, 255))
    layer(img, bar)
    if t < T_END:
        text_layer(img, [(W / 2, OY + GH * C + 130, 'A, B OR C?', 52, (255, 214, 60), 7, 255)])
        if f % 30 == 0 and t > 0.2: ev.append((round(t, 3), 'tick_8bit'))
    else:
        u = t - T_END
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 14, int(140 * min(1, u / 0.3)))))
        text_layer(img, [(W / 2, 880, "TIME'S UP!", 80, (255, 214, 60), 9, 255), (W / 2, 1010, 'Comment A, B or C', 44, (255, 255, 255), 7, 255)])
        if not any(e[1] == 'buzz_8bit' for e in ev): ev.append((round(T_END, 3), 'buzz_8bit'))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('path_ev.json', 'w')); print('done')
