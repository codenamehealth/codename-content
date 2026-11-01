import sys; sys.path.insert(0, '../fork1'); from common import *
import numpy as np, pymunk
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 13.5; N = int(DUR * FPS)
BG = bg_frames('hub.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.8)
PED = up(crop(Image.open('../fork2/pedestal/00.png').convert('RGBA')), 4)
CX = 540; FLOOR = 1760; PTOP = FLOOR - PED.height + 16
SEQ = ['acv', 'cre', 'mush', 'mel', 'cre', 'acv', 'mush', 'mel']
LBL = {'acv': 'ACV', 'cre': 'CREATINE', 'mush': 'MUSHROOM', 'mel': 'MELATONIN'}
LCOL = {'acv': (120, 200, 90), 'cre': (110, 160, 255), 'mush': (255, 160, 50), 'mel': (205, 125, 245)}
SPR = {k: gummy(k, 4) for k in set(SEQ)}
def hull(img):
    a = np.array(img)[:, :, 3] > 0; pts = []
    for y in range(0, a.shape[0], 2):
        xs = np.where(a[y])[0]
        if len(xs): pts += [(xs[0], y), (xs[-1] + 1, y)]
    ys = np.where(a.any(1))[0]; xs = np.where(a[ys[-1]])[0]; pts += [(xs[0], ys[-1] + 1), (xs[-1] + 1, ys[-1] + 1)]
    return [(x - img.width / 2, y - img.height / 2) for x, y in pts]
HULL = {k: hull(v) for k, v in SPR.items()}
# build: stacked rest positions (center coords, relative to pivot at pedestal top centre)
OFF = [0, 6, -8, 10, 4, 14, 20, 34]
rest = []; y = PTOP
for i, k in enumerate(SEQ):
    hgt = SPR[k].height; y = y - hgt - 1
    rest.append((CX + OFF[i], y + hgt / 2)); y = y
TD = [0.9 + 1.0 * i for i in range(len(SEQ))]; FALL = 0.45
T_TIP = TD[-1] + FALL + 0.75
def sway(t):
    n = sum(1 for td in TD if td + FALL <= t)
    if n == 0: return 0.0
    amp = 0.004 * n ** 1.6
    base = 0.0
    if t > TD[-1] + FALL: base = 0.06 * min(1, (t - TD[-1] - FALL) / 0.75) ** 2
    return amp * math.sin(t * 5.2) + base
def rot(px, py, a):
    dx, dy = px - CX, py - PTOP; c, s = math.cos(a), math.sin(a)
    return CX + dx * c - dy * s, PTOP + dx * s + dy * c
# collapse physics
space = pymunk.Space(); space.gravity = (0, 2600)
ground = pymunk.Segment(space.static_body, (-400, FLOOR), (1480, FLOOR), 4); ground.friction = 0.9; ground.elasticity = 0.35
pedb = pymunk.Poly.create_box(space.static_body, (PED.width - 20, PED.height - 20)); 
pedb = pymunk.Poly(space.static_body, [(CX - PED.width / 2 + 10, PTOP), (CX + PED.width / 2 - 10, PTOP), (CX + PED.width / 2 - 10, FLOOR), (CX - PED.width / 2 + 10, FLOOR)]); pedb.friction = 0.8
space.add(ground, pedb)
bodies = []
a0 = sway(T_TIP); w0 = 0.6
for i, k in enumerate(SEQ):
    m = 1.0; mom = pymunk.moment_for_poly(m, HULL[k])
    b = pymunk.Body(m, mom); px, py = rot(*rest[i], a0); b.position = (px, py); b.angle = a0
    r = math.hypot(px - CX, py - PTOP); b.velocity = (w0 * (PTOP - py) * -1 * 0 + w0 * (py - PTOP) * -1, w0 * (px - CX))
    b.angular_velocity = w0
    sh = pymunk.Poly(b, HULL[k]); sh.friction = 0.7; sh.elasticity = 0.4
    space.add(b, sh); bodies.append(b)
PH = []
for f in range(int((DUR - T_TIP) * FPS) + 2):
    PH.append([(b.position.x, b.position.y, b.angle) for b in bodies])
    for _ in range(6): space.step(1 / (FPS * 6))
WATCH = {'joy': (150, 1790), 'cyrus': (330, 1840), 'cleo': (750, 1840), 'ray': (930, 1790)}
IDL = {g: idle(g, 3) for g in WATCH}
PAN = {g: seq(PL + f'maze/anim/{g}_panic', 3, 1) for g in WATCH}
ev = [(td + FALL, 'stomp_8bit') for td in TD[:-1]] + [(TD[-1] + FALL, 'stomp_8bit'), (T_TIP + 0.15, 'boing'), (T_TIP + 0.5, 'boom'), (11.4, 'twinkle')]
w = Writer('v62_noaudio.mp4')
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: d.ellipse([CX - 120, FLOOR - 18, CX + 120, FLOOR + 18], fill=(0, 0, 0, 90)))
    img.alpha_composite(PED, (CX - PED.width // 2, FLOOR - PED.height))
    if t < T_TIP:
        a = sway(t)
        for i, k in enumerate(SEQ):
            if t < TD[i]: continue
            u = (t - TD[i]) / FALL
            rx, ry = rest[i]
            if u < 1: y = (380) + (ry - 380) * u * u; x = rx; ang = 0; sq = 1
            else:
                x, y = rot(rx, ry, a); ang = a; sq = 1 + 0.15 * max(0, 1 - (u - 1) * FALL / 0.15) if u * FALL - FALL < 0.15 else 1
            s = SPR[k]
            if sq != 1: s = s.resize((int(s.width * sq), int(s.height / sq)), Image.NEAREST)
            if ang: s = s.rotate(-math.degrees(ang), resample=Image.NEAREST, expand=True)
            img.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2 + (s.height * (1 - 1 / sq) / 2 if sq != 1 else 0))))
    else:
        ph = PH[min(int((t - T_TIP) * FPS), len(PH) - 1)]
        for i, k in enumerate(SEQ):
            x, y, ang = ph[i]; s = SPR[k].rotate(-math.degrees(ang), resample=Image.NEAREST, expand=True)
            img.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2)))
    # watchers
    for g, (wx, wy) in sorted(WATCH.items(), key=lambda kv: kv[1][1]):
        fr = PAN[g][int(t * 10) % len(PAN[g])] if T_TIP + 0.3 < t < T_TIP + 2.4 else IDL[g][int(t * 6) % 6]
        layer(img, lambda d: d.ellipse([wx - 50, wy - 10, wx + 50, wy + 10], fill=(0, 0, 0, 80)))
        img.alpha_composite(fr, (int(wx - fr.width / 2), int(wy - 78 * 3)))
    # labels
    items = []
    for i, k in enumerate(SEQ):
        if TD[i] - 0.25 <= t < TD[i] + 0.95 and t < T_TIP:
            u = t - TD[i] + 0.25; a_ = int(255 * min(1, u / 0.15, (1.2 - u) / 0.2))
            items.append((CX, 440, f'#{i + 1} {LBL[k]}', 40, LCOL[k], 6, max(0, a_)))
    layer(img, lambda d: d.rectangle([0, 100, W, 330], fill=(12, 10, 26, 200)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 140, 'WHICH GUMMY', F(64), (255, 255, 255), 7)
    ctext(d, W / 2, 230, 'MAKES IT FALL?', F(64), (232, 182, 76), 7)
    text_layer(img, items)
    if 1.5 < t < T_TIP:
        layer(img, lambda dd: dd.rounded_rectangle([170, 520, 910, 590], 18, fill=(12, 10, 26, 190)))
        d = ImageDraw.Draw(img); ctext(d, W / 2, 536, 'Comment your guess', F(34), (255, 255, 255), 5)
    if t >= T_TIP + 0.1:
        u = t - T_TIP - 0.1; sc = min(1, u / 0.15)
        d = ImageDraw.Draw(img)
        ctext(d, W / 2 + int(6 * math.sin(u * 40) * max(0, 1 - u)), 640, 'TIMBER!', F(int(96 * (0.6 + 0.4 * sc))), (240, 80, 70), 9)
    if t >= 11.4:
        u = min(1, (t - 11.4) / 0.3)
        layer(img, lambda dd: dd.rounded_rectangle([130, 790, 950, 900], 24, fill=(12, 10, 26, int(220 * u))))
        d = ImageDraw.Draw(img); ctext(d, W / 2, 822, 'Did you guess right?', F(40), (232, 182, 76), 6, int(255 * u))
    w.write(img)
    if f in (100, 245, 285, 300, 330, 380): img.convert('RGB').save(f'k62_{f}.png')
w.close(); json.dump(ev, open('v62_ev.json', 'w')); print('tip', T_TIP)
