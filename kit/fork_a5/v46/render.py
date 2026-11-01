import sys, math, json, random, heapq
sys.path.insert(0, '../../fork1'); from common import *
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
C = 64; NR, NC = 20, 45                      # corner grid (tiles 19 x 44)
BW, BH = (NC - 1) * C, (NR - 1) * C
BY = 560                                     # board top on screen
FIN_X = 42.3 * C
def make_map(seed):
    rnd = random.Random(seed)
    cg = np.ones((NR, NC), np.uint8)
    cg[0, :] = 0; cg[NR - 1, :] = 0; cg[:, 0] = 0
    props = set()
    for bc in (6, 11, 16, 21, 26, 31, 36):
        cg[1:NR - 1, bc] = 0
        ngap = rnd.choice([2, 3])
        rows = sorted(rnd.sample(range(2, NR - 4), ngap))
        last = -9
        for r0 in rows:
            if r0 - last < 5: r0 = min(NR - 4, last + 5)
            cg[r0:r0 + 3, bc] = 1; last = r0
    for bc in (8, 13, 18, 23, 28, 33):          # short horizontal stubs
        r = rnd.randrange(4, NR - 5); cg[r, bc:bc + 2] = 0
    for _ in range(26):
        r, c = rnd.randrange(2, NR - 2), rnd.randrange(3, 40)
        if cg[r, c] and all(cg[r + dr, c + dc] for dr in (-1, 0, 1) for dc in (-1, 0, 1)) and (r, c) not in props:
            props.add((r, c))
    return cg, props
MSEED = int(os.environ.get('MSEED', '3'))
CG, PROPS = make_map(MSEED)
def cpt(x, y): return int(round(y / C)), int(round(x / C))
def grass_at(x, y):
    r, c = cpt(x, y)
    if r < 0 or r >= NR or c < 0: return True
    if c >= NC: return False
    return CG[r, c] == 0
def prop_at(x, y): return cpt(x, y) in PROPS
FINE = 4; FC = C // FINE; GR, GCn = BH // FC, BW // FC
pas = np.zeros((GR, GCn), bool)
for i in range(GR):
    for j in range(GCn):
        x, y = (j + 0.5) * FC, (i + 0.5) * FC
        pas[i, j] = not grass_at(x, y) and not prop_at(x, y)
def dijk(starts):
    d = np.full((GR, GCn), np.inf); h = []
    for p in starts: d[p] = 0; heapq.heappush(h, (0.0, p))
    while h:
        dist, (a, b) = heapq.heappop(h)
        if dist > d[a, b]: continue
        for da, db, w in ((1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)):
            na, nb = a + da, b + db
            if 0 <= na < GR and 0 <= nb < GCn and pas[na, nb]:
                if da and db and not (pas[a + da, b] and pas[a, b + db]): continue
                nd = dist + w
                if nd < d[na, nb]: d[na, nb] = nd; heapq.heappush(h, (nd, (na, nb)))
    return d
DEX = dijk([(i, j) for i in range(GR) for j in range(GCn) if pas[i, j] and (j + 0.5) * FC > FIN_X + 40])
GY, GX = np.gradient(np.where(np.isinf(DEX), 9999, DEX))
NAMES = ['cyrus', 'joy', 'ray', 'cleo']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
START_R = [3, 7, 12, 16]
BOOSTS = []
for (r, c) in [(9, 14), (5, 24), (14, 29), (10, 34), (3, 19), (15, 9)]:
    if CG[r, c] and (r, c) not in PROPS: BOOSTS.append((c * C, r * C))
BOOST_T, BOOST_K = 2.4, 1.55
R = 22; SL = 0.5; T_START = 2.4
def sim(seed, dur=22.0):
    rnd = random.Random(seed); order = NAMES[:]; rnd.shuffle(order)
    rc = {}
    for i, n in enumerate(order):
        rc[n] = dict(x=1.4 * C, y=START_R[i] * C, vx=0.0, vy=0.0, base=rnd.uniform(255, 290), ph=rnd.uniform(0, 6.3), out=None, mode='side',
                     slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, dist=0.0)
    taken = {}; frames = []; leaders = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        for n, s in rc.items():
            if s['out'] is not None or t < T_START: continue
            sliding = t - s['slide'] < SL or (s['slide'] > 0 and prop_at(s['x'], s['y']))
            sp = s['base'] * (1 + 0.28 * math.sin(0.8 * t + s['ph']) + 0.15 * math.sin(2.1 * t + 2 * s['ph']))
            if s['boost'] is not None and t - s['boost'] < BOOST_T: sp *= BOOST_K
            if sliding:
                sp *= 1.2; s['vx'] += (s['sdx'] * sp - s['vx']) * 0.3; s['vy'] += (s['sdy'] * sp - s['vy']) * 0.3
            else:
                a, b = min(GR - 1, max(0, int(s['y'] // FC))), min(GCn - 1, max(0, int(s['x'] // FC)))
                gx, gy = -GX[a, b], -GY[a, b]; L = math.hypot(gx, gy) or 1
                wob = 0.4 * math.sin(3.3 * t + s['ph'] * 3); dx, dy = gx / L, gy / L
                tx, ty = dx - dy * wob, dy + dx * wob
                s['vx'] += (tx * sp - s['vx']) * 0.12; s['vy'] += (ty * sp - s['vy']) * 0.12
            v = math.hypot(s['vx'], s['vy']) or 1
            if not sliding and t - s['slide'] > 1.0 and t > T_START + 0.6:
                ux, uy = s['vx'] / v, s['vy'] / v
                if any(prop_at(s['x'] + ux * d, s['y'] + uy * d) for d in (R + 10, R + 26)):
                    s['slide'] = t; s['sdx'], s['sdy'] = ux, uy; sliding = True
            nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
            for _ in range(2):
                for ax, ay in ((R, 0), (-R, 0), (0, R), (0, -R), (R * .7, R * .7), (-R * .7, R * .7), (R * .7, -R * .7), (-R * .7, -R * .7)):
                    if grass_at(nx + ax, ny + ay) or (not sliding and prop_at(nx + ax, ny + ay)):
                        if ax: nx -= ax * 0.18; s['vx'] *= -0.4
                        if ay: ny -= ay * 0.18; s['vy'] *= -0.4
            s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
            for m, o in rc.items():
                if m == n or o['out'] is not None: continue
                if sliding or t - o['slide'] < SL: continue
                ddx, ddy = s['x'] - o['x'], (s['y'] - o['y']) * 1.6; dd = math.hypot(ddx, ddy)
                if 0 < dd < 2 * R + 8:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and t - s['slide'] > 1.0 and t > T_START + 0.6:
                        s['slide'] = t; s['sdx'], s['sdy'] = s['vx'] / v, s['vy'] / v; sliding = True; continue
                    push = (2 * R + 8 - dd) / 2; s['x'] += ddx / dd * push * 0.8; s['y'] += ddy / dd * push * 0.5
            s['mode'] = 'down' if s['vy'] > 0.72 * v else 'side'; s['sliding'] = sliding
            for k, (bx, by) in enumerate(BOOSTS):
                if k not in taken and math.hypot(s['x'] - bx, s['y'] - by) < 46: taken[k] = (n, t); s['boost'] = t
            if s['x'] > FIN_X: s['out'] = t
        def prog(s):
            if s['out'] is not None: return -1e6 + s['out']
            a, b = min(GR - 1, max(0, int(s['y'] // FC))), min(GCn - 1, max(0, int(s['x'] // FC)))
            return DEX[a, b] if not np.isinf(DEX[a, b]) else 1e5
        rank = sorted(rc, key=lambda n: prog(rc[n]))
        if t > T_START + 1 and (not leaders or leaders[-1] != rank[0]): leaders.append(rank[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], out=s['out'], mode=s['mode'], slide=s['slide'], sliding=s['sliding'],
                                boost=s['boost'], dist=s['dist']) for n, s in rc.items()}, rank, dict(taken)))
        if all(s['out'] is not None for s in rc.values()): break
    return rc, frames, leaders
def score(seed):
    rc, fr, ld = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    if len(outs) < 3: return None
    t1, w = outs[0]; t2 = outs[1][0]
    if not (10.5 < t1 < 13.5) or t2 - t1 > 0.7 or len(ld) < 4: return None
    return round(t1, 2), w, round(t2 - t1, 2), len(ld), ld
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
if len(sys.argv) > 1 and sys.argv[1] == 'map':
    im = Image.new('RGB', (NC, NR)); px = im.load()
    for r in range(NR):
        for c in range(NC): px[c, r] = (200, 180, 120) if CG[r, c] else (40, 120, 40)
    for (r, c) in PROPS: px[c, r] = (120, 60, 20)
    im.resize((NC * 12, NR * 12), Image.NEAREST).save('map.png'); sys.exit()
SEED = int(sys.argv[1])
RC, FR, LD = sim(SEED)
OUTS = sorted((s['out'], n) for n, s in RC.items() if s['out'] is not None)
T_WIN, WIN = OUTS[0]
print('winner', WIN, round(T_WIN, 2), 'order', [(n, round(t, 2)) for t, n in OUTS], 'leaders', LD)
# ---------------- art
meta = json.load(open('../../pixellab/steal/plaza_meta.json')); sheet_ = Image.open('../../pixellab/steal/plaza_sheet.png').convert('RGBA')
TILE = {}
for tt in meta['tileset_data']['tiles']:
    cc = tt['corners']; key = tuple(cc[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = tt['bounding_box']
    TILE[key] = up(sheet_.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
BOARD = Image.new('RGBA', (BW + 600, BH), (40, 90, 40, 255))
for j in range(NR - 1):
    for i in range(NC - 1):
        key = (bool(CG[j, i]), bool(CG[j, i + 1]), bool(CG[j + 1, i]), bool(CG[j + 1, i + 1]))
        tl = TILE[key]
        if all(key) or not any(key):
            if (i + j) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
            if (i * 3 + j) % 3 == 0: tl = tl.transpose(Image.FLIP_TOP_BOTTOM)
        BOARD.alpha_composite(tl, (i * C, j * C))
for i in range(NC - 1, (BW + 600) // C + 1):           # cobble run-out past the finish
    for j in range(NR - 1):
        key = (True, True, True, True) if 0 < j < NR - 2 else ((j > 0), (j > 0), (j < NR - 2), (j < NR - 2))
        BOARD.alpha_composite(TILE[key], (i * C, j * C))
def pick(d, i): return crop(Image.open(f'../../pixellab/steal/{d}/{i:02d}.png').convert('RGBA'))
PROPIM = [up(pick('barrel', 0), 3), up(pick('crate', 1), 3), up(pick('flowers', 1), 3), up(pick('barrel', 4), 3), up(pick('crate', 7), 3)]
rr = random.Random(7)
# flower pots and crates decorating the grass walls
DECO = []
for r in range(NR):
    for c in range(1, NC - 1):
        if CG[r, c] == 0 and rr.random() < 0.06 and 0 < r < NR - 1: DECO.append((c * C, r * C, up(pick('flowers', rr.choice([1, 4, 7, 12])), 2)))
PROPL = [(c * C, r * C, PROPIM[(r * 7 + c) % len(PROPIM)]) for (r, c) in sorted(PROPS)]
# finish line
FL = Image.new('RGBA', (48, BH), (0, 0, 0, 0)); fd = ImageDraw.Draw(FL)
for yy in range(0, BH, 24):
    for xx in range(0, 48, 24): fd.rectangle([xx, yy, xx + 23, yy + 23], fill=(245, 245, 245, 255) if (xx // 24 + yy // 24) % 2 else (25, 25, 30, 255))
BOARD.alpha_composite(FL, (int(FIN_X), 0))
for x, y, im in DECO: BOARD.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
SS = 2; FOOT = 78 * SS
def seqa(d, lo=1, hi=9): return [up(Image.open(p).convert('RGBA'), SS) for p in sorted(glob.glob(d + '/*.png'))[lo:hi]]
SRUN = {g: seqa(f'../../pixellab/race/{g}_run') for g in NAMES}
FRUN = {g: seqa(f'../../pixellab/maze/anim/{g}_frun') for g in NAMES}
SLIDE = {g: seqa(f'../../pixellab/maze/anim/{g}_slide', 1, 8) for g in NAMES}
STAND = {g: idle(g, 2) for g in NAMES}
FL_ = lambda L: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in L]
SRUNL = {g: FL_(v) for g, v in SRUN.items()}; SLIDEL = {g: FL_(v) for g, v in SLIDE.items()}
GUMB = gummy('mush', 3)
SMALL = [gummy(k, 1) for k in ('acv', 'cre', 'mel', 'mush')]
ICS = {}
# cosmetic gummy trail along corridor centers
TRAIL = []
for r in (5, 9, 13):
    for c in range(3, 42, 2):
        if CG[r, c] and (r, c) not in PROPS and all((c * C - bx) ** 2 + (r * C - by) ** 2 > 90 ** 2 for bx, by in BOOSTS): TRAIL.append((c * C, r * C, (r + c) % 4))
trail_gone = {}
for f, (st, rank, taken) in enumerate(FR):
    for k, (x, y, _) in enumerate(TRAIL):
        if k in trail_gone: continue
        for n, s in st.items():
            if abs(s['x'] - x) < 34 and abs(s['y'] - y) < 40: trail_gone[k] = f / FPS; break
ICON = {}
SRCF = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
def face(name, rad):
    im = Image.open('../../syeda_src/' + SRCF[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), m); return b
ICON = {n: face(n, 40) for n in NAMES}
HUB = bg_frames('hub.gif', (W, 540), box=(0, 120, 1920, 120 + 960), step=2, bright=0.6)
HUBP = bg_frames('hub.gif', (W, H), box=(420, 0, 420 + 1080, 1920 * 1080 // 1920 * 1), step=2, bright=0.75) if False else None
hubp_src = bg_frames('hub.gif', (int(1920 * H / 1080), H), step=4, bright=0.72)
HUBP = [h.crop(((h.width - W) // 2, 0, (h.width - W) // 2 + W, H)) for h in hubp_src]
PED = crop(Image.open('../../fork2/pedestal/00.png').convert('RGBA'))
VICF = vic(WIN, 330)
DUR_RACE = T_WIN + 1.2; T_POD = DUR_RACE; DUR = T_POD + 4.0; NF = int(DUR * FPS)
wr = Writer('v46_noaudio.mp4'); ev = []; camx = 0.0; ghosts = {n: [] for n in NAMES}
seen_boost = set(); seen_slide = set(); fin_seen = set(); prev_rank = None; rank_pos = {n: float(i) for i, n in enumerate(NAMES)}
for f in range(NF):
    t = f / FPS
    st, rank, taken = FR[min(f, len(FR) - 1)]
    if t < T_POD:
        lead_x = max(s['x'] for s in st.values())
        target = min(max(lead_x - 640, 0), BW + 600 - W)
        camx += (target - camx) * 0.12 if t > T_START else 0
        view = BOARD.crop((int(camx), 0, int(camx) + W, BH)).copy()
        d = ImageDraw.Draw(view)
        # trail gummies
        for k, (x, y, kind) in enumerate(TRAIL):
            if k in trail_gone and t >= trail_gone[k]:
                u = t - trail_gone[k]
                if u < 0.35:
                    for q in range(5):
                        a = q * 1.256; rr_ = 10 + 60 * u
                        d.rectangle([x - camx + rr_ * math.cos(a) - 3, y - 14 + rr_ * math.sin(a) - 3, x - camx + rr_ * math.cos(a) + 3, y - 14 + rr_ * math.sin(a) + 3], fill=(255, 245, 190))
                continue
            g = SMALL[kind]; bob = int(4 * math.sin(t * 5 + k))
            if -60 < x - camx < W + 60: view.alpha_composite(g, (int(x - camx - g.width / 2), int(y - g.height / 2 - 10 + bob)))
        # boost gummies
        for k, (bx, by) in enumerate(BOOSTS):
            sx = bx - camx
            if not (-100 < sx < W + 100): continue
            if k in taken and t >= taken[k][1]:
                u = t - taken[k][1]
                if u < 0.6:
                    layer(view, lambda dd: [dd.rectangle([sx + (20 + 100 * u) * math.cos(q * 0.628) - 5, by - 20 + (20 + 100 * u) * math.sin(q * 0.628) - 5,
                                                         sx + (20 + 100 * u) * math.cos(q * 0.628) + 5, by - 20 + (20 + 100 * u) * math.sin(q * 0.628) + 5], fill=(255, 210, 120, int(255 * (1 - u / 0.6)))) for q in range(10)])
                continue
            bob = int(7 * math.sin(t * 4 + k))
            layer(view, lambda dd: [dd.ellipse([sx - rr_, by - rr_ + bob - 12, sx + rr_, by + rr_ + bob - 12], fill=(255, 190, 90, al)) for rr_, al in ((52, 40), (38, 70), (26, 90))])
            view.alpha_composite(GUMB, (int(sx - GUMB.width / 2), int(by - GUMB.height / 2 - 12 + bob)))
        # props + racers y-sorted
        items = [(y, 'p', x, im) for x, y, im in PROPL if -120 < x - camx < W + 120] + [(st[n]['y'], 'r', n, None) for n in NAMES]
        layer(view, lambda dd: [dd.ellipse([st[n]['x'] - camx - 26, st[n]['y'] - 8, st[n]['x'] - camx + 26, st[n]['y'] + 8], fill=(0, 0, 0, 80)) for n in NAMES])
        for y, kind, a_, im in sorted(items, key=lambda z: z[0]):
            if kind == 'p':
                view.alpha_composite(im, (int(a_ - camx - im.width / 2), int(y - im.height + 26))); continue
            n = a_; s = st[n]; x = s['x'] - camx
            if t < T_START: spr = STAND[n][int(t * 8) % len(STAND[n])]
            elif s['out'] is not None and t > s['out'] + 0.6: spr = STAND[n][int(t * 8) % len(STAND[n])]
            elif s['sliding']:
                k = min(6, int((t - s['slide']) / SL * 7)); spr = (SLIDEL if s['vx'] < 0 else SLIDE)[n][k]
                if (n, round(s['slide'], 2)) not in seen_slide: seen_slide.add((n, round(s['slide'], 2))); ev.append((round(t, 3), 'jump'))
                layer(view, lambda dd: [dd.ellipse([x - math.copysign(1, s['vx']) * (22 + q * 22) - 12, y - 14 - q * 3, x - math.copysign(1, s['vx']) * (22 + q * 22) + 12, y + 6],
                                                   fill=(210, 195, 160, max(0, int(170 * (1 - (t - s['slide']) / SL)) - q * 40))) for q in range(3)])
            else:
                ph = int(s['dist'] / 22) % 8
                spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
            boosted = s['boost'] is not None and 0 <= t - s['boost'] < BOOST_T
            if boosted:
                ghosts[n] = (ghosts[n] + [(spr, s['x'], y)])[-5:]
                for i_, (gs, gx2, gy2) in enumerate(ghosts[n][:-1]):
                    tint = Image.new('RGBA', gs.size, (255, 180, 60, 255)); tint.putalpha(gs.getchannel('A').point(lambda p, i_=i_: int(p * (0.12 + 0.08 * i_))))
                    view.alpha_composite(tint, (int(gx2 - camx - gs.width / 2), int(gy2 - FOOT)))
            else: ghosts[n] = []
            view.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
            # rank tag
            rk = rank.index(n) + 1
            dv = ImageDraw.Draw(view); ctext(dv, x, y - FOOT + 4, str(rk), F(26), RING[n], 5)
            if boosted:
                u = t - s['boost']
                if u < 1.3:
                    al = int(255 * min(1, (1.3 - u) / 0.4)); text_layer(view, [(x, y - FOOT - 50 - u * 40, 'ENERGY GUMMY!', 26, (255, 200, 70), 5, al)])
                if (n, s['boost']) not in seen_boost: seen_boost.add((n, s['boost'])); ev.append((round(t, 3), 'powerup_8bit'))
            if s['out'] is not None and n not in fin_seen and t >= s['out']:
                fin_seen.add(n); ev.append((round(t, 3), 'ding_8bit' if rank.index(n) else 'vg02'))
        img = Image.new('RGBA', (W, H), (20, 40, 20, 255))
        img.alpha_composite(view, (0, BY))
        layer(img, lambda dd: dd.rectangle([0, BY - 6, W, BY], fill=(14, 10, 24, 255)))
        # footer minimap
        layer(img, lambda dd: dd.rectangle([0, BY + BH, W, H], fill=(14, 10, 24, 255)))
        d = ImageDraw.Draw(img); my = BY + BH + 72
        d.rounded_rectangle([60, my - 8, W - 60, my + 8], 8, fill=(80, 70, 100))
        d.rectangle([W - 70, my - 22, W - 58, my + 22], fill=(245, 245, 245))
        for n in sorted(NAMES, key=lambda n: st[n]['x']):
            px = 60 + (W - 130) * min(1, st[n]['x'] / FIN_X)
            ic = ICS.setdefault(n, ICON[n].resize((56, 56), Image.NEAREST)); img.alpha_composite(ic, (int(px - 28), my - 28))
        # header
        img.alpha_composite(HUB[int(t * 6) % len(HUB)], (0, 0))
        layer(img, lambda dd: (dd.rectangle([0, 0, W, 540], fill=(14, 10, 24, 80)), dd.rounded_rectangle([30, 330, W - 30, 520], 22, fill=(14, 10, 24, 210))))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([30, 330, W - 30, 520], 22, outline=(255, 214, 60), width=5)
        ctext(d, W / 2, 60, "WHO'S IN", F(70)); ctext(d, W / 2, 160, 'FIRST PLACE?', F(70), (255, 214, 60))
        for i, n in enumerate(NAMES):
            tgt = rank.index(n); rank_pos[n] += (tgt - rank_pos[n]) * 0.2
        for ri in range(4):
            sx = 30 + (W - 60) * (ri + 0.5) / 4
            ctext(d, sx, 446, ['1ST', '2ND', '3RD', '4TH'][ri], F(32), (255, 214, 60) if ri == 0 else (230, 230, 230), 5)
        for n in sorted(NAMES, key=lambda n: -rank_pos[n]):
            sx = 30 + (W - 60) * (rank_pos[n] + 0.5) / 4; ic = ICON[n]
            img.alpha_composite(ic, (int(sx - ic.width / 2), 345))
            d = ImageDraw.Draw(img); ri = rank.index(n)
            if ri == 0 and abs(rank_pos[n]) < 0.15: d.polygon([(sx - 26, 352), (sx - 16, 330), (sx - 4, 346), (sx, 324), (sx + 4, 346), (sx + 16, 330), (sx + 26, 352)], fill=(255, 214, 60), outline=(20, 15, 35))
        if t < T_START:
            cd = ['3', '2', '1'][min(2, int(t / 0.8))]; sc = 1 + 0.4 * (1 - (t % 0.8) / 0.8)
            text_layer(img, [(W / 2, BY + 500, cd, int(140 * sc), (255, 255, 255), 10, 255)])
            if abs(t % 0.8) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
        elif t < T_START + 0.6:
            text_layer(img, [(W / 2, BY + 520, 'GO!', 130, (120, 230, 90), 10, int(255 * (1 - (t - T_START) / 0.6)))])
            if abs(t - T_START) < 0.5 / FPS: ev.append((round(t, 3), 'go_8bit'))
    else:
        u = t - T_POD; order = [n for _, n in OUTS] + [n for n in rank if n not in [m for _, m in OUTS]]
        img = HUBP[int(t * 3) % len(HUBP)].copy()
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(10, 8, 18, 110)))
        # podium
        spots = [(W / 2, 1340, 6, 0), (W / 2 - 300, 1440, 5, 1), (W / 2 + 300, 1500, 5, 2)]
        for cx, top, k, idx in spots:
            ped = up(PED, k); img.alpha_composite(ped, (int(cx - ped.width / 2), int(top)))
            d = ImageDraw.Draw(img); ctext(d, cx, top + ped.height * 0.45, str(idx + 1), F(64 if idx == 0 else 52), (255, 214, 60) if idx == 0 else (235, 235, 235), 7)
            n = order[idx]; q = ease_ = max(0, min(1, (u - 0.2 * (2 - idx)) / 0.4))
            if q <= 0: continue
            if idx == 0:
                vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (int(cx - vf.width / 2), int(top + 20 - vf.height - (1 - q) * 300)))
                d = ImageDraw.Draw(img); cy_ = top + 20 - vf.height - 60
                d.polygon([(cx - 50, cy_ + 40), (cx - 32, cy_), (cx - 10, cy_ + 28), (cx, cy_ - 8), (cx + 10, cy_ + 28), (cx + 32, cy_), (cx + 50, cy_ + 40)], fill=(255, 214, 60), outline=(20, 15, 35))
            else:
                sp_ = STAND[n][int(t * 8) % len(STAND[n])]; sp_ = up(sp_, 1.5)
                img.alpha_composite(sp_, (int(cx - sp_.width / 2), int(top + 20 - 78 * 3 - (1 - q) * 200)))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2, 160, 'WINNER', F(110), (255, 214, 60), 10)
        ctext(d, W / 2, 310, LABEL[WIN] + '!', F(70), (255, 255, 255), 8)
        if u > 1.0: text_layer(img, [(W / 2, 1830, 'DID YOU PICK RIGHT?', 46, (255, 255, 255), 7, int(255 * min(1, (u - 1.0) / 0.4)))])
        rr2 = random.Random(f)
        for _ in range(50):
            cx_, cy_ = rr2.uniform(0, W), (rr2.uniform(-200, H) + u * 520) % H
            d.rectangle([cx_, cy_, cx_ + 11, cy_ + 11], fill=rr2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]))
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'victory')); ev.append((round(t, 3), 'cheer'))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('v46_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
