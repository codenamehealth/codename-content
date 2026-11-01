import sys, os; os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '../../fork1')
from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
sys.path.insert(0, '..'); import powers as PW
B7 = '../../fork_b7/'
import numpy as np
SEED = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] != 'search' else 0
NAMES = ['ray', 'joy', 'cyrus', 'cleo']   # HOLLOW RULE: the Hollow no longer competes
NG = len(NAMES)
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'HOLLOW'}
# SPEC 12 gummy powers: the gummy's TYPE decides the power (no per-guide realm powers any more)
T0 = float(os.environ.get('T0', '0.3')); T1 = T0 + 30.0; TEND = T1 + 3.0
SPEED_T, SPEED_K, STRONG_T, SLEEP_T, DIZZY_T, SHIELD_T = 3.0, 1.8, 3.0, 1.0, 0.9, 8.0
COL = {'joy': (90, 200, 80), 'cyrus': (245, 150, 40), 'cleo': (70, 130, 240), 'ray': (170, 80, 220), 'hollow': (110, 105, 140)}
# map grid
MAPCX, MAPCY = 478, 1095
LD = float(os.environ.get('LD', '286')); LR = float(os.environ.get('LR', '172')); RC = float(os.environ.get('RC', '200'))
CS = 30; GW, GH = 26, 26; GX0, GY0 = MAPCX - GW * CS // 2, MAPCY - GH * CS // 2
cx0, cy0 = GX0 + GW * CS / 2, GY0 + GH * CS / 2
LOBES = [(cx0 + LD * math.cos(-3 * math.pi / 4 + k * math.pi / 2), cy0 + LD * math.sin(-3 * math.pi / 4 + k * math.pi / 2)) for k in range(4)]
HOME = {n: LOBES[i] for i, n in enumerate(NAMES)}
yy, xx = np.mgrid[0:GH, 0:GW]; px = GX0 + (xx + 0.5) * CS; py = GY0 + (yy + 0.5) * CS
LAND = np.zeros((GH, GW), bool)
for (lx, ly) in LOBES: LAND |= (px - lx) ** 2 + (py - ly) ** 2 < LR ** 2
LAND |= (px - cx0) ** 2 + (py - cy0) ** 2 < RC ** 2
NL = LAND.sum()
SPK = float(os.environ.get('SPK', '0.9'))
def sim(seed):
    rnd = random.Random(seed)
    own = np.full((GH, GW), -1, int)
    for i, n in enumerate(NAMES):
        hx, hy = HOME[n]; own[LAND & ((px - hx) ** 2 + (py - hy) ** 2 < 70 ** 2)] = i
    ag = {n: dict(x=HOME[n][0], y=HOME[n][1], vx=0.0, vy=0.0, tx=None, ty=None, rt=0, spd=rnd.uniform(215, 245) * SPK, dist=0.0, ph=rnd.uniform(0, 6),
                  boost=-9.0, strong=-9.0, shield=None, sleep=-9.0, dizzy=-9.0, hitcd=-9.0, pop=-9.0) for n in NAMES}
    gum = None; next_gum = T0 + 2.2; frames = []; fx = []
    def hit(b, n_b, by, t):
        if t < b['hitcd']: return
        b['hitcd'] = t + 1.2
        if b['shield'] is not None: b['shield'] = None; b['pop'] = t; fx.append((t, 'block', n_b, b['x'], b['y'], 'hit')); return
        dx, dy = b['x'] - by['x'], b['y'] - by['y']; L = math.hypot(dx, dy) or 1
        b['vx'], b['vy'] = dx / L * 760, dy / L * 760; b['dizzy'] = t + DIZZY_T; b['tx'] = None
        fx.append((t, 'bonk', n_b, b['x'], b['y'], (by['x'] + b['x']) / 2, (by['y'] + b['y']) / 2))
    def move(a, nx, ny):
        gj, gi = int((ny - GY0) // CS), int((nx - GX0) // CS)
        if 0 <= gj < GH and 0 <= gi < GW and LAND[gj, gi]: a['dist'] += math.hypot(nx - a['x'], ny - a['y']); a['x'], a['y'] = nx, ny; return True
        a['vx'] *= -0.5; a['vy'] *= -0.5; a['rt'] = 0; return False
    for f in range(int(TEND * FPS)):
        t = f / FPS; dt = 1 / FPS
        if T0 <= t < T1:
            if gum is None and t >= next_gum:
                for _ in range(200):
                    gy_, gx_ = rnd.randrange(GH), rnd.randrange(GW)
                    if LAND[gy_, gx_] and min(math.hypot(px[gy_, gx_] - a['x'], py[gy_, gx_] - a['y']) for a in ag.values()) > 220: break
                gum = dict(x=px[gy_, gx_], y=py[gy_, gx_], kind=rnd.choice(['mush', 'acv', 'mel', 'cre']), t=t)
            for i, n in enumerate(NAMES):
                a = ag[n]
                if a['shield'] is not None and t - a['shield'] > SHIELD_T: a['shield'] = None; a['pop'] = t
                if t < a['sleep']: a['vx'] = a['vy'] = 0.0; continue              # SLEEP: frozen, paints nothing
                if t < a['dizzy']:                                                   # BONKED: slides back, can't steer or paint
                    a['vx'] *= 0.88; a['vy'] *= 0.88; move(a, a['x'] + a['vx'] * dt, a['y'] + a['vy'] * dt); continue
                if a['tx'] is None or t > a['rt'] or math.hypot(a['tx'] - a['x'], a['ty'] - a['y']) < 30:
                    cand = []
                    for _ in range(40):
                        gy_, gx_ = rnd.randrange(GH), rnd.randrange(GW)
                        if not LAND[gy_, gx_] or own[gy_, gx_] == i: continue
                        dd = math.hypot(px[gy_, gx_] - a['x'], py[gy_, gx_] - a['y'])
                        sc = dd - (120 if own[gy_, gx_] >= 0 else 60) + rnd.uniform(0, 120)
                        cand.append((sc, px[gy_, gx_], py[gy_, gx_]))
                    if gum and math.hypot(gum['x'] - a['x'], gum['y'] - a['y']) < 420: cand.append((-200, gum['x'], gum['y']))
                    if cand: _, a['tx'], a['ty'] = min(cand)
                    a['rt'] = t + rnd.uniform(1.0, 2.0)
                dx, dy = a['tx'] - a['x'], a['ty'] - a['y']; L = math.hypot(dx, dy) or 1
                sp = a['spd'] * (1 + 0.15 * math.sin(t * 1.3 + a['ph']))
                if t - a['boost'] < SPEED_T: sp *= SPEED_K
                a['vx'] += (dx / L * sp - a['vx']) * 0.15; a['vy'] += (dy / L * sp - a['vy']) * 0.15
                move(a, a['x'] + a['vx'] * dt, a['y'] + a['vy'] * dt)
                m = LAND & ((px - a['x']) ** 2 + (py - a['y']) ** 2 < 62 ** 2)
                own[m] = i
                if t - a['strong'] < STRONG_T:                                       # STRONG: anyone it runs into gets shoved
                    for m_ in NAMES:
                        b = ag[m_]
                        if m_ != n and math.hypot(b['x'] - a['x'], b['y'] - a['y']) < 72: hit(b, m_, a, t)
                if gum and math.hypot(gum['x'] - a['x'], gum['y'] - a['y']) < 55:
                    k = gum['kind']; fx.append((t, 'pick', n, a['x'], a['y'], k)); gum = None; next_gum = t + rnd.uniform(1.8, 3.0)
                    if k == 'mush': a['boost'] = t
                    elif k == 'acv': a['shield'] = t
                    elif k == 'cre':
                        a['strong'] = t
                        for m_ in NAMES:
                            b = ag[m_]
                            if m_ != n and math.hypot(b['x'] - a['x'], b['y'] - a['y']) < 300: hit(b, m_, a, t)
                    elif k == 'mel':
                        fx.append((t, 'sleepwave', n, a['x'], a['y']))
                        for m_ in NAMES:
                            b = ag[m_]
                            if m_ == n: continue
                            if b['shield'] is not None: b['shield'] = None; b['pop'] = t; fx.append((t, 'block', m_, b['x'], b['y'], 'sleep'))
                            else: b['sleep'] = t + SLEEP_T; b['vx'] = b['vy'] = 0.0; b['dizzy'] = -9.0; fx.append((t, 'sleep', m_, b['x'], b['y']))
            for n in NAMES:
                for m_ in NAMES:
                    if n >= m_: continue
                    a, b = ag[n], ag[m_]; dx, dy = a['x'] - b['x'], a['y'] - b['y']; dd = math.hypot(dx, dy)
                    if 0 < dd < 50:
                        for c_, sg in ((a, 1), (b, -1)):
                            nx, ny = c_['x'] + sg * dx / dd * (50 - dd) / 2, c_['y'] + sg * dy / dd * (50 - dd) / 2
                            gj, gi = int((ny - GY0) // CS), int((nx - GX0) // CS)
                            if 0 <= gj < GH and 0 <= gi < GW and LAND[gj, gi]: c_['x'], c_['y'] = nx, ny   # never pushed into the sea
        cnt = [(own == k).sum() / NL * 100 for k in range(NG)]
        frames.append((own.copy(), {n: {k_: a[k_] for k_ in ('x', 'y', 'vx', 'vy', 'dist', 'boost', 'strong', 'shield', 'sleep', 'dizzy', 'pop')} for n, a in ag.items()}, dict(gum) if gum else None, cnt))
    return frames, fx
def score(seed):
    fr, fx = sim(seed)
    T1f = int(T1 * FPS)
    final = fr[T1f - 1][3]; order = sorted(range(NG), key=lambda k: -final[k])
    leaders = []
    for f in range(int(8 * FPS), T1f, 15):
        c = fr[f][3]; l = max(range(NG), key=lambda k: c[k])
        if not leaders or leaders[-1] != l: leaders.append(l)
    margin = final[order[0]] - final[order[1]]
    kinds = set(e[5] for e in fx if e[1] == 'pick'); ev = [e[1] for e in fx]
    return NAMES[order[0]], round(margin, 1), len(leaders), [round(x, 1) for x in final], (len(kinds), ev.count('bonk'), ev.count('block'), ev.count('sleep'))
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for s_ in range(int(sys.argv[2]), int(sys.argv[3])):
        w_, mg, lc, fin, nfx = score(s_)
        if w_ == os.environ.get('WN', 'cyrus') and mg < 2.5 and lc >= 5 and nfx[0] == 4 and nfx[1] >= 1: print(s_, w_, mg, lc, fin, nfx, flush=True)
    sys.exit()
FR, FX = sim(SEED)
fin = FR[int(T1 * FPS) - 1][3]; WIN = NAMES[max(range(NG), key=lambda k: fin[k])]
print('winner', WIN, [round(x, 1) for x in fin])
# ---------- art
tiles = {i: Image.open(PL + f'race/tiles/tile_{i}.png').convert('RGBA') for i in (0, 15)}
GR = up(tiles[0], 2); DIRT = up(tiles[15], 2)
GROUND = Image.new('RGBA', (W, H), (0, 0, 0, 0))
landimg = Image.new('RGBA', (GW * CS, GH * CS))
for y in range(0, GH * CS, 64):
    for x in range(0, GW * CS, 64):
        g = GR if (x // 64 + y // 64) % 5 else GR.transpose(Image.FLIP_LEFT_RIGHT); landimg.alpha_composite(g, (x, y))
mask = Image.fromarray((LAND * 255).astype(np.uint8), 'L').resize((GW * CS, GH * CS), Image.NEAREST)
sand = Image.fromarray(((np.pad(LAND, 1)[2:, 1:-1] | np.pad(LAND, 1)[:-2, 1:-1] | np.pad(LAND, 1)[1:-1, 2:] | np.pad(LAND, 1)[1:-1, :-2] | LAND) * 255).astype(np.uint8), 'L').resize((GW * CS, GH * CS), Image.NEAREST)
SAND = Image.new('RGBA', landimg.size, (222, 196, 140, 255))
PROPS = [(up(crop(Image.open(SP + 'fork2/bigtree/00.png').convert('RGBA')), 1), HOME['joy']), (up(crop(Image.open(SP + 'fork2/moongate/00.png').convert('RGBA')), 2), HOME['ray']),
         (up(crop(Image.open(SP + 'fork2/smalltree/00.png').convert('RGBA')), 1), (cx0 - 60, cy0 - 40)), (up(crop(Image.open(SP + 'fork2/lantern/00.png').convert('RGBA')), 2), (cx0 + 70, cy0 + 50))]
HOOK, HB = hook_layer(['REALM WAR'], accent=0, sub='PICK WHO CONQUERS THE MAP')
TBY = HB + 10; LBY = HB + 46   # timer bar row, leaderboard chip row (both under the hook)
hdr = bg_frames('bg_castle.gif', (W, int(900 * W / 1600 * 1.0)), box=(0, 0, 1600, 900), step=2, bright=0.55)
FACE = {}
for n in NAMES:
    src = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}[n]
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); c_ = (bb[0] + bb[2]) // 2
    hd = im.crop((c_ - 15, 12, c_ + 15, 42)).resize((52, 52), Image.NEAREST)
    b = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(b); d.ellipse([0, 0, 63, 63], fill=COL[n] + (255,)); d.ellipse([5, 5, 58, 58], fill=(235, 232, 220, 255))
    mk = Image.new('L', (52, 52), 0); ImageDraw.Draw(mk).ellipse([0, 0, 51, 51], fill=255); b.paste(hd, (6, 6), Image.composite(hd, Image.new('RGBA', hd.size), mk).getchannel('A'))
    FACE[n] = b
SRUN = {g: seq(PL + f'race/{g}_run', 2, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', 2, 1, 9) for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', 2, 0, 1)[0] for g in NAMES}
VICF = vic(WIN, 380)
GUM = {k: gummy(k, 3) for k in GUMK}
FLAG = up(crop(Image.open(B7 + 'flag/12.png').convert('RGBA')), 3)
def tint_flag(c):
    a = np.array(FLAG).astype(int); wmask = (a[..., 0] > 200) & (a[..., 1] > 200) & (a[..., 3] > 0)
    for k in range(3): a[..., k][wmask] = (c[k] * a[..., k][wmask] / 255).astype(int)
    return Image.fromarray(a.astype(np.uint8))
FLAGS = {n: tint_flag(COL[n]) for n in NAMES}
cols = np.array([COL[n] for n in NAMES] + [(0, 0, 0)], np.uint8)
w = Writer('v67_noaudio.mp4'); events = []; OPEN = []
KEYF = [int(float(x) * FPS) for x in os.environ.get('KEYT', '').split(',') if x]
GCOL = {'mush': (255, 160, 40), 'acv': (110, 230, 90), 'mel': (190, 120, 255), 'cre': (90, 160, 255)}
RAWP = []     # (t0, guide, text, colour, size)
for e in FX:
    te, kind, n = e[0], e[1], e[2]
    if kind == 'pick':
        k = e[5]; RAWP.append((te, n, PW.POWER[k][0], PW.POWER[k][1], 42)); events.append((round(te, 3), PW.SFX[k]))
        if k == 'cre': events.append((round(te + 0.08, 3), 'boom'))
    elif kind == 'bonk': RAWP.append((te, n, 'BONK!', (255, 255, 255), 36)); events.append((round(te, 3), 'punch'))
    elif kind == 'block': RAWP.append((te, n, 'BLOCKED!', (110, 230, 90), 36)); events.append((round(te + 0.05, 3), 'chime'))
class Pops2(PW.Pops):
    """like PW.Pops but a label that can't stack upward (top clamp) tries below instead, so labels never overlap."""
    def items(self, t, avoid=()):
        act = [p for p in sorted(self.P, key=lambda p: p[0]) if 0 <= t - p[0] < self.dur]; placed = list(avoid); out = []
        for t0, x, y, text, col, size in act:
            u = t - t0; w = len(text) * size + 20; hh = size + 16
            y0 = max(y - u * 30, self.ymin + hh / 2)
            for k in (0, -1, 1, -2, 2, -3, 3, 4, 5):
                sy = y0 + k * (hh + 6)
                if sy < self.ymin + hh / 2 or sy > 1480: continue
                xmax = self.xmax if sy < 1110 else min(self.xmax, 880)
                sx = min(max(x, self.xmin + w / 2), xmax - w / 2)
                if not any(abs(sx - px) < (w + pw) / 2 and abs(sy - py) < (hh + ph) / 2 for px, py, pw, ph in placed): break
            placed.append((sx, sy, w, hh)); al = int(255 * min(1, (self.dur - u) / 0.3)); sc = 1 + 0.3 * max(0, 1 - u / 0.15)
            out.append((sx, sy - hh / 2, text, int(size * sc), col, 6, al))
        return out
POPS = Pops2(1.1, xmin=72, xmax=1010, ymin=LBY + 100)
def speedfx(img, x, y, vx, vy, t):
    v = math.hypot(vx, vy) or 1; ux, uy = vx / v, vy / v; qx, qy = -uy, ux
    def fn(dd):
        for q in range(4):
            off = (q - 1.5) * 30; ln = 60 + (q * 37 + int(t * 60)) % 50
            ax, ay = x - ux * (45 + 12 * q) + qx * off, y - 70 - uy * (45 + 12 * q) + qy * off
            dd.line([ax, ay, ax - ux * ln, ay - uy * ln], fill=(255, 240, 200, 220), width=7)
        for q in range(3):
            cx_, cy_ = x - ux * (34 + q * 26), y - uy * (34 + q * 26)
            dd.ellipse([cx_ - 15 + q * 2, cy_ - 12 - q * 3, cx_ + 15 - q * 2, cy_ + 8], fill=(225, 205, 160, 170 - q * 45))
    layer(img, fn)
def sprite_of(n, s, t):
    if t < T0 or t >= T1 or t < s['sleep'] or t < s['dizzy']: return STAND[n]
    v = math.hypot(s['vx'], s['vy']) or 1; ph = int(s['dist'] / 22) % 8
    return FRUN[n][ph] if s['vy'] > 0.7 * v else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
NF = int(TEND * FPS)
for f in range(NF):
    t = f / FPS; own, st, gum, cnt = FR[f]
    img = Image.new('RGBA', (W, H), (18, 40, 84, 255)); d = ImageDraw.Draw(img)
    # water ripples
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L); rr = random.Random(7)
    for _ in range(90):
        x0, y0 = rr.uniform(0, W), rr.uniform(HB, 1500); ox = (t * 18 + x0) % W
        dl.rectangle([ox, y0, ox + rr.choice([12, 18, 24]), y0 + 4], fill=(90, 150, 220, int(80 + 60 * math.sin(t * 2 + x0))))
    img.alpha_composite(L)
    bd = Image.new('RGBA', landimg.size, (0, 0, 0, 0)); bd.paste(SAND, (0, 0), sand); bd.paste(landimg, (0, 0), mask)
    o = own.copy(); o[o < 0] = NG
    rgb = cols[o]; al = np.where((own >= 0) & LAND, 150, 0).astype(np.uint8)
    edge = np.zeros_like(LAND)
    edge[:, 1:] |= o[:, 1:] != o[:, :-1]; edge[1:, :] |= o[1:, :] != o[:-1, :]
    rgb = rgb.copy(); rgb[edge & LAND] = (rgb[edge & LAND] * 0.55).astype(np.uint8); al = np.where(edge & LAND & (own >= 0), 210, al).astype(np.uint8)
    ov = Image.fromarray(np.dstack([rgb, al]), 'RGBA').resize((GW * CS, GH * CS), Image.NEAREST)
    bd.alpha_composite(ov)
    img.alpha_composite(bd, (GX0, GY0))
    for im_, (x, y) in PROPS: img.alpha_composite(im_, (int(x - im_.width / 2), int(y - im_.height + 20)))
    for n in NAMES:
        hx, hy = HOME[n]; fl = FLAGS[n]; img.alpha_composite(fl, (int(hx - 40), int(hy - fl.height - 10)))
    # gummy pickup (always a product gummy; its TYPE decides the power)
    if gum:
        g = GUM[gum['kind']]; bob = int(8 * math.sin(t * 5)); L = Image.new('RGBA', (W, H)); dl = ImageDraw.Draw(L)
        dl.ellipse([gum['x'] - 46, gum['y'] - 70 + bob, gum['x'] + 46, gum['y'] + 22 + bob], fill=GCOL[gum['kind']] + (70,)); img.alpha_composite(L)
        img.alpha_composite(g, (int(gum['x'] - g.width / 2), int(gum['y'] - g.height / 2 - 24 + bob)))
    # one-shot power fx under the guides
    for e in FX:
        u = t - e[0]
        if e[1] == 'pick' and 0 <= u < 0.45:
            PW.burst(img, e[3], e[4] - 70, u / 0.45, GCOL[e[5]], 12, 20, 130)
            if e[5] == 'cre':   # STRONG shock ring = the shove radius
                r = 60 + 240 * (u / 0.45); layer(img, lambda dd: dd.ellipse([e[3] - r, e[4] - r * 0.75, e[3] + r, e[4] + r * 0.75], outline=(120, 180, 255, int(240 * (1 - u / 0.45))), width=12))
        if e[1] == 'sleepwave' and 0 <= u < 0.7: PW.sleep_wave(img, e[3], e[4] - 70, u / 0.7, 900)
    # guides
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']; spr = sprite_of(n, s, t); x0, y0 = int(x - spr.width / 2), int(y - 156)
        live = T0 <= t < T1
        boosted = live and 0 <= t - s['boost'] < SPEED_T and t >= s['sleep'] and t >= s['dizzy']
        strong = live and 0 <= t - s['strong'] < STRONG_T
        layer(img, lambda dd: dd.ellipse([x - 26, y - 8, x + 26, y + 8], fill=(0, 0, 0, 90)))
        if boosted:
            for k in (3, 2, 1):
                p_ = FR[max(0, f - 3 * k)][1][n]; img.alpha_composite(PW.tinted(spr, (255, 170, 50), int(255 * (0.42 - 0.1 * k))), (int(p_['x'] - spr.width / 2), int(p_['y'] - 156)))
            speedfx(img, x, y, s['vx'], s['vy'], t)
        if strong: PW.strong_aura(img, spr, x0, y0, t, 6, 3)
        if live and t < s['sleep']:
            PW.sleepy(img, spr, x0, y0); PW.zzz(img, x - 10, y0 + 10, t - (s['sleep'] - SLEEP_T))
        else: img.alpha_composite(spr, (x0, y0))
        if live and t < s['dizzy']: PW.dizzy(img, x, y - 150, t)
        if s['shield'] is not None and live: PW.shield(img, x, y + 12, 190, 64)
        if 0 <= t - s['pop'] < 0.5: PW.shield_pop(img, x, y + 12, 190, (t - s['pop']) / 0.5, 64)
    for e in FX:
        u = t - e[0]
        if e[1] == 'bonk' and 0 <= u < 0.35: PW.bonk_burst(img, e[5], e[6] - 80, u / 0.35)
    if any(e[1] == 'sleepwave' and 0 <= t - e[0] < 0.25 for e in FX): img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 50)))
    POPS.P = [(t0, FR[int(round(t0 * FPS))][1][n_]['x'], FR[int(round(t0 * FPS))][1][n_]['y'] - 200, txt, col, sz) for (t0, n_, txt, col, sz) in RAWP]   # anchored where it happened (no jumping)
    POPS.ymin = LBY + (175 if T1 - 5 <= t < T1 else 100)   # keep pops clear of FINAL SECONDS!
    items = POPS.items(t) if t < T1 + 0.2 else []
    text_layer(img, items)
    # header
    hb = hdr[int(t * 6) % len(hdr)]; img.alpha_composite(hb.crop((0, 120, W, 120 + 330)), (0, 0))
    layer(img, lambda dd: dd.rectangle([0, 0, W, 330], fill=(14, 10, 24, 120)))
    layer(img, lambda dd: dd.rounded_rectangle([70, TBY - 4, 1025, LBY + 84], 14, fill=(14, 10, 24, 215)))
    d = ImageDraw.Draw(img)
    secs = max(0, int(math.ceil(T1 - max(t, T0)))) if t < T1 else 0
    tb = 1 - min(1, max(0, (t - T0) / (T1 - T0)))
    d.rounded_rectangle([84, TBY + 2, 890, TBY + 28], 10, fill=(20, 18, 40), outline=(200, 190, 255), width=3)
    d.rounded_rectangle([88, TBY + 6, 88 + int((886 - 92) * tb), TBY + 24], 8, fill=(90, 220, 120) if secs > 5 else (240, 80, 80))
    ctext(d, 957, TBY + 1, f'{secs}s', F(28), (255, 255, 255), 4)
    if T1 - 5 <= t < T1:
        text_layer(img, [(478, LBY + 110, 'FINAL SECONDS!', 44, (255, 90, 90), 7, int(255 * (0.6 + 0.4 * math.sin(t * 12))))])
        sc_ = int(math.ceil(T1 - t))
        if abs((T1 - t) - sc_) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
    if t < T0 + 1.2: text_layer(img, [(478, LBY + 110, 'PICK A GUIDE!', 48, (255, 255, 255), 7, int(255 * min(1, (T0 + 1.2 - t) / 0.3)))])
    # leaderboard
    order = sorted(range(NG), key=lambda k: -cnt[k])
    d = ImageDraw.Draw(img)
    for r, k in enumerate(order):
        n = NAMES[k]; x0 = 78 + r * 236.5; y = LBY
        d.rounded_rectangle([x0, y, x0 + 228, y + 78], 14, fill=(26, 22, 44), outline=COL[n], width=4)
        img.alpha_composite(FACE[n], (int(x0 + 7), y + 7)); d = ImageDraw.Draw(img)
        d.text((x0 + 78, y + 10), f'{r + 1}', font=F(20), fill=(255, 214, 60) if r == 0 else (200, 195, 220))
        pct = f'{cnt[k]:.0f}%'; tw_ = d.textlength(pct, font=F(30)); d.text((x0 + 218 - tw_, y + 10), pct, font=F(30), fill=(255, 255, 255))
        nm = LABEL[n] if n != 'ray' else 'RAYLEIGH'; d.text((x0 + 78, y + 46), nm, font=F(16), fill=COL[n])
        bw = int(140 * cnt[k] / max(1, max(cnt))); d.rounded_rectangle([x0 + 78, y + 66, x0 + 78 + max(6, bw), y + 72], 3, fill=COL[n])
    if t >= T1 + 0.3:
        u = t - T1 - 0.3; img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(160 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1110 - vf.height))
        k = NAMES.index(WIN)
        text_layer(img, [(478, 1150, LABEL[WIN] + ' CONQUERS', 52, (255, 214, 60), 8, 255), (478, 1225, f'THE REALM WITH {cnt[k]:.0f}%', 38, (255, 255, 255), 6, 255), (478, 1320, 'DID YOUR PICK WIN?', 36, COL[WIN], 6, 255)])
        if not any(e[1] == 'victory' for e in events): events.append((round(t, 3), 'victory')); events.append((round(t, 3), 'cheer'))
    img.alpha_composite(HOOK)
    w.write(img)
    if f < 9: OPEN.append(img.copy())
    if f in KEYF: img.convert('RGB').save(f'k67_{f}.png')
for im_ in OPEN: w.write(im_)          # loop: cut back to the opening
w.close(); json.dump(events, open('v67_ev.json', 'w')); print('HB', HB)
