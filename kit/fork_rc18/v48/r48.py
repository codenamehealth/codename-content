import sys, math, json, random
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c7'); from powers import *
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
T = {i: up(Image.open(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/race/tiles/tile_{i}.png').convert('RGBA'), 2) for i in range(16)}
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
def pick(d, i): return crop(Image.open(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/steal/{d}/{i:02d}.png').convert('RGBA'))
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
SLM = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/race/slime_idle_c/*.png'))]
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int); a[(r > 140) & (g < 110) & (b < 140)] = 0; return Image.fromarray(a)
SLM = [nored(f) for f in SLM]
OBIM = {'crate': up(pick('crate', 1), 2), 'hay': up(pick('barrel', 0), 2)}
SS = 2; FOOT = 78 * SS
def seqa(d, lo=1, hi=9): return [up(Image.open(p).convert('RGBA'), SS) for p in sorted(glob.glob(d + '/*.png'))[lo:hi]]
SRUN = {g: seqa(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/race/{g}_run') for g in ['joy', 'cyrus', 'cleo', 'ray']}; 
FRUN = {g: seqa(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/maze/anim/{g}_frun') for g in NAMES}
SLIDE = {g: seqa(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/maze/anim/{g}_slide', 1, 8) for g in NAMES}
STAND = {g: seqa(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/maze/anim/{g}_frun', 0, 1)[0] for g in NAMES}
FLIP = lambda L: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in L]
SRUNL = {g: FLIP(v) for g, v in SRUN.items()}; SLIDEL = {g: FLIP(v) for g, v in SLIDE.items()}
MUSH = gummy('mush', 2)          # rc18: 2x in the world, 3x on screen after the 1.5x camera zoom
SRCF = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
def face(name, rad):
    im = Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/syeda_src/' + SRCF[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255); b.paste(head, (6, 6), m); return b
ICON = {n: face(n, 44) for n in NAMES}   # rc18: standings faces 76 -> 92px
HOOK, HB = hook_layer(['CHOOSE YOUR', 'GUIDE'], accent=1)
# rc18: standings strip 96 -> 112px (faces 76 -> 92px, 1ST-4TH 28 -> 44px), swaps snap (debounced) with a ring flash, never stacked
CHIP_Y = HB + 6; CHIP_H = 112
BY = CHIP_Y + CHIP_H + 6; VH = 1500 - BY
HDR = bg_frames('found_hd.gif', (W, BY), box=(8, 0, 1912, 1080), step=2, bright=0.6)
print('hook bottom', HB, 'view', BY)
# rc18: camera zoom 1.5x on the pack (2x world art -> 3x on screen, exact pixel blocks: crop origin and sprites snapped to even px)
Z = 1.5; VWW = 720; VHW = VH / Z; FULLH = int((H - BY) / Z) // 2 * 2 + 4
def vcomp(v, im, pos): v.alpha_composite(im, (int(pos[0]) // 2 * 2, int(pos[1]) // 2 * 2))
def cam_target(st):
    ps = [min(st[n]['p'], YF + 150) for n in NAMES]; top = min(ps) - 118; bot = max(ps) + 30; span = bot - top
    cy = (top + bot) / 2 - VHW / 2 if span <= VHW else top + (span - VHW) / 2 - 10
    xs = [xc(st[n]['p']) + st[n]['l'] for n in NAMES]; cx = (min(xs) + max(xs)) / 2 - VWW / 2
    return max(0, min(WH - FULLH - 2, cy)), max(0, min(W - VWW, cx))
VICF = vic(WIN, 360)
OFF = T_START                # rc18: video opens on GO! with the pack already starting to run (was 0.5s jogging on the spot)
FREEZE = 0.4; CARD = 1.5     # rc18: 0.4s freeze on Joy crossing the line; win card 3.0 -> 1.5s
DUR = T_WIN - OFF + FREEZE + 0.6 + CARD; NF = int(DUR * FPS)
# lead-change stamps (a new leader counts once they hold it 0.3s, or hold it to the line); the opening leader is not a change
LEADS = []; cur = None; cand = None; cand_t = 0
for f_ in range(int(round((T_START + 1) * FPS)), int(round(T_WIN * FPS)) + 1):
    l = FR[f_][1][0]; tt = f_ / FPS
    if l != cand: cand, cand_t = l, tt
    if cand != cur and (tt - cand_t >= 0.3 or tt >= T_WIN - 1.5 / FPS): cur = cand; LEADS.append((cand_t, cand))
LEADS = LEADS[1:]; print('lead stamps', [(round(a, 2), b) for a, b in LEADS])
def lead_box(t):
    for k, (t0, n) in enumerate(LEADS):
        t1 = min(t0 + 1.4, LEADS[k + 1][0] if k + 1 < len(LEADS) else 99)
        if t0 <= t < t1 and t < T_WIN + 0.6: return t0, t1, n
    return None
GHOST = {n: [] for n in NAMES}; POPS = Pops(1.0, ymin=BY + 8); OPEN = []
disp = list(FR[int(round(OFF * FPS))][1]); cand_r = disp[:]; cand_rt = 0; flash = {}
wr = Writer('v48_noaudio.mp4'); ev = []; camy = camx = None
seen = set()
def E(tt): return round(tt - OFF + (FREEZE if tt > T_WIN + 1e-6 else 0), 3)
for t0_, n_ in LEADS: ev.append((E(t0_), 'twinkle'))
for f in range(NF):
    tv = f / FPS; frozen = T_WIN - OFF <= tv < T_WIN - OFF + FREEZE
    t = OFF + tv if tv < T_WIN - OFF else (T_WIN if frozen else OFF + tv - FREEZE)
    fs = int(round(t * FPS)); st, rank, taken = FR[min(fs, len(FR) - 1)]
    ty, tx = cam_target(st)
    if camy is None: camy, camx = ty, tx
    elif not frozen: camy += (ty - camy) * 0.12; camx += (tx - camx) * 0.12
    cy0 = int(camy) // 2 * 2; cx0 = int(camx) // 2 * 2; view = GROUND.crop((0, cy0, W, cy0 + FULLH)).copy()
    items = []
    for k, (oy, ol, kind) in enumerate(OBST):
        if cy0 - 100 < oy < cy0 + VH + 100: items.append((oy, 'o', k))
    for n in NAMES: items.append((st[n]['p'], 'r', n))
    for k, (by, bl) in enumerate(BOOST):
        if (k not in taken or t < taken[k][1]) and cy0 - 100 < by < cy0 + VH + 100:
            bx = xc(by) + bl; bob = int(8 * math.sin(t * 4 + k)); sy = by - cy0
            layer(view, lambda dd: [dd.ellipse([bx - r_, sy - r_ + bob - 16, bx + r_, sy + r_ + bob - 16], fill=(255, 160, 40, a_)) for r_, a_ in ((56, 40), (40, 70), (28, 90))])
            vcomp(view, MUSH, (int(bx - MUSH.width / 2), int(sy - MUSH.height / 2 - 16 + bob)))
        elif k in taken and 0 <= t - taken[k][1] < 0.6:
            u = t - taken[k][1]; bx = xc(by) + bl; sy = by - cy0
            layer(view, lambda dd: [dd.rectangle([bx + (20 + 110 * u) * math.cos(q * 0.628) - 5, sy - 20 + (20 + 110 * u) * math.sin(q * 0.628) - 5, bx + (20 + 110 * u) * math.cos(q * 0.628) + 5, sy - 20 + (20 + 110 * u) * math.sin(q * 0.628) + 5], fill=(255, 170, 60, int(255 * (1 - u / 0.6)))) for q in range(10)])
    layer(view, lambda dd: [dd.ellipse([xc(st[n]['p']) + st[n]['l'] - 26, st[n]['p'] - cy0 - 8, xc(st[n]['p']) + st[n]['l'] + 26, st[n]['p'] - cy0 + 8], fill=(0, 0, 0, 80)) for n in NAMES])
    for yy, kind, key in sorted(items, key=lambda z: z[0]):
        if kind == 'o':
            oy, ol, ok = OBST[key]; ox = xc(oy) + ol
            im = SLM[(int(t * 8) + key) % len(SLM)] if ok == 'slime' else OBIM[ok]
            vcomp(view, im, (int(ox - im.width / 2), int(oy - cy0 - im.height + 18 if ok != 'slime' else oy - cy0 - 62 * 2 + 4)))
            continue
        n = key; s = st[n]; x = xc(s['p']) + s['l']; y = s['p'] - cy0
        slope = s['vx'] / max(1, 330)
        if t < T_START: spr = FRUN[n][int(t * 14 + NAMES.index(n) * 2) % 8]
        elif s['out'] is not None and t > s['out'] + 0.4: spr = STAND[n]
        elif s['sliding']:
            k = min(6, int((t - s['slide']) / SL * 7)); spr = (SLIDEL if s['vx'] < 0 else SLIDE)[n][k]
            if (n, round(s['slide'], 2)) not in seen:
                seen.add((n, round(s['slide'], 2))); ev.append((E(t), 'jump'))
                if any(k_ == 'slime' and -20 < oy - s['p'] < 80 and abs(ol - s['l']) < 52 for oy, ol, k_ in OBST):   # rc18: SLIMED! on every slime trip
                    POPS.add(t, (x - cx0) * Z, BY + (y - FOOT) * Z - 10, 'SLIMED!', (130, 235, 90), 44); ev.pop(); ev.append((E(t), 'squish'))
            layer(view, lambda dd: [dd.ellipse([x - 14 - q * 4, y - 40 - q * 26, x + 14 + q * 4, y - 22 - q * 26], fill=(205, 175, 130, max(0, int(170 * (1 - (t - s['slide']) / SL)) - q * 40))) for q in range(3)])
        else:
            ph = int(s['dist'] / 24) % 8
            spr = FRUN[n][ph] if abs(slope) < 0.55 else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        boosted = s['boost'] is not None and 0 <= t - s['boost'] < BOOST_T and s['out'] is None
        if boosted:
            # mushroom SPEED (SPEC 12): orange afterimages trailing up the path, speed lines + dust behind
            for i_, (gs, gx, gwy) in enumerate(GHOST[n][-5:-1]):
                vcomp(view, tinted(gs, (255, 170, 50), int(255 * (0.14 + 0.09 * i_))), (int(gx - gs.width / 2), int(gwy - cy0 - FOOT)))
            GHOST[n].append((spr, x, s['p']))
            def sl(dd, x=x, y=y):
                for q in range(4):
                    xx = x - 45 + q * 30; y0 = y - FOOT - 30 - (q * 23 + int(t * 70)) % 40; dd.rectangle([xx - 3, y0 - 80 - q * 10, xx + 3, y0], fill=(255, 240, 200, 210))
                for q in range(3):
                    dd.ellipse([x - 22 - q * 6, y - 30 - q * 26, x + 22 + q * 6, y - 4 - q * 26], fill=(210, 190, 150, 170 - q * 50))
            layer(view, sl)
            if (n, 'b', s['boost']) not in seen:
                seen.add((n, 'b', s['boost'])); ev.append((E(t), 'powerup_8bit')); POPS.add(t, (x - cx0) * Z, BY + (y - FOOT) * Z - 20, 'SPEED!', POWER['mush'][1], 52)
        else: GHOST[n] = []
        vcomp(view, spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['out'] is not None and t >= s['out'] and (n, 'out') not in seen: seen.add((n, 'out')); ev.append((E(t), 'ding_8bit'))
    zv = view.crop((cx0, 0, cx0 + VWW, FULLH)).resize((W, int(FULLH * Z)), Image.NEAREST)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); img.alpha_composite(zv.crop((0, 0, W, H - BY)), (0, BY))
    LB = lead_box(t)
    if t < T_WIN + 0.6: text_layer(img, POPS.items(t, avoid=[(480, BY + 88, 760, 150)] if LB else []))
    # FINISH banner when on screen
    fy = BY + (YF - cy0) * Z; fx = (xc(YF) - cx0) * Z
    if BY - 200 < fy < 1500 - 154 and t < T_WIN + 0.6:
        layer(img, lambda dd: dd.rounded_rectangle([fx - 170, fy + 70, fx + 170, fy + 154], 14, fill=(170, 40, 40, 235), outline=(255, 255, 255, 255), width=5))
        d = ImageDraw.Draw(img); ctext(d, fx, fy + 90, 'FINISH', F(44), (255, 255, 255), 6)
    if frozen:
        # Joy alone on the line: flash + ring for one clear beat
        u = tv - (T_WIN - OFF); s = st[WIN]; jx = (xc(s['p']) + s['l'] - cx0) * Z; jy = BY + (s['p'] - cy0) * Z - FOOT * Z * 0.32
        if u < 0.1: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(150 * (1 - u / 0.1)))))
        layer(img, lambda dd: [dd.ellipse([jx - 110 - q, jy - 130 - q, jx + 110 + q, jy + 130 + q], outline=(255, 214, 60, 255 - q * 20), width=8) for q in (0, 6)])
    if LB:
        t0, t1, n = LB; u = t - t0; a = int(255 * min(1, (t1 - t) / 0.15)); sc = 1 + 0.3 * max(0, 1 - u / 0.12)
        layer(img, lambda dd: dd.rounded_rectangle([100, BY + 14, 860, BY + 164], 18, fill=(14, 10, 24, int(225 * a / 255)), outline=RING[n] + (a,), width=6))
        text_layer(img, [(480, BY + 26 - int(32 * (sc - 1)), LABEL[n], int(64 * sc), RING[n], 9, a), (480, BY + 106, 'TAKES THE LEAD!', 44, (255, 255, 255), 7, a)])
    # header: realm art behind the hook + standings
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda dd: (dd.rectangle([0, 0, W, BY], fill=(14, 10, 24, 70)), dd.rounded_rectangle([70, CHIP_Y, 1010, CHIP_Y + CHIP_H], 18, fill=(14, 10, 24, 225))))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, CHIP_Y, 1010, CHIP_Y + CHIP_H], 18, outline=(255, 214, 60), width=4)
    d.rectangle([0, BY - 6, W, BY], fill=(14, 10, 24))
    if list(rank) != cand_r: cand_r = list(rank); cand_rt = t
    if cand_r != disp and (t - cand_rt >= 0.25 or t >= T_WIN - 0.05) and not frozen:
        for ri, n in enumerate(cand_r):
            if disp[ri] != n: flash[n] = t
        disp = cand_r[:]
    for ri, n in enumerate(disp):
        x0 = 70 + 235 * ri; ic = ICON[n]; img.alpha_composite(ic, (x0 + 8, CHIP_Y + 10))
        d = ImageDraw.Draw(img); ctext(d, x0 + 164, CHIP_Y + 34, ['1ST', '2ND', '3RD', '4TH'][ri], F(44), (255, 214, 60) if ri == 0 else (235, 235, 235), 6)
        if n in flash and 0 <= t - flash[n] < 0.3:
            fa = int(255 * (1 - (t - flash[n]) / 0.3))
            layer(img, lambda dd, x0=x0, fa=fa: dd.ellipse([x0 + 2, CHIP_Y + 4, x0 + 106, CHIP_Y + 108], outline=(255, 255, 255, fa), width=7))
    if t < T_START + 0.6:
        sc = 1 + 0.25 * max(0, 1 - (t - T_START) / 0.12)
        text_layer(img, [(478, BY + 300, 'GO!', int(140 * sc), (120, 230, 90), 10, int(255 * min(1, (T_START + 0.6 - t) / 0.25)))])
        if f == 0: ev.append((0.0, 'go_8bit'))
    if t >= T_WIN + 0.6:
        u = t - T_WIN - 0.6; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, BY, W, H], fill=(8, 6, 14, int(160 * a))))
        ic = up(ICON[WIN], 2); img.alpha_composite(ic, (478 - ic.width // 2, BY + 24))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1250 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, 478, 1270, LABEL[WIN] + ' WINS!', F(56), (255, 214, 60), 8)
        text_layer(img, [(478, 1354, 'DID YOUR GUIDE', 44, (255, 255, 255), 7, 255), (478, 1412, 'MAKE IT?', 44, (255, 255, 255), 7, 255)])
        r2 = random.Random(f)
        for _ in range(45):
            cx_, cy_ = r2.uniform(80, 870), BY + (r2.uniform(0, VH) + u * 480) % VH
            d.rectangle([cx_, cy_, cx_ + 11, cy_ + 11], fill=r2.choice([(90, 200, 80), (90, 150, 255), (255, 120, 120), (190, 90, 240), (255, 160, 40)]))
        if not any(e_[1] == 'victory' for e_ in ev): ev.append((E(t), 'victory')); ev.append((E(t), 'cheer'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f < 9: OPEN.append(img.copy())
    if os.environ.get('PV') and f in [int(x) for x in os.environ['PV'].split(',')]: img.convert('RGB').save(f'pv_{f:04d}.png')
for im_ in OPEN: wr.write(im_)          # loop: cut back to the opening
wr.close(); json.dump(ev, open('v48_ev.json', 'w')); print('done', round(DUR + 0.3, 2), len(ev))
