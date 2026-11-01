import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
from PIL import Image, ImageDraw, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
VY0 = 380; VH = H - VY0
Y_START, Y_F = 520, 5900
WORLD_H = Y_F + 1500
def cx(y): return 540 + 170 * math.sin(y / 820) + 70 * math.sin(y / 330 + 1.3)
HW = 300
def sim(seed, dur=40):
    rnd = random.Random(seed)
    obs = []; y = 1000; kinds = ['rock', 'pool', 'gum', 'rock', 'gum', 'pool']; i = 0
    while y < Y_F - 250:
        k = kinds[i % len(kinds)]; i += 1
        if k == 'rock':
            for _ in range(rnd.choice([1, 2])): obs.append(['rock', y + rnd.uniform(-40, 40), rnd.uniform(-170, 170), 0])
        elif k == 'pool': obs.append(['pool', y, rnd.uniform(-140, 140), 0])
        else:
            g = rnd.choice(['acv', 'mush', 'cre', 'mel', 'gold']); obs.append(['gum', y, rnd.choice([-1, 1]) * rnd.uniform(110, 210), g])
        y += rnd.uniform(330, 470)
    R = {}
    offs = [-200, -100, 0, 100, 200]; rnd.shuffle(offs)
    for k, n in enumerate(NAMES):
        R[n] = dict(y=Y_START, x=cx(Y_START) + offs[k], off=offs[k] * 0.8, pad=rnd.uniform(78, 105), ph=rnd.uniform(0, 6.3),
                    boost=-9, dizzy=-9, bonk=-9, imm=-9, fin=None, greedy=rnd.random() < 0.6)
    frames = []; events = []; T_GO = 2.4; leaders = []; taken = set()
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= T_GO:
            for n, s in R.items():
                if s['fin'] is not None:
                    s['y'] += 120 * dt; continue
                c = cx(s['y']); tgt = c + s['off'] + 60 * math.sin(t * 0.7 + s['ph'])
                if s['greedy']:
                    for j, o in enumerate(obs):
                        if o[0] == 'gum' and j not in taken and 0 < o[1] - s['y'] < 520: tgt = cx(o[1]) + o[2]; break
                s['x'] += (tgt - s['x']) * 0.035
                s['x'] = max(c - HW + 75, min(c + HW - 75, s['x']))
                sp = 205 + s['pad'] * (1 + 0.3 * math.sin(t * 1.1 + s['ph']))
                if t - s['boost'] < 1.6: sp *= 1.75
                if t - s['dizzy'] < 1.3: sp *= 0.12
                if t - s['bonk'] < 0.35: sp = -70
                s['y'] += sp * dt
                for j, o in enumerate(obs):
                    ox, oy = cx(o[1]) + o[2], o[1]
                    dd = math.hypot(s['x'] - ox, (s['y'] - oy) * 0.9)
                    if o[0] == 'rock' and dd < 82 and t - s['bonk'] > 0.8:
                        s['bonk'] = t; s['x'] += 30 if s['x'] > ox else -30; events.append((t, 'bonk', n))
                    elif o[0] == 'pool' and dd < 80 and t - s['imm'] > 2.4:
                        s['dizzy'] = t; s['imm'] = t; events.append((t, 'dizzy', n))
                    elif o[0] == 'gum' and dd < 78 and j not in taken:
                        taken.add(j); s['boost'] = t; events.append((t, 'zoom', n))
                for m, o in R.items():
                    if m == n: continue
                    if abs(s['y'] - o['y']) < 125 and abs(s['x'] - o['x']) < 140:
                        s['x'] += 7 if s['x'] >= o['x'] else -7
                        if abs(s['x'] - o['x']) < 60 and s['y'] < o['y']: s['y'] -= 2
                if s['y'] >= Y_F: s['fin'] = t; events.append((t, 'fin', n))
            live = [n for n in NAMES]
            ld = max(live, key=lambda n: R[n]['y'] if R[n]['fin'] is None else 1e9 - R[n]['fin'])
            if not leaders or leaders[-1] != ld: leaders.append(ld)
        frames.append(({n: dict(x=s['x'], y=s['y'], boost=s['boost'], dizzy=s['dizzy'], bonk=s['bonk'], fin=s['fin']) for n, s in R.items()}, set(taken)))
        if all(s['fin'] is not None for s in R.values()) and t > max(s['fin'] for s in R.values()) + 4: break
    return frames, events, obs, leaders, {n: R[n]['fin'] for n in NAMES}
def score(seed):
    fr, ev, obs, ld, fin = sim(seed)
    if any(v is None for v in fin.values()): return None
    order = sorted(NAMES, key=lambda n: fin[n]); w = order[0]
    if w == 'hollow' or w == 'cyrus': return None
    tw = fin[w]
    if not (17 < tw < 23): return None
    if fin[order[1]] - tw > 0.6 or len(ld) < 5: return None
    nz = sum(1 for e in ev if e[1] == 'zoom'); nd = sum(1 for e in ev if e[1] == 'dizzy'); nb = sum(1 for e in ev if e[1] == 'bonk')
    if nz < 3 or nd < 2 or nb < 2: return None
    return round(tw, 2), w, order, len(ld), nz, nd, nb
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EVS, OBS, LEAD, FIN = sim(SEED)
ORDER = sorted(NAMES, key=lambda n: FIN[n]); WIN = ORDER[0]; T_WIN = FIN[WIN]
print('order', ORDER, {n: round(FIN[n], 2) for n in NAMES}, 'leaders', LEAD)
# ---------------- world
meta = json.load(open('river_meta.json')); sheet = Image.open('river_sheet.png').convert('RGBA')
TILE = {}
for t in meta['tileset_data']['tiles']:
    c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
TS = 64; GC = 18; GR = WORLD_H // TS + 1
def low(i, j):
    x, y = i * TS - 20, j * TS
    return abs(x - cx(y)) < HW + 10
WORLD = Image.new('RGBA', (W, GR * TS), (40, 90, 40, 255))
for j in range(GR):
    for i in range(GC):
        key = (low(i, j), low(i + 1, j), low(i, j + 1), low(i + 1, j + 1)); tl = TILE[key]
        if all(key) or not any(key):
            if (i * 5 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        WORLD.alpha_composite(tl, (i * TS - 20, j * TS))
rr = random.Random(7)
TREES = [up(crop(Image.open(p).convert('RGBA')), 1.5) for p in sorted(glob.glob(SP + 'fork2/bigtree/*.png'))]
LILY = [up(crop(Image.open(p).convert('RGBA')), 2) for p in sorted(glob.glob(SP + 'fork4/lilypad/*.png'))]
ROCKS = [up(crop(Image.open(f'rock/{i:02d}.png').convert('RGBA')), 3) for i in (5, 10, 0, 23)]
BANKROCK = [up(crop(Image.open(f'rock/{i:02d}.png').convert('RGBA')), 2) for i in (6, 12, 16, 22)]
for y in range(0, GR * TS, 150):
    c = cx(y)
    for side in (-1, 1):
        if rr.random() < 0.75:
            x = c + side * (HW + rr.uniform(150, 330))
            if 0 < x < W:
                tr = rr.choice(TREES) if rr.random() < 0.6 else rr.choice(BANKROCK)
                WORLD.alpha_composite(tr, (int(x - tr.width / 2), int(y - tr.height / 2)))
for y in range(300, GR * TS, 260):
    c = cx(y); x = c + rr.choice([-1, 1]) * rr.uniform(HW - 60, HW - 20)
    lp = rr.choice(LILY); WORLD.alpha_composite(lp, (int(x - lp.width / 2), int(y)))
for o in OBS:
    if o[0] == 'rock':
        r_ = ROCKS[int(abs(o[2])) % len(ROCKS)]; x = cx(o[1]) + o[2]
        WORLD.alpha_composite(r_, (int(x - r_.width / 2), int(o[1] - r_.height / 2)))
wd = ImageDraw.Draw(WORLD)
for yy, lab in ((Y_START - 60, 'START'), (Y_F, 'FINISH')):
    c = cx(yy)
    for r_ in range(2):
        for k in range(int(2 * HW / 18) + 1):
            x = c - HW + k * 18; col = (245, 245, 245, 255) if (k + r_) % 2 == 0 else (25, 22, 30, 255)
            wd.rectangle([x, yy + r_ * 18, x + 17, yy + r_ * 18 + 17], fill=col)
DOCK = up(crop(Image.open('dock/03.png').convert('RGBA')), 3)
for side in (-1, 1):
    x = cx(Y_F) + side * (HW + 40); WORLD.alpha_composite(DOCK, (int(x - DOCK.width / 2), int(Y_F - DOCK.height + 40)))
# ---------------- sprites
BARREL = up(crop(Image.open('barrel/02.png').convert('RGBA')), 3)
FRONT = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
UPPER = {}
for n, p in FRONT.items():
    im = Image.open(SP + 'syeda_src/' + p).convert('RGBA'); bb = im.getbbox()
    UPPER[n] = up(im.crop((bb[0] - 4, 10, bb[2] + 4, 58)), 2)
GUM = {k: gummy(k, 3) for k in GUMK}
VICF = vic(WIN, 340)
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
ICON = {n: face(n, 32) for n in NAMES}; ICS = {n: face(n, 22) for n in NAMES}
HDR = bg_frames('found_hd.gif', (W, VY0), box=(0, 120, 1920, 120 + 675), step=2, bright=0.6)
def boat(n, x, y, t, s):
    """barrel with the guide sitting in it, centered at x,y (screen)"""
    B = Image.new('RGBA', (220, 260), (0, 0, 0, 0))
    bx, by = 110 - BARREL.width // 2, 150 - BARREL.height // 2
    B.alpha_composite(BARREL, (bx, by))
    u = UPPER[n]; bob = int(3 * math.sin(t * 6 + x * 0.01))
    B.alpha_composite(u, (110 - u.width // 2, 150 - u.height + 10 + bob))
    front = BARREL.crop((0, int(BARREL.height * 0.55), BARREL.width, BARREL.height))
    B.alpha_composite(front, (bx, by + int(BARREL.height * 0.55)))
    d = ImageDraw.Draw(B)
    side = 1 if int(t * 2.6 + hash(n) % 7) % 2 else -1
    ph = (t * 2.6) % 1.0
    ox0, oy0 = 110 + side * 26, 130 + bob
    ox1, oy1 = 110 + side * (78 + 16 * math.sin(ph * math.pi)), 120 + 70 * ph
    d.line([ox0, oy0, ox1, oy1], fill=(120, 80, 40, 255), width=6)
    d.ellipse([ox1 - 9, oy1 - 5, ox1 + 9, oy1 + 13], fill=(150, 100, 50, 255), outline=(70, 45, 20, 255), width=2)
    if t - s['dizzy'] < 1.3:
        B = B.rotate(((t - s['dizzy']) * 720) % 360, resample=Image.NEAREST, center=(110, 150))
    return B
EV = []
def ev(t, name): EV.append((round(t, 3), name))
for tt in (0.6, 1.2, 1.8): ev(tt, 'tick_8bit')
ev(2.4, 'go_8bit'); ev(2.45, 'cheer')
for (t, k, n) in EVS:
    if t > T_WIN + 3.5: continue
    ev(t, {'bonk': 'stomp_8bit', 'dizzy': 'whoosh_8bit', 'zoom': 'powerup_8bit', 'fin': 'ding_8bit'}[k])
ev(T_WIN, 'victory')
T_END = T_WIN + 4.0; NF = int(T_END * FPS)
cam = 0.0
wr = Writer('v56_noaudio.mp4')
FX = []
for (t, k, n) in EVS: FX.append((t, k, n))
for f in range(NF):
    t = f / FPS; st, taken = FR[min(f, len(FR) - 1)]
    racing = [n for n in NAMES]
    lead_y = max(st[n]['y'] for n in NAMES)
    tgt = max(0, min(WORLD.height - VH, lead_y - VH * 0.62))
    cam = tgt if f == 0 else cam + (tgt - cam) * 0.12
    view = WORLD.crop((0, int(cam), W, int(cam) + VH))
    img = Image.new('RGBA', (W, H), (20, 40, 20, 255)); img.alpha_composite(view, (0, VY0))
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    # whirlpools
    for o in OBS:
        if o[0] != 'pool': continue
        sx, sy = cx(o[1]) + o[2], o[1] - cam + VY0
        if not (VY0 - 150 < sy < H + 150): continue
        for r_ in range(6):
            rad = 20 + r_ * 14; a0 = (t * 220 + r_ * 40) % 360
            dl.arc([sx - rad, sy - rad * 0.7, sx + rad, sy + rad * 0.7], a0, a0 + 230, fill=(225, 245, 255, 200 - r_ * 22), width=5)
        dl.ellipse([sx - 14, sy - 9, sx + 14, sy + 9], fill=(20, 60, 110, 200))
    img.alpha_composite(L)
    # floating gummies
    for j, o in enumerate(OBS):
        if o[0] != 'gum' or j in taken: continue
        sx, sy = cx(o[1]) + o[2], o[1] - cam + VY0 + 6 * math.sin(t * 3 + j)
        if not (VY0 - 100 < sy < H + 100): continue
        layer(img, lambda dd: [dd.ellipse([sx - 46 + k_ * 8, sy - 34 + k_ * 6, sx + 46 - k_ * 8, sy + 34 - k_ * 6], fill=(255, 230, 140, 40 + k_ * 25)) for k_ in range(3)])
        g = GUM[o[3]]; img.alpha_composite(g, (int(sx - g.width / 2), int(sy - g.height / 2)))
    # racers
    off_top = []
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; sx, sy = s['x'], s['y'] - cam + VY0
        if sy < VY0 - 60: off_top.append(n); continue
        if sy > H + 150: continue
        L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        for k_ in range(6):
            wy = sy - 50 - k_ * 22; a = 200 - k_ * 32
            spread = 30 + k_ * 9
            dl.rectangle([sx - spread - 6, wy - 4, sx - spread + 6, wy + 4], fill=(240, 250, 255, a))
            dl.rectangle([sx + spread - 6, wy - 4, sx + spread + 6, wy + 4], fill=(240, 250, 255, a))
        if t - s['boost'] < 1.6:
            for k_ in range(5):
                lx = sx - 70 + k_ * 35; ly = sy - 120 - ((t * 600 + k_ * 50) % 160)
                dl.rectangle([lx - 3, ly, lx + 3, ly + 40], fill=(255, 220, 90, 200))
        img.alpha_composite(L)
        B = boat(n, sx, sy, t, s); img.alpha_composite(B, (int(sx - 110), int(sy - 150)))
        tag = ICS[n]; img.alpha_composite(tag, (int(sx + 50), int(sy + 30)))
    # effect texts
    items = []
    for (te, k, n) in FX:
        u = t - te
        if 0 <= u < 1.0:
            s = st[n]; sx, sy = s['x'], s['y'] - cam + VY0
            txt, col = {'bonk': ('BONK!', (255, 120, 90)), 'dizzy': ('DIZZY!', (150, 220, 255)), 'zoom': ('ZOOM!', (255, 214, 60)), 'fin': ('', (0, 0, 0))}[k]
            if txt and VY0 < sy < H: items.append((sx, sy - 190 - u * 50, txt, 34, col, 6, int(255 * min(1, (1 - u) / 0.3))))
    if items: text_layer(img, items)
    if t - 0 < 2.4:
        text_layer(img, [(W / 2, VY0 + 160, 'PICK YOUR CHAMPION!', 40, (255, 255, 255), 7, 255)])
        if t >= 0.6: text_layer(img, [(W / 2, VY0 + 600, str(max(1, 3 - int((t - 0.6) / 0.6))), 120, (255, 214, 60), 10, 255)])
    elif t < 3.0:
        text_layer(img, [(W / 2, VY0 + 600, 'PADDLE!', 100, (120, 220, 255), 10, int(255 * (1 - (t - 2.4) / 0.6)))])
    for k_, n in enumerate(off_top):
        ic = ICS[n]; x = int(max(30, min(W - 80, st[n]['x'])))
        img.alpha_composite(ic, (x - 23, VY0 + 14))
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda dd: dd.rectangle([0, 0, W, VY0], fill=(14, 10, 24, 70)))
    text_layer(img, [(W / 2, 30, 'CHOOSE YOUR', 58, (255, 255, 255), 7, 255), (W / 2, 112, 'CHAMPION!', 58, (120, 220, 255), 7, 255)])
    rank = sorted(NAMES, key=lambda n: (-(1e9 - st[n]['fin']) if st[n]['fin'] is not None else -st[n]['y']))
    layer(img, lambda dd: dd.rounded_rectangle([20, 205, W - 20, 362], 16, fill=(14, 10, 24, 190)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([20, 205, W - 20, 362], 16, outline=(120, 220, 255, 255), width=4)
    for i, n in enumerate(rank):
        x = 20 + (W - 40) * (i + 0.5) / 5; ic = ICON[n]; img.alpha_composite(ic, (int(x - ic.width / 2), 218))
        text_layer(img, [(x, 312, ['1ST', '2ND', '3RD', '4TH', '5TH'][i], 24, (255, 214, 60) if i == 0 else (230, 230, 230), 4, 255)])
    # ticker
    layer(img, lambda dd: dd.rounded_rectangle([24, H - 120, W - 24, H - 30], 16, fill=(14, 10, 24, 215)))
    d = ImageDraw.Draw(img); d.rounded_rectangle([24, H - 120, W - 24, H - 30], 16, outline=(120, 220, 255, 255), width=4)
    msg = 'PICK ONE!' if t < 2.4 else (LABEL[rank[0]] + ' IS IN FRONT' if t < T_WIN else LABEL[WIN] + ' WINS!')
    text_layer(img, [(W / 2, H - 90, msg, 30, (255, 255, 255), 4, 255)])
    if t >= T_WIN + 0.8:
        u = t - T_WIN - 0.8; a = min(1, u / 0.35)
        layer(img, lambda dd: dd.rectangle([0, VY0, W, H - 130], fill=(8, 10, 22, int(165 * a))))
        if a > 0.2:
            vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
            text_layer(img, [(W / 2, 1220, LABEL[WIN] + ' WINS!', 60, (255, 214, 60), 8, int(255 * a)),
                             (W / 2, 1320, 'Did your champion win?', 34, (255, 255, 255), 6, int(255 * a))])
            rr2 = random.Random(f); L = Image.new('RGBA', img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            for _ in range(40):
                x_, y_ = rr2.uniform(0, W), (rr2.uniform(0, H) + u * 400) % (H - 520) + VY0
                dl.rectangle([x_, y_, x_ + 10, y_ + 10], fill=rr2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]) + (255,))
            img.alpha_composite(L)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p56_{f:04d}.png')
wr.close()
json.dump(EV, open('v56_ev.json', 'w'))
print('done', round(T_END, 2), len(EV))
