import sys, os, math, random, json
sys.path.insert(0, '../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SS = 2; FOOT = 78 * SS
SRUN = {g: seq(PL + f'race/{g}_run', SS) for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq(PL + 'maze/anim/hollow_srun', SS)
SLIDE = {g: seq(PL + f'maze/anim/{g}_slide', SS, 1, 8) for g in NAMES}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SS) for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', SS, 0, 1)[0] for g in NAMES}
FL = lambda L: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in L]
SRUNL = {g: FL(v) for g, v in SRUN.items()}; SLIDEL = {g: FL(v) for g, v in SLIDE.items()}
# --- scene
BG = up(Image.open('mountain_b/00.png').convert('RGBA'), 3)
BG = ImageEnhance.Brightness(BG).enhance(0.8)
LEDGE = up(crop(Image.open('ledge/00.png').convert('RGBA')), 2)            # 318 x 70
STAIR = up(crop(Image.open('stair/00.png').convert('RGBA')), 2)            # ~56
DR = gif_frames(A + 'dragon.gif'); DR = [f.resize((300, 300), Image.NEAREST) for f in DR]
GUM = gummy('mush', 3)
# switchback course: levels from bottom
LEVY = [1740, 1470, 1200, 930, 660]
XL, XR = 150, 930
def build_path():
    pts = []
    for k, y in enumerate(LEVY):
        a, b = (XL, XR) if k % 2 == 0 else (XR, XL)
        if k == 0: pts.append((a, y))
        pts.append((b, y))
        if k < len(LEVY) - 1:
            # stairs climbing up and back inward 130px
            ny = LEVY[k + 1]; sx = b + (-130 if b == XR else 130)
            pts.append((sx, ny))
    return pts
PTS = build_path()
# the top level ends at the hoard: shorten final segment to the dragon
PTS[-1] = (XL + 260, LEVY[-1])
SEG = []; acc = 0
for i in range(len(PTS) - 1):
    (x0, y0), (x1, y1) = PTS[i], PTS[i + 1]; L = math.hypot(x1 - x0, y1 - y0)
    SEG.append((acc, L, x0, y0, x1, y1)); acc += L
TOTAL = acc
def pos(s):
    s = max(0, min(TOTAL, s))
    for a, L, x0, y0, x1, y1 in SEG:
        if s <= a + L: u = (s - a) / L; return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, (1 if x1 > x0 else -1), abs(y1 - y0) > 1
    a, L, x0, y0, x1, y1 = SEG[-1]; return x1, y1, (1 if x1 > x0 else -1), False
def s_at(level, x):
    for a, L, x0, y0, x1, y1 in SEG:
        if y0 == y1 == LEVY[level] and min(x0, x1) <= x <= max(x0, x1): return a + abs(x - x0)
    return None
# gummy on level 2 near its start
GUM_LEV = int(os.environ.get('GL', '1'))
GUM_S = s_at(GUM_LEV, int(os.environ.get('GX', '540')))
T_DROP = float(os.environ.get('TD', '7.0'))
T_GO = 3.0; T_DARK = 4.4; DA, DB = float(os.environ.get('DA', '62')), float(os.environ.get('DB', '3.2'))
def dark_y(t):
    if t < T_DARK: return 1990
    u = t - T_DARK; return 1990 - (DA * u + DB * u * u)
def sim(seed):
    rnd = random.Random(seed)
    R = {}
    order = list(range(5)); rnd.shuffle(order)
    for i, n in enumerate(NAMES):
        R[n] = dict(s=-order[i] * 46.0, base=rnd.uniform(285, 345), ph=rnd.uniform(0, 6.3), out=None, win=None, slide=-9, jump=None, gum=False)
    frames = []; gum_by = None; winner = None
    for f in range(int(30 * FPS)):
        t = f / FPS; dt = 1 / FPS; dy = dark_y(t)
        for n, r in R.items():
            if r['out'] is not None or r['win'] is not None or t < T_GO: continue
            if r['jump'] is not None:
                j = r['jump']; u = (t - j['t0']) / 0.75
                if u >= 1: r['s'] = j['s1']; r['jump'] = None
                continue
            sp = r['base'] * (1 + 0.22 * math.sin(1.1 * t + r['ph']) + 0.1 * math.sin(2.9 * t + r['ph'] * 2))
            x, y, d, st = pos(r['s'])
            if st: sp *= 0.72
            sliding = t - r['slide'] < 0.55
            if sliding: sp *= 1.35
            # blocked by someone just ahead on the path -> slide through them
            if not sliding and not st:
                for m, o in R.items():
                    if m != n and o['out'] is None and o['win'] is None and 0 < o['s'] - r['s'] < 38 and o['jump'] is None:
                        if t - r['slide'] > 1.2: r['slide'] = t
                        else: sp = min(sp, o['base'] * 0.95)
            r['s'] += sp * dt
            if gum_by is None and t >= T_DROP + 0.8 and r['s'] - sp * dt < GUM_S <= r['s']:
                gum_by = (n, t); r['gum'] = True
                x, y, _, _ = pos(r['s']); s1 = s_at(GUM_LEV + 1, x) or r['s'] + 300
                r['jump'] = dict(t0=t, x0=x, y0=y, s0=r['s'], s1=s1)
                r['behind'] = sum(1 for m, o in R.items() if m != n and o['s'] > r['s'])
            if r['s'] >= TOTAL: r['win'] = t; winner = winner or (n, t)
            x, y, _, _ = pos(r['s'])
            if dy < y - 26: r['out'] = t
        snap = {n: dict(r) for n, r in R.items()}
        for n in snap: snap[n]['jump'] = dict(R[n]['jump']) if R[n]['jump'] else None
        frames.append((snap, dy, gum_by))
        if winner and t > winner[1] + 3.3: break
    return frames, winner, gum_by, R
def score(seed):
    fr, win, gb, R = sim(seed)
    if not win or not gb: return None
    outs = sorted(r['out'] for r in R.values() if r['out'] is not None)
    wins = [n for n, r in R.items() if r['win'] is not None]
    if len(wins) != 1 or len(outs) != 4: return None
    if gb[0] != win[0] or R[win[0]].get('behind', 0) < 2: return None
    if not (12 < win[1] < 16.5) or outs[0] < 7.5 or len([o for o in outs if o <= win[1] + 0.3]) < 3 or outs[-1] > win[1] + 3.0: return None
    return round(win[1], 2), win[0], [round(o, 1) for o in outs], R[win[0]]['behind']
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, WIN, GB, RR = sim(SEED)
print('win', WIN, 'gum', GB, {n: (round(r['out'], 1) if r['out'] else None) for n, r in RR.items()})
win = WIN[0]; T_W = WIN[1]; END = T_W + 3.2
VF = vic(win, 340)
ICON = {}
for n in NAMES:
    from PIL import ImageDraw as _D
    src = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}[n]
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((60, 60), Image.NEAREST)
    b = Image.new('RGBA', (72, 72), (0, 0, 0, 0)); d = _D.Draw(b)
    d.ellipse([0, 0, 71, 71], fill=(20, 16, 30, 255)); d.ellipse([3, 3, 68, 68], fill=RING[n] + (255,)); d.ellipse([7, 7, 64, 64], fill=(235, 232, 220, 255))
    m = Image.new('L', (60, 60), 0); _D.Draw(m).ellipse([0, 0, 59, 59], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', (60, 60), (0, 0, 0, 0)), m).getchannel('A')); ICON[n] = b
# static course layer
COURSE = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for k, y in enumerate(LEVY):
    x0 = XL - 40; x1 = XR + 40
    if k == len(LEVY) - 1: x1 = XL + 420
    x = x0
    while x < x1: COURSE.alpha_composite(LEDGE, (int(x), y - 14)); x += LEDGE.width - 6
for i in range(len(PTS) - 1):
    (x0, y0), (x1, y1) = PTS[i], PTS[i + 1]
    if y0 != y1:
        n = 6
        for j in range(n):
            u = (j + 0.5) / n; sx = x0 + (x1 - x0) * u; sy = y0 + (y1 - y0) * u
            st = STAIR if x1 > x0 else STAIR.transpose(Image.FLIP_LEFT_RIGHT)
            COURSE.alpha_composite(st, (int(sx - st.width / 2), int(sy - 6)))
W_ = Writer('d35_noaudio.mp4'); ev = []
rng = random.Random(3)
SPARK = [(rng.uniform(0, W), rng.uniform(0, 1), rng.uniform(0.5, 1.5)) for _ in range(70)]
seen_out = set(); seen_slide = set()
for f in range(int(END * FPS)):
    t = f / FPS; st_, dy, gb = FR[min(f, len(FR) - 1)]
    img = BG.copy(); img.alpha_composite(COURSE)
    # dragon + hoard at the top
    df = DR[int(t * 5) % len(DR)]; img.alpha_composite(df, (XL + 240, LEVY[-1] - 250))
    for i, k in enumerate(['acv', 'mush', 'mel', 'cre', 'gold']):
        g = gummy(k, 2); img.alpha_composite(g, (XL + 300 + i * 44, LEVY[-1] - 34 - (i % 2) * 10))
    # gummy pickup on level 2
    if T_DROP <= t < T_DROP + 0.8:
        u = (t - T_DROP) / 0.8; gx0, gy0 = XL + 390, LEVY[-1] - 120; gx1, gy1, _, _ = pos(GUM_S)
        gx = gx0 + (gx1 - gx0) * u; gy = gy0 + (gy1 - 56 - gy0) * u - 260 * math.sin(math.pi * u)
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        if not any(e[1] == 'whoosh_8bit' for e in ev): ev.append((round(T_DROP, 3), 'whoosh_8bit'))
    if T_DROP <= t < T_DROP + 2.2:
        a_ = int(255 * min(1, (T_DROP + 2.2 - t) / 0.4)); text_layer(img, [(W / 2, 400, 'THE DRAGON DROPS A GUMMY!', 34, (255, 190, 80), 5, a_)])
    if t >= T_DROP + 0.8 and (gb is None or t < gb[1]):
        gx, gy, _, _ = pos(GUM_S); bob = int(8 * math.sin(t * 4))
        layer(img, lambda d: [d.ellipse([gx - 40 + q, gy - 96 + bob + q, gx + 40 - q, gy - 16 + bob - q], fill=(255, 200, 120, 30 + q * 3)) for q in range(0, 30, 6)])
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - 56 - GUM.height / 2 + bob)))
    # racers
    for n in sorted(NAMES, key=lambda n: pos(st_[n]['s'])[1]):
        r = st_[n]; x, y, d, stair = pos(r['s'])
        if r['win'] is not None: continue
        if r['jump'] is not None:
            j = r['jump']; u = min(1, (t - j['t0']) / 0.75); x1, y1, _, _ = pos(j['s1'])
            x = j['x0'] + (x1 - j['x0']) * u; y = j['y0'] + (y1 - j['y0']) * u - 210 * math.sin(math.pi * u)
            spr = (SRUN if d > 0 else SRUNL)[n][2]
            if not any(e[1] == 'powerup_8bit' for e in ev): ev.append((round(j['t0'], 3), 'powerup_8bit')); ev.append((round(j['t0'] + 0.05, 3), 'jump'))
        elif r['out'] is not None:
            spr = PANIC[n][int(t * 12) % 8]
            if n not in seen_out: seen_out.add(n); ev.append((round(t, 3), 'poof'))
        elif t < T_GO: spr = STAND[n]
        elif t - r['slide'] < 0.55:
            k = min(6, int((t - r['slide']) / 0.55 * 7)); spr = (SLIDE if d > 0 else SLIDEL)[n][k]
            if (n, r['slide']) not in seen_slide: seen_slide.add((n, r['slide'])); ev.append((round(t, 3), 'swish'))
        else:
            ph = int(r['s'] / 22) % 8; spr = (SRUN if d > 0 else SRUNL)[n][ph]
        if r['out'] is not None:
            # caught: fade into the shadow
            a = max(0, 1 - (t - r['out']) / 1.2)
            if a <= 0: continue
            s2 = spr.copy(); s2.putalpha(s2.getchannel('A').point(lambda p: int(p * a)))
            tint = Image.new('RGBA', s2.size, (60, 30, 90, 0)); tint.putalpha(s2.getchannel('A').point(lambda p: int(p * 0.5)))
            s2.alpha_composite(tint); spr = s2
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if r['gum'] and r['jump'] is not None:
            u = t - r['jump']['t0']
            text_layer(img, [(x, y - FOOT - 40, 'SUPER JUMP!', 34, (255, 190, 80), 5, 255)])
    # rising dark: purple shadow with a wavy top and sparkles
    if dy < 1990:
        def dark(d):
            pts = [(0, H)] + [(xx, dy + 14 * math.sin(xx / 70 + t * 3) + 8 * math.sin(xx / 23 - t * 5)) for xx in range(0, W + 20, 20)] + [(W, H)]
            d.polygon(pts, fill=(28, 10, 48, 235))
            pts2 = [(xx, dy + 14 * math.sin(xx / 70 + t * 3) + 8 * math.sin(xx / 23 - t * 5)) for xx in range(0, W + 20, 20)]
            d.line(pts2, fill=(170, 110, 255, 255), width=6)
            for (sx, sy, sp) in SPARK:
                yy = dy + 40 + ((sy + t * 0.05 * sp) % 1) * (H - dy)
                if yy > dy + 20: d.rectangle([sx, yy, sx + 4, yy + 4], fill=(200, 160, 255, 200))
            for q in range(6):
                ex = (q * 197 + t * 30) % W; ey = dy + 120 + (q % 3) * 140
                if ey < H - 20: d.ellipse([ex, ey, ex + 10, ey + 10], fill=(255, 255, 255, 230)); d.ellipse([ex + 22, ey, ex + 32, ey + 10], fill=(255, 255, 255, 230))
        layer(img, dark)
    # header
    layer(img, lambda d: d.rectangle([0, 0, W, 330], fill=(14, 10, 24, 200)))
    items = [(W / 2, 40, 'PICK A GUIDE', 64, (255, 255, 255), 7, 255), (W / 2, 124, 'BEFORE THE DARK RISES', 44, (190, 140, 255), 6, 255)]
    text_layer(img, items)
    d = ImageDraw.Draw(img)
    for i, n in enumerate(NAMES):
        ix = W / 2 + (i - 2) * 180; iy = 250; ic = ICON[n]; r = st_[n]
        if r['out'] is not None: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(ix - 36), int(iy - 36)))
        d = ImageDraw.Draw(img)
        if r['out'] is not None:
            d.line([ix - 26, iy - 26, ix + 26, iy + 26], fill=(230, 50, 50), width=9); d.line([ix - 26, iy + 26, ix + 26, iy - 26], fill=(230, 50, 50), width=9)
        if r['gum'] and r['out'] is None: img.alpha_composite(gummy('mush', 1), (int(ix + 18), int(iy + 12)))
    if t < T_GO:
        c = 3 - int(t); text_layer(img, [(W / 2, 820, str(c) if t > 0.6 else 'PICK ONE!', 120 if t > 0.6 else 70, (255, 255, 255), 9, 255)])
        if t > 0.6 and abs(t - round(t)) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    elif t < T_GO + 0.6:
        text_layer(img, [(W / 2, 820, 'GO!', 130, (255, 214, 60), 10, 255)])
        if not any(e[1] == 'go_8bit' for e in ev): ev.append((round(T_GO, 3), 'go_8bit'))
    if t >= T_W:
        u = t - T_W; layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 6, 20, int(160 * min(1, u / 0.3)))))
        vf = VF[int(u * 8) % len(VF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        text_layer(img, [(W / 2, 1230, LABEL[win] + ' WINS!', 62, (255, 214, 60), 8, 255), (W / 2, 1330, 'Did your guide make it?', 34, (255, 255, 255), 5, 255)])
        if not any(e[1] == 'victory' for e in ev): ev.append((round(T_W, 3), 'victory'))
    W_.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/a_{f:04d}.png')
W_.close()
json.dump(ev, open('d35_ev.json', 'w')); print('done', END)
