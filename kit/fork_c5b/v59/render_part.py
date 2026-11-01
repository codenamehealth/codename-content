# ---------------- render (content pass)
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SK) for g in NAMES}
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
EV = []
def ev(t, name): EV.append((round(t, 3), name))
ev(0.0, 'go_8bit'); ev(T_GO, 'whoosh_8bit')
PSFX = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
lastj = -1
for e in EVS:
    t, kd = e[0], e[1]
    if kd == 'jump' and t - lastj > 0.25: ev(t, 'jump'); lastj = t
    elif kd == 'boing': ev(t, 'boing')
    elif kd == 'pick': ev(t, PSFX[e[3]])
    elif kd == 'shove': ev(t, 'punch')
    elif kd == 'block': ev(t, 'boing')
    elif kd == 'caught': ev(t, 'poof'); ev(t + 0.05, 'buzz_8bit')
    elif kd == 'win': ev(t, 'victory'); ev(t + 0.1, 'cheer')
T_CARD = T_WIN + 0.8; T_LOOP = T_CARD + 2.6; T_ALL = T_LOOP + 0.3; NF = int(round(T_ALL * FPS))
POPS = []
for e in EVS:
    if e[0] > T_WIN: continue
    if e[1] == 'pick': POPS.append((e[0], e[2], POWER[e[3]][0], POWER[e[3]][1], 50))
    elif e[1] == 'shove': POPS.append((e[0], e[2], 'BONK!', (255, 255, 255), 50))
    elif e[1] == 'block': POPS.append((e[0], e[2], 'BLOCKED!', (110, 230, 90), 46))
    elif e[1] == 'boing': POPS.append((e[0], e[2], 'BOING!', (150, 255, 150), 36))
CAUGHT = [e for e in EVS if e[1] == 'caught']
SLEEPW = [e for e in EVS if e[1] == 'sleepwave']
GCOL = {k: v[1] for k, v in POWER.items()}
cam = 0
wr = Writer(OUT + 'v59_noaudio.mp4')
for f in range(NF):
    t = f / FPS; loopcut = t >= T_LOOP
    if loopcut: t = 0.0
    fi = int(round(t * FPS)); st, wl, taken = FR[min(fi, len(FR) - 1)]
    live = [n for n in NAMES if st[n]['caught'] is None]
    focus = min(st[n]['y'] for n in live) if live else st[WIN]['y']
    if t < T_GO: focus = py(0)
    low = max(st[n]['y'] for n in live) if live else focus
    recent = any(0 <= t - e[0] < 1.3 for e in CAUGHT)
    danger = (wl - low < 330) or recent
    hi_c = focus - 880
    lo_c = (max(wl - 30, low) if danger else low) - 1450
    tgt = lo_c if lo_c > hi_c and danger else min(hi_c, max(lo_c, focus - 1300))
    if t < T_GO: tgt = py(0) - 1300
    tgt = max(0, min(WH - H, tgt))
    cam = tgt if (f == 0 or loopcut) else cam + (tgt - cam) * 0.1
    c0 = int(cam)
    img = WORLD.crop((0, c0, W, c0 + H)).copy()
    for r, i in SLIMEPAD.items():
        rr, x0, x1 = PLAT[i]; sx = (x0 + x1) / 2; sy = py(rr) - c0
        hit = any(0 <= t - e[0] < 0.3 and e[1] == 'boing' and abs(st[e[2]]['x'] - sx) < 400 for e in EVS)
        fr = SPLAT[3] if hit else SLIME[int(t * 10) % len(SLIME)]
        img.alpha_composite(fr, (int(sx - fr.width / 2), int(sy - fr.height + 30)))
        if not hit: text_layer(img, [(sx, sy - 120, 'BOING PAD', 18, (150, 255, 150), 4, 220)])
    # gummies (each one on a platform the guides climb through)
    for g in GUMS:
        if g in taken: continue
        i, gx, kd = g; gy = py(PLAT[i][0]) - c0 - 60 + 8 * math.sin(t * 3 + gx); col = GCOL[kd]
        layer(img, lambda dd, gx=gx, gy=gy, col=col: [dd.ellipse([gx - 48 + k_ * 9, gy - 44 + k_ * 9, gx + 48 - k_ * 9, gy + 44 - k_ * 9], fill=col + (40 + k_ * 30,)) for k_ in range(3)])
        gm = GUM[kd]; img.alpha_composite(gm, (int(gx - gm.width / 2), int(gy - gm.height / 2)))
    for e in EVS:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.6:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.6
            px_, py_ = s0['x'], s0['y'] - c0 - 90; col = GCOL[e[3]]
            layer(img, lambda dd, px_=px_, py_=py_, u=u, col=col: [dd.rectangle([px_ + (30 + 140 * u) * math.cos(q * 0.628) - 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) - 7, px_ + (30 + 140 * u) * math.cos(q * 0.628) + 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    for e in SLEEPW:
        if 0 <= t - e[0] < 0.7:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
            px_, py_ = s0['x'], s0['y'] - c0 - 110
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.ellipse([px_ - r_, py_ - r_, px_ + r_, py_ + r_], outline=(190, 120, 255, int(230 * (1 - u))), width=14) for r_ in (60 + 1400 * u, 20 + 1000 * u)])
    # guides
    for n in NAMES:
        s = st[n]; x, yy = s['x'], s['y'] - c0
        if s['caught'] is not None:
            fr = SWIM[n][int(t * 8) % len(SWIM[n])]
            if int(t * 1.5 + NAMES.index(n)) % 2: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(fr, (int(x - fr.width / 2), int(yy - 78 * SK + 70 + 4 * math.sin(t * 4))))
            continue
        asleep = t < s['sleep']; stunned = t < s['stun'] and not asleep
        boosted = t - s['boost'] < SPEED_T; strong = t - s['strong'] < STRONG_T
        if t < T_GO or (s['done'] is not None and t > s['done']) or asleep: fr = STAND[n]
        elif stunned: fr = PANIC[n][int(t * 12) % len(PANIC[n])]
        elif s['mode'] == 'jump': fr = SR[n][3]
        else: fr = SR[n][int(t * (20 if boosted else 14)) % 8]
        if s['vx'] < 0 and fr is not STAND[n]: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
        x0, y0 = int(x - fr.width / 2), int(yy - 78 * SK + 6)
        if boosted and not asleep and not stunned:
            for q in range(3):
                img.alpha_composite(tinted(fr, (255, 170, 50), int(255 * (0.34 - 0.09 * q))), (x0 - int(s['vx'] * (q + 1) * 26), y0 + (q + 1) * 6))
            sgn = -1 if s['vx'] >= 0 else 1
            layer(img, lambda dd: [dd.rectangle([min(x + sgn * (50 + 26 * q), x + sgn * (130 + 26 * q + (q * 37 + int(t * 60)) % 40)), yy - 150 + q * 30 - 4, max(x + sgn * (50 + 26 * q), x + sgn * (130 + 26 * q + (q * 37 + int(t * 60)) % 40)), yy - 150 + q * 30 + 4], fill=(255, 240, 200, 210)) for q in range(4)] +
                                  [dd.ellipse([x + sgn * (40 + q * 30) - 18, yy - 18 - q * 5, x + sgn * (40 + q * 30) + 18, yy + 6], fill=(210, 190, 150, 170 - q * 45)) for q in range(3)])
        if strong and not asleep:
            tt = tinted(fr, (90, 160, 255), int(170 + 70 * math.sin(t * 14)))
            for ox, oy in ((-7, 0), (7, 0), (0, -7), (0, 7), (-5, -5), (5, 5), (-5, 5), (5, -5)): img.alpha_composite(tt, (x0 + ox, y0 + oy))
        img.alpha_composite(fr, (x0, y0))
        if asleep:
            img.alpha_composite(tinted(fr, (40, 20, 90), 120), (x0, y0))
            u = t - (s['sleep'] - SLEEP_T)
            text_layer(img, [(x + 50 + 22 * kz, yy - 200 - ((u * 1.4 + kz * 0.33) % 1) * 70 - kz * 16, 'Z', 36 + 10 * kz, (225, 205, 255), 6, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
        if stunned:
            layer(img, lambda dd: [dd.polygon([(x + 50 * math.cos(t * 9 + q * 2.09) + dx_ * 1.4, yy - 200 + 14 * math.sin(t * 9 + q * 2.09) + dy_ * 1.4) for dx_, dy_ in ((0, -9), (3, -3), (9, -2), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -2), (-3, -3))], fill=(255, 230, 60, 255)) for q in range(3)])
        if s['shield']:
            layer(img, lambda dd: (dd.ellipse([x - 100, yy - 250, x + 100, yy + 20], fill=(110, 230, 90, 55), outline=(150, 255, 120, 230), width=7),
                                   dd.arc([x - 74, yy - 226, x - 14, yy - 150], 200, 260, fill=(230, 255, 220, 230), width=6)))
    for e in EVS:
        if e[1] == 'shove' and 0 <= t - e[0] < 0.35:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.35
            cx_, cy_ = s0['x'], s0['y'] - c0 - 110
            layer(img, lambda dd, cx_=cx_, cy_=cy_, u=u: [dd.polygon([(cx_ + math.cos(q * 0.785) * 40, cy_ + math.sin(q * 0.785) * 40), (cx_ + math.cos(q * 0.785 + 0.2) * (80 + 80 * u), cy_ + math.sin(q * 0.785 + 0.2) * (80 + 80 * u)), (cx_ + math.cos(q * 0.785 + 0.39) * 40, cy_ + math.sin(q * 0.785 + 0.39) * 40)], fill=(255, 255, 255, int(240 * (1 - u)))) for q in range(8)])
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
    if any(0 <= t - e[0] < 0.25 for e in SLEEPW):
        img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 55)))
    # pop labels (stacked, never overlapping)
    placed = []; items = []
    for t0, n, text, col, size in POPS:
        u = t - t0
        if not (0 <= u < 1.0): continue
        s = st[n]; sx, sy = s['x'], s['y'] - c0 - 290 - u * 30
        w_ = len(text) * size + 20; hh = size + 16
        sy = max(sy, P1 + hh / 2 + 16)
        lim_r = 1015 if sy < 1110 else 877
        sx = min(max(sx, 70 + w_ / 2), lim_r - w_ / 2)
        for _ in range(8):
            if any(abs(sx - px) < (w_ + pw) / 2 and abs(sy - py_) < (hh + ph) / 2 for px, py_, pw, ph in placed): sy += hh + 4
            else: break
        if sy > 1490 - hh / 2: continue
        placed.append((sx, sy, w_, hh)); al = int(255 * min(1, (1.0 - u) / 0.3)); sc = 1 + 0.3 * max(0, 1 - u / 0.15)
        items.append((sx, sy - hh / 2, text, int(size * sc), col, 8, al))
    # big OUT stamps (same weight as the win stamp)
    for e in CAUGHT:
        u = t - e[0]
        if 0 <= u < 1.0:
            s = st[e[2]]; sc = 1 + 0.4 * max(0, 1 - u / 0.15); txt = LABEL[e[2]] + ' OUT!'
            wv = len(txt) * 72; sx = min(max(s['x'], 70 + wv / 2 + 10), 877 - wv / 2)
            sy = min(max(wl - c0 - 230, P1 + 80), 1330)
            items.append((sx, sy, txt, int(72 * sc), (255, 95, 95), 10, int(255 * min(1, (1.0 - u) / 0.25))))
    if T_WIN <= t < T_CARD:
        u = t - T_WIN; s = st[WIN]; sc = 1 + 0.4 * max(0, 1 - u / 0.15)
        items.append((W / 2 - 60, min(max(s['y'] - c0 - 330, P1 + 80), 1300), 'WINNER!', int(80 * sc), (255, 214, 60), 10, 255))
    if items: text_layer(img, items)
    layer(img, lambda dd: dd.rounded_rectangle([70, P0, 1025, P1], 16, fill=(10, 24, 30, 220)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, P0, 1025, P1], 16, outline=(120, 220, 255, 255), width=4)
    for i, n in enumerate(NAMES):
        x = 70 + 955 * (i + 0.5) / 4; ic = ICON[n]
        if st[n]['caught'] is not None: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55)
        img.alpha_composite(ic, (int(x - ic.width / 2), P0 + 8))
        if st[n]['caught'] is not None: text_layer(img, [(x, P0 + 90, 'OUT', 24, (255, 110, 110), 4, 255)])
        elif st[n]['done'] is not None: text_layer(img, [(x, P0 + 90, 'SAFE!', 24, (255, 214, 60), 4, 255)])
    if t < 0.8:
        sc = 1 + 0.3 * max(0, 1 - t / 0.2)
        text_layer(img, [(W / 2 - 60, 1000, 'CLIMB!', int(130 * sc), (120, 220, 255), 12, int(255 * min(1, (0.8 - t) / 0.3)))])
    if t >= T_CARD:
        u = t - T_CARD; a = min(1, u / 0.35)
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
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p59_{f:04d}.png')
    if os.environ.get('FULL') and not loopcut and any(abs(t - (e[0] + 0.2)) < 0.5 / FPS for e in EVS if e[1] in ('pick', 'shove', 'caught', 'win')):
        img.convert('RGB').save(OUT + f'k_{f:04d}.png')
wr.close()
json.dump({'events': sorted(EV)}, open(OUT + 'v59_ev.json', 'w'))
print('done', round(T_ALL, 2), len(EV))
