import sys; sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, '../../fork_rc3'); from rc3 import acv_gummy_strong
import numpy as np, pymunk
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../../fork1')
DUR = 14.0
BG0 = bg_frames('hub.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.8)
SH = 300   # background raised 300px so the plaza ground sits under the new floor; bottom strip repeated
BG = []
for b in BG0:
    nb = Image.new('RGBA', (W, H)); nb.paste(b, (0, -SH)); nb.paste(b.crop((0, H - SH, W, H)), (0, H - SH)); BG.append(nb)
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['WHICH GUMMY', 'MAKES IT FALL?'], accent=1)   # Oct 29: soft fade, no box, comment line cut
PED = up(crop(Image.open('../../fork2/pedestal/00.png').convert('RGBA')), 2)   # prop 4x -> 2x so the 8-gummy tower (gummies still 4x) fits under the hook
CX = 478; FLOOR = 1495; PTOP = FLOOR - PED.height + 8
SEQ = ['acv', 'cre', 'mush', 'mel', 'cre', 'acv', 'mush', 'mel']
LBL = {'acv': 'ACV GUMMY', 'cre': 'CREATINE', 'mush': 'MUSHROOM', 'mel': 'MELATONIN'}
LCOL = {'acv': (120, 200, 90), 'cre': (110, 160, 255), 'mush': (255, 160, 50), 'mel': (205, 125, 245)}
SPR = {k: gummy(k, 4) for k in set(SEQ)}; SPR['acv'] = up(acv_gummy_strong(), 4)
NEST = 17  # soft gummies nest into each other a little so the 8-high tower clears the hook band
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
    hgt = SPR[k].height; y = y - hgt + (1 if i == 0 else NEST)
    rest.append((CX + OFF[i], y + hgt / 2)); y = y
TD = [-0.3 + sum([0, 1.05, 0.95, 1.05, 0.9, 1.0, 0.85, 0.95][:i + 1]) for i in range(len(SEQ))]; FALL = 0.45  # uneven drop rhythm (no metronome); #1 already mid-fall on frame 0
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
for seg in [((75, 0), (75, FLOOR)), ((880, 0), (880, FLOOR))]:
    wl = pymunk.Segment(space.static_body, seg[0], seg[1], 6); wl.friction = 0.6; wl.elasticity = 0.3; space.add(wl)
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
for f in range(int((DUR - T_TIP) * FPS) + 2):  # (NEST overlap: hulls collide, the pile pushes apart on the tip)
    PH.append([(b.position.x, b.position.y, b.angle) for b in bodies])
    for _ in range(6): space.step(1 / (FPS * 6))
WATCH = {'joy': (152, 1478), 'cyrus': (318, 1495), 'cleo': (648, 1495), 'ray': (800, 1478)}
IDL = {g: idle(g, 4) for g in WATCH}
PAN = {g: seq(PL + f'maze/anim/{g}_panic', 4, 1) for g in WATCH}
print('hook bottom', HB, 'tower top', min(r[1] - SPR[k].height / 2 for r, k in zip(rest, SEQ)))
T_ASK = T_TIP + 1.5; T_SWEEP = T_ASK + 1.3; T_END = T_SWEEP + 0.27; N = int(round(T_END * FPS))
ev = [(round(td + FALL, 3), 'squish') for td in TD if td + FALL > 0] + [(T_TIP + 0.15, 'boing'), (T_TIP + 0.5, 'boom'), (T_ASK, 'twinkle'), (T_SWEEP, 'swish')]
print('tip', T_TIP, 'ask', T_ASK, 'end', T_END)
w = Writer('v62_noaudio.mp4')
OUTD = os.path.dirname(os.path.abspath(sys.argv[0]))
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
            if u < 1: y = (HB - 40) + (ry - (HB - 40)) * u * u; x = rx; ang = 0; sq = 1   # Oct 29: drops start just under the hook text, not behind it
            else:
                x, y = rot(rx, ry, a); ang = a; sq = 1 + 0.15 * max(0, 1 - (u - 1) * FALL / 0.15) if u * FALL - FALL < 0.15 else 1
            s = SPR[k]
            if sq != 1: s = s.resize((int(s.width * sq), int(s.height / sq)), Image.NEAREST)
            if ang: s = s.rotate(-math.degrees(ang), resample=Image.NEAREST, expand=True)
            img.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2 + (s.height * (1 - 1 / sq) / 2 if sq != 1 else 0))))
    else:
        ph = PH[min(int((t - T_TIP) * FPS), len(PH) - 1)]
        sw = max(0.0, (t - T_SWEEP) / (T_END - T_SWEEP)) ** 1.5 * 1400
        for i, k in enumerate(SEQ):
            x, y, ang = ph[i]; x += sw * (1 if x >= CX else -1); s = SPR[k].rotate(-math.degrees(ang), resample=Image.NEAREST, expand=True)
            img.alpha_composite(s, (int(x - s.width / 2), int(y - s.height / 2)))
    # watchers
    for g, (wx, wy) in sorted(WATCH.items(), key=lambda kv: kv[1][1]):
        fr = PAN[g][int(t * 10) % len(PAN[g])] if T_TIP + 0.3 < t < T_TIP + 2.4 else IDL[g][int(t * 6) % 6]
        layer(img, lambda d: d.ellipse([wx - 64, wy - 12, wx + 64, wy + 12], fill=(0, 0, 0, 80)))
        img.alpha_composite(fr, (int(wx - fr.width / 2), int(wy - 78 * 4)))
    # one fixed chip right of the stack: '#n' + gummy name, stays until the next gummy lands
    cur = [i for i in range(len(SEQ)) if TD[i] - 0.1 <= t] if t < T_TIP else []
    if cur:
        i = cur[-1]; k = SEQ[i]; u = t - TD[i] + 0.1; pop = 1.0 if u > 0.12 else 0.75 + 2 * u
        # Oct 29: chip text only, no box (the #n + name is the comment vocabulary)
        text_layer(img, [(802, 916, f'#{i + 1}', int(64 * pop), (255, 255, 255), 9, 255), (802, 998, LBL[k], 44, LCOL[k], 8, 255)])
    if t >= T_TIP + 0.1:
        u = t - T_TIP - 0.1; sc = min(1, u / 0.15)
        d = ImageDraw.Draw(img)
        ctext(d, CX + int(6 * math.sin(u * 40) * max(0, 1 - u)), 650, 'TIMBER!', F(int(96 * (0.6 + 0.4 * sc))), (240, 80, 70), 9)
    # Oct 29: DID YOU / GUESS RIGHT? end plate cut (the hook already asks; the pile stays visible for the hold)
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (0, 100, 215, 250, 290, 320, N - 3): img.convert('RGB').save(f'k62_{f}.png')
w.close(); json.dump({'events': sorted(ev)}, open('v62_ev.json', 'w')); print('done', N / FPS)
