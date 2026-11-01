import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RINGC = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
CX, CY, RR = 540, 1180, 430
def sim(seed, dur=30):
    rnd = random.Random(seed)
    ag = {}
    for k, n in enumerate(NAMES):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        ag[n] = dict(x=CX + 220 * math.cos(a), y=CY + 220 * math.sin(a), vx=0.0, vy=0.0, out=None, dash=-9, cd=rnd.uniform(0.3, 1.2), tgt=None,
                     spd=rnd.uniform(220, 260), pow=1.0, mass=1.0, buff=None, bt=-9, stun=-9, dist=0.0, ph=rnd.uniform(0, 6.3), dx=0, dy=0)
    gums = []; gsched = [(4.5, None), (8.5, None), (12.5, None), (16.5, None)]
    frames = []; events = []; T0 = 2.2; outs = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        alive = [n for n in NAMES if ag[n]['out'] is None]
        for gt, _ in gsched:
            if abs(t - gt) < dt / 2 and len(alive) > 1:
                a = rnd.uniform(0, 6.28); r = rnd.uniform(0, 160)
                gums.append(dict(x=CX + r * math.cos(a), y=CY + r * math.sin(a), k=rnd.choice(['mush', 'cre']), t=t))
        if t >= T0 and len(alive) > 1:
            for n in alive:
                s = ag[n]
                if s['buff'] and t - s['bt'] > 4.0: s['buff'] = None; s['pow'] = 1.0; s['mass'] = 1.0
                # pick target: nearest gummy if close, else a rival (prefer one near the edge)
                if gums and min(math.hypot(g['x'] - s['x'], g['y'] - s['y']) for g in gums) < 260:
                    g = min(gums, key=lambda g: math.hypot(g['x'] - s['x'], g['y'] - s['y'])); tx, ty = g['x'], g['y']; tg = None
                else:
                    if s['tgt'] not in alive or s['tgt'] == n or rnd.random() < 0.01:
                        opts = [m for m in alive if m != n]
                        s['tgt'] = min(opts, key=lambda m: math.hypot(ag[m]['x'] - s['x'], ag[m]['y'] - s['y']) - 0.6 * math.hypot(ag[m]['x'] - CX, ag[m]['y'] - CY) + rnd.uniform(0, 140))
                    o = ag[s['tgt']]; tg = s['tgt']
                    # approach from the inside so the shove points outward
                    ox, oy = o['x'] - CX, o['y'] - CY; L = math.hypot(ox, oy) or 1
                    tx, ty = o['x'] - ox / L * 50, o['y'] - oy / L * 50
                dashing = t - s['dash'] < 0.32; stunned = t - s['stun'] < 0.45
                if not dashing and not stunned:
                    dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                    sp = s['spd'] * (1 + 0.15 * math.sin(2.1 * t + s['ph']))
                    # keep away from the edge
                    ex, ey = s['x'] - CX, s['y'] - CY; er = math.hypot(ex, ey) or 1
                    inx = iny = 0
                    if er > RR - 90: inx, iny = -ex / er * 1.4, -ey / er * 1.4
                    ux, uy = dx / L + inx, dy / L + iny; U = math.hypot(ux, uy) or 1
                    s['vx'] += (ux / U * sp - s['vx']) * 0.15; s['vy'] += (uy / U * sp - s['vy']) * 0.15
                    if tg and t > s['cd'] + T0 and math.hypot(ag[tg]['x'] - s['x'], ag[tg]['y'] - s['y']) < 150:
                        o = ag[tg]; dx, dy = o['x'] - s['x'], o['y'] - s['y']; L = math.hypot(dx, dy) or 1
                        s['dash'] = t; s['dx'], s['dy'] = dx / L, dy / L; s['vx'], s['vy'] = dx / L * 760, dy / L * 760
                        s['cd'] = t - T0 + rnd.uniform(0.9, 1.7)
                if stunned: s['vx'] *= 0.9; s['vy'] *= 0.9
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
            # collisions
            for i, a in enumerate(alive):
                for b in alive[i + 1:]:
                    A_, B_ = ag[a], ag[b]; dx, dy = B_['x'] - A_['x'], B_['y'] - A_['y']; d = math.hypot(dx, dy)
                    if 0 < d < 56:
                        ux, uy = dx / d, dy / d
                        ad = t - A_['dash'] < 0.32; bd = t - B_['dash'] < 0.32
                        if ad or bd:
                            sh, vi = (A_, B_) if (ad and not bd) or (ad and bd and rnd.random() < 0.5) else (B_, A_)
                            sgn = 1 if sh is A_ else -1
                            imp = 760 * sh['pow'] / vi['mass'] * rnd.uniform(0.85, 1.15)
                            vi['vx'] = ux * sgn * imp; vi['vy'] = uy * sgn * imp; vi['stun'] = t
                            sh['vx'] *= 0.15; sh['vy'] *= 0.15; sh['dash'] = -9
                            events.append((t, 'shove', a if sh is A_ else b, b if sh is A_ else a))
                        push = (56 - d) / 2; A_['x'] -= ux * push; A_['y'] -= uy * push; B_['x'] += ux * push; B_['y'] += uy * push
            for n in alive:
                s = ag[n]
                for g in list(gums):
                    if math.hypot(g['x'] - s['x'], g['y'] - s['y']) < 46:
                        gums.remove(g); s['buff'] = g['k']; s['bt'] = t
                        if g['k'] == 'mush': s['pow'] = 1.6
                        else: s['mass'] = 1.9
                        events.append((t, 'gum', n, g['k']))
                if math.hypot(s['x'] - CX, s['y'] - CY) > RR + 16:
                    s['out'] = t; outs.append((n, t)); events.append((t, 'splash', n, None))
        for n in NAMES:
            s = ag[n]
            if s['out'] is not None:
                ex, ey = s['x'] - CX, s['y'] - CY; er = math.hypot(ex, ey) or 1
                if er < RR + 110: s['x'] += ex / er * 70 * dt; s['y'] += ey / er * 70 * dt
        frames.append(({n: dict(x=ag[n]['x'], y=ag[n]['y'], vx=ag[n]['vx'], vy=ag[n]['vy'], out=ag[n]['out'], dash=ag[n]['dash'], stun=ag[n]['stun'], buff=ag[n]['buff'], dist=ag[n]['dist']) for n in NAMES}, [dict(g) for g in gums]))
        alive = [n for n in NAMES if ag[n]['out'] is None]
        if len(alive) == 1 and t > outs[-1][1] + 3.4: break
    win = [n for n in NAMES if ag[n]['out'] is None]
    return frames, events, outs, (win[0] if len(win) == 1 else None)
def score(seed):
    fr, ev, outs, win = sim(seed)
    if not win or win not in ('joy', 'ray'): return None
    if len(outs) != 4 or not (13 <= outs[-1][1] <= 20): return None
    ts = [o[1] for o in outs]
    if min(b - a for a, b in zip([2.2] + ts, ts)) < 1.4: return None
    sh = sum(1 for e in ev if e[1] == 'shove')
    if sh < 8 or outs[0][0] not in ('hollow',) and outs[0][0] == win: return None
    return win, [(o[0], round(o[1], 1)) for o in outs], sh
if __name__ == '__main__' and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, OUTS, WIN = sim(SEED)
print('winner', WIN, OUTS)
SS = 2; FOOT = 78 * SS
SRUN = {g: seq(PL + f'race/{g}_run', 2, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq(PL + 'maze/anim/hollow_srun', 2, 1, 9)
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', 2, 1, 9) for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', 2, 0, 1)[0] for g in NAMES}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', 2, 1, 9) for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RINGC[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 30) for n in NAMES}; HEAD = {n: face(n, 34) for n in NAMES}
# ground: deck disc inside lake from the Wang tileset
T = wang('../gen/deck_meta.json', '../gen/deck_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
TS = 64; AY0 = 470; GC, GR = 17, 23
def lowc(i, j):
    x, y = i * TS - 4, AY0 + j * TS
    return (x - CX) ** 2 + (y - CY) ** 2 < (RR + 26) ** 2
CORN = [[lowc(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (40, 110, 180, 255)); DECK = Image.new('RGBA', (W, H))
WT = ImageEnhance.Brightness(T[(False, False, False, False)]).enhance(0.82); DT = T[(True, True, True, True)]
for j in range(GR):
    for i in range(GC):
        fl = (i + j) % 2
        GROUND.alpha_composite(WT.transpose(Image.FLIP_LEFT_RIGHT) if fl else WT, (i * TS - 4, AY0 + j * TS))
        DECK.alpha_composite(DT.transpose(Image.FLIP_LEFT_RIGHT) if fl else DT, (i * TS - 4, AY0 + j * TS))
DR = RR + 26
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse([CX - DR, CY - DR, CX + DR, CY + DR], fill=255)
layer(GROUND, lambda d: d.ellipse([CX - DR - 10, CY - DR + 6, CX + DR + 10, CY + DR + 26], fill=(10, 40, 70, 150)))
GROUND.paste(DECK, (0, 0), mask)
layer(GROUND, lambda d: (d.ellipse([CX - DR, CY - DR, CX + DR, CY + DR], outline=(70, 40, 20, 255), width=10), d.ellipse([CX - DR + 8, CY - DR + 8, CX + DR - 8, CY + DR - 8], outline=(150, 100, 55, 255), width=4)))
LILY = [up(crop(Image.open(p).convert('RGBA')), 2) for p in sorted(glob.glob(SP + 'fork4/lilypad/*.png'))[:3]]
rr = random.Random(4)
for k in range(9):
    while True:
        x, y = rr.uniform(40, W - 40), rr.uniform(AY0 + 40, H - 160)
        if math.hypot(x - CX, y - CY) > RR + 110: break
    lp = LILY[k % len(LILY)]; GROUND.alpha_composite(lp, (int(x - lp.width / 2), int(y - lp.height / 2)))
gd = ImageDraw.Draw(GROUND)
# rope ring + center mark painted on the deck
def deco(d):
    d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], outline=(240, 220, 170, 255), width=8)
    d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], outline=(120, 80, 40, 255), width=3)
    d.ellipse([CX - 70, CY - 70, CX + 70, CY + 70], outline=(240, 220, 170, 160), width=5)
layer(GROUND, deco)
HDR = bg_frames('found_hd.gif', (W, 470), box=(0, 120, 1920, 120 + 835), step=2, bright=0.7)
GUM = {k: gummy(k, 2) for k in ['mush', 'cre', 'acv', 'mel', 'gold']}
VICF = vic(WIN, 330)
T_WIN = OUTS[-1][1]; END = T_WIN + 3.4
wr = Writer('ring_noaudio.mp4'); out_ev = []
sh_items = [e for e in EV if e[1] == 'shove']
for f in range(int(END * FPS)):
    t = f / FPS; st, gums = FR[min(f, len(FR) - 1)]
    img = GROUND.copy()
    def water(d):
        r2 = random.Random(7)
        for _ in range(110):
            x, y = r2.uniform(0, W), r2.uniform(AY0, H)
            if math.hypot(x - CX, y - CY) < RR + 40: continue
            ph = r2.uniform(0, 6.28); a = int(120 + 120 * math.sin(t * 3 + ph))
            if a > 150: d.rectangle([x, y, x + 6, y + 3], fill=(230, 250, 255, a - 60))
        for n in NAMES:
            s = st[n]
            if s['out'] is not None:
                for k in range(3):
                    u = ((t - s['out']) * 0.8 + k / 3) % 1.0; rr_ = 20 + 60 * u
                    d.ellipse([s['x'] - rr_, s['y'] - rr_ * 0.5, s['x'] + rr_, s['y'] + rr_ * 0.5], outline=(230, 250, 255, int(200 * (1 - u))), width=3)
    layer(img, water)
    for g in gums:
        gi = GUM[g['k']]; bob = int(6 * math.sin(t * 5 + g['x']))
        layer(img, lambda d, g=g: d.ellipse([g['x'] - 30, g['y'] - 16 - 6, g['x'] + 30, g['y'] + 16 - 6], fill=(255, 220, 120, 90)))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height - 4 + bob)))
    layer(img, lambda d: [d.ellipse([st[n]['x'] - 28, st[n]['y'] - 8, st[n]['x'] + 28, st[n]['y'] + 8], fill=(0, 0, 0, 80)) for n in NAMES if st[n]['out'] is None])
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if s['out'] is not None:
            u = t - s['out']
            if u < 0.35:
                spr = PANIC[n][int(t * 14) % 8]; sink = int(u / 0.35 * 120)
                c = spr.crop((0, 0, spr.width, max(1, FOOT - sink))); img.alpha_composite(c, (int(x - spr.width / 2), int(y - FOOT + sink)))
            else:
                hd = HEAD[n]; bob = int(5 * math.sin(t * 4 + x))
                img.alpha_composite(hd, (int(x - hd.width / 2), int(y - hd.height / 2 + bob)))
            continue
        if t < 2.2 or (WIN and t >= T_WIN): spr = STAND[n]
        elif t - s['stun'] < 0.45: spr = PANIC[n][int(t * 14) % 8]
        else:
            ph = int(s['dist'] / 22) % 8; v = math.hypot(s['vx'], s['vy']) or 1
            spr = FRUN[n][ph] if s['vy'] > 0.75 * v else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        if s['buff']:
            col = (255, 160, 40) if s['buff'] == 'mush' else (90, 150, 255)
            layer(img, lambda d, x=x, y=y, col=col: d.ellipse([x - 46, y - 18, x + 46, y + 18], outline=col + (220,), width=5))
        if t - s['dash'] < 0.3:
            layer(img, lambda d, x=x, y=y: [d.ellipse([x - 8 - 10 * k - s['vx'] * 0.02 * k, y - 10 - s['vy'] * 0.02 * k, x + 8 + 10 * k - s['vx'] * 0.02 * k, y + 4 - s['vy'] * 0.02 * k], fill=(230, 220, 200, 120 - 30 * k)) for k in range(3)])
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    items = []
    for e in EV:
        u = t - e[0]
        if 0 <= u < 0.8:
            a = int(255 * min(1, (0.8 - u) / 0.3))
            s = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[2]]
            if e[1] == 'shove': items.append((s['x'], s['y'] - FOOT - 30 - u * 40, 'SHOVE!', 30, (255, 220, 60), 6, a))
            elif e[1] == 'gum': items.append((s['x'], s['y'] - FOOT - 30 - u * 40, 'POWER SHOVE!' if e[3] == 'mush' else 'HEAVY!', 28, (255, 160, 40) if e[3] == 'mush' else (120, 170, 255), 6, a))
            elif e[1] == 'splash': items.append((s['x'], s['y'] - 80 - u * 40, 'SPLASH!', 32, (180, 230, 255), 6, a))
        if abs(t - e[0]) < 0.5 / FPS:
            out_ev.append((round(e[0], 3), {'shove': 'punch', 'gum': 'powerup_8bit', 'splash': 'boom'}[e[1]]))
    text_layer(img, items)
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda d: (d.rectangle([0, 0, W, 470], fill=(12, 8, 24, 70)), d.rounded_rectangle([18, 300, W - 18, 450], 18, fill=(12, 8, 24, 200))))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([18, 300, W - 18, 450], 18, outline=(255, 214, 60, 255), width=4)
    text_layer(img, [(W / 2, 50, 'LAST ONE IN', 70, (255, 255, 255), 8, 255), (W / 2, 150, 'THE RING WINS', 70, (255, 214, 60), 8, 255),
                     (W / 2, 245, 'Shoving allowed', 30, (255, 255, 255), 5, 255)])
    chips = []
    for i, n in enumerate(['joy', 'cyrus', 'cleo', 'ray', 'hollow']):
        sx = 18 + (W - 36) * (i + 0.5) / 5; ic = ICON[n] if st[n]['out'] is None else ImageEnhance.Brightness(ImageEnhance.Color(ICON[n]).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(sx - ic.width / 2), 312))
        out = st[n]['out'] is not None and st[n]['out'] <= t
        chips.append((sx, 392, 'OUT' if out else 'IN', 24, (255, 90, 80) if out else (140, 230, 120), 5, 255))
        if WIN and t >= T_WIN and n == WIN: layer(img, lambda d, sx=sx: d.ellipse([sx - 38, 308, sx + 38, 384], outline=(255, 214, 60, 255), width=6))
    text_layer(img, chips)
    if t < 2.6: text_layer(img, [(W / 2, CY - 40, 'PICK A PLAYER!', 54, (255, 255, 255), 8, 255)])
    for (n, to) in OUTS:
        u = t - to
        if 0 <= u < 1.6 and not (WIN and t >= T_WIN):
            text_layer(img, [(W / 2, H - 170, LABEL[n] + ' IS OUT!', 50, (255, 110, 100), 7, int(255 * min(1, (1.6 - u) / 0.4)))])
    if t >= T_WIN:
        u = t - T_WIN
        layer(img, lambda d: d.rectangle([0, 470, W, H], fill=(8, 6, 14, int(150 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1150 - vf.height))
        def conf(d):
            r2 = random.Random(f)
            for _ in range(45):
                x, y = r2.uniform(0, W), (r2.uniform(470, H) + u * 500) % H
                d.rectangle([x, y, x + 10, y + 10], fill=r2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (190, 90, 240)]) + (255,))
        layer(img, conf)
        text_layer(img, [(W / 2, 1200, LABEL[WIN] + ' WINS!', 66, (255, 214, 60), 8, 255)])
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN, 3), 'victory'))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(out_ev, open('ring_ev.json', 'w')); print('done', round(END, 2))
