import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['hollow', 'joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    d.ellipse([12, 9, 20, 15], fill=(255, 255, 255, 170))
    return b
RB = 30
ORB = {n: face(n, RB) for n in NAMES}
def sleepy(im):
    g = ImageEnhance.Color(im).enhance(0.25); return ImageEnhance.Brightness(g).enhance(0.6)
ORBS = {n: sleepy(ORB[n]) for n in NAMES}
CX, CY = 540, 1060
RINGS = [170, 290, 410]; TH = 16
LIFE = float(os.environ.get("LIFE","1.3")); SPD = float(os.environ.get("SPD","1000"))
GK = ['mush', 'acv', 'mel', 'cre']
GPOS = [(230, 1.0), (350, 3.3), (230, 4.4), (350, 5.6)]   # (radius, angle) gummy spots between rings
def sim(seed, dur=18.0):
    rnd = random.Random(seed)
    spd = [rnd.choice([1, -1]) * rnd.uniform(35, 55), rnd.choice([1, -1]) * rnd.uniform(50, 75), rnd.choice([1, -1]) * rnd.uniform(70, 95)]
    if spd[0] * spd[1] > 0: spd[1] *= -1
    if spd[1] * spd[2] > 0: spd[2] *= -1
    gaps = [math.radians(32), math.radians(27), math.radians(23)]
    ph0 = [rnd.uniform(0, 6.28) for _ in RINGS]
    sleepers = []; ball = None; att = 0; frames = []; events = []; esc = None; gum_alive = [True] * 4
    t_next = 1.2
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        rot = [ph0[i] + math.radians(spd[i]) * t for i in range(3)]
        if ball is None and esc is None and t >= t_next:
            n = NAMES[att % 5]; a = rnd.uniform(0, 6.28)
            ball = dict(n=n, x=CX, y=CY, vx=SPD * math.cos(a), vy=SPD * math.sin(a), t0=t, boost=1.0, trail=[])
            att += 1; events.append((t, 'launch', n)); gum_alive = [True] * 4
        if ball is not None:
            sub = 4
            for _ in range(sub):
                b = ball; b['x'] += b['vx'] * dt / sub * b['boost']; b['y'] += b['vy'] * dt / sub * b['boost']
                px, py = b['x'] - CX, b['y'] - CY; r = math.hypot(px, py) or 1e-6; nx, ny = px / r, py / r
                for i, R in enumerate(RINGS):
                    if abs(r - R) < RB + TH / 2:
                        ang = math.atan2(py, px); da = (ang - rot[i] + math.pi) % (2 * math.pi) - math.pi
                        if abs(da) > gaps[i] - (RB * 0.8) / R:
                            vn = b['vx'] * nx + b['vy'] * ny
                            if (r < R and vn > 0) or (r > R and vn < 0):
                                b['vx'] -= 2 * vn * nx; b['vy'] -= 2 * vn * ny
                                ja = rnd.uniform(-0.25, 0.25); c, s = math.cos(ja), math.sin(ja)
                                b['vx'], b['vy'] = b['vx'] * c - b['vy'] * s, b['vx'] * s + b['vy'] * c
                                if not events or events[-1][1] != 'bonk' or t - events[-1][0] > 0.08: events.append((t, 'bonk', i))
                for s in sleepers:
                    dx, dy = b['x'] - s['x'], b['y'] - s['y']; d = math.hypot(dx, dy)
                    if 0 < d < 2 * RB:
                        ux, uy = dx / d, dy / d; vn = b['vx'] * ux + b['vy'] * uy
                        if vn < 0: b['vx'] -= 2 * vn * ux; b['vy'] -= 2 * vn * uy; events.append((t, 'tap', 0))
                        b['x'] = s['x'] + ux * 2 * RB; b['y'] = s['y'] + uy * 2 * RB
                for gi, (gr, ga) in enumerate(GPOS):
                    if gum_alive[gi]:
                        gx, gy = CX + gr * math.cos(ga), CY + gr * math.sin(ga)
                        if math.hypot(b['x'] - gx, b['y'] - gy) < RB + 22:
                            gum_alive[gi] = False; b['boost'] = min(1.5, b['boost'] + 0.18); events.append((t, 'gum', gi))
            b['trail'] = (b['trail'] + [(b['x'], b['y'])])[-10:]
            if math.hypot(b['x'] - CX, b['y'] - CY) > RINGS[-1] + RB + 14:
                esc = (b['n'], t, att); events.append((t, 'escape', b['n'])); ball = None
            elif t - b['t0'] > LIFE:
                sleepers.append(dict(n=b['n'], x=b['x'], y=b['y'], t=t)); events.append((t, 'sleep', b['n'])); ball = None; t_next = t + 0.15
        frames.append(dict(rot=list(rot), ball=None if ball is None else dict(ball, trail=list(ball['trail'])), sleepers=list(sleepers), att=att, gums=list(gum_alive)))
        if esc and t > esc[1] + 3.2: break
    return frames, events, esc, gaps
def score(seed):
    fr, ev, esc, g = sim(seed)
    if not esc: return None
    n, t, att = esc
    if n == 'hollow' or not (8 <= att <= 11) or not (11.0 <= t <= 16.0): return None
    return n, round(t, 2), att
if __name__ == '__main__' and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, ESC, GAPS = sim(SEED)
print('escape', ESC)
BGF = bg_frames('sun_hd.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.42)
TINT = Image.new('RGBA', (W, H), (40, 20, 70, 90))
win = ESC[0]; T_ESC = ESC[1]; VICF = vic(win, 300)
GUM = {k: gummy(k, 2) for k in GK}
END = T_ESC + 3.2; wr = Writer('blink_noaudio.mp4'); out = []
rr = random.Random(3); STARS = [(rr.uniform(0, W), rr.uniform(380, 1700), rr.uniform(0, 6)) for _ in range(70)]
for f in range(int(END * FPS)):
    t = f / FPS; st = FR[min(f, len(FR) - 1)]
    img = BGF[int(t * 6) % len(BGF)].copy(); img.alpha_composite(TINT)
    def deco(d):
        for (sx, sy, ph) in STARS:
            a = int(90 + 90 * math.sin(t * 3 + ph)); d.rectangle([sx, sy, sx + 3, sy + 3], fill=(255, 230, 160, max(0, a)))
        d.ellipse([CX - 470, CY - 470, CX + 470, CY + 470], fill=(10, 6, 22, 120))
    layer(img, deco)
    # rings
    def rings(d):
        for i, R in enumerate(RINGS):
            g = math.degrees(GAPS[i]); c = math.degrees(st['rot'][i])
            a0, a1 = c + g, c + 360 - g
            for w, col in ((TH + 10, (60, 30, 10, 255)), (TH, (232, 180, 60, 255)), (4, (255, 236, 150, 255))):
                d.arc([CX - R, CY - R, CX + R, CY + R], a0, a1, fill=col, width=w)
            # gear teeth
            nt = int(R / 9)
            for k in range(nt):
                ang = math.radians(c + g + (360 - 2 * g) * (k + 0.5) / nt)
                for rad in (R + TH / 2 + 3, R - TH / 2 - 3):
                    x, y = CX + rad * math.cos(ang), CY + rad * math.sin(ang)
                    d.rectangle([x - 3, y - 3, x + 3, y + 3], fill=(200, 140, 40, 255))
            # glowing gap ends
            for e in (c + g, c - g):
                ang = math.radians(e); x, y = CX + R * math.cos(ang), CY + R * math.sin(ang)
                p = 0.5 + 0.5 * math.sin(t * 8 + i)
                d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=(255, 250, 200, int(120 + 100 * p)))
        d.ellipse([CX - 18, CY - 18, CX + 18, CY + 18], fill=(255, 220, 120, 160))
    layer(img, rings)
    for gi, (gr, ga) in enumerate(GPOS):
        if st['gums'][gi] and st['ball'] is not None:
            g = GUM[GK[gi]]; bob = int(5 * math.sin(t * 5 + gi))
            img.alpha_composite(g, (int(CX + gr * math.cos(ga) - g.width / 2), int(CY + gr * math.sin(ga) - g.height / 2 + bob)))
    for s in st['sleepers']:
        o = ORBS[s['n']]; img.alpha_composite(o, (int(s['x'] - o.width / 2), int(s['y'] - o.height / 2)))
    def zz(d):
        for s in st['sleepers']:
            u = (t - s['t']) * 1.2 + (hash(s['n'] + str(int(s['t'] * 10))) % 10) / 10
            k = u % 1.0; d.text((s['x'] + 14 + 10 * k, s['y'] - 36 - 22 * k), 'z', font=F(18), fill=(230, 230, 255, int(220 * (1 - k))))
    layer(img, zz)
    b = st['ball']
    if b:
        col = RING[b['n']]
        def tr(d):
            for i, (x, y) in enumerate(b['trail'][:-1]):
                a = int(40 + 150 * i / len(b['trail'])); rr_ = 8 + 2 * i
                d.ellipse([x - rr_, y - rr_, x + rr_, y + rr_], fill=col + (a,))
        layer(img, tr)
        o = ORB[b['n']]; img.alpha_composite(o, (int(b['x'] - o.width / 2), int(b['y'] - o.height / 2)))
        if b['boost'] > 1.01:
            layer(img, lambda d: d.ellipse([b['x'] - RB - 8, b['y'] - RB - 8, b['x'] + RB + 8, b['y'] + RB + 8], outline=(255, 220, 90, 220), width=4))
    # popups
    items = []
    for (te, kind, arg) in EV:
        u = t - te
        if kind == 'gum' and 0 <= u < 0.8:
            gr, ga = GPOS[arg]; items.append((CX + gr * math.cos(ga), CY + gr * math.sin(ga) - 40 - u * 60, 'SPEED UP!', 24, (255, 214, 60), 5, int(255 * min(1, (0.8 - u) / 0.3))))
    text_layer(img, items)
    # header
    def hdr(d):
        d.rectangle([0, 0, W, 330], fill=(12, 8, 24, 190))
        d.rectangle([0, H - 300, W, H], fill=(12, 8, 24, 150))
    layer(img, hdr)
    text_layer(img, [(W / 2, 70, "DON'T BLINK", 72, (255, 255, 255), 8, 255), (W / 2, 170, 'UNTIL ONE ESCAPES!', 40, (255, 214, 60), 6, 255),
                     (W / 2, 250, 'Pick a guide', 28, (220, 210, 255), 5, 255 if t < 3 else 0)])
    d = ImageDraw.Draw(img)
    # roster strip
    for i, n in enumerate(['joy', 'cyrus', 'cleo', 'ray', 'hollow']):
        sx = W / 2 + (i - 2) * 150; o = ORB[n] if not any(s['n'] == n for s in st['sleepers'][-5:]) or True else ORBS[n]
        img.alpha_composite(o, (int(sx - o.width / 2), H - 250))
    text_layer(img, [(W / 2, H - 150, f"ATTEMPTS: {st['att']}", 40, (255, 255, 255), 6, 255)])
    if t >= T_ESC:
        u = t - T_ESC
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 14, int(150 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1010 - vf.height))
        def conf(d):
            r2 = random.Random(f)
            for _ in range(50):
                x, y = r2.uniform(0, W), (r2.uniform(0, H) + u * 600) % H
                d.rectangle([x, y, x + 10, y + 10], fill=r2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (190, 90, 240), (255, 160, 40)]) + (255,))
        layer(img, conf)
        text_layer(img, [(W / 2, 1060, LABEL[win] + ' ESCAPED!', 60, (255, 214, 60), 8, 255), (W / 2, 1150, f'on attempt {ESC[2]}', 34, (255, 255, 255), 6, 255)])
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close()
ev = []
for (te, kind, arg) in EV:
    if kind == 'bonk': ev.append((round(te, 3), 'tick_8bit'))
    elif kind == 'gum': ev.append((round(te, 3), 'coin_8bit'))
    elif kind == 'sleep': ev.append((round(te, 3), 'poof'))
    elif kind == 'launch': ev.append((round(te, 3), 'whoosh_8bit'))
    elif kind == 'escape': ev.append((round(te, 3), 'victory'))
json.dump(ev, open('blink_ev.json', 'w')); print('done', round(END, 2))
