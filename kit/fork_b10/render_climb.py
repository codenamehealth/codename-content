import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
LANE_X = {n: 140 + i * 200 for i, n in enumerate(NAMES)}
CLIMB_D = 4700; GROUND = 6300; TOP_Y = GROUND - CLIMB_D; WH = GROUND + 250
T_GO = 2.6
# ---------------- sim
def sim(seed):
    rnd = random.Random(seed)
    cl = {}
    for n in NAMES:
        cl[n] = dict(y=float(GROUND), base=rnd.uniform(178, 205), ph=rnd.uniform(0, 6.3), boost=-9.0, stun=-9.0, fin=None, dist=0.0)
    slimes = []
    for n in NAMES:
        for k in range(rnd.choice([3, 4])):
            slimes.append(dict(lane=n, t0=rnd.uniform(4, 19), y=None, hit=None, done=False))
    gums = []
    for n in NAMES:
        hs = sorted(rnd.sample(range(700, CLIMB_D - 600, 150), 3))
        for h in hs: gums.append(dict(lane=n, y=GROUND - h, got=None))
    frames = []; events = []
    for f in range(int(40 * 30)):
        t = f / 30; dt = 1 / 30
        if t >= T_GO:
            ys = sorted(c['y'] for c in cl.values() if c['fin'] is None)
            lead = min(c['y'] for c in cl.values())
            for n, c in cl.items():
                if c['fin'] is not None: continue
                sp = c['base'] * (1 + 0.2 * math.sin(0.8 * t + c['ph']) + 0.1 * math.sin(2.1 * t + 2 * c['ph']))
                gap = c['y'] - lead
                if gap < 1: sp *= 0.95
                elif gap > 500: sp *= 1.08
                if t - c['boost'] < 1.4: sp *= 1.75
                if t - c['stun'] < 0.45: sp *= 0.0
                ny = c['y'] - sp * dt; c['dist'] += c['y'] - ny; c['y'] = ny
                for g in gums:
                    if g['lane'] == n and g['got'] is None and c['y'] <= g['y']:
                        g['got'] = t; c['boost'] = t; events.append((t, 'boost', n))
                if c['y'] <= TOP_Y:
                    c['y'] = TOP_Y; c['fin'] = t; events.append((t, 'fin', n))
            for s in slimes:
                if s['done'] or t < s['t0']: continue
                c = cl[s['lane']]
                if s['y'] is None: s['y'] = c['y'] - 1150
                s['y'] += 300 * dt
                if c['fin'] is None and s['hit'] is None and s['y'] >= c['y'] - 230:
                    s['hit'] = t; c['stun'] = t; events.append((t, 'pow', s['lane'])); s['done'] = True
                if s['y'] > GROUND: s['done'] = True
        frames.append({n: dict(y=c['y'], boost=c['boost'], stun=c['stun'], fin=c['fin'], dist=c['dist']) for n, c in cl.items()})
        if all(c['fin'] is not None for c in cl.values()) or (any(c['fin'] for c in cl.values()) and t > min(c['fin'] for c in cl.values() if c['fin']) + 3.4): break
    return frames, events, slimes, gums
def leaders(frames):
    out = []
    for fr in frames[int(T_GO * 30):]:
        n = min(NAMES, key=lambda k: fr[k]['y'])
        if not out or out[-1] != n: out.append(n)
    return out
def score(seed):
    fr, ev, sl, gm = sim(seed)
    fins = sorted((e[0], e[2]) for e in ev if e[1] == 'fin')
    if not fins: return None
    tw, win = fins[0]
    if not (19 < tw < 25): return None
    ld = leaders(fr)
    second = fr[-1]
    st_y = sorted(fr[int(tw * 30)][n]['y'] for n in NAMES)
    margin = st_y[1] - st_y[0]
    if margin > 260 or len(ld) < 5: return None
    return round(tw, 2), win, len(ld), round(margin)
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); WIN_WANT = None
FR, EV, SL, GM = sim(SEED)
fins = sorted((e[0], e[2]) for e in EV if e[1] == 'fin'); T_WIN, WIN = fins[0]
print('winner', WIN, round(T_WIN, 2), 'leaders', leaders(FR))
# ---------------- art
CLIMB = {g: seq(f'{g}_climb', 3, 1, 9) for g in NAMES}
if os.path.isdir('ray_climb2') and os.environ.get('RAY2', '1') == '1': CLIMB['ray'] = seq('ray_climb2', 3, 1, 9)
STAND = {g: seq(f'../pixellab/maze/anim/{g}_frun', 3, 0, 1)[0] for g in NAMES}
SL_IDLE = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob('../pixellab/race/slime_idle_c/*.png'))[1:]]
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
SL_IDLE = [nored(s) for s in SL_IDLE]
DUST = up(crop(Image.open('../pixellab/king/dust_cands/00.png').convert('RGBA')), 1)
STALK = crop(Image.open(sorted(glob.glob('stalk/*.png'))[int(os.environ.get('STALK', '2'))]).convert('RGBA').crop((0, 0, 64, 142)))
STALK = up(STALK, 2)
CLOUDS = [crop(Image.open(p).convert('RGBA')) for p in sorted(glob.glob('cloud/*.png'))[:8]]
CTOP = crop(Image.open(sorted(glob.glob('cloudtop/*.png'))[int(os.environ.get('CTOP', '0'))]).convert('RGBA'))
GUM = {n: gummy(GK[n], 3) for n in NAMES}
ICON = {}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 30) for n in NAMES}
# world background: sky gradient bottom->top, clouds, vines
rng = random.Random(3)
SKY = np.zeros((WH, W, 3), np.uint8)
cols = [(0, (255, 214, 150)), (0.12, (255, 190, 170)), (0.35, (150, 190, 255)), (0.75, (120, 200, 255)), (1.0, (170, 225, 255))]
for y in range(WH):
    u = 1 - y / WH
    for k in range(len(cols) - 1):
        if cols[k][0] <= u <= cols[k + 1][0]:
            a = (u - cols[k][0]) / (cols[k + 1][0] - cols[k][0]); c = [int(cols[k][1][i] * (1 - a) + cols[k + 1][1][i] * a) for i in range(3)]; break
    SKY[y] = c
WORLD = Image.fromarray(SKY).convert('RGBA')
for k in range(42):
    c = rng.choice(CLOUDS); s = rng.choice([3, 4, 5]); c2 = up(c, s)
    a = c2.getchannel('A').point(lambda p: int(p * 0.85)); c2.putalpha(a)
    WORLD.alpha_composite(c2, (rng.randint(-150, W - 100), rng.randint(200, GROUND - 1700)))
for n in NAMES:
    x = LANE_X[n]
    y = GROUND + 60; k = 0
    while y > TOP_Y + 60:
        seg = STALK if k % 2 == 0 else STALK.transpose(Image.FLIP_LEFT_RIGHT)
        WORLD.alpha_composite(seg, (int(x - seg.width / 2), int(y - seg.height))); y -= seg.height - 4; k += 1
# cloud layer at the top
for k in range(7):
    c = up(CTOP, 4)
    WORLD.alpha_composite(c, (k * 170 - 160 + (k % 2) * 40, TOP_Y - c.height // 2 - 40 + (k % 3) * 18))
FOREST = bg_frames('found_hd.gif', (int(1920 * 1.0), 1080), step=2)
FOREST = [f.crop((420, 0, 420 + 1080, 1080)) for f in FOREST]
FADE = Image.fromarray(np.tile(np.clip(np.arange(1080) * 255 // 320, 0, 255).astype(np.uint8)[:, None], (1, W)), 'L')
# ---------------- render
END = T_WIN + 3.4; NF = int(END * 30)
wr = Writer('climb_noaudio.mp4'); out_ev = []; cam = GROUND - H + 120
def scr(y): return int(y - cam)
VICF = vic(WIN, 340)
for f in range(NF):
    t = f / 30; st = FR[min(f, len(FR) - 1)]
    lead_y = min(st[n]['y'] for n in NAMES)
    ys_ = sorted(st[n]['y'] for n in NAMES)
    target = min(lead_y - 520, (ys_[0] + ys_[2]) / 2 - 1000) if t >= T_GO else GROUND - H + 120
    target = max(TOP_Y - 640, min(GROUND - H + 120, target))
    cam += (target - cam) * 0.08
    img = WORLD.crop((0, int(cam), W, int(cam) + H)).copy()
    # forest at the bottom (animated)
    fy = scr(GROUND - 900)
    if fy < H:
        fo = FOREST[int(t * 6) % len(FOREST)].copy()
        fo.putalpha(FADE)
        img.alpha_composite(fo, (0, fy))
        # redraw vines over forest
        for n in NAMES:
            x = LANE_X[n]; y = GROUND + 60; k = 0
            while y > GROUND - 1100:
                seg = STALK if k % 2 == 0 else STALK.transpose(Image.FLIP_LEFT_RIGHT)
                img.alpha_composite(seg, (int(x - seg.width / 2), scr(y - seg.height))); y -= seg.height - 4; k += 1
    # gummies on the vines
    for g in GM:
        if g['got'] is not None and t >= g['got']:
            u = t - g['got']
            if u < 0.5:
                for q in range(8):
                    a = q * 0.785; rr = 20 + 120 * u
                    sx, sy = LANE_X[g['lane']] + rr * math.cos(a), scr(g['y'] - 80) + rr * math.sin(a)
                    layer(img, lambda d: d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 230, 140, int(255 * (1 - u / 0.5)))))
            continue
        gs = GUM[g['lane']]; bob = int(5 * math.sin(t * 4 + g['y']))
        gx, gy = LANE_X[g['lane']], scr(g['y'] - 90) + bob
        if -100 < gy < H + 100:
            layer(img, lambda d: d.ellipse([gx - 42, gy - 42, gx + 42, gy + 42], fill=(255, 240, 180, 90)))
            img.alpha_composite(gs, (int(gx - gs.width / 2), int(gy - gs.height / 2)))
    # slimes sliding down
    for s in SL:
        if s['t0'] > t or s['y'] is None: continue
    # recompute slime positions for this frame from sim timing
    for s in SL:
        if t < s['t0']: continue
        c0 = FR[min(int(s['t0'] * 30), len(FR) - 1)][s['lane']]['y'] - 1150
        sy = c0 + 300 * (t - s['t0'])
        if s['hit'] is not None and t >= s['hit']:
            u = t - s['hit']
            if u < 0.4:
                du = up(DUST, 1); al = du.getchannel('A').point(lambda p, u=u: int(p * (1 - u / 0.4))); du.putalpha(al)
                img.alpha_composite(du, (LANE_X[s['lane']] - du.width // 2, scr(sy) - du.height // 2))
            continue
        if sy > GROUND: continue
        sp = SL_IDLE[int(t * 10) % len(SL_IDLE)]
        img.alpha_composite(sp, (LANE_X[s['lane']] - sp.width // 2, scr(sy) - sp.height + 20))
    # climbers
    for n in NAMES:
        c = st[n]; x = LANE_X[n]; y = c['y']
        if t < T_GO: spr = STAND[n]; yy = GROUND
        else:
            ph = int(c['dist'] / 26) % 8; spr = CLIMB[n][ph]; yy = y
        if c['fin'] is not None and t >= c['fin']:
            spr = STAND[n] if n != WIN else STAND[n]; yy = TOP_Y - 40
        if t < T_GO or (c['fin'] is not None and t >= c['fin']): sx, sy = int(x - 30 - spr.width / 2), scr(yy) - 234
        else: sx, sy = int(x - 165), scr(yy) - 249
        if c['boost'] > 0 and 0 <= t - c['boost'] < 1.4 and c['fin'] is None:
            for q in range(3):
                gy = sy + 40 + q * 40
                layer(img, lambda d: d.rectangle([x - 30, gy + 60 + (int(t * 30) * 7 + q * 13) % 40, x - 24, gy + 90 + (int(t * 30) * 7 + q * 13) % 40], fill=(255, 220, 120, 160)))
        img.alpha_composite(spr, (sx, sy))
        if c['stun'] > 0 and 0 <= t - c['stun'] < 0.45:
            u = t - c['stun']
            layer(img, lambda d: d.arc([x - 20, sy - 30, x + 100, sy + 90], 200, 340, fill=(255, 255, 255, int(255 * (1 - u / 0.45))), width=8))
    # popups
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for (te, kind, n) in EV:
        u = t - te
        if 0 <= u < 0.9:
            y = scr(FR[min(int(te * 30), len(FR) - 1)][n]['y']) - 200 - u * 60; a = int(255 * min(1, (0.9 - u) / 0.3))
            if kind == 'boost': ctext(d, LANE_X[n] + 20, y, 'BOOST!', F(30), (255, 214, 60), 5, a)
            elif kind == 'pow': ctext(d, LANE_X[n] + 40, y, 'POW!', F(34), (255, 255, 255), 6, a)
        if abs(t - te) < 0.5 / 30:
            out_ev.append((round(te, 3), {'boost': 'powerup_8bit', 'pow': 'sword_hit', 'fin': 'ding_8bit'}[kind]))
    img.alpha_composite(L)
    # header
    layer(img, lambda d: d.rectangle([0, 0, W, 330], fill=(14, 10, 24, 175)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 34, 'CHOOSE YOUR GUIDE!', F(54)); ctext(d, W / 2, 112, 'FIRST TO THE TOP WINS', F(36), (255, 214, 60), 5)
    order = sorted(NAMES, key=lambda n: (st[n]['fin'] if st[n]['fin'] else 99, st[n]['y']))
    for i, n in enumerate(NAMES):
        ix = 108 + i * 216; ic = ICON[n]
        img.alpha_composite(ic, (ix - ic.width // 2, 180))
        pct = int(100 * min(1, (GROUND - st[n]['y']) / CLIMB_D))
        d = ImageDraw.Draw(img); ctext(d, ix, 262, f'{pct}%', F(26), RING[n] if n != 'hollow' else (220, 215, 235), 4)
        if order[0] == n and t >= T_GO:
            ctext(d, ix, 150, '1ST', F(22), (255, 214, 60), 4)
    if t < T_GO:
        k = 3 - int(t / (T_GO / 3)) if t < T_GO else 0
        ctext(d, W / 2, 760, str(max(1, k)), F(140), (255, 90, 90), 10)
        ctext(d, W / 2, 950, 'PICK ONE!', F(54), (255, 255, 255), 8)
        if f == 0: out_ev += [(0.0, 'tick_8bit'), (round(T_GO / 3, 3), 'tick_8bit'), (round(2 * T_GO / 3, 3), 'tick_8bit')]
    elif t < T_GO + 0.6:
        ctext(d, W / 2, 760, 'GO!', F(140), (120, 255, 120), 10)
        if not any(e[1] == 'go_8bit' for e in out_ev): out_ev.append((round(T_GO, 3), 'go_8bit'))
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, 330, W, H], fill=(8, 6, 14, int(130 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, W / 2, 1230, LABEL[WIN] + ' WINS!', F(64), (255, 214, 60), 8)
        rr = random.Random(f)
        for _ in range(40):
            cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H
            if cy_ > 330: d.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120)]))
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN, 3), 'victory'))
    wr.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/c_{f:04d}.png')
wr.close() if hasattr(wr, 'close') else (wr.p.stdin.close(), wr.p.wait())
json.dump({'events': out_ev}, open('climb_events.json', 'w'))
print('done', round(END, 2))
