import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
import numpy as np
import hook as HK
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
# rc10 review recut (source fork_sz86/v90/r90.py). Bennett APPROVED #90: one growing hole, slimes off the glass; only light trims + universal fixes.
# #90 Slimes eat all the glass: safe zone + hook + Bennett note (source fork_b9/v92/render.py):
# slimes stay OFF the glass: they live in the scene BEHIND the glass and eat it from that side, so there is ONE hole that
# starts at the bottom and grows bigger and bigger until the glass is gone (same rule as #32). Glass is near-opaque so the
# artwork only shows through the hole.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import pymunk
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 3
BITE = float(os.environ.get('BITE', '2.6'))
rnd = random.Random(SEED)
def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
_old, HB = band(['SLIMES EAT ALL', 'THE GLASS'], 1, 'HOW MANY SLIMES?', color=(130, 210, 255))   # old band kept only for its height: the window geometry (and so the sim) hangs off it
P0, P1 = HB + 10, HB + 80
from hook import hook_fade
HOOK, HBF = hook_fade(['SLIMES EAT ALL', 'THE GLASS'], accent=1, color=(130, 210, 255), size=64)   # hfg10: soft fade, no box; HOW MANY SLIMES? cut (caption asks)
CP0, CP1 = HBF + 22, HBF + 92    # hfg10: counter drawn right under the hook (geometry unchanged)                      # rc10: one-row counter panel (44px), was two rows of 36/30px
# ---------------- geometry: arched window (was x150-930, y400-1560)
X0, X1 = 136, 820; CXW = (X0 + X1) // 2; RA = (X1 - X0) // 2; YB = 1446; YR = P1 + 70 + RA
WX0, WY0 = X0, int(YR - RA); WW, WH = X1 - X0, YB - WY0
print('hook', HB, 'panel', P0, P1, 'glass', X0, WY0, X1, YB)
def inside(x, y): return (X0 <= x <= X1 and YR <= y <= YB) or ((x - CXW) ** 2 + (y - YR) ** 2 <= RA ** 2 and y < YR)
CELL = 10; GW, GH = WW // CELL + 1, WH // CELL + 1
INSIDE = np.zeros((GH, GW), bool)
for j in range(GH):
    for i in range(GW): INSIDE[j, i] = inside(WX0 + i * CELL + 5, WY0 + j * CELL + 5)
NTOT = INSIDE.sum()
MASKW = Image.new('L', (WW, WH), 0); md = ImageDraw.Draw(MASKW)
md.rectangle([0, YR - WY0, WW, WH], fill=255); md.ellipse([0, 0, WW, 2 * RA], fill=255)
# ---------------- reveal scene: Cleo at the castle gate (Liza's vit_hd), crop re-cut to the new window aspect
cw = int(1080 * WW / WH); REV = bg_frames('vit_hd.gif', (WW, WH), box=(1254 - cw // 2, 0, 1254 + cw // 2, 1080), step=2)
GROUND = YB - 56
CLEOV = vic('cleo', 380); CLEO_STAND = idle('cleo', 4)          # unchanged sizes
CRE = gummy('cre', 3)
PILE = [(-150, -20), (-100, 5), (130, -10), (175, 10), (-190, 15), (95, 20)]
# ---------------- glass texture: frosted and near-opaque (only the hole shows the scene)
gq = Image.new('RGBA', (WW // 4 + 1, WH // 4 + 1), (196, 222, 242, 252)); gd = ImageDraw.Draw(gq)
for k in range(-40, 80):
    x = k * 22
    gd.polygon([(x, 0), (x + 6, 0), (x + 6 - WH // 4 * 0.55, WH // 4), (x - WH // 4 * 0.55, WH // 4)], fill=(236, 246, 255, 254))
nrnd = random.Random(1)
for _ in range(700):
    x, y = nrnd.randrange(WW // 4), nrnd.randrange(WH // 4); gq.putpixel((x, y), nrnd.choice([(210, 232, 248, 252), (185, 212, 236, 252)]))
GLASS = up(gq, 4).crop((0, 0, WW, WH))
# ---------------- frame (gold + stone band with gummy gems; the old gold gem on top is now creatine)
FRAME = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(FRAME)
def arch_outline(d, pad, col, width):
    d.arc([X0 - pad, YR - RA - pad, X1 + pad, YR + RA + pad], 180, 360, fill=col, width=width)
    d.line([(X0 - pad + width // 2 - 1, YR), (X0 - pad + width // 2 - 1, YB + pad)], fill=col, width=width)
    d.line([(X1 + pad - width // 2, YR), (X1 + pad - width // 2, YB + pad)], fill=col, width=width)
    d.line([(X0 - pad, YB + pad - width // 2), (X1 + pad, YB + pad - width // 2)], fill=col, width=width)
arch_outline(fd, 40, (40, 30, 52, 255), 16); arch_outline(fd, 30, (120, 80, 28, 255), 14); arch_outline(fd, 22, (232, 182, 76, 255), 10)
arch_outline(fd, 15, (255, 226, 130, 255), 4); arch_outline(fd, 8, (120, 80, 28, 255), 8)
for kind, (gx, gy) in zip(['acv', 'cre', 'mush', 'mel', 'cre'], [(X0 - 22, YR + 120), (X1 + 22, YR + 120), (X0 - 22, YB - 80), (X1 + 22, YB - 80), (CXW, YR - RA - 22)]):
    g = up(acv_gummy_strong(), 3) if kind == 'acv' else gummy(kind, 3); fd.ellipse([gx - 34, gy - 34, gx + 34, gy + 34], fill=(40, 30, 52, 255), outline=(255, 214, 90, 255), width=5)
    FRAME.alpha_composite(g, (gx - g.width // 2, gy - g.height // 2))
# ---------------- wall background (castle stone, full bleed)
wm = json.load(open(PL + 'maze/walls_meta.json'))
wsh = Image.open(PL + 'maze/walls_sheet.png').convert('RGBA'); TL = wm['tileset_data']['tiles']
def tile(b): return up(wsh.crop((b['x'], b['y'], b['x'] + 32, b['y'] + 32)), 2)
BRICK = tile(TL[15]['bounding_box']); TOPT = tile(TL[6]['bounding_box'])
BG = Image.new('RGBA', (W, H), (14, 10, 22, 255))
for y in range(0, H, 64):
    for x in range(0, W, 64): BG.alpha_composite(BRICK if (y // 64 + x // 64) % 5 else TOPT, (x, y))
BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (10, 8, 20, 110)))   # hfg10: wall less dimmed (was 150) so it reads as the scene
TORCH = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(PL + 'maze/torch_anim/*.png'))]   # wall sconces
SL = slime_frames(2)
# ---------------- n16 (Oct 29 notes2, "physics need to be good on this"): real 2D physics (pymunk, fixed 1/480s step).
# Slimes are round rigid bodies with gravity, ground, window-jamb walls and slime-slime contact: they pile up on the ground,
# never float, only make small hops (<=150px). They bite the hole's rim where they can reach it; the glass over the hole cracks
# (0.2s of crack lines) and drops as rigid polygon pieces (exact cell shape of the glass that broke, same gravity, bounce,
# tumble, settle on the ground or on the slime pile), and the slimes eat the fallen pieces. Still ONE hole that only grows from
# its rim (bites and cracks both start at the rim), slimes stay on the scene side behind the glass. Newborn slimes pop out of
# their parent and grow over 0.25s. Glass dust from bites falls, bounces and settles before fading.
GS = float(os.environ.get('GS', '2200')); AIRMAX = int(os.environ.get('AIRMAX', '99')); HMAX = float(os.environ.get('HMAX', '240')); ROLL = int(os.environ.get('ROLL', '1')); RS_ = 30; REACH = float(os.environ.get('REACH', '48'))
SGY = YB + 2                                   # slime ground line (feet), just behind the frame's bottom edge
S0 = (CXW - 150, SGY - RS_)
def cell_of(x, y): return min(GH - 1, max(0, int((y - WY0) // CELL))), min(GW - 1, max(0, int((x - WX0) // CELL)))
def cpos(j, i): return WX0 + i * CELL + 5, WY0 + j * CELL + 5
eaten = np.zeros((GH, GW), bool)
def bite(x, y):
    cj, ci = cell_of(x, y); R = int(BITE) + 1; got = 0
    for jj in range(cj - R, cj + R + 1):
        for ii in range(ci - R, ci + R + 1):
            if 0 <= jj < GH and 0 <= ii < GW and INSIDE[jj, ii] and not eaten[jj, ii] and (ii - ci) ** 2 + (jj - cj) ** 2 <= BITE * BITE + 1:
                eaten[jj, ii] = True; got += 1
    return got
def rim_cells():
    e = eaten; nb = np.zeros_like(e)
    nb[1:, :] |= e[:-1, :]; nb[:-1, :] |= e[1:, :]; nb[:, 1:] |= e[:, :-1]; nb[:, :-1] |= e[:, 1:]
    return np.argwhere(INSIDE & ~e & nb)
space = pymunk.Space(); space.gravity = (0, GS); space.iterations = 60
for a_, b_ in (((X0 - 200, SGY), (X1 + 200, SGY)), ((X0, SGY + 50), (X0, -3000)), ((X1, SGY + 50), (X1, -3000))):
    sg = pymunk.Segment(space.static_body, a_, b_, 2); sg.friction = 0.9; sg.elasticity = 0.1; space.add(sg)
slimes = []
def add_slime(x, y, t, r0=RS_, vx=0.0, vy=0.0):
    b = pymunk.Body(1.0, pymunk.moment_for_circle(1.0, 0, RS_) if ROLL else float('inf')); b.position = (x, y); b.velocity = (vx, vy)
    sh = pymunk.Circle(b, r0); sh.friction = 1.2; sh.elasticity = 0.05; space.add(b, sh)
    s = dict(i=len(slimes), b=b, sh=sh, born=t, r=r0, hop=rnd.uniform(0, 6), chomp=-9.0, bite_cd=0.0, act=t + rnd.uniform(0.15, 0.4), air=False)
    slimes.append(s); return s
def grounded(b):
    """resting on something: any contact whose normal has a downward (supporting) component, or wedged and at rest"""
    sup = [False, False]
    def chk(arb):
        n = arb.normal; me_first = arb.shapes[0].body is b; sup[1] = True
        if (n.y > 0.2 if me_first else n.y < -0.2): sup[0] = True
    b.each_arbiter(chk)
    return sup[0] or (sup[1] and b.velocity.length < 40)
def airborne(b):
    c = [False]; b.each_arbiter(lambda arb: c.__setitem__(0, True)); return not c[0]
add_slime(*S0, -1.0)
SPLITS = [float(x) for x in os.environ.get('SPLITS', '0.6,1.3,2.1,3.0,4.2,5.6').split(',')]
events = []; shards = []; frames = []; DUR_MAX = 30
last_crunch = -1; t_done = None; NSUB = int(os.environ.get("NSUB", "16")); dts = 1 / FPS / NSUB; bites_n = 0; air_bites = 0; maxpen = 0.0; penlog = []
def do_bite(s, x, y, t):
    global last_crunch, bites_n
    if bite(x, y):
        s['chomp'] = t; s['bite_cd'] = t + 0.2; bites_n += 1
        for _ in range(3): shards.append(dict(x=x, y=y, vx=rnd.uniform(-170, 170), vy=rnd.uniform(-300, -60), t=t, rest=None))
        if t - last_crunch > 0.16: events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
        return True
    return False
from scipy.spatial import ConvexHull
chunks = []; pending = []; next_chunk = float(os.environ.get('CH0', '0.9')); nchunks = 0; chunk_bites = 0
CH_RATE = float(os.environ.get('CHR', '1.5')); CH_RMIN, CH_RMAX = float(os.environ.get('CRMIN', '3')), float(os.environ.get('CRMAX', '5'))
CH_BITE = float(os.environ.get('CHB', '30')); CAP0 = int(os.environ.get('CAP0', '3')); CAPD = int(os.environ.get('CAPD', '3'))
def overhang():
    e = eaten; below = np.zeros_like(e); below[:-1, :] = e[1:, :]
    m = INSIDE & ~e & below
    for p in pending: m &= ~p['cells']
    return np.argwhere(m)
def make_chunk(t, cells):
    idx = np.argwhere(cells); n = len(idx)
    pts = []
    for j, i in idx:
        x0_, y0_ = WX0 + i * CELL, WY0 + j * CELL; pts += [(x0_, y0_), (x0_ + CELL, y0_), (x0_, y0_ + CELL), (x0_ + CELL, y0_ + CELL)]
    pts = np.array(pts, float); cx_, cy_ = pts.mean(0)
    hull = pts[ConvexHull(pts).vertices]; verts = [((x - cx_) * 0.93, (y - cy_) * 0.93) for x, y in hull]
    mass = 0.012 * n; body = pymunk.Body(mass, pymunk.moment_for_poly(mass, verts)); body.position = (cx_, cy_)
    body.velocity = (rnd.uniform(-40, 40), 0); body.angular_velocity = rnd.uniform(-1.5, 1.5)
    sh = pymunk.Poly(body, verts); sh.friction = 0.9; sh.elasticity = 0.12; space.add(body, sh)
    # sprite: the exact glass texture of these cells, centred on the centroid (so it rotates with the body)
    j0, i0 = idx.min(0); j1, i1 = idx.max(0) + 1
    bx0, by0 = i0 * CELL, j0 * CELL; crop_ = GLASS.crop((bx0, by0, i1 * CELL, j1 * CELL))
    sub = cells[j0:j1, i0:i1]
    m = Image.fromarray((sub * 255).astype(np.uint8), 'L').resize(crop_.size, Image.NEAREST)
    a_ = np.minimum(np.asarray(crop_.getchannel('A')), np.asarray(m)); crop_.putalpha(Image.fromarray(a_))
    inner = sub.copy(); inner[1:, :] &= sub[:-1, :]; inner[:-1, :] &= sub[1:, :]; inner[:, 1:] &= sub[:, :-1]; inner[:, :-1] &= sub[:, 1:]
    inner[0, :] = False; inner[-1, :] = False; inner[:, 0] = False; inner[:, -1] = False
    ed = Image.fromarray(((sub & ~inner) * 255).astype(np.uint8), 'L').resize(crop_.size, Image.NEAREST)
    el = Image.new('RGBA', crop_.size, (255, 255, 255, 0)); el.putalpha(ed.point(lambda v: 200 if v else 0)); crop_.alpha_composite(el)
    R_ = int(math.ceil(max(math.hypot(x, y) for x, y in pts - (cx_, cy_)))) + 2
    spr = Image.new('RGBA', (2 * R_, 2 * R_), (0, 0, 0, 0)); spr.alpha_composite(crop_, (int(round(WX0 + bx0 - cx_ + R_)), int(round(WY0 + by0 - cy_ + R_))))
    c = dict(b=body, sh=sh, spr=spr, n=n, n0=n, t=t, verts=verts, k=len(chunks)); chunks.append(c); return c
def bite_chunk(s, c, t):
    global last_crunch, chunk_bites
    c['n'] -= CH_BITE; s['chomp'] = t; s['bite_cd'] = t + 0.22; chunk_bites += 1
    x, y = c['b'].position
    for _ in range(3): shards.append(dict(x=x, y=y, vx=rnd.uniform(-170, 170), vy=rnd.uniform(-300, -60), t=t, rest=None))
    if t - last_crunch > 0.16: events.append((round(t, 3), 'crunch_8bit')); last_crunch = t
    space.remove(c['sh'])
    if c['n'] <= 0: space.remove(c['b']); c['dead'] = t; return
    k = math.sqrt(c['n'] / c['n0']); c['sh'] = pymunk.Poly(c['b'], [(x_ * k, y_ * k) for x_, y_ in c['verts']]); c['sh'].friction = 0.9; c['sh'].elasticity = 0.12; space.add(c['sh'])
for f in range(int(DUR_MAX * FPS)):
    t = f / FPS
    if SPLITS and t >= SPLITS[0]:
        SPLITS.pop(0)
        for s in list(slimes):
            b = s['b']; d = rnd.choice((-1, 1))
            add_slime(b.position.x + d * 8, b.position.y - 2, t, r0=RS_ * 0.35, vx=b.velocity.x + d * 140, vy=b.velocity.y - 120)
            b.velocity = (b.velocity.x - d * 140, b.velocity.y - 60)
        events.append((round(t, 3), 'boing'))
    for s in slimes:
        if s['r'] < RS_:
            s['r'] = min(RS_, RS_ * (0.35 + 0.65 * (t - s['born']) / 0.25)); s['sh'].unsafe_set_radius(s['r'])
    live = [c for c in chunks if 'dead' not in c]
    if t_done is None:
        if t >= 0.1 and not eaten.any(): do_bite(slimes[0], *S0, t)
        # the glass over the hole cracks (0.2s of crack lines) and the piece drops
        for p in list(pending):
            if t >= p['t'] + 0.2:
                pending.remove(p); eaten[p['cells']] = True; make_chunk(t, p['cells']); nchunks += 1
        if t >= next_chunk and len(live) + len(pending) < CAP0 + len(slimes) // CAPD:
            oh = overhang()
            if len(oh):
                j, i = oh[rnd.randrange(len(oh))]; rc = rnd.uniform(CH_RMIN, CH_RMAX)
                jj, ii = np.ogrid[:GH, :GW]; disk = ((jj - j) ** 2 + (ii - i) ** 2 <= rc * rc) & INSIDE & ~eaten
                for p in pending: disk &= ~p['cells']
                if disk.sum() >= 6 or (disk.sum() >= 1 and (INSIDE & ~eaten).sum() < 300): pending.append(dict(cells=disk, t=t))
            next_chunk = t + max(0.05, CH_RATE / (len(slimes) ** 0.5 + 1)) * rnd.uniform(0.7, 1.3)
        rim = rim_cells()
        RP = np.array([cpos(j, i) for j, i in rim], float) if len(rim) else np.zeros((0, 2))
        rest = [c for c in live if c['b'].velocity.length < 80 and t - c['t'] > 0.25]
        nair = sum(1 for s in slimes if airborne(s['b']))
        for s in slimes:
            b = s['b']; x, y = b.position
            if s['r'] < RS_ * 0.95: continue
            if rest and t >= s['bite_cd']:   # eat a fallen piece of glass right next to it
                dd = [math.hypot(c['b'].position.x - x, c['b'].position.y - y) - math.sqrt(max(c['n'], 1) / math.pi) * CELL for c in rest]
                k = int(np.argmin(dd))
                if dd[k] < s['r'] + 16:
                    bite_chunk(s, rest[k], t); rest = [c for c in rest if 'dead' not in c]; continue
            if len(RP) and t >= s['bite_cd']:   # or bite the hole's rim if it can reach it
                d2 = (RP[:, 0] - x) ** 2 + (RP[:, 1] - y) ** 2; k = int(np.argmin(d2))
                if d2[k] <= REACH * REACH:
                    if do_bite(s, RP[k, 0], RP[k, 1], t):
                        rim = rim_cells(); RP = np.array([cpos(j, i) for j, i in rim], float) if len(rim) else np.zeros((0, 2)); continue
            if t >= s['act'] and nair < AIRMAX and grounded(b) and b.velocity.length < 80:
                if rest:   # hop over to the nearest fallen piece
                    c = min(rest, key=lambda c: abs(c['b'].position.x - x) + rnd.uniform(0, 40)); tx = c['b'].position.x; hj = 70.0
                elif len(RP):   # small hop up at the lowest rim it can reach
                    ok = (y - RP[:, 1]) <= HMAX + REACH * 0.7
                    if not ok.any(): s['act'] = t + 0.3; continue
                    sc = np.abs(RP[:, 0] - x) + 0.8 * np.maximum(0, y - RP[:, 1]) + np.where(ok, 0, 1e6) + np.random.RandomState(f * 131 + s['i']).uniform(0, 60, len(RP))
                    k = int(np.argmin(sc)); tx, ty = RP[k]; hj = min(HMAX, max(60.0, y - ty + 6))
                else: continue
                vy = -math.sqrt(2 * GS * hj); tair = 2 * (-vy) / GS
                vx = max(-380, min(380, (tx - x) / (tair if hj < 100 else tair / 2)))
                b.velocity = (vx, vy); s['act'] = t + 0.35 + rnd.uniform(0, 0.4); nair += 1
        left_frac = 1 - eaten[INSIDE].sum() / NTOT
        if left_frac <= 0.0 and not pending and not live:
            t_done = t; events.append((round(t, 3), 'victory'))
            for s in slimes: s['cel'] = [t + 0.15 + rnd.uniform(0, 0.5), t + 0.75 + rnd.uniform(0, 0.4)]
    else:
        for s in slimes:
            if s.get('cel') and t >= s['cel'][0] and grounded(s['b']):
                s['cel'].pop(0); s['b'].velocity = (rnd.uniform(-60, 60), -rnd.uniform(560, 760))
    for _ in range(NSUB): space.step(dts)
    for sd in shards:
        if sd['rest'] is not None: continue
        for _ in range(4):
            dd_ = 1 / FPS / 4; sd['vy'] += GS * dd_; sd['x'] += sd['vx'] * dd_; sd['y'] += sd['vy'] * dd_
            if sd['y'] > SGY - 4:
                sd['y'] = SGY - 4; sd['vy'] *= -0.35; sd['vx'] *= 0.55
                if abs(sd['vy']) < 60: sd['vy'] = 0; sd['vx'] = 0; sd['rest'] = t; break
    shards = [sd for sd in shards if t - sd['t'] < 2.2]
    full = [s for s in slimes if t - s['born'] > 0.4]
    P = np.array([s['b'].position for s in full]); Rr = np.array([s['r'] for s in full])
    if len(P) > 1:
        D = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)) + np.eye(len(P)) * 1e9
        pen = (Rr[:, None] + Rr[None, :] - D).max(); maxpen = max(maxpen, pen)
        if pen > 4: penlog.append((round(t, 2), round(pen, 1)))
    left_frac = 1 - eaten[INSIDE].sum() / NTOT
    pend_mask = np.zeros_like(eaten)
    for p in pending: pend_mask |= p['cells']
    frames.append(([dict(x=s['b'].position.x, y=s['b'].position.y, r=s['r'], born=s['born'], chomp=s['chomp'], hop=s['hop'], vy=s['b'].velocity.y) for s in slimes],
                   eaten.copy(), max(0.0, left_frac + sum(c['n'] for c in chunks if 'dead' not in c) / NTOT) if t_done is None else 0.0,
                   [(sd['x'], sd['y'], sd['t'], sd['rest']) for sd in shards],
                   [(c['k'], c['b'].position.x, c['b'].position.y, c['b'].angle, max(0.0, c['n']) / c['n0']) for c in chunks if 'dead' not in c], pend_mask))
    if t_done is not None and t > t_done + 1.5: break
print('chunks', nchunks, 'chunk bites', chunk_bites, 'max live chunks', max(len(fr[4]) for fr in frames))
airs = [sum(1 for s_ in fr[0] if abs(s_['vy']) > 80) for fr in frames]; print('max airborne', max(airs), 'mean', round(sum(airs) / len(airs), 1))
print('done eating at', t_done, 'slimes', len(slimes), 'frames', len(frames), 'bites', bites_n, 'air bites', air_bites, 'max slime overlap px', round(maxpen, 1))
from scipy import ndimage
ncomp = max(ndimage.label(fr[1])[1] for fr in frames[::5])
print('max holes', ncomp); print('overlap>4px frames', len(penlog), penlog[:12])
print('glass left at 2/3/5/8/10s', [round(frames[min(len(frames) - 1, int(x * FPS))][2], 2) for x in (2, 3, 5, 8, 10, 11, 12, 13)]); print('live chunks at 8,10,11,12,13', [len(frames[min(len(frames) - 1, int(x * FPS))][4]) for x in (8, 10, 11, 12, 13)])
ys = [min(s['y'] for s in fr[0]) for fr in frames]; print('highest slime y', round(min(ys)), 'window top', WY0)
if len(sys.argv) > 2 and sys.argv[2] == 'sim': sys.exit()
# ---------------- render
out = Writer('v90_noaudio.mp4' if not os.environ.get('ONLY') else 'quick_tmp.mp4'); NF = len(frames)
SAVE = (0, 10, 45, 90, 150, 200, 250, 300, int(t_done * FPS) - 15, int(t_done * FPS) + 20, NF - 1)
ONLYF = set(int(x) for x in os.environ.get('ONLY', '').split(',') if x)
for f in range(NF):
    if ONLYF and f not in ONLYF: continue
    t = f / FPS; sl, em, left, shs, chs, pend = frames[f]
    img = BG.copy()
    for k, tx_ in enumerate((96, W - 210)):
        fr = TORCH[(int(t * 10) + k * 3) % len(TORCH)]; img.alpha_composite(fr, (tx_ - fr.width // 2, 760 - fr.height))
    win = REV[int(t * 6) % len(REV)].copy()
    rv = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rv.alpha_composite(win, (WX0, WY0))
    for (px, py) in PILE: rv.alpha_composite(CRE, (CXW + 60 + px - CRE.width // 2, GROUND + 6 + py - CRE.height))
    # fallen / falling glass pieces (rigid polygons, drawn at their body pose)
    for k, x, y, ang, frac in chs:
        sp = chunks[k]['spr']
        if frac < 0.999: sp = sp.resize((max(1, int(sp.width * math.sqrt(frac))), max(1, int(sp.height * math.sqrt(frac)))), Image.NEAREST)
        sp = sp.rotate(-math.degrees(ang), resample=Image.NEAREST, expand=True)
        rv.alpha_composite(sp, (int(round(x - sp.width / 2)), int(round(y - sp.height / 2))))
    # slimes (scene side, behind the glass)
    for k, s in enumerate(sorted(sl, key=lambda s: s['y'])):
        fr = SL[int(t * 10 + s['hop'] * 3) % len(SL)]
        k_ = s['r'] / RS_
        if t - s['chomp'] < 0.12: fr = fr.resize((int(fr.width * 1.15 * k_), int(fr.height * 0.88 * k_)), Image.NEAREST)
        elif k_ < 1: fr = fr.resize((max(1, int(fr.width * k_)), max(1, int(fr.height * k_))), Image.NEAREST)
        feet = s['y'] + s['r']; fh = 124 * fr.height / 128   # sprite feet row (native 62 of 64) sits on the body's bottom
        rv.alpha_composite(fr, (int(round(s['x'] - fr.width / 2)), int(round(feet - fh))))
    # Cleo always in front of the slimes (never hidden), behind the glass until it is eaten
    if t_done is not None and t >= t_done:
        cf = CLEOV[int((t - t_done) * 8) % len(CLEOV)]; rv.alpha_composite(cf, (CXW + 60 - cf.width // 2, GROUND + 6 - cf.height))
    else:
        st = CLEO_STAND[int(t * 6) % len(CLEO_STAND)]; rv.alpha_composite(st, (CXW + 60 - st.width // 2, GROUND + 6 - 78 * 4))
    # glass with the one hole
    gm = Image.fromarray((~em).astype(np.uint8) * 255, 'L').resize((GW * CELL, GH * CELL), Image.NEAREST).crop((0, 0, WW, WH))
    gl = GLASS.copy(); a = np.array(gl.getchannel('A')).astype(np.uint16) * np.array(gm).astype(np.uint16) // 255
    gl.putalpha(Image.fromarray(a.astype(np.uint8))); rv.alpha_composite(gl, (WX0, WY0))
    edge = (~em) & (np.roll(em, 1, 0) | np.roll(em, -1, 0) | np.roll(em, 1, 1) | np.roll(em, -1, 1)) & INSIDE
    if edge.any():
        e = Image.fromarray(edge.astype(np.uint8) * 200, 'L').resize((GW * CELL, GH * CELL), Image.NEAREST).crop((0, 0, WW, WH))
        el = Image.new('RGBA', (WW, WH), (255, 255, 255, 0)); el.putalpha(e); rv.alpha_composite(el, (WX0, WY0))
    if pend.any():   # crack lines around the piece that is about to drop
        inner = pend & np.roll(pend, 1, 0) & np.roll(pend, -1, 0) & np.roll(pend, 1, 1) & np.roll(pend, -1, 1)
        e = Image.fromarray(((pend & ~inner) * 255).astype(np.uint8), 'L').resize((GW * CELL, GH * CELL), Image.NEAREST).crop((0, 0, WW, WH))
        el = Image.new('RGBA', (WW, WH), (70, 100, 140, 0)); el.putalpha(e.point(lambda v: 235 if v else 0)); rv.alpha_composite(el, (WX0, WY0))
    L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(L2)
    for x, y, t0, rest in shs:
        a = 230 if rest is None or t - rest < 0.8 else int(230 * max(0, 1 - (t - rest - 0.8) / 0.5))
        if a > 0: sd.rectangle([x - 4, y - 4, x + 4, y + 4], fill=(225, 240, 255, a))
    rv.alpha_composite(L2)
    mk = Image.new('L', (W, H), 0); mk.paste(MASKW, (WX0, WY0))
    img.paste(rv, (0, 0), Image.composite(rv.getchannel('A'), Image.new('L', (W, H), 0), mk))
    img.alpha_composite(FRAME)
    # counter panel under the hook
    layer(img, lambda d: d.rectangle([0, CP0, W, CP1], fill=(10, 8, 20, 170)))   # hfg10: edge-to-edge strip, no box
    if t_done is not None and t >= t_done:
        u = t - t_done; sc_ = min(1.0, u / 0.25)
        text_layer(img, [(547, (CP0 + CP1) / 2 - int(56 * (0.6 + 0.4 * sc_)) / 2, 'ALL GONE!', int(56 * (0.6 + 0.4 * sc_)), (255, 214, 60), 8, 255)])
    else:
        text_layer(img, [(310, CP0 + 13, f'GLASS {int(math.ceil(left * 100)) if left > 0 else 0}%', 44, (225, 240, 255), 7, 255),
                         (784, CP0 + 13, f'SLIMES {len(sl)}', 44, (150, 235, 110), 7, 255)])
    img.alpha_composite(HOOK)
    out.write(img)
    if f in SAVE or f in ONLYF: img.convert('RGB').save(f'f90_{f}.png')
out.close()
json.dump({'events': events}, open('v90_ev.json', 'w')); print('rendered', NF / FPS)
