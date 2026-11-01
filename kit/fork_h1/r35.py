import sys, os, math, random, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c7'); from powers import *
NAMES = ['joy', 'cyrus', 'cleo', 'ray']  # Hollow rule: the Hollow is the player, never a pickable racer
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SS = int(os.environ.get('SS', '3')); FOOT = 78 * SS
SRUN = {g: seq(PL + f'race/{g}_run', SS) for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq(PL + 'maze/anim/hollow_srun', SS)
SLIDE = {g: seq(PL + f'maze/anim/{g}_slide', SS, 1, 8) for g in NAMES}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SS) for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', SS, 0, 1)[0] for g in NAMES}
FL = lambda L: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in L]
SRUNL = {g: FL(v) for g, v in SRUN.items()}; SLIDEL = {g: FL(v) for g, v in SLIDE.items()}
# --- scene
BG = up(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/mountain_b/00.png').convert('RGBA'), 3)
BG = ImageEnhance.Brightness(BG).enhance(0.8)
LEDGE = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/ledge/00.png').convert('RGBA')), 2)            # 318 x 70
STAIR = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/stair/00.png').convert('RGBA')), 2)            # ~56
DR = [Image.open(p).convert('RGBA') for p in sorted(glob.glob('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c7/assets/dragon_gum/*.png'))]   # hoard = gummy pile (no gold)
GUM = gummy('mush', 3)
# switchback course: levels from bottom
LEVY = [1480, 1312, 1144, 976, 808]
XL, XR = 150, 840
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
GUM_S = s_at(GUM_LEV, int(os.environ.get('GX', '495')))
T_GO = float(os.environ.get('TG', '0.6')); T_DARK = T_GO + 1.4
T_DROP = T_GO + float(os.environ.get('TD', '4.0'))
BT, BK = float(os.environ.get('BT', '3.0')), float(os.environ.get('BK', '2.0'))   # mushroom SPEED: time, factor
DA, DB = float(os.environ.get('DA', '38.6')), float(os.environ.get('DB', '2.0'))
def dark_y(t):
    # rc18: the dark is already lapping at the bottom ledge on frame 1 (creeps up slowly), then rises exactly as before.
    # It never gets above y1505 before it merges with the old curve, so no catch changes (racers' feet are at y<=1480).
    creep = 1525 - 4.0 * t
    if t < T_DARK: return creep
    u = t - T_DARK; return min(creep, 1660 - (DA * u + DB * u * u))
def sim(seed):
    rnd = random.Random(seed)
    R = {}
    order = list(range(4)); rnd.shuffle(order)
    for i, n in enumerate(NAMES):
        R[n] = dict(s=-order[i] * 46.0, base=rnd.uniform(285, 345) * float(os.environ.get('SPF', '0.73')), ph=rnd.uniform(0, 6.3), out=None, win=None, slide=-9, boost=None, gum=False)
    frames = []; gum_by = None; winner = None
    for f in range(int(30 * FPS)):
        t = f / FPS; dt = 1 / FPS; dy = dark_y(t)
        for n, r in R.items():
            if r['out'] is not None or r['win'] is not None or t < T_GO: continue
            sp = r['base'] * (1 + 0.22 * math.sin(1.1 * t + r['ph']) + 0.1 * math.sin(2.9 * t + r['ph'] * 2))
            x, y, d, st = pos(r['s'])
            if st: sp *= 0.72
            sliding = t - r['slide'] < 0.55
            if sliding: sp *= 1.35
            boosted = r['boost'] is not None and t - r['boost'] < BT
            if boosted: sp *= BK
            # blocked by someone just ahead on the path -> slide through them (a SPEED racer just zooms past)
            if not sliding and not st and not boosted:
                for m, o in R.items():
                    if m != n and o['out'] is None and o['win'] is None and 0 < o['s'] - r['s'] < 38:
                        if t - r['slide'] > 1.2: r['slide'] = t
                        else: sp = min(sp, o['base'] * 0.95)
            r['s'] += sp * dt
            if gum_by is None and t >= T_DROP + 0.8 and r['s'] - sp * dt < GUM_S <= r['s']:
                gum_by = (n, t); r['gum'] = True; r['boost'] = t
                r['behind'] = sum(1 for m, o in R.items() if m != n and o['s'] > r['s'])
            if r['s'] >= TOTAL: r['win'] = t; winner = winner or (n, t)
            x, y, _, _ = pos(r['s'])
            if dy < y - 18: r['out'] = t
        snap = {n: dict(r) for n, r in R.items()}
        frames.append((snap, dy, gum_by))
        if winner and t > winner[1] + 3.3: break
    return frames, winner, gum_by, R
def score(seed):
    fr, win, gb, R = sim(seed)
    if not win or not gb: return None
    outs = sorted(r['out'] for r in R.values() if r['out'] is not None)
    wins = [n for n, r in R.items() if r['win'] is not None]
    if len(wins) != 1 or len(outs) != 3: return None
    if gb[0] != win[0] or R[win[0]].get('behind', 0) < 2: return None
    if not (9.4 < win[1] < 14.2) or outs[0] < 5.0 or len([o for o in outs if o <= win[1] + 0.3]) < 2 or (os.environ.get('WN') and win[0] != os.environ.get('WN')) or outs[-1] > win[1] + 3.0: return None
    return round(win[1], 2), win[0], [round(o, 1) for o in outs], R[win[0]]['behind']
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, WIN, GB, RR = sim(SEED)
print('win', WIN, 'gum', GB, {n: (round(r['out'], 1) if r['out'] else None) for n, r in RR.items()})
win = WIN[0]; T_W = WIN[1]; TOFF = next(i for i, (sn, _, _) in enumerate(FR) if all(v['s'] >= 0 for v in sn.values())) / FPS; print('TOFF', TOFF); END = T_W + float(os.environ.get('HOLD', '1.4'))   # rc18: video starts on GO!, win hold 3.2 -> 1.4s
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
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
# Oct 29 soft-fade pass: no box. PICK A GUIDE (80px gold) + the rule of the game in the same fade (44px, the purple at the bottom
# only reads as a threat once you know the dark rises), status icons right under it.
_, HB0 = hook_fade(['Pick a guide'], accent=0, size=80)
HOOK, _ = hook_fade(['Pick a guide'], accent=0, size=80, fade_to=HB0 + 170)
import sys as _hw; _hw.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h1'); from hookw import hook_fade_w
HOOK, HG = hook_fade_w(['WHO OUTRUNS', 'THE DARK?'], ['DARK?'], size=72, glyph_bottom=HB0 + 4 + 44, fade_to=HB0 + 170); print('new hook', HG)   # fork_h1: replaces PICK A GUIDE + sub, same bottom
HB = HB0 + 56; ICON_Y = HB + 48; print('hook bottom', HB, 'icons', ICON_Y)
W_ = Writer('v35_noaudio.mp4'); ev = []
rng = random.Random(3)
SPARK = [(rng.uniform(0, W), rng.uniform(0, 1), rng.uniform(0.5, 1.5)) for _ in range(70)]
seen_out = set(); seen_slide = set(); seen_boost = set(); GHOST = {n: [] for n in NAMES}; POPS = Pops(1.2)
# caught stamps: one big stamp per catch moment (same weight as the win stamp), never overlapping
CATCH = {}
for n, r in RR.items():
    if r['out'] is not None: CATCH.setdefault(round(r['out'], 2), []).append(n)
CATCH = sorted(CATCH.items()); print('catches', CATCH)
OPEN = []
NF0 = int(round(TOFF * FPS))
for f in range(NF0, int(END * FPS)):
    t = f / FPS; st_, dy, gb = FR[min(f, len(FR) - 1)]
    img = BG.copy(); img.alpha_composite(COURSE)
    # dragon + hoard at the top
    df = DR[int(t * 5) % len(DR)]; img.alpha_composite(df, (XL + 240, LEVY[-1] - 250))
    # gummy pickup on level 2
    if T_DROP <= t < T_DROP + 0.8:
        u = (t - T_DROP) / 0.8; gx0, gy0 = XL + 390, LEVY[-1] - 120; gx1, gy1, _, _ = pos(GUM_S)
        gx = gx0 + (gx1 - gx0) * u; gy = gy0 + (gy1 - 56 - gy0) * u - 260 * math.sin(math.pi * u)
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        if not any(e[1] == 'whoosh_8bit' for e in ev): ev.append((round(T_DROP, 3), 'whoosh_8bit'))
    if t >= T_DROP + 0.8 and (gb is None or t < gb[1]):
        gx, gy, _, _ = pos(GUM_S); bob = int(8 * math.sin(t * 4))
        layer(img, lambda d: [d.ellipse([gx - 40 + q, gy - 96 + bob + q, gx + 40 - q, gy - 16 + bob - q], fill=(255, 200, 120, 30 + q * 3)) for q in range(0, 30, 6)])
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - 56 - GUM.height / 2 + bob)))
    # racers
    for n in sorted(NAMES, key=lambda n: pos(st_[n]['s'])[1]):
        r = st_[n]; x, y, d, stair = pos(r['s'])
        if r['win'] is not None: continue
        boosted = r['boost'] is not None and 0 <= t - r['boost'] < BT and r['out'] is None
        if r['out'] is not None:
            spr = PANIC[n][int(t * 12) % 8]
            if n not in seen_out: seen_out.add(n); ev.append((round(t, 3), 'poof'))
        elif t < T_GO: spr = SRUN[n][int(t * 14 + NAMES.index(n) * 2) % 8]      # jogging on the spot under PICK ONE!
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
        x0_, y0_ = int(x - spr.width / 2), int(y - FOOT)
        if boosted:
            afterimages(img, GHOST[n][-4:]); speed_lines(img, x, y, d, t, FOOT)
            GHOST[n].append((spr, x0_, y0_))
            if n not in seen_boost: seen_boost.add(n); ev.append((round(t, 3), 'powerup_8bit')); POPS.add(t, x, y - FOOT - 20, 'SPEED!', POWER['mush'][1], 44)
        else: GHOST[n] = []
        img.alpha_composite(spr, (x0_, y0_))
    # rising dark: purple shadow with a wavy top and sparkles
    if dy < 1660:
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
    d = ImageDraw.Draw(img)
    for i, n in enumerate(NAMES):
        ix = W / 2 + (i - 1.5) * 180; iy = ICON_Y; ic = ICON[n]; r = st_[n]
        if r['out'] is not None: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(ix - 36), int(iy - 36)))
        d = ImageDraw.Draw(img)
        if r['out'] is not None:
            d.line([ix - 26, iy - 26, ix + 26, iy + 26], fill=(230, 50, 50), width=9); d.line([ix - 26, iy + 26, ix + 26, iy - 26], fill=(230, 50, 50), width=9)
        if r['gum'] and r['out'] is None: img.alpha_composite(gummy('mush', 1), (int(ix + 18), int(iy + 12)))
    text_layer(img, POPS.items(t))
    for tc, who in CATCH:
        u = t - tc
        if 0 <= u < 1.1 and t < T_W:
            a_ = int(255 * min(1, (1.1 - u) / 0.25)); sc = 1 + 0.35 * max(0, 1 - u / 0.15)
            text_layer(img, [(478, 1150, 'CAUGHT!', int(72 * sc), (255, 70, 70), 10, a_), (478, 1250, ' & '.join(LABEL[n] for n in who), 44, (255, 255, 255), 8, a_)])
    if t < T_GO:
        text_layer(img, [(480, 1020, 'PICK ONE!', 80, (255, 255, 255), 9, 255)])
    elif t < TOFF + 0.6:
        sc_ = 1 + 0.25 * max(0, 1 - (t - TOFF) / 0.12)
        text_layer(img, [(480, 1020, 'GO!', int(130 * sc_), (255, 214, 60), 10, 255)])
        if not any(e[1] == 'go_8bit' for e in ev): ev.append((round(TOFF, 3), 'go_8bit'))
    if t >= T_W:
        u = t - T_W; layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(10, 6, 20, int(160 * min(1, u / 0.3)))))
        vf = VF[int(u * 8) % len(VF)]; img.alpha_composite(vf, (480 - vf.width // 2, 1180 - vf.height))
        text_layer(img, [(480, 1230, LABEL[win] + ' WINS!', 56, (255, 214, 60), 8, 255)])   # 'DID YOUR GUIDE / MAKE IT?' cut (caption asks)
        if not any(e[1] == 'victory' for e in ev): ev.append((round(T_W, 3), 'victory'))
    img.alpha_composite(HOOK)
    W_.write(img)
    if os.environ.get('PV') and (f - NF0) in [int(x) for x in os.environ['PV'].split(',')]: img.convert('RGB').save(f'pv_{f - NF0:04d}.png')
    if f - NF0 < 9: OPEN.append(img.copy())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/a_{f:04d}.png')
for im_ in OPEN: W_.write(im_)          # loop: cut back to the opening
W_.close()
ev = [(round(max(0, a - TOFF), 3), b) for a, b in ev if a >= TOFF - 0.05]
json.dump(ev, open('v35_ev.json', 'w')); print('done', END - TOFF + 0.3)
