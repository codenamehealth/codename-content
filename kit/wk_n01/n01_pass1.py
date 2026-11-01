# n01 slime chase (Oct 30 post). Built from fork_n11/v63/r63.py (063 'who survives the slime'), same low-res rooftop look
# (hub.gif village nearest-scaled, 3x guides, roof tiles), with physics fixes:
#  - attack frames aligned to the run frames (+14 native, the old -14 offset made every attack jump the guide 84px back)
#  - crates never vanish or fade in: guides vault them on a real ballistic hop (fixed speed, gravity arc, ground shadow);
#    a STRENGTH punch breaks a crate into planks that fly, bounce and slide to rest on the roof (persist in world)
#  - nobody freezes mid-air (sleep / catch wait for the landing), shield bounce is a push, not a teleport
#  - planted strikes: stop, wind-up, Syeda/PixelLab attack, hit lands on the impact frame
#  - catch: the crest slime pounces onto the guide's head, KO recoil, the goo rolls over them
#  - ending break: the wave stops, falls back, and the three 'caught' guides are standing there fine, each wearing a slime hat
import sys, os
S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S_ + 'fork1'); from common import *
sys.path.insert(0, S_ + 'pixellab/safezone'); from hook import hook_fade
sys.path.insert(0, S_ + 'fork_n11/tools'); from stamps import schedule
import numpy as np
B6 = S_ + 'fork_b6/'
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (120, 200, 90), 'cleo': (110, 160, 255), 'cyrus': (255, 160, 50), 'ray': (205, 125, 245)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel'}
HOOK, HB = hook_fade(['WHO ESCAPES', 'THE SLIME?'], accent=1)
HOOK_END, _ = hook_fade(['DID YOU', 'CALL IT?'], accent=1)
RY = HB + 10; RH = 0          # roster row cut: lane 0 needs the headroom for the crate vaults
LANE_Y = [840, 1040, 1240, 1440]
L = float(os.environ.get('LEN', '4200')); T_START = 0.3
SA, SB, S0 = float(os.environ.get('SA', '320')), float(os.environ.get('SB', '1')), float(os.environ.get('S0', '-650'))
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'cre': ('STRENGTH!', (90, 160, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
SPEED_T, STRONG_T, SLEEP_T = 2.0, 8.0, 1.0
FLY = 0.35
EDGE = 95.0
# ---- planted strike timing (stop ~1.05s): stand planted in attack frame 0, then the 12-frame swing at 17fps
PLANT, ANIM = 0.35, 0.7
ATK_D = PLANT + ANIM
def _impact(g):
    fs = sorted(glob.glob(PL + f'race/{g}_atk/*.png'))[:9]
    r = [Image.open(p).convert('RGBA').getbbox()[2] for p in fs]
    k = max(range(len(r)), key=lambda i: r[i]); return k, r[k]
IMP = {g: _impact(g) for g in G}                     # (impact frame, weapon tip in attack-native x)
def hit_at(g): return PLANT + (IMP[g][0] + 0.5) / 12 * ANIM
def frame_idx(u):
    if u < PLANT: return 0
    return min(11, int((u - PLANT) / ANIM * 12))
# tip relative to body centre (run-native 46): attack-native a sits at run-native a + 14
REACH = {g: (IMP[g][1] + 14 - 46) * 3 for g in G}
SLIME_HALF = 48
STOPD = {g: REACH[g] + SLIME_HALF - 18 for g in G}  # the tip sinks ~18px into the slime; body never overlaps it
CRATE_SMASH_D = {g: REACH[g] + 30 - 14 for g in G}  # crate half-width 36 at 3x
HOP_D, HOP_H, HOP_D0 = 0.6, 165.0, 105.0            # vault: 0.6s airtime, 175px apex, takes off 105px before the crate centre
def sim(seed, dur=20):
    rnd = random.Random(seed); order = G[:]; rnd.shuffle(order)
    lanes = {g: i for i, g in enumerate(order)}
    obs = {}
    for g in G:
        xs = []; x = 650 + rnd.uniform(0, 500)
        while x < L - 400:
            xs.append([x, 'crate', None, None]); x += rnd.uniform(float(os.environ.get('OMIN', '800')), float(os.environ.get('OMAX', '1250')))
        cand = [o for o in xs if float(os.environ.get('GLO', '700')) < o[0] < L - float(os.environ.get('GHI', '1300'))] or xs
        o = rnd.choice(cand); o[1] = 'slime'; o[3] = GK[g]
        rest = [o2 for o2 in xs if o2[1] == 'crate']
        if rest and rnd.random() < float(os.environ.get('P2', '0.5')): rnd.choice(rest)[1] = 'slime'   # a plain slime too
        obs[g] = xs
    st = {g: dict(x=60.0 * (3 - lanes[g]), mode='run', t0=0, ad=ATK_D, tgt=None, hitdone=False, hop0=0.0, hsp=0.0, boost=-9, strong=-9, shield=False,
                  sleep=-9, sleep0=-9, psleep=None, fire=None, base=rnd.uniform(300, 335), ph=rnd.uniform(0, 6.3), caught=None, pcatch=False, done=None,
                  dist=0.0, oi=0, bump=-9) for g in G}
    frames = []; events = []; leaders = []
    wx = S0; wsleep = -9.0; tau = 0.0
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= T_START - 0.5 and t >= wsleep:
            tau += dt; wx += (SA + 2 * SB * tau) * dt
        sx = wx
        for g in G:
            s = st[g]
            if s['caught'] is not None or s['done'] is not None or t < T_START: continue
            if s['fire'] is not None and t >= s['fire'][0] and t >= s['sleep'] and s['mode'] != 'hop':
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
                        elif o['mode'] == 'hop': o['psleep'] = True; vic.append(m)        # falls asleep on landing (never mid-air)
                        else: o['sleep0'] = t; o['sleep'] = t + SLEEP_T; vic.append(m)
                    wsleep = t + SLEEP_T + 0.2
                    events.append((t, 'sleepwave', g, vic))
            asleep = t < s['sleep']
            if s['mode'] == 'hop':
                sp = s['hsp']
                if t - s['t0'] >= HOP_D:
                    s['mode'] = 'run'; events.append((t, 'land', g))
                    if s['psleep']: s['psleep'] = None; s['sleep0'] = t; s['sleep'] = t + SLEEP_T; asleep = True; sp = 0
            elif asleep:
                sp = 0.0
                if s['mode'] == 'atk': s['t0'] += dt                                    # swing paused while asleep
            else:
                sp = s['base'] * (1 + 0.2 * math.sin(0.8 * t + s['ph']) + 0.1 * math.sin(2.1 * t + s['ph'] * 2))
                if t - s['boost'] < SPEED_T: sp *= 1.6
                if s['mode'] == 'atk':
                    sp = 0; u = t - s['t0']; o = s['tgt']
                    if not s['hitdone'] and u >= hit_at(g):
                        s['hitdone'] = True; o[2] = t
                        events.append((t, 'smash' if o[1] == 'crate' else 'hit', g, o[0]))
                        if o[3]: s['fire'] = (t + FLY, o[3])
                    if u >= s['ad']: s['mode'] = 'run'
                o = obs[g][s['oi']] if s['oi'] < len(obs[g]) else None
                if o and s['mode'] == 'run':
                    strong = t - s['strong'] < STRONG_T
                    if o[1] == 'crate' and strong and o[0] - s['x'] <= CRATE_SMASH_D[g]:
                        s['mode'] = 'atk'; s['t0'] = t; s['ad'] = ATK_D; s['tgt'] = o; s['hitdone'] = False; s['oi'] += 1; s['strong'] = -9; sp = 0
                        s['x'] = o[0] - CRATE_SMASH_D[g]; events.append((t, 'satk', g))
                    elif o[1] == 'slime' and o[0] - s['x'] <= STOPD[g]:
                        s['mode'] = 'atk'; s['t0'] = t; s['ad'] = ATK_D; s['tgt'] = o; s['hitdone'] = False; s['oi'] += 1; sp = 0
                        s['x'] = o[0] - STOPD[g]; events.append((t, 'atk', g))
                    elif o[1] == 'crate' and o[0] - s['x'] <= HOP_D0:
                        s['mode'] = 'hop'; s['t0'] = t; s['hop0'] = s['x']; d0 = o[0] - s['x']; s['hsp'] = 2 * d0 / HOP_D; s['oi'] += 1
                        sp = s['hsp']; events.append((t, 'hop', g))
                if t - s['bump'] < 0.45 and s['mode'] == 'run': sp += 750 * (1 - (t - s['bump']) / 0.45)
            s['x'] += sp * dt; s['dist'] += sp * dt
            if s['x'] >= L: s['done'] = t
            elif s['x'] < sx + EDGE and s['mode'] != 'hop':
                if s['shield']:
                    s['shield'] = False; s['bump'] = t; s['sleep'] = -9; s['mode'] = 'run' if s['mode'] != 'atk' else 'atk'; events.append((t, 'block', g, 'wave'))
                else: s['caught'] = t; events.append((t, 'caught', g))
        alive = [g for g in G if st[g]['caught'] is None]
        if alive:
            ld = max(alive, key=lambda g: st[g]['x'])
            if t > T_START + 1 and (not leaders or leaders[-1] != ld): leaders.append(ld)
        frames.append(({g: dict(x=st[g]['x'], mode=st[g]['mode'], t0=st[g]['t0'], ad=st[g]['ad'], boost=st[g]['boost'], strong=st[g]['strong'],
                                shield=st[g]['shield'], sleep=st[g]['sleep'], sleep0=st[g]['sleep0'], caught=st[g]['caught'], done=st[g]['done'], dist=st[g]['dist'])
                        for g in G}, sx, wsleep))
        if any(st[g]['done'] is not None for g in G) and t > max(st[g]['done'] or 0 for g in G) + 0.01:
            for _ in range(int(4 * FPS)): frames.append(frames[-1])
            break
    return st, frames, events, obs, lanes, leaders
WANTS = os.environ.get('WANT', 'cleo,cyrus').split(',')
def score(seed):
    st, fr, ev, obs, lanes, ld = sim(seed, 18)
    done = [g for g in G if st[g]['done'] is not None]; caught = sorted(st[g]['caught'] for g in G if st[g]['caught'] is not None)
    if len(done) != 1 or len(caught) != 3 or done[0] not in WANTS: return None
    w = done[0]; tw = st[w]['done']
    if not (10.5 < tw < 15.5) or not (3.0 < caught[0] < 8.5): return None
    gaps = (caught[1] - caught[0], caught[2] - caught[1])
    if min(gaps) < 1.0 or max(gaps) > 5.0 or not (0.3 < tw - caught[-1] < 3.0): return None
    kinds = [e[1] for e in ev if e[0] < tw]
    for k in ('sleepwave', 'smash'):
        if k not in kinds: return None
    if sum(1 for e in ev if e[1] == 'pick' and e[0] < tw) < 3: return None
    clear = min(f[0][w]['x'] - f[1] for f in fr[int(1.5 * FPS):int(tw * FPS)])
    if clear < EDGE + 140: return None
    gap = max(max(f[0][g]['x'] for g in G if f[0][g]['caught'] is None) - f[1] for f in fr[int(1.5 * FPS):int(tw * FPS)])
    if gap > 1000: return None
    bt = sorted(e[0] for e in ev if e[1] in ('pick', 'smash', 'block', 'caught', 'sleepwave') and e[0] <= tw)
    clash = sum(1 for i in range(len(bt) - 1) if bt[i + 1] - bt[i] < 0.6)
    if clash > int(os.environ.get('CLASH', '0')): return None
    idle_gap = max(b - a for a, b in zip([1.0] + bt, bt + [tw]))
    return round(idle_gap, 2), w, round(tw, 1), [round(c, 1) for c in caught], round(clear), [(round(e[0], 1), e[1], e[2]) for e in ev if e[1] in ('pick', 'block', 'smash', 'caught', 'sleepwave') and e[0] <= tw]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r and r[0] <= float(os.environ.get('IDLE', '2.6')): print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
ST, FR, EV, OBS, LANES, LD = sim(SEED)
WIN = [g for g in G if ST[g]['done'] is not None][0]; T_WIN = ST[WIN]['done']
print('winner', WIN, round(T_WIN, 2), {g: ST[g]['caught'] for g in G}, LD)
for e in EV:
    if e[1] not in ('atk', 'satk', 'hop', 'land'): print('  ', round(e[0], 2), e[1:])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()
# ---------------- assets
RUN = {g: seq(PL + f'race/{g}_run', 3, 1) for g in G}
ATK = {g: seq(PL + f'race/{g}_atk', 3, 1) for g in G}
KO = {g: seq(PL + f'king/{g}_ko', 3, 0) for g in G}
def gif92(path, k=3):
    im = Image.open(path); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), k))
    return out
IDL = {g: idle(g, 3) for g in G}
VICF = {g: gif92(A + VIC[g]) for g in G}
HOPF = {g: max(RUN[g], key=lambda f: f.getbbox()[2] - f.getbbox()[0]) for g in G}   # widest stride held in the air
def nored(im):
    a = np.array(im); r, g_, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g_ < 110) & (b < 140)] = 0; return Image.fromarray(a)
SLRAW = [nored(Image.open(p).convert('RGBA')) for p in sorted(glob.glob(PL + 'race/slime_idle_c/*.png'))]
SLI = [up(f, 3) for f in SLRAW]
HAT = [up(f, 2) for f in SLRAW]
SLS = [up(nored(Image.open(p).convert('RGBA')), 3) for p in sorted(glob.glob(PL + 'race/slime_splat_c/*.png'))]
CRATE = up(crop(Image.open(B6 + 'gen/crate/00.png').convert('RGBA')), 3)
FLAG = up(crop(Image.open(B6 + 'gen/flag/00.png').convert('RGBA')), 3)
GUMG = {k: gummy(k, 3) for k in POWER}
ICON = {}
for g in G:
    im = idle(g, 1)[0]; bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2; ICON[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
meta = json.load(open(B6 + 'gen/roof_meta.json')); sheet = Image.open(B6 + 'gen/roof_sheet.png').convert('RGBA')
TL = {}
for t_ in meta['tileset_data']['tiles']:
    bb = t_['bounding_box']; TL[t_['name']] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + 32, bb['y'] + 32)), 2)
TOP, MID, BOT, TL_, TR_, ML_, MR_, BL_, BR_ = TL['wang_12'], TL['wang_0'], TL['wang_3'], TL['wang_14'], TL['wang_13'], TL['wang_10'], TL['wang_5'], TL['wang_11'], TL['wang_7']
hub = Image.open(A + 'hub.gif'); BGF = []
for i in range(0, hub.n_frames, 3):
    hub.seek(i); f_ = hub.convert('RGB').resize((3413, 1920), Image.NEAREST)
    a_ = np.array(f_).astype(float); a_ *= np.array([0.62, 0.42, 0.52]); BGF.append(Image.fromarray(a_.clip(0, 255).astype(np.uint8)).convert('RGBA'))
X0W, X1W = -900, L + 900
def lane_strip():
    w_ = int(X1W - X0W) // 64 * 64 + 64; im = Image.new('RGBA', (w_, 192), (0, 0, 0, 0))
    for x in range(0, w_, 64):
        e = 0 if x == 0 else (2 if x == w_ - 64 else 1)
        im.alpha_composite([TL_, TOP, TR_][e], (x, 0)); im.alpha_composite([ML_, MID, MR_][e], (x, 64)); im.alpha_composite([BL_, BOT, BR_][e], (x, 128))
    return im
STRIP = lane_strip()
FOOT = 78 * 3
def head_top(fr, k=3):
    """(x, y) of the top of the head in a frame (canvas coords): topmost opaque rows, centre of their columns"""
    a = np.array(fr.getchannel('A')) > 0; rows = np.where(a.any(1))[0]; top = rows[0]
    band = a[top:top + 4 * k]; cols = np.where(band.any(0))[0]
    return (cols.min() + cols.max()) / 2, top
def hat_on(img, fr, x0, y0, t, sink=10):
    hx, hy = head_top(fr); h = HAT[int(t * 8) % len(HAT)]; bb = h.getbbox()
    img.alpha_composite(h, (int(x0 + hx - (bb[0] + bb[2]) / 2), int(y0 + hy - bb[3] + sink)))
    return x0 + hx, y0 + hy - (bb[3] - bb[1]) + sink
def heart(img, x, y, a=255, cell=7):
    pat = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']
    def dr(d):
        for r_, row in enumerate(pat):
            for c_, ch in enumerate(row):
                if ch == 'X':
                    x_ = x + (c_ - 3.5) * cell; y_ = y + r_ * cell
                    d.rectangle([x_ - 2, y_ - 2, x_ + cell + 1, y_ + cell + 1], fill=(60, 10, 30, a))
        for r_, row in enumerate(pat):
            for c_, ch in enumerate(row):
                if ch == 'X':
                    x_ = x + (c_ - 3.5) * cell; y_ = y + r_ * cell
                    d.rectangle([x_, y_, x_ + cell - 1, y_ + cell - 1], fill=(255, 110, 150, a) if (r_, c_) != (1, 1) else (255, 220, 230, a))
    layer(img, dr)
def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_
# ---------------- crate debris: real ballistic planks (bounce, friction, rest), in world coords
def debris_for(ox, seed):
    r = random.Random(seed); out = []
    for k in range(7):
        w_, h_ = r.choice([(30, 12), (24, 12), (36, 12), (18, 18)])
        x, y = ox + r.uniform(-24, 24), -r.uniform(20, 80); vx = r.uniform(80, 460); vy = -r.uniform(450, 950)
        ang = r.uniform(0, 3.14); va = r.uniform(-14, 14); path = []
        for i in range(int(4 * FPS)):
            dt = 1 / FPS
            if y < 0 or vy < 0 or abs(vy) > 40:
                vy += 3000 * dt; x += vx * dt; y += vy * dt; ang += va * dt
                if y >= 0:
                    y = 0; vy = -vy * 0.3 if abs(vy) > 160 else 0; vx *= 0.6; va *= 0.5
            else:
                y = 0; vy = 0
                sgn = 1 if vx > 0 else -1; vx = sgn * max(0, abs(vx) - 1400 * dt); x += vx * dt
                ang += va * dt; va *= 0.7
                # settle flat: rotate toward the nearest flat angle only while still sliding (eases, no snap)
                tgt = round(ang / math.pi) * math.pi; ang += (tgt - ang) * 0.25
            path.append((x, y, ang))
        out.append((w_, h_, path))
    return out
DEBRIS = []    # (t_hit, lane_y, pieces)
for e in EV:
    if e[1] == 'smash': DEBRIS.append((e[0], LANE_Y[LANES[e[2]]], debris_for(e[3], int(e[3]))))
def draw_debris(img, t, cam):
    def dr(d):
        for th, ly, pcs in DEBRIS:
            if t < th: continue
            i = min(int((t - th) * FPS), int(4 * FPS) - 1)
            for w_, h_, path in pcs:
                x, y, ang = path[i]; cx, cy = x - cam, ly + 4 + y - h_ / 2
                if cx < -80 or cx > W + 80: continue
                c, s_ = math.cos(ang), math.sin(ang); pts = [(cx + c * dx - s_ * dy, cy + s_ * dx + c * dy) for dx, dy in ((-w_ / 2, -h_ / 2), (w_ / 2, -h_ / 2), (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2))]
                d.polygon(pts, fill=(160, 108, 58, 255), outline=(70, 42, 22, 255))
    layer(img, dr)
# ---------------- ending timeline (after the escape)
FPSf = float(FPS)
iw = int(round(T_WIN * FPS)); XW0 = FR[iw][1]; VW = SA + 2 * SB * (T_WIN - T_START + 0.5)
XF = max(L - 190, XW0 + 120)                         # the wave stops ~190px behind the line
A_BR = 700.0
d_br = VW * VW / (2 * A_BR)
if XF - XW0 > d_br: T_BR = T_WIN + (XF - XW0 - d_br) / VW
else: T_BR = T_WIN; A_BR = VW * VW / (2 * (XF - XW0))
T_STOP = T_BR + VW / A_BR
T_REC = T_STOP + 0.35; A_REC = 1500.0
def wave_world(t):
    if t <= T_WIN: return FR[min(int(round(t * FPS)), len(FR) - 1)][1]
    if t <= T_BR: return XW0 + VW * (t - T_WIN)
    if t <= T_STOP: u = t - T_BR; return XW0 + VW * (T_BR - T_WIN) + VW * u - 0.5 * A_BR * u * u
    if t <= T_REC: return XF
    u = t - T_REC; return XF - 0.5 * A_REC * u * u
XR = XF - 125                                        # where the swallowed guides were carried; the wave leaves them here
CAUGHT_ORDER = sorted([g for g in G if ST[g]['caught'] is not None], key=lambda g: ST[g]['caught'])
T_HEART = {g: T_REC + 0.75 + 0.35 * i for i, g in enumerate(CAUGHT_ORDER)}
T_TEXT = max(T_HEART.values()) + 0.15
T_LOOP = T_TEXT + 2.3; END = T_LOOP + 0.2; NF = int(round(END * FPS))
WSTOP = 0.4                                           # winner slows to a stop past the line, then the victory pose
VWIN = ST[WIN]['base']
def win_x(t):
    u = min(t - T_WIN, WSTOP); return L + VWIN * (u - u * u / (2 * WSTOP))
print('ending: brake', round(T_BR, 2), 'stop', round(T_STOP, 2), 'recede', round(T_REC, 2), 'text', round(T_TEXT, 2), 'end', round(END, 2))
def SN(g): return NAME[g]
RAWS = []
for e in EV:
    if e[0] > T_WIN: continue
    if e[1] == 'pick': RAWS.append((e[0], 'pop', ('pop', e[2], SN(e[2]) + ': ' + POWER[e[3]][0], POWER[e[3]][1]), True))
    elif e[1] == 'caught': RAWS.append((e[0], 'caught', ('caught', e[2], SN(e[2]) + ' CAUGHT!', (255, 95, 95)), True))
RAWS.append((T_WIN, 'win', ('win', WIN, SN(WIN) + ' ESCAPED!', (255, 214, 60)), True))
def sched2(items, dur=0.9, gap=0.12, mind=0.5, end=None):
    items = sorted(items, key=lambda z: z[0]); out = []
    for i, (t0, k_, it, must) in enumerate(items):
        st0 = max(t0, out[-1][1] + gap) if out else t0
        nxt = items[i + 1][0] if i + 1 < len(items) else 1e9
        en = st0 + dur
        if nxt - gap < en: en = max(st0 + (mind if k_ == 'caught' else 0.5), nxt - gap)     # a newer event cuts this stamp short (never stacks)
        if end is not None and k_ == 'win': en = end
        out.append((st0, en, k_, it))
    return out
SCHED = sched2(RAWS, mind=0.7, end=T_WIN + 1.3)
print('stamps', [(round(a_, 2), round(b_, 2), it[2]) for a_, b_, k_, it in SCHED])
PICKS = {e[2]: e for e in EV if e[1] == 'pick'}
SLEEPW = [e for e in EV if e[1] == 'sleepwave']
BLOCKW = {e[2]: e[0] for e in EV if e[1] == 'block'}
FACES = [(i * 0.137 % 1, RY + RH + 50 + i * 108 + 24 * math.sin(i * 2.1)) for i in range(7)]
def edge_x(ssx, y, t): return ssx + 30 * math.sin(y / 90 + t * 3) + 14 * math.sin(y / 31 - t * 6)
STILLS = [float(x) for x in os.environ.get('STILLS', '').split(',') if x]
w = None if STILLS else Writer('n01_noaudio.mp4'); cam = None
for f in range(NF):
    t = f / FPS; loopcut = t >= T_LOOP
    if loopcut: t = 0.0
    if STILLS and not any(abs(f / FPS - x) < 0.5 / FPS for x in STILLS):
        # keep the camera smoothing state exact even when skipping frames
        pass
    fi = int(round(t * FPS)); st, sxw, wsl = FR[min(fi, len(FR) - 1)]
    alive = [g for g in G if not (st[g]['caught'] is not None and st[g]['caught'] <= t)]
    lead_x = max(st[g]['x'] for g in G) if t < T_WIN else win_x(t)
    last_x = min(st[g]['x'] for g in alive) if alive else lead_x
    if t < T_WIN: target = max(min(lead_x - 600, last_x - 160, sxw - 130), lead_x - 800, X0W)
    else: target = L + VWIN * WSTOP / 2 - 700
    cam = target if (cam is None or loopcut) else cam + (target - cam) * 0.12
    if STILLS and not any(abs(f / FPS - x) < 0.5 / FPS for x in STILLS): continue
    img = BGF[int(t * 4) % len(BGF)].crop((int(600 + cam * 0.12), 0, int(600 + cam * 0.12) + W, H))
    for li, ly in enumerate(LANE_Y):
        sxs = int(X0W - cam); sx0 = max(0, -sxs)
        img.alpha_composite(STRIP.crop((sx0, 0, min(STRIP.width, sx0 + W + 64), 192)), (max(0, sxs), ly - 38))
    for li, ly in enumerate(LANE_Y):
        fx = L - 40 - cam
        if -200 < fx < W + 200: img.alpha_composite(FLAG, (int(fx - FLAG.width / 2), ly - FLAG.height + 6))
    # obstacles
    for g in G:
        ly = LANE_Y[LANES[g]]
        for (ox, kind, thit, gk) in OBS[g]:
            px = ox - cam
            if px < -150 or px > W + 150: continue
            if kind == 'slime':
                if thit is None or t < thit:
                    s_ = SLI[int(t * 8 + ox) % len(SLI)]; bb = s_.getbbox()
                    img.alpha_composite(s_, (int(px - s_.width / 2), ly - s_.height + 6 + 30))
                    if gk:
                        gm = GUMG[gk]; top = ly - s_.height + 36 + bb[1]          # gummy rides on the slime's head
                        layer(img, lambda dd, px=px, top=top, gk=gk, gm=gm: [dd.ellipse([px - 50 + k_ * 10, top - gm.height / 2 - 44 + k_ * 10, px + 50 - k_ * 10, top - gm.height / 2 + 44 - k_ * 10], fill=POWER[gk][1] + (40 + k_ * 30,)) for k_ in range(3)])
                        img.alpha_composite(gm, (int(px - gm.width / 2), int(top - gm.height + 8)))
                elif t - thit < 0.45: s_ = SLS[min(len(SLS) - 1, int((t - thit) / 0.45 * len(SLS)))]; img.alpha_composite(s_, (int(px - s_.width / 2), ly - s_.height + 6 + 30))
            else:
                if thit is None or t < thit: img.alpha_composite(CRATE, (int(px - CRATE.width / 2), ly - CRATE.height + 8))
    draw_debris(img, t, cam)
    # gummies flying from the popped slime to the guide (ballistic arc)
    for g, e in PICKS.items():
        o = next(o for o in OBS[g] if o[3])
        if o[2] is None or t < o[2] or t >= e[0] or e[0] > T_WIN: continue
        ly = LANE_Y[LANES[g]]; s = st[g]; u = min(1, (t - o[2]) / FLY)
        gm = GUMG[e[3]]
        x0_, y0_ = o[0] - cam, ly - 60; x1_, y1_ = s['x'] - cam, ly - 230
        if u >= 1:     # caught it: held over the head until it fires (waits out sleep / landing)
            gx_, gy_ = x1_, y1_
        else: gx_, gy_ = x0_ + (x1_ - x0_) * u, y0_ + (y1_ - y0_) * u - 4 * 140 * u * (1 - u)
        img.alpha_composite(gm, (int(gx_ - gm.width / 2), int(gy_ - gm.height / 2)))
    for e in EV:
        if e[1] == 'pick' and 0 <= t - e[0] < 0.6 and e[0] <= T_WIN:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.6
            px_, py_ = s0['x'] - cam, LANE_Y[LANES[e[2]]] - 130; col = POWER[e[3]][1]
            layer(img, lambda dd, px_=px_, py_=py_, u=u, col=col: [dd.rectangle([px_ + (30 + 140 * u) * math.cos(q * 0.628) - 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) - 7, px_ + (30 + 140 * u) * math.cos(q * 0.628) + 7, py_ + (30 + 140 * u) * math.sin(q * 0.628) + 7], fill=col + (int(255 * (1 - u)),)) for q in range(10)])
    for e in SLEEPW:
        if 0 <= t - e[0] < 0.7:
            s0 = FR[min(int(round(e[0] * FPS)), len(FR) - 1)][0][e[2]]; u = (t - e[0]) / 0.7
            px_, py_ = s0['x'] - cam, LANE_Y[LANES[e[2]]] - 130
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.ellipse([px_ - r_, py_ - r_, px_ + r_, py_ + r_], outline=(190, 120, 255, int(230 * (1 - u))), width=14) for r_ in (60 + 1400 * u, 20 + 1000 * u)])
    ssx = wave_world(t) - cam
    # runners
    for g in G:
        s = st[g]; ly = LANE_Y[LANES[g]]; px = s['x'] - cam
        tc = s['caught']
        if tc is not None and tc <= t:
            if t >= T_REC - 0.05:                      # the wave falls back: standing there fine, wearing the slime that pounced
                fr = IDL[g][int(t * 8 + LANES[g]) % len(IDL[g])]; x0, y0 = int(XR + (-55 if LANES[g] % 2 else 55) - cam - 46 * 3), ly - FOOT
                img.alpha_composite(fr, (x0, y0)); hx, hy = hat_on(img, fr, x0, y0, t + LANES[g] * 0.3)
                if g in T_HEART and t >= T_HEART[g]:
                    u = t - T_HEART[g]; heart(img, hx, hy - 70 - min(u, 0.4) * 40, int(255 * min(1, u / 0.15)))
            elif t < tc + 1.0:                         # pounced on: KO recoil, the goo rolls over them
                k = min(2, int((t - tc) / 0.12)); fr = KO[g][k]
                x0, y0 = int(px - 64 * 3 + 0), ly - 96 * 3      # KO canvas 128, feet at row 96, body centre ~64
                img.alpha_composite(fr, (x0, y0)); hat_on(img, fr, x0, y0, t)
            continue
        hop = s['mode'] == 'hop'; asleep = t < s['sleep'] and not hop
        if g == WIN and t >= T_WIN:
            px = win_x(t) - cam
            if t >= T_WIN + WSTOP:
                fr = VICF[g][int((t - T_WIN - WSTOP) * 8) % len(VICF[g])]
                img.alpha_composite(fr, (int(px - 46 * 3), ly - FOOT)); continue
            fr = RUN[g][int((s['dist'] + VWIN * (t - T_WIN)) / 34) % 8]
        elif t < T_START: fr = RUN[g][0]
        elif asleep and s['mode'] == 'atk': fr = ATK[g][frame_idx(t - s['t0'])]
        elif asleep: fr = RUN[g][0]
        elif s['mode'] == 'atk': fr = ATK[g][frame_idx(t - s['t0'])]
        elif hop: fr = HOPF[g]
        else: fr = RUN[g][int(s['dist'] / 34) % 8]
        dy = 0
        if hop:
            u = min(1, (t - s['t0']) / HOP_D); dy = int(4 * HOP_H * u * (1 - u))
            sh = int(70 * (1 - 0.5 * dy / HOP_H))
            layer(img, lambda dd, px=px, ly=ly, sh=sh: dd.ellipse([px - sh / 2, ly - 8, px + sh / 2, ly + 8], fill=(20, 10, 10, 90)))
        boosted = t - s['boost'] < SPEED_T and not asleep and t < T_WIN
        strong = t - s['strong'] < STRONG_T and t < T_WIN
        atk = s['mode'] == 'atk' and t >= T_START and not (g == WIN and t >= T_WIN)
        x0, y0 = (int(px - 46 * 3 + 14 * 3), ly - FOOT - 26 * 3) if atk else (int(px - 46 * 3), ly - FOOT - dy)
        if boosted:
            for q in range(3):
                img.alpha_composite(tinted(fr, (255, 170, 50), int(255 * (0.34 - 0.09 * q))), (x0 - (q + 1) * 34, y0))
            layer(img, lambda dd: [dd.rectangle([px - 200 - 30 * q - (q * 37 + int(t * 90)) % 50, ly - 170 + q * 34 - 4 - dy, px - 90 - 30 * q, ly - 170 + q * 34 + 4 - dy], fill=(255, 240, 200, 210)) for q in range(4)])
        if strong:
            tt = tinted(fr, (90, 160, 255), int(170 + 70 * math.sin(t * 14)))
            for ox, oy in ((-7, 0), (7, 0), (0, -7), (0, 7), (-5, -5), (5, 5), (-5, 5), (5, -5)): img.alpha_composite(tt, (x0 + ox, y0 + oy))
        img.alpha_composite(fr, (x0, y0))
        if asleep:
            img.alpha_composite(tinted(fr, (40, 20, 90), 120), (x0, y0))
            u = t - s['sleep0']
            text_layer(img, [(px + 50 + 22 * kz, ly - 230 - ((u * 1.4 + kz * 0.33) % 1) * 60 - kz * 16, 'Z', 36 + 10 * kz, (225, 205, 255), 6, int(255 * (1 - (u * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
        if s['shield'] and t < T_WIN:
            layer(img, lambda dd: (dd.ellipse([px - 105, ly - 250 - dy, px + 105, ly + 16 - dy], fill=(110, 230, 90, 28), outline=(150, 255, 120, 235), width=7),
                                   dd.arc([px - 78, ly - 226 - dy, px - 18, ly - 150 - dy], 200, 260, fill=(230, 255, 220, 230), width=6)))
        if g in BLOCKW and 0 <= t - BLOCKW[g] < 0.5:
            u = (t - BLOCKW[g]) / 0.5
            layer(img, lambda dd: [dd.rectangle([px + (110 + 120 * u) * math.cos(q * 0.524) - 8, ly - 117 + (135 + 100 * u) * math.sin(q * 0.524) - 8, px + (110 + 120 * u) * math.cos(q * 0.524) + 8, ly - 117 + (135 + 100 * u) * math.sin(q * 0.524) + 8], fill=(150, 255, 120, int(255 * (1 - u)))) for q in range(12)])
    # the SLIME WAVE
    if ssx > -160:
        def goo(d):
            for y in range(0, H, 10):
                ex = edge_x(ssx, y, t)
                if ex <= 0: continue
                if ex > 46: d.rectangle([0, y, ex - 46, y + 10], fill=(52, 140, 44, 250))
                if ex > 18: d.rectangle([max(0, ex - 46), y, ex - 18, y + 10], fill=(92, 190, 64, 252))
                d.rectangle([max(0, ex - 18), y, ex, y + 10], fill=(150, 232, 104, 252))
                d.rectangle([max(0, ex), y, ex + 6, y + 10], fill=(30, 80, 30, 230))
            for k in range(16):
                by = RY + RH + 20 + ((k * 151 - t * 90) % (1700 - RY - RH - 20)); bx = ssx - 60 - (k * 97) % 420
                if bx > 10: d.ellipse([bx - 10 - k % 3 * 4, by - 10 - k % 3 * 4, bx + 10 + k % 3 * 4, by + 10 + k % 3 * 4], outline=(190, 250, 150, 200), width=4)
            for k in range(5):
                dy_ = (t * 260 + k * 233) % 300; yy_ = RY + RH + 40 + k * 150 + dy_
                ex = edge_x(ssx, yy_, t)
                if ex > 10: d.ellipse([ex - 4, yy_ - 12, ex + 18, yy_ + 12], fill=(120, 215, 90, 240))
            for i, (fx_, fy) in enumerate(FACES):
                fyy = fy + 12 * math.sin(t * 2.5 + i)
                ex = edge_x(ssx, fyy, t) - 70 - fx_ * 140
                if ex < 30: continue
                blink = (int(t * 2 + i * 1.7) % 9) == 0
                for sgn in (-1, 1):
                    cx_ = ex + sgn * 20
                    if blink: d.rectangle([cx_ - 9, fyy + 4, cx_ + 9, fyy + 8], fill=(20, 40, 20, 255))
                    else:
                        d.ellipse([cx_ - 9, fyy - 13, cx_ + 9, fyy + 13], fill=(20, 40, 20, 255)); d.rectangle([cx_ - 3, fyy - 8, cx_ + 2, fyy - 3], fill=(240, 255, 230, 255))
                d.arc([ex - 18, fyy + 6, ex + 18, fyy + 30], 20, 160, fill=(20, 40, 20, 255), width=5)
        layer(img, goo)
        asleep_w = t < wsl and t < T_WIN
        for li, ly in enumerate(LANE_Y):                    # little slimes surfing the crest
            ex = edge_x(ssx, ly - 80, t)
            s_ = SLI[(int(t * 8) + li * 2) % len(SLI)] if not asleep_w else SLI[0]; hop_ = 0 if (asleep_w or t > T_STOP) else int(abs(math.sin(t * 5 + li)) * 26)
            gl = next((g_ for g_ in G if LANES[g_] == li), None); tc = ST[gl]['caught'] if gl else None
            if tc is not None and tc - 1.0 <= t < tc:     # planted catch: squats at the crest, then pounces onto the guide's head
                sg = FR[min(int(round(tc * FPS)), len(FR) - 1)][0][gl]; xg = sg['x'] - cam
                k0 = KO[gl][0]; hx, hy = head_top(k0); tx, ty = xg - 64 * 3 + hx, ly - 96 * 3 + hy + 10
                if t < tc - 0.35:
                    q = (t - (tc - 1.0)) / 0.65; sq = 1 - 0.2 * min(1, q * 1.6) + 0.04 * math.sin(t * 30)
                    sp_ = s_.resize((int(s_.width * (2 - sq)), max(1, int(s_.height * sq))), Image.NEAREST)
                    img.alpha_composite(sp_, (int(ex - 20 - sp_.width / 2), int(ly - 60 - sp_.height)))
                else:
                    q = (t - (tc - 0.35)) / 0.35; hs = HAT[0]; bb = hs.getbbox()
                    sc_ = 3 - q                               # shrinks to hat size in flight (3x -> 2x), lands on the head
                    fr_ = up(SLRAW[0], 1); fr_ = fr_.resize((int(64 * sc_), int(64 * sc_)), Image.NEAREST); b2 = fr_.getbbox()
                    x_ = (ex - 20) + (tx - (ex - 20)) * q; y_ = (ly - 60) + (ty - (ly - 60)) * q - 4 * 150 * q * (1 - q)
                    img.alpha_composite(fr_, (int(x_ - (b2[0] + b2[2]) / 2), int(y_ - b2[3])))
                continue
            if tc is not None and tc <= t: continue
            if ex - 20 > 0: img.alpha_composite(s_, (int(ex - 20 - s_.width / 2), int(ly - s_.height - hop_ - 60)))
            if asleep_w and ex - 20 > 0: text_layer(img, [(ex + 10 + 18 * kz, ly - 60 - s_.height - 10 - ((t * 1.4 + kz * 0.33) % 1) * 50 - kz * 12, 'Z', 28 + 8 * kz, (225, 205, 255), 5, int(255 * (1 - (t * 1.4 + kz * 0.33) % 1))) for kz in range(3)])
    if any(0 <= t - e[0] < 0.25 for e in SLEEPW): img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 55)))
    # stamps: one at a time
    items = []
    for st0, en, k_, it in SCHED:
        if not (st0 <= t < en) or loopcut: continue
        kind, g, text, col = it; u = t - st0; ly = LANE_Y[LANES[g]]
        al = int(255 * min(1, (en - t) / 0.25))
        if kind == 'pop':
            size = min(56, int(760 / len(text))); sc = 1 + 0.12 * max(0, 1 - u / 0.12)
            gx = st[g]['x'] - cam; wv = len(text) * size * sc + 20
            sxx = min(max(gx, 70 + wv / 2), (1015 if ly - 200 < 1110 else 877) - wv / 2)
            syy = max(ly - 196 - size - u * 16 - 60, RY + RH + 8)
            items.append((sxx, syy, text, int(size * sc), col, 8, al))
        else:
            base = min(72, int(800 / len(text)))
            yy = ly - 150 if kind == 'caught' else ly - 300
            yy = max(yy, RY + RH + 8); lim_r = 1015 if yy + base < 1110 else 877
            base = min(base, int((lim_r - 78) / len(text)))
            sc = min(1 + 0.35 * max(0, 1 - u / 0.15), (lim_r - 78) / (len(text) * base)); wv = len(text) * base * sc
            sxx = min(max(478, 70 + wv / 2 + 4), lim_r - wv / 2 - 4)
            if kind == 'caught':        # sits to the right of the caught guide (who is at the goo's edge), never on top of them
                tc_ = ST[g]['caught']; gx = FR[min(int(round(tc_ * FPS)), len(FR) - 1)][0][g]['x'] - cam
                x_l = gx + 125; fs_ = max(44, min(72, int((lim_r - 8 - x_l) / len(text))))
                sc = 1 + 0.25 * max(0, 1 - u / 0.15); base = fs_; wv = len(text) * base * sc
                sxx = min(x_l + wv / 2, lim_r - wv / 2 - 4)
            items.append((sxx, yy, text, int(base * sc), col, 10, al))
    if items: text_layer(img, items)
    # (roster cut)
    for i, g in ([] if True else enumerate(G)):
        cx = 70 + 238.75 * (i + 0.5); ic = ICON[g]; s = st[g]
        caught = s['caught'] is not None and s['caught'] <= t and not (t >= T_REC + 0.3)
        if caught: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.5)
        ix = int(cx - ic.width / 2); img.alpha_composite(ic, (ix, RY))
        d = ImageDraw.Draw(img); d.rectangle([ix, RY, ix + ic.width, RY + ic.height], outline=COL[g], width=3)
        if caught:
            d.line([ix + 4, RY + 4, ix + ic.width - 4, RY + ic.height - 4], fill=(230, 50, 50), width=9); d.line([ix + 4, RY + ic.height - 4, ix + ic.width - 4, RY + 4], fill=(230, 50, 50), width=9)
        if t >= T_WIN and g == WIN and not loopcut: d.rectangle([ix - 6, RY - 6, ix + ic.width + 6, RY + ic.height + 6], outline=(255, 214, 60), width=6)
    if t < 0.75:
        scl = 1 + 0.3 * max(0, 1 - t / 0.2)
        text_layer(img, [(478, RY + RH + 60, 'GO!', int(130 * scl), (255, 214, 60), 10, int(255 * min(1, (0.75 - t) / 0.3)))])
    img.alpha_composite(HOOK_END if (t >= T_TEXT and not loopcut) else HOOK)
    if STILLS: img.convert('RGB').save(f'st_{f / FPS:.2f}.png')
    else: w.write(img)
if w: w.close()
if STILLS: sys.exit()
# ---------------- sound events
SW = {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'sword_swish', 'cyrus': 'punch'}
PS = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}
out_ev = []
for e in EV:
    te, kind, g = e[0], e[1], e[2]
    if te > T_WIN + 0.01: continue
    if kind in ('atk', 'satk'): out_ev.append((round(te + hit_at(g) - 0.08, 3), SW[g]))
    elif kind == 'hit': out_ev.append((round(te, 3), 'squish'))
    elif kind == 'smash': out_ev.append((round(te, 3), 'crunch_8bit')); out_ev.append((round(te, 3), 'punch'))
    elif kind == 'hop': out_ev.append((round(te, 3), 'jump'))
    elif kind == 'caught': out_ev.append((round(te - 0.35, 3), 'jump')); out_ev.append((round(te, 3), 'squish')); out_ev.append((round(te + 0.05, 3), 'buzz_8bit'))
    elif kind == 'pick': out_ev.append((round(te, 3), PS[e[3]]))
    elif kind == 'block': out_ev.append((round(te, 3), 'boing'))
out_ev += [(0.0, 'go_8bit'), (round(T_WIN, 3), 'victory'), (round(T_WIN + 0.1, 3), 'cheer'), (round(T_REC, 3), 'whoosh_8bit')]
out_ev += [(round(T_HEART[g], 3), 'coin_8bit') for g in CAUGHT_ORDER]
out_ev = sorted(e for e in out_ev if e[0] < T_LOOP)
json.dump({'events': out_ev, 'end': END, 'beats': {'win': T_WIN, 'stop': T_STOP, 'recede': T_REC, 'hearts': T_HEART, 'text': T_TEXT, 'loop': T_LOOP}}, open('n01_ev.json', 'w'), indent=1)
print('done', round(END, 2), NF)
