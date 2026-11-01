import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '..'); from powers import *
TS = 64; HW = 196                         # path half width
Y0, YF = 260, 5300                        # start and finish (world y)
WH = YF + 900
def xc(y): return 478 + 215 * math.sin(2 * math.pi * (y - 200) / 1500)
def dxc(y): return 215 * 2 * math.pi / 1500 * math.cos(2 * math.pi * (y - 200) / 1500)
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
rr = random.Random(11)
OBST = []                                 # (y, lateral, kind)
y = 700
while y < YF - 250:
    for _ in range(rr.choice([1, 1, 2])):
        OBST.append((y + rr.uniform(-40, 40), rr.uniform(-130, 130), rr.choice(['slime', 'slime', 'crate', 'hay'])))
    y += rr.uniform(260, 380)
BOOST = [(1500, -60), (2900, 80), (4200, -90)]
BOOST_T, BOOST_K = 2.2, 1.5
SL = 0.5; T_START = 2.4; R = 40
def sim(seed, dur=26):
    rnd = random.Random(seed); order = NAMES[:]; rnd.shuffle(order)
    rc = {}
    for i, n in enumerate(order):
        rc[n] = dict(p=Y0, l=-120 + i * 80, vl=0.0, base=rnd.uniform(300, 335), ph=rnd.uniform(0, 6.3), pref=rnd.uniform(-100, 100), out=None,
                     slide=-9, boost=None, dist=0.0, sp=0.0, vx=0.0)
    taken = {}; frames = []; leaders = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        for n, s in rc.items():
            if s['out'] is not None or t < T_START:
                if s['out'] is not None: s['p'] += 120 * dt * max(0, 1 - (t - s['out']) * 1.5); s['sp'] = 0
                continue
            sliding = t - s['slide'] < SL
            sp = s['base'] * (1 + 0.22 * math.sin(0.9 * t + s['ph']) + 0.12 * math.sin(2.4 * t + 2 * s['ph']))
            if s['boost'] is not None and t - s['boost'] < BOOST_T: sp *= BOOST_K
            if sliding: sp *= 1.18
            if t > s.get('nextpref', 0): s['pref'] = rnd.uniform(-120, 120); s['nextpref'] = t + rnd.uniform(1.0, 2.2)
            if not sliding:
                # dodge obstacles a bit when there's room (but only by steering, never through)
                s['vl'] += ((s['pref'] - s['l']) * 1.2 - s['vl']) * 0.08
            s['l'] = max(-HW + 40, min(HW - 40, s['l'] + s['vl'] * dt))
            # blocked by an obstacle or a guide just ahead -> slide through
            if not sliding and t - s['slide'] > 0.9 and t > T_START + 0.5:
                block = any(0 < oy - s['p'] < 70 and abs(ol - s['l']) < 48 for oy, ol, k in OBST)
                if not block:
                    block = any(m != n and o['out'] is None and 0 < o['p'] - s['p'] < 46 and abs(o['l'] - s['l']) < 40 for m, o in rc.items())
                if block: s['slide'] = t; sliding = True
            if not sliding:
                hit = [(oy, ol) for oy, ol, k in OBST if -10 < oy - s['p'] < 40 and abs(ol - s['l']) < 48]
                if hit: sp *= 0.35
                for m, o in rc.items():
                    if m != n and o['out'] is None and 0 < o['p'] - s['p'] < 36 and abs(o['l'] - s['l']) < 36 and t - o['slide'] >= SL: sp = min(sp, o['sp'] * 0.95)
            s['sp'] = sp; s['p'] += sp * dt; s['dist'] += sp * dt
            s['vx'] = s['vl'] + dxc(s['p']) * sp
            for k, (by, bl) in enumerate(BOOST):
                if k not in taken and abs(by - s['p']) < 40 and abs(bl - s['l']) < 60: taken[k] = (n, t); s['boost'] = t
            if s['p'] >= YF: s['out'] = t
        rank = sorted(rc, key=lambda n: (-(1e6 - rc[n]['out']) if rc[n]['out'] is not None else -rc[n]['p']))
        if t > T_START + 1 and (not leaders or leaders[-1] != rank[0]): leaders.append(rank[0])
        frames.append(({n: dict(p=s['p'], l=s['l'], vx=s['vx'], out=s['out'], slide=s['slide'], sliding=t - s['slide'] < SL, boost=s['boost'], dist=s['dist']) for n, s in rc.items()}, rank, dict(taken)))
        if all(s['out'] is not None for s in rc.values()) and t > max(s['out'] for s in rc.values()) + 0.5: break
    return rc, frames, leaders
def score(seed):
    rc, fr, ld = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    if len(outs) < 2: return None
    t1, w = outs[0]; t2 = outs[1][0]
    if not (15 < t1 < 18.5) or t2 - t1 > 0.6 or len(ld) < 5: return None
    return round(t1, 2), w, round(t2 - t1, 2), len(ld), ld
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
RC, FR, LD = sim(SEED)
OUTS = sorted((s['out'], n) for n, s in RC.items() if s['out'] is not None); T_WIN, WIN = OUTS[0]
print('winner', WIN, round(T_WIN, 2), [(n, round(t, 2)) for t, n in OUTS], LD)
# ---------------- ground
T = {i: up(Image.open(f'../../pixellab/race/tiles/tile_{i}.png').convert('RGBA'), 2) for i in range(16)}
def dirt(x, y): return abs(x - xc(y)) < HW
GROUND = Image.new('RGBA', (W, WH), (40, 90, 40, 255))
for j in range(WH // TS + 1):
    for i in range(W // TS + 2):
        x0, y0 = i * TS - 24, j * TS
        nw, ne, sw, se = dirt(x0, y0), dirt(x0 + TS, y0), dirt(x0, y0 + TS), dirt(x0 + TS, y0 + TS)
        idx = 8 * nw + 4 * ne + 2 * sw + 1 * se
        tl = T[idx]
        if idx in (0, 15):
            if (i + j) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
            if (i * 3 + j) % 3 == 0: tl = tl.transpose(Image.FLIP_TOP_BOTTOM)
        GROUND.alpha_composite(tl, (x0, y0))
gd = ImageDraw.Draw(GROUND)
# wooden fences along both edges
for yy in range(0, WH, 6):
    for side in (-1, 1):
        x = xc(yy) + side * (HW + 26)
        if yy % 72 < 6: gd.rectangle([x - 6, yy - 30, x + 6, yy + 8], fill=(110, 70, 38), outline=(60, 36, 20))
        gd.rectangle([x - 3, yy - 22, x + 3, yy - 16], fill=(150, 98, 52)); gd.rectangle([x - 3, yy - 8, x + 3, yy - 2], fill=(150, 98, 52))
# grass decoration: flowers / pots from the plaza props
def pick(d, i): return crop(Image.open(f'../../pixellab/steal/{d}/{i:02d}.png').convert('RGBA'))
DEC = [up(pick('flowers', k), 2) for k in (1, 4, 7, 12, 16)] + [up(pick('barrel', 0), 2), up(pick('crate', 1), 2)]
for _ in range(42):
    yy = rr.uniform(0, WH); side = rr.choice([-1, 1]); x = xc(yy) + side * (HW + rr.uniform(110, 300))
    if 20 < x < W - 20:
        im = rr.choice(DEC); GROUND.alpha_composite(im, (int(x - im.width / 2), int(yy - im.height / 2)))
# start and finish lines
for xx in range(int(xc(YF) - HW), int(xc(YF) + HW), 28):
    for k in range(2):
        gd.rectangle([xx, YF - 28 + k * 28, xx + 27, YF - 1 + k * 28], fill=(245, 245, 245) if ((xx // 28) + k) % 2 else (25, 25, 30))
gd.rectangle([xc(Y0) - HW, Y0 - 3, xc(Y0) + HW, Y0 + 3], fill=(245, 245, 240))
SLM = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob('../../pixellab/race/slime_idle_c/*.png'))]
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int); a[(r > 140) & (g < 110) & (b < 140)] = 0; return Image.fromarray(a)
SLM = [nored(f) for f in SLM]
OBIM = {'crate': up(pick('crate', 1), 2), 'hay': up(pick('barrel', 0), 2)}
SS = 2; FOOT = 78 * SS
def seqa(d, lo=1, hi=9): return [up(Image.open(p).convert('RGBA'), SS) for p in sorted(glob.glob(d + '/*.png'))[lo:hi]]
SRUN = {g: seqa(f'../../pixellab/race/{g}_run') for g in ['joy', 'cyrus', 'cleo', 'ray']}; 
FRUN = {g: seqa(f'../../pixellab/maze/anim/{g}_frun') for g in NAMES}
SLIDE = {g: seqa(f'../../pixellab/maze/anim/{g}_slide', 1, 8) for g in NAMES}
STAND = {g: seqa(f'../../pixellab/maze/anim/{g}_frun', 0, 1)[0] for g in NAMES}
FLIP = lambda L: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in L]
SRUNL = {g: FLIP(v) for g, v in SRUN.items()}; SLIDEL = {g: FLIP(v) for g, v in SLIDE.items()}
MUSH = gummy('mush', 3)
SRCF = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
def face(name, rad):
    im = Image.open('../../syeda_src/' + SRCF[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255); b.paste(head, (6, 6), m); return b
ICON = {n: face(n, 36) for n in NAMES}
HOOK, HB = hook_layer(['CHOOSE YOUR', 'GUIDE'], accent=1)
CHIP_Y = HB + 6
HDR = bg_frames('found_hd.gif', (W, CHIP_Y + 102), box=(8, 0, 1912, 1080), step=2, bright=0.6)
print('hook bottom', HB)
VICF = vic(WIN, 360)
BY = CHIP_Y + 102; VH = 1500 - BY
print('view', BY, BY + VH)
OFF = T_START - 0.5          # reel-review: the static 3-2-1 is cut; video starts 0.5s before GO with the racers jogging on the spot
DUR = T_WIN + 3.6 - OFF; NF = int(DUR * FPS)
GHOST = {n: [] for n in NAMES}; POPS = Pops(1.1, ymin=BY + 8); OPEN = []
rank_pos = {n: float(FR[int(round(OFF * FPS))][1].index(n)) for n in NAMES}
wr = Writer('v48_noaudio.mp4'); ev = []; camy = 0.0
seen = set()
def E(tt): return round(tt - OFF, 3)
for f in range(NF):
    fs = f + int(round(OFF * FPS)); t = fs / FPS; st, rank, taken = FR[min(fs, len(FR) - 1)]
    lead = max(st[n]['p'] for n in NAMES if st[n]['out'] is None) if any(st[n]['out'] is None for n in NAMES) else YF
    tgt = min(max(min(lead, YF + 200) - VH * 0.55, 0), WH - VH)
    if t > T_START: camy += (tgt - camy) * 0.1
    cy0 = int(camy); view = GROUND.crop((0, cy0, W, cy0 + VH + 420)).copy()
    items = []
    for k, (oy, ol, kind) in enumerate(OBST):
        if cy0 - 100 < oy < cy0 + VH + 100: items.append((oy, 'o', k))
    for n in NAMES: items.append((st[n]['p'], 'r', n))
    for k, (by, bl) in enumerate(BOOST):
        if (k not in taken or t < taken[k][1]) and cy0 - 100 < by < cy0 + VH + 100:
            bx = xc(by) + bl; bob = int(8 * math.sin(t * 4 + k)); sy = by - cy0
            layer(view, lambda dd: [dd.ellipse([bx - r_, sy - r_ + bob - 16, bx + r_, sy + r_ + bob - 16], fill=(255, 160, 40, a_)) for r_, a_ in ((56, 40), (40, 70), (28, 90))])
            view.alpha_composite(MUSH, (int(bx - MUSH.width / 2), int(sy - MUSH.height / 2 - 16 + bob)))
        elif k in taken and 0 <= t - taken[k][1] < 0.6:
            u = t - taken[k][1]; bx = xc(by) + bl; sy = by - cy0
            layer(view, lambda dd: [dd.rectangle([bx + (20 + 110 * u) * math.cos(q * 0.628) - 5, sy - 20 + (20 + 110 * u) * math.sin(q * 0.628) - 5, bx + (20 + 110 * u) * math.cos(q * 0.628) + 5, sy - 20 + (20 + 110 * u) * math.sin(q * 0.628) + 5], fill=(255, 170, 60, int(255 * (1 - u / 0.6)))) for q in range(10)])
    layer(view, lambda dd: [dd.ellipse([xc(st[n]['p']) + st[n]['l'] - 26, st[n]['p'] - cy0 - 8, xc(st[n]['p']) + st[n]['l'] + 26, st[n]['p'] - cy0 + 8], fill=(0, 0, 0, 80)) for n in NAMES])
    for yy, kind, key in sorted(items, key=lambda z: z[0]):
        if kind == 'o':
            oy, ol, ok = OBST[key]; ox = xc(oy) + ol
            im = SLM[(int(t * 8) + key) % len(SLM)] if ok == 'slime' else OBIM[ok]
            view.alpha_composite(im, (int(ox - im.width / 2), int(oy - cy0 - im.height + 18 if ok != 'slime' else oy - cy0 - 62 * 2 + 4)))
            continue
        n = key; s = st[n]; x = xc(s['p']) + s['l']; y = s['p'] - cy0
        slope = s['vx'] / max(1, 330)
        if t < T_START: spr = FRUN[n][int(t * 14 + NAMES.index(n) * 2) % 8]
        elif s['out'] is not None and t > s['out'] + 0.4: spr = STAND[n]
        elif s['sliding']:
            k = min(6, int((t - s['slide']) / SL * 7)); spr = (SLIDEL if s['vx'] < 0 else SLIDE)[n][k]
            if (n, round(s['slide'], 2)) not in seen: seen.add((n, round(s['slide'], 2))); ev.append((E(t), 'jump'))
            layer(view, lambda dd: [dd.ellipse([x - 14 - q * 4, y - 40 - q * 26, x + 14 + q * 4, y - 22 - q * 26], fill=(205, 175, 130, max(0, int(170 * (1 - (t - s['slide']) / SL)) - q * 40))) for q in range(3)])
        else:
            ph = int(s['dist'] / 24) % 8
            spr = FRUN[n][ph] if abs(slope) < 0.55 else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        boosted = s['boost'] is not None and 0 <= t - s['boost'] < BOOST_T and s['out'] is None
        if boosted:
            # mushroom SPEED (SPEC 12): orange afterimages trailing up the path, speed lines + dust behind
            for i_, (gs, gx, gwy) in enumerate(GHOST[n][-5:-1]):
                view.alpha_composite(tinted(gs, (255, 170, 50), int(255 * (0.14 + 0.09 * i_))), (int(gx - gs.width / 2), int(gwy - cy0 - FOOT)))
            GHOST[n].append((spr, x, s['p']))
            def sl(dd, x=x, y=y):
                for q in range(4):
                    xx = x - 45 + q * 30; y0 = y - FOOT - 30 - (q * 23 + int(t * 70)) % 40; dd.rectangle([xx - 3, y0 - 80 - q * 10, xx + 3, y0], fill=(255, 240, 200, 210))
                for q in range(3):
                    dd.ellipse([x - 22 - q * 6, y - 30 - q * 26, x + 22 + q * 6, y - 4 - q * 26], fill=(210, 190, 150, 170 - q * 50))
            layer(view, sl)
            if (n, 'b', s['boost']) not in seen:
                seen.add((n, 'b', s['boost'])); ev.append((E(t), 'powerup_8bit')); POPS.add(t, x, BY + y - FOOT - 30, 'SPEED!', POWER['mush'][1], 44)
        else: GHOST[n] = []
        view.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['out'] is not None and t >= s['out'] and (n, 'out') not in seen: seen.add((n, 'out')); ev.append((E(t), 'ding_8bit'))
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); img.alpha_composite(view, (0, BY))
    if t < T_WIN + 0.6: text_layer(img, POPS.items(t))
    # FINISH banner when on screen
    fy = YF - cy0 + BY
    if BY - 100 < fy < 1500 + 60 and t < T_WIN + 0.6:
        layer(img, lambda dd: dd.rounded_rectangle([xc(YF) - 150, fy - 140, xc(YF) + 150, fy - 70], 14, fill=(170, 40, 40, 235), outline=(255, 255, 255, 255), width=4))
        d = ImageDraw.Draw(img); ctext(d, xc(YF), fy - 124, 'FINISH', F(40), (255, 255, 255), 5)
    # header: realm art behind the hook + rank chips
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda dd: (dd.rectangle([0, 0, W, BY], fill=(14, 10, 24, 70)), dd.rounded_rectangle([70, CHIP_Y, 1010, CHIP_Y + 96], 18, fill=(14, 10, 24, 225))))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, CHIP_Y, 1010, CHIP_Y + 96], 18, outline=(255, 214, 60), width=4)
    d.rectangle([0, BY - 6, W, BY], fill=(14, 10, 24))
    for i, n in enumerate(NAMES): rank_pos[n] += (rank.index(n) - rank_pos[n]) * 0.2
    for ri in range(4):
        sx = 70 + 940 * (ri + 0.5) / 4
        ctext(d, sx + 44, CHIP_Y + 34, ['1ST', '2ND', '3RD', '4TH'][ri], F(28), (255, 214, 60) if ri == 0 else (230, 230, 230), 4)
    for n in sorted(NAMES, key=lambda n: -rank_pos[n]):
        sx = 70 + 940 * (rank_pos[n] + 0.5) / 4 - 50; ic = ICON[n]; img.alpha_composite(ic, (int(sx - ic.width / 2), CHIP_Y + 10))
    if t < T_START:
        text_layer(img, [(478, BY + 320, 'PICK ONE!', 80, (255, 255, 255), 9, 255)])
    elif t < T_START + 0.6:
        text_layer(img, [(478, BY + 320, 'GO!', 140, (120, 230, 90), 10, int(255 * (1 - (t - T_START) / 0.6)))])
        if abs(t - T_START) < 0.5 / FPS: ev.append((E(t), 'go_8bit'))
    if t >= T_WIN + 0.6:
        u = t - T_WIN - 0.6; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, BY, W, H], fill=(8, 6, 14, int(160 * a))))
        ic = up(ICON[WIN], 2); img.alpha_composite(ic, (478 - ic.width // 2, BY + 24))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1290 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, 478, 1310, LABEL[WIN] + ' WINS!', F(56), (255, 214, 60), 8)
        if u > 0.6: text_layer(img, [(478, 1408, 'Did your guide make it?', 32, (255, 255, 255), 5, int(255 * min(1, (u - 0.6) / 0.4)))])
        r2 = random.Random(f)
        for _ in range(45):
            cx_, cy_ = r2.uniform(80, 870), BY + (r2.uniform(0, VH) + u * 480) % VH
            d.rectangle([cx_, cy_, cx_ + 11, cy_ + 11], fill=r2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240)]))
        if not any(e_[1] == 'victory' for e_ in ev): ev.append((E(t), 'victory')); ev.append((E(t), 'cheer'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f < 9: OPEN.append(img.copy())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
for im_ in OPEN: wr.write(im_)          # loop: cut back to the opening
wr.close(); json.dump(ev, open('v48_ev.json', 'w')); print('done', round(DUR + 0.3, 2), len(ev))
