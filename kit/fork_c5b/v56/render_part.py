# ---------------- render (content pass)
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
EV = []
def ev(t, name): EV.append((round(t, 3), name))
ev(0.0, 'go_8bit'); ev(0.05, 'cheer'); ev(T_GO, 'whoosh_8bit')
SFX = {'bonk': 'stomp_8bit', 'dizzy': 'whoosh_8bit', 'fin': 'ding_8bit', 'smash': 'crunch_8bit', 'shove': 'punch', 'block': 'boing'}
PSFX = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
for e in EVS:
    t, k = e[0], e[1]
    if t > T_WIN + 3.0: continue
    if k == 'pick': ev(t, PSFX[e[3]])
    elif k in SFX: ev(t, SFX[k])
ev(T_WIN, 'victory')
T_CARD = T_WIN + 0.8; T_LOOP = T_CARD + 2.6; T_ALL = T_LOOP + 0.3; NF = int(round(T_ALL * FPS))
POPTXT = {'bonk': ('BONK!', (255, 255, 255), 40), 'dizzy': ('DIZZY!', (150, 220, 255), 40), 'smash': ('SMASH!', (90, 160, 255), 46),
          'shove': ('BONK!', (255, 255, 255), 46), 'block': ('BLOCKED!', (110, 230, 90), 46)}
POPS = []   # (t0, name, text, col, size)
for e in EVS:
    t, k = e[0], e[1]
    if t > T_WIN: continue
    if k == 'pick': POPS.append((t, e[2], POWER[e[3]][0], POWER[e[3]][1], 50))
    elif k in POPTXT: POPS.append((t, e[2], ) + POPTXT[k])
POP_D = 1.0
SLEEPW = [e for e in EVS if e[1] == 'sleepwave']
ROCKSPR = ROCKS
cam = 0.0
wr = Writer(OUT + 'v56_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    if t >= T_LOOP: t = 0.0; cam_reset = True
    else: cam_reset = False
    fi = int(round(t * FPS)); st, taken, smashed = FR[min(fi, len(FR) - 1)]
    lead_y = max(st[n]['y'] for n in NAMES)
    tgt = max(0, min(WORLD.height - VH, lead_y - LEADY))
    cam = tgt if (f == 0 or cam_reset) else cam + (tgt - cam) * 0.12
    view = WORLD.crop((0, int(cam), W, int(cam) + VH))
    img = Image.new('RGBA', (W, H), (20, 40, 20, 255)); img.alpha_composite(view, (0, VY0))
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    for o in OBS:
        if o[0] != 'pool': continue
        sx, sy = cx(o[1]) + o[2], o[1] - cam + VY0
        if not (VY0 - 150 < sy < H + 150): continue
        for r_ in range(6):
            rad = 20 + r_ * 14; a0 = (t * 220 + r_ * 40) % 360
            dl.arc([sx - rad, sy - rad * 0.7, sx + rad, sy + rad * 0.7], a0, a0 + 230, fill=(225, 245, 255, 200 - r_ * 22), width=5)
        dl.ellipse([sx - 14, sy - 9, sx + 14, sy + 9], fill=(20, 60, 110, 200))
    img.alpha_composite(L)
    # floating gummies + pickup bursts
    for j, o in enumerate(OBS):
        if o[0] != 'gum': continue
        sx, sy = cx(o[1]) + o[2], o[1] - cam + VY0 + 6 * math.sin(t * 3 + j)
        if not (VY0 - 100 < sy < H + 100): continue
        col = POWER[o[3]][1]
        if j in taken:
            tp = next((e[0] for e in EVS if e[1] == 'pick' and e[0] <= t + 1e-6 and abs((cx(o[1]) + o[2]) - 0) >= 0 and e[3] == o[3]), None)
            continue
        layer(img, lambda dd, sx=sx, sy=sy, col=col: [dd.ellipse([sx - 50 + k_ * 9, sy - 38 + k_ * 7, sx + 50 - k_ * 9, sy + 38 - k_ * 7], fill=col + (40 + k_ * 25,)) for k_ in range(3)])
        g = GUM[o[3]]; img.alpha_composite(g, (int(sx - g.width / 2), int(sy - g.height / 2)))
    for e in EVS:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.6:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.6
            px_, py_ = s0['x'], s0['y'] - cam + VY0 - 40; col = POWER[e[3]][1]
            layer(img, lambda dd, px_=px_, py_=py_, u=u, col=col: [dd.rectangle([px_ + (30 + 140 * u) * math.cos(q * 0.628) - 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) - 7, px_ + (30 + 140 * u) * math.cos(q * 0.628) + 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    # sleep wave rings
    for e in SLEEPW:
        if 0 <= t - e[0] < 0.7:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
            px_, py_ = s0['x'], s0['y'] - cam + VY0 - 60
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.ellipse([px_ - r_, py_ - r_ * 0.8, px_ + r_, py_ + r_ * 0.8], outline=(190, 120, 255, int(230 * (1 - u))), width=14) for r_ in (60 + 1300 * u, 20 + 900 * u)])
    # rocks + barrels, y-sorted
    items = []
    for j, o in enumerate(OBS):
        if o[0] != 'rock': continue
        sy = o[1] - cam + VY0
        if not (-150 < sy < H + 150): continue
        if j in smashed and t >= smashed[j]:
            u = (t - smashed[j]) / 0.7
            if u < 1:
                sx = cx(o[1]) + o[2]
                layer(img, lambda dd, sx=sx, sy=sy, u=u, j=j: [dd.rectangle([sx + math.cos(q * 0.8 + j) * 200 * u - 10, sy + math.sin(q * 0.8 + j) * 120 * u - 10, sx + math.cos(q * 0.8 + j) * 200 * u + 10, sy + math.sin(q * 0.8 + j) * 120 * u + 10], fill=(120, 116, 104, int(255 * (1 - u)))) for q in range(10)])
            continue
        items.append((o[1], 'rock', j))
    for n in NAMES: items.append((st[n]['y'], 'boat', n))
    off_top = []
    for _, kind, ref in sorted(items, key=lambda it: it[0]):
        if kind == 'rock':
            o = OBS[ref]; r_ = ROCKSPR[o[3]]; x = cx(o[1]) + o[2]; sy = o[1] - cam + VY0
            layer(img, lambda dd, x=x, sy=sy, r_=r_: dd.ellipse([x - r_.width * 0.55, sy + r_.height * 0.25, x + r_.width * 0.55, sy + r_.height * 0.62], fill=(225, 245, 255, 120)))
            img.alpha_composite(r_, (int(x - r_.width / 2), int(sy - r_.height / 2)))
            continue
        n = ref; s = st[n]; sx, sy = s['x'], s['y'] - cam + VY0
        if sy < P1 + 70: off_top.append(n); continue
        if sy > H + 150: continue
        asleep = t < s['sleep']; boosted = t - s['boost'] < SPEED_T; strong = t - s['strong'] < STRONG_T
        L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        for k_ in range(6):
            wy = sy - 50 - k_ * 22; a = (200 - k_ * 32) // (3 if asleep else 1)
            spread = 30 + k_ * 9
            dl.rectangle([sx - spread - 6, wy - 4, sx - spread + 6, wy + 4], fill=(240, 250, 255, a))
            dl.rectangle([sx + spread - 6, wy - 4, sx + spread + 6, wy + 4], fill=(240, 250, 255, a))
        if boosted:
            for k_ in range(6):
                lx = sx - 85 + k_ * 34; ly = sy - 130 - ((t * 700 + k_ * 47) % 180)
                dl.rectangle([lx - 4, ly, lx + 4, ly + 54], fill=(255, 200, 110, 220))
        img.alpha_composite(L)
        B = boat(n, sx, sy, 0.0 if asleep else t, s)
        bx0, by0 = int(sx - 110), int(sy - 150)
        if boosted:
            for q in range(3):
                img.alpha_composite(tinted(B, (255, 170, 50), int(255 * (0.32 - 0.09 * q))), (bx0, by0 - int((q + 1) * 26)))
        if strong:
            tt = tinted(B, (90, 160, 255), int(170 + 70 * math.sin(t * 14)))
            for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)): img.alpha_composite(tt, (bx0 + ox, by0 + oy))
        img.alpha_composite(B, (bx0, by0))
        if asleep:
            img.alpha_composite(tinted(B, (40, 20, 90), 120), (bx0, by0))
            u = t - (s['sleep'] - SLEEP_T)
            text_layer(img, [(sx + 50 + 22 * kz, sy - 120 - ((u * 1.4 + kz * 0.33) % 1) * 70 - kz * 16, 'Z', 36 + 10 * kz, (225, 205, 255), 6, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
        if s['shield']:
            layer(img, lambda dd: (dd.ellipse([sx - 105, sy - 150, sx + 105, sy + 100], fill=(110, 230, 90, 50), outline=(150, 255, 120, 230), width=7),
                                   dd.arc([sx - 80, sy - 128, sx - 20, sy - 60], 200, 260, fill=(230, 255, 220, 230), width=6)))
        if t - s['bonk'] < 0.5 and t >= s['bonk']:
            u = (t - s['bonk']) / 0.5
            layer(img, lambda dd: [dd.polygon([(sx + math.cos(q * 0.785) * 40, sy - 60 + math.sin(q * 0.785) * 40), (sx + math.cos(q * 0.785 + 0.2) * (80 + 60 * u), sy - 60 + math.sin(q * 0.785 + 0.2) * (80 + 60 * u)), (sx + math.cos(q * 0.785 + 0.39) * 40, sy - 60 + math.sin(q * 0.785 + 0.39) * 40)], fill=(255, 255, 255, int(220 * (1 - u)))) for q in range(8)])
        tag = ICS[n]; tx = sx + 50 if sx < 700 else sx - 96; img.alpha_composite(tag, (int(tx), int(sy + 30)))
    if any(0 <= t - e[0] < 0.25 for e in SLEEPW):
        img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 55)))
    # pop labels (stacked, never overlapping)
    placed = []; items = []
    for t0, n, text, col, size in POPS:
        u = t - t0
        if not (0 <= u < POP_D): continue
        s = st[n]; sx, sy = s['x'], s['y'] - cam + VY0 - 200 - u * 30
        w_ = len(text) * size + 20; hh = size + 16
        lim_r = 1015 if sy < 1110 else 877
        sx = min(max(sx, 70 + w_ / 2), lim_r - w_ / 2)
        for _ in range(8):
            if any(abs(sx - px) < (w_ + pw) / 2 and abs(sy - py) < (hh + ph) / 2 for px, py, pw, ph in placed): sy -= hh + 4
            else: break
        sy = max(sy, P1 + 20)
        if sy > 1490 - hh: continue
        placed.append((sx, sy, w_, hh)); al = int(255 * min(1, (POP_D - u) / 0.3)); sc = 1 + 0.3 * max(0, 1 - u / 0.15)
        items.append((sx, sy - hh / 2, text, int(size * sc), col, 8, al))
    if T_WIN <= t < T_CARD:
        u = t - T_WIN; s = st[WIN]; sc = 1 + 0.4 * max(0, 1 - u / 0.15)
        items.append((min(max(s['x'], 330), 640), min(1300, s['y'] - cam + VY0 - 260), 'WINNER!', int(72 * sc), (255, 214, 60), 10, 255))
    if items: text_layer(img, items)
    if t < 0.8:
        sc = 1 + 0.3 * max(0, 1 - t / 0.2)
        text_layer(img, [(W / 2, 760, 'PADDLE!', int(110 * sc), (120, 220, 255), 10, int(255 * min(1, (0.8 - t) / 0.3)))])
    for k_, n in enumerate(off_top):
        ic = ICS[n]; x = int(max(100, min(W - 110, st[n]['x'])))
        img.alpha_composite(ic, (x - 23, P1 + 10))
    rank = sorted(NAMES, key=lambda n: (-(1e9 - st[n]['fin']) if st[n]['fin'] is not None else -st[n]['y']))
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(14, 10, 24, 200)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(120, 220, 255, 255), width=4)
    for i, n in enumerate(rank):
        x = 70 + 955 * (i + 0.5) / 4; ic = ICON[n]; img.alpha_composite(ic, (int(x - ic.width / 2), P0 + 12))
        text_layer(img, [(x, P0 + 98, ['1ST', '2ND', '3RD', '4TH'][i], 26, (255, 214, 60) if i == 0 else (230, 230, 230), 4, 255)])
    if t >= T_CARD:
        u = t - T_CARD; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, P1 + 4, W, H], fill=(8, 10, 22, int(165 * a))))
        if a > 0.2:
            vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1040 - vf.height))
            text_layer(img, [(W / 2, 1075, LABEL[WIN] + ' WINS!', 60, (255, 214, 60), 8, int(255 * a)),
                             (W / 2, 1175, 'DID YOUR CHAMPION WIN?', 30, (255, 255, 255), 6, int(255 * a))])
            rr2 = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                x_, y_ = rr2.uniform(80, 1010), (rr2.uniform(0, H) + u * 400) % (1480 - P1) + P1
                dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p56_{f:04d}.png')
    if os.environ.get('FULL') and any(abs(t - (e[0] + 0.2)) < 0.5 / FPS for e in EVS if e[1] in ('pick', 'smash', 'shove', 'bonk')) and not f >= int(T_LOOP * FPS):
        img.convert('RGB').save(OUT + f'k_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'v56_ev.json', 'w'))
print('done', round(T_ALL, 2), len(EV))
