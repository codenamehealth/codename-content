import sys; sys.path.insert(0, '../fork1'); from common import *
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (120, 200, 90), 'cleo': (110, 160, 255), 'cyrus': (255, 160, 50), 'ray': (205, 125, 245)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel'}
LANE_Y = [700, 1000, 1300, 1600]
L = float(os.environ.get('LEN', '5600')); T_START = 2.0
SA, SB, S0 = float(os.environ.get('SA', '235')), float(os.environ.get('SB', '7.0')), -650
def shadow_x(t): return S0 + SA * max(0, t - T_START + 0.5) + SB * max(0, t - T_START + 0.5) ** 2
ATK_D, SLIDE_D = 0.5, 0.45
def sim(seed, dur=30):
    rnd = random.Random(seed); order = G[:]; rnd.shuffle(order)
    lanes = {g: i for i, g in enumerate(order)}
    obs = {}
    for g in G:
        xs = []; x = 500 + rnd.uniform(0, 400)
        while x < L - 400:
            xs.append([x, rnd.choice(['slime', 'slime', 'crate']), None]); x += rnd.uniform(700, 1150)
        obs[g] = xs
    st = {g: dict(x=0.0, mode='run', t0=0, boost=-9, base=rnd.uniform(300, 335), ph=rnd.uniform(0, 6.3), caught=None, done=None, dist=0.0, oi=0) for g in G}
    frames = []; events = []; leaders = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS; sx = shadow_x(t)
        for g in G:
            s = st[g]
            if s['caught'] is not None or s['done'] is not None or t < T_START: continue
            sp = s['base'] * (1 + 0.2 * math.sin(0.8 * t + s['ph']) + 0.1 * math.sin(2.1 * t + s['ph'] * 2))
            if t - s['boost'] < 1.3: sp *= 1.45
            if s['mode'] == 'atk':
                sp = 0
                if t - s['t0'] >= ATK_D: s['mode'] = 'run'; s['boost'] = t
            elif s['mode'] == 'slide':
                sp *= 1.15
                if t - s['t0'] >= SLIDE_D: s['mode'] = 'run'
            o = obs[g][s['oi']] if s['oi'] < len(obs[g]) else None
            if o and s['mode'] == 'run':
                if o[1] == 'slime' and o[0] - s['x'] < 70:
                    s['mode'] = 'atk'; s['t0'] = t; o[2] = t + 0.25; s['oi'] += 1; events.append((t, 'atk', g)); sp = 0
                elif o[1] == 'crate' and o[0] - s['x'] < 90:
                    s['mode'] = 'slide'; s['t0'] = t; o[2] = t + 0.18; s['oi'] += 1; events.append((t, 'slide', g))
            s['x'] += sp * dt; s['dist'] += sp * dt
            if s['x'] >= L: s['done'] = t
            elif s['x'] < sx + 10: s['caught'] = t; events.append((t, 'caught', g))
        alive = [g for g in G if st[g]['caught'] is None]
        if alive:
            ld = max(alive, key=lambda g: st[g]['x'])
            if t > T_START + 1 and (not leaders or leaders[-1] != ld): leaders.append(ld)
        frames.append(({g: dict(x=st[g]['x'], mode=st[g]['mode'], t0=st[g]['t0'], boost=st[g]['boost'], caught=st[g]['caught'], done=st[g]['done'], dist=st[g]['dist']) for g in G}, sx))
        if any(st[g]['done'] is not None for g in G) and t > max(st[g]['done'] or 0 for g in G) + 0.01: break
    return st, frames, events, obs, lanes, leaders
def score(seed):
    st, fr, ev, obs, lanes, ld = sim(seed)
    done = [g for g in G if st[g]['done'] is not None]; caught = sorted(st[g]['caught'] for g in G if st[g]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3: return None
    tw = st[done[0]]['done']
    if not (16 < tw < 20) or caught[0] < 9 or caught[-1] < tw - 3 or len(ld) < 4: return None
    return done[0], round(tw, 1), [round(c, 1) for c in caught], len(ld)
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
ST, FR, EV, OBS, LANES, LD = sim(SEED)
WIN = [g for g in G if ST[g]['done'] is not None][0]; T_WIN = ST[WIN]['done']
print('winner', WIN, T_WIN, {g: ST[g]['caught'] for g in G}, LD)
# ---------------- assets
RUN = {g: seq(PL + f'race/{g}_run', 3, 1) for g in G}
ATK = {g: seq(PL + f'race/{g}_atk', 3, 1) for g in G}
SLD = {g: seq(PL + f'maze/anim/{g}_slide', 3, 1, 8) for g in G}
PAN = {g: seq(PL + f'maze/anim/{g}_panic', 3, 1) for g in G}
def nored(im):
    a = np.array(im); r, g_, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g_ < 110) & (b < 140)] = 0; return Image.fromarray(a)
SLI = [up(nored(Image.open(p).convert('RGBA')), 3) for p in sorted(glob.glob(PL + 'race/slime_idle_c/*.png'))]
SLS = [up(nored(Image.open(p).convert('RGBA')), 3) for p in sorted(glob.glob(PL + 'race/slime_splat_c/*.png'))]
CRATE = up(crop(Image.open('gen/crate/00.png').convert('RGBA')), 3)
FLAG = up(crop(Image.open('gen/flag/00.png').convert('RGBA')), 3)
GUMS = {g: gummy(GK[g], 3) for g in G}
ICON = {}
for g in G:
    im = idle(g, 1)[0]; bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2; ICON[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
VICF = vic(WIN, 380)
meta = json.load(open('gen/roof_meta.json')); sheet = Image.open('gen/roof_sheet.png').convert('RGBA')
TL = {}
for t in meta['tileset_data']['tiles']:
    bb = t['bounding_box']; TL[t['name']] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + 32, bb['y'] + 32)), 2)
TOP, MID, BOT, TL_, TR_, ML_, MR_, BL_, BR_ = TL['wang_12'], TL['wang_0'], TL['wang_3'], TL['wang_14'], TL['wang_13'], TL['wang_10'], TL['wang_5'], TL['wang_11'], TL['wang_7']
hub = Image.open(A + 'hub.gif'); BGF = []
for i in range(0, hub.n_frames, 3):
    hub.seek(i); f = hub.convert('RGB').resize((3413, 1920), Image.NEAREST)
    a = np.array(f).astype(float); a *= np.array([0.62, 0.42, 0.52]); BGF.append(Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'))
X0W, X1W = -900, L + 600
def lane_strip():
    w_ = int(X1W - X0W) // 64 * 64 + 64; im = Image.new('RGBA', (w_, 192), (0, 0, 0, 0))
    for x in range(0, w_, 64):
        e = 0 if x == 0 else (2 if x == w_ - 64 else 1)
        im.alpha_composite([TL_, TOP, TR_][e], (x, 0)); im.alpha_composite([ML_, MID, MR_][e], (x, 64)); im.alpha_composite([BL_, BOT, BR_][e], (x, 128))
    return im
STRIP = lane_strip()
FOOT = 78 * 3
END = T_WIN + 3.4; NF = int(END * FPS)
w = Writer('v63_noaudio.mp4'); out_ev = []; cam = None; eyes = [(random.Random(i).uniform(0, 1), random.Random(i + 50).uniform(380, 1700)) for i in range(14)]
for f in range(NF):
    t = f / FPS; st, sx = FR[min(f, len(FR) - 1)]
    alive = [g for g in G if not (st[g]['caught'] is not None and st[g]['caught'] <= t)]
    lead_x = max(st[g]['x'] for g in G) if t < T_WIN else st[WIN]['x']
    last_x = min(st[g]['x'] for g in alive) if alive else lead_x
    target = max(min(lead_x - 760, last_x - 160), lead_x - 940, X0W)
    cam = target if cam is None else cam + (target - cam) * 0.12
    img = BGF[int(t * 4) % len(BGF)].crop((int(600 + cam * 0.12), 0, int(600 + cam * 0.12) + W, H))
    for li, ly in enumerate(LANE_Y):
        sxs = int(X0W - cam); sx0 = max(0, -sxs)
        img.alpha_composite(STRIP.crop((sx0, 0, min(STRIP.width, sx0 + W + 64), 192)), (max(0, sxs), ly - 38))
    # finish flags
    for li, ly in enumerate(LANE_Y):
        fx = L - cam + 40
        if -200 < fx < W + 200: img.alpha_composite(FLAG, (int(fx - FLAG.width / 2), ly - FLAG.height + 6))
    # obstacles
    for g in G:
        ly = LANE_Y[LANES[g]]
        for (ox, kind, thit) in OBS[g]:
            px = ox - cam
            if px < -150 or px > W + 150: continue
            if kind == 'slime':
                if thit is None or t < thit: s = SLI[int(t * 8) % len(SLI)]; img.alpha_composite(s, (int(px - s.width / 2), ly - s.height + 6 + 30))
                elif t - thit < 0.45: s = SLS[min(len(SLS) - 1, int((t - thit) / 0.45 * len(SLS)))]; img.alpha_composite(s, (int(px - s.width / 2), ly - s.height + 6 + 30))
                if thit is not None and 0 <= t - thit < 0.7:
                    gm = GUMS[g]; u = (t - thit) / 0.7
                    img.alpha_composite(gm, (int(px - gm.width / 2 - 60 * u), int(ly - 170 - 110 * math.sin(u * math.pi))))
            else:
                if thit is None or t < thit: img.alpha_composite(CRATE, (int(px - CRATE.width / 2), ly - CRATE.height + 8))
                elif t - thit < 0.5:
                    u = (t - thit) / 0.5
                    def splint(d, px=px, ly=ly, u=u):
                        for k in range(8):
                            a = k * 0.8; r = 20 + 120 * u
                            d.rectangle([px + r * math.cos(a) - 7, ly - 40 - r * math.sin(a) * 0.8 + 140 * u * u - 6, px + r * math.cos(a) + 7, ly - 40 - r * math.sin(a) * 0.8 + 140 * u * u + 6], fill=(150, 100, 55, int(255 * (1 - u))))
                    layer(img, splint)
    # runners
    for g in G:
        s = st[g]; ly = LANE_Y[LANES[g]]; px = s['x'] - cam
        if s['caught'] is not None and s['caught'] <= t:
            u = t - s['caught']
            if u < 1.4:
                fr = PAN[g][int(t * 10) % len(PAN[g])]; dk = ImageEnhance.Brightness(fr).enhance(max(0.15, 1 - u * 0.7))
                img.alpha_composite(dk, (int(px - dk.width / 2), ly - FOOT))
            continue
        if t < T_START or (t >= T_WIN and g != WIN):
            fr = RUN[g][0]
        elif g == WIN and t >= T_WIN: continue
        elif s['mode'] == 'atk': fr = ATK[g][min(len(ATK[g]) - 1, int((t - s['t0']) / ATK_D * len(ATK[g])))]
        elif s['mode'] == 'slide': fr = SLD[g][min(6, int((t - s['t0']) / SLIDE_D * 7))]
        else: fr = RUN[g][int(s['dist'] / 34) % 8]
        boosted = t - s['boost'] < 1.3
        if boosted:
            def trail(d, px=px, ly=ly, g=g):
                for k in range(5): d.rectangle([px - 90 - k * 40, ly - 130 + k * 8, px - 64 - k * 40, ly - 122 + k * 8], fill=COL[g] + (200 - k * 35,))
            layer(img, trail)
        if s['mode'] == 'atk' and t >= T_START: img.alpha_composite(fr, (int(px - 46 * 3 - 14 * 3), ly - FOOT - 26 * 3))
        else: img.alpha_composite(fr, (int(px - fr.width / 2), ly - FOOT))
        if boosted and t - s['boost'] < 0.9:
            text_layer(img, [(px, ly - 250 - (t - s['boost']) * 40, 'BOOST!', 26, COL[g], 4, int(255 * min(1, (0.9 - (t - s['boost'])) / 0.3)))])
    # the shadow
    ssx = sx - cam
    if ssx > -120:
        def shade(d):
            for y in range(380, 1770, 12):
                ex = ssx + 26 * math.sin(y / 70 + t * 4) + 14 * math.sin(y / 23 - t * 7)
                if ex > 0: d.rectangle([0, y, ex, y + 12], fill=(18, 6, 34, 235))
                for k in range(1, 6):
                    if ex + k * 14 > 0: d.rectangle([max(0, ex + (k - 1) * 14), y, ex + k * 14, y + 12], fill=(40, 12, 70, 200 - k * 36))
        layer(img, shade)
        d = ImageDraw.Draw(img)
        for i, (fx, fy) in enumerate(eyes):
            ex = ssx - 60 - fx * 500 + 20 * math.sin(t * 2 + i)
            if 0 < ex < ssx - 30 and (int(t * 3 + i) % 7) != 0:
                d.rectangle([ex - 14, fy, ex - 4, fy + 10], fill=(235, 225, 255)); d.rectangle([ex + 6, fy, ex + 16, fy + 10], fill=(235, 225, 255))
    # caught tags
    for g in G:
        s = st[g]
        if s['caught'] is not None and 0 <= t - s['caught'] < 1.6:
            text_layer(img, [(max(140, s['x'] - cam + 40), LANE_Y[LANES[g]] - 270, 'CAUGHT!', 30, (240, 90, 90), 5, int(255 * min(1, (1.6 - (t - s['caught'])) / 0.3)))])
    # header + roster
    layer(img, lambda d: (d.rectangle([0, 80, W, 330], fill=(12, 10, 26, 215)), d.rectangle([0, 1785, W, 1915], fill=(12, 10, 26, 215))))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 115, 'CHOOSE YOUR GUIDE', F(56), (255, 255, 255), 6)
    ctext(d, W / 2, 200, 'OUTRUN THE SHADOW', F(44), (190, 120, 255), 6)
    ctext(d, W / 2, 270, 'Rooftop run', F(26), (232, 182, 76), 4)
    for i, g in enumerate(G):
        x = W * (i + 0.5) / 4; ic = ICON[g]; s = st[g]
        caught = s['caught'] is not None and s['caught'] <= t
        if caught: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.5)
        img.alpha_composite(ic, (int(x - 120), 1802))
        d = ImageDraw.Draw(img); d.rectangle([x - 120, 1802, x - 120 + ic.width, 1802 + ic.height], outline=COL[g], width=3)
        d.text((x - 20, 1835), NAME[g] if g != 'ray' else 'RAY', font=F(24), fill=COL[g] if not caught else (110, 100, 120), stroke_width=3, stroke_fill=(20, 15, 35))
        if caught:
            d.line([x - 116, 1806, x - 28, 1894], fill=(230, 50, 50), width=8); d.line([x - 116, 1894, x - 28, 1806], fill=(230, 50, 50), width=8)
        if t >= T_WIN and g == WIN: d.rectangle([x - 126, 1796, x + 110, 1906], outline=(255, 214, 60), width=6)
    # lane labels
    for g in G:
        ly = LANE_Y[LANES[g]]; gm = GUMS[g]
    if t < T_START:
        n = 3 - int(t / (T_START / 3)); txt = str(n) if n > 0 else 'GO!'
        text_layer(img, [(W / 2, 520, txt, 110, (255, 255, 255), 9, 255)])
    elif t < T_START + 0.6: text_layer(img, [(W / 2, 520, 'GO!', 110, (255, 214, 60), 9, int(255 * (1 - (t - T_START) / 0.6)))])
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, 330, W, 1785], fill=(8, 6, 14, int(160 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, W / 2, 1230, NAME[WIN] + ' ESCAPED!', F(58), (255, 214, 60), 8)
        ctext(d, W / 2, 1330, 'Did your guide win?', F(36), (255, 255, 255), 5)
    w.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/q63_{f:04d}.png')
w.close()
for (te, kind, g) in EV:
    if kind == 'atk': out_ev.append((round(te + 0.2, 3), {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'sword_swish', 'cyrus': 'punch'}[g])); out_ev.append((round(te + 0.3, 3), 'squish')); out_ev.append((round(te + 0.55, 3), 'coin_8bit'))
    elif kind == 'slide': out_ev.append((round(te, 3), 'whoosh_8bit')); out_ev.append((round(te + 0.18, 3), 'crunch_8bit'))
    elif kind == 'caught': out_ev.append((round(te, 3), 'poofpops'))
out_ev += [(0.0, 'tick_8bit'), (T_START / 3, 'tick_8bit'), (2 * T_START / 3, 'tick_8bit'), (T_START, 'go_8bit'), (round(T_WIN, 3), 'victory')]
out_ev = [e for e in out_ev if e[0] < END]
json.dump(out_ev, open('v63_ev.json', 'w')); print('done', END)
