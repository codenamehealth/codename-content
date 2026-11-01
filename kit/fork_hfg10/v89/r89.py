import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
# #89 Last one in the ring wins: rc10 review recut (source fork_sz86/v89/r89.py). Bennett loves it: rule/legibility/universal fixes only.
# rc10: guides 2x -> 3x (collision 56 -> 80), shoving from frame 0, gummies earlier, re-simmed for ~15s with even eliminations; Joy still wins.
import hook as HK
COLL = float(os.environ.get('COLL', '80'))
# HOLLOW RULE: the Hollow contestant is removed (4 guides). GUMMY POWERS (SPEC 12): creatine = STRONG! (power shove),
# mushroom = SPEED! (runs and dashes faster, speed lines + dust); the old POWER SHOVE (mushroom) / HEAVY (creatine) labels are gone.
# Ring 430 -> 340 radius (characters unchanged 2x) so the whole deck fits the safe zone; re-simulated.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RINGC = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
CX, CY, RR = 478, 1120, 340
def sim(seed, dur=30):
    rnd = random.Random(seed)
    ag = {}
    for k, n in enumerate(NAMES):
        a = -math.pi / 4 + k * 2 * math.pi / 4
        ag[n] = dict(x=CX + 175 * math.cos(a), y=CY + 175 * math.sin(a), vx=0.0, vy=0.0, out=None, dash=-9, cd=rnd.uniform(0.3, 1.2), tgt=None,
                     spd=rnd.uniform(220, 260), pow=1.0, mass=1.0, buff=None, bt=-9, stun=-9, dist=0.0, ph=rnd.uniform(0, 6.3), dx=0, dy=0)
    gums = []; gsched = [(2.2, None), (5.2, None), (8.2, None), (11.2, None)]
    frames = []; events = []; T0 = 0.0; outs = []   # rc10: shoving from frame 0 (was a 2.2s still line-up)
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        alive = [n for n in NAMES if ag[n]['out'] is None]
        for gt, _ in gsched:
            if abs(t - gt) < dt / 2 and len(alive) > 1:
                a = rnd.uniform(0, 6.28); r = rnd.uniform(0, 130)
                gums.append(dict(x=CX + r * math.cos(a), y=CY + r * math.sin(a), k=rnd.choice(['mush', 'cre']), t=t))
        if t >= T0 and len(alive) > 1:
            for n in alive:
                s = ag[n]
                if s['buff'] and t - s['bt'] > 4.0: s['buff'] = None; s['pow'] = 1.0; s['mass'] = 1.0
                # pick target: nearest gummy if close, else a rival (prefer one near the edge)
                if gums and min(math.hypot(g['x'] - s['x'], g['y'] - s['y']) for g in gums) < 260:
                    g = min(gums, key=lambda g: math.hypot(g['x'] - s['x'], g['y'] - s['y'])); tx, ty = g['x'], g['y']; tg = None
                else:
                    if s['tgt'] not in alive or s['tgt'] == n or rnd.random() < 0.01:
                        opts = [m for m in alive if m != n]
                        s['tgt'] = min(opts, key=lambda m: math.hypot(ag[m]['x'] - s['x'], ag[m]['y'] - s['y']) - 0.6 * math.hypot(ag[m]['x'] - CX, ag[m]['y'] - CY) + rnd.uniform(0, 140))
                    o = ag[s['tgt']]; tg = s['tgt']
                    # approach from the inside so the shove points outward
                    ox, oy = o['x'] - CX, o['y'] - CY; L = math.hypot(ox, oy) or 1
                    tx, ty = o['x'] - ox / L * 50, o['y'] - oy / L * 50
                dashing = t - s['dash'] < 0.32; stunned = t - s['stun'] < 0.45
                if not dashing and not stunned:
                    dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                    sp = s['spd'] * (1 + 0.15 * math.sin(2.1 * t + s['ph']))
                    if s['buff'] == 'mush': sp *= 1.6                      # SPEED!
                    # keep away from the edge
                    ex, ey = s['x'] - CX, s['y'] - CY; er = math.hypot(ex, ey) or 1
                    inx = iny = 0
                    if er > RR - 90: inx, iny = -ex / er * 1.4, -ey / er * 1.4
                    ux, uy = dx / L + inx, dy / L + iny; U = math.hypot(ux, uy) or 1
                    s['vx'] += (ux / U * sp - s['vx']) * 0.15; s['vy'] += (uy / U * sp - s['vy']) * 0.15
                    if tg and t > s['cd'] + T0 and math.hypot(ag[tg]['x'] - s['x'], ag[tg]['y'] - s['y']) < 150:
                        o = ag[tg]; dx, dy = o['x'] - s['x'], o['y'] - s['y']; L = math.hypot(dx, dy) or 1
                        s['dash'] = t; s['dx'], s['dy'] = dx / L, dy / L; dv = 760 * (1.3 if s['buff'] == 'mush' else 1.0); s['vx'], s['vy'] = dx / L * dv, dy / L * dv
                        s['cd'] = t - T0 + rnd.uniform(0.9, 1.7)
                if stunned: s['vx'] *= 0.9; s['vy'] *= 0.9
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
            # collisions
            for i, a in enumerate(alive):
                for b in alive[i + 1:]:
                    A_, B_ = ag[a], ag[b]; dx, dy = B_['x'] - A_['x'], B_['y'] - A_['y']; d = math.hypot(dx, dy)
                    if 0 < d < COLL:
                        ux, uy = dx / d, dy / d
                        ad = t - A_['dash'] < 0.32; bd = t - B_['dash'] < 0.32
                        if ad or bd:
                            sh, vi = (A_, B_) if (ad and not bd) or (ad and bd and rnd.random() < 0.5) else (B_, A_)
                            sgn = 1 if sh is A_ else -1
                            imp = 760 * sh['pow'] / vi['mass'] * rnd.uniform(0.85, 1.15)
                            vi['vx'] = ux * sgn * imp; vi['vy'] = uy * sgn * imp; vi['stun'] = t
                            sh['vx'] *= 0.15; sh['vy'] *= 0.15; sh['dash'] = -9
                            events.append((t, 'shove', a if sh is A_ else b, b if sh is A_ else a))
                        push = (COLL - d) / 2; A_['x'] -= ux * push; A_['y'] -= uy * push; B_['x'] += ux * push; B_['y'] += uy * push
            for n in alive:
                s = ag[n]
                for g in list(gums):
                    if math.hypot(g['x'] - s['x'], g['y'] - s['y']) < 46:
                        gums.remove(g); s['buff'] = g['k']; s['bt'] = t
                        if g['k'] == 'cre': s['pow'] = 1.7            # STRONG!: power shove
                        s['cd'] = min(s['cd'], t - T0 + 0.2)
                        events.append((t, 'gum', n, g['k']))
                if math.hypot(s['x'] - CX, s['y'] - CY) > RR + 16:
                    s['out'] = t; outs.append((n, t)); events.append((t, 'splash', n, None))
        for n in NAMES:
            s = ag[n]
            if s['out'] is not None:
                ex, ey = s['x'] - CX, s['y'] - CY; er = math.hypot(ex, ey) or 1
                if er < RR + 58: s['x'] += ex / er * 70 * dt; s['y'] += ey / er * 70 * dt
        frames.append(({n: dict(x=ag[n]['x'], y=ag[n]['y'], vx=ag[n]['vx'], vy=ag[n]['vy'], out=ag[n]['out'], dash=ag[n]['dash'], stun=ag[n]['stun'], buff=ag[n]['buff'], dist=ag[n]['dist']) for n in NAMES}, [dict(g) for g in gums]))
        alive = [n for n in NAMES if ag[n]['out'] is None]
        if len(alive) == 1 and t > outs[-1][1] + 2.4: break
    win = [n for n in NAMES if ag[n]['out'] is None]
    return frames, events, outs, (win[0] if len(win) == 1 else None)
def score(seed):
    fr, ev, outs, win = sim(seed)
    if not win or win != 'joy': return None
    if len(outs) != 3 or not (10.5 <= outs[-1][1] <= 13.0): return None
    ts = [o[1] for o in outs]
    if ts[0] < 2.5 or min(b - a for a, b in zip(ts, ts[1:])) < 2.6: return None
    sh = sum(1 for e in ev if e[1] == 'shove')
    if sh < 8: return None
    gk = [e[3] for e in ev if e[1] == 'gum']
    if 'mush' not in gk or 'cre' not in gk: return None
    return win, [(o[0], round(o[1], 1)) for o in outs], sh, gk
if __name__ == '__main__' and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, OUTS, WIN = sim(SEED)
print('winner', WIN, OUTS)
def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['LAST ONE IN', 'THE RING WINS'], accent=1, size=64)   # hfg10: soft fade, COMMENT YOUR PICK cut (caption asks)   # rc10: 46px comment line; SHOVING ALLOWED moves to the opening plate
CH0 = HB + 10; CH1 = CH0 + 96
print('hook bottom', HB, 'chips', CH0, CH1, 'deck', CX - RR - 26, CY - RR - 26, CX + RR + 26, CY + RR + 26)
def clampx(x, w, y): return max(70 + w / 2 + 8, min((887 if y > 1110 else 1025) - w / 2 - 8, x))
SS = 3; FOOT = 78 * SS   # rc10: guides 2x -> 3x
SRUN = {g: seq(PL + f'race/{g}_run', SS, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', SS, 1, 9) for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', SS, 0, 1)[0] for g in NAMES}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SS, 1, 9) for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RINGC[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 32) for n in NAMES}; HEAD = {n: face(n, 42) for n in NAMES}
# ground: deck disc inside lake from the Wang tileset
T = wang(SP + 'fork_a9/gen/deck_meta.json', SP + 'fork_a9/gen/deck_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
TS = 64; AY0 = 470; GC, GR = 17, 23
def lowc(i, j):
    x, y = i * TS - 4, AY0 + j * TS
    return (x - CX) ** 2 + (y - CY) ** 2 < (RR + 26) ** 2
CORN = [[lowc(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (40, 110, 180, 255)); DECK = Image.new('RGBA', (W, H))
WT = ImageEnhance.Brightness(T[(False, False, False, False)]).enhance(0.82); DT = T[(True, True, True, True)]
for j in range(GR):
    for i in range(GC):
        fl = (i + j) % 2
        GROUND.alpha_composite(WT.transpose(Image.FLIP_LEFT_RIGHT) if fl else WT, (i * TS - 4, AY0 + j * TS))
        DECK.alpha_composite(DT.transpose(Image.FLIP_LEFT_RIGHT) if fl else DT, (i * TS - 4, AY0 + j * TS))
DR = RR + 26
mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).ellipse([CX - DR, CY - DR, CX + DR, CY + DR], fill=255)
layer(GROUND, lambda d: d.ellipse([CX - DR - 10, CY - DR + 6, CX + DR + 10, CY + DR + 26], fill=(10, 40, 70, 150)))
GROUND.paste(DECK, (0, 0), mask)
layer(GROUND, lambda d: (d.ellipse([CX - DR, CY - DR, CX + DR, CY + DR], outline=(70, 40, 20, 255), width=10), d.ellipse([CX - DR + 8, CY - DR + 8, CX + DR - 8, CY + DR - 8], outline=(150, 100, 55, 255), width=4)))
LILY = [up(crop(Image.open(p).convert('RGBA')), 2) for p in sorted(glob.glob(SP + 'fork4/lilypad/*.png'))[:3]]
rr = random.Random(4)
for k in range(9):
    while True:
        x, y = rr.uniform(40, W - 40), rr.uniform(AY0 + 40, H - 160)
        if math.hypot(x - CX, y - CY) > RR + 110: break
    lp = LILY[k % len(LILY)]; GROUND.alpha_composite(lp, (int(x - lp.width / 2), int(y - lp.height / 2)))
gd = ImageDraw.Draw(GROUND)
# rope ring + center mark painted on the deck
def deco(d):
    d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], outline=(240, 220, 170, 255), width=8)
    d.ellipse([CX - RR, CY - RR, CX + RR, CY + RR], outline=(120, 80, 40, 255), width=3)
    d.ellipse([CX - 70, CY - 70, CX + 70, CY + 70], outline=(240, 220, 170, 160), width=5)
layer(GROUND, deco)
HDR = bg_frames('found_hd.gif', (W, 470), box=(0, 120, 1920, 120 + 835), step=2, bright=0.7)
GUM = {k: gummy(k, 3) for k in ['mush', 'cre']}   # rc10: gummies 2x -> 3x
VICF = vic(WIN, 330)
T_LAST = OUTS[-1][1]; T_WIN = T_LAST + 0.7; END = T_WIN + 1.5   # rc10: final OUT shown at full brightness 0.7s, win held 1.5s, then loop
# rc10: one stamp slot under the IN/OUT panel; OUT stamps and power stamps queued so they never overlap
STAMPS = []
for e in sorted([e for e in EV if e[1] in ('gum', 'splash')], key=lambda e: e[0]):
    if e[1] == 'gum': txt, col, dur = ('SPEED!' if e[3] == 'mush' else 'STRONG!'), ((255, 200, 60) if e[3] == 'mush' else (255, 110, 50)), 0.9
    else: txt, col, dur = LABEL[e[2]] + ' IS OUT!', (255, 90, 80), 1.2
    if e[1] == 'splash' and STAMPS and STAMPS[-1][1] > e[0]:   # an OUT always shows the moment it happens: cut the power stamp short
        a_, b_, c_, d_ = STAMPS[-1]; STAMPS[-1] = (a_, e[0], c_, d_)
    t1 = max(e[0], STAMPS[-1][1]) if STAMPS else e[0]
    if e[1] == 'splash' and e[2] == OUTS[-1][0]: dur = T_WIN - t1
    STAMPS.append((t1, t1 + dur, txt, col))
print('stamps', [(round(a, 2), round(b, 2), c) for a, b, c, _ in STAMPS])
SY = CH1 + 8
wr = Writer('v89_noaudio.mp4'); out_ev = []
BUSY = [0, 20] + [int(e[0] * FPS) + 3 for e in EV if e[1] == 'gum'][:2] + [int(T_LAST * FPS) + 8, int(END * FPS) - 1]
sh_items = [e for e in EV if e[1] == 'shove']
for f in range(int(END * FPS)):
    t = f / FPS; st, gums = FR[min(f, len(FR) - 1)]
    img = GROUND.copy()
    def water(d):
        r2 = random.Random(7)
        for _ in range(110):
            x, y = r2.uniform(0, W), r2.uniform(AY0, H)
            if math.hypot(x - CX, y - CY) < RR + 40: continue
            ph = r2.uniform(0, 6.28); a = int(120 + 120 * math.sin(t * 3 + ph))
            if a > 150: d.rectangle([x, y, x + 6, y + 3], fill=(230, 250, 255, a - 60))
        for n in NAMES:
            s = st[n]
            if s['out'] is not None:
                sx_, sy_ = s['x'], max(SY + 140, min(s['y'], 1500 - 50)); sx_ = max(120, min((887 if sy_ + 50 > 1110 else 1025) - 50, sx_))
                s = dict(s, x=sx_, y=sy_)
                for k in range(3):
                    u = ((t - s['out']) * 0.8 + k / 3) % 1.0; rr_ = 20 + 60 * u
                    d.ellipse([s['x'] - rr_, s['y'] - rr_ * 0.5, s['x'] + rr_, s['y'] + rr_ * 0.5], outline=(230, 250, 255, int(200 * (1 - u))), width=3)
    layer(img, water)
    for g in gums:
        gi = GUM[g['k']]; bob = int(6 * math.sin(t * 5 + g['x']))
        layer(img, lambda d, g=g: d.ellipse([g['x'] - 30, g['y'] - 16 - 6, g['x'] + 30, g['y'] + 16 - 6], fill=(255, 220, 120, 90)))
        img.alpha_composite(gi, (int(g['x'] - gi.width / 2), int(g['y'] - gi.height - 4 + bob)))
    layer(img, lambda d: [d.ellipse([st[n]['x'] - 40, st[n]['y'] - 11, st[n]['x'] + 40, st[n]['y'] + 11], fill=(0, 0, 0, 80)) for n in NAMES if st[n]['out'] is None])
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if s['out'] is not None:
            u = t - s['out']
            if u < 0.35:
                spr = PANIC[n][int(t * 14) % 8]; sink = int(u / 0.35 * 180)
                c = spr.crop((0, 0, spr.width, max(1, FOOT - sink))); img.alpha_composite(c, (int(x - spr.width / 2), int(y - FOOT + sink)))
            else:
                hd = HEAD[n]; bob = int(5 * math.sin(t * 4 + x))
                y = max(SY + 140, min(y, 1500 - 50)); x = max(70 + 50, min((887 if y + 50 > 1110 else 1025) - 50, x))   # rc10: never under the stamp slot   # bobbing heads stay in the zone
                img.alpha_composite(hd, (int(x - hd.width / 2), int(y - hd.height / 2 + bob)))
            continue
        if WIN and t >= T_WIN: spr = STAND[n]
        elif t - s['stun'] < 0.45: spr = PANIC[n][int(t * 14) % 8]
        else:
            ph = int(s['dist'] / 22) % 8; v = math.hypot(s['vx'], s['vy']) or 1
            spr = FRUN[n][ph] if s['vy'] > 0.75 * v else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        if s['buff']:
            col = (255, 210, 60) if s['buff'] == 'mush' else (255, 80, 40)
            layer(img, lambda d, x=x, y=y, col=col: d.ellipse([x - 62, y - 22, x + 62, y + 22], outline=col + (230,), width=6))
            v = math.hypot(s['vx'], s['vy'])
            if s['buff'] == 'mush' and v > 60:          # SPEED!: speed lines + dust trail behind the runner
                ux, uy = s['vx'] / v, s['vy'] / v
                def spl(d, x=x, y=y, ux=ux, uy=uy):
                    for k, oy in enumerate((-160, -110, -60)):
                        x0, y0 = x - ux * 40, y + oy - uy * 20
                        d.line([x0, y0, x0 - ux * (60 + 15 * k), y0 - uy * (60 + 15 * k)], fill=(255, 230, 160, 220), width=5)
                    for k in range(4):
                        r_ = 9 + 5 * k; cx_, cy_ = x - ux * (30 + 26 * k), y - uy * (30 + 26 * k) - 4
                        d.ellipse([cx_ - r_, cy_ - r_ * 0.6, cx_ + r_, cy_ + r_ * 0.6], fill=(230, 210, 170, 150 - 30 * k))
                layer(img, spl)
            if s['buff'] == 'cre':                       # STRONG!: rc10: red/orange power flames rising off the body (no oval: an oval read as the ACV shield)
                def flames(d, x=x, y=y):
                    r3 = random.Random(int(t * 15) + int(x))
                    for k in range(9):
                        fx = x + r3.uniform(-62, 62); fy = y - r3.uniform(20, FOOT - 20); L = r3.uniform(26, 54)
                        c = r3.choice([(255, 80, 40), (255, 140, 40), (255, 200, 80)])
                        d.polygon([(fx - 7, fy), (fx + 7, fy), (fx, fy - L)], fill=c + (215,))
                layer(img, flames)
        if t - s['dash'] < 0.3:
            layer(img, lambda d, x=x, y=y: [d.ellipse([x - 8 - 10 * k - s['vx'] * 0.02 * k, y - 10 - s['vy'] * 0.02 * k, x + 8 + 10 * k - s['vx'] * 0.02 * k, y + 4 - s['vy'] * 0.02 * k], fill=(230, 220, 200, 120 - 30 * k)) for k in range(3)])
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    items = []
    for e in EV:
        u = t - e[0]
        if 0 <= u < 0.8:
            a = int(255 * min(1, (0.8 - u) / 0.3))
            s = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[2]]
            yy = s['y'] - FOOT - 30 - u * 40
            if e[1] == 'shove' and s['buff'] == 'cre':     # rc10: only STRONG shoves get a pop: POW! 52px + orange impact burst (SHOVE! pops cut)
                v = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[3]]; ix, iy = (s['x'] + v['x']) / 2, (s['y'] + v['y']) / 2 - FOOT * 0.45
                if u < 0.35:
                    k_ = 1 - u / 0.35
                    def burst(d, ix=ix, iy=iy, k_=k_):
                        pts = []
                        for j in range(16):
                            rr_ = (95 if j % 2 == 0 else 42) * (0.6 + 0.6 * (1 - k_)); an = j * math.pi / 8
                            pts.append((ix + rr_ * math.cos(an), iy + rr_ * math.sin(an)))
                        d.polygon(pts, fill=(255, 150, 40, int(230 * k_)), outline=(255, 240, 160, int(255 * k_)))
                    layer(img, burst)
                items.append((clampx(s['x'], 4 * 52, yy), max(SY + 104, yy - 20), 'POW!', 52, (255, 120, 50), 8, a))
        if abs(t - e[0]) < 0.5 / FPS:
            out_ev.append((round(e[0], 3), {'shove': 'punch', 'gum': 'powerup_8bit', 'splash': 'boom'}[e[1]]))
    text_layer(img, items)
    # header
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda d: d.rectangle([0, CH0, W, CH1], fill=(12, 8, 24, 170)))   # hfg10: IN/OUT standings on an edge-to-edge strip, no box
    chips = []
    for i, n in enumerate(['joy', 'cyrus', 'cleo', 'ray']):
        sx = 78 + 939 * (i + 0.5) / 4; ic = ICON[n] if st[n]['out'] is None else ImageEnhance.Brightness(ImageEnhance.Color(ICON[n]).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(sx - 90 - ic.width / 2), CH0 + 20))
        out = st[n]['out'] is not None and st[n]['out'] <= t
        chips.append((sx + 22, CH0 + 26, 'OUT' if out else 'IN', 44, (255, 90, 80) if out else (140, 230, 120), 7, 255))   # rc10: 30 -> 44px
        if WIN and t >= T_WIN and n == WIN: layer(img, lambda d, sx=sx: d.ellipse([sx - 130, CH0 + 12, sx - 50, CH0 + 92], outline=(255, 214, 60, 255), width=6))
    text_layer(img, chips)
    if t < 1.8:   # rc10: premise plate over the action (guides already shoving)
        text_layer(img, [(547, SY + 18, 'PICK A PLAYER!', 60, (255, 255, 255), 10, 255)])   # in the stamp slot over open water, not over the guides (first stamp is at 3.2s)   # hfg10: plate + SHOVING ALLOWED cut (the shoving shows)
    for (t1, t2, txt, col) in STAMPS:
        if t1 <= t < t2 and t < T_WIN:
            sc = 1.0 + 0.25 * max(0, 0.12 - (t - t1)) / 0.12; fs_ = int((56 if 'OUT' in txt else 60) * sc)
            text_layer(img, [(547, SY + 46 - fs_ // 2, txt, fs_, col, 10, 255)])   # hfg10: stamp without plate
    if t >= T_WIN:
        u = t - T_WIN
        layer(img, lambda d: d.rectangle([0, CH1 + 6, W, H], fill=(8, 6, 14, int(150 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1170 - vf.height))
        def conf(d):
            r2 = random.Random(f)
            for _ in range(45):
                x, y = r2.uniform(0, W), (r2.uniform(470, H) + u * 500) % H
                d.rectangle([x, y, x + 10, y + 10], fill=r2.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (190, 90, 240)]) + (255,))
        layer(img, conf)
        text_layer(img, [(CX, 1206, LABEL[WIN] + ' WINS!', int(66 * (1 + 0.3 * max(0, 0.12 - u) / 0.12)), (255, 214, 60), 9, 255)])
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN, 3), 'victory'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in BUSY: img.convert('RGB').save(f'f89_{f}.png')
wr.close(); json.dump({'events': out_ev}, open('v89_ev.json', 'w')); print('done', round(END, 2))
