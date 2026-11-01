# r051 recut (rc7). Approved reel: same concept (Cleo vs Cyrus marble race over Liza's castle), Cleo still wins.
# Fixes: gate open on frame 0 + GO! flash; 2 of 3 zigzag ramps cut (payoff earlier); marbles 1.5x (~100px);
# gold SPEED gummies -> one of each product gummy with its own power (SPEC 12), vanish on touch; gummy bumpers -> neutral bumpers;
# lead flips flash the strip in the leader's colour with a 48px line; comment prompt in the hook band from frame 0;
# end hold 1.4s then cut back to frame 0 (loop); end text big.
import sys, os, math, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = HERE + '/'
SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP + 'fork1'); sys.path.insert(0, HERE); sys.path.insert(0, SP + 'fork_rc1'); sys.path.insert(0, SP + 'fork_rc3'); sys.path.insert(0, SP + 'fork_hfg5')
from common import *
from hk import hook_fade_segs
from rc3 import acv_gummy_strong
from sim51r import sim, R
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 3
PREVIEW = len(sys.argv) > 2
FR, EV, FIN_T, LEADS, SEGS, PEGS, BUMPERS, SPINNERS, PICKUPS, FIN = sim(SEED)
win = min(FIN_T, key=FIN_T.get); lose = [n for n in FIN_T if n != win][0]
TEND = FIN_T[win] + 0.6; HOLD = 1.4; NF = int(round((TEND + HOLD) * FPS))
print('winner', win, FIN_T, 'leads', len(LEADS), 'dur', round(NF / FPS, 2))
L = 3; WY0 = -500; WH = 6200
def MX(x): return 70 + (x - 50) * 0.976
# hfg5: soft fade, no box; 'Comment your pick' sub cut (caption asks); CLEO blue / CYRUS orange = their marble rings
HK, HB = hook_fade_segs([[('PICK YOUR MARBLE', (255, 255, 255))], [('CLEO', (90, 150, 255)), (' OR ', (255, 255, 255)), ('CYRUS', (255, 160, 40))]])
STRIP0, STRIP1 = HB + 8, HB + 128
BAND_BOT = 1090; MID = 925
# ---------- static course (walls, planks, small studs, finish) ----------
course = Image.new('RGBA', (W // L, WH // L), (0, 0, 0, 0)); d = ImageDraw.Draw(course)
def Y(y): return (y - WY0) / L
for (a, b, r, kind) in SEGS:
    p = [(MX(a[0]) / L, Y(a[1])), (MX(b[0]) / L, Y(b[1]))]
    if kind == 'wall':
        x = MX(a[0]) / L; d.rectangle([x - 6, 0, x + 6, WH // L], fill=(70, 66, 80, 255))
        for yy in range(0, WH // L, 8): d.line([(x - 6, yy), (x + 6, yy)], fill=(45, 42, 55, 255)); d.line([(x - 6 + (yy // 8 % 2) * 6, yy), (x - 6 + (yy // 8 % 2) * 6, yy + 8)], fill=(45, 42, 55, 255))
        d.line([(x + (5 if x < 100 else -5), 0), (x + (5 if x < 100 else -5), WH // L)], fill=(110, 105, 120, 255))
    else:
        d.line(p, fill=(52, 30, 12, 255), width=9); d.line(p, fill=(150, 96, 48, 255), width=6)
        d.line([(p[0][0], p[0][1] - 2), (p[1][0], p[1][1] - 2)], fill=(196, 140, 84, 255), width=1)
        n = int(math.hypot(p[1][0] - p[0][0], p[1][1] - p[0][1]) // 30)
        for k in range(1, n):
            u = k / n; x, y = p[0][0] + (p[1][0] - p[0][0]) * u, p[0][1] + (p[1][1] - p[0][1]) * u
            d.point((x, y), fill=(60, 36, 16, 255))
for (x, y, r, kind, c) in PEGS:
    if kind == 'ball': continue
    X, Yy, rr = MX(x) / L, Y(y), r / L
    d.ellipse([X - rr - 1, Yy - rr - 1, X + rr + 1, Yy + rr + 1], fill=(90, 58, 12, 255)); d.ellipse([X - rr, Yy - rr, X + rr, Yy + rr], fill=(232, 180, 60, 255))
    d.point((X - 1, Yy - 2), fill=(255, 240, 180, 255)); d.point((X - 2, Yy - 1), fill=(255, 240, 180, 255))
fy = Y(FIN)
for i in range(0, W // L, 6):
    for j in range(2):
        d.rectangle([i, fy + j * 6, i + 5, fy + j * 6 + 5], fill=(240, 240, 240, 255) if (i // 6 + j) % 2 else (20, 20, 24, 255))
COURSE = up(course, L)
BG = bg_frames('vit_hd.gif', (W, H), box=(560, 0, 1167, 1080), step=2, bright=0.38)
# ---------- sprites ----------
def stone_ball(rr):
    s = int(rr * 2 / L) + 3; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); c = (s - 1) / 2; q = rr / L
    dd.ellipse([c - q - 1, c - q - 1, c + q + 1, c + q + 1], fill=(60, 52, 48, 255)); dd.ellipse([c - q, c - q, c + q, c + q], fill=(206, 196, 176, 255))
    dd.ellipse([c - q * 0.6, c - q * 0.7, c - q * 0.1, c - q * 0.25], fill=(240, 234, 220, 255)); return up(im, L)
STONE = stone_ball(40)
def bumper_img():
    s = 32; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.ellipse([0, 0, 31, 31], fill=(24, 20, 34, 255)); dd.ellipse([2, 2, 29, 29], fill=(150, 156, 178, 255))
    dd.ellipse([5, 5, 26, 26], fill=(84, 88, 112, 255)); dd.ellipse([9, 9, 22, 22], fill=(200, 60, 60, 255)); dd.ellipse([12, 12, 19, 19], fill=(250, 220, 120, 255))
    for a in range(8):
        x = 15.5 + math.cos(a * math.pi / 4) * 12.5; y = 15.5 + math.sin(a * math.pi / 4) * 12.5; dd.point((x, y), fill=(220, 224, 236, 255))
    dd.arc([3, 3, 28, 28], 200, 260, fill=(235, 238, 248, 255), width=2)
    return up(im, 3)
BUMP = bumper_img()
GSRC = {'mush': gummy('mush', 1), 'cre': gummy('cre', 1), 'mel': gummy('mel', 1), 'acv': acv_gummy_strong()}
GUM = {k: up(v, 3) for k, v in GSRC.items()}; GI = {k: up(v, 2) for k, v in GSRC.items()}
GCOL = {'mush': (255, 170, 50), 'cre': (255, 90, 60), 'mel': (200, 130, 255), 'acv': (110, 230, 110)}
POW = {'mush': 'SPEED!', 'cre': 'STRONG!', 'mel': 'SLEEP!', 'acv': 'SHIELD!'}
def face(name, rad):
    SRC = {'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); dd = ImageDraw.Draw(b)
    dd.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); dd.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    dd.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    dd.ellipse([int(rad * 0.35), int(rad * 0.25), int(rad * 0.65), int(rad * 0.45)], fill=(255, 255, 255, 150))
    return b
RING = {'cleo': (90, 150, 255), 'cyrus': (255, 160, 40)}
BALL = {n: face(n, int(R * 0.976)) for n in RING}; ICS2 = {n: face(n, 44) for n in RING}; ICS = {n: face(n, 26) for n in RING}; ICON = {n: face(n, 34) for n in RING}
LABEL = {'cleo': 'CLEO', 'cyrus': 'CYRUS'}
VICF = vic(win, 360)
def podium():
    im = Image.new('RGBA', (80, 28), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rectangle([0, 0, 79, 27], fill=(20, 16, 30, 255)); dd.rectangle([2, 2, 77, 25], fill=(120, 110, 140, 255)); dd.rectangle([2, 2, 77, 5], fill=(190, 182, 210, 255))
    dd.rectangle([2, 22, 77, 25], fill=(80, 72, 98, 255)); dd.rectangle([36, 8, 43, 19], fill=(255, 214, 60, 255)); dd.rectangle([34, 8, 36, 10], fill=(255, 214, 60, 255)); dd.rectangle([34, 18, 45, 19], fill=(255, 214, 60, 255))
    return up(im, 4)
PODIUM = podium()
def spinner_img(angle):
    S = 120; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); c = S / 2
    for a in range(4):
        ang = angle + a * math.pi / 2; ex = (c + math.cos(ang) * 55, c + math.sin(ang) * 55)
        dd.line([(c, c), ex], fill=(52, 30, 12, 255), width=9); dd.line([(c, c), ex], fill=(170, 110, 52, 255), width=6)
    dd.ellipse([c - 7, c - 7, c + 7, c + 7], fill=(40, 40, 50, 255)); dd.ellipse([c - 5, c - 5, c + 5, c + 5], fill=(130, 130, 145, 255))
    return up(im, L)
SPOS = [(340 if k % 2 == 0 else 740, 3850 - 1440 + k * 260) for k in range(4)]
# ---------- events -> stamps ----------
picks = [e for e in EV if e[1] == 'pick']; blocks = {round(e[0], 3): e[2] for e in EV if e[1] == 'block'}
sleeps = [e for e in EV if e[1] == 'sleep']; smashes = [e for e in EV if e[1] == 'smash']
req = []
for e in picks:
    t, _, who, k = e
    if k == 'mel' and round(t, 3) in blocks: req.append((t, 'pow', who, k, 0.75)); req.append((t + 0.75, 'block', blocks[round(t, 3)], 'acv', 0.7))
    else: req.append((t, 'pow', who, k, 1.0))
req.sort(); STAMPS = []
for (te, kind, who, k, dur) in req:
    t0 = max([te] + [s[1] + 0.05 for s in STAMPS])
    if t0 - te > 0.8 or t0 + dur > TEND: continue
    STAMPS.append((t0, t0 + dur, kind, who, k))
print('stamps', [(round(a, 2), round(b, 2), c, w, k) for a, b, c, w, k in STAMPS])
STY = 1350
def stamp_layer(kind, who, k, u, dur):
    Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(Lr)
    a = int(255 * min(1, (dur - u) / 0.15)); pop = 1.0 if u > 0.1 else 0.7 + 0.3 * u / 0.1
    txt = POW[k] if kind == 'pow' else 'BLOCKED!'; col = GCOL[k]
    f = F(int(72 * pop)); tw = dd.textlength(txt, font=f); ic = ICON[who]; gi = GI[k]
    w = ic.width + 14 + gi.width + 22 + tw + 48; h = int(112 * pop); x0 = 478 - w / 2; y0 = STY + (112 - h) / 2
    # hfg5: no plate behind the power stamp (face + gummy + stroked word)
    ic2 = ic.copy(); ic2.putalpha(Image.eval(ic2.getchannel('A'), lambda v: v * a // 255)); gi2 = gi.copy(); gi2.putalpha(Image.eval(gi2.getchannel('A'), lambda v: v * a // 255))
    Lr.alpha_composite(ic2, (int(x0 + 22), int(y0 + (h - ic.height) / 2))); Lr.alpha_composite(gi2, (int(x0 + 22 + ic.width + 12), int(y0 + (h - gi.height) / 2)))
    dd.text((x0 + 22 + ic.width + 14 + gi.width + 18, y0 + (h - f.size) / 2), txt, font=f, fill=col + (a,), stroke_width=8, stroke_fill=(10, 6, 18, a))
    return Lr
# ---------- render ----------
lead_flash = -9; lead_prev = None; ev_out = [(0.25, 'go_8bit')]; last_sfx = -9
trails = {n: [] for n in BALL}
def render(f, cam, state):
    t = f / FPS; P, SA, lead, used, strong, frozen, shield, broken = FR[min(f, len(FR) - 1)]
    img = BG[int(t * 6) % len(BG)].copy()
    top = int(cam - WY0); img.alpha_composite(COURSE.crop((0, top, W, top + H)))
    for (x, y), ang in zip(SPOS, SA):
        sp = spinner_img(ang); img.alpha_composite(sp, (int(MX(x) - sp.width / 2), int(y - cam - sp.height / 2)))
    # breakable stone balls + bumpers (smashed by STRONG)
    fx = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fx)
    def debris(x, y, tb, col):
        u = t - tb
        if 0 <= u < 0.55:
            rnd = random.Random(int(x * 7 + y))
            for i in range(12):
                ang = rnd.uniform(0, 2 * math.pi); sp_ = rnd.uniform(250, 520); px = x + math.cos(ang) * sp_ * u; py = y - cam + math.sin(ang) * sp_ * u + 900 * u * u
                s = rnd.choice([9, 12, 15]); fd.rectangle([px - s / 2, py - s / 2, px + s / 2, py + s / 2], fill=col + (int(255 * (1 - u / 0.55)),))
            fd.ellipse([x - 70 - 90 * u, y - cam - 70 - 90 * u, x + 70 + 90 * u, y - cam + 70 + 90 * u], outline=(255, 120, 60, int(230 * (1 - u / 0.55))), width=8)
    for j, (x, y, r, kind, c) in enumerate(PEGS):
        if kind != 'ball': continue
        if ('peg', j) in broken: debris(MX(x), y, broken[('peg', j)], (206, 196, 176)); continue
        img.alpha_composite(STONE, (int(MX(x) - STONE.width / 2), int(y - cam - STONE.height / 2)))
    for j, (x, y, kind, c) in enumerate(BUMPERS):
        if ('bump', j) in broken: debris(MX(x), y, broken[('bump', j)], (150, 156, 178)); continue
        img.alpha_composite(BUMP, (int(MX(x) - BUMP.width / 2), int(y - cam - BUMP.height / 2)))
    # pickups: typed product gummies, gone the moment one is touched
    for i, (x, y, k) in enumerate(PICKUPS):
        x = MX(x)
        if i in used:
            u = t - used[i][0]
            if 0 <= u < 0.35:
                for a in range(8):
                    ang = a * math.pi / 4; rr = 30 + 160 * u
                    fd.rectangle([x + math.cos(ang) * rr - 7, y - cam + math.sin(ang) * rr - 7, x + math.cos(ang) * rr + 7, y - cam + math.sin(ang) * rr + 7], fill=GCOL[k] + (int(255 * (1 - u / 0.35)),))
            continue
        bob = 6 * math.sin(t * 4 + i); g = GUM[k]
        layer(img, lambda dd, x=x, y=y: dd.ellipse([x - 62, y - cam - 62 + bob, x + 62, y - cam + 62 + bob], fill=GCOL[k] + (60,)))
        img.alpha_composite(g, (int(x - g.width / 2), int(y - cam - g.height / 2 + bob)))
        # hfg5: 'ACV GUMMY' tag cut (SHIELD! names it when it fires)
    img.alpha_composite(fx)
    # marbles
    for n in P:
        x, y, a = P[n]; x = MX(x); trails[n] = (trails[n] + [(x, y)])[-10:]
        if y > FIN + 70: continue
        sy = y - cam
        spd = next((pt for (pt, _, w_, k_) in picks if w_ == n and k_ == 'mush' and 0 <= t - pt < 1.3), None)
        stg = n in strong; zz = n in frozen; sh = n in shield
        col = (255, 170, 50) if spd is not None else (255, 90, 60) if stg else RING[n]
        def tr(dd, n=n, col=col):
            for i, (tx, ty) in enumerate(trails[n][:-1]):
                rr = 8 + i * 3; al = int(30 + 150 * i / len(trails[n]))
                dd.ellipse([tx - rr, ty - cam - rr, tx + rr, ty - cam + rr], fill=col + (al,))
        if not zz: layer(img, tr)
        if spd is not None:
            def lines(dd, x=x, sy=sy):
                rnd = random.Random(f)
                for i in range(7):
                    lx = x + rnd.uniform(-48, 48); ly = sy - 70 - rnd.uniform(0, 90)
                    dd.line([(lx, ly), (lx, ly - rnd.uniform(60, 130))], fill=(255, 255, 255, 210), width=5)
                for i in range(4):
                    px = x + rnd.uniform(-60, 60); py = sy - 40 - rnd.uniform(0, 50); s = rnd.uniform(10, 20)
                    dd.ellipse([px - s, py - s, px + s, py + s], fill=(210, 190, 160, 140))
            layer(img, lines)
        if stg:
            def aura(dd, x=x, sy=sy):
                rr = R + 16 + 6 * math.sin(t * 30)
                dd.ellipse([x - rr, sy - rr, x + rr, sy + rr], fill=(255, 90, 40, 70), outline=(255, 140, 60, 230), width=7)
                for i in range(8):
                    ang = i * math.pi / 4 + t * 6; dd.line([(x + math.cos(ang) * (R + 6), sy + math.sin(ang) * (R + 6)), (x + math.cos(ang) * (R + 34), sy + math.sin(ang) * (R + 34))], fill=(255, 210, 90, 220), width=5)
            layer(img, aura)
        bl = BALL[n]
        if stg: bl = up(bl, 1.12)
        if zz:
            bl = bl.copy(); tint = Image.new('RGBA', bl.size, (120, 80, 200, 0)); tint.putalpha(Image.eval(bl.getchannel('A'), lambda v: v * 90 // 255)); bl.alpha_composite(tint)
        img.alpha_composite(bl, (int(x - bl.width / 2), int(sy - bl.height / 2)))
        if zz:
            u = t % 0.9
            text_layer(img, [(x + 52 + 30 * u, sy - 70 - 60 * u, 'Z', 48, (210, 170, 255), 7, 255), (x + 20 + 30 * ((u + 0.45) % 0.9), sy - 60 - 60 * ((u + 0.45) % 0.9), 'z', 40, (210, 170, 255), 6, 255)])
        if sh:
            def bub(dd, x=x, sy=sy):
                rr = R + 18 + 3 * math.sin(t * 8)
                dd.ellipse([x - rr, sy - rr, x + rr, sy + rr], fill=(110, 230, 110, 55), outline=(150, 255, 150, 235), width=6)
                dd.arc([x - rr + 12, sy - rr + 12, x + rr - 12, sy + rr - 12], 200, 250, fill=(235, 255, 235, 230), width=6)
            layer(img, bub)
        for (bt, who) in blocks.items():
            u = t - bt
            if who == n and 0 <= u < 0.45:
                def pop_(dd, x=x, sy=sy, u=u):
                    rr = R + 18 + 120 * u; al = int(255 * (1 - u / 0.45))
                    dd.ellipse([x - rr, sy - rr, x + rr, sy + rr], outline=(150, 255, 150, al), width=10)
                layer(img, pop_)
    # hfg5: info strip (box, CLEO VS CYRUS intro, X LEADS! line, progress bar) cut
    ld = lead or win; fl = t - state['lead_flash']
    if False and 0.9 <= t < FIN_T[win] and 0 <= fl < 1.1:      # hfg5: lead line cut too (two marbles, both on screen: the lead is visible)
        a_ = int(255 * min(1, (1.1 - fl) / 0.25)); sc = 1 + 0.25 * max(0, 1 - fl / 0.12)
        text_layer(img, [(540, STRIP0 + 14 - int(20 * (sc - 1)), LABEL[ld] + ' LEADS!', int(52 * sc), RING[ld], 8, a_)])
    # GO! flash over the moving start
    if 0.2 <= t < 0.95:
        u = t - 0.2; s = 140 if u > 0.1 else int(80 + 600 * u); a = int(255 * min(1, (0.75 - u) / 0.2))
        text_layer(img, [(478, 1180, 'GO!', s, (90, 230, 110), 12, a)])
    for (t0, t1, kind, who, k) in STAMPS:
        if t0 <= t < t1: img.alpha_composite(stamp_layer(kind, who, k, t - t0, t1 - t0))
    if t >= TEND:
        u = t - TEND; a = 1.0 if u > 0.12 else u / 0.12
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(175 * a))))
        pop = 1.0 if u > 0.12 else 0.75 + 0.25 * u / 0.12
        text_layer(img, [(540, 590, LABEL[win] + ' WINS!', int(80 * pop), (255, 214, 60), 10, 255)])
        img.alpha_composite(PODIUM, (500 - PODIUM.width // 2, 1052))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (500 - vf.width // 2, 1066 - vf.height))
        # hfg5: 'DID YOUR / MARBLE WIN?' cut (caption asks)
    img.alpha_composite(HK)
    return img
cam = None; state = {'lead_flash': -9}; lp = None
wr = Writer(OUT + 'v51_noaudio.mp4'); F0 = None
for f in range(NF):
    t = f / FPS; P, SA, lead, *_ = FR[min(f, len(FR) - 1)]
    ys = [P[n][1] for n in P if P[n][1] <= FIN + 70] or [FIN]
    a_, b_ = max(ys), min(ys); target = (a_ + b_) / 2 - MID
    if a_ - target > BAND_BOT - 20: target = a_ - (BAND_BOT - 20)
    target = min(target, FIN + 90 - BAND_BOT)
    cam = target if cam is None else cam + (target - cam) * 0.12
    ld = lead or win
    if lp is not None and ld != lp and t < FIN_T[win]:
        state['lead_flash'] = t
        if t - last_sfx > 1.0 and not any(abs(t - p[0]) < 0.4 for p in picks): ev_out.append((round(t, 3), 'whoosh_8bit')); last_sfx = t
    lp = ld
    img = render(f, cam, state)
    if f == 0: F0 = img.copy()
    wr.write(img)
    if PREVIEW and f % 15 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'pv_{f:04d}.png')
wr.close()
F0.convert('RGB').save(OUT + 'first.png')
last = -9; lsm = -9
for e in EV:
    if e[0] >= TEND: continue
    if e[1] == 'bump' and e[0] - last > 0.35: ev_out.append((round(e[0], 3), 'boing')); last = e[0]
    if e[1] == 'pick': ev_out.append((round(e[0], 3), 'powerup_8bit'))
    if e[1] == 'smash' and e[0] - lsm > 0.2: ev_out.append((round(e[0], 3), 'crunch_8bit')); ev_out.append((round(e[0], 3), 'punch')); lsm = e[0]
    if e[1] == 'block': ev_out.append((round(e[0] + 0.05, 3), 'poof'))
    if e[1] == 'sleep': ev_out.append((round(e[0] + 0.05, 3), 'twinkle'))
    if e[1] == 'finish' and e[2] == win: ev_out.append((round(e[0], 3), 'ding_8bit'))
ev_out += [(round(TEND, 3), 'victory'), (round(TEND + 0.2, 3), 'cheer')]
json.dump({'events': sorted(ev_out)}, open(OUT + 'ev51.json', 'w')); print('done', round(NF / FPS, 2), len(ev_out))
