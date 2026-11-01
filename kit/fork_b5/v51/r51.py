import sys; sys.path.insert(0, '../../fork1'); sys.path.insert(0, '.')
from common import *
from sim51 import sim, T_START, R
SEED = int(sys.argv[1])
FR, EV, FIN_T, LEADS, SEGS, PEGS, BUMPERS, SPINNERS, BOOSTS, FIN = sim(SEED)
win = min(FIN_T, key=FIN_T.get); lose = [n for n in FIN_T if n != win][0]
T_END = max(FIN_T.values()) + 0.25; DUR = T_END + 3.6; NF = int(DUR * FPS)
print('winner', win, FIN_T, 'leads', len(LEADS), 'dur', round(DUR, 1))
L = 3; WY0 = -500; WH = 7000
course = Image.new('RGBA', (W // L, WH // L), (0, 0, 0, 0)); d = ImageDraw.Draw(course)
def Y(y): return (y - WY0) / L
for (a, b, r, kind) in SEGS:
    p = [(a[0] / L, Y(a[1])), (b[0] / L, Y(b[1]))]
    if kind == 'wall':
        x = a[0] / L; d.rectangle([x - 6, 0, x + 6, WH // L], fill=(70, 66, 80, 255))
        for yy in range(0, WH // L, 8): d.line([(x - 6, yy), (x + 6, yy)], fill=(45, 42, 55, 255)); d.line([(x - 6 + (yy // 8 % 2) * 6, yy), (x - 6 + (yy // 8 % 2) * 6, yy + 8)], fill=(45, 42, 55, 255))
        d.line([(x + (5 if x < 100 else -5), 0), (x + (5 if x < 100 else -5), WH // L)], fill=(110, 105, 120, 255))
    else:
        d.line(p, fill=(52, 30, 12, 255), width=9); d.line(p, fill=(150, 96, 48, 255), width=6)
        d.line([(p[0][0], p[0][1] - 2), (p[1][0], p[1][1] - 2)], fill=(196, 140, 84, 255), width=1)
        n = int(math.hypot(p[1][0] - p[0][0], p[1][1] - p[0][1]) // 30)
        for k in range(1, n):
            u = k / n; x, y = p[0][0] + (p[1][0] - p[0][0]) * u, p[0][1] + (p[1][1] - p[0][1]) * u
            d.point((x, y), fill=(60, 36, 16, 255))
for (x, y, r, kind) in PEGS:
    X, Yy, rr = x / L, Y(y), r / L
    if kind == 'ball':
        d.ellipse([X - rr - 1, Yy - rr - 1, X + rr + 1, Yy + rr + 1], fill=(60, 52, 48, 255)); d.ellipse([X - rr, Yy - rr, X + rr, Yy + rr], fill=(206, 196, 176, 255))
        d.ellipse([X - rr * 0.6, Yy - rr * 0.7, X - rr * 0.1, Yy - rr * 0.25], fill=(240, 234, 220, 255))
    else:
        d.ellipse([X - rr - 1, Yy - rr - 1, X + rr + 1, Yy + rr + 1], fill=(90, 58, 12, 255)); d.ellipse([X - rr, Yy - rr, X + rr, Yy + rr], fill=(232, 180, 60, 255))
        d.point((X - 1, Yy - 2), fill=(255, 240, 180, 255)); d.point((X - 2, Yy - 1), fill=(255, 240, 180, 255))
# finish checkers
fy = Y(FIN)
for i in range(0, W // L, 6):
    for j in range(2):
        d.rectangle([i, fy + j * 6, i + 5, fy + j * 6 + 5], fill=(240, 240, 240, 255) if (i // 6 + j) % 2 else (20, 20, 24, 255))
COURSE = up(course, L)
BG = bg_frames('vit_hd.gif', (W, H), box=(560, 0, 1167, 1080), step=2, bright=0.38)
GUM = {k: gummy(k, 3) for k in ['mush', 'cre', 'acv', 'mel', 'gold']}
def face(name, rad):
    SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
    RING = {'cleo': (90, 150, 255), 'cyrus': (255, 160, 40)}
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); dd = ImageDraw.Draw(b)
    dd.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); dd.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    dd.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    dd.ellipse([12, 9, 22, 16], fill=(255, 255, 255, 170))
    return b
RING = {'cleo': (90, 150, 255), 'cyrus': (255, 160, 40)}
BALL = {n: face(n, R) for n in ['cleo', 'cyrus']}; ICON = {n: face(n, 50) for n in ['cleo', 'cyrus']}; ICS = {n: face(n, 26) for n in ['cleo', 'cyrus']}
LABEL = {'cleo': 'CLEO', 'cyrus': 'CYRUS'}
VICF = vic(win, 340)
def spinner_img(angle):
    S = 120; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); c = S / 2
    for a in range(4):
        ang = angle + a * math.pi / 2; ex = (c + math.cos(ang) * 55, c + math.sin(ang) * 55)
        dd.line([(c, c), ex], fill=(52, 30, 12, 255), width=9); dd.line([(c, c), ex], fill=(170, 110, 52, 255), width=6)
    dd.ellipse([c - 7, c - 7, c + 7, c + 7], fill=(40, 40, 50, 255)); dd.ellipse([c - 5, c - 5, c + 5, c + 5], fill=(130, 130, 145, 255))
    return up(im, L)
SPOS = [(310, 3850 + k * 260) for k in range(4)]; SPOS = [(x if k % 2 == 0 else 770, y) for k, (x, y) in enumerate(SPOS)]
cam = -400.0; trails = {n: [] for n in BALL}; out = []; ev_out = []
boost_t = {}; lead_prev = None; lead_flash = -9
for e in EV:
    if e[1] == 'boost': boost_t.setdefault(e[2], []).append(e[0])
wr = Writer('v51_noaudio.mp4')
HDR = 380
for f in range(NF):
    t = f / FPS; P, SA, lead, used = FR[min(f, len(FR) - 1)]
    ys = {n: P[n][1] for n in P}
    if t < T_START: target = -480
    else:
        a, b = max(ys.values()), min(ys.values())
        target = (a + b) / 2 - 900 if a - b < 1100 else a - 1300
    target = min(max(target, -480), FIN + 380 - H)
    cam += (target - cam) * 0.12
    img = BG[int(t * 6) % len(BG)].copy()
    top = int(cam - WY0)
    img.alpha_composite(COURSE.crop((0, top, W, top + H)))
    # spinners
    for (x, y), ang in zip(SPOS, SA):
        sp = spinner_img(ang); img.alpha_composite(sp, (int(x - sp.width / 2), int(y - cam - sp.height / 2)))
    # bumpers & boosts
    for (x, y, k) in BUMPERS:
        g = GUM[k]; wob = 1 + 0.06 * math.sin(t * 5 + x)
        img.alpha_composite(g, (int(x - g.width / 2), int(y - cam - g.height / 2)))
    for i, (x, y, k) in enumerate(BOOSTS):
        if any(u[1] == i for u in used): continue
        g = GUM['gold']; bob = 6 * math.sin(t * 4 + i)
        layer(img, lambda dd, x=x, y=y: dd.ellipse([x - 52, y - cam - 52 + bob, x + 52, y - cam + 52 + bob], fill=(255, 214, 60, 70)))
        img.alpha_composite(g, (int(x - g.width / 2), int(y - cam - g.height / 2 + bob)))
    # gate
    if t < T_START:
        layer(img, lambda dd: dd.line([(440, 345 - cam), (640, 345 - cam)], fill=(150, 150, 165, 255), width=16))
    # marbles + trails
    for n in P:
        x, y, a = P[n]; trails[n] = (trails[n] + [(x, y)])[-10:]
        boosted = any(0 <= t - bt < 1.2 for bt in boost_t.get(n, []))
        def tr(dd, n=n, boosted=boosted):
            for i, (tx, ty) in enumerate(trails[n][:-1]):
                rr = 6 + i * 2; al = int(30 + 150 * i / len(trails[n]))
                col = (255, 214, 60) if boosted else RING[n]
                dd.ellipse([tx - rr, ty - cam - rr, tx + rr, ty - cam + rr], fill=col + (al,))
        layer(img, tr)
        bl = BALL[n]; img.alpha_composite(bl, (int(x - bl.width / 2), int(y - cam - bl.height / 2)))
        for bt in boost_t.get(n, []):
            u = t - bt
            if 0 <= u < 1.2: text_layer(img, [(x, y - cam - 90 - u * 40, 'SPEED UP!', 30, (255, 214, 60), 5, int(255 * min(1, (1.2 - u) / 0.3)))])
    # header
    layer(img, lambda dd: dd.rounded_rectangle([30, 40, W - 30, HDR - 20], 24, fill=(14, 10, 24, 225), outline=(255, 214, 60, 255), width=5))
    if t < T_START:
        for n, x in (('cleo', W / 2 - 170), ('cyrus', W / 2 + 170)):
            ic = ICON[n]; img.alpha_composite(ic, (int(x - ic.width / 2), 70))
        text_layer(img, [(W / 2, 112, 'VS', 44, (255, 90, 90), 6, 255), (W / 2 - 170, 196, 'CLEO', 28, (255, 255, 255), 5, 255), (W / 2 + 170, 196, 'CYRUS', 28, (255, 255, 255), 5, 255), (W / 2, 262, 'PICK YOUR MARBLE', 36, (255, 214, 60), 6, 255)])
    else:
        ld = lead or win
        if ld != lead_prev and lead_prev is not None: lead_flash = t; ev_out.append((round(t, 3), 'whoosh_8bit'))
        lead_prev = ld
        ic = ICON[ld]; pop = 1 + 0.15 * max(0, 1 - (t - lead_flash) / 0.3)
        icz = ic.resize((int(ic.width * pop), int(ic.height * pop)), Image.NEAREST); img.alpha_composite(icz, (int(W / 2 - icz.width / 2), int(118 - icz.height / 2)))
        msg = LABEL[ld] + ' IS IN THE LEAD' if not FIN_T or t < min(FIN_T.values()) else LABEL[win] + ' FINISHED!'
        text_layer(img, [(W / 2, 186, msg, 32, (255, 255, 255), 5, 255)])
        # progress bar
        layer(img, lambda dd: dd.rounded_rectangle([100, 262, W - 100, 282], 10, fill=(50, 44, 66, 255)))
        for n in P:
            u = max(0, min(1, (P[n][1] - 250) / (FIN - 250))); x = 100 + (W - 200) * u; ic = ICS[n]
            img.alpha_composite(ic, (int(x - ic.width / 2), 272 - ic.height // 2 + (-16 if n == 'cleo' else 16)))
    # countdown
    if 0.4 < t < T_START + 0.6:
        k = int(T_START - t) + 1
        if t >= T_START: txt, col = 'GO!', (90, 230, 110)
        else: txt, col = str(k), (255, 255, 255)
        text_layer(img, [(W / 2, 560 if t < T_START else 600, txt, 110, col, 10, 255)])
    if f == int(T_START * FPS): ev_out.append((T_START, 'go_8bit'))
    for kk in (1, 2, 3):
        if f == int((T_START - kk) * FPS): ev_out.append((round(T_START - kk, 3), 'tick_8bit'))
    # end card
    if t >= T_END:
        u = t - T_END; a = min(1, u / 0.3)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(160 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        text_layer(img, [(W / 2, 1230, LABEL[win] + ' WINS!', 70, (255, 214, 60), 9, int(255 * a)), (W / 2, 1340, 'Did your marble win?', 38, (255, 255, 255), 6, int(255 * a))])
        if not any(e[1] == 'victory' for e in ev_out): ev_out += [(round(T_END, 3), 'victory'), (round(T_END + 0.2, 3), 'cheer')]
    wr.write(img)
    if f % 60 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close()
last = {}
for e in EV:
    if e[1] == 'bump' and e[0] - last.get('b', -9) > 0.25: ev_out.append((round(e[0], 3), 'boing')); last['b'] = e[0]
    if e[1] == 'boost': ev_out.append((round(e[0], 3), 'powerup_8bit'))
    if e[1] == 'finish': ev_out.append((round(e[0], 3), 'ding_8bit'))
json.dump(sorted(ev_out), open('ev51.json', 'w')); print('done', round(DUR, 2))
