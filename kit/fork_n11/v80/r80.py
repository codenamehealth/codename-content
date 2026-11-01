import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; B8 = SP0 + 'fork_b8/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer, hook_fade
# #80 safe-zone + hook pass (source: fork_b8/r82.py). HOLLOW RULE: the Hollow racer is removed (4 guides).
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP0 + 'fork_c7'); from powers import *
POWER['cre'] = ('STRENGTH!', POWER['cre'][1])   # Oct 29: creatine is always STRENGTH!
G = ['ray', 'cleo', 'joy', 'cyrus']   # review fix: the bottom-lane sleeper is Cyrus (the only guide with an eyes-closed sleep animation: fork_a5/gen/cyrus_sleep, PixelLab from Syeda's sprite, used in #33/#47)
NAPPER = 'cyrus'
CSLEEP = [up(Image.open(p).convert('RGBA'), 3) for p in sorted(glob.glob(SP0 + 'fork_a5/gen/cyrus_sleep/*.png'))]
sys.path.insert(0, SP0 + 'fork_n11/tools'); from stamps import schedule, active
NAME = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
COL = {'joy': (110, 210, 90), 'cyrus': (255, 160, 40), 'cleo': (100, 160, 255), 'ray': (190, 110, 240), 'hollow': (190, 180, 220)}
GUM = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
SIDE = {g: SP0 + f'pixellab/race/in/{g}_side.png' for g in ['joy', 'cyrus', 'cleo', 'ray']}
SPR = {g: up(Image.open(p).convert('RGBA'), 3) for g, p in SIDE.items()}          # 2x -> 3x (4 lanes leave room), feet at y=234
ATKF = {g: seq(SP0 + f'pixellab/race/{g}_atk', 3, 1) for g in ['joy', 'cyrus', 'cleo', 'ray']}
ATK_CX = {'joy': 34, 'ray': 30, 'cleo': 31, 'cyrus': 29}; SIDE_CX = {'joy': 48, 'cleo': 45, 'cyrus': 43, 'ray': 43}
BOARD = up(crop(Image.open(B8 + 'surfboard/02.png').convert('RGBA')), 3)
LH = up(crop(Image.open(B8 + 'lighthouse/01.png').convert('RGBA')), 3)
BUOY = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(SP0 + 'fork4/buoy/*.png'))]
SLIME = [up(Image.open(p).convert('RGBA'), 2) for p in sorted(glob.glob(SP0 + 'pixellab/race/slime_idle_c/*.png'))]
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0; return Image.fromarray(a)
SLIME = [nored(s) for s in SLIME]
OCEAN = Image.open(B8 + 'ocean/00.png').convert('RGBA')
SKY = OCEAN.resize((OCEAN.width * 3, OCEAN.height * 3), Image.NEAREST)        # 1344x768
SKYX = (SKY.width - W) // 2
HOOK, HB = hook_fade(['WATCH THE', 'BOTTOM LANE'], accent=1)   # Oct 29 notes2: job hook; the nap cutscene pays it off
HOOK_END = HOOK   # Oct 29 notes2: the hook stays up through the card and the cutscene (no end question)
TRK0 = HB + 12; TRK1 = TRK0 + 90          # progress track box under the hook
ROPE0 = 700; LY = [ROPE0 + 120 + i * 205 for i in range(4)]
OFF = 200                                  # rider screen offset (was 90) so the start line clears x70
CAMOFF = 440                               # leader kept at screen x ~640 (was 730)
from PIL import ImageChops
_fx = np.arange(W)[None, :]; _fy = np.arange(H)[:, None]
_lo = np.clip((870 - _fx) / 70.0, 0, 1); _hi = np.clip((1015 - _fx) / 60.0, 0, 1)
FADE = Image.fromarray((np.where(_fy >= 1040, _lo, _hi) * 255).astype(np.uint8), 'L')
print('hook bottom', HB, 'track', TRK0, TRK1, 'lanes', LY)
COURSE = float(os.environ.get('COURSE', '6600')); T0 = float(os.environ.get('T0', '0.0'))
SPEED_T, SPEED_K = 1.6, 1.55; STRONG_T = 3.0; SLEEP_T = 1.0
from strike import ATK_D, hit_at, frame_idx   # review fix: planted hits (stand ~0.6s, then the full swing; hit on the impact frame)   # Oct 29 notes2: a smash is a real attack: the board stops ~1s while the rider plays the attack animation
# ---------- sim
def sim(seed):
    rnd = random.Random(seed)
    order = list(G)
    st = {g: dict(x=0.0, v=0.0, base=rnd.uniform(355, 380), ph=rnd.uniform(0, 6.3), boost=-9, bonk=-9, fin=None, atk=-9) for g in G}
    items = []
    for li, g in enumerate(G):
        for k in range(2):
            x_ = rnd.uniform(900 + k * 2600, 2600 + k * 2600)
            if g != NAPPER: items.append(dict(kind='gum', lane=li, x=x_, got=None))
        for k in range(2):
            x_ = rnd.uniform(1400 + k * 2400, 3000 + k * 2400)
            if g != NAPPER and x_ < COURSE - 500: items.append(dict(kind='slime', lane=li, x=x_, got=None))   # napper's lane stays clear: he never touches anything
    frames = []; ev = []
    for g in G: st[g].update(sleep=-9.0, shield=False, strong=-9.0, pop=None)
    f = 0
    while True:
        t = f / FPS
        if t >= T0:
            for li, g in enumerate(G):
                s = st[g]
                if s['fin'] is not None: continue
                sp = s['base'] * (1 + 0.16 * math.sin(0.8 * t + s['ph']) + 0.08 * math.sin(2.1 * t + 2 * s['ph']))
                if t - s['boost'] < SPEED_T: sp *= SPEED_K
                if t - s['bonk'] < 0.7: sp *= 0.35
                if t < s['sleep']: sp = 0.0
                if t - s['atk'] < ATK_D: sp = 0.0
                s['v'] += (sp - s['v']) * (0.25 if (t < s['sleep'] or t - s['atk'] < ATK_D) else 0.08); s['x'] += s['v'] / FPS
                for it in items:   # STRENGTH: stop short of the slime, plant, swing, the hit lands on it (sword reach ~110px)
                    if it['lane'] == li and it['got'] is None and it['kind'] == 'slime' and t - s['strong'] < STRONG_T and t - s['atk'] >= ATK_D and 85 < it['x'] - s['x'] < 125:
                        it['got'] = t; s['atk'] = t; it['smash'] = t + hit_at(g); ev.append((t, 'satk', g)); ev.append((t + hit_at(g), 'smash', g)); s['strong'] = -9
                for it in items:
                    if it['lane'] == li and it['got'] is None and abs(it['x'] - s['x']) < 40:
                        it['got'] = t
                        if it['kind'] == 'gum':
                            k = GUM[g]; ev.append((t, 'pick', g, k))
                            if k == 'mush': s['boost'] = t
                            elif k == 'acv': s['shield'] = True
                            elif k == 'cre': s['strong'] = t
                            elif k == 'mel':
                                ev.append((t, 'sleepwave', g))
                                for h in G:
                                    o = st[h]
                                    if h == g or o['fin'] is not None or o['sleep'] > 1e8: continue
                                    if h == NAPPER: o['sleep'] = 1e9; ev.append((t, 'nap', h)); continue   # Cyrus never wakes up
                                    if o['shield']: o['shield'] = False; o['pop'] = t; ev.append((t, 'block', h))
                                    else: o['sleep'] = t + SLEEP_T; ev.append((t, 'sleep', h))
                        else:
                            if s['shield']: s['shield'] = False; s['pop'] = t; it['blocked'] = t; ev.append((t, 'block', g))
                            else: s['bonk'] = t; ev.append((t, 'bonk', g))
                if s['x'] >= COURSE: s['fin'] = t; ev.append((t, 'fin', g))
        frames.append({g: (st[g]['x'], st[g]['boost'], st[g]['bonk'], st[g]['fin'], st[g]['sleep'], st[g]['shield'], st[g]['strong'], st[g]['pop'], st[g]['atk']) for g in G})
        f += 1
        if all(st[g]['fin'] for g in G if g != NAPPER) or t > 40: break
    return frames, ev, items, st
def leadchanges(frames):
    lead = None; n = 0
    for fr in frames[int(T0 * FPS) + 30:]:
        l = max([g for g in G if g != NAPPER], key=lambda g: fr[g][0])
        if l != lead: n += 1; lead = l
    return n - 1
def tmap_len(ev, tw):
    evt = sorted(set([0.4] + [e[0] for e in ev if e[0] < tw] + [tw])); n = 0; ts = 0.4
    while ts < tw - 1e-9:
        r = 1.0
        for a, b in zip(evt, evt[1:]):
            if a <= ts < b and b - a > 1.8:
                rm = 2.0 if b == tw else 1.7; lo, hi = a + 0.5, b - 0.6
                if lo <= ts < hi: r = 1 + (rm - 1) * min(1, (ts - lo) / 0.3, (hi - ts) / 0.3)
        n += 1; ts = min(tw, ts + r / FPS)
    return n / FPS
def score(seed):
    fr, ev, it, st = sim(seed)
    fins = sorted((s['fin'], g) for g, s in st.items() if g != NAPPER)
    nap = [e[0] for e in ev if e[1] == 'nap']
    if not nap or not (1.0 < nap[0] < 3.2): return None
    twv = tmap_len(ev, fins[0][0])
    if not (float(os.environ.get('TV0', '10.0')) < twv < float(os.environ.get('TV1', '11.2'))): return None
    m = fins[1][0] - fins[0][0]
    lc = leadchanges(fr)
    if not (0.04 < m < 0.35) or lc < int(os.environ.get('LC', '4')): return None
    kinds = [e[1] for e in ev if e[0] < fins[0][0]]
    if 'block' not in kinds or 'sleep' not in kinds: return None
    if os.environ.get('WN') and fins[0][1] != os.environ['WN']: return None
    return fins[0][1], round(m, 2), lc, round(fins[0][0], 1)
def score2(seed):
    fr, ev, it, st = sim(seed)
    fins = sorted((s['fin'], g) for g, s in st.items() if g != NAPPER)
    bt = sorted(set(round(e[0], 2) for e in ev if e[1] in ('pick', 'block', 'smash', 'sleepwave') and e[0] < fins[0][0]))
    clash = sum(1 for i in range(len(bt) - 1) if bt[i + 1] - bt[i] < 0.7)
    return 'clash', clash, fins[0][1], fins[1][1], round(fins[1][0] - fins[0][0], 2), leadchanges(fr), round(fins[0][0], 1), round(tmap_len(ev, fins[0][0]), 2), [(round(e[0], 1), e[1], e[2]) for e in ev if e[1] not in ('bonk', 'fin', 'satk')]
if sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, score2(s), flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, EV, ITEMS, ST = sim(SEED)
fins = sorted((s['fin'], g) for g, s in ST.items() if g != NAPPER); WIN = fins[0][1]; TW = fins[0][0]
T_NAP = [e[0] for e in EV if e[1] == 'nap'][0]
print('winner', WIN, round(TW, 2), [(g, round(t, 2)) for t, g in fins])
# rc18 timeline: video opens 0.4s in (boards already pulling forward under GO!); stretches with no event for >1.8s play
# faster (ramped, up to 1.7x; the last lull before the finish up to 2.0x), every event and the last 0.6s before the line in
# real time; win card 3.6 -> 1.5s
TOFF = float(os.environ.get('TOFF', '0.4')); CARD = 1.8   # review fix: win text held 1.8s
EVT = sorted(set([TOFF] + [e[0] for e in EV if e[0] < TW] + [TW]))
def rate(ts):
    for a, b in zip(EVT, EVT[1:]):
        if a <= ts < b and b - a > 1.8:
            rm = 2.0 if b == TW else 1.7; lo, hi = a + 0.5, b - 0.6
            if lo <= ts < hi: return 1 + (rm - 1) * min(1, (ts - lo) / 0.3, (hi - ts) / 0.3)
    return 1.0
TMAP = []; ts = TOFF
while ts < TW - 1e-9: TMAP.append(ts); ts = min(TW, ts + rate(ts) / FPS)
NRACE = len(TMAP); TWV = NRACE / FPS
NF0 = NRACE + int(CARD * FPS)
CUT = float(os.environ.get('CUT', '3.4'))   # review fix: the slime's nap holds 1.65s   # Oct 29 notes2: expectation break, Cleo napping in the bottom lane gets a slime buddy
NF = NF0 + int(round(CUT * FPS))
T_EM, T_HOP, HOP_D, T_HEART, T_SZ = 0.45, 0.8, 0.45, 1.4, 1.75   # cutscene beats (s after the cut)
def heart(d, cx, cy, s, col=(255, 90, 140)):
    for (x, y) in [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (0, 2)]:
        d.rectangle([cx + x * s - s // 2, cy + y * s - s // 2, cx + x * s + s // 2 - 1, cy + y * s + s // 2 - 1], fill=col)
def cutscene(u, f):
    t = TW + CARD + u; cx_ = 1500.0   # static camera, no finish line in view
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    sx = int(SKYX + cx_ * 0.03) % max(1, SKY.width - W)
    img.alpha_composite(SKY.crop((sx, 160, sx + W, 160 + 640)), (0, 0))
    img.alpha_composite(water(cx_ + u * 40, t), (0, 600))
    layer(img, lambda d: [d.rectangle([0, 600 + k * 4, W, 604 + k * 4], fill=(255, 200, 140, max(0, 120 - k * 12))) for k in range(10)])
    d = ImageDraw.Draw(img)
    for li in range(5):
        ry = ROPE0 + li * 205; d.line([0, ry, W, ry], fill=(240, 240, 240), width=3)
        off = int(-cx_) % 200
        for bx in range(off - 200, W + 200, 200):
            b = BUOY[(f // 4 + (bx - off) // 200) % len(BUOY)]; img.alpha_composite(b, (bx - b.width // 2, ry - b.height // 2 + int(3 * math.sin(t * 3 + bx))))
    y = LY[G.index(NAPPER)]; sx_ = 380 + 18 * u          # Cyrus drifting slowly in his lane, fast asleep (eyes closed), no wake
    land = T_HOP + HOP_D
    dip = 8 * math.exp(-(u - land) / 0.12) * math.sin((u - land) / 0.12 * 2.2) if u >= land else 0   # board takes the slime's weight
    bob = 6 * math.sin(t * 2.2 + 3) + dip
    b = BOARD; s = CSLEEP[12]; bx0, by0 = int(sx_ - b.width / 2), int(y - b.height / 2 + bob); rx0, ry0 = int(sx_ - s.width / 2 + 9), int(y - 234 + bob)
    img.alpha_composite(b, (bx0, by0)); img.alpha_composite(s, (rx0, ry0)); zzz(img, sx_ - 40, ry0 + 150, u + 0.4)
    # the slime: surfaces ahead of her board, hops on the nose, settles, naps too
    sl = SLIME[(f // 3) % len(SLIME)]
    ex = sx_ + 200; nx = sx_ + 30   # lands on his chest
    if T_EM - 0.2 <= u < T_HOP + 0.25:   # ripple where it comes up
        a_ = int(255 * max(0, min(1, (u - T_EM + 0.2) / 0.15, (T_HOP + 0.25 - u) / 0.25)))
        layer(img, lambda dd: dd.ellipse([ex - 44, y + 6, ex + 44, y + 22], outline=(230, 250, 255, a_), width=3))
    if T_EM <= u < T_HOP:                  # rising out of the water, clipped at the waterline
        k = (u - T_EM) / (T_HOP - T_EM); rise = 52 * (1 - (1 - k) ** 2)
        top = int(y + 14 - 124 + 52 - rise)   # visible bottom rises from 52px under the waterline (y+14) up to it
        clip = sl.crop((0, 0, sl.width, max(1, (y + 14) - top)))
        img.alpha_composite(clip, (int(ex - sl.width / 2), top))
    elif u >= T_HOP:
        p = min(1, (u - T_HOP) / HOP_D)
        hx = ex + (nx - ex) * p
        hy = (y + 14) + ((y - 50 + bob) - (y + 14)) * p - 110 * 4 * p * (1 - p)   # parabola: real arc under gravity, onto his chest
        spr = sl
        if u >= land:
            q = (u - land) / 0.16
            if q < 1:
                sq = 1 - 0.22 * math.sin(q * math.pi); spr = sl.resize((int(sl.width * (2 - sq)), max(1, int(sl.height * sq))), Image.NEAREST)
            hx = nx
        img.alpha_composite(spr, (int(hx - spr.width / 2), int(hy - (124 / 128) * spr.height)))
        if u >= T_SZ: zzz(img, nx - 30, hy - 70, (u - T_SZ) * 0.8)
    if u >= T_HEART:   # one heart over the two of them
        q = (u - T_HEART) / 0.18; sc = (1.25 * min(1, q) if q < 1 else 1 + 0.25 * math.exp(-(q - 1) * 2) * math.cos((q - 1) * 3)) * (1 + 0.04 * math.sin(u * 6))
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        hcx, hcy = sx_ + 70, y - 300 - 18 * (u - T_HEART)
        heart(dl, int(hcx), int(hcy), max(2, int(14 * sc)), (20, 10, 30)); heart(dl, int(hcx), int(hcy), max(2, int(11 * sc)))
        img.alpha_composite(L)
    # close-up: 2x integer zoom on Cleo's spot in the bottom lane (her sprite 3x -> 6x) so the payoff reads on a phone
    img = img.crop((150, 795, 150 + W // 2, 795 + H // 2)).resize((W, H), Image.NEAREST)
    if u < 0.3: img.alpha_composite(Image.new('RGBA', (W, H), (10, 8, 20, int(230 * (1 - u / 0.3)))))
    return img
def VT(x):
    import bisect
    if x >= TW: return round(TWV + (x - TW), 3)
    return round(bisect.bisect_left(TMAP, x - 1e-6) / FPS, 3)
print('video finish', round(TWV, 2), 'total', round(NF / FPS + 0.3, 2))
VICF = vic(WIN, 300)
sys.path.insert(0, SP0 + 'fork_rc2'); from rc2 import gummy_src, acv_tag, FF
GUMI = {k: up(gummy_src(k), 3) for k in ('acv', 'mush', 'cre', 'mel')}   # rc18: ACV gummy gloss
# water (low-res procedural, upscaled 4x for pixel look)
WR = (270, 340)
def water(camx, t):
    w, h = WR
    xs = (np.arange(w) * 4 + camx)[None, :]; ys = (np.arange(h) * 4)[:, None]
    yy = np.arange(h)[:, None]
    band = np.sin(yy / 2.3 + 0.8 * np.sin(xs / 140.0 + t * 0.9))
    dash = np.sin(xs / 29.0 - t * 2.2 + yy * 1.7) + 0.5 * np.sin(xs / 71.0 + t * 0.7 + yy * 0.6)
    hi = (band > 0.82) & (dash > 0.9); mid = (band > 0.6) & (dash > 0.2) & ~hi
    base = np.array([30, 120, 168], float)[None, None, :] + (ys / (h * 4))[..., None] * np.array([-18, -52, -50])[None, None, :]
    img = base + hi[..., None] * np.array([120, 120, 85]) + mid[..., None] * np.array([18, 26, 22])
    img = np.clip(img, 0, 255).astype(np.uint8)
    return Image.fromarray(img, 'RGB').resize((w * 4, h * 4), Image.NEAREST).convert('RGBA')
KEYF = [int(float(x) * FPS) for x in os.environ.get('KEYT', '').split(',') if x]
wr = Writer('v80_noaudio.mp4'); events = []; camx = 0.0; seen = set(); OPEN = []
POPS = Pops(1.0, ymin=TRK0 + 8); RAWP = []
for e in EV:
    te, kind, g = e[0], e[1], e[2]
    px_ = FR[min(int(round(te * FPS)), len(FR) - 1)][g][0]
    # rc18: stamps 30-40px -> 52px on a dark outlined plate (see draw_pops)
    if te >= TW: continue
    if kind == 'pick': RAWP.append((VT(te), 'pick', (g, NAME[g] + ': ' + POWER[e[3]][0], POWER[e[3]][1]), True)); events.append((VT(te), SFX[e[3]]))
    elif kind == 'bonk': events.append((VT(te), 'boing'))   # review fix: no BOING! stamps (they stacked); the hop + sfx stay
    elif kind == 'block': RAWP.append((VT(te) + 0.01, 'block', (g, 'BLOCKED!', (110, 230, 90)), True)); events.append((VT(te), 'twinkle'))
    elif kind in ('satk', 'smash') and max(FR[min(int(round(te * FPS)), len(FR) - 1)][h][0] for h in G) - px_ > CAMOFF + OFF + 80: pass   # off screen: no sound for an attack nobody sees
    elif kind == 'satk': events.append((VT(te + hit_at(g) - 0.12), {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'sword_swish', 'cyrus': 'swish'}[g]))
    elif kind == 'smash': RAWP.append((VT(te), 'smash', (g, 'SMASH!', (90, 160, 255)), False)); events.append((VT(te), 'crunch_8bit'))
    elif kind == 'fin': events.append((VT(te), 'ding_8bit'))
def draw_pops(img, items):
    def fn(dd):
        for sx, ty, text, size, col, sw, al in items:
            w = len(text) * size; dd.rounded_rectangle([sx - w / 2 - 14, ty - 10, sx + w / 2 + 14, ty + size + 10], 12, fill=(10, 14, 30, int(210 * al / 255)), outline=tuple(col[:3]) + (al,), width=4)
    layer(img, fn); text_layer(img, [(sx, ty, text, size, col, 7, al) for sx, ty, text, size, col, sw, al in items])
CLEO_OFF = None; ACV_T0 = None
RAWP.append((VT(TW - 0.55), 'photo', (None, 'PHOTO FINISH!', (255, 214, 60)), True))
SCHED = schedule(RAWP, hard_end=TWV)
print('stamps', [(round(a, 2), round(b, 2), p_[1]) for a, b, k_, p_ in SCHED])
NAP_SX0 = None
ICON = {g: up(Image.open(SIDE[g]).convert('RGBA').crop((24, 10, 72, 46)), 2) for g in G}
for f in range(NF):
    if f >= NF0:
        u = (f - NF0) / FPS; img = cutscene(u, f)
        if f == NF0:
            T0V = NF0 / FPS
            events.extend([(round(T0V + T_EM, 3), 'squish'), (round(T0V + T_HOP, 3), 'jump'), (round(T0V + T_HOP + HOP_D, 3), 'squish'), (round(T0V + T_HEART, 3), 'chime')])
        img.alpha_composite(HOOK); wr.write(img)
        if os.environ.get('PV') and f in [int(x) for x in os.environ['PV'].split(',')]: img.convert('RGB').save(f'pv_{f:04d}.png')
        continue
    t = TMAP[f] if f < NRACE else TW + (f - NRACE) / FPS; fi = min(int(round(t * FPS)), len(FR) - 1); fr = FR[fi]
    lead = max(fr[g][0] for g in G)
    target = min(max(0, lead - CAMOFF), COURSE - CAMOFF)
    camx += (target - camx) * 0.12
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    # sky band with slow parallax
    sx = int(SKYX + camx * 0.03) % max(1, SKY.width - W)
    img.alpha_composite(SKY.crop((sx, 160, sx + W, 160 + 640)), (0, 0))
    img.alpha_composite(water(camx, t), (0, 600))  # water from y600, lanes start at rope y660
    # horizon blend
    layer(img, lambda d: [d.rectangle([0, 600 + k * 4, W, 604 + k * 4], fill=(255, 200, 140, max(0, 120 - k * 12))) for k in range(10)])
    d = ImageDraw.Draw(img)
    # finish line + lighthouse
    fx = COURSE - camx + OFF - 123
    if -200 < fx < W + 200:
        for yy in range(ROPE0 - 30, 1840, 30):
            for k in range(2):
                d.rectangle([fx - 15 + k * 15, yy + (15 if k else 0), fx + k * 15, yy + 15 + (15 if k else 0)], fill=(245, 245, 245))
                d.rectangle([fx - 15 + k * 15, yy + (0 if k else 15), fx + k * 15, yy + (15 if k else 30)], fill=(30, 30, 40))
        img.alpha_composite(LH, (int(fx + 30), ROPE0 + 40 - LH.height))
    # lane ropes with buoys
    for li in range(5):
        ry = ROPE0 + li * 205
        d.line([0, ry, W, ry], fill=(240, 240, 240), width=3)
        off = int(-camx) % 200
        for bx in range(off - 200, W + 200, 200):
            b = BUOY[(fi // 4 + (bx - off) // 200) % len(BUOY)]; img.alpha_composite(b, (bx - b.width // 2, ry - b.height // 2 + int(3 * math.sin(t * 3 + bx))))
    # items (drawn on their own layer, faded in from the right so nothing sits in the right-edge / lower-right button zone)
    IL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(IL)
    for it in ITEMS:
        ix = it['x'] - camx + OFF
        if -80 < ix < W + 80:
            y = LY[it['lane']] + int(6 * math.sin(t * 3 + it['x']))
            if it['kind'] == 'gum':
                if it['got'] is None or t < it['got']:
                    g = GUMI[GUM[G[it['lane']]]]  # GOLD FIX: always the lane's product gummy
                    layer(IL, lambda dd: dd.ellipse([ix - 40, y - 60, ix + 40, y + 10], fill=(255, 230, 140, 70)))
                    IL.alpha_composite(g, (int(ix - g.width / 2), int(y - g.height - 6)))
                    d = ImageDraw.Draw(IL); d.ellipse([ix - 26, y - 6, ix + 26, y + 8], outline=(255, 255, 255), width=3)
            elif it.get('smash') is not None and t >= it['smash']:
                u = t - it['smash']
                if u < 0.5: burst(IL, ix, y - 40, u / 0.5, (120, 230, 90), 12, 20, 160); burst(IL, ix, y - 40, u / 0.5, (255, 255, 255), 6, 10, 90)
            else:
                if it.get('smash') is not None and t < it['smash']:   # waiting to be hit: sits still in front of the planted rider
                    s = SLIME[(fi // 3) % len(SLIME)]; IL.alpha_composite(s, (int(ix - s.width / 2), int(y - s.height + 30)))
                elif it['got'] is None or t - it['got'] < 0.6:
                    s = SLIME[(fi // 3) % len(SLIME)]
                    yy = y - (0 if it['got'] is None else int(60 * math.sin((t - it['got']) / 0.6 * math.pi)))
                    IL.alpha_composite(s, (int(ix - s.width / 2), int(yy - s.height + 30)))
                    d = ImageDraw.Draw(IL); d.ellipse([ix - 40, y + 6, ix + 40, y + 22], outline=(230, 250, 255), width=3)
    IL.putalpha(ImageChops.multiply(IL.getchannel('A'), FADE)); img.alpha_composite(IL); d = ImageDraw.Draw(img)
    # surfers
    SX_OVR = {}
    for li, g in enumerate(G):
        x, bt, kt, fin, slp, shd, sgt, popt, atk_t = fr[g]; sx_ = x - camx + OFF; y = LY[li]
        if g == NAPPER and t >= T_NAP:   # asleep for good: drifts slowly back but never leaves the frame
            if NAP_SX0 is None: NAP_SX0 = sx_
            q = min(1, (t - T_NAP) / max(0.1, TW - T_NAP)); q = q * q * (3 - 2 * q)
            sx_ = NAP_SX0 + (float(os.environ.get('NAPX1', '250')) - NAP_SX0) * q; SX_OVR[g] = sx_
        attacking = 0 <= t - atk_t < ATK_D and not (t < slp)
        bob = 6 * math.sin(t * 4 + li)
        if t - kt < 0.7: bob += -20 * math.sin((t - kt) / 0.7 * math.pi)
        asleep = t < slp; boosted = 0 <= t - bt < SPEED_T and fin is None; strong = 0 <= t - sgt < STRONG_T and fin is None
        # wake
        if not asleep and not attacking and not (g == WIN and t >= TW):
            layer(img, lambda dd: [dd.rectangle([sx_ - 130 - k * 34, y + 12 + (k % 2) * 6, sx_ - 110 - k * 30, y + 20 + (k % 2) * 6], fill=(255, 255, 255, 200 - k * 30)) for k in range(6)])
        b = BOARD; s = SPR[g]; bx0, by0 = int(sx_ - b.width / 2), int(y - b.height / 2 + bob); rx0, ry0 = int(sx_ - s.width / 2 + 9), int(y - 234 + bob)
        if boosted:   # mushroom SPEED: orange afterimages + speed lines + spray
            for k in (3, 2, 1):
                img.alpha_composite(tinted(b, (255, 170, 50), int(255 * (0.4 - 0.1 * k))), (bx0 - 46 * k, by0)); img.alpha_composite(tinted(s, (255, 170, 50), int(255 * (0.4 - 0.1 * k))), (rx0 - 46 * k, ry0))
            speed_lines(img, sx_ - 60, y + 10, 1, t, 260)
        if attacking:   # Syeda-based attack animation, feet and body aligned to the side sprite
            s = ATKF[g][frame_idx(t - atk_t, len(ATKF[g]))]
            rx0, ry0 = int(sx_ + 9 + 46 * 3 - 46 * 3 - ATK_CX[g] * 3 + 3 * (SIDE_CX[g] - 46)), int(y - 312 + bob)
        if strong: strong_aura(img, b, bx0, by0, t, 7, 4); strong_aura(img, s, rx0, ry0, t)
        img.alpha_composite(b, (bx0, by0))
        if g == NAPPER and t >= T_NAP:
            k_ = min(12, 5 + int((t - T_NAP) / 0.11)); img.alpha_composite(CSLEEP[k_], (rx0, ry0))   # yawn, lie down, sleep (eyes closed)
            if k_ >= 10: zzz(img, sx_ - 40, ry0 + 150, t - T_NAP)
        elif g == WIN and t >= TW:   # review fix: the win pose replaces the rider, standing on her own board
            vf = VICF[int((t - TW) * 8) % len(VICF)]; WINPOS = (sx_, y + bob)
        elif asleep: sleepy(img, s, rx0, ry0); zzz(img, sx_, ry0 + 20, t - (slp - SLEEP_T))
        else: img.alpha_composite(s, (rx0, ry0))
        if shd: shield(img, sx_, y + 20, 270, 110)
        if popt is not None and 0 <= t - popt < 0.5: shield_pop(img, sx_, y + 20, 270, (t - popt) / 0.5, 110)
    for e in EV:
        if e[1] == 'sleepwave' and 0 <= t - e[0] < 0.7:
            sleep_wave(img, FR[min(int(round(e[0] * FPS)), len(FR) - 1)][e[2]][0] - camx + OFF, LY[G.index(e[2])] - 100, (t - e[0]) / 0.7, 1300)
    if any(e[1] == 'sleepwave' and 0 <= t - e[0] < 0.25 for e in EV): img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 50)))
    def _px(wx, g_, txt, sz):   # pop label in the rider's own lane at chest height: ahead of the board if it fits, else behind
        rx = fr[g_][0] - camx + OFF; w = len(txt) * sz + 20; yy = LY[G.index(g_)] - 60
        xmax = 1010 if yy < 1110 else 880
        if rx + 130 + w <= xmax: return rx + 130 + w / 2, yy
        if rx - 130 - w >= 70: return rx - 130 - w / 2, yy
        return rx + 130 + w / 2, yy
    tv = f / FPS; A_ = active(SCHED, tv)
    if A_ is not None and t < TW:
        st0, en0, key_, (g_, txt, col) = A_; u_ = tv - st0; sz = 48 if len(txt) <= 10 else 40
        sc_ = 1 + 0.25 * max(0, 1 - u_ / 0.12); al = int(255 * min(1, (en0 - tv) / 0.2)); w_ = len(txt) * sz * sc_ + 20
        if g_ is None: xx, yy = 478, 618
        else:
            rx = (SX_OVR[g_] if g_ in SX_OVR else fr[g_][0] - camx + OFF); yy = LY[G.index(g_)] - 330
            xmax = 1010 if yy < 1040 else 870; xx = min(max(rx, 70 + w_ / 2 + 14), xmax - w_ / 2 - 14)
        draw_pops(img, [(xx, yy, txt, int(sz * sc_), col, 7, al)])
    # ACV GUMMY label on the first ACV gummy while it is on screen (max 1.6s, gone once picked)
    ia = min((it_ for it_ in ITEMS if it_['kind'] == 'gum' and GUM[G[it_['lane']]] == 'acv'), key=lambda z: z['x'])
    iax = ia['x'] - camx + OFF
    if ia['got'] is None or t < ia['got']:
        if iax < 900 and ACV_T0 is None: ACV_T0 = t
    if False:
        acv_tag(img, int(iax), int(LY[G.index('joy')] - GUMI['acv'].height - 6), int(255 * min(1, (ACV_T0 + 1.6 - t) / 0.25)), xmax=1010)
    # Cleo drops off the left edge after the second SLEEP: small callout in her lane
    csx = fr['cleo'][0] - camx + OFF

    if False:
        a_ = int(255 * min(1, (CLEO_OFF + 1.4 - t) / 0.2)); draw_pops(img, [(470, LY[G.index('cleo')] - 80, 'CLEO FALLS BEHIND!', 44, COL['cleo'], 7, a_)])
    if TW - 0.55 <= t < TW:
        if not any(e_[1] == 'whistle' for e_ in events): events.append((VT(TW - 0.55), 'ding_8bit')); events.append((VT(TW - 0.55), 'whistle'))    # rc18: the progress strip (15px portraits stacked on each other) is removed
    # lane names at start
    if t < T0 + 1.6:
        a = int(255 * min(1, max(0, (T0 + 1.6 - t) / 0.4)))
        if t < TOFF + 0.6: text_layer(img, [(760, 940, "GO!", 130, (255, 214, 60), 10, int(255 * min(1, (TOFF + 0.6 - t) / 0.25)))])
        if f == 0: events.append((0.0, 'go_8bit'))
    if t >= TW:
        u = t - TW
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(10, 8, 20, int(110 * min(1, u / 0.4)))))
        wx_, wy_ = WINPOS; lw = G.index(WIN); bb_ = BOARD
        img.alpha_composite(bb_, (int(wx_ - bb_.width / 2), int(LY[lw] - bb_.height / 2 + (wy_ - LY[lw]))))   # her board, lit, under the pose
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (int(wx_ - vf.width / 2), int(wy_ - vf.height + 4)))
        tx_ = min(max(wx_, 70 + 300), 1010 - 300)
        text_layer(img, [(tx_, int(wy_ - vf.height - 110), NAME[WIN] + ' WINS!', 64, COL[WIN], 8, 255)])
        if not any(e[1] == 'victory' for e in events): events.append((VT(TW), 'victory')); events.append((VT(TW + 0.1), 'cheer'))
    img.alpha_composite(HOOK_END if t >= TW else HOOK)
    wr.write(img)
    if f < 9: OPEN.append(img.copy())
    if os.environ.get('PV') and f in [int(x) for x in os.environ['PV'].split(',')]: img.convert('RGB').save(f'pv_{f:04d}.png')
    if f in KEYF: img.convert('RGB').save(f'k80_{f}.png')
for im_ in OPEN: wr.write(im_)          # loop: cut back to the opening
wr.close()
json.dump(events, open('v80_ev.json', 'w'))
print('done', NF / FPS + 0.3, 'cut starts', NF0, round(NF0 / FPS, 3))
