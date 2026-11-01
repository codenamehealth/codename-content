import sys, os, math, random, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '..'); from powers import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['Choose your', 'champion'], accent=1, color=(110, 200, 255), sub='BEFORE THE RACE STARTS')
NAMES = ['joy', 'cleo', 'cyrus', 'ray']  # Hollow rule: the Hollow is the player, never a pickable champion
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel', 'hollow': 'gold'}
SWIM_SRC = {'joy': ('joy_swim', [4, 5, 6, 7, 8]), 'ray': ('ray_swim', [3, 4, 5, 6, 7, 8]), 'cyrus': ('cyrus_swim', [3, 4, 5, 6, 7, 8]),
            'cleo': ('cleo_swim3', [4, 5, 6, 7, 8])}
SS = 3
SWIM = {}
for g, (d, idx) in SWIM_SRC.items():
    fr = [Image.open(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/{d}/{i:02d}.png').convert('RGBA') for i in idx]
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    SWIM[g] = [up(f.crop(bb), SS) for f in fr]
# scene
BGF = bg_frames('found_hd.gif', (W, H), box=(1100, 0, 1707, 1080), step=2, bright=0.95)
STONE = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/stair/00.png').convert('RGBA')), 2)
BUOY = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/buoy/04.png').convert('RGBA')), 2)
PX0, PX1, PY0, PY1 = 150, 830, HB + 76, 1448
NL = 4; LH = (PY1 - PY0) / NL
LANEY = [PY0 + LH * (i + 0.5) for i in range(NL)]
XL, XR = 280, 700; LEN = XR - XL; TOT = 2 * LEN
T_GO = float(os.environ.get('TG', '0.6'))
SPEED_T, SPEED_K = 2.0, 1.8; STRONG_T = 2.5; SLEEP_T = 1.0; STUN_T = 0.6
def water_layer(t):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([PX0, PY0, PX1, PY1], fill=(38, 128, 206, 255))
    for i in range(NL):
        y0 = PY0 + LH * i
        d.rectangle([PX0, y0 + LH * 0.15, PX1, y0 + LH * 0.85], fill=(46, 142, 218, 255))
    rr = random.Random(11)
    for k in range(160):
        x = (rr.uniform(PX0, PX1) + t * rr.uniform(10, 30)) % (PX1 - PX0 - 30) + PX0; y = rr.uniform(PY0 + 6, PY1 - 10)
        x = int(x / 6) * 6; y = int(y / 6) * 6; w = rr.choice([12, 18, 24])
        d.rectangle([x, y, x + w, y + 5], fill=(120, 200, 245, 200))
    # lane line markers on the pool floor
    for i in range(NL):
        y = int(LANEY[i] / 6) * 6
        d.rectangle([XL - 20, y - 3, XR + 20, y + 3], fill=(28, 96, 170, 255))
    return L
FRAME = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for x in range(PX0 - STONE.width, PX1 + STONE.width, STONE.width - 4):
    FRAME.alpha_composite(STONE, (x, PY0 - STONE.height + 6)); FRAME.alpha_composite(STONE, (x, PY1 - 6))
for y in range(PY0 - STONE.height + 6, PY1 + STONE.height, STONE.height - 4):
    FRAME.alpha_composite(STONE, (PX0 - STONE.width + 6, y)); FRAME.alpha_composite(STONE.transpose(Image.FLIP_LEFT_RIGHT), (PX1 - 6, y))
for i in range(1, NL):
    y = PY0 + LH * i
    for k, x in enumerate(range(PX0 + 4, PX1 - 20, BUOY.width + 4)):
        b = BUOY if k % 2 == 0 else BUOY.rotate(90)
        FRAME.alpha_composite(b, (x, int(y - BUOY.height / 2)))
def sim(seed):
    """gummy powers (SPEC 12): each lane's gummy does what its type does.
    Cyrus mushroom SPEED (x1.8 for 2s), Cleo creatine STRONG (blue aura, power strokes x1.2 for 2.5s, and her
    first power stroke sends a wave that BONKs the swimmers in the lanes next to her: shoved back + slowed),
    Rayleigh melatonin SLEEP (every other swimmer stops 1s with Zzz), Joy ACV SHIELD (bubble blocks the next bonk/sleep)."""
    rnd = random.Random(seed)
    S = {n: dict(s=0.0, base=rnd.uniform(118, 134) * float(os.environ.get('SPF', '0.62')), ph=rnd.uniform(0, 6.3), fin=None, boost=None,
                 gs=rnd.uniform(200 * LEN / 680, TOT - 260 * LEN / 680), sleep=-9.0, stun=-9.0, shield=False, shield_t=None, pop=None) for n in NAMES}
    frames = []; first = None; half_lead = None; FX = []; PEND = []
    def hit(m, t, kind):
        o = S[m]
        if o['fin'] is not None: return
        if o['shield']: o['shield'] = False; o['pop'] = t; FX.append((t, 'block', m, kind)); return
        if kind == 'sleep': o['sleep'] = t + SLEEP_T
        else: o['stun'] = t + STUN_T; o['s'] = max(0.0, o['s'] - 18)
        FX.append((t, kind, m))
    for f in range(int(40 * FPS)):
        t = f / FPS; dt = 1 / FPS
        for pe in [p for p in PEND if p[0] <= t + 1e-6]: PEND.remove(pe); hit(pe[1], t, 'bonk')
        if t >= T_GO:
            for n, r in S.items():
                if r['fin'] is not None: continue
                if t < r['sleep']: continue
                sp = r['base'] * (1 + 0.16 * math.sin(0.9 * (t - T_GO) + r['ph']) + 0.07 * math.sin(2.7 * t + 2 * r['ph']))
                if r['boost'] is not None and t - r['boost'] < SPEED_T and GK[n] == 'mush': sp *= SPEED_K
                if r['boost'] is not None and t - r['boost'] < STRONG_T and GK[n] == 'cre': sp *= 1.2
                if t < r['stun']: sp *= 0.3
                if r['boost'] is None and r['s'] < r['gs'] <= r['s'] + sp * dt:
                    r['boost'] = t; k = GK[n]; FX.append((t, 'pick', n, k))
                    if k == 'acv': r['shield'] = True; r['shield_t'] = t
                    elif k == 'mel':
                        for m in NAMES:
                            if m != n: hit(m, t, 'sleep')
                        FX.append((t, 'sleepwave', n))
                    elif k == 'cre':
                        i = NAMES.index(n); FX.append((t, 'wave', n))
                        for j in (i - 1, i + 1):
                            if 0 <= j < len(NAMES): PEND.append((t + 0.25, NAMES[j]))
                r['s'] += sp * dt
                if r['s'] >= TOT: r['s'] = TOT; r['fin'] = t; first = first or (n, t)
            if half_lead is None and max(r['s'] for r in S.values()) >= LEN: half_lead = max(S, key=lambda n: S[n]['s'])
        frames.append({n: dict(s=r['s'], fin=r['fin'], boost=r['boost'], gs=r['gs'], sleep=r['sleep'], stun=r['stun'], shield=r['shield'], pop=r['pop']) for n, r in S.items()})
        if all(r['fin'] is not None for r in S.values()): break
    fins = sorted((r['fin'], n) for n, r in S.items())
    return frames, fins, half_lead, FX
def score(seed):
    fr, fins, hl, fx = sim(seed)
    if not any(e[1] in ('sleep', 'block') for e in fx) or not any(e[1] in ('bonk',) for e in fx): return None
    gap = fins[1][0] - fins[0][0]
    if not (0.03 < gap < 0.2): return None
    if hl == fins[0][1]: return None
    if not (10.0 < fins[0][0] < 15.0): return None
    # lead changes
    lead = None; ch = 0
    for st in fr[int(T_GO * FPS):]:
        l = max(st, key=lambda n: st[n]['s'])
        if l != lead: ch += 1; lead = l
    if ch < 4: return None
    if os.environ.get('WN') and fins[0][1] != os.environ['WN']: return None
    return round(fins[0][0], 2), fins[0][1], fins[1][1], round(gap, 3), ch
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, FINS, HL, FX = sim(SEED); print(FX)
win, T_F = FINS[0][1], FINS[0][0]; second = FINS[1][1]
print('fins', [(n, round(t, 2)) for t, n in FINS], 'half leader', HL)
VF = vic(win, 360)
ICON = {}
for n in NAMES:
    src = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}[n]
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((52, 52), Image.NEAREST)
    b = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([0, 0, 63, 63], fill=(20, 16, 30, 255)); d.ellipse([3, 3, 60, 60], fill=RING[n] + (255,)); d.ellipse([6, 6, 57, 57], fill=(235, 232, 220, 255))
    m = Image.new('L', (52, 52), 0); ImageDraw.Draw(m).ellipse([0, 0, 51, 51], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', (52, 52), (0, 0, 0, 0)), m).getchannel('A')); ICON[n] = b
def xpos(s):
    if s <= LEN: return XL + s, 1
    return XR - (s - LEN), -1
GHOST = {}
def swimmer(img, n, s, t, moving, fx={}):
    x, d = xpos(s); i = NAMES.index(n); y = LANEY[i]
    fr = SWIM[n][int(t * 10) % len(SWIM[n])] if moving else SWIM[n][0]
    if d < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    bob = 4 * math.sin(t * 6 + i)
    top = int(y - fr.height * 0.62 + bob); left = int(x - fr.width / 2)
    wl = int(y + 6 + bob) - top                     # waterline inside sprite
    a = fr.getchannel('A'); below = a.crop((0, max(0, wl), fr.width, fr.height)).point(lambda p: int(p * 0.35))
    fr2 = fr.copy(); a2 = a.copy(); a2.paste(below, (0, max(0, wl))); fr2.putalpha(a2)
    tint = Image.new('RGBA', fr.size, (40, 130, 210, 0)); ta = a.copy(); ta.paste(0, (0, 0, fr.width, max(0, wl))); ta = ta.point(lambda p: int(p * 0.55)); tint.putalpha(ta)
    fr2.alpha_composite(tint)
    if fx.get('speed'):
        afterimages(img, GHOST.get(n, [])[-4:]); speed_lines(img, x, y + bob + 10, d, t, 130)
        GHOST[n] = (GHOST.get(n, []) + [(fr2, left, top)])[-6:]
    else: GHOST[n] = []
    if fx.get('strong'):
        pu = 0.5 + 0.5 * math.sin(t * 14)
        layer(img, lambda dd: [dd.ellipse([x - 100 - q, top - 6 - q / 2, x + 100 + q, y + 30 + q / 2], fill=(90, 160, 255, int(40 + 30 * pu))) for q in (0, 16)])
        tt = tinted(fr, (200, 235, 255), int(200 + 55 * pu))
        for k_ in range(12):
            a_ = k_ * math.pi / 6; img.alpha_composite(tt, (int(left + 9 * math.cos(a_)), int(top + 9 * math.sin(a_))))
        tt = tinted(fr, (60, 130, 255), 255)
        for k_ in range(8):
            a_ = k_ * math.pi / 4; img.alpha_composite(tt, (int(left + 5 * math.cos(a_)), int(top + 5 * math.sin(a_))))
    if fx.get('asleep') is not None: sleepy(img, fr2, left, top); zzz(img, x, top + 10, fx['asleep'])
    else: img.alpha_composite(fr2, (left, top))
    if fx.get('stun'): dizzy(img, x, top + 8, t)
    if fx.get('shield'):
        layer(img, lambda dd: (dd.ellipse([x - 92, top - 14, x + 92, y + 34], fill=(110, 230, 90, 55), outline=(150, 255, 120, 230), width=6),
                               dd.arc([x - 70, top, x - 10, top + 60], 200, 260, fill=(230, 255, 220, 230), width=5)))
    if moving:
        def splash(dd):
            rr = random.Random(int(t * 30) + i * 7)
            for k in range(10):
                sx = x - d * (fr.width * 0.45 + rr.uniform(0, 50)); sy = y + bob + rr.uniform(-14, 10)
                dd.rectangle([sx, sy, sx + 6, sy + 6], fill=(235, 250, 255, 220))
            dd.arc([x - fr.width / 2 - 10, y - 6, x + fr.width / 2 + 10, y + 26], 200, 340, fill=(220, 245, 255, 160), width=4)
        layer(img, splash)
W_ = Writer('v37_noaudio.mp4'); ev = []
HOLD = 1.4                                    # photo finish freeze
END = T_F + HOLD + 3.4
seen_boost = set(); seen_turn = set(); seen_fin = set()
POPS = Pops(1.1)
for e in FX:
    if e[1] == 'pick':
        x, _ = xpos(FR[min(int(round(e[0] * FPS)), len(FR) - 1)][e[2]]['s']); POPS.add(e[0], x, LANEY[NAMES.index(e[2])] - 110, POWER[e[3]][0], POWER[e[3]][1], 40)
        ev.append((round(e[0], 3), SFX[e[3]]))
    elif e[1] == 'bonk':
        x, _ = xpos(FR[min(int(round(e[0] * FPS)), len(FR) - 1)][e[2]]['s']); POPS.add(e[0], x, LANEY[NAMES.index(e[2])] - 110, 'BONK!', (255, 255, 255), 36); ev.append((round(e[0], 3), 'punch'))
    elif e[1] == 'block':
        x, _ = xpos(FR[min(int(round(e[0] * FPS)), len(FR) - 1)][e[2]]['s']); POPS.add(e[0], x, LANEY[NAMES.index(e[2])] - 110, 'BLOCKED!', (110, 230, 90), 34); ev.append((round(e[0], 3), 'boing'))
OPEN = []
def scene(t_sim, t_anim):
    img = BGF[int(t_anim * 6) % len(BGF)].copy()
    img.alpha_composite(water_layer(t_anim)); img.alpha_composite(FRAME)
    st = FR[min(int(t_sim * FPS), len(FR) - 1)]
    # gummies
    for n in NAMES:
        r = st[n]
        if r['boost'] is None:
            gx, _ = xpos(r['gs']); gy = LANEY[NAMES.index(n)]; bob = int(5 * math.sin(t_anim * 4 + gx))
            g = gummy(GK[n], 3)
            layer(img, lambda d, gx=gx, gy=gy: d.ellipse([gx - 34, gy - 20, gx + 34, gy + 20], fill=(255, 255, 255, 60)))
            img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2 - 14 + bob)))
    # wave / sleep rings under the swimmers
    for e in FX:
        u = t_sim - e[0]
        if e[1] == 'wave' and 0 <= u < 0.45:
            x, _ = xpos(FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]['s']); y = LANEY[NAMES.index(e[2])]; q = u / 0.45
            layer(img, lambda dd, x=x, y=y, q=q: [dd.ellipse([x - 60 - 90 * q, y - 30 - LH * 1.1 * q, x + 60 + 90 * q, y + 30 + LH * 1.1 * q], outline=(150, 200, 255, int(240 * (1 - q))), width=12 - 4 * k_) for k_ in range(2)])
        if e[1] == 'sleepwave' and 0 <= u < 0.7:
            x, _ = xpos(FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]['s']); y = LANEY[NAMES.index(e[2])]
            sleep_wave(img, x, y, u / 0.7, 1100)
    for n in NAMES:
        r = st[n]; moving = r['fin'] is None and t_sim >= r['sleep']
        b = r['boost']; k = GK[n]
        fx = dict(speed=b is not None and k == 'mush' and 0 <= t_sim - b < SPEED_T, strong=b is not None and k == 'cre' and 0 <= t_sim - b < STRONG_T,
                  asleep=(t_sim - (r['sleep'] - SLEEP_T)) if t_sim < r['sleep'] else None, stun=t_sim < r['stun'] and r['fin'] is None, shield=r['shield'])
        swimmer(img, n, r['s'], t_anim, moving, fx)
        if r['pop'] is not None and 0 <= t_sim - r['pop'] < 0.5:
            x, _ = xpos(r['s']); shield_pop(img, x, LANEY[NAMES.index(n)] + 30, 140, (t_sim - r['pop']) / 0.5, 92)
    for e in FX:
        if e[1] == 'bonk' and 0 <= t_sim - e[0] < 0.3:
            x, _ = xpos(st[e[2]]['s']); bonk_burst(img, x, LANEY[NAMES.index(e[2])] - 20, (t_sim - e[0]) / 0.3)
    if any(e[1] == 'sleepwave' and 0 <= t_sim - e[0] < 0.25 for e in FX): img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 50)))
    text_layer(img, POPS.items(t_sim))
    for i, n in enumerate(NAMES):
        img.alpha_composite(ICON[n], (PX0 - 58, int(LANEY[i] - 32)))
    return img, st
for f in range(int(END * FPS)):
    t = f / FPS
    if t < T_F: t_sim = t; frozen = False
    elif t < T_F + HOLD: t_sim = T_F; frozen = True
    else: t_sim = t - HOLD; frozen = False
    img, st = scene(t_sim, t if not frozen else T_F)
    for n in NAMES:
        r = st[n]
        if r['s'] >= LEN and n not in seen_turn: seen_turn.add(n); ev.append((round(t, 3), 'swish'))
    if frozen:
        u = t - T_F
        # zoom on the finish wall around the two leaders
        ys = [LANEY[NAMES.index(win)], LANEY[NAMES.index(second)]]; cy = (ys[0] + ys[1]) / 2
        BX0, BY0, BX1, BY1 = PX0 - 50, int(PY0 - 48), PX1 + 50, 1496; bw, bh = BX1 - BX0, BY1 - BY0
        z = 1 + 0.9 * min(1, u / 0.35); cw, ch = bw / z, bh / z
        x0 = BX0; y0 = max(BY0, min(BY1 - ch, cy - ch / 2))
        zoom = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((bw, bh), Image.NEAREST)
        img.paste(zoom, (BX0, BY0))
        if u < 0.12: layer(img, lambda d: d.rectangle([BX0, BY0, BX1, BY1], fill=(255, 255, 255, int(200 * (1 - u / 0.12)))))
        layer(img, lambda d: d.rectangle([BX0, BY0, BX1, BY1], outline=(255, 255, 255, 255), width=8))
        text_layer(img, [(490, HB + 70, 'PHOTO FINISH!', 60, (255, 255, 255), 9, 255)])
        if u > 0.6: text_layer(img, [(490, HB + 160, LABEL[win] + ' BY A HAIR', 44, (255, 214, 60), 7, 255)])
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_F, 3), 'ding_8bit'))
    # header
    if t < T_GO:
        text_layer(img, [(490, 980, 'PICK ONE!', 80, (255, 255, 255), 9, 255)])
    elif t < T_GO + 0.6:
        text_layer(img, [(490, 960, 'GO!', 130, (255, 214, 60), 10, 255)])
        if not any(e[1] == 'go_8bit' for e in ev): ev.append((round(T_GO, 3), 'go_8bit'))
    if t >= T_F + HOLD:
        u = t - T_F - HOLD
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 8, 24, int(165 * min(1, u / 0.3)))))
        vf = VF[int(u * 8) % len(VF)]; img.alpha_composite(vf, (480 - vf.width // 2, 1170 - vf.height))
        text_layer(img, [(480, 1220, LABEL[win] + ' WINS!', 64, (255, 214, 60), 8, 255), (480, 1320, 'Did your champion win?', 34, (255, 255, 255), 5, 255)])
        if not any(e[1] == 'victory' for e in ev): ev.append((round(t, 3), 'victory'))
    img.alpha_composite(HOOK)
    W_.write(img)
    if f < 9: OPEN.append(img.copy())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/c_{f:04d}.png')
for im_ in OPEN: W_.write(im_)          # loop: cut back to the opening
W_.close()
json.dump(ev, open('v37_ev.json', 'w')); print('done', END)
