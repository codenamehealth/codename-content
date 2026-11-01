import sys; sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
sys.path.insert(0, '../../fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, '../../fork_rc2'); from rc2 import acv_gloss, acv_tag
B6 = '../../fork_b6/'
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (120, 200, 90), 'cleo': (110, 160, 255), 'cyrus': (255, 160, 50), 'ray': (205, 125, 245)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel'}
HOOK, HB = hook_layer2(['CHOOSE YOUR', 'GUIDE'], accent=1, sub='COMMENT YOUR PICK', sub_max=48)   # rc16: comment prompt >=44px in the band from frame 0
RY = HB + 8   # roster row under the hook
RH = 150      # roster: 3x faces + 40px names under them (was 24px names beside them)
LANE_Y = [975, 1148, 1322, 1495]
L = float(os.environ.get('LEN', '4200')); T_START = 0.3
SA, SB, S0 = float(os.environ.get('SA', '235')), float(os.environ.get('SB', '7.0')), float(os.environ.get('S0', '-650'))
def shadow_x(t): return S0 + SA * max(0, t - T_START + 0.5) + SB * max(0, t - T_START + 0.5) ** 2
ATK_D, SLIDE_D = 0.5, 0.45
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'cre': ('STRONG!', (90, 160, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
SPEED_T, STRONG_T, SLEEP_T = 2.0, 8.0, 1.0       # STRONG holds until it smashes the next obstacle
FLY = 0.35
def sim(seed, dur=30):
    rnd = random.Random(seed); order = G[:]; rnd.shuffle(order)
    lanes = {g: i for i, g in enumerate(order)}
    obs = {}
    for g in G:
        xs = []; x = 500 + rnd.uniform(0, 400)
        while x < L - 400:
            xs.append([x, rnd.choice(['slime', 'slime', 'crate']), None, None]); x += rnd.uniform(700, 1150)
        cand = [o for o in xs if o[1] == 'slime' and 900 < o[0] < L - 1600]
        if not cand: cand = [o for o in xs if o[1] == 'slime']
        if not cand: xs[1][1] = 'slime'; cand = [xs[1]]
        rnd.choice(cand)[3] = GK[g]          # this slime carries the guide's guild gummy
        obs[g] = xs
    st = {g: dict(x=0.0, mode='run', t0=0, boost=-9, strong=-9, shield=False, sleep=-9, fire=None, base=rnd.uniform(300, 335), ph=rnd.uniform(0, 6.3), caught=None, done=None, dist=0.0, oi=0) for g in G}
    frames = []; events = []; leaders = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS; sx = shadow_x(t)
        for g in G:
            s = st[g]
            if s['caught'] is not None or s['done'] is not None or t < T_START: continue
            if s['fire'] is not None and t >= s['fire'][0] and t >= s['sleep']:
                kd = s['fire'][1]; s['fire'] = None; events.append((t, 'pick', g, kd))
                if kd == 'mush': s['boost'] = t
                elif kd == 'cre': s['strong'] = t
                elif kd == 'acv': s['shield'] = True
                else:
                    vic = []
                    for m in G:
                        o = st[m]
                        if m == g or o['caught'] is not None or o['done'] is not None: continue
                        if o['shield']: o['shield'] = False; events.append((t, 'block', m, g))
                        else: o['sleep'] = t + SLEEP_T; vic.append(m)
                    events.append((t, 'sleepwave', g, vic))
            if t < s['sleep']:
                sp = 0.0
            else:
                sp = s['base'] * (1 + 0.2 * math.sin(0.8 * t + s['ph']) + 0.1 * math.sin(2.1 * t + s['ph'] * 2))
                if t - s['boost'] < SPEED_T: sp *= 1.6
                if s['mode'] == 'atk':
                    sp = 0
                    if t - s['t0'] >= ATK_D: s['mode'] = 'run'
                elif s['mode'] == 'slide':
                    sp *= 1.15
                    if t - s['t0'] >= SLIDE_D: s['mode'] = 'run'
                o = obs[g][s['oi']] if s['oi'] < len(obs[g]) else None
                if o and s['mode'] == 'run':
                    strong = t - s['strong'] < STRONG_T
                    if strong and o[0] - s['x'] < 90:
                        o[2] = t; s['oi'] += 1; events.append((t, 'smash', g, o[1])); s['strong'] = -9
                        if o[3]: s['fire'] = (t + FLY, o[3])
                    elif o[1] == 'slime' and o[0] - s['x'] < 70:
                        s['mode'] = 'atk'; s['t0'] = t; o[2] = t + 0.25; s['oi'] += 1; events.append((t, 'atk', g)); sp = 0
                        if o[3]: s['fire'] = (t + 0.25 + FLY, o[3])
                    elif o[1] == 'crate' and o[0] - s['x'] < 90:
                        s['mode'] = 'slide'; s['t0'] = t; o[2] = t + 0.18; s['oi'] += 1; events.append((t, 'slide', g))
            s['x'] += sp * dt; s['dist'] += sp * dt
            if s['x'] >= L: s['done'] = t
            elif s['x'] < sx + 10:
                if s['shield']:
                    s['shield'] = False; s['x'] = sx + 240; s['sleep'] = -9; s['mode'] = 'run'; events.append((t, 'block', g, 'wave'))
                else: s['caught'] = t; events.append((t, 'caught', g))
        alive = [g for g in G if st[g]['caught'] is None]
        if alive:
            ld = max(alive, key=lambda g: st[g]['x'])
            if t > T_START + 1 and (not leaders or leaders[-1] != ld): leaders.append(ld)
        frames.append(({g: dict(x=st[g]['x'], mode=st[g]['mode'], t0=st[g]['t0'], boost=st[g]['boost'], strong=st[g]['strong'], shield=st[g]['shield'], sleep=st[g]['sleep'], caught=st[g]['caught'], done=st[g]['done'], dist=st[g]['dist']) for g in G}, sx))
        if any(st[g]['done'] is not None for g in G) and t > max(st[g]['done'] or 0 for g in G) + 0.01: break
    return st, frames, events, obs, lanes, leaders
def score(seed):
    # rc16 review targets: Joy escapes ~12.5-14.5s; first catch ~4.5-7s, then one every ~2-4s; Joy's SHIELD absorbs an EARLIER
    # hit (not what saves her at the line); the wave stays within ~900px of the leader so it can stay on screen
    st, fr, ev, obs, lanes, ld = sim(seed, 18)
    done = [g for g in G if st[g]['done'] is not None]; caught = sorted(st[g]['caught'] for g in G if st[g]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3 or done[0] != os.environ.get('WANT', 'joy'): return None
    tw = st[done[0]]['done']
    if not (12.3 < tw < 14.6) or not (4.3 < caught[0] < 7.2) or len(ld) < 3: return None
    gaps = (caught[1] - caught[0], caught[2] - caught[1])
    if min(gaps) < 1.8 or max(gaps) > 4.2 or not (0.3 < tw - caught[-1] < 2.2): return None
    picks = [e for e in ev if e[1] == 'pick' and e[0] < tw]
    if len(picks) < 4: return None
    jb = [e[0] for e in ev if e[1] == 'block' and e[2] == 'joy']
    if not jb or min(jb) > tw - 3.0 or any(b_ > tw - 3.0 for b_ in jb): return None
    sw = [e for e in ev if e[1] == 'sleepwave']
    if not sw or len(sw[0][3]) + sum(1 for b in ev if b[1] == 'block' and abs(b[0] - sw[0][0]) < 0.01) < 2: return None
    nsm = sum(e[1] == 'smash' for e in ev)
    if nsm < 1: return None
    gap = max(max(f[0][g]['x'] for g in G if f[0][g]['caught'] is None) - f[1] for f in fr[int(1.5 * FPS):int(tw * FPS)])
    if gap > float(os.environ.get('MAXGAP', '950')): return None
    stt = sorted(e[0] for e in ev if e[1] in ('pick', 'smash', 'block', 'caught') and e[0] <= tw)
    clash = sum(1 for i in range(len(stt) - 1) if stt[i + 1] - stt[i] < 0.7)
    return clash, round(tw, 1), [round(c, 1) for c in caught], round(gap), len(ld), [(round(e[0], 1), e[2], e[3]) for e in picks], [round(x, 1) for x in jb], nsm
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
ST, FR, EV, OBS, LANES, LD = sim(SEED)
WIN = [g for g in G if ST[g]['done'] is not None][0]; T_WIN = ST[WIN]['done']
print('winner', WIN, T_WIN, {g: ST[g]['caught'] for g in G}, LD)
for e in EV:
    if e[1] not in ('atk', 'slide'): print('  ', round(e[0], 2), e[1:])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()
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
CRATE = up(crop(Image.open(B6 + 'gen/crate/00.png').convert('RGBA')), 3)
FLAG = up(crop(Image.open(B6 + 'gen/flag/00.png').convert('RGBA')), 3)
GUMS = {g: gummy(GK[g], 3) for g in G}
ICON = {}
for g in G:
    im = idle(g, 1)[0]; bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2; ICON[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
VICF = vic(WIN, 380)
meta = json.load(open(B6 + 'gen/roof_meta.json')); sheet = Image.open(B6 + 'gen/roof_sheet.png').convert('RGBA')
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
# ---------------- render (content pass): slime wave chaser, gummy powers, stamps, loop
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
def fade(im, a):
    if a >= 1: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda p: int(p * a))); return im
def safe_alpha(px_right, ly):
    """objects in the lower lanes fade in only once they are fully left of the lower-right button area"""
    if ly <= 1110: return 1.0
    return max(0.0, min(1.0, (887 - px_right) / 70))
GUMG = {k: gummy(k, 3) for k in POWER}
GUMG['acv'] = up(acv_gloss(Image.open(PL + 'gummies/pick_acv.png').convert('RGBA')), 3)   # rc16: gummy gloss on Syeda's ACV gummy
GY = 160   # gummy height above the lane (was 190; lanes are closer now)
ACV_SEEN = [None]
T_CARD = T_WIN + 0.6; T_LOOP = T_CARD + 1.3; END = T_LOOP + 0.2; NF = int(round(END * FPS))   # rc16: card hold 2.6 -> 1.3s, loop cut 0.2s
PICKS = {e[2]: e for e in EV if e[1] == 'pick'}
SLEEPW = [e for e in EV if e[1] == 'sleepwave']
BLOCKW = {e[2]: e[0] for e in EV if e[1] == 'block' and e[3] == 'wave'}
CAUGHT = [e for e in EV if e[1] == 'caught']
POPS = []
for e in EV:
    if e[0] > T_WIN: continue
    if e[1] == 'pick': POPS.append((e[0], e[2], POWER[e[3]][0], POWER[e[3]][1], 50))
    elif e[1] == 'smash': POPS.append((e[0], e[2], 'SMASH!', (255, 255, 255), 50))
    elif e[1] == 'block': POPS.append((e[0], e[2], 'BLOCKED!', (110, 230, 90), 46))
FACES = [(i * 0.137 % 1, RY + RH + 50 + i * 108 + 24 * math.sin(i * 2.1)) for i in range(7)]
# rc16: one stamp at a time. CAUGHT stamps name the guide and sit on that guide's lane; ESCAPED! at the win; power pops queue
# behind them (a pop that would wait more than 0.6s is dropped, a CAUGHT/ESCAPED stamp cuts a running pop short)
def SN(g): return 'RAY' if g == 'ray' else NAME[g]
_raw = [(e[0], 2, 0.8, ('caught', e[2], SN(e[2]) + ' CAUGHT!', (255, 95, 95))) for e in CAUGHT if e[0] <= T_WIN]
_raw += [(T_WIN, 3, T_CARD - T_WIN, ('win', WIN, 'ESCAPED!', (255, 214, 60)))]
_raw += [(t0, 1.5 if text in ('SPEED!', 'SLEEP!', 'STRONG!', 'SHIELD!') else 1, 0.7, ('pop', g, text, col)) for t0, g, text, col, size in POPS]
SCHED = []
for t0, pr, du, it in sorted(_raw, key=lambda r: (r[0], -r[1])):
    st0 = t0
    if SCHED and SCHED[-1][1] > t0:
        ps, pe, ppr, pit = SCHED[-1]
        if pr > ppr:
            if ppr == 1.5 and pr == 2 and ps + 0.6 - t0 <= 0.45:      # let a power label finish ~0.6s, the CAUGHT stamp waits a moment
                st0 = max(t0, ps + 0.6); SCHED[-1] = (ps, st0, ppr, pit)
            elif t0 - ps < 0.3: SCHED.pop()
            else: SCHED[-1] = (ps, t0, ppr, pit)
        else: st0 = pe
    if pr < 2 and st0 - t0 > 0.6: print('dropped pop', round(t0, 2), it); continue
    SCHED.append((st0, st0 + du, pr, it))
print('stamps', [(round(a, 2), round(b, 2), it[2]) for a, b, pr, it in SCHED])
def acv_side(img, gx, gy, a):
    # 'ACV GUMMY' 44px tag on a dark plate to the RIGHT of the gummy, pointer to it (keeps clear of the roster above lane 0)
    L2 = Image.new('RGBA', img.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(L2); tag = 'ACV GUMMY'; f = F(44); tw = d2.textlength(tag, font=f)
    x0 = gx + 62; y0 = gy - 36
    if x0 + tw + 36 > 875: x0 = gx - 62 - tw - 36
    d2.rounded_rectangle([x0, y0, x0 + tw + 36, y0 + 72], 14, fill=(14, 10, 24, int(235 * a / 255)), outline=(90, 200, 80, a), width=5)
    if x0 > gx: d2.polygon([(x0 + 2, gy - 14), (x0 + 2, gy + 14), (gx + 40, gy)], fill=(90, 200, 80, a))
    else: d2.polygon([(x0 + tw + 34, gy - 14), (x0 + tw + 34, gy + 14), (gx - 40, gy)], fill=(90, 200, 80, a))
    d2.text((x0 + 18, y0 + 14), tag, font=f, fill=(255, 255, 255, a), stroke_width=5, stroke_fill=(10, 6, 18, a))
    img.alpha_composite(L2)
w = Writer('v63_noaudio.mp4'); out_ev = []; cam = None
for f in range(NF):
    t = f / FPS; loopcut = t >= T_LOOP
    if loopcut: t = 0.0
    fi = int(round(t * FPS)); st, sx = FR[min(fi, len(FR) - 1)]; ACV_TAG = []
    alive = [g for g in G if not (st[g]['caught'] is not None and st[g]['caught'] <= t)]
    lead_x = max(st[g]['x'] for g in G) if t < T_WIN else st[WIN]['x']
    last_x = min(st[g]['x'] for g in alive) if alive else lead_x
    target = max(min(lead_x - 600, last_x - 160), lead_x - 700, X0W)
    if t < T_WIN: target = max(min(lead_x - 600, last_x - 160, sx - 130), lead_x - 800, X0W)   # rc16: keep the wave's edge in view
    cam = target if (cam is None or loopcut) else cam + (target - cam) * 0.12
    img = BGF[int(t * 4) % len(BGF)].crop((int(600 + cam * 0.12), 0, int(600 + cam * 0.12) + W, H))
    for li, ly in enumerate(LANE_Y):
        sxs = int(X0W - cam); sx0 = max(0, -sxs)
        img.alpha_composite(STRIP.crop((sx0, 0, min(STRIP.width, sx0 + W + 64), 192)), (max(0, sxs), ly - 38))
    for li, ly in enumerate(LANE_Y):
        fx = L - cam + 40
        if -200 < fx < W + 200:
            a = safe_alpha(fx + FLAG.width / 2, ly)
            if a > 0: img.alpha_composite(fade(FLAG, a), (int(fx - FLAG.width / 2), ly - FLAG.height + 6))
    # obstacles (the gummy slime carries its gummy on its head)
    for g in G:
        ly = LANE_Y[LANES[g]]
        for (ox, kind, thit, gk) in OBS[g]:
            px = ox - cam
            if px < -150 or px > W + 150: continue
            if kind == 'slime':
                if thit is None or t < thit:
                    s_ = SLI[int(t * 8) % len(SLI)]; a = safe_alpha(px + s_.width / 2, ly)
                    if a > 0:
                        img.alpha_composite(fade(s_, a), (int(px - s_.width / 2), ly - s_.height + 6 + 30))
                        if gk:
                            gm = GUMG[gk]; bob = 8 * math.sin(t * 5 + ox)
                            layer(img, lambda dd, px=px, ly=ly, bob=bob, gk=gk, a=a: [dd.ellipse([px - 46 + k_ * 9, ly - GY + bob - 40 + k_ * 9, px + 46 - k_ * 9, ly - GY + bob + 40 - k_ * 9], fill=POWER[gk][1] + (int((40 + k_ * 30) * a),)) for k_ in range(3)])
                            img.alpha_composite(fade(gm, a), (int(px - gm.width / 2), int(ly - GY + bob - gm.height / 2)))
                            if gk == 'acv' and a > 0.9 and 80 < px < 860:
                                if ACV_SEEN[0] is None: ACV_SEEN[0] = t
                                if t - ACV_SEEN[0] < 1.8: ACV_TAG.append((int(px), int(ly - GY + bob - gm.height / 2 - 6), int(255 * min(1, (1.8 - (t - ACV_SEEN[0])) / 0.3))))
                elif t - thit < 0.45: s_ = SLS[min(len(SLS) - 1, int((t - thit) / 0.45 * len(SLS)))]; img.alpha_composite(s_, (int(px - s_.width / 2), ly - s_.height + 6 + 30))
            else:
                if thit is None or t < thit:
                    a = safe_alpha(px + CRATE.width / 2, ly)
                    if a > 0: img.alpha_composite(fade(CRATE, a), (int(px - CRATE.width / 2), ly - CRATE.height + 8))
                elif t - thit < 0.5:
                    u = (t - thit) / 0.5
                    def splint(d, px=px, ly=ly, u=u):
                        for k in range(8):
                            a_ = k * 0.8; r = 20 + 120 * u
                            d.rectangle([px + r * math.cos(a_) - 7, ly - 40 - r * math.sin(a_) * 0.8 + 140 * u * u - 6, px + r * math.cos(a_) + 7, ly - 40 - r * math.sin(a_) * 0.8 + 140 * u * u + 6], fill=(150, 100, 55, int(255 * (1 - u))))
                    layer(img, splint)
    # gummies flying from the popped slime to the guide
    for g, e in PICKS.items():
        o = next(o for o in OBS[g] if o[3])
        if o[2] is None or t < o[2] or t >= e[0]: continue
        ly = LANE_Y[LANES[g]]; s = st[g]; u = min(1, (t - o[2]) / FLY)
        x0_, y0_ = o[0] - cam, ly - GY; x1_, y1_ = s['x'] - cam, ly - 230
        gx_, gy_ = x0_ + (x1_ - x0_) * u, y0_ + (y1_ - y0_) * u - 120 * math.sin(u * math.pi) + (6 * math.sin(t * 6) if u >= 1 else 0)
        gm = GUMG[e[3]]; img.alpha_composite(gm, (int(gx_ - gm.width / 2), int(gy_ - gm.height / 2)))
    for e in EV:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.6:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.6
            px_, py_ = s0['x'] - cam, LANE_Y[LANES[e[2]]] - 130; col = POWER[e[3]][1]
            layer(img, lambda dd, px_=px_, py_=py_, u=u, col=col: [dd.rectangle([px_ + (30 + 140 * u) * math.cos(q * 0.628) - 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) - 7, px_ + (30 + 140 * u) * math.cos(q * 0.628) + 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    for e in SLEEPW:
        if 0 <= t - e[0] < 0.7:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
            px_, py_ = s0['x'] - cam, LANE_Y[LANES[e[2]]] - 130
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.ellipse([px_ - r_, py_ - r_, px_ + r_, py_ + r_], outline=(190, 120, 255, int(230 * (1 - u))), width=14) for r_ in (60 + 1400 * u, 20 + 1000 * u)])
    ssx = sx - cam - (max(0.0, t - T_WIN) ** 1.5) * 900     # the wave falls back once someone escapes
    # runners
    for g in G:
        s = st[g]; ly = LANE_Y[LANES[g]]; px = s['x'] - cam
        if g in BLOCKW and 0 <= t - BLOCKW[g] < 0.25: px -= 240 * (1 - (t - BLOCKW[g]) / 0.25)
        if s['caught'] is not None and s['caught'] <= t:
            u = t - s['caught']; px = min(px, ssx - 40)            # swallowed: carried along inside the wave
            if u < 1.4:
                fr = PAN[g][int(t * 10) % len(PAN[g])]; dk = ImageEnhance.Brightness(fr).enhance(max(0.15, 1 - u * 0.7))
                img.alpha_composite(dk, (int(px - dk.width / 2), ly - FOOT))
            continue
        asleep = t < s['sleep']
        if t < T_START or (t >= T_WIN and g != WIN) or asleep:
            fr = RUN[g][0]
        elif g == WIN and t >= T_WIN:
            if t >= T_CARD: continue
            fr = RUN[g][0]; ly = ly - int(abs(math.sin((t - T_WIN) * 7)) * 40)     # happy hops at the flag
        elif s['mode'] == 'atk': fr = ATK[g][min(len(ATK[g]) - 1, int((t - s['t0']) / ATK_D * len(ATK[g])))]
        elif s['mode'] == 'slide': fr = SLD[g][min(6, int((t - s['t0']) / SLIDE_D * 7))]
        else: fr = RUN[g][int(s['dist'] / 34) % 8]
        boosted = t - s['boost'] < SPEED_T and not asleep
        strong = t - s['strong'] < STRONG_T
        atk = s['mode'] == 'atk' and t >= T_START and not asleep
        x0, y0 = (int(px - 46 * 3 - 14 * 3), ly - FOOT - 26 * 3) if atk else (int(px - fr.width / 2), ly - FOOT)
        if boosted:
            for q in range(3):
                img.alpha_composite(tinted(fr, (255, 170, 50), int(255 * (0.34 - 0.09 * q))), (x0 - (q + 1) * 34, y0))
            layer(img, lambda dd: [dd.rectangle([px - 200 - 30 * q - (q * 37 + int(t * 90)) % 50, ly - 170 + q * 34 - 4, px - 90 - 30 * q, ly - 170 + q * 34 + 4], fill=(255, 240, 200, 210)) for q in range(4)] +
                                  [dd.ellipse([px - 60 - q * 34 - 18, ly - 18 - q * 5, px - 60 - q * 34 + 18, ly + 6], fill=(210, 190, 150, 170 - q * 45)) for q in range(3)])
        if strong:
            tt = tinted(fr, (90, 160, 255), int(170 + 70 * math.sin(t * 14)))
            for ox, oy in ((-7, 0), (7, 0), (0, -7), (0, 7), (-5, -5), (5, 5), (-5, 5), (5, -5)): img.alpha_composite(tt, (x0 + ox, y0 + oy))
        img.alpha_composite(fr, (x0, y0))
        if asleep:
            img.alpha_composite(tinted(fr, (40, 20, 90), 120), (x0, y0))
            u = t - (s['sleep'] - SLEEP_T)
            text_layer(img, [(px + 50 + 22 * kz, ly - 230 - ((u * 1.4 + kz * 0.33) % 1) * 60 - kz * 16, 'Z', 36 + 10 * kz, (225, 205, 255), 6, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
        if s['shield']:
            layer(img, lambda dd: (dd.ellipse([px - 105, ly - 250, px + 105, ly + 16], fill=(110, 230, 90, 28), outline=(150, 255, 120, 235), width=7),
                                   dd.arc([px - 78, ly - 226, px - 18, ly - 150], 200, 260, fill=(230, 255, 220, 230), width=6)))
        if g in BLOCKW and 0 <= t - BLOCKW[g] < 0.5:
            u = (t - BLOCKW[g]) / 0.5
            layer(img, lambda dd: [dd.rectangle([px + (110 + 120 * u) * math.cos(q * 0.524) - 8, ly - 117 + (135 + 100 * u) * math.sin(q * 0.524) - 8, px + (110 + 120 * u) * math.cos(q * 0.524) + 8, ly - 117 + (135 + 100 * u) * math.sin(q * 0.524) + 8], fill=(150, 255, 120, int(255 * (1 - u)))) for q in range(12)])
    # the SLIME WAVE (clearly not the Hollow: a bright green wall of goo full of slimes)
    if ssx > -160:
        def goo(d):
            for y in range(RY + RH + 4, 1700, 10):
                ex = ssx + 30 * math.sin(y / 90 + t * 3) + 14 * math.sin(y / 31 - t * 6)
                if ex <= 0: continue
                if ex > 46: d.rectangle([0, y, ex - 46, y + 10], fill=(52, 140, 44, 248))
                if ex > 18: d.rectangle([max(0, ex - 46), y, ex - 18, y + 10], fill=(92, 190, 64, 250))
                d.rectangle([max(0, ex - 18), y, ex, y + 10], fill=(150, 232, 104, 250))
                d.rectangle([max(0, ex), y, ex + 6, y + 10], fill=(30, 80, 30, 230))
            for k in range(16):                             # bubbles inside the goo
                by = RY + RH + 20 + ((k * 151 - t * 90) % (1700 - RY - RH - 20)); bx = ssx - 60 - (k * 97) % 420
                if bx > 10: d.ellipse([bx - 10 - k % 3 * 4, by - 10 - k % 3 * 4, bx + 10 + k % 3 * 4, by + 10 + k % 3 * 4], outline=(190, 250, 150, 200), width=4)
            for k in range(5):                              # drips falling off the front
                dy_ = (t * 260 + k * 233) % 300; yy_ = RY + RH + 40 + k * 150 + dy_
                ex = ssx + 30 * math.sin(yy_ / 90 + t * 3) + 14 * math.sin(yy_ / 31 - t * 6)
                d.ellipse([ex - 4, yy_ - 12, ex + 18, yy_ + 12], fill=(120, 215, 90, 240))
            for i, (fx_, fy) in enumerate(FACES):           # slime faces in the wave
                fyy = fy + 12 * math.sin(t * 2.5 + i)
                ex = ssx + 30 * math.sin(fyy / 90 + t * 3) + 14 * math.sin(fyy / 31 - t * 6) - 70 - fx_ * 140
                if ex < 30: continue
                blink = (int(t * 2 + i * 1.7) % 9) == 0
                for sgn in (-1, 1):
                    cx_ = ex + sgn * 20
                    if blink: d.rectangle([cx_ - 9, fyy + 4, cx_ + 9, fyy + 8], fill=(20, 40, 20, 255))
                    else:
                        d.ellipse([cx_ - 9, fyy - 13, cx_ + 9, fyy + 13], fill=(20, 40, 20, 255)); d.rectangle([cx_ - 3, fyy - 8, cx_ + 2, fyy - 3], fill=(240, 255, 230, 255))
                d.arc([ex - 18, fyy + 6, ex + 18, fyy + 30], 20, 160, fill=(20, 40, 20, 255), width=5)
        layer(img, goo)
        for li, ly in enumerate(LANE_Y):                    # little slimes surfing the crest
            ex = ssx + 30 * math.sin((ly - 80) / 90 + t * 3) + 14 * math.sin((ly - 80) / 31 - t * 6)
            s_ = SLI[(int(t * 8) + li * 2) % len(SLI)]; hop = int(abs(math.sin(t * 5 + li)) * 26)
            if ex - 20 > 0: img.alpha_composite(s_, (int(ex - 20 - s_.width / 2), int(ly - s_.height - hop - 60)))
    if any(0 <= t - e[0] < 0.25 for e in SLEEPW): img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 55)))
    # stamps: one at a time (rc16)
    items = []
    for st0, en, pr, it in SCHED:
        if not (st0 <= t < en) or t >= T_CARD: continue
        kind, g, text, col = it; u = t - st0; ly = LANE_Y[LANES[g]]
        al = int(255 * min(1, (en - t) / 0.25))
        if kind == 'pop':
            if st[g]['caught'] is not None and st[g]['caught'] <= t: continue
            size = 56; sc = 1 + 0.3 * max(0, 1 - u / 0.15); wv = len(text) * size * sc + 20
            sxx = min(max(st[g]['x'] - cam, 70 + wv / 2), (1015 if ly - 200 < 1110 else 877) - wv / 2)
            syy = max(ly - 196 - size - u * 16, RY + RH + 8)
            items.append((sxx, syy, text, int(size * sc), col, 8, al))
        else:
            base = min(72, int(800 / len(text))); sc = 1 + 0.35 * max(0, 1 - u / 0.15); wv = len(text) * base * sc
            yy = ly - 150 if kind == 'caught' else ly - 220
            yy = max(yy, RY + RH + 8); lim_r = 1015 if yy + base < 1110 else 877
            sxx = min(max(478, 70 + wv / 2 + 4), lim_r - wv / 2 - 4)
            items.append((sxx, yy, text, int(base * sc), col, 10, al))
    if items: text_layer(img, items)
    for gx_, gy_, a_ in ACV_TAG: acv_side(img, gx_, gy_ + 40, a_)
    # header + roster
    layer(img, lambda d: d.rounded_rectangle([70, RY - 6, 1025, RY + RH], 14, fill=(12, 10, 26, 215)))
    d = ImageDraw.Draw(img)
    for i, g in enumerate(G):
        cx = 70 + 238.75 * (i + 0.5); ic = ICON[g]; s = st[g]
        caught = s['caught'] is not None and s['caught'] <= t
        if caught: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.5)
        ix = int(cx - ic.width / 2); img.alpha_composite(ic, (ix, RY))
        d = ImageDraw.Draw(img); d.rectangle([ix, RY, ix + ic.width, RY + ic.height], outline=COL[g], width=3)
        nm = SN(g); fw = d.textlength(nm, font=F(40))
        d.text((cx - fw / 2, RY + ic.height + 6), nm, font=F(40), fill=COL[g] if not caught else (110, 100, 120), stroke_width=5, stroke_fill=(20, 15, 35))
        if caught:
            d.line([ix + 4, RY + 4, ix + ic.width - 4, RY + ic.height - 4], fill=(230, 50, 50), width=9); d.line([ix + 4, RY + ic.height - 4, ix + ic.width - 4, RY + 4], fill=(230, 50, 50), width=9)
        if t >= T_WIN and g == WIN: d.rounded_rectangle([cx - 116, RY - 2, cx + 116, RY + RH - 4], 10, outline=(255, 214, 60), width=6)
    if t < 0.75:
        scl = 1 + 0.3 * max(0, 1 - t / 0.2)
        text_layer(img, [(478, RY + RH + 60, 'GO!', int(130 * scl), (255, 214, 60), 10, int(255 * min(1, (0.75 - t) / 0.3)))])
    if t >= T_CARD:
        u = t - T_CARD; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, RY + RH + 4, W, H], fill=(8, 6, 14, int(160 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (540 - vf.width // 2, 1330 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, 540, RY + RH + 34, NAME[WIN] + ' ESCAPED!', F(64), (255, 214, 60), 9)
        ctext(d, 540, RY + RH + 124, 'DID YOUR GUIDE WIN?', F(48), (255, 255, 255), 8)   # rc16: one big line (was 36px mixed case)
    img.alpha_composite(HOOK)
    w.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/q63_{f:04d}.png')
    if os.environ.get('FULL') and not loopcut and any(abs(t - (e[0] + 0.2)) < 0.5 / FPS for e in EV if e[1] in ('pick', 'smash', 'caught', 'block')):
        img.convert('RGB').save(f'k_{f:04d}.png')
w.close()
PS = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
for e in EV:
    te, kind, g = e[0], e[1], e[2]
    if kind == 'atk': out_ev.append((round(te + 0.2, 3), {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'sword_swish', 'cyrus': 'punch'}[g])); out_ev.append((round(te + 0.3, 3), 'squish'))
    elif kind == 'slide': out_ev.append((round(te, 3), 'whoosh_8bit')); out_ev.append((round(te + 0.18, 3), 'crunch_8bit'))
    elif kind == 'caught': out_ev.append((round(te, 3), 'squish')); out_ev.append((round(te + 0.05, 3), 'buzz_8bit'))
    elif kind == 'pick': out_ev.append((round(te, 3), PS[e[3]]))
    elif kind == 'smash': out_ev.append((round(te, 3), 'crunch_8bit')); out_ev.append((round(te, 3), 'punch'))
    elif kind == 'block': out_ev.append((round(te, 3), 'boing'))
out_ev += [(0.0, 'go_8bit'), (T_START, 'whoosh_8bit'), (round(T_WIN, 3), 'victory'), (round(T_WIN + 0.1, 3), 'cheer')]
out_ev = sorted(e for e in out_ev if e[0] < T_LOOP)
json.dump({'events': out_ev}, open('v63_ev.json', 'w')); print('done', END)
