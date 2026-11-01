import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import pymunk
os.chdir(SP + 'fork_a6'); OUT = SP + 'fork_n10/v58/'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['CAN YOU CALL', 'THE TOP 3?'], accent=1, fade_to=640)   # Oct 29 n10: job hook (call the podium), soft fade
P0, P1 = HB + 10, HB + 196; print('HB', HB)
XL, XR = 90, 860; DY = 520
def X(x): return XL + (x - 44) * (XR - XL) / 992
CX = (XL + XR) / 2
NAMES = ['joy', 'cyrus', 'ray', 'cleo']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
CUT = 1240  # Trapdoors stage removed: everything below it moves up
MR = 45; WH = 6000 - CUT + DY; T_GO = 0.3   # review3: marbles rest on a visible gate until GO!
SEGS = []        # static course segments (a, b, radius, kind)
PEGS = []        # crystal pegs (x, y, r)
SLIMES = []      # slime bumpers (x, y, r)
WHEELS = [(360, 2980 + DY, 130, 1.7), (590, 3380 + DY, 130, -1.9)]   # review3: >=110px between spoke tips and the walls (Joy was pinned against the wall by the spoke tips)
SHELVES = []     # (y, trap_x0, trap_x1, phase)
SIGNS = [(y + DY, s) for y, s in [(560, 'CRYSTAL CAVERN'), (1610, 'SLIME BOUNCERS'), (2740, 'WATERWHEELS'), (4880 - CUT, 'FINAL STRETCH')]]
def seg(a, b, r=10, kind='stone'): SEGS.append(((X(a[0]), a[1] + DY), (X(b[0]), b[1] + DY), r, kind))
seg((44, -DY), (44, WH + 300), 16, 'wall'); seg((1036, -DY), (1036, WH + 300), 16, 'wall'); seg((44, 5980 - CUT), (1036, 5980 - CUT), 20)
seg((60, 300), (380, 470)); seg((1020, 300), (700, 470))   # review2: start funnel wider so true-size marbles can't arch-jam
for j, y in enumerate(range(620, 1500, 140)):   # review2: peg field re-spaced for the true-size marbles (no wedging pockets)
    for x in ([255, 445, 635, 825] if j % 2 == 0 else [350, 540, 730]): PEGS.append((X(x), y + DY, 13))
_pr = random.Random(58); PEGTILT = [_pr.choice([-1, 1]) * _pr.uniform(0.05, 0.09) for _ in PEGS]   # review4: pegs tilted 3-5 deg so nothing balances on a tip
def peg_pts(i, x, y, r):
    a = PEGTILT[i]; ca, sa = math.cos(a), math.sin(a)
    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in [(0, -r - 8), (r, 0), (0, r + 8), (-r, 0)]]
for j, y in enumerate(range(1720, 2620, 175)):
    row = [298, 475, 652] if j % 2 == 0 else [386, 564]   # review2: wall-hugging slimes removed (they made corner pockets for the true-size marbles)
    for x in row: SLIMES.append((x, y + DY, 36))
print('slimes', SLIMES)
seg((1020, 2700), (720, 2780)); seg((60, 2700), (330, 2770))
C = CUT
seg((60, 4950 - C), (420, 5150 - C)); seg((1020, 5250 - C), (660, 5450 - C)); seg((60, 5520 - C), (440, 5700 - C)); seg((1020, 5520 - C), (640, 5700 - C))
FIN_Y = 5700 - C + DY + 10      # review2: finish = entering the single-file chute under the last funnel
JT = FIN_Y + 75                  # jar top (world y); marbles drop behind the jar and are removed once fully hidden
SEGS.append(((CX - 68, FIN_Y + 12), (CX - 68, JT + 20), 8, 'chute')); SEGS.append(((CX + 68, FIN_Y + 12), (CX + 68, JT + 20), 8, 'chute'))   # review4: 110px inside, tops tucked under the funnel lips
def trap_open(k, t):
    y, x0, x1, ph = SHELVES[k]
    return ((t - T_GO + ph) % 1.6) < 0.8
KLOG = []
DBGQ = None
import numpy as _np
_sl = Image.open(sorted(glob.glob(PL + 'race/slime_idle_c/*.png'))[1]).convert('RGBA'); _sl = _sl.resize((_sl.width * 2, _sl.height * 2), Image.NEAREST)
_a = _np.array(_sl)[:, :, 3] > 0; SLIME_HULL = []
for _y in range(_a.shape[0]):
    _xs = _np.where(_a[_y])[0]
    if len(_xs): SLIME_HULL += [(_xs[0] - _sl.width / 2, _y - _sl.height / 2 - 24), (_xs[-1] + 1 - _sl.width / 2, _y - _sl.height / 2 - 24)]
def sim(seed, dur=45, record=True):
    rnd = random.Random(seed)
    sp = pymunk.Space(); sp.gravity = (0, 1650)
    for (a, b, r, kind) in SEGS:
        s = pymunk.Segment(sp.static_body, a, b, r if kind == 'wall' else r + 5); s.friction = 0.5; s.elasticity = 0.45; sp.add(s)
    for i_, (x, y, r) in enumerate(PEGS):
        c = pymunk.Poly(sp.static_body, peg_pts(i_, x, y, r)); c.elasticity = 0.7; c.friction = 0.3; sp.add(c)   # same diamond as drawn
    for (x, y, r) in SLIMES:
        c = pymunk.Poly(sp.static_body, [(x + 36 * math.cos(q * math.pi / 12), y + 12 + 24 * math.sin(q * math.pi / 12)) for q in range(24)]); c.elasticity = 0.9; c.friction = 0.2; c.collision_type = 3; sp.add(c)   # slime body as drawn (2x), springy but no energy gain
    wheels = []
    for (x, y, R, w) in WHEELS:
        b = pymunk.Body(body_type=pymunk.Body.KINEMATIC); b.position = (x, y); b.angular_velocity = w; sp.add(b)
        for k in range(6):
            a = k * math.pi / 3; s = pymunk.Segment(b, (0, 0), (R * math.cos(a), R * math.sin(a)), 11); s.friction = 0.6; s.elasticity = 0.3; sp.add(s)
        hub = pymunk.Circle(b, 28); sp.add(hub); wheels.append(b)   # spoke/hub thickness = drawn thickness
    traps = []
    for (y, x0, x1, ph) in SHELVES:
        s = pymunk.Segment(sp.static_body, (x0, y + 24), (x1, y + 24), 10); s.friction = 0.5; s.elasticity = 0.3; sp.add(s); traps.append([s, True])
    gate = pymunk.Segment(sp.static_body, (X(60), 230 + DY), (X(1020), 230 + DY), 8); sp.add(gate)
    balls = {}
    xs = [X(300), X(460), X(620), X(780)]; rnd.shuffle(xs)
    for n, x in zip(NAMES, xs):
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, MR)); b.position = (x + rnd.uniform(-15, 15), 230 + DY - 8 - MR - 2)   # resting on the gate
        c = pymunk.Circle(b, MR); c.friction = 0.4; c.elasticity = 0.55; c.collision_type = 1; sp.add(b, c); balls[n] = b
    bounces = []
    def on_bounce(arb, space, data):
        bounces.append((cur_t[0], tuple(arb.contact_point_set.points[0].point_a) if arb.contact_point_set.points else (0, 0)))
    try:
        sp.on_collision(1, 3, begin=lambda arb, space, data: on_bounce(arb, space, data))
    except Exception:
        h = sp.add_collision_handler(1, 3); h.begin = lambda arb, space, data: (on_bounce(arb, space, data), True)[1]
    cur_t = [0.0]; lastbo = {}
    fin = {}; frames = []; leaders = []; still = {n: 0 for n in NAMES}
    for f in range(int(dur * FPS)):
        t = f / FPS; cur_t[0] = t
        if t >= T_GO and gate is not None: sp.remove(gate); gate = None
        for k, tr in enumerate(traps):
            op = trap_open(k, t)
            if op and tr[1]: sp.remove(tr[0]); tr[1] = False
            elif not op and not tr[1]: sp.add(tr[0]); tr[1] = True
        for _ in range(8): sp.step(1 / (FPS * 8))
        for n, b in balls.items():
            v = b.velocity
            if v.length > 1500: KLOG.append(('cap', round(t,2), n, round(v.length)))   # review2: no velocity clamp, logged only (search rejects)
            for (sx_, sy_, sr) in SLIMES:
                if math.hypot(b.position.x - sx_, b.position.y - sy_) < sr + MR + 6 and t - lastbo.get((n, sx_), -9) > 0.3:
                    lastbo[(n, sx_)] = t; bounces.append((t, (sx_, sy_)))
        for n, b in balls.items():
            if n in fin: continue
            onshelf = any(abs(b.position.y - (yy - MR - 10)) < 40 for (yy, x0, x1, ph) in SHELVES)
            if b.velocity.length < 20 and t > T_GO and not onshelf:
                still[n] += 1
                if still[n] > 30: KLOG.append(('kick', round(t,2), n, round(b.position.x), round(b.position.y))); still[n] = 0   # review2: no scripted kick, logged only (search rejects)
            else: still[n] = 0
            if b.position.y > FIN_Y:
                fin[n] = t
        for n, b in balls.items():
            if b.position.y > JT + 95 and b.space is not None: sp.remove(b, *b.shapes)   # fully behind the jar: it's in
        if t > T_GO:
            live = [n for n in NAMES]
            ld = min(live, key=lambda n: fin[n] if n in fin else 1e6 - balls[n].position.y)
            if not leaders or leaders[-1] != ld: leaders.append(ld)
        if record:
            frames.append(({n: (b.position.x, b.position.y, b.angle) for n, b in balls.items()}, [w.angle for w in wheels], [tr[1] for tr in traps], dict(fin)))
        if DBGQ is not None:   # independent check: pymunk's own distance from each marble centre to every wheel shape
            wsh = [sh for w in wheels for sh in w.shapes]
            DBGQ.append(({n: min(sh.point_query(b.position).distance for sh in wsh) - MR for n, b in balls.items()},
                         [[(sh.body.local_to_world(sh.a), sh.body.local_to_world(sh.b)) for sh in w.shapes if isinstance(sh, pymunk.Segment)] for w in wheels]))
        if len(fin) == len(NAMES) and t > max(fin.values()) + 3.5: break
    return frames, fin, leaders, bounces
def score(seed):
    del KLOG[:]
    global DBGQ
    DBGQ = []
    fr, fin, ld, bo = sim(seed, record=True)
    if any(k_[0] == 'kick' for k_ in KLOG): return None
    # review4: nothing stays still (<15px over 0.4s) except on the gate or at the bottle; nothing rides a waterwheel >0.3s
    for n in NAMES:
        ride = 0
        for f in range(len(fr)):
            if n in fr[f][3] or fr[f][0][n][1] > FIN_Y - 5: break
            if (f + 1) / FPS > T_GO + 0.15 and f + 12 < len(fr):
                p = fr[f][0][n]
                if all(math.hypot(fr[g][0][n][0] - p[0], fr[g][0][n][1] - p[1]) < 15 for g in range(f, f + 12)): return None
            ride = ride + 1 if DBGQ[f][0][n] < 1.5 else 0
            if ride > 18: return None   # carried by a paddle up to 0.6s is fine (it gets thrown off)
    if len(fin) < 4: return None
    order = sorted(NAMES, key=lambda n: fin[n]); w = order[0]
    pass   # review4: any winner (the podium follows the race)
    tw = fin[w]
    if not (9 < tw < 17): return None
    if fin[order[1]] - tw > 0.4 or fin[order[1]] - tw < 0.12 or len(ld) < 4: return None
    if fin[order[2]] - tw > 3.0: return None
    return round(tw, 2), w, order, len(ld), round(fin[order[1]] - tw, 2)
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, FIN, LEAD, BOUNCES = sim(SEED)
ORDER = sorted(NAMES, key=lambda n: FIN.get(n, 99)); WIN = ORDER[0]; T_WIN = FIN[WIN]
print('KLOG', KLOG); print('order', ORDER, {n: round(v, 2) for n, v in FIN.items()}, 'leaders', len(LEAD))
if os.environ.get('PROBE'): sys.exit()
# ---------------- art
bg = Image.open('templebg2/00.png').convert('RGBA'); k = W / bg.width
bgt = bg.resize((W, int(bg.height * k)), Image.NEAREST)
bgt = ImageEnhance.Brightness(bgt).enhance(0.42)
WORLD = Image.new('RGBA', (W, WH + 500), (0, 0, 0, 255))   # review3: room to frame the finish higher
OUTSIDE = None
y = 0; flip = False
while y < WORLD.height:
    WORLD.alpha_composite(bgt.transpose(Image.FLIP_TOP_BOTTOM) if flip else bgt, (0, y)); y += bgt.height; flip = not flip
wd = ImageDraw.Draw(WORLD)
def stone_seg(a, b, r):
    (x0, y0), (x1, y1) = a, b
    wd.line([x0, y0, x1, y1], fill=(60, 52, 60, 255), width=int(2 * r + 10))
    wd.line([x0, y0, x1, y1], fill=(138, 124, 118, 255), width=int(2 * r + 2))
    wd.line([x0, y0 - r + 2, x1, y1 - r + 2], fill=(196, 182, 160, 255), width=4)
    L = math.hypot(x1 - x0, y1 - y0)
    for s in range(0, int(L), 34):
        px, py = x0 + (x1 - x0) * s / L, y0 + (y1 - y0) * s / L
        wd.rectangle([px - 2, py - 2, px + 2, py + r - 2], fill=(98, 86, 84, 255))
for (a, b, r, kind) in SEGS:
    if a[0] == b[0] and kind == 'wall': continue   # chute walls are vertical but drawn
    stone_seg(a, b, r)
for x in (XL - 4, XR + 4):
    wd.rectangle([x - 20, 0, x + 20, WORLD.height], fill=(58, 50, 58, 255)); wd.rectangle([x - 14, 0, x + 14, WORLD.height], fill=(110, 98, 96, 255))
    for yy in range(0, WORLD.height, 48): wd.line([x - 14, yy, x + 14, yy], fill=(80, 70, 70, 255), width=3)
pass   # Oct 29 full-bleed: no extra dim strips outside the walls; the temple runs to both frame edges
for i_, (x, y_, r) in enumerate(PEGS):
    pts = peg_pts(i_, x, y_, r)
    wd.polygon(pts, fill=(70, 220, 230, 255), outline=(20, 70, 90, 255)); wd.polygon([(x, y_ - r - 4), (x + 6, y_ - 2), (x, y_ + 4), (x - 6, y_ - 2)], fill=(210, 255, 255, 255))
for (sy, txt) in []:   # Oct 29: stage signs cut (the pegs/slimes/wheels show each stage)
    f = F(44); w_ = wd.textlength(txt, font=f)
    wd.rounded_rectangle([CX - w_ / 2 - 24, sy - 52, CX + w_ / 2 + 24, sy + 14], 10, fill=(70, 46, 26, 255), outline=(240, 200, 120, 255), width=5)
    wd.text((CX - w_ / 2, sy - 41), txt, font=f, fill=(255, 230, 160, 255), stroke_width=3, stroke_fill=(40, 24, 10, 255))
JAR = crop(Image.open(A + 'jar_mushroom.png').convert('RGBA')); JAR = JAR.crop((0, 50, JAR.width, JAR.height))   # review3: bottle opened (cork rows cut) so marbles visibly drop into the mouth
JAR = JAR.resize((400, int(JAR.height * 400 / JAR.width)), Image.NEAREST)   # review2: neck now wider than a marble
SLIME = seq(PL + 'race/slime_idle_c', 2)
SPLAT = seq(PL + 'race/slime_splat_c', 2)
SPLAT = [Image.blend(Image.new('RGBA', s_.size, (0, 0, 0, 0)), s_, 0.65) for s_ in SPLAT]   # review2: smaller, see-through splats
FRONT = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + FRONT[name]).convert('RGBA')
    bb = im.getbbox(); c_ = (bb[0] + bb[2]) // 2
    head = im.crop((c_ - 15, 12, c_ + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    d.ellipse([12, 9, 22, 16], fill=(255, 255, 255, 170))
    return b
BALL = {n: face(n, MR) for n in NAMES}; ICON = {n: face(n, 50) for n in NAMES}   # review3: drawn radius = physics radius (was +6: looked like overlaps)
VICF = vic(WIN, 380)
def podium():
    im = Image.new('RGBA', (80, 28), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rectangle([0, 0, 79, 27], fill=(20, 16, 30, 255)); dd.rectangle([2, 2, 77, 25], fill=(120, 110, 140, 255)); dd.rectangle([2, 2, 77, 5], fill=(190, 182, 210, 255))
    dd.rectangle([2, 22, 77, 25], fill=(80, 72, 98, 255)); dd.rectangle([36, 8, 43, 19], fill=(255, 214, 60, 255)); dd.rectangle([34, 8, 36, 10], fill=(255, 214, 60, 255)); dd.rectangle([34, 18, 45, 19], fill=(255, 214, 60, 255))
    return up(im, 4)
PODIUM = podium()
# ---- output time -> sim time (slow-mo photo finish) ----
T2 = sorted(FIN.values())[1]; T3 = sorted(FIN.values())[2]; PHOTO = T2 - T_WIN < 0.2   # review3: only a real photo finish gets the slow-mo and stamp
SM0, SM1, SPD = T_WIN - 0.2, T2 + 0.08, 0.5
TMAP = []; st = 0.0
while True:
    TMAP.append(st)
    if st >= T3 + 0.3: break
    st += (SPD if PHOTO and SM0 <= st < SM1 else 1.0) / FPS
T_CARD = len(TMAP) / FPS            # output time the podium scene lands
NHOLD = int(round(2.0 * FPS))   # review2: podium hold 2.6 -> 1.8s
NF = len(TMAP) + NHOLD
def out_t(simt):  # output time of a sim time
    for i, v in enumerate(TMAP):
        if v >= simt: return i / FPS
    return len(TMAP) / FPS
SM0o, SM1o = out_t(SM0), out_t(SM1); TWo = out_t(T_WIN)
print('photo', PHOTO, 'slowmo out', round(SM0o, 2), round(SM1o, 2), 'card', round(T_CARD, 2), 'total', round(NF / FPS, 2))
EV = []
def ev(t, name): EV.append((round(t, 3), name))
ev(T_GO, 'go_8bit')
lastb = -1
for (t, p) in BOUNCES:
    if t - lastb > 0.15 and t < T_WIN: ev(out_t(t), 'boing'); lastb = t
for n, tf in FIN.items():
    if tf <= T3 + 0.05: ev(out_t(tf), 'ding_8bit')
if PHOTO: ev(TWo, 'whoosh_8bit')
POP = [0.0, 0.22, 0.44]   # podium: 3rd, 2nd, 1st pop onto their blocks
ev(T_CARD + POP[2], 'victory'); ev(T_CARD + POP[2] + 0.2, 'cheer'); ev(T_CARD + POP[0], 'twinkle')
# ---- podium scene (Oct 29 n10): full-bleed temple, 2nd | 1st (tallest) | 3rd, Syeda victory poses
PBG = bg.resize((W, int(bg.height * W / bg.width)), Image.NEAREST)
PBG = ImageEnhance.Brightness(PBG).enhance(0.55)
SCENE = Image.new('RGBA', (W, H), (0, 0, 0, 255))
yy_ = 0
while yy_ < H: SCENE.alpha_composite(PBG, (0, yy_)); yy_ += PBG.height
sd = ImageDraw.Draw(SCENE)
FLOOR = 1420
sd.rectangle([0, FLOOR, W, H], fill=(34, 28, 34, 255))
for gx in range(-40, W + 80, 96):
    for r_, gy in enumerate(range(FLOOR, H, 48)):
        ox = 48 if r_ % 2 else 0
        sd.rectangle([gx + ox, gy, gx + ox + 92, gy + 44], fill=(66, 56, 58, 255)); sd.rectangle([gx + ox, gy, gx + ox + 92, gy + 5], fill=(94, 82, 80, 255))
sd.rectangle([0, FLOOR - 6, W, FLOOR + 2], fill=(30, 24, 34, 255))
_g = Image.new('L', (1, H - FLOOR)); [_g.putpixel((0, i), int(40 + 170 * i / (H - FLOOR))) for i in range(H - FLOOR)]
_sh = Image.new('RGBA', (W, H - FLOOR), (8, 6, 14, 255)); _sh.putalpha(_g.resize((W, H - FLOOR))); SCENE.alpha_composite(_sh, (0, FLOOR))   # floor recedes into shadow
PCOL = {1: (255, 214, 60), 2: (220, 226, 240), 3: (226, 150, 84)}
PSLOT = {1: (478, 1050), 2: (230, 1170), 3: (726, 1240)}     # centre x, block top y
PW = 232
def block(rank, x, top):
    bw, bh = PW // 4, (FLOOR - top) // 4
    im = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rectangle([0, 0, bw - 1, bh - 1], fill=(24, 18, 32, 255)); dd.rectangle([2, 2, bw - 3, bh - 1], fill=(120, 110, 140, 255))
    dd.rectangle([2, 2, bw - 3, 5], fill=(196, 188, 214, 255)); dd.rectangle([bw - 8, 6, bw - 3, bh - 1], fill=(92, 84, 112, 255))
    for yy in range(14, bh, 12): dd.line([4, yy, bw - 9, yy], fill=(104, 96, 124, 255))
    im = up(im, 4); d2 = ImageDraw.Draw(im); f2 = F(96 if rank == 1 else 80); t2 = str(rank); w2 = d2.textlength(t2, font=f2)
    d2.text((im.width / 2 - w2 / 2 - 8, 44), t2, font=f2, fill=PCOL[rank] + (255,), stroke_width=8, stroke_fill=(24, 16, 30, 255))
    SCENE.alpha_composite(im, (x - im.width // 2, top))
for rk in (1, 2, 3): block(rk, *PSLOT[rk])
PVIC = {rk: vic(ORDER[rk - 1], 300) for rk in (1, 2, 3)}
def podium_scene(u, f):
    img = SCENE.copy()
    for k_, rk in enumerate((3, 2, 1)):
        uu = u - POP[k_]
        if uu < 0: continue
        x, top = PSLOT[rk]; fr = PVIC[rk][int(uu * 8) % len(PVIC[rk])]
        DROP = float(top); tf = math.sqrt(2 * DROP / 5000.0)   # review4: each guide falls from above the top of the frame and lands
        dy_ = -DROP + 0.5 * 5000.0 * min(uu, tf) ** 2
        if uu < tf:
            img.alpha_composite(fr, (x - fr.width // 2, int(top - fr.height + dy_))); continue
        uu = uu - tf
        if uu < 0.18:   # sparkle burst where they appear
            layer(img, lambda dd, x=x, top=top, uu=uu: [dd.rectangle([x + math.cos(a) * (40 + 500 * uu) - 6, top - 150 + math.sin(a) * (40 + 500 * uu) - 6, x + math.cos(a) * (40 + 500 * uu) + 6, top - 150 + math.sin(a) * (40 + 500 * uu) + 6], fill=PCOL[rk] + (int(255 * (1 - uu / 0.18)),)) for a in [j * math.pi / 4 for j in range(8)]])
        img.alpha_composite(fr, (x - fr.width // 2, top - fr.height))
    if u >= POP[2]:
        uu = u - POP[2]; rr = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        for _ in range(46):
            x_, y_ = rr.uniform(70, 1010), (rr.uniform(0, 1300) + uu * 380) % (FLOOR - HB) + HB
            dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
        img.alpha_composite(L)
    if u < 0.1: img.alpha_composite(Image.new('RGBA', img.size, (255, 255, 255, int(200 * (1 - u / 0.1)))))
    return img
cam = 0.0
RANK_SHOWN = None; RANK_PEND = (None, 0)
def SIMF(simt): return min(int(round(simt * FPS)), len(FR) - 1)
def frame(f):
    global cam
    t = TMAP[f] if f < len(TMAP) else TMAP[-1]; pf = SIMF(t); pos, wang, traps, fin = FR[pf]
    tout = f / FPS
    live = [n for n in NAMES if n not in fin]
    if t < T_WIN:   # review2: camera locks once the first marble finishes (no bob)
        focus = max(pos[n][1] for n in live) if live else FIN_Y
        tgt = max(0, min(WORLD.height - H, focus - 1290, FIN_Y - 1150))   # review3: finish framed at y~1150
        cam = tgt if f == 0 else cam + (tgt - cam) * 0.1
    c0 = int(cam)
    img = WORLD.crop((0, c0, W, c0 + H)).copy(); d = ImageDraw.Draw(img)
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for (wx, wy, R, w_), ang in zip(WHEELS, wang):
        sy = wy - c0
        if -260 < sy < H + 260:
            for s_ in range(0, 40):
                yy = sy - 300 + ((s_ * 37 + t * 420) % 360); xx = wx - 30 + (s_ * 13 % 60)
                dl.rectangle([xx, yy, xx + 6, yy + 18], fill=(150, 210, 255, 150))
    img.alpha_composite(L); d = ImageDraw.Draw(img)
    for (wx, wy, R, w_), ang in zip(WHEELS, wang):
        sy = wy - c0
        if -260 < sy < H + 260:
            for kk in range(6):
                a = ang + kk * math.pi / 3; ex, ey = wx + R * math.cos(a), sy + R * math.sin(a)
                d.line([wx, sy, ex, ey], fill=(70, 45, 22, 255), width=22); d.line([wx, sy, ex, ey], fill=(150, 104, 56, 255), width=14)
            d.ellipse([wx - 28, sy - 28, wx + 28, sy + 28], fill=(200, 160, 70, 255), outline=(70, 45, 22, 255), width=5)
    for i, (x, yy, r) in enumerate(SLIMES):
        sy = yy - c0
        if -120 < sy < H + 120:
            hit = any(0 <= t - bt < 0.2 and math.hypot(p[0] - x, p[1] - yy) < 100 for (bt, p) in BOUNCES if bt <= t)
            fr = SPLAT[min(len(SPLAT) - 1, 3)] if hit else SLIME[(int(t * 10) + i * 2) % len(SLIME)]
            img.alpha_composite(fr, (int(x - fr.width / 2), int(sy - fr.height / 2 - 24)))
    jy = JT - c0
    if -800 < jy < H + 100:
        layer(img, lambda dd: dd.ellipse([CX - 280, jy - 40, CX + 280, jy + 420], fill=(255, 210, 120, 50)))
        layer(img, lambda dd: dd.ellipse([CX - 70, jy + 4, CX + 70, jy + 40], fill=(16, 8, 6, 255)))   # dark mouth of the open bottle
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for n in NAMES:
        if pos[n][1] > JT + 95: continue
        for k_ in range(1, 9):
            p = FR[max(0, pf - k_ * 2)][0][n]; sy_ = p[1] - c0; rr_ = 20 - k_
            dl.rectangle([p[0] - rr_, sy_ - rr_, p[0] + rr_, sy_ + rr_], fill=RING[n] + (200 - k_ * 22,))
        x, yy, ang = pos[n]; sy = yy - c0
    img.alpha_composite(L)
    for n in NAMES:
        x, yy, ang = pos[n]; sy = yy - c0
        if yy > JT + 95: continue
        if -60 < sy < H + 60:
            b = BALL[n].rotate(-math.degrees(ang), resample=Image.NEAREST)
            img.alpha_composite(b, (int(x - b.width / 2), int(sy - b.height / 2)))
    if -800 < jy < H + 100: img.alpha_composite(JAR, (int(CX - JAR.width / 2), int(jy)))   # drawn over the marbles: they drop into it
    gy_ = 230 + DY - c0
    if tout < T_GO + 0.2:
        uu = max(0.0, tout - T_GO) / 0.2; ang_ = (math.pi / 2) * uu * uu
        for side, hx in ((1, XL + 16), (-1, XR - 16)):
            L_ = (XR - XL - 32) / 2; ex_, ey_ = hx + side * L_ * math.cos(ang_), gy_ + L_ * math.sin(ang_)
            layer(img, lambda dd, hx=hx, ex_=ex_, ey_=ey_: (dd.line([hx, gy_, ex_, ey_], fill=(60, 40, 24, 255), width=20), dd.line([hx, gy_, ex_, ey_], fill=(150, 104, 56, 255), width=12)))
    # standings panel (1.4x): leader slot glows
    raw = sorted(NAMES, key=lambda n: (fin[n] if n in fin else 1e6 - pos[n][1]))
    global RANK_SHOWN, RANK_PEND
    if f == 0 or RANK_SHOWN is None: RANK_SHOWN, RANK_PEND = raw, (raw, 0)
    if raw != RANK_SHOWN:   # review4: a new order must hold 4 frames before the bar changes (no one-frame flicker)
        RANK_PEND = (raw, RANK_PEND[1] + 1) if RANK_PEND[0] == raw else (raw, 1)
        if RANK_PEND[1] >= 4 or any(n in fin for n in raw[:1]): RANK_SHOWN = raw
    rank = RANK_SHOWN
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(14, 10, 24, 225)))
    glow = 0.75 + 0.25 * math.sin(tout * 8)
    for i, n in enumerate(NAMES):
        x = 70 + 955 * (i + 0.5) / 4; rk = rank.index(n)
        if rk == 0 and tout >= 1.0: layer(img, lambda dd, x=x: dd.rounded_rectangle([x - 112, P0 + 8, x + 112, P1 - 8], 14, fill=(255, 214, 60, int(70 * glow)), outline=(255, 214, 60, int(255 * glow)), width=6))
        ic = ICON[n]; img.alpha_composite(ic, (int(x - ic.width / 2), P0 + 14))
        text_layer(img, [(x, P0 + 128, ['1ST', '2ND', '3RD', '4TH'][rk] if tout >= 1.0 else '?', 44, (255, 214, 60) if (rk == 0 and tout >= 1.0) else (225, 225, 225), 7, 255)])   # review2: no ranks before ~1s
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(255, 214, 60, 255), width=4)
    if T_GO <= tout < T_GO + 0.5:
        u = tout - T_GO; sz = 150 if u > 0.1 else int(90 + 600 * u)
        text_layer(img, [(CX, 1250, 'GO!', sz, (120, 255, 120), 12, int(255 * min(1, (0.5 - u) / 0.15)))])   # review3: below the marbles, gone by 0.5s
    if PHOTO and TWo <= tout < min(T_CARD, TWo + 0.8):
        u = tout - TWo; pop = 1.0 if u > 0.1 else 0.7 + 3 * u
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], outline=(255, 255, 255, 120), width=0))
        Ls = Image.new('RGBA', img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(Ls); fnt = F(int(56 * pop)); tw = ds.textlength('PHOTO FINISH!', font=fnt)
        ds.text((CX - tw / 2, 720), 'PHOTO FINISH!', font=fnt, fill=(255, 255, 255, 255), stroke_width=8, stroke_fill=(10, 6, 18, 255))
        img.alpha_composite(Ls)
    if not PHOTO and TWo <= tout < min(T_CARD, TWo + 0.8):
        u = tout - TWo; pop = 1.0 if u > 0.1 else 0.7 + 3 * u
        text_layer(img, [(CX, 760, '1ST!', int(96 * pop), (255, 214, 60), 10, int(255 * min(1, (0.8 - u) / 0.15)))])
    if tout >= T_CARD:
        img = podium_scene(tout - T_CARD, f)
    img.alpha_composite(HOOK)
    return img
if os.environ.get('FRAMES'):
    for f in [int(x) for x in os.environ['FRAMES'].split(',')]: frame(f).convert('RGB').save(OUT + f'k_{f}.png')
    sys.exit()
wr = Writer(OUT + 'v58_noaudio.mp4'); PV = len(sys.argv) > 2
for f in range(NF):
    img = frame(f); wr.write(img)
    if PV and f % 15 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'pv_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'v58_ev.json', 'w'))
print('done', round(NF / FPS, 2), len(EV))
