import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import pymunk
os.chdir(SP + 'fork_a6'); OUT = SP + 'fork_hfg6/v58/'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['PICK YOUR MARBLE'], accent=0, fade_to=600)   # Oct 29: soft fade, no box, comment line cut
P0, P1 = HB + 10, HB + 196; print('HB', HB)
XL, XR = 90, 860; DY = 520
def X(x): return XL + (x - 44) * (XR - XL) / 992
CX = (XL + XR) / 2
NAMES = ['joy', 'cyrus', 'ray', 'cleo']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
CUT = 1240  # Trapdoors stage removed: everything below it moves up
MR = 39; WH = 6000 - CUT + DY; T_GO = 0.0
SEGS = []        # static course segments (a, b, radius, kind)
PEGS = []        # crystal pegs (x, y, r)
SLIMES = []      # slime bumpers (x, y, r)
WHEELS = [(X(360), 2980 + DY, 130, 1.7), (X(720), 3380 + DY, 130, -1.9)]
SHELVES = []     # (y, trap_x0, trap_x1, phase)
SIGNS = [(y + DY, s) for y, s in [(560, 'CRYSTAL CAVERN'), (1610, 'SLIME BOUNCERS'), (2740, 'WATERWHEELS'), (4880 - CUT, 'FINAL STRETCH')]]
def seg(a, b, r=10, kind='stone'): SEGS.append(((X(a[0]), a[1] + DY), (X(b[0]), b[1] + DY), r, kind))
seg((44, -DY), (44, WH + 300), 26); seg((1036, -DY), (1036, WH + 300), 26); seg((44, 5980 - CUT), (1036, 5980 - CUT), 20)
seg((60, 300), (420, 470)); seg((1020, 300), (660, 470))
for j, y in enumerate(range(620, 1500, 105)):
    off = 65 if j % 2 else 0
    for x in range(190 + off * 85 // 65, 920, 170): PEGS.append((X(x), y + DY, 13))
for j, y in enumerate(range(1720, 2620, 175)):
    row = [298, 475, 652] if j % 2 == 0 else [XL + 26 + 36, 386, 564, XR - 26 - 36]
    for x in row: SLIMES.append((x, y + DY, 36))
print('slimes', SLIMES)
seg((1020, 2700), (720, 2780)); seg((60, 2700), (330, 2770))
C = CUT
seg((60, 4950 - C), (420, 5150 - C)); seg((1020, 5250 - C), (660, 5450 - C)); seg((60, 5520 - C), (440, 5700 - C)); seg((1020, 5520 - C), (640, 5700 - C))
FIN_Y = 5740 - C + DY
def trap_open(k, t):
    y, x0, x1, ph = SHELVES[k]
    return ((t - T_GO + ph) % 1.6) < 0.8
def sim(seed, dur=45, record=True):
    rnd = random.Random(seed)
    sp = pymunk.Space(); sp.gravity = (0, 1650)
    for (a, b, r, kind) in SEGS:
        s = pymunk.Segment(sp.static_body, a, b, r); s.friction = 0.5; s.elasticity = 0.45; sp.add(s)
    for (x, y, r) in PEGS:
        c = pymunk.Circle(sp.static_body, r, (x, y)); c.elasticity = 0.7; c.friction = 0.3; sp.add(c)
    for (x, y, r) in SLIMES:
        c = pymunk.Circle(sp.static_body, r, (x, y)); c.elasticity = 1.35; c.friction = 0.2; c.collision_type = 3; sp.add(c)
    wheels = []
    for (x, y, R, w) in WHEELS:
        b = pymunk.Body(body_type=pymunk.Body.KINEMATIC); b.position = (x, y); b.angular_velocity = w; sp.add(b)
        for k in range(6):
            a = k * math.pi / 3; s = pymunk.Segment(b, (0, 0), (R * math.cos(a), R * math.sin(a)), 9); s.friction = 0.6; s.elasticity = 0.3; sp.add(s)
        hub = pymunk.Circle(b, 26); sp.add(hub); wheels.append(b)
    traps = []
    for (y, x0, x1, ph) in SHELVES:
        s = pymunk.Segment(sp.static_body, (x0, y + 24), (x1, y + 24), 10); s.friction = 0.5; s.elasticity = 0.3; sp.add(s); traps.append([s, True])
    gate = pymunk.Segment(sp.static_body, (X(60), 230 + DY), (X(1020), 230 + DY), 8); sp.add(gate)
    balls = {}
    xs = [X(300), X(460), X(620), X(780)]; rnd.shuffle(xs)
    for n, x in zip(NAMES, xs):
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, MR)); b.position = (x + rnd.uniform(-15, 15), 170 + DY)
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
            if v.length > 1500: b.velocity = v * (1500 / v.length)
            for (sx_, sy_, sr) in SLIMES:
                if math.hypot(b.position.x - sx_, b.position.y - sy_) < sr + MR + 6 and t - lastbo.get((n, sx_), -9) > 0.3:
                    lastbo[(n, sx_)] = t; bounces.append((t, (sx_, sy_)))
        for n, b in balls.items():
            if n in fin: continue
            onshelf = any(abs(b.position.y - (yy - MR - 10)) < 40 for (yy, x0, x1, ph) in SHELVES)
            if b.velocity.length < 20 and t > T_GO and not onshelf:
                still[n] += 1
                if still[n] > 30: b.apply_impulse_at_local_point((rnd.choice([-1, 1]) * rnd.uniform(180, 300), -260)); still[n] = 0
            else: still[n] = 0
            if b.position.y > FIN_Y:
                fin[n] = t
        if t > T_GO:
            live = [n for n in NAMES]
            ld = min(live, key=lambda n: fin[n] if n in fin else 1e6 - balls[n].position.y)
            if not leaders or leaders[-1] != ld: leaders.append(ld)
        if record:
            frames.append(({n: (b.position.x, b.position.y, b.angle) for n, b in balls.items()}, [w.angle for w in wheels], [tr[1] for tr in traps], dict(fin)))
        if len(fin) == len(NAMES) and t > max(fin.values()) + 3.5: break
    return frames, fin, leaders, bounces
def score(seed):
    fr, fin, ld, bo = sim(seed, record=False)
    if len(fin) < 4: return None
    order = sorted(NAMES, key=lambda n: fin[n]); w = order[0]
    if w != 'ray': return None
    tw = fin[w]
    if not (10 < tw < 17): return None
    if fin[order[1]] - tw > 0.4 or len(ld) < 6: return None
    return round(tw, 2), w, order, len(ld), round(fin[order[1]] - tw, 2)
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, FIN, LEAD, BOUNCES = sim(SEED)
ORDER = sorted(NAMES, key=lambda n: FIN.get(n, 99)); WIN = ORDER[0]; T_WIN = FIN[WIN]
print('order', ORDER, {n: round(v, 2) for n, v in FIN.items()}, 'leaders', len(LEAD))
# ---------------- art
bg = Image.open('templebg2/00.png').convert('RGBA'); k = W / bg.width
bgt = bg.resize((W, int(bg.height * k)), Image.NEAREST)
bgt = ImageEnhance.Brightness(bgt).enhance(0.42)
WORLD = Image.new('RGBA', (W, WH + 400), (0, 0, 0, 255))
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
    if a[0] == b[0]: continue
    stone_seg(a, b, r)
for x in (XL - 4, XR + 4):
    wd.rectangle([x - 20, 0, x + 20, WORLD.height], fill=(58, 50, 58, 255)); wd.rectangle([x - 14, 0, x + 14, WORLD.height], fill=(110, 98, 96, 255))
    for yy in range(0, WORLD.height, 48): wd.line([x - 14, yy, x + 14, yy], fill=(80, 70, 70, 255), width=3)
pass   # Oct 29 full-bleed: no extra dim strips outside the walls; the temple runs to both frame edges
for (x, y_, r) in PEGS:
    pts = [(x, y_ - r - 8), (x + r, y_), (x, y_ + r + 8), (x - r, y_)]
    wd.polygon(pts, fill=(70, 220, 230, 255), outline=(20, 70, 90, 255)); wd.polygon([(x, y_ - r - 4), (x + 6, y_ - 2), (x, y_ + 4), (x - 6, y_ - 2)], fill=(210, 255, 255, 255))
for (sy, txt) in []:   # Oct 29: stage signs cut (the pegs/slimes/wheels show each stage)
    f = F(44); w_ = wd.textlength(txt, font=f)
    wd.rounded_rectangle([CX - w_ / 2 - 24, sy - 52, CX + w_ / 2 + 24, sy + 14], 10, fill=(70, 46, 26, 255), outline=(240, 200, 120, 255), width=5)
    wd.text((CX - w_ / 2, sy - 41), txt, font=f, fill=(255, 230, 160, 255), stroke_width=3, stroke_fill=(40, 24, 10, 255))
JAR = up(crop(Image.open(A + 'jar_mushroom.png').convert('RGBA')), 1)
JAR = JAR.resize((300, int(JAR.height * 300 / JAR.width)), Image.NEAREST) if JAR.width > 0 else JAR
SLIME = seq(PL + 'race/slime_idle_c', 3)
SPLAT = seq(PL + 'race/slime_splat_c', 3)
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
BALL = {n: face(n, MR + 6) for n in NAMES}; ICON = {n: face(n, 50) for n in NAMES}
VICF = vic(WIN, 380)
def podium():
    im = Image.new('RGBA', (80, 28), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rectangle([0, 0, 79, 27], fill=(20, 16, 30, 255)); dd.rectangle([2, 2, 77, 25], fill=(120, 110, 140, 255)); dd.rectangle([2, 2, 77, 5], fill=(190, 182, 210, 255))
    dd.rectangle([2, 22, 77, 25], fill=(80, 72, 98, 255)); dd.rectangle([36, 8, 43, 19], fill=(255, 214, 60, 255)); dd.rectangle([34, 8, 36, 10], fill=(255, 214, 60, 255)); dd.rectangle([34, 18, 45, 19], fill=(255, 214, 60, 255))
    return up(im, 4)
PODIUM = podium()
# ---- output time -> sim time (slow-mo photo finish) ----
T2 = sorted(FIN.values())[1]; PHOTO = T2 - T_WIN < 0.5
SM0, SM1, SPD = T_WIN - 0.2, T2 + 0.08, 0.5
TMAP = []; st = 0.0
while True:
    TMAP.append(st)
    if st >= T_WIN + 0.5: break
    st += (SPD if PHOTO and SM0 <= st < SM1 else 1.0) / FPS
T_CARD = len(TMAP) / FPS            # output time the win card lands
NHOLD = int(round(1.5 * FPS))
NF = len(TMAP) + NHOLD
def out_t(simt):  # output time of a sim time
    for i, v in enumerate(TMAP):
        if v >= simt: return i / FPS
    return len(TMAP) / FPS
SM0o, SM1o = out_t(SM0), out_t(SM1)
print('photo', PHOTO, 'slowmo out', round(SM0o, 2), round(SM1o, 2), 'card', round(T_CARD, 2), 'total', round(NF / FPS, 2))
EV = []
def ev(t, name): EV.append((round(t, 3), name))
ev(0.2, 'go_8bit')
lastb = -1
for (t, p) in BOUNCES:
    if t - lastb > 0.15 and t < T_WIN: ev(out_t(t), 'boing'); lastb = t
for n, tf in FIN.items():
    if tf <= T_WIN + 0.5: ev(out_t(tf), 'ding_8bit')
if PHOTO: ev(SM0o, 'whoosh_8bit')
ev(T_CARD, 'victory'); ev(T_CARD + 0.2, 'cheer')
cam = 0.0
def SIMF(simt): return min(int(round(simt * FPS)), len(FR) - 1)
def frame(f):
    global cam
    t = TMAP[f] if f < len(TMAP) else TMAP[-1]; pf = SIMF(t); pos, wang, traps, fin = FR[pf]
    tout = f / FPS
    live = [n for n in NAMES if n not in fin]
    if t < T_WIN:
        focus = max(pos[n][1] for n in live) if live else FIN_Y
        tgt = max(0, min(WORLD.height - H, focus - 1290))
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
            d.ellipse([wx - R, sy - R, wx + R, sy + R], outline=(90, 60, 30, 255), width=10)
            for kk in range(6):
                a = ang + kk * math.pi / 3; ex, ey = wx + R * math.cos(a), sy + R * math.sin(a)
                d.line([wx, sy, ex, ey], fill=(70, 45, 22, 255), width=22); d.line([wx, sy, ex, ey], fill=(150, 104, 56, 255), width=14)
            d.ellipse([wx - 28, sy - 28, wx + 28, sy + 28], fill=(200, 160, 70, 255), outline=(70, 45, 22, 255), width=5)
    for i, (x, yy, r) in enumerate(SLIMES):
        sy = yy - c0
        if -120 < sy < H + 120:
            hit = any(0 <= t - bt < 0.25 and math.hypot(p[0] - x, p[1] - yy) < 90 for (bt, p) in BOUNCES if bt <= t)
            fr = SPLAT[min(len(SPLAT) - 1, 3)] if hit else SLIME[(int(t * 10) + i * 2) % len(SLIME)]
            img.alpha_composite(fr, (int(x - fr.width / 2), int(sy - fr.height + 70)))
    jy = FIN_Y - c0 - 40
    if -400 < jy < H + 100:
        layer(img, lambda dd: dd.ellipse([CX - 230, jy - 40, CX + 230, jy + 340], fill=(255, 210, 120, 50)))
        img.alpha_composite(JAR, (int(CX - JAR.width / 2), int(jy - 30)))
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for n in NAMES:
        if n in fin and t > fin[n] + 0.25: continue
        for k_ in range(1, 9):
            p = FR[max(0, pf - k_ * 2)][0][n]; sy_ = p[1] - c0; rr_ = 20 - k_
            dl.rectangle([p[0] - rr_, sy_ - rr_, p[0] + rr_, sy_ + rr_], fill=RING[n] + (200 - k_ * 22,))
        x, yy, ang = pos[n]; sy = yy - c0
        dl.ellipse([x - 68, sy - 68, x + 68, sy + 68], fill=RING[n] + (70,))
    img.alpha_composite(L)
    for n in NAMES:
        x, yy, ang = pos[n]; sy = yy - c0
        if n in fin and t > fin[n] + 0.25: continue
        if -60 < sy < H + 60:
            b = BALL[n].rotate(-math.degrees(ang), resample=Image.NEAREST)
            img.alpha_composite(b, (int(x - b.width / 2), int(sy - b.height / 2)))
    # standings panel (1.4x): leader slot glows
    rank = sorted(NAMES, key=lambda n: (fin[n] if n in fin else 1e6 - pos[n][1]))
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(14, 10, 24, 225)))
    glow = 0.75 + 0.25 * math.sin(tout * 8)
    for i, n in enumerate(NAMES):
        x = 70 + 955 * (i + 0.5) / 4; rk = rank.index(n)
        if rk == 0: layer(img, lambda dd, x=x: dd.rounded_rectangle([x - 112, P0 + 8, x + 112, P1 - 8], 14, fill=(255, 214, 60, int(70 * glow)), outline=(255, 214, 60, int(255 * glow)), width=6))
        ic = ICON[n]; img.alpha_composite(ic, (int(x - ic.width / 2), P0 + 14))
        text_layer(img, [(x, P0 + 128, ['1ST', '2ND', '3RD', '4TH'][rk], 44, (255, 214, 60) if rk == 0 else (225, 225, 225), 7, 255)])
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(255, 214, 60, 255), width=4)
    if 0.15 <= tout < 0.9:
        u = tout - 0.15; sz = 150 if u > 0.1 else int(90 + 600 * u)
        text_layer(img, [(CX, 1000, 'GO!', sz, (120, 255, 120), 12, int(255 * min(1, (0.75 - u) / 0.2)))])
    if PHOTO and SM0o <= tout < T_CARD:
        u = tout - SM0o; pop = 1.0 if u > 0.1 else 0.7 + 3 * u
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], outline=(255, 255, 255, 120), width=0))
        Ls = Image.new('RGBA', img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(Ls); fnt = F(int(56 * pop)); tw = ds.textlength('PHOTO FINISH!', font=fnt)
        ds.text((CX - tw / 2, 720), 'PHOTO FINISH!', font=fnt, fill=(255, 255, 255, 255), stroke_width=8, stroke_fill=(10, 6, 18, 255))
        img.alpha_composite(Ls)
        if u < 0.12: img.alpha_composite(Image.new('RGBA', img.size, (255, 255, 255, int(150 * (1 - u / 0.12)))))
    if tout >= T_CARD:
        u = tout - T_CARD; a = 1.0 if u > 0.12 else u / 0.12
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], fill=(10, 8, 18, int(185 * a))))
        img.alpha_composite(PODIUM, (478 - PODIUM.width // 2, 1032))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1046 - vf.height))
        pop = 1.0 if u > 0.12 else 0.75 + 0.25 * u / 0.12
        text_layer(img, [(478, 1170, LABEL[WIN] + ' WINS!', int(56 * pop), (255, 214, 60), 9, 255)])
        rr = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        for _ in range(40):
            x_, y_ = rr.uniform(80, 1000), (rr.uniform(0, H) + u * 400) % (1480 - P1) + P1
            dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
        img.alpha_composite(L)
    img.alpha_composite(HOOK)
    return img
wr = Writer(OUT + 'v58_noaudio.mp4'); PV = len(sys.argv) > 2
for f in range(NF):
    img = frame(f); wr.write(img)
    if PV and f % 15 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'pv_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'v58_ev.json', 'w'))
print('done', round(NF / FPS, 2), len(EV))
