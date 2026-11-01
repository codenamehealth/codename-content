PANIC = {g: seqa(f'../../pixellab/maze/anim/{g}_panic') for g in NAMES}
POWIM = {k: gummy(k, 3) for k in POWER}
SRCF = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
def face(name, rad):
    im = Image.open('../../syeda_src/' + SRCF[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), m); return b
ICS2 = {n: face(n, 42) for n in NAMES}
HOOK, HB = hook_layer(["WHO'S IN", 'FIRST PLACE?'], accent=1)
CHIP_Y = HB + 6
print('hook bottom', HB, 'board', BY, BY + BH)
HUB = bg_frames('hub.gif', (W, 540), box=(0, 120, 1920, 120 + 960), step=2, bright=0.6)
hubp_src = bg_frames('hub.gif', (int(1920 * H / 1080), H), step=4, bright=0.72)
HUBP = [h.crop(((h.width - W) // 2, 0, (h.width - W) // 2 + W, H)) for h in hubp_src]
PED = crop(Image.open('../../fork2/pedestal/00.png').convert('RGBA'))
VICF = vic(WIN, 330)
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
def aura(view, spr, x0, y0, col, a):
    tt = tinted(spr, col, a)
    for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)): view.alpha_composite(tt, (x0 + ox, y0 + oy))
# pop labels (world coords) - stacked so they never overlap
POPS = []   # (t0, x, y, text, col, size)
def add_pop(t0, x, y, text, col, size=34):
    POPS.append((t0, x, y, text, col, size))
for e in FX:
    t0, kind = e[0], e[1]
    st0 = FR[min(int(round(t0 * FPS)), len(FR) - 1)][0]
    if kind == 'pick':
        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, POWER[e[3]][0], POWER[e[3]][1], 40)
    elif kind == 'hit':
        s = st0[e[3]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BONK!', (255, 255, 255), 36)
    elif kind == 'block':
        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BLOCKED!', (110, 230, 90), 32)
    elif kind == 'smash':
        r_, c_ = e[3]; add_pop(t0, c_ * C, r_ * C - 90, 'SMASH!', (90, 160, 255), 32)
POPS.sort(key=lambda p: p[0])
POP_D = 1.1
def pop_items(t, camx):
    act = [p for p in POPS if 0 <= t - p[0] < POP_D]; placed = []; items = []
    for t0, x, y, text, col, size in act:
        u = t - t0; sx = x - camx; sy = y - u * 30
        w = len(text) * size + 20; hh = size + 16
        sx = min(max(sx, 70 + w / 2), 1010 - w / 2)
        for _ in range(8):
            if any(abs(sx - px) < (w + pw) / 2 and abs(sy - py) < (hh + ph) / 2 for px, py, pw, ph in placed): sy -= hh + 4
            else: break
        sy = max(sy, 30)
        placed.append((sx, sy, w, hh)); al = int(255 * min(1, (POP_D - u) / 0.3)); sc = 1 + 0.3 * max(0, 1 - u / 0.15)
        items.append((sx, sy - hh / 2, text, int(size * sc), col, 6, al))
    return items
DUR_RACE = T_WIN + 1.2; T_POD = DUR_RACE; T_LOOP = T_POD + 3.0; DUR = T_LOOP + 0.3; NF = int(round(DUR * FPS))
wr = Writer('v46_noaudio.mp4'); ev = []; camx = -40.0; ghosts = {n: [] for n in NAMES}
seen_slide = set(); fin_seen = set(); rank_pos = {n: float(i) for i, n in enumerate(NAMES)}
SFX = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
for e in FX:
    if e[1] == 'pick': ev.append((round(e[0], 3), SFX[e[3]]))
    elif e[1] == 'hit': ev.append((round(e[0], 3), 'punch'))
    elif e[1] == 'block': ev.append((round(e[0], 3), 'boing'))
    elif e[1] == 'smash': ev.append((round(e[0], 3), 'crunch_8bit'))
ev.append((0.0, 'go_8bit'))
CAM0 = -40.0
for f in range(NF):
    t = f / FPS
    loop = t >= T_LOOP
    if loop: t = 0.0; camx = CAM0; rank_pos = {n: float(i) for i, n in enumerate(FR[0][1])}
    fi = int(round(t * FPS))
    st, rank, taken = FR[min(fi, len(FR) - 1)]
    if t < T_POD:
        lead_x = max(s['x'] for s in st.values())
        target = min(max(lead_x - 600, -40), BW + 600 - W)
        camx += (target - camx) * 0.12 if t > T_START else 0
        view = BOARD.crop((int(camx), 0, int(camx) + W, BH)).copy()
        # power gummies
        for k, (bx, by, kind) in enumerate(POWS):
            sx = bx - camx
            if not (-100 < sx < W + 100): continue
            col = POWER[kind][1]
            if k in taken and t >= taken[k][1]:
                u = t - taken[k][1]
                if u < 0.6:
                    layer(view, lambda dd, sx=sx, by=by, u=u, col=col: [dd.rectangle([sx + (20 + 120 * u) * math.cos(q * 0.628) - 6, by - 20 + (20 + 120 * u) * math.sin(q * 0.628) - 6,
                                                         sx + (20 + 120 * u) * math.cos(q * 0.628) + 6, by - 20 + (20 + 120 * u) * math.sin(q * 0.628) + 6], fill=col + (int(255 * (1 - u / 0.6)),)) for q in range(10)])
                continue
            bob = int(7 * math.sin(t * 4 + k)); g = POWIM[kind]
            layer(view, lambda dd, sx=sx, by=by, bob=bob, col=col: [dd.ellipse([sx - rr_, by - rr_ + bob - 12, sx + rr_, by + rr_ + bob - 12], fill=col + (al,)) for rr_, al in ((56, 40), (42, 70), (30, 90))])
            view.alpha_composite(g, (int(sx - g.width / 2), int(by - g.height / 2 - 12 + bob)))
        # sleep wave rings
        for e in FX:
            if e[1] == 'sleepwave' and 0 <= t - e[0] < 0.7:
                s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
                layer(view, lambda dd, s0=s0, u=u: [dd.ellipse([s0['x'] - camx - r_, s0['y'] - 60 - r_ * 0.7, s0['x'] - camx + r_, s0['y'] - 60 + r_ * 0.7], outline=(190, 120, 255, int(220 * (1 - u))), width=10) for r_ in (60 + 900 * u, 20 + 600 * u)])
            if e[1] == 'smash' and 0 <= t - e[0] < 0.5:
                r_, c_ = e[3]; u = (t - e[0]) / 0.5; px_, py_ = c_ * C - camx, r_ * C - 30
                layer(view, lambda dd, px_=px_, py_=py_, u=u: [dd.rectangle([px_ + math.cos(q * 0.9) * 140 * u - 8, py_ + math.sin(q * 0.9) * 90 * u + 160 * u * u - 8, px_ + math.cos(q * 0.9) * 140 * u + 8, py_ + math.sin(q * 0.9) * 90 * u + 160 * u * u + 8], fill=(150, 96, 50, int(255 * (1 - u)))) for q in range(9)])
            if e[1] == 'hit' and 0 <= t - e[0] < 0.3:
                s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[3]]; u = (t - e[0]) / 0.3
                cx_, cy_ = s0['x'] - camx, s0['y'] - FOOT / 2
                layer(view, lambda dd, cx_=cx_, cy_=cy_, u=u: [dd.polygon([(cx_ + math.cos(q * 0.785) * 30, cy_ + math.sin(q * 0.785) * 30), (cx_ + math.cos(q * 0.785 + 0.2) * (60 + 60 * u), cy_ + math.sin(q * 0.785 + 0.2) * (60 + 60 * u)),
                                                                 (cx_ + math.cos(q * 0.785 + 0.39) * 30, cy_ + math.sin(q * 0.785 + 0.39) * 30)], fill=(255, 255, 255, int(255 * (1 - u)))) for q in range(8)])
        # props (minus smashed ones) + racers, y-sorted
        items = [(y, 'p', x, im) for x, y, im in PROPL if -120 < x - camx < W + 120 and not (cpt(x, y) in SMASHED and t >= SMASHED[cpt(x, y)])] + [(st[n]['y'], 'r', n, None) for n in NAMES]
        layer(view, lambda dd: [dd.ellipse([st[n]['x'] - camx - 26, st[n]['y'] - 8, st[n]['x'] - camx + 26, st[n]['y'] + 8], fill=(0, 0, 0, 80)) for n in NAMES])
        for y, kind, a_, im in sorted(items, key=lambda z: z[0]):
            if kind == 'p':
                view.alpha_composite(im, (int(a_ - camx - im.width / 2), int(y - im.height + 26))); continue
            n = a_; s = st[n]; x = s['x'] - camx
            asleep = t < s['sleep']; stunned = t < s['stun']
            strong = s['strong'] is not None and 0 <= t - s['strong'] < STRONG_T
            boosted = s['boost'] is not None and 0 <= t - s['boost'] < SPEED_T
            if t < T_START: spr = (SRUN[n][int(t * 16) % 8])                     # running on the spot at the GO
            elif s['out'] is not None and t > s['out'] + 0.6: spr = STAND[n][int(t * 8) % len(STAND[n])]
            elif asleep: spr = STAND[n][0]
            elif stunned: spr = PANIC[n][int(t * 12) % len(PANIC[n])]
            elif s['sliding']:
                k = min(6, int((t - s['slide']) / SL * 7)); spr = (SLIDEL if s['vx'] < 0 else SLIDE)[n][k]
                if (n, round(s['slide'], 2)) not in seen_slide: seen_slide.add((n, round(s['slide'], 2))); ev.append((round(t, 3), 'jump'))
            else:
                ph = int(s['dist'] / 22) % 8
                spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
            x0, y0 = int(x - spr.width / 2), int(y - FOOT)
            if boosted and not asleep and not stunned:
                ghosts[n] = (ghosts[n] + [(spr, s['x'], y)])[-5:]
                for i_, (gs, gx2, gy2) in enumerate(ghosts[n][:-1]):
                    view.alpha_composite(tinted(gs, (255, 170, 50), int(255 * (0.14 + 0.09 * i_))), (int(gx2 - camx - gs.width / 2), int(gy2 - FOOT)))
                sgn = -1 if s['vx'] >= 0 else 1
                layer(view, lambda dd, x=x, y=y, sgn=sgn: ([dd.rectangle([x + sgn * (50 + 30 * q), y - 100 + q * 26 - 3, x + sgn * (50 + 30 * q) + sgn * (70 + (q * 37 + int(t * 60)) % 50), y - 100 + q * 26 + 3], fill=(255, 240, 200, 200)) for q in range(4)] +
                                                            [dd.ellipse([x + sgn * (30 + q * 26) - 14 + q * 2, y - 12 - q * 4, x + sgn * (30 + q * 26) + 14, y + 8], fill=(210, 190, 150, 150 - q * 40)) for q in range(3)]))
            else: ghosts[n] = []
            if strong: aura(view, spr, x0, y0, (90, 160, 255), int(150 + 80 * math.sin(t * 14)))
            if asleep:
                dark = spr.copy(); view.alpha_composite(dark, (x0, y0)); view.alpha_composite(tinted(spr, (40, 20, 90), 90), (x0, y0))
                u = (t - (s['sleep'] - SLEEP_T))
                text_layer(view, [(x + 30 + 18 * k_, y - FOOT - 10 - ((u * 1.6 + k_ * 0.33) % 1) * 70 - k_ * 14, 'Z', 30 + 8 * k_, (220, 200, 255), 5, int(255 * (1 - (u * 1.6 + k_ * 0.33) % 1))) for k_ in range(3)])
            else:
                view.alpha_composite(spr, (x0, y0))
            if stunned:
                layer(view, lambda dd, x=x, y=y: [dd.polygon([(x + 34 * math.cos(t * 9 + q * 2.09) + dx_, y - FOOT + 20 + 10 * math.sin(t * 9 + q * 2.09) + dy_) for dx_, dy_ in ((0, -9), (3, -3), (9, -2), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -2), (-3, -3))], fill=(255, 230, 60, 255)) for q in range(3)])
            if s['shield']:
                layer(view, lambda dd, x=x, y=y: (dd.ellipse([x - 70, y - FOOT + 6, x + 70, y + 18], fill=(110, 230, 90, 55), outline=(150, 255, 120, 220), width=6),
                                                  dd.arc([x - 52, y - FOOT + 24, x + 10, y - FOOT + 90], 200, 260, fill=(230, 255, 220, 230), width=5)))
            rk = rank.index(n) + 1
            dv = ImageDraw.Draw(view); ctext(dv, x, y - FOOT + 4, str(rk), F(26), RING[n], 5)
            if s['out'] is not None and n not in fin_seen and t >= s['out']:
                fin_seen.add(n); ev.append((round(t, 3), 'ding_8bit' if rank.index(n) else 'vg02'))
        text_layer(view, pop_items(t, camx))
        img = Image.new('RGBA', (W, H), (20, 40, 20, 255))
        img.alpha_composite(view, (0, BY))
        if any(e[1] == 'sleepwave' and 0 <= t - e[0] < 0.25 for e in FX):
            img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 50)))
        layer(img, lambda dd: dd.rectangle([0, BY - 6, W, BY], fill=(14, 10, 24, 255)))
        layer(img, lambda dd: (dd.rectangle([0, 0, W, BY], fill=(14, 10, 24, 255)), dd.rounded_rectangle([70, CHIP_Y, 1010, CHIP_Y + 100], 18, fill=(14, 10, 24, 230), outline=(255, 214, 60, 255), width=4)))
        img.alpha_composite(HUB[int(t * 6) % len(HUB)].crop((0, 0, W, CHIP_Y - 6)), (0, 0))
        d = ImageDraw.Draw(img)
        for i, n in enumerate(NAMES):
            tgt = rank.index(n); rank_pos[n] += (tgt - rank_pos[n]) * 0.2
        for ri in range(4):
            sx = 70 + 940 * (ri + 0.5) / 4
            ctext(d, sx + 44, CHIP_Y + 36, ['1ST', '2ND', '3RD', '4TH'][ri], F(28), (255, 214, 60) if ri == 0 else (230, 230, 230), 5)
        for n in sorted(NAMES, key=lambda n: -rank_pos[n]):
            sx = 70 + 940 * (rank_pos[n] + 0.5) / 4 - 50; ic = ICS2[n]
            img.alpha_composite(ic, (int(sx - ic.width / 2), CHIP_Y + 8))
            d = ImageDraw.Draw(img); ri = rank.index(n)
            if ri == 0 and abs(rank_pos[n]) < 0.15:
                cy0 = CHIP_Y + 4; d.polygon([(sx - 20, cy0 + 16), (sx - 12, cy0), (sx - 3, cy0 + 12), (sx, cy0 - 6), (sx + 3, cy0 + 12), (sx + 12, cy0), (sx + 20, cy0 + 16)], fill=(255, 214, 60), outline=(20, 15, 35))
        if t < 0.7:
            text_layer(img, [(W / 2, BY + 380, 'GO!', 150, (120, 230, 90), 10, int(255 * min(1, (0.7 - t) / 0.3)))])
    else:
        u = t - T_POD; order = [n for _, n in OUTS] + [n for n in rank if n not in [m for _, m in OUTS]]
        img = HUBP[int(t * 3) % len(HUBP)].copy()
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(10, 8, 18, 110)))
        spots = [(478, 1120, 6, 0), (478 - 270, 1200, 5, 1), (478 + 270, 1230, 5, 2)]
        for cx, top, k, idx in spots:
            ped = up(PED, k); img.alpha_composite(ped, (int(cx - ped.width / 2), int(top)))
            d = ImageDraw.Draw(img); ctext(d, cx, top + ped.height * 0.45, str(idx + 1), F(64 if idx == 0 else 52), (255, 214, 60) if idx == 0 else (235, 235, 235), 7)
            n = order[idx]; q = max(0, min(1, (u - 0.2 * (2 - idx)) / 0.4))
            if q <= 0: continue
            if idx == 0:
                vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (int(cx - vf.width / 2), int(top + 20 - vf.height - (1 - q) * 300)))
                d = ImageDraw.Draw(img); cy_ = top + 20 - vf.height - 60
                d.polygon([(cx - 50, cy_ + 40), (cx - 32, cy_), (cx - 10, cy_ + 28), (cx, cy_ - 8), (cx + 10, cy_ + 28), (cx + 32, cy_), (cx + 50, cy_ + 40)], fill=(255, 214, 60), outline=(20, 15, 35))
            else:
                sp_ = STAND[n][int(t * 8) % len(STAND[n])]; sp_ = up(sp_, 1.5)
                img.alpha_composite(sp_, (int(cx - sp_.width / 2), int(top + 20 - 78 * 3 - (1 - q) * 200)))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2, HB + 24, 'WINNER', F(84), (255, 214, 60), 10)
        ctext(d, W / 2, HB + 130, LABEL[WIN] + '!', F(60), (255, 255, 255), 8)
        if u > 0.8: text_layer(img, [(W / 2, HB + 214, 'DID YOU PICK RIGHT?', 40, (255, 255, 255), 7, int(255 * min(1, (u - 0.8) / 0.4)))])
        rr2 = random.Random(f)
        for _ in range(50):
            cx_, cy_ = rr2.uniform(0, W), (rr2.uniform(-200, H) + u * 520) % H
            d.rectangle([cx_, cy_, cx_ + 11, cy_ + 11], fill=rr2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]))
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'victory')); ev.append((round(t, 3), 'cheer'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0 or f == NF - 1: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
    if os.environ.get('FULL') and f in [int(round(e[0] * FPS)) + 4 for e in FX]: img.convert('RGB').save(f'fx_{f:04d}.png')
wr.close(); json.dump(ev, open('v46_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
