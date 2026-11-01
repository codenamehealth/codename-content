import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import pymunk
os.chdir(SP + 'fork_a6'); OUT = SP + 'fork_sz56/v58/'
HOOK, HB = hook_layer(['PICK YOUR', 'MARBLE'], accent=1)
P0, P1 = HB + 12, HB + 150
XL, XR = 90, 860; DY = 520
def X(x): return XL + (x - 44) * (XR - XL) / 992
CX = (XL + XR) / 2
NAMES = ['joy', 'cyrus', 'ray', 'cleo']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
MR = 30; WH = 6000 + DY; T_GO = 2.4
SEGS = []        # static course segments (a, b, radius, kind)
PEGS = []        # crystal pegs (x, y, r)
SLIMES = []      # slime bumpers (x, y, r)
WHEELS = [(X(360), 2980 + DY, 150, 1.7), (X(720), 3380 + DY, 150, -1.9)]
SHELVES = []     # (y, trap_x0, trap_x1, phase)
SIGNS = [(y + DY, s) for y, s in [(560, 'CRYSTAL CAVERN'), (1610, 'SLIME BOUNCERS'), (2740, 'WATERWHEELS'), (3620, 'TRAPDOORS'), (4880, 'FINAL STRETCH')]]
def seg(a, b, r=10, kind='stone'): SEGS.append(((X(a[0]), a[1] + DY), (X(b[0]), b[1] + DY), r, kind))
seg((44, -DY), (44, WH + 300), 26); seg((1036, -DY), (1036, WH + 300), 26); seg((44, 5980), (1036, 5980), 20)
seg((60, 300), (420, 470)); seg((1020, 300), (660, 470))
for j, y in enumerate(range(620, 1500, 105)):
    off = 65 if j % 2 else 0
    for x in range(175 + off, 920, 130): PEGS.append((X(x), y + DY, 13))
for j, y in enumerate(range(1720, 2620, 175)):
    row = [298, 475, 652] if j % 2 == 0 else [XL + 26 + 36, 386, 564, XR - 26 - 36]
    for x in row: SLIMES.append((x, y + DY, 36))
print('slimes', SLIMES)
seg((1020, 2700), (720, 2780)); seg((60, 2700), (330, 2770))
for k, (y, tx, ph) in enumerate([(3800, 640, 0.0), (4200, 180, 0.9), (4600, 640, 1.6)]):
    tw = 230
    if tx > 500:
        seg((60, y - 60), (tx, y)); seg((tx + tw, y + 24), (1020, y - 50))
    else:
        seg((tx + tw, y), (1020, y - 60)); seg((60, y - 50), (tx, y + 24))
    SHELVES.append((y + DY, X(tx), X(tx + tw), ph))
seg((60, 4950), (420, 5150)); seg((1020, 5250), (660, 5450)); seg((60, 5520), (440, 5700)); seg((1020, 5520), (640, 5700))
FIN_Y = 5740 + DY
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
    if not (18 < tw < 30): return None
    if fin[order[1]] - tw > 1.0 or len(ld) < 6: return None
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
wd.rectangle([0, 0, XL - 24, WORLD.height], fill=(8, 6, 14, 150)); wd.rectangle([XR + 24, 0, W, WORLD.height], fill=(8, 6, 14, 150))
for (x, y_, r) in PEGS:
    pts = [(x, y_ - r - 8), (x + r, y_), (x, y_ + r + 8), (x - r, y_)]
    wd.polygon(pts, fill=(70, 220, 230, 255), outline=(20, 70, 90, 255)); wd.polygon([(x, y_ - r - 4), (x + 6, y_ - 2), (x, y_ + 4), (x - 6, y_ - 2)], fill=(210, 255, 255, 255))
for (sy, txt) in SIGNS:
    f = F(26); w_ = wd.textlength(txt, font=f)
    wd.rounded_rectangle([CX - w_ / 2 - 24, sy - 34, CX + w_ / 2 + 24, sy + 12], 8, fill=(70, 46, 26, 255), outline=(240, 200, 120, 255), width=4)
    wd.text((CX - w_ / 2, sy - 24), txt, font=f, fill=(255, 230, 160, 255))
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
BALL = {n: face(n, MR + 6) for n in NAMES}; ICON = {n: face(n, 36) for n in NAMES}
VICF = vic(WIN, 380)
EV = []
def ev(t, name): EV.append((round(t, 3), name))
for tt in (0.6, 1.2, 1.8): ev(tt, 'tick_8bit')
ev(T_GO, 'go_8bit')
lastb = -1
for (t, p) in BOUNCES:
    if t - lastb > 0.12 and t < T_WIN + 3: ev(t, 'boing'); lastb = t
for n, tf in FIN.items(): ev(tf, 'ding_8bit')
ev(T_WIN, 'victory')
T_END = T_WIN + 4.2; NF = int(T_END * FPS)
cam = 0.0
wr = Writer(OUT + 'v58_noaudio.mp4')
for f in range(NF):
    t = f / FPS; pos, wang, traps, fin = FR[min(f, len(FR) - 1)]
    live = [n for n in NAMES if n not in fin]
    focus = max(pos[n][1] for n in live) if live else FIN_Y
    tgt = max(0, min(WORLD.height - H, focus - 1290))
    cam = tgt if f == 0 else cam + (tgt - cam) * 0.1
    c0 = int(cam)
    img = WORLD.crop((0, c0, W, c0 + H)).copy(); d = ImageDraw.Draw(img)
    # trapdoors
    for k, (yy, x0, x1, ph) in enumerate(SHELVES):
        sy = yy - c0
        if -40 < sy < H + 40:
            if traps[k]:
                d.rectangle([x0, sy - 10, x1, sy + 10], fill=(120, 80, 40, 255), outline=(60, 36, 18, 255), width=3)
                for xx in range(int(x0) + 20, int(x1), 40): d.line([xx, sy - 10, xx, sy + 10], fill=(80, 52, 26, 255), width=3)
            else:
                d.rectangle([x0, sy - 10, x0 + 18, sy + 60], fill=(120, 80, 40, 255)); d.rectangle([x1 - 18, sy - 10, x1, sy + 60], fill=(120, 80, 40, 255))
            lamp = (120, 255, 120, 255) if not traps[k] else (255, 90, 80, 255)
            d.ellipse([x1 + 10, sy - 40, x1 + 30, sy - 20], fill=lamp, outline=(30, 20, 20, 255), width=3)
    # waterwheels + water
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for (wx, wy, R, w_), ang in zip(WHEELS, wang):
        sy = wy - c0
        if -260 < sy < H + 260:
            for s in range(0, 40):
                yy = sy - 300 + ((s * 37 + t * 420) % 360); xx = wx - 30 + (s * 13 % 60)
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
    # slime bumpers (squash when hit)
    for i, (x, yy, r) in enumerate(SLIMES):
        sy = yy - c0
        if -120 < sy < H + 120:
            hit = any(0 <= t - bt < 0.25 and math.hypot(p[0] - x, p[1] - yy) < 90 for (bt, p) in BOUNCES[-200:] if bt <= t)
            fr = SPLAT[min(len(SPLAT) - 1, 3)] if hit else SLIME[(int(t * 10) + i * 2) % len(SLIME)]
            img.alpha_composite(fr, (int(x - fr.width / 2), int(sy - fr.height + 70)))
    # finish jar
    jy = FIN_Y - c0 - 40
    if -400 < jy < H + 100:
        layer(img, lambda dd: dd.ellipse([CX - 230, jy - 40, CX + 230, jy + 340], fill=(255, 210, 120, 50)))
        img.alpha_composite(JAR, (int(CX - JAR.width / 2), int(jy - 30)))
        text_layer(img, [(CX, jy - 110, 'FINISH', 44, (255, 214, 60), 7, 255)])
    # marbles + trails
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for n in NAMES:
        if n in fin and t > fin[n] + 0.25: continue
        for k_ in range(1, 9):
            p = FR[max(0, min(f, len(FR) - 1) - k_ * 2)][0][n]; sy_ = p[1] - c0; rr_ = 16 - k_
            dl.rectangle([p[0] - rr_, sy_ - rr_, p[0] + rr_, sy_ + rr_], fill=RING[n] + (200 - k_ * 22,))
        x, yy, ang = pos[n]; sy = yy - c0
        dl.ellipse([x - 54, sy - 54, x + 54, sy + 54], fill=RING[n] + (70,))
    img.alpha_composite(L)
    for n in NAMES:
        x, yy, ang = pos[n]; sy = yy - c0
        if n in fin and t > fin[n] + 0.25: continue
        if -60 < sy < H + 60:
            b = BALL[n].rotate(-math.degrees(ang), resample=Image.NEAREST)
            img.alpha_composite(b, (int(x - b.width / 2), int(sy - b.height / 2)))
    # rank panel under the hook
    rank = sorted(NAMES, key=lambda n: (fin[n] if n in fin else 1e6 - pos[n][1]))
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(14, 10, 24, 215)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(255, 214, 60, 255), width=4)
    for i, n in enumerate(NAMES):
        x = 70 + 955 * (i + 0.5) / 4; ic = ICON[n]; img.alpha_composite(ic, (int(x - ic.width / 2), P0 + 10))
        rk = rank.index(n)
        if t > T_GO: text_layer(img, [(x, P0 + 98, ['1ST', '2ND', '3RD', '4TH'][rk], 26, (255, 214, 60) if rk == 0 else (220, 220, 220), 4, 255)])
    if t < T_GO:
        if t >= 0.6: text_layer(img, [(CX, 900, str(max(1, 3 - int((t - 0.6) / 0.6))), 150, (255, 214, 60), 12, 255)])
    elif t < T_GO + 0.6:
        text_layer(img, [(CX, 900, 'GO!', 150, (120, 255, 120), 12, int(255 * (1 - (t - T_GO) / 0.6)))])
    if t >= T_WIN + 0.6:
        u = t - T_WIN - 0.6; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], fill=(10, 8, 18, int(175 * a))))
        if a > 0.2:
            vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1040 - vf.height))
            text_layer(img, [(W / 2, 1075, LABEL[WIN] + ' WINS!', 64, (255, 214, 60), 8, int(255 * a)),
                             (W / 2, 1175, 'DID YOUR MARBLE WIN?', 30, (255, 255, 255), 6, int(255 * a))])
            rr = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                x_, y_ = rr.uniform(80, 1000), (rr.uniform(0, H) + u * 400) % (1480 - P1) + P1
                dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p58_{f:04d}.png')
wr.close()
json.dump({'events': EV}, open(OUT + 'v58_ev.json', 'w'))
print('done', round(T_END, 2), len(EV))
