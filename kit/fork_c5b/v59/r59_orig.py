import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
from PIL import Image, ImageDraw, ImageEnhance
os.chdir(SP + 'fork_a6'); OUT = SP + 'fork_sz56/v59/'
HOOK, HB = hook_layer(['PICK A GUIDE'], accent=0, sub='BEFORE THE WATER RISES', sub_color=(120, 220, 255))
P0, P1 = HB + 12, HB + 140
def X(x): return 110 + (x - 60) * 0.75
CX = X(540)
NAMES = ['joy', 'cleo', 'cyrus', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
ROWH = 250; NROW = 20; Y_BOT = 760 + NROW * ROWH; WH = Y_BOT + 400
T_GO = 2.4
# platform layout: (row, x0, x1); row 0 = floor
rl = random.Random(3)
PLAT = [(0, X(60), X(1020))]
for r in range(1, NROW):
    if r % 2:
        a = rl.uniform(70, 160); w1 = rl.uniform(300, 380); PLAT.append((r, X(a), X(a + w1))); b = rl.uniform(600, 690); w2 = rl.uniform(300, 380); PLAT.append((r, X(b), X(min(1010, b + w2))))
    else:
        a = rl.uniform(330, 400); w1 = rl.uniform(330, 380); PLAT.append((r, X(a), X(a + w1)))
PLAT.append((NROW, X(380), X(700)))
def py(r): return Y_BOT - r * ROWH
SLIMEPAD = {}      # row -> platform index (filled below)
for i, (r, x0, x1) in enumerate(PLAT):
    if r in (4, 10, 15) and SLIMEPAD.get(r) is None: SLIMEPAD[r] = i
SLIMEPAD = {r: i for r, i in SLIMEPAD.items() if i is not None}
GUMS = []   # (platform index, x, kind)
for i, (r, x0, x1) in enumerate(PLAT):
    if r in (3, 7, 12, 17) and (r % 2 == 0 or x0 > X(500)): GUMS.append((i, (x0 + x1) / 2, ['mush', 'acv', 'cre', 'mel', 'mush'][r % 5]))
def water(t):
    if t < T_GO + 1.0: return Y_BOT + 120
    u = t - T_GO - 1.0
    return Y_BOT + 120 - (WA * u + WB * u * u)
WA, WB = float(os.environ.get('WA', '150')), float(os.environ.get('WB', '4'))
def sim(seed, dur=40):
    rnd = random.Random(seed)
    R = {}
    xs = [X(200), X(420), X(640), X(860)]; rnd.shuffle(xs)
    for n, x in zip(NAMES, xs):
        R[n] = dict(p=0, x=x, y=py(0), mode='run', tgt=None, j0=None, sp=rnd.uniform(165, 300), jt=rnd.uniform(0.5, 0.8), ph=rnd.uniform(0, 6),
                    boost=-9, caught=None, done=None, vx=1, hes=0.0, pend=None)
    taken = set(); frames = []; events = []; leaders = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS; wl = water(t)
        for n, s in R.items():
            if s['caught'] is not None:
                s['y'] = wl + 30; continue
            if s['done'] is not None or t < T_GO: continue
            if s['mode'] == 'run':
                r = PLAT[s['p']][0]
                if r >= NROW:
                    s['done'] = t; events.append((t, 'win', n)); continue
                if s['tgt'] is None:
                    # choose next platform in the row above (or two above off a slime pad)
                    cand = [i for i, P in enumerate(PLAT) if P[0] == r + 1]
                    cur = PLAT[s['p']]
                    def cost(i):
                        P = PLAT[i]; cx = min(max(s['x'], P[1] + 40), P[2] - 40)
                        return abs(cx - s['x']) + rnd.uniform(0, 260)
                    nxt = min(cand, key=cost); P = PLAT[nxt]
                    lx = min(max(s['x'], P[1] + 50), P[2] - 50)
                    takeoff = min(max(lx, cur[1] + 30), cur[2] - 30)
                    s['tgt'] = (nxt, takeoff, lx); s['hes'] = rnd.uniform(0.1, 0.6) if rnd.random() < 0.45 else 0
                nxt, takeoff, lx = s['tgt']
                sp = s['sp'] * (1 + 0.15 * math.sin(t * 1.3 + s['ph'])) * (1.6 if t - s['boost'] < 3 else 1)
                if abs(takeoff - s['x']) > 6:
                    d = 1 if takeoff > s['x'] else -1; s['vx'] = d; s['x'] += d * min(sp * dt, abs(takeoff - s['x']))
                    # gummy pickups on this platform
                    for g in GUMS:
                        if g[0] == s['p'] and g not in taken and abs(g[1] - s['x']) < 40:
                            taken.add(g); s['boost'] = t; events.append((t, 'gum', n))
                else:
                    if s['hes'] > 0: s['hes'] -= dt; continue
                    s['mode'] = 'jump'; s['j0'] = (t, s['x'], s['y'], lx, py(PLAT[nxt][0]), nxt); events.append((t, 'jump', n))
                    s['vx'] = 1 if lx >= s['x'] else -1
            elif s['mode'] == 'jump':
                t0, x0, y0, x1, y1, nxt = s['j0']; D = s['jt'] * (0.8 if t - s['boost'] < 3 else 1)
                u = min(1, (t - t0) / D)
                s['x'] = x0 + (x1 - x0) * u; s['y'] = y0 + (y1 - y0) * u - 170 * 4 * u * (1 - u)
                if u >= 1:
                    s['p'] = nxt; s['y'] = y1; s['tgt'] = None; s['mode'] = 'run'
                    if PLAT[nxt][0] in SLIMEPAD and SLIMEPAD[PLAT[nxt][0]] == nxt:
                        # friendly slime pad: launch two rows up
                        r2 = PLAT[nxt][0] + 2; cand = [i for i, P in enumerate(PLAT) if P[0] == r2]
                        tgt = min(cand, key=lambda i: abs((PLAT[i][1] + PLAT[i][2]) / 2 - s['x']))
                        P = PLAT[tgt]; lx2 = min(max(s['x'], P[1] + 50), P[2] - 50)
                        s['mode'] = 'jump'; s['j0'] = (t, s['x'], s['y'], lx2, py(P[0]), tgt); s['jt'] = s['jt']; events.append((t, 'boing', n))
            if s['y'] > wl - 10 and s['done'] is None:
                s['caught'] = t; events.append((t, 'caught', n))
        live = [n for n in NAMES if R[n]['caught'] is None]
        if live:
            ld = min(live, key=lambda n: (R[n]['done'] if R[n]['done'] is not None else 1e5 + R[n]['y']))
            if not leaders or leaders[-1] != ld: leaders.append(ld)
        frames.append(({n: dict(x=s['x'], y=s['y'], mode=s['mode'], vx=s['vx'], caught=s['caught'], done=s['done'], boost=s['boost'], j0=s['j0']) for n, s in R.items()}, wl, set(taken)))
        if all(R[n]['caught'] is not None or R[n]['done'] is not None for n in NAMES) and any(R[n]['done'] for n in NAMES): break
    return frames, events, leaders, {n: (R[n]['done'], R[n]['caught']) for n in NAMES}
def score(seed):
    fr, ev, ld, res = sim(seed)
    wins = [n for n in NAMES if res[n][0] is not None]
    if len(wins) != 1: return None
    w = wins[0]
    if w != 'cleo': return None
    tw = res[w][0]; caught = sorted(res[n][1] for n in NAMES if res[n][1] is not None)
    if len(caught) != 3 or not (17 < tw < 25): return None
    if caught[0] < 9 or tw - caught[-1] > 3.0 or len(ld) < 4: return None
    return round(tw, 2), w, [round(c, 1) for c in caught], len(ld), sum(1 for e in ev if e[1] == 'gum'), sum(1 for e in ev if e[1] == 'boing')
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EVS, LEAD, RES = sim(SEED)
WIN = [n for n in NAMES if RES[n][0] is not None][0]; T_WIN = RES[WIN][0]
print('win', WIN, round(T_WIN, 2), {n: RES[n] for n in NAMES}, 'leaders', LEAD)
# ---------------- art
bg = Image.open('templebg/00.png').convert('RGBA'); k = W / bg.width
bgt = ImageEnhance.Brightness(bg.resize((W, int(bg.height * k)), Image.NEAREST)).enhance(0.62)
WORLD = Image.new('RGBA', (W, WH), (0, 0, 0, 255))
y = WH - bgt.height; flip = False
while y > -bgt.height:
    WORLD.alpha_composite(bgt.transpose(Image.FLIP_TOP_BOTTOM) if flip else bgt, (0, y)); y -= bgt.height; flip = not flip
LEDGE = crop(Image.open('ledge/03.png').convert('RGBA'))
for i, (r, x0, x1) in enumerate(PLAT):
    w_ = int(x1 - x0); lg = LEDGE.resize((w_, int(LEDGE.height * 3)), Image.NEAREST)
    WORLD.alpha_composite(lg, (int(x0), int(py(r) - 14)))
wd = ImageDraw.Draw(WORLD)
ex = (X(380) + X(700)) / 2; ey = py(NROW)
for k_ in range(6): wd.ellipse([ex - 170 + k_ * 12, ey - 330 + k_ * 10, ex + 170 - k_ * 12, ey - 10 - k_ * 4], fill=(255, 240, 190, 40 + k_ * 25))
wd.rounded_rectangle([ex - 90, ey - 200, ex + 90, ey - 10], 60, fill=(255, 248, 215, 255), outline=(120, 100, 70, 255), width=8)
SLIME = seq(PL + 'race/slime_idle_c', 3); SPLAT = seq(PL + 'race/slime_splat_c', 3)
SK = 3
SR = {g: seq(PL + f'race/{g}_run', SK) for g in NAMES}
SWIM = {g: seq(SP + f'fork4/{g}_swim' + ('3' if g == 'cleo' else ''), SK)[3:8] for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', SK, 0, 1)[0] for g in NAMES}
GUM = {k: gummy(k, 3) for k in GUMK}
VICF = vic(WIN, 380)
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
    return b
ICON = {n: face(n, 34) for n in NAMES}
EV = []
def ev(t, name): EV.append((round(t, 3), name))
for tt in (0.6, 1.2, 1.8): ev(tt, 'tick_8bit')
ev(T_GO, 'go_8bit')
lastj = -1
for (t, kd, n) in EVS:
    if kd == 'jump' and t - lastj > 0.25: ev(t, 'jump'); lastj = t
    elif kd == 'boing': ev(t, 'boing')
    elif kd == 'gum': ev(t, 'powerup_8bit')
    elif kd == 'caught': ev(t, 'poof')
    elif kd == 'win': ev(t, 'victory')
T_END = T_WIN + 4.2; NF = int(T_END * FPS)
HDR = 330
cam = 0
wr = Writer(OUT + 'v59_noaudio.mp4')
FX = [(t, kd, n) for (t, kd, n) in EVS if kd in ('boing', 'gum', 'caught')]
for f in range(NF):
    t = f / FPS; st, wl, taken = FR[min(f, len(FR) - 1)]
    live = [n for n in NAMES if st[n]['caught'] is None]
    focus = min(st[n]['y'] for n in live) if live else st[WIN]['y']
    if t < T_GO: focus = py(0)
    low = max(st[n]['y'] for n in live) if live else focus
    recent = any(0 <= t - te < 1.3 for (te, kd, n) in FX if kd == 'caught')
    danger = (wl - low < 330) or recent
    hi_c = focus - 880                          # leader feet at >= 880
    lo_c = (max(wl - 30, low) if danger else low) - 1450   # lowest guide / water line at <= 1450
    tgt = lo_c if lo_c > hi_c and danger else min(hi_c, max(lo_c, focus - 1300))
    if t < T_GO: tgt = py(0) - 1300
    tgt = max(0, min(WH - H, tgt))
    cam = tgt if f == 0 else cam + (tgt - cam) * 0.1
    c0 = int(cam)
    img = WORLD.crop((0, c0, W, c0 + H)).copy()
    # slime pads
    for r, i in SLIMEPAD.items():
        rr, x0, x1 = PLAT[i]; sx = (x0 + x1) / 2; sy = py(rr) - c0
        hit = any(0 <= t - te < 0.3 and kd == 'boing' and abs(st[n]['x'] - sx) < 400 for (te, kd, n) in FX)
        fr = SPLAT[3] if hit else SLIME[int(t * 10) % len(SLIME)]
        img.alpha_composite(fr, (int(sx - fr.width / 2), int(sy - fr.height + 30)))
        if not hit: text_layer(img, [(sx, sy - 120, 'BOING PAD', 18, (150, 255, 150), 4, 220)])
    # gummies
    for g in GUMS:
        if g in taken: continue
        i, gx, kd = g; gy = py(PLAT[i][0]) - c0 - 60 + 8 * math.sin(t * 3 + gx)
        layer(img, lambda dd: [dd.ellipse([gx - 44 + k_ * 9, gy - 40 + k_ * 9, gx + 44 - k_ * 9, gy + 40 - k_ * 9], fill=(255, 230, 140, 40 + k_ * 30)) for k_ in range(3)])
        gm = GUM[kd]; img.alpha_composite(gm, (int(gx - gm.width / 2), int(gy - gm.height / 2)))
    # guides
    for n in NAMES:
        s = st[n]; x, yy = s['x'], s['y'] - c0
        if s['caught'] is not None:
            fr = SWIM[n][int(t * 8) % len(SWIM[n])]
            if int(t * 1.5 + NAMES.index(n)) % 2: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(fr, (int(x - fr.width / 2), int(yy - 78 * SK + 70 + 4 * math.sin(t * 4))))
            continue
        if t < T_GO or (s['done'] is not None and t > s['done']): fr = STAND[n]
        elif s['mode'] == 'jump': fr = SR[n][3]
        else: fr = SR[n][int(t * 14) % 8]
        if s['vx'] < 0 and fr is not STAND[n]: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        if t - s['boost'] < 3 and s['caught'] is None:
            layer(img, lambda dd: [dd.rectangle([x - 40 - k_ * 14, yy - 70 - (k_ * 23 % 50), x - 32 - k_ * 14, yy - 64 - (k_ * 23 % 50)], fill=(255, 220, 90, 220 - k_ * 40)) for k_ in range(5)])
        img.alpha_composite(fr, (int(x - fr.width / 2), int(yy - 78 * SK + 6)))
    # water
    wy = wl - c0
    if wy < H:
        L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        pts = [(x, wy + 10 * math.sin(x / 70 + t * 3)) for x in range(0, W + 20, 20)]
        dl.polygon(pts + [(W, H), (0, H)], fill=(40, 140, 200, 150))
        for x, yv in pts: dl.rectangle([x - 10, yv - 4, x + 10, yv + 4], fill=(200, 240, 255, 220))
        for k_ in range(26):
            bx = (k_ * 97 + t * 30) % W; by = wy + 40 + ((k_ * 131 - t * 120) % max(1, H - wy))
            if by < H: dl.rectangle([bx - 4, by - 4, bx + 4, by + 4], fill=(210, 245, 255, 140))
        img.alpha_composite(L)
    # popups
    items = []
    for (te, kd, n) in FX:
        u = t - te
        if 0 <= u < 1.1:
            s = st[n]; x, yy = s['x'], s['y'] - c0
            txt, col = {'boing': ('BOING!', (150, 255, 150)), 'gum': ('SPEED UP!', (255, 214, 60)), 'caught': ('SPLASH! OUT', (140, 210, 255))}[kd]
            items.append((max(220, min(660, x)), max(P1 + 40, yy - 260 - u * 50), txt, 32, col, 6, int(255 * min(1, (1.1 - u) / 0.35))))
    if items: text_layer(img, items)
    # status panel under the hook
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(10, 24, 30, 220)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(120, 220, 255, 255), width=4)
    for i, n in enumerate(NAMES):
        x = 70 + 955 * (i + 0.5) / 4; ic = ICON[n]
        if st[n]['caught'] is not None: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55)
        img.alpha_composite(ic, (int(x - ic.width / 2), P0 + 8))
        if st[n]['caught'] is not None: text_layer(img, [(x, P0 + 90, 'OUT', 24, (255, 110, 110), 4, 255)])
        elif st[n]['done'] is not None: text_layer(img, [(x, P0 + 90, 'SAFE!', 24, (255, 214, 60), 4, 255)])
    if t < T_GO:
        if t >= 0.6: text_layer(img, [(CX, 1000, str(max(1, 3 - int((t - 0.6) / 0.6))), 150, (255, 214, 60), 12, 255)])
    elif t < T_GO + 0.6:
        text_layer(img, [(W / 2, 1000, 'CLIMB!', 120, (120, 220, 255), 12, int(255 * (1 - (t - T_GO) / 0.6)))])
    if t >= T_WIN + 0.5:
        u = t - T_WIN - 0.5; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], fill=(8, 14, 22, int(170 * a))))
        if a > 0.2:
            vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1040 - vf.height))
            text_layer(img, [(W / 2, 1075, LABEL[WIN] + ' WINS!', 64, (255, 214, 60), 8, int(255 * a)),
                             (W / 2, 1175, 'DID YOUR GUIDE WIN?', 30, (255, 255, 255), 6, int(255 * a))])
            rr = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                x_, y_ = rr.uniform(80, 1000), (rr.uniform(0, H) + u * 400) % (1480 - P1) + P1
                dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p59_{f:04d}.png')
wr.close()
json.dump({'events': EV}, open(OUT + 'v59_ev.json', 'w'))
print('done', round(T_END, 2), len(EV))
