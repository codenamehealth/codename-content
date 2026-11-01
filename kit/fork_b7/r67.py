import sys; sys.path.insert(0, '../fork1')
from common import *
import numpy as np
SEED = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] != 'search' else 0
NAMES = ['ray', 'joy', 'cyrus', 'cleo', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'HOLLOW'}
POWER = {'ray': 'TELEPORTS', 'joy': 'GROWS LIKE VINES', 'cyrus': 'FIRES SUN BEAMS', 'cleo': 'BUILDS WALLS', 'hollow': 'STEALS LAND'}
SHOUT = {'ray': 'TELEPORT!', 'joy': 'VINE BLOOM!', 'cyrus': 'SUN BEAM!', 'cleo': 'STONE WALLS!', 'hollow': 'LAND GRAB!'}
COL = {'joy': (90, 200, 80), 'cyrus': (245, 150, 40), 'cleo': (70, 130, 240), 'ray': (170, 80, 220), 'hollow': (110, 105, 140)}
# map grid
CS = 30; GX0, GY0 = 30, 370; GW, GH = 34, 34
cx0, cy0 = GX0 + GW * CS / 2, GY0 + GH * CS / 2
LOBES = [(cx0 + 330 * math.cos(-math.pi / 2 + k * 2 * math.pi / 5), cy0 + 330 * math.sin(-math.pi / 2 + k * 2 * math.pi / 5)) for k in range(5)]
HOME = {n: LOBES[i] for i, n in enumerate(NAMES)}
yy, xx = np.mgrid[0:GH, 0:GW]; px = GX0 + (xx + 0.5) * CS; py = GY0 + (yy + 0.5) * CS
LAND = np.zeros((GH, GW), bool)
for (lx, ly) in LOBES: LAND |= (px - lx) ** 2 + (py - ly) ** 2 < 205 ** 2
LAND |= (px - cx0) ** 2 + (py - cy0) ** 2 < 260 ** 2
NL = LAND.sum()
def sim(seed):
    rnd = random.Random(seed)
    own = np.full((GH, GW), -1, int)
    for i, n in enumerate(NAMES):
        hx, hy = HOME[n]; own[LAND & ((px - hx) ** 2 + (py - hy) ** 2 < 70 ** 2)] = i
    ag = {n: dict(x=HOME[n][0], y=HOME[n][1], vx=0.0, vy=0.0, tx=None, ty=None, rt=0, spd=rnd.uniform(215, 245), wall=-9, dist=0.0, ph=rnd.uniform(0, 6)) for n in NAMES}
    gum = None; next_gum = 2.5; frames = []; fx = []
    T0, T1 = 1.5, 31.5
    for f in range(int(34.5 * FPS)):
        t = f / FPS; dt = 1 / FPS
        if T0 <= t < T1:
            if gum is None and t >= next_gum:
                for _ in range(200):
                    gy_, gx_ = rnd.randrange(GH), rnd.randrange(GW)
                    if LAND[gy_, gx_] and min(math.hypot(px[gy_, gx_] - a['x'], py[gy_, gx_] - a['y']) for a in ag.values()) > 220: break
                gum = dict(x=px[gy_, gx_], y=py[gy_, gx_], kind=rnd.choice(['mush', 'acv', 'mel', 'cre', 'gold']), t=t)
            for i, n in enumerate(NAMES):
                a = ag[n]
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
                a['vx'] += (dx / L * sp - a['vx']) * 0.15; a['vy'] += (dy / L * sp - a['vy']) * 0.15
                nx, ny = a['x'] + a['vx'] * dt, a['y'] + a['vy'] * dt
                gj, gi = int((ny - GY0) // CS), int((nx - GX0) // CS)
                if 0 <= gj < GH and 0 <= gi < GW and LAND[gj, gi]: a['dist'] += math.hypot(nx - a['x'], ny - a['y']); a['x'], a['y'] = nx, ny
                else: a['vx'] *= -0.5; a['vy'] *= -0.5; a['rt'] = 0
                # paint
                m = LAND & ((px - a['x']) ** 2 + (py - a['y']) ** 2 < 62 ** 2)
                prot = np.zeros_like(own, bool)
                ci = NAMES.index('cleo')
                if t - ag['cleo']['wall'] < 4.0: prot = own == ci
                own[m & ~(prot & (own != i))] = i
                if gum and math.hypot(gum['x'] - a['x'], gum['y'] - a['y']) < 55:
                    fx.append((t, n, a['x'], a['y'], a['vx'], a['vy'], gum['kind'])); gum = None; next_gum = t + rnd.uniform(1.8, 3.0)
                    if n == 'joy':
                        own[LAND & ((px - a['x']) ** 2 + (py - a['y']) ** 2 < 190 ** 2) & ~(prot & (own != i))] = i
                    elif n == 'cyrus':
                        v = math.hypot(a['vx'], a['vy']) or 1; ux, uy = a['vx'] / v, a['vy'] / v
                        dist = (px - a['x']) * ux + (py - a['y']) * uy; perp = np.abs(-(px - a['x']) * uy + (py - a['y']) * ux)
                        own[LAND & (dist > 0) & (perp < 50) & ~(prot & (own != i))] = i
                    elif n == 'ray':
                        cnt = [(own == k).sum() for k in range(5)]; lead = max(range(5), key=lambda k: cnt[k] if k != i else -1)
                        ys, xs = np.where(own == lead)
                        if len(ys):
                            j = rnd.randrange(len(ys)); a['x'], a['y'] = px[ys[j], xs[j]], py[ys[j], xs[j]]; fx.append((t, 'ray_arrive', a['x'], a['y'], 0, 0, ''))
                            own[LAND & ((px - a['x']) ** 2 + (py - a['y']) ** 2 < 140 ** 2) & ~(prot & (own != i))] = i
                    elif n == 'cleo': a['wall'] = t
                    elif n == 'hollow':
                        cnt = [(own == k).sum() for k in range(5)]; lead = max(range(5), key=lambda k: cnt[k] if k != i else -1)
                        own[LAND & (own == lead) & ((px - a['x']) ** 2 + (py - a['y']) ** 2 < 230 ** 2) & ~(prot & (own != i))] = i
            # separate guides
            for n in NAMES:
                for m_ in NAMES:
                    if n >= m_: continue
                    a, b = ag[n], ag[m_]; dx, dy = a['x'] - b['x'], a['y'] - b['y']; dd = math.hypot(dx, dy)
                    if 0 < dd < 50: a['x'] += dx / dd * (50 - dd) / 2; a['y'] += dy / dd * (50 - dd) / 2; b['x'] -= dx / dd * (50 - dd) / 2; b['y'] -= dy / dd * (50 - dd) / 2
        cnt = [(own == k).sum() / NL * 100 for k in range(5)]
        frames.append((own.copy(), {n: dict(x=a['x'], y=a['y'], vx=a['vx'], vy=a['vy'], dist=a['dist'], wall=a['wall']) for n, a in ag.items()}, dict(gum) if gum else None, cnt))
    return frames, fx
def score(seed):
    fr, fx = sim(seed)
    T1 = int(31.5 * FPS)
    final = fr[T1 - 1][3]; order = sorted(range(5), key=lambda k: -final[k])
    leaders = []
    for f in range(int(8 * FPS), T1, 15):
        c = fr[f][3]; l = max(range(5), key=lambda k: c[k])
        if not leaders or leaders[-1] != l: leaders.append(l)
    margin = final[order[0]] - final[order[1]]
    return NAMES[order[0]], round(margin, 1), len(leaders), [round(x, 1) for x in final], len(fx)
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for s_ in range(int(sys.argv[2]), int(sys.argv[3])):
        w_, mg, lc, fin, nfx = score(s_)
        if mg < 4 and lc >= 4 and w_ in ('cyrus', 'cleo', 'joy'): print(s_, w_, mg, lc, fin, nfx, flush=True)
    sys.exit()
FR, FX = sim(SEED)
T0, T1 = 1.5, 31.5
fin = FR[int(T1 * FPS) - 1][3]; WIN = NAMES[max(range(5), key=lambda k: fin[k])]
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
hdr = bg_frames('bg_castle.gif', (W, int(900 * W / 1600 * 1.0)), box=(0, 0, 1600, 900), step=2, bright=0.55)
FACE = {}
for n in NAMES:
    src = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}[n]
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); c_ = (bb[0] + bb[2]) // 2
    hd = im.crop((c_ - 15, 12, c_ + 15, 42)).resize((52, 52), Image.NEAREST)
    b = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(b); d.ellipse([0, 0, 63, 63], fill=COL[n] + (255,)); d.ellipse([5, 5, 58, 58], fill=(235, 232, 220, 255))
    mk = Image.new('L', (52, 52), 0); ImageDraw.Draw(mk).ellipse([0, 0, 51, 51], fill=255); b.paste(hd, (6, 6), Image.composite(hd, Image.new('RGBA', hd.size), mk).getchannel('A'))
    FACE[n] = b
SRUN = {g: seq(PL + f'race/{g}_run', 2, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq(PL + 'maze/anim/hollow_srun', 2, 1, 9)
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', 2, 1, 9) for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', 2, 0, 1)[0] for g in NAMES}
VICF = vic(WIN, 380)
GUM = {k: gummy(k, 3) for k in GUMK}
FLAG = up(crop(Image.open('flag/12.png').convert('RGBA')), 3)
def tint_flag(c):
    a = np.array(FLAG).astype(int); wmask = (a[..., 0] > 200) & (a[..., 1] > 200) & (a[..., 3] > 0)
    for k in range(3): a[..., k][wmask] = (c[k] * a[..., k][wmask] / 255).astype(int)
    return Image.fromarray(a.astype(np.uint8))
FLAGS = {n: tint_flag(COL[n]) for n in NAMES}
cols = np.array([COL[n] for n in NAMES] + [(0, 0, 0)], np.uint8)
w = Writer('v67/noaudio.mp4'); events = []
fxi = 0; popups = []
for f in range(int(34.5 * FPS)):
    t = f / FPS; own, st, gum, cnt = FR[f]
    img = Image.new('RGBA', (W, H), (18, 40, 84, 255)); d = ImageDraw.Draw(img)
    # water ripples
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L); rr = random.Random(7)
    for _ in range(90):
        x0, y0 = rr.uniform(0, W), rr.uniform(330, 1430); ox = (t * 18 + x0) % W
        dl.rectangle([ox, y0, ox + rr.choice([12, 18, 24]), y0 + 4], fill=(90, 150, 220, int(80 + 60 * math.sin(t * 2 + x0))))
    img.alpha_composite(L)
    bd = Image.new('RGBA', landimg.size, (0, 0, 0, 0)); bd.paste(SAND, (0, 0), sand); bd.paste(landimg, (0, 0), mask)
    # territory overlay
    o = own.copy(); o[o < 0] = 5
    rgb = cols[o]; al = np.where((own >= 0) & LAND, 150, 0).astype(np.uint8)
    edge = np.zeros_like(LAND)
    edge[:, 1:] |= o[:, 1:] != o[:, :-1]; edge[1:, :] |= o[1:, :] != o[:-1, :]
    rgb = rgb.copy(); rgb[edge & LAND] = (rgb[edge & LAND] * 0.55).astype(np.uint8); al = np.where(edge & LAND & (own >= 0), 210, al).astype(np.uint8)
    ov = Image.fromarray(np.dstack([rgb, al]), 'RGBA').resize((GW * CS, GH * CS), Image.NEAREST)
    # cleo walls: stone border while active
    bd.alpha_composite(ov)
    img.alpha_composite(bd, (GX0, GY0))
    if t - st['cleo']['wall'] < 4.0:
        ci = NAMES.index('cleo'); e2 = np.zeros_like(LAND)
        mine = own == ci; e2[:, 1:] |= mine[:, 1:] != mine[:, :-1]; e2[1:, :] |= mine[1:, :] != mine[:-1, :]
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        for (j, i) in zip(*np.where(e2 & LAND)):
            x, y = GX0 + i * CS, GY0 + j * CS; dl.rectangle([x + 4, y + 4, x + CS - 4, y + CS - 4], fill=(150, 150, 165, 230), outline=(80, 80, 95, 255), width=3)
        img.alpha_composite(L)
    for im_, (x, y) in PROPS: img.alpha_composite(im_, (int(x - im_.width / 2), int(y - im_.height + 20)))
    for n in NAMES:
        hx, hy = HOME[n]; fl = FLAGS[n]; img.alpha_composite(fl, (int(hx - 40), int(hy - fl.height - 10)))
    # gummy pickup
    if gum:
        g = GUM[gum['kind']]; bob = int(8 * math.sin(t * 5)); L = Image.new('RGBA', (W, H)); dl = ImageDraw.Draw(L)
        dl.ellipse([gum['x'] - 46, gum['y'] - 70 + bob, gum['x'] + 46, gum['y'] + 22 + bob], fill=(255, 235, 150, 70)); img.alpha_composite(L)
        img.alpha_composite(g, (int(gum['x'] - g.width / 2), int(gum['y'] - g.height / 2 - 24 + bob)))
    # power fx
    while fxi < len(FX) and FX[fxi][0] <= t:
        te, n, x, y, vx, vy, kind = FX[fxi]; fxi += 1
        if n == 'ray_arrive': continue
        popups.append((te, n, x, y, vx, vy)); events.append((round(te, 3), 'powerup_8bit'))
        if n == 'cyrus': events.append((round(te + 0.05, 3), 'boom'))
        if n == 'ray': events.append((round(te + 0.1, 3), 'poof'))
        if n == 'hollow': events.append((round(te + 0.1, 3), 'whoosh_8bit'))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for (te, n, x, y, vx, vy) in popups:
        u = t - te
        if u > 1.4: continue
        if n == 'joy':
            r = 190 * min(1, u / 0.5); dl.ellipse([x - r, y - r, x + r, y + r], outline=(120, 230, 90, int(230 * (1 - u / 1.4))), width=14)
            for k in range(14):
                a = k * 0.45 + u * 2; dl.rectangle([x + r * math.cos(a) - 6, y + r * math.sin(a) - 6, x + r * math.cos(a) + 6, y + r * math.sin(a) + 6], fill=(60, 170, 60, int(255 * (1 - u / 1.4))))
        elif n == 'cyrus':
            v = math.hypot(vx, vy) or 1; ux, uy = vx / v, vy / v; ex, ey = x + ux * 1500, y + uy * 1500
            al = int(255 * max(0, 1 - u / 0.8)); dl.line([x, y - 40, ex, ey - 40], fill=(255, 220, 90, al), width=90); dl.line([x, y - 40, ex, ey - 40], fill=(255, 255, 220, al), width=34)
        elif n == 'ray':
            r = 140 * min(1, u / 0.4); dl.ellipse([x - r, y - r, x + r, y + r], outline=(200, 140, 255, int(230 * (1 - u / 1.4))), width=10)
        elif n == 'hollow':
            r = 230 * (1 - min(1, u / 0.7)); dl.ellipse([x - r, y - r, x + r, y + r], outline=(60, 50, 90, int(240 * (1 - u / 1.4))), width=18)
        elif n == 'cleo':
            dl.ellipse([x - 70, y - 120, x + 70, y + 20], outline=(180, 200, 255, int(230 * (1 - u / 1.4))), width=8)
    img.alpha_composite(L)
    # guides
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if t < T0 or t >= T1: spr = STAND[n]
        else:
            v = math.hypot(s['vx'], s['vy']) or 1; ph = int(s['dist'] / 22) % 8
            spr = FRUN[n][ph] if s['vy'] > 0.7 * v else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        layer(img, lambda dd: dd.ellipse([x - 26, y - 8, x + 26, y + 8], fill=(0, 0, 0, 90)))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - 156)))
    items = []
    for (te, n, x, y, vx, vy) in popups:
        u = t - te
        if 0 <= u < 1.3: items.append((x, y - 210 - u * 40, SHOUT[n], 30, COL[n], 6, int(255 * min(1, (1.3 - u) / 0.3))))
    text_layer(img, items)
    # header
    hb = hdr[int(t * 6) % len(hdr)]; img.alpha_composite(hb.crop((0, 120, W, 120 + 330)), (0, 0))
    layer(img, lambda dd: dd.rectangle([0, 0, W, 330], fill=(14, 10, 24, 120)))
    d = ImageDraw.Draw(img); ctext(d, W / 2, 50, 'REALM WAR', F(74), (255, 214, 60), 8); ctext(d, W / 2, 150, 'PICK WHO CONQUERS THE MAP', F(30), (255, 255, 255), 5)
    secs = max(0, int(math.ceil(T1 - max(t, T0)))) if t < T1 else 0
    tb = 1 - min(1, max(0, (t - T0) / (T1 - T0)))
    d.rounded_rectangle([240, 220, W - 240, 252], 12, fill=(20, 18, 40), outline=(200, 190, 255), width=3)
    d.rounded_rectangle([244, 224, 244 + int((W - 488) * tb), 248], 10, fill=(90, 220, 120) if secs > 5 else (240, 80, 80))
    ctext(d, W / 2, 268, f'{secs}s', F(28), (255, 255, 255), 4)
    if T1 - 5 <= t < T1:
        text_layer(img, [(W / 2, 360, 'FINAL SECONDS!', 44, (255, 90, 90), 7, int(255 * (0.6 + 0.4 * math.sin(t * 12))))])
        sc_ = int(math.ceil(T1 - t))
        if abs((T1 - t) - sc_) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
    if t < T0: text_layer(img, [(W / 2, 360, 'PICK A GUIDE!', 48, (255, 255, 255), 7, 255)])
    # leaderboard
    order = sorted(range(5), key=lambda k: -cnt[k])
    layer(img, lambda dd: dd.rectangle([0, 1420, W, H], fill=(14, 10, 24, 230)))
    d = ImageDraw.Draw(img)
    for r, k in enumerate(order):
        n = NAMES[k]; y = 1440 + r * 92
        d.rounded_rectangle([30, y, W - 30, y + 80], 14, fill=(26, 22, 44), outline=COL[n], width=4)
        img.alpha_composite(FACE[n], (44, y + 8)); d = ImageDraw.Draw(img)
        d.text((122, y + 18), LABEL[n], font=F(30), fill=(255, 255, 255)); d.text((122, y + 54), POWER[n], font=F(16), fill=(190, 180, 220))
        bw = int(330 * cnt[k] / max(1, max(cnt))); d.rounded_rectangle([560, y + 26, 560 + max(8, bw), y + 54], 6, fill=COL[n])
        pct = f'{cnt[k]:.0f}%'; tw_ = d.textlength(pct, font=F(30)); d.text((W - 50 - tw_, y + 24), pct, font=F(30), fill=(255, 255, 255))
    if t >= T1 + 0.3:
        u = t - T1 - 0.3; img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(160 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1100 - vf.height))
        k = NAMES.index(WIN)
        text_layer(img, [(W / 2, 1140, LABEL[WIN] + ' CONQUERS', 52, (255, 214, 60), 8, 255), (W / 2, 1215, f'THE REALM WITH {cnt[k]:.0f}%', 38, (255, 255, 255), 6, 255), (W / 2, 1320, 'DID YOUR PICK WIN?', 36, COL[WIN], 6, 255)])
        if not any(e[1] == 'victory' for e in events): events.append((round(t, 3), 'victory')); events.append((round(t, 3), 'cheer'))
    w.write(img)
    if f % 60 == 0: img.convert('RGB').resize((270, 480)).save(f'v67/p_{f:04d}.png')
w.close(); json.dump(events, open('v67/events.json', 'w'))
