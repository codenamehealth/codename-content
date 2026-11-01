import sys, math, json, random, heapq
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); import hook as _hk
sys.path.insert(0, SP + 'fork_rc1'); import hook2 as _h2
_f0 = _hk._fit; _h2._fit = lambda lines, maxw, hi=80, lo=48: _f0(lines, maxw, min(hi, 64), lo)
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
C = 64; NR, NC = 15, 45                      # corner grid (tiles 19 x 44)
BW, BH = (NC - 1) * C, (NR - 1) * C
BY = 590                                     # hfg4: board top on screen (was 656); the whole board (rows 0-896) shows, y590-1486
VY0 = 0; VH = (NR - 1) * 64                  # grass field continues above and below the board to the frame edges
SPD = 1.15                                   # race plays 15% faster (same sim, same winner) so the finish lands earlier
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
START_R = [2, 5, 9, 12]
R = 22; SL = 0.5; T_START = 0.4
# ---------------- power gummies (SPEC 12): every gummy on the board does something
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'cre': ('STRONG!', (90, 160, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
SPEED_T, SPEED_K = 2.4, 1.6
STRONG_T = 2.8; SLEEP_T = 1.0; STUN_T = 0.75
POW_COLS = [int(c) for c in os.environ.get('PCOLS', '7,11,15,19,23,27,31,35').split(',')]
POW_TYPES = os.environ.get('PTYPES', 'cre,mush,acv,mel,mush,cre,mel,acv').split(',')
def traffic(seeds=(1, 2, 3)):
    tr = np.zeros((NR, NC))
    for sd in seeds:
        _, fr, *_ = sim(sd, pows=[])
        for st, _, _ in fr[::3]:
            for s in st.values(): tr[min(NR - 1, max(0, int(round(s['y'] / C)))), min(NC - 1, max(0, int(round(s['x'] / C))))] += 1
    return tr
def place_pows(tr):
    out = []
    for c, k in zip(POW_COLS, POW_TYPES):
        best = None
        for cc in (c - 1, c, c + 1):
            for r in range(2, NR - 2):
                if CG[r, cc] and (r, cc) not in PROPS and all(CG[r + dr, cc + dc] for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                    if best is None or tr[r, cc] > best[0]: best = (tr[r, cc], r, cc)
        out.append((best[2] * C, best[1] * C, k))
    return out
def sim(seed, dur=24.0, pows=None):
    pows = POWS if pows is None else pows
    rnd = random.Random(seed); order = NAMES[:]; rnd.shuffle(order)
    rc = {}; props = set(PROPS); smashed = {}
    for i, n in enumerate(order):
        rc[n] = dict(x=1.4 * C, y=START_R[i] * C, vx=0.0, vy=0.0, base=rnd.uniform(255, 290), ph=rnd.uniform(0, 6.3), out=None, mode='side',
                     slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, dist=0.0, strong=None, shield=False, sleep=-9, stun=-9, hitcd={})
    taken = {}; frames = []; leaders = []; fx = []; prank = order[:]
    PULL = float(os.environ.get('PULL', '230'))
    def pa(x, y): return cpt(x, y) in props
    def powered(s, t):
        return (s['boost'] is not None and t - s['boost'] < SPEED_T) or (s['strong'] is not None and t - s['strong'] < STRONG_T) or s['shield']
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        for n, s in rc.items():
            if s['out'] is not None or t < T_START: continue
            if t < s['sleep']: s['vx'] = s['vy'] = 0.0; s['sliding'] = False; continue
            stunned = t < s['stun']
            strong = s['strong'] is not None and t - s['strong'] < STRONG_T
            sliding = t - s['slide'] < SL or (s['slide'] > 0 and pa(s['x'], s['y']))
            sp = s['base'] * (1 + 0.28 * math.sin(0.8 * t + s['ph']) + 0.15 * math.sin(2.1 * t + 2 * s['ph']))
            if s['boost'] is not None and t - s['boost'] < SPEED_T: sp *= SPEED_K
            if stunned:
                s['vx'] *= 0.86; s['vy'] *= 0.86
            elif sliding:
                sp *= 1.2; s['vx'] += (s['sdx'] * sp - s['vx']) * 0.3; s['vy'] += (s['sdy'] * sp - s['vy']) * 0.3
            else:
                a, b = min(GR - 1, max(0, int(s['y'] // FC))), min(GCn - 1, max(0, int(s['x'] // FC)))
                gx, gy = -GX[a, b], -GY[a, b]; L = math.hypot(gx, gy) or 1
                wob = 0.4 * math.sin(3.3 * t + s['ph'] * 3); dx, dy = gx / L, gy / L
                tx, ty = dx - dy * wob, dy + dx * wob
                # gummies pull racers in when they are close and ahead (so every gummy gets used)
                for k, (px, py, kind) in enumerate(pows):
                    if k in taken or n == prank[0] or powered(s, t): continue
                    ddx, ddy = px - s['x'], py - s['y']; dd = math.hypot(ddx, ddy)
                    if dd < PULL and ddx > -10:
                        w = 0.75 * (1 - dd / PULL) + 0.25; tx, ty = tx * (1 - w) + ddx / dd * w, ty * (1 - w) + ddy / dd * w; break
                s['vx'] += (tx * sp - s['vx']) * 0.12; s['vy'] += (ty * sp - s['vy']) * 0.12
            v = math.hypot(s['vx'], s['vy']) or 1
            if not sliding and not stunned and t - s['slide'] > 1.0 and t > T_START + 0.6:
                ux, uy = s['vx'] / v, s['vy'] / v
                for d_ in (R + 10, R + 26):
                    cell = cpt(s['x'] + ux * d_, s['y'] + uy * d_)
                    if cell in props:
                        if strong:
                            props.discard(cell); smashed[cell] = t; fx.append((t, 'smash', n, cell))
                        else:
                            s['slide'] = t; s['sdx'], s['sdy'] = ux, uy; sliding = True
                        break
            nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
            for _ in range(2):
                for ax, ay in ((R, 0), (-R, 0), (0, R), (0, -R), (R * .7, R * .7), (-R * .7, R * .7), (R * .7, -R * .7), (-R * .7, -R * .7)):
                    if grass_at(nx + ax, ny + ay) or (not sliding and pa(nx + ax, ny + ay)):
                        if ax: nx -= ax * 0.18; s['vx'] *= -0.4
                        if ay: ny -= ay * 0.18; s['vy'] *= -0.4
            s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
            for m, o in rc.items():
                if m == n or o['out'] is not None: continue
                ddx, ddy = s['x'] - o['x'], (s['y'] - o['y']) * 1.6; dd = math.hypot(ddx, ddy)
                if strong and 0 < dd < 2 * R + 22 and t - s['hitcd'].get(m, -9) > 1.0 and t >= o['sleep']:
                    s['hitcd'][m] = t
                    if o['shield']:
                        o['shield'] = False; fx.append((t, 'block', m, n))
                    else:
                        o['stun'] = t + STUN_T; o['vx'] = -ddx / dd * 420; o['vy'] = -ddy / dd * 260; o['slide'] = -9
                        fx.append((t, 'hit', n, m))
                    continue
                if sliding or t - o['slide'] < SL: continue
                if 0 < dd < 2 * R + 8:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and t - s['slide'] > 1.0 and t > T_START + 0.6 and not stunned:
                        s['slide'] = t; s['sdx'], s['sdy'] = s['vx'] / v, s['vy'] / v; sliding = True; continue
                    push = (2 * R + 8 - dd) / 2; s['x'] += ddx / dd * push * 0.8; s['y'] += ddy / dd * push * 0.5
            s['mode'] = 'down' if s['vy'] > 0.72 * v else 'side'; s['sliding'] = sliding and not stunned
            for k, (bx, by, kind) in enumerate(pows):
                if k not in taken and not stunned and not powered(s, t) and math.hypot(s['x'] - bx, s['y'] - by) < 48:
                    taken[k] = (n, t); fx.append((t, 'pick', n, kind))
                    if kind == 'mush': s['boost'] = t
                    elif kind == 'cre': s['strong'] = t
                    elif kind == 'acv': s['shield'] = True; s['stun'] = -9
                    elif kind == 'mel':
                        vic, blk = [], []
                        for m, o in rc.items():
                            if m == n or o['out'] is not None: continue
                            if o['shield']: o['shield'] = False; blk.append(m); fx.append((t, 'block', m, n))
                            else: o['sleep'] = t + SLEEP_T; vic.append(m)
                        fx.append((t, 'sleepwave', n, vic))
            if s['x'] > FIN_X: s['out'] = t; s['shield'] = False
        def prog(s):
            if s['out'] is not None: return -1e6 + s['out']
            a, b = min(GR - 1, max(0, int(s['y'] // FC))), min(GCn - 1, max(0, int(s['x'] // FC)))
            return DEX[a, b] if not np.isinf(DEX[a, b]) else 1e5
        rank = sorted(rc, key=lambda n: prog(rc[n])); prank = rank
        if t > T_START + 1 and (not leaders or leaders[-1] != rank[0]): leaders.append(rank[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], out=s['out'], mode=s['mode'], slide=s['slide'], sliding=s['sliding'],
                                boost=s['boost'], dist=s['dist'], strong=s['strong'], shield=s['shield'], sleep=s['sleep'], stun=s['stun']) for n, s in rc.items()}, rank, dict(taken)))
        if all(s['out'] is not None for s in rc.values()): break
    return rc, frames, leaders, fx, smashed
POWS = []
POWS = place_pows(traffic())
def score(seed):
    rc, fr, ld, fx, sm = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    if len(outs) < 4: return None
    t1, w = outs[0]; t2 = outs[1][0]
    if w != os.environ.get('WANT', 'cleo'): return None
    picks = [e for e in fx if e[1] == 'pick']
    if len(picks) < len(POWS): return None
    if not (9.0 < t1 < 14.5) or t2 - t1 > 0.6 or len(ld) < 5: return None
    if not any(e[1] == 'sleepwave' and len(e[3]) >= 2 for e in fx): return None
    nh = sum(e[1] == 'hit' for e in fx); nb = sum(e[1] == 'block' for e in fx)
    if nh < 1 or nb < 1: return None
    seq_ = [e[3] for e in picks]
    if seq_[:4] == seq_[4:8]: return None                       # never a fixed repeating order
    return round(t1, 2), w, round(t2 - t1, 2), len(ld), nh, nb, len(sm), seq_, [e[2] for e in picks]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
if len(sys.argv) > 1 and sys.argv[1] == 'map':
    print(POWS); sys.exit()
SEED = int(sys.argv[1])
RC, FR, LD, FX, SMASHED = sim(SEED)
OUTS = sorted((s['out'], n) for n, s in RC.items() if s['out'] is not None)
T_WIN, WIN = OUTS[0]
print('winner', WIN, round(T_WIN, 2), 'order', [(n, round(t, 2)) for t, n in OUTS], 'leaders', LD)
print('fx', [(round(e[0], 2), e[1], e[2], e[3]) for e in FX])
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
# hfg4 full-bleed: the plaza sits in a grass field that runs to every frame edge (scrolls with the camera)
XOFF = 128
FIELD = Image.new('RGBA', (BW + 600 + XOFF + 64, H), (40, 90, 40, 255))
_g = TILE[(False, False, False, False)]; rf = random.Random(11)
for j in range(-(BY // C) - 1, (H - BY) // C + 1):
    for i in range(-(XOFF // C), (BW + 600) // C + 1):
        tl = _g
        if (i + j) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        if (i * 3 + j) % 3 == 0: tl = tl.transpose(Image.FLIP_TOP_BOTTOM)
        FIELD.alpha_composite(tl, (XOFF + i * C, BY + j * C))
for _ in range(60):
    fx_, fy_ = rf.uniform(0, FIELD.width), rf.uniform(0, H)
    if BY - 40 < fy_ < BY + BH + 40: continue
    im = up(pick('flowers', rf.choice([1, 4, 7, 12])), 2); FIELD.alpha_composite(im, (int(fx_), int(fy_)))
FIELD.alpha_composite(BOARD, (XOFF, BY))
SS = 2; FOOT = 78 * SS
def seqa(d, lo=1, hi=9): return [up(Image.open(p).convert('RGBA'), SS) for p in sorted(glob.glob(d + '/*.png'))[lo:hi]]
SRUN = {g: seqa(f'../../pixellab/race/{g}_run') for g in NAMES}
FRUN = {g: seqa(f'../../pixellab/maze/anim/{g}_frun') for g in NAMES}
SLIDE = {g: seqa(f'../../pixellab/maze/anim/{g}_slide', 1, 8) for g in NAMES}
STAND = {g: idle(g, 2) for g in NAMES}
FL_ = lambda L: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in L]
SRUNL = {g: FL_(v) for g, v in SRUN.items()}; SLIDEL = {g: FL_(v) for g, v in SLIDE.items()}
PANIC = {g: seqa(f'../../pixellab/maze/anim/{g}_panic') for g in NAMES}
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import acv_gloss, acv_tag
POWIM = {k: (up(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')), 3) if k == 'acv' else gummy(k, 3)) for k in POWER}
SRCF = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
def face(name, rad):
    im = Image.open('../../syeda_src/' + SRCF[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), m); return b
ICS2 = {n: face(n, 52) for n in NAMES}   # hfg4: standings faces 88 -> 108px
HOOK, HB = _hk.hook_fade(["WHO'S IN", 'FIRST PLACE?'], accent=1, color=(255, 214, 60), size=72)   # hfg4: soft fade, no box, no sub
CHIP_Y = HB - 2; CHIP_H = 108
assert CHIP_Y + CHIP_H + 6 <= BY, (HB, BY)
print('hook bottom', HB, 'board', BY, BY + BH)
HUB = bg_frames('hub.gif', (W, 540), box=(0, 120, 1920, 120 + 960), step=2, bright=0.6)
hubp_src = bg_frames('hub.gif', (int(1920 * H / 1080), H), step=4, bright=0.72)
HUBP = [h.crop(((h.width - W) // 2, 0, (h.width - W) // 2 + W, H)) for h in hubp_src]
PED = crop(Image.open('../../fork2/pedestal/00.png').convert('RGBA'))
VICF = vic(WIN, 330)
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
def aura(view, spr, x0, y0, col, a):
    tt = tinted(spr, col, a)
    for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)): view.alpha_composite(tt, (x0 + ox, y0 + oy))
# pop labels (world coords) - stacked so they never overlap
POPS = []   # (t0, x, y, text, col, size, who) - who: racer the stamp follows (None = fixed world point)
def add_pop(t0, x, y, text, col, size=34, who=None):
    POPS.append((t0, x, y, text, col, size, who))
for e in FX:
    t0, kind = e[0], e[1]
    st0 = FR[min(int(round(t0 * FPS)), len(FR) - 1)][0]
    if kind == 'pick':
        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, POWER[e[3]][0], POWER[e[3]][1], 64, e[2])
    elif kind == 'hit':
        s = st0[e[3]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BONK!', (255, 255, 255), 64, e[3])
    elif kind == 'block':
        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BLOCKED!', (110, 230, 90), 60, e[2])
    elif kind == 'smash':
        r_, c_ = e[3]; add_pop(t0, c_ * C, r_ * C - 90, 'SMASH!', (90, 160, 255), 60)
POPS.sort(key=lambda p: p[0])
POP_D = 1.1
def pop_items(t, camx, st):
    act = [p for p in POPS if 0 <= t - p[0] < POP_D]; placed = []; items = []
    for t0, x, y, text, col, size, who in act:
        if who is not None: x, y = st[who]['x'], st[who]['y'] - FOOT - 70      # rides directly above the racer it applies to
        u = t - t0; sx = x - camx; sy = y - u * 20
        w = len(text) * size + 20; hh = size + 16
        xr = 1018 if BY + sy - VY0 < 1110 else 880
        sx = min(max(sx, 76 + w / 2), xr - w / 2)
        for _ in range(8):
            if any(abs(sx - px) < (w + pw) / 2 and abs(sy - py) < (hh + ph) / 2 for px, py, pw, ph in placed): sy -= hh + 4
            else: break
        sy = max(sy, (CHIP_Y + CHIP_H + 4 - BY) + hh / 2)     # never over the standings row
        placed.append((sx, sy, w, hh)); al = int(255 * min(1, (POP_D - u) / 0.3)); sc = 1 + 0.3 * max(0, 1 - u / 0.15)
        items.append((sx, sy - hh / 2, text, int(size * sc), col, 6, al))
    return items
T_POD_D = (T_WIN + 1.0) / SPD; PODIUM = 2.5; DUR = T_POD_D + PODIUM; NF = int(round(DUR * FPS))   # ends on the podium; the loop supplies the GO!
wr = Writer('v46_noaudio.mp4'); ev = []; camx = -40.0; ghosts = {n: [] for n in NAMES}
ACVT = [None]; SWAPT = {}; seen_slide = set(); fin_seen = set(); rank_pos = {n: float(i) for i, n in enumerate(NAMES)}
SFX = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
for e in FX:
    td = round(e[0] / SPD, 3)
    if e[1] == 'pick': ev.append((td, SFX[e[3]]))
    elif e[1] == 'hit': ev.append((td, 'punch'))
    elif e[1] == 'block': ev.append((td, 'boing'))
    elif e[1] == 'smash': ev.append((td, 'crunch_8bit'))
ev.append((0.0, 'go_8bit'))
CAM0 = -40.0
for f in range(NF):
    td = f / FPS; t = td * SPD
    fi = int(round(t * FPS))
    st, rank, taken = FR[min(fi, len(FR) - 1)]
    if td < T_POD_D:
        lead_x = max(s['x'] for s in st.values())
        target = min(max(lead_x - 600, -40), BW + 600 - W)
        camx += (target - camx) * 0.15 if t > T_START else 0
        view = BOARD.crop((int(camx), 0, int(camx) + W, BH)).copy()
        # power gummies
        for k, (bx, by, kind) in enumerate(POWS):
            sx = bx - camx
            if not (-100 < sx < W + 100): continue
            col = POWER[kind][1]
            if k in taken and t >= taken[k][1]:
                u = t - taken[k][1]
                if u < 0.6:
                    layer(view, lambda dd, sx=sx, by=by, u=u, col=col: [dd.rectangle([sx + (20 + 120 * u) * math.cos(q * 0.628) - 6, by - 20 + (20 + 120 * u) * math.sin(q * 0.628) - 6,
                                                         sx + (20 + 120 * u) * math.cos(q * 0.628) + 6, by - 20 + (20 + 120 * u) * math.sin(q * 0.628) + 6], fill=col + (int(255 * (1 - u / 0.6)),)) for q in range(10)])
                continue
            bob = int(7 * math.sin(t * 4 + k)); g = POWIM[kind]
            layer(view, lambda dd, sx=sx, by=by, bob=bob, col=col: [dd.ellipse([sx - rr_, by - rr_ + bob - 12, sx + rr_, by + rr_ + bob - 12], fill=col + (al,)) for rr_, al in ((56, 40), (42, 70), (30, 90))])
            view.alpha_composite(g, (int(sx - g.width / 2), int(by - g.height / 2 - 12 + bob)))
        # sleep wave rings
        for e in FX:
            if e[1] == 'sleepwave' and 0 <= t - e[0] < 0.7:
                s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
                layer(view, lambda dd, s0=s0, u=u: [dd.ellipse([s0['x'] - camx - r_, s0['y'] - 60 - r_ * 0.7, s0['x'] - camx + r_, s0['y'] - 60 + r_ * 0.7], outline=(190, 120, 255, int(220 * (1 - u))), width=10) for r_ in (60 + 900 * u, 20 + 600 * u)])
            if e[1] == 'smash' and 0 <= t - e[0] < 0.5:
                r_, c_ = e[3]; u = (t - e[0]) / 0.5; px_, py_ = c_ * C - camx, r_ * C - 30
                layer(view, lambda dd, px_=px_, py_=py_, u=u: [dd.rectangle([px_ + math.cos(q * 0.9) * 140 * u - 8, py_ + math.sin(q * 0.9) * 90 * u + 160 * u * u - 8, px_ + math.cos(q * 0.9) * 140 * u + 8, py_ + math.sin(q * 0.9) * 90 * u + 160 * u * u + 8], fill=(150, 96, 50, int(255 * (1 - u)))) for q in range(9)])
            if e[1] == 'hit' and 0 <= t - e[0] < 0.3:
                s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[3]]; u = (t - e[0]) / 0.3
                cx_, cy_ = s0['x'] - camx, s0['y'] - FOOT / 2
                layer(view, lambda dd, cx_=cx_, cy_=cy_, u=u: [dd.polygon([(cx_ + math.cos(q * 0.785) * 30, cy_ + math.sin(q * 0.785) * 30), (cx_ + math.cos(q * 0.785 + 0.2) * (60 + 60 * u), cy_ + math.sin(q * 0.785 + 0.2) * (60 + 60 * u)),
                                                                 (cx_ + math.cos(q * 0.785 + 0.39) * 30, cy_ + math.sin(q * 0.785 + 0.39) * 30)], fill=(255, 255, 255, int(255 * (1 - u)))) for q in range(8)])
        # props (minus smashed ones) + racers, y-sorted
        items = [(y, 'p', x, im) for x, y, im in PROPL if -120 < x - camx < W + 120 and not (cpt(x, y) in SMASHED and t >= SMASHED[cpt(x, y)])] + [(st[n]['y'], 'r', n, None) for n in NAMES]
        layer(view, lambda dd: [dd.ellipse([st[n]['x'] - camx - 26, st[n]['y'] - 8, st[n]['x'] - camx + 26, st[n]['y'] + 8], fill=(0, 0, 0, 80)) for n in NAMES])
        for y, kind, a_, im in sorted(items, key=lambda z: z[0]):
            if kind == 'p':
                view.alpha_composite(im, (int(a_ - camx - im.width / 2), int(y - im.height + 26))); continue
            n = a_; s = st[n]; x = s['x'] - camx
            asleep = t < s['sleep']; stunned = t < s['stun']
            strong = s['strong'] is not None and 0 <= t - s['strong'] < STRONG_T
            boosted = s['boost'] is not None and 0 <= t - s['boost'] < SPEED_T
            if t < T_START: spr = (SRUN[n][int(t * 16) % 8])                     # running on the spot at the GO
            elif s['out'] is not None and t > s['out'] + 0.6: spr = STAND[n][int(t * 8) % len(STAND[n])]
            elif asleep: spr = STAND[n][0]
            elif stunned: spr = PANIC[n][int(t * 12) % len(PANIC[n])]
            elif s['sliding']:
                k = min(6, int((t - s['slide']) / SL * 7)); spr = (SLIDEL if s['vx'] < 0 else SLIDE)[n][k]
                if (n, round(s['slide'], 2)) not in seen_slide: seen_slide.add((n, round(s['slide'], 2))); ev.append((round(td, 3), 'jump'))
            else:
                ph = int(s['dist'] / 22) % 8
                spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
            x0, y0 = int(x - spr.width / 2), int(y - FOOT)
            if boosted and not asleep and not stunned:
                ghosts[n] = (ghosts[n] + [(spr, s['x'], y)])[-5:]
                for i_, (gs, gx2, gy2) in enumerate(ghosts[n][:-1]):
                    view.alpha_composite(tinted(gs, (255, 170, 50), int(255 * (0.14 + 0.09 * i_))), (int(gx2 - camx - gs.width / 2), int(gy2 - FOOT)))
                sgn = -1 if s['vx'] >= 0 else 1
                layer(view, lambda dd, x=x, y=y, sgn=sgn: ([dd.rectangle([min(x + sgn * (50 + 30 * q), x + sgn * (50 + 30 * q) + sgn * (70 + (q * 37 + int(t * 60)) % 50)), y - 100 + q * 26 - 3, max(x + sgn * (50 + 30 * q), x + sgn * (50 + 30 * q) + sgn * (70 + (q * 37 + int(t * 60)) % 50)), y - 100 + q * 26 + 3], fill=(255, 240, 200, 200)) for q in range(4)] +
                                                            [dd.ellipse([x + sgn * (30 + q * 26) - 14 + q * 2, y - 12 - q * 4, x + sgn * (30 + q * 26) + 14, y + 8], fill=(210, 190, 150, 150 - q * 40)) for q in range(3)]))
            else: ghosts[n] = []
            if strong: aura(view, spr, x0, y0, (90, 160, 255), int(150 + 80 * math.sin(t * 14)))
            if asleep:
                dark = spr.copy(); view.alpha_composite(dark, (x0, y0)); view.alpha_composite(tinted(spr, (40, 20, 90), 90), (x0, y0))
                u = (t - (s['sleep'] - SLEEP_T))
                text_layer(view, [(x + 30 + 18 * k_, y - FOOT - 10 - ((u * 1.6 + k_ * 0.33) % 1) * 70 - k_ * 14, 'Z', 30 + 8 * k_, (220, 200, 255), 5, int(255 * (1 - (u * 1.6 + k_ * 0.33) % 1))) for k_ in range(3)])
            else:
                view.alpha_composite(spr, (x0, y0))
            if stunned:
                layer(view, lambda dd, x=x, y=y: [dd.polygon([(x + 34 * math.cos(t * 9 + q * 2.09) + dx_, y - FOOT + 20 + 10 * math.sin(t * 9 + q * 2.09) + dy_) for dx_, dy_ in ((0, -9), (3, -3), (9, -2), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -2), (-3, -3))], fill=(255, 230, 60, 255)) for q in range(3)])
            if s['shield']:
                layer(view, lambda dd, x=x, y=y: (dd.ellipse([x - 70, y - FOOT + 6, x + 70, y + 18], fill=(110, 230, 90, 55), outline=(150, 255, 120, 220), width=6),
                                                  dd.arc([x - 52, y - FOOT + 24, x + 10, y - FOOT + 90], 200, 260, fill=(230, 255, 220, 230), width=5)))
            rk = rank.index(n) + 1
            dv = ImageDraw.Draw(view); ctext(dv, x, max(VY0 + 4, y - FOOT - 24), str(rk), F(52), RING[n], 8)
            if s['out'] is not None and n not in fin_seen and t >= s['out']:
                fin_seen.add(n); ev.append((round(td, 3), 'ding_8bit' if rank.index(n) else 'vg02'))
        text_layer(view, pop_items(t, camx, st))
        img = FIELD.crop((int(camx) + XOFF, 0, int(camx) + XOFF + W, H))
        img.alpha_composite(view.crop((0, VY0, W, VY0 + VH)), (0, BY))
        ka = min(k for k, p_ in enumerate(POWS) if p_[2] == 'acv'); bx, by_, _ = POWS[ka]
        jx = int(bx - camx); gtop = int(BY + by_ - VY0 - 12 - POWIM['acv'].height / 2 - 6)
        if False:                                        # hfg4: 'ACV GUMMY' tag cut (SHIELD! names its power when it fires)      # 'ACV GUMMY' tag on first appearance: plate kept in the safe zone, arrow down to the gummy
            aa = int(255 * min(1, (td - 0.15) / 0.12, (1.8 - td) / 0.25))
            def acvtag(dd, jx=jx, gtop=gtop, aa=aa):
                tg = 'ACV GUMMY'; f_ = F(44); tw = dd.textlength(tg, font=f_); y0 = 1026
                x0 = max(80, min(1004 - tw - 36, jx - tw / 2 - 18)); ring = (90, 200, 80)
                dd.line([(jx, y0 + 72), (jx, gtop - 22)], fill=ring + (aa,), width=6)
                dd.polygon([(jx - 16, gtop - 26), (jx + 16, gtop - 26), (jx, gtop - 2)], fill=ring + (aa,))
                dd.rounded_rectangle([x0, y0, x0 + tw + 36, y0 + 72], 14, fill=(14, 10, 24, int(235 * aa / 255)), outline=ring + (aa,), width=5)
                dd.text((x0 + 18, y0 + 14), tg, font=f_, fill=(255, 255, 255, aa), stroke_width=5, stroke_fill=(10, 6, 18, aa))
            layer(img, acvtag)
        if any(e[1] == 'sleepwave' and 0 <= t - e[0] < 0.25 for e in FX):
            img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 50)))
        d = ImageDraw.Draw(img)                          # hfg4: standings = faces in order on the grass (no box, no 1ST-4TH labels; crown on the leader)
        for i, n in enumerate(NAMES):
            tgt = rank.index(n)
            if rank_pos[n] != float(tgt) and td > 0.05: SWAPT[n] = td          # swaps snap (no sliding over the labels), with a short flash
            rank_pos[n] = float(tgt)
        for n in sorted(NAMES, key=lambda n: -rank_pos[n]):
            sx = 290 + 166 * rank_pos[n]; ic = ICS2[n]
            img.alpha_composite(ic, (int(sx - ic.width / 2), CHIP_Y + 2))
            if 0 <= td - SWAPT.get(n, -9) < 0.25:
                fa = int(255 * (1 - (td - SWAPT[n]) / 0.25))
                layer(img, lambda dd, sx=sx, fa=fa: dd.ellipse([sx - 60, CHIP_Y - 6, sx + 60, CHIP_Y + 114], outline=(255, 255, 255, fa), width=6))
            d = ImageDraw.Draw(img); ri = rank.index(n)
            if ri == 0 and abs(rank_pos[n]) < 0.15:
                cy0 = CHIP_Y - 12; d.polygon([(sx - 26, cy0 + 20), (sx - 15, cy0), (sx - 4, cy0 + 15), (sx, cy0 - 8), (sx + 4, cy0 + 15), (sx + 15, cy0), (sx + 26, cy0 + 20)], fill=(255, 214, 60), outline=(20, 15, 35))
        if td < 0.7:
            text_layer(img, [(W / 2, BY + 300, 'GO!', 150, (120, 230, 90), 10, int(255 * min(1, (0.7 - td) / 0.3)))])
    else:
        t = td; u = td - T_POD_D; order = [n for _, n in OUTS] + [n for n in rank if n not in [m for _, m in OUTS]]
        img = HUBP[int(t * 3) % len(HUBP)].copy()
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(10, 8, 18, 40)))   # hfg4: village no longer dimmed to a backdrop
        spots = [(478, 1120, 6, 0), (478 - 270, 1200, 5, 1), (478 + 270, 1230, 5, 2)]
        for cx, top, k, idx in spots:
            ped = up(PED, k); img.alpha_composite(ped, (int(cx - ped.width / 2), int(top)))
            d = ImageDraw.Draw(img); ctext(d, cx, top + ped.height * 0.45, str(idx + 1), F(64 if idx == 0 else 52), (255, 214, 60) if idx == 0 else (235, 235, 235), 7)
            n = order[idx]; q = max(0, min(1, (u - 0.2 * (2 - idx)) / 0.4))
            if q <= 0: continue
            if idx == 0:
                vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (int(cx - vf.width / 2), int(top + 20 - vf.height - (1 - q) * 300)))
                d = ImageDraw.Draw(img); cy_ = top + 20 - vf.height - 36
                d.polygon([(cx - 50, cy_ + 40), (cx - 32, cy_), (cx - 10, cy_ + 28), (cx, cy_ - 8), (cx + 10, cy_ + 28), (cx + 32, cy_), (cx + 50, cy_ + 40)], fill=(255, 214, 60), outline=(20, 15, 35))
            else:
                sp_ = STAND[n][int(t * 8) % len(STAND[n])]; sp_ = up(sp_, 1.5)
                img.alpha_composite(sp_, (int(cx - sp_.width / 2), int(top + 20 - 78 * 3 - (1 - q) * 200)))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2, HB + 40, LABEL[WIN] + ' WINS!', F(72), (255, 214, 60), 10)   # hfg4: WINNER / CLEO! -> one line; DID YOU PICK RIGHT? cut (caption asks)
        rr2 = random.Random(f)
        for _ in range(50):
            cx_, cy_ = rr2.uniform(0, W), (rr2.uniform(-200, H) + u * 520) % H
            d.rectangle([cx_, cy_, cx_ + 11, cy_ + 11], fill=rr2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]))
        if not any(e_[1] == 'victory' for e_ in ev): ev.append((round(t, 3), 'victory')); ev.append((round(t, 3), 'cheer'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0 or f == NF - 1: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
    if os.environ.get('FULL') and f in [int(round(e[0] * FPS)) + 4 for e in FX]: img.convert('RGB').save(f'fx_{f:04d}.png')
print('ACVT', ACVT); wr.close(); json.dump({'events': ev}, open('v46_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
