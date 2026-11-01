import sys, os, math, random, json
sys.path.insert(0, '../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cleo', 'cyrus', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel', 'hollow': 'gold'}
SWIM_SRC = {'joy': ('joy_swim', [4, 5, 6, 7, 8]), 'ray': ('ray_swim', [3, 4, 5, 6, 7, 8]), 'cyrus': ('cyrus_swim', [3, 4, 5, 6, 7, 8]),
            'cleo': ('cleo_swim3', [4, 5, 6, 7, 8]), 'hollow': ('hollow_swim3', [4, 5, 6, 7, 8])}
SS = 3
SWIM = {}
for g, (d, idx) in SWIM_SRC.items():
    fr = [Image.open(f'{d}/{i:02d}.png').convert('RGBA') for i in idx]
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    SWIM[g] = [up(f.crop(bb), SS) for f in fr]
# scene
BGF = bg_frames('found_hd.gif', (W, H), box=(1100, 0, 1707, 1080), step=2, bright=0.95)
STONE = up(crop(Image.open('stair/00.png').convert('RGBA')), 2)
BUOY = up(crop(Image.open('buoy/04.png').convert('RGBA')), 2)
PX0, PX1, PY0, PY1 = 64, 1016, 600, 1680
NL = 5; LH = (PY1 - PY0) / NL
LANEY = [PY0 + LH * (i + 0.5) for i in range(NL)]
XL, XR = 200, 880; LEN = XR - XL; TOT = 2 * LEN
T_GO = 3.2
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
    rnd = random.Random(seed)
    S = {n: dict(s=0.0, base=rnd.uniform(118, 134), ph=rnd.uniform(0, 6.3), fin=None, boost=None,
                 gs=rnd.uniform(200, TOT - 260)) for n in NAMES}
    frames = []; first = None; half_lead = None
    for f in range(int(40 * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= T_GO:
            for n, r in S.items():
                if r['fin'] is not None: continue
                sp = r['base'] * (1 + 0.16 * math.sin(0.9 * (t - T_GO) + r['ph']) + 0.07 * math.sin(2.7 * t + 2 * r['ph']))
                if r['boost'] is not None and t - r['boost'] < 1.7: sp *= 1.55
                if r['boost'] is None and r['s'] < r['gs'] <= r['s'] + sp * dt: r['boost'] = t
                r['s'] += sp * dt
                if r['s'] >= TOT: r['s'] = TOT; r['fin'] = t; first = first or (n, t)
            if half_lead is None and max(r['s'] for r in S.values()) >= LEN: half_lead = max(S, key=lambda n: S[n]['s'])
        frames.append({n: dict(s=r['s'], fin=r['fin'], boost=r['boost'], gs=r['gs']) for n, r in S.items()})
        if all(r['fin'] is not None for r in S.values()): break
    fins = sorted((r['fin'], n) for n, r in S.items())
    return frames, fins, half_lead
def score(seed):
    fr, fins, hl = sim(seed)
    gap = fins[1][0] - fins[0][0]
    if not (0.03 < gap < 0.2): return None
    if hl == fins[0][1]: return None
    if not (12.5 < fins[0][0] < 17.5): return None
    # lead changes
    lead = None; ch = 0
    for st in fr[int(T_GO * FPS):]:
        l = max(st, key=lambda n: st[n]['s'])
        if l != lead: ch += 1; lead = l
    if ch < 4: return None
    return round(fins[0][0], 2), fins[0][1], fins[1][1], round(gap, 3), ch
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, FINS, HL = sim(SEED)
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
def swimmer(img, n, s, t, moving):
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
    img.alpha_composite(fr2, (left, top))
    if moving:
        def splash(dd):
            rr = random.Random(int(t * 30) + i * 7)
            for k in range(10):
                sx = x - d * (fr.width * 0.45 + rr.uniform(0, 50)); sy = y + bob + rr.uniform(-14, 10)
                dd.rectangle([sx, sy, sx + 6, sy + 6], fill=(235, 250, 255, 220))
            dd.arc([x - fr.width / 2 - 10, y - 6, x + fr.width / 2 + 10, y + 26], 200, 340, fill=(220, 245, 255, 160), width=4)
        layer(img, splash)
W_ = Writer('d37_noaudio.mp4'); ev = []
HOLD = 1.4                                    # photo finish freeze
END = T_F + HOLD + 3.4
seen_boost = set(); seen_turn = set(); seen_fin = set()
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
    for n in NAMES:
        r = st[n]; moving = t_sim >= T_GO and r['fin'] is None
        swimmer(img, n, r['s'], t_anim, moving)
        if r['boost'] is not None and 0 <= t_sim - r['boost'] < 1.7:
            x, _ = xpos(r['s']); y = LANEY[NAMES.index(n)]
            u = t_sim - r['boost']
            if u < 1.0: text_layer(img, [(x, y - 110 - u * 30, 'SPEED UP!', 30, (255, 214, 60), 5, int(255 * min(1, (1 - u) / 0.3)))])
            layer(img, lambda d, x=x, y=y: [d.rectangle([x - 90 - k * 26, y - 30 + (k * 17) % 50, x - 50 - k * 26, y - 26 + (k * 17) % 50], fill=(255, 230, 140, 200)) for k in range(5)])
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
        if r['boost'] is not None and n not in seen_boost and t_sim >= r['boost']: seen_boost.add(n); ev.append((round(t, 3), 'powerup_8bit'))
        if r['s'] >= LEN and n not in seen_turn: seen_turn.add(n); ev.append((round(t, 3), 'swish'))
    if frozen:
        u = t - T_F
        # zoom on the finish wall around the two leaders
        ys = [LANEY[NAMES.index(win)], LANEY[NAMES.index(second)]]; cy = (ys[0] + ys[1]) / 2
        z = 1 + 0.9 * min(1, u / 0.35); cw, ch = W / z, H / z
        x0 = max(0, min(W - cw, 40)); y0 = max(0, min(H - ch, cy - ch / 2))
        img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.NEAREST)
        if u < 0.12: layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 255, 255, int(200 * (1 - u / 0.12)))))
        text_layer(img, [(W / 2, 330, 'PHOTO FINISH!', 72, (255, 255, 255), 9, 255)])
        if u > 0.6: text_layer(img, [(W / 2, 430, LABEL[win] + ' BY A HAIR', 44, (255, 214, 60), 7, 255)])
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_F, 3), 'ding_8bit'))
    # header
    layer(img, lambda d: d.rectangle([0, 0, W, 290], fill=(14, 10, 24, 190)))
    text_layer(img, [(W / 2, 46, 'CHOOSE YOUR', 64, (255, 255, 255), 7, 255), (W / 2, 128, 'CHAMPION', 76, (110, 200, 255), 8, 255), (W / 2, 220, 'Two lengths. First to touch wins.', 28, (230, 230, 230), 4, 255)])
    if t < T_GO:
        if t < 0.7: text_layer(img, [(W / 2, 410, 'PICK ONE!', 70, (255, 255, 255), 8, 255)])
        else:
            k = int((t - 0.7) / ((T_GO - 0.7) / 3)); text_layer(img, [(W / 2, 380, str(3 - k), 120, (255, 255, 255), 10, 255)])
            tk = 0.7 + k * (T_GO - 0.7) / 3
            if abs(t - tk) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    elif t < T_GO + 0.6:
        text_layer(img, [(W / 2, 380, 'GO!', 130, (255, 214, 60), 10, 255)])
        if not any(e[1] == 'go_8bit' for e in ev): ev.append((round(T_GO, 3), 'go_8bit'))
    if t >= T_F + HOLD:
        u = t - T_F - HOLD
        layer(img, lambda d: d.rectangle([0, 290, W, H], fill=(10, 8, 24, int(165 * min(1, u / 0.3)))))
        vf = VF[int(u * 8) % len(VF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1170 - vf.height))
        text_layer(img, [(W / 2, 1220, LABEL[win] + ' WINS!', 64, (255, 214, 60), 8, 255), (W / 2, 1320, 'Did your champion win?', 36, (255, 255, 255), 5, 255)])
        if not any(e[1] == 'victory' for e in ev): ev.append((round(t, 3), 'victory'))
    W_.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/c_{f:04d}.png')
W_.close()
json.dump(ev, open('d37_ev.json', 'w')); print('done', END)
