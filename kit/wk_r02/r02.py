# r02: 1:1 recreation of igref/Dd4TeRFSsqG (running-track obstacle race) with Code Name's guides, in the r01 look (wk_r01/env.py).
# Roles: Cyrus = axolotl (grabbed by the slime 8.4, knocked out by it in the cones 28.1), Cleo = axolotl's wall slide + stuck in the net
# + left behind in the cones, Rayleigh = penguin (hurdle trip 3.64, slime knock 5.6, cone trip 27.4, naps just short of the line 30.94),
# Joy = octopus (hurdle trip 3.9, cone flip 27.1, walks past the napper and wins 32.0). Slime = the duck (ballistic hops only).
# Backdrop: Liza's Royal Castle training yard (pause/assets/vit_hd.gif). World native 270x480 drawn 4x.
import numpy as np, glob, math, random, subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy.interpolate import PchipInterpolator
OUTD = os.path.dirname(os.path.abspath(__file__)); S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S_ + 'wk_r01'); import env as ENV
import bubble as BUB
ENV.BG_FILE = 'pause/assets/vit_hd.gif'
FONT = S_ + 'npmfont/ps/package/files/PressStart2P.ttf'
HOOK = ['WHO CROSSES', 'THE LINE FIRST?']          # hook wording: edit here only
HOOK_COL = [(255, 255, 255), (255, 214, 60)]
WIN_TXT = 'WINNER!'
W, H, FPS, K = 1080, 1920, 30, 4
NW, NH = W // K, H // K
END = 35.4; NF = int(round(END * FPS))
G = 1400.0
_fc = {}
def F(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
def load(d): return [Image.open(f).convert('RGBA') for f in sorted(glob.glob(d + '/*.png'))]
def gif(p, size=92):
    im = Image.open(p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA').resize((size, size), Image.NEAREST))
    return fr
GS = ['cyrus', 'cleo', 'ray', 'joy']; LANE = {g: i for i, g in enumerate(GS)}
P = S_ + 'pixellab/'; R1 = S_ + 'wk_r01/gen/'; R2 = OUTD + '/gen/'
RUN = {g: load(P + f'race/{g}_run') for g in GS}
KO = {g: load(P + f'king/{g}_ko') for g in GS}
JUMP = {'joy': load(R1 + 'joy_jump'), 'ray': load(R1 + 'ray_jump'), 'cleo': load(R1 + 'cleo_jump'), 'cyrus': load(P + 'plat/cyrus_jump')}
JAIR = {'joy': (6, 10), 'ray': (6, 10), 'cleo': (6, 10), 'cyrus': (5, 9)}
JLAND = {'joy': [11, 12], 'ray': [11, 12], 'cleo': [11, 12], 'cyrus': [10, 11]}
CLIMB = {g: load(R2 + f'{g}_climb') for g in GS}
CRAWL = {g: load(R2 + f'{g}_crawl') for g in GS}
NAP = load(R2 + 'ray_nap')
PANIC = load(R1 + 'cyrus_panic_f')
IDLE_J = [f.resize((184, 184), Image.NEAREST) for f in gif(S_ + 'pause/assets/idle_0.gif')]     # Joy's idle (mouth closed), 2x for the winner card
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int); a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
SLIME = [nored(f.crop((0, 0, 64, 64))) for f in load(P + 'race/slime_idle_c')]
CROWN = Image.open(P + 'ref/crown_cands/01.png').convert('RGBA'); CROWN = CROWN.crop(CROWN.getbbox())
def foot(fr): b = fr.getbbox(); return ((b[0] + b[2]) / 2, b[3])
REF = {}
for g in GS:
    REF[('run', g)] = foot(RUN[g][0]); REF[('jump', g)] = foot(JUMP[g][0]); REF[('ko', g)] = foot(KO[g][0])
    REF[('climb', g)] = foot(CLIMB[g][0]); REF[('crawl', g)] = foot(CRAWL[g][0])
REF['nap'] = foot(NAP[0])
CLIMB_DX = {'cleo': 22, 'joy': 22, 'ray': 19, 'cyrus': 19}    # anchor -> wall face (Cleo/Joy's sets carry their own pole edge)
def place(fr, ax, ay, ref): return fr, ax - ref[0], ay - ref[1]
def bottom_place(fr, cx, by):
    b = fr.getbbox(); return fr, cx - (b[0] + b[2]) / 2, by - b[3]
def head(fr):
    a = np.array(fr)[..., 3] > 0; ys = np.where(a.any(1))[0]; top = ys[0]; xs = np.where(a[top:top + 6].any(0))[0]; return ((xs.min() + xs.max()) / 2, top)
# ------------------------------------------------------------------ camera (reference scroll speeds, full-res px/s)
CSEG = [(0, 0), (2.8, 0), (3.0, 240), (4.5, 260), (5.0, 290), (6.0, 300), (6.4, 440), (7.2, 440), (7.5, 190), (8.4, 200), (8.7, 400), (9.6, 400),
        (9.9, 260), (12.0, 250), (12.3, 140), (13.2, 150), (13.5, 280), (14.2, 260), (14.5, 115), (17.2, 115), (17.5, 480), (18.7, 480), (19.0, 150),
        (20.7, 150), (21.0, 460), (21.7, 460), (22.0, 190), (23.8, 190), (24.1, 450), (24.8, 450), (25.1, 240), (25.8, 240), (26.1, 450), (29.2, 450),
        (29.4, 20), (30.3, 40), (30.5, 560), (31.1, 560), (31.4, 0), (99, 0)]
_ts = np.array([a for a, b in CSEG]); _vs = np.array([b for a, b in CSEG]) / K
TT = np.arange(NF + 60) / FPS
_v = np.interp(TT, _ts, _vs); _v = np.convolve(_v, np.ones(7) / 7, 'same'); _v[:int(2.8 * FPS)] = 0
CAM = np.concatenate([[0.0], np.cumsum(_v / FPS)])[:len(TT)]
CAM[int(31.4 * FPS):] = CAM[int(31.4 * FPS)]
def cam(t): return float(np.interp(t * FPS, np.arange(len(CAM)), CAM))
# ------------------------------------------------------------------ layout (native)
BT, LH, NL = 116, 64, 4
LT = [BT + LH * i for i in range(NL)]; SURF = [lt + 46 for lt in LT]; BB = BT + LH * NL
START_X = 44; START_LINE = 70
FX = int(cam(31.4) + 110)                                       # finish line: screen x 110 native when the camera settles
WX = int(cam(14.3) + 0.5 * NW + 6); WW, WH = 34, 40              # one climbing wall across all lanes (log palisade)
NX = int(cam(21.0) + 0.98 * NW); NLEN = 60; NHGT = 32            # cargo nets
# ------------------------------------------------------------------ runner tracks
def fk(t, f): return ('f', t, f)
def wk(t, x): return ('w', t, x)
def hold(t): return ('h', t)
KEYS = {
 'cyrus': [wk(0, START_X), wk(2.75, START_X), fk(3.2, .30), fk(4.0, .52), fk(5.0, .62), fk(6.0, .68), fk(7.0, .70), fk(7.9, .66), fk(8.4, .64), hold(11.3),
           fk(11.75, -.14), fk(12.4, .40), fk(13.3, .55), wk(14.6, WX - CLIMB_DX['cyrus']), hold(17.3), wk(17.5, WX + WW - 8), wk(17.8, WX + WW + 16),
           fk(18.6, .62), fk(19.6, .58), fk(20.6, .58), wk(22.1, NX - 6), wk(22.9, NX + NLEN + 8), hold(23.0), fk(23.8, .64), fk(24.8, .62), fk(25.8, .62),
           fk(26.6, .62), fk(27.4, .62), fk(28.1, .62), ('r', 28.55, 26), hold(99)],
 'cleo':  [wk(0, START_X), wk(2.75, START_X), fk(3.2, .26), fk(4.0, .44), fk(5.0, .50), fk(6.0, .54), fk(7.0, .54), fk(8.0, .50), fk(9.0, .54), fk(10.0, .50),
           fk(11.0, .50), fk(12.0, .50), fk(13.0, .48), wk(13.7, WX - CLIMB_DX['cleo']), hold(17.0), wk(17.45, WX + WW + 16), hold(17.75),
           fk(18.6, .48), fk(19.6, .48), fk(20.6, .48), wk(21.55, NX - 6), wk(21.75, NX + 22), hold(24.5), wk(24.65, NX + 26), fk(25.4, .46), fk(26.4, .50),
           fk(27.4, .50), fk(28.2, .48), wk(28.7, None), ('r', 29.0, 10), hold(99)],
 'ray':   [wk(0, START_X), wk(2.75, START_X), fk(3.2, .30), fk(3.64, .45), ('r', 3.95, 12), hold(4.1), fk(4.6, .52), fk(5.3, .60), fk(5.6, .62), ('r', 5.75, 3), hold(9.0),
           fk(9.2, -.14), fk(9.9, .40), fk(11.0, .45), fk(12.0, .48), fk(13.0, .45), fk(13.8, .45), wk(14.3, WX - CLIMB_DX['ray']), hold(17.0),
           wk(17.45, WX + WW + 16), hold(17.75), fk(18.6, .56), fk(19.6, .60), fk(20.6, .60), fk(21.5, .58), wk(22.0, NX - 6), wk(22.8, NX + NLEN + 8), hold(22.9),
           fk(23.8, .64), fk(24.8, .62), fk(25.8, .60), fk(26.6, .60), fk(27.4, .62), ('r', 27.6, 10), hold(27.75), fk(28.5, .58), fk(29.3, .60), fk(30.3, .55),
           wk(30.94, FX - 44), hold(99)],
 'joy':   [wk(0, START_X), wk(2.75, START_X), fk(3.2, .24), fk(3.9, .44), ('r', 4.2, 12), hold(7.9), fk(8.0, -.14), fk(8.6, .40), fk(9.5, .48), fk(10.5, .45), fk(11.5, .47),
           fk(12.5, .45), fk(13.5, .46), wk(14.3, WX - CLIMB_DX['joy']), hold(17.0), wk(17.45, WX + WW + 16), hold(17.75), fk(18.6, .52), fk(19.6, .52), fk(20.6, .50),
           fk(21.5, .50), wk(22.0, NX - 6), wk(22.8, NX + NLEN + 8), hold(22.95), fk(23.8, .58), fk(24.8, .55), fk(25.8, .55), fk(26.6, .55), fk(27.1, .56),
           ('r', 27.6, 30), hold(27.85), fk(28.5, .50), fk(29.3, .48), fk(30.3, .40), wk(30.94, FX - 118), wk(31.4, FX - 80), wk(32.0, FX), wk(32.45, FX + 40), hold(99)],
}
def build_track(keys):
    ts, xs = [], []
    for k in keys:
        if k[0] == 'h': ts.append(k[1]); xs.append(xs[-1]); continue
        if k[0] == 'r': ts.append(k[1]); xs.append(xs[-1] + k[2]); continue
        kind, t, v = k
        if kind == 'w' and v is None: v = cam(t) + 0.48 * NW
        ts.append(t); xs.append(v if kind == 'w' else cam(t) + v * NW)
    ts = np.array(ts); xs = np.maximum.accumulate(np.array(xs, float))
    keep = np.concatenate([[True], np.diff(ts) > 1e-6]); ts, xs = ts[keep], xs[keep]
    return PchipInterpolator(ts, xs)(np.clip(TT, ts[0], ts[-1]))
X = {g: build_track(KEYS[g]) for g in GS}
def xat(g, t): return float(np.interp(t * FPS, np.arange(len(X[g])), X[g]))
# ------------------------------------------------------------------ scripted spans (one gag at a time, reference beat times)
T_GO = 2.75
SP = {
 'cyrus': [(8.4, 11.3, 'panic'), (14.6, 17.3, 'climb'), (17.3, 17.5, 'top'), (17.5, 17.8, 'down'), (22.1, 22.9, 'crawl'), (22.9, 23.0, 'standup'),
           (28.1, 28.55, 'crashed'), (28.55, 99, 'lie')],
 'cleo':  [(13.7, 15.15, 'climb'), (15.15, 15.85, 'slide'), (15.85, 16.0, 'wallbottom'), (16.0, 16.85, 'climb2'), (16.85, 17.0, 'top'), (17.0, 17.45, 'over'),
           (17.45, 17.75, 'lie'), (21.55, 21.75, 'crawl'), (21.75, 24.5, 'stuck'), (24.5, 24.65, 'free'), (28.7, 29.0, 'trip'), (29.0, 99, 'lie')],
 'ray':   [(3.64, 3.95, 'trip'), (3.95, 4.1, 'lie'), (5.6, 5.75, 'knock'), (5.75, 9.0, 'lie'), (14.3, 16.85, 'climb'), (16.85, 17.0, 'top'), (17.0, 17.45, 'over'),
           (17.45, 17.75, 'lie'), (22.0, 22.8, 'crawl'), (22.8, 22.9, 'standup'), (27.4, 27.6, 'trip'), (27.6, 27.75, 'lie'), (30.94, 99, 'nap')],
 'joy':   [(3.9, 4.2, 'trip'), (4.2, 7.9, 'lie'), (14.3, 16.85, 'climb'), (16.85, 17.0, 'top'), (17.0, 17.45, 'over'), (17.45, 17.75, 'lie'),
           (22.0, 22.8, 'crawl'), (22.8, 22.95, 'standup'), (27.1, 27.6, 'flip'), (27.6, 27.85, 'lie'), (32.45, 99, 'win')],
}
GETUP = {('ray', 4.1), ('ray', 17.75), ('ray', 27.75), ('joy', 17.75), ('joy', 27.85), ('cleo', 17.75), ('cleo', 24.65)}     # dust puff covers each get-up
def span(g, t):
    for a, b, k in SP[g]:
        if a <= t < b: return a, b, k
    return None
CLIMB_T = {'cyrus': (14.6, 17.3), 'cleo': (13.7, 15.15), 'ray': (14.3, 16.85), 'joy': (14.3, 16.85)}
# ------------------------------------------------------------------ obstacles
OB = {li: [] for li in range(NL)}                                 # dict(kind, x, fallen_t)
def gag_x(g, t): return xat(g, t) + 6
GAG_OB = {('ray', 'hurdle'): gag_x('ray', 3.64), ('joy', 'hurdle'): gag_x('joy', 3.9), ('joy', 'cone'): gag_x('joy', 27.1),
          ('ray', 'cone'): gag_x('ray', 27.4), ('cleo', 'cone'): gag_x('cleo', 28.7)}
GAG_T = {('ray', 'hurdle'): 3.64, ('joy', 'hurdle'): 3.9, ('joy', 'cone'): 27.1, ('ray', 'cone'): 27.4, ('cleo', 'cone'): 28.7}
def lying_ranges(g):
    out = []
    for a, b, k in SP[g]:
        if k in ('lie', 'panic', 'trip', 'knock', 'flip', 'crashed', 'nap', 'stuck'): out.append((xat(g, a) - 30, xat(g, min(b, END)) + 34))
    return out
H_END = cam(7.5) + NW; C0 = cam(26.0) + NW * 0.9; C_END = cam(29.2) + NW * 0.5
for li, g in enumerate(GS):
    bad = lying_ranges(g)
    x = 118 + li * 16
    while x < H_END:
        if not any(a <= x <= b for a, b in bad): OB[li].append(dict(kind='hurdle', x=x, fall=None))
        x += 64
    x = C0 + li * 17
    while x < C_END:
        if not any(a <= x <= b for a, b in bad): OB[li].append(dict(kind='cone', x=x, fall=None))
        x += 50
for (g, kind), gx in GAG_OB.items():
    li = LANE[g]; OB[li] = [o for o in OB[li] if abs(o['x'] - gx) > 40]
    OB[li].append(dict(kind=kind, x=gx, fall=GAG_T[(g, kind)]))
for li in range(NL): OB[li].sort(key=lambda o: o['x'])
# hops over obstacles (ballistic, from the x track): (t0, t1, x_obstacle)
HOPS = {g: [] for g in GS}
HALF = {'hurdle': 19, 'cone': 15}
for g in GS:
    li = LANE[g]
    for o in OB[li]:
        if o['fall'] is not None and GAG_T.get((g, o['kind'])) == o['fall'] and abs(GAG_OB[(g, o['kind'])] - o['x']) < 1: continue
        xa, xb = o['x'] - HALF[o['kind']], o['x'] + HALF[o['kind']]
        fa = next((f for f in range(NF) if X[g][f] >= xa), None); fb = next((f for f in range(NF) if X[g][f] >= xb), None)
        if fa is None or fb is None or fb <= fa: continue
        if any(span(g, f / FPS) for f in range(fa, fb + 1)) or fa / FPS < T_GO: continue
        HOPS[g].append((fa / FPS, fb / FPS, o['x']))
def hop_at(g, t):
    for a, b, ox in HOPS[g]:
        if a <= t < b: return a, b
    return None
# ------------------------------------------------------------------ slime plan (ballistic hops only)
def ballistic(p0, p1, T, tt):
    u = tt / T; return p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - 0.5 * G * T * T * u * (1 - u)
SL = []                                                          # (t0, t1, kind, data)
def sl_hops(pts, t0, t1):
    n = len(pts) - 1; d = (t1 - t0) / n
    for i in range(n): SL.append((t0 + i * d, t0 + (i + 1) * d, 'hop', (pts[i], pts[i + 1])))
def ground_pts(li, xs): return [(x, SURF[li]) for x in xs]
# act 1: hops in along Rayleigh's lane behind him, lands on his head at 5.6 (he's knocked flat), bounces off ahead
def ray_head(t):
    f = int(round(t * FPS)); fr, ox, oy = sprite_for('ray', f); hx, hy = head(fr); return ox + hx, oy + hy + 2
_a1 = [cam(2.9) - 20] + [cam(2.9) - 20 + (xat('ray', 5.1) - 10 - cam(2.9) + 20) * k / 5 for k in range(1, 6)]
# act 3 (8.0-8.4): from lane 1 up onto Cyrus's head; act 4 (25.3-28.1): along Cyrus's lane, into him
def cyr_head(t):
    f = int(round(t * FPS)); fr, ox, oy = sprite_for('cyrus', f); hx, hy = head(fr); return ox + hx, oy + hy + 2
# ------------------------------------------------------------------ sprite selection
def ground(li): return SURF[li]
def sprite_for(g, f):
    t = f / FPS; li = LANE[g]; x = X[g][f]; sp = span(g, t)
    if t < T_GO: return place(RUN[g][0], x, SURF[li], REF[('run', g)])
    if sp: return special(g, f, *sp)
    h = hop_at(g, t)
    if h:
        a, b = h; u = (t - a) / (b - a); T = b - a; y = SURF[li] - 0.5 * G * T * T * u * (1 - u)
        j0, j1 = JAIR[g]; j = j0 + min(j1 - j0, int(u * (j1 - j0 + 1)))
        return bottom_place(JUMP[g][j], x, y)
    since = min([t - b for a, b, ox in HOPS[g] if b <= t] + [9])
    if since < 0.1: return place(JUMP[g][JLAND[g][0 if since < 0.05 else 1]], x, SURF[li], REF[('jump', g)])
    dist = DIST[g][f]
    return place(RUN[g][1 + int(dist / 6.5) % 8], x, SURF[li], REF[('run', g)])
def special(g, f, a, b, k):
    t = f / FPS; li = LANE[g]; x = X[g][f]; u = (t - a) / max(1e-6, b - a)
    if k == 'panic':
        fr = PANIC[1] if t - a < 0.1 else PANIC[2 + int(t * 10) % 7]; sh = 1 if (f // 2) % 2 else -1
        fx, fy, fz = bottom_place(fr, x + sh, SURF[li]); return fx, fy, fz
    if k in ('trip', 'knock'):                                    # impact frames, then pitches forward onto the track
        tt = t - a
        fr = KO[g][1] if tt < 0.07 else KO[g][2] if tt < 0.14 else KO[g][3 + min(4, int((tt - 0.14) * 20))]
        return bottom_place(fr, x, SURF[li])
    if k == 'lie':
        if g == 'cleo' and a >= 17: pass
        return bottom_place(KO[g][8], x, SURF[li])
    if k == 'crashed':                                            # knocked along the track by the slime, tumbling under gravity
        T = b - a; y = SURF[li] - 0.5 * G * T * T * u * (1 - u) * 0.3
        return bottom_place(KO[g][3 + int((t - a) * 18) % 5], x, y)
    if k == 'flip':                                               # clips the cone and flips: ballistic tumble
        T = b - a; y = SURF[li] - 0.5 * G * T * T * u * (1 - u) * 0.45
        return bottom_place(KO[g][1 if t - a < 0.06 else 3 + int((t - a) * 16) % 5], x, y)
    if k in ('climb', 'climb2'):
        c0, c1 = CLIMB_T[g] if k == 'climb' else (16.0, 16.85)
        if g == 'cleo' and k == 'climb': h = 30 * min(1, (t - c0) / (c1 - c0))
        elif g == 'cleo': h = WH * (t - c0) / (c1 - c0)
        else: h = WH * min(1, max(0, (t - c0 - 0.15) / (c1 - c0 - 0.15)))
        fr = CLIMB[g][0] if t - c0 < 0.12 else CLIMB[g][1 + int(h / 3.2) % 8]
        return place(fr, WX - CLIMB_DX[g], SURF[li] - h, REF[('climb', g)])
    if k == 'slide':                                              # loses grip near the top and slides back down the wall face
        tt = t - a; h = max(0.0, 30 - 0.5 * (0.45 * G) * tt * tt)
        return place(CLIMB[g][3], WX - CLIMB_DX[g], SURF[li] - h, REF[('climb', g)])
    if k == 'wallbottom': return place(CLIMB[g][1], WX - CLIMB_DX[g], SURF[li], REF[('climb', g)])
    if k == 'top':
        xx = WX + 7 if g != 'cyrus' else WX + 6 + (WW - 14) * u
        return place(RUN[g][0] if g != 'cyrus' else RUN[g][1 + int(u * 6) % 8], xx, SURF[li] - WH, REF[('run', g)])
    if k == 'over':                                               # the three tumble over the top together and drop to the track
        T = b - a; x0, x1 = WX + 9, WX + WW + 16; y0, y1 = SURF[li] - WH, SURF[li]
        y = y0 + (y1 - y0) * u - 0.5 * G * T * T * u * (1 - u) * 0.6
        return bottom_place(KO[g][3 + int((t - a) * 16) % 5], x0 + (x1 - x0) * u, y)
    if k == 'down':                                               # Cyrus jumps down clean
        T = b - a; x0, x1 = WX + WW - 8, WX + WW + 16; y0, y1 = SURF[li] - WH, SURF[li]
        y = y0 + (y1 - y0) * u - 0.5 * G * T * T * u * (1 - u)
        j0, j1 = JAIR[g]; j = j0 + min(j1 - j0, int(u * (j1 - j0 + 1)))
        return bottom_place(JUMP[g][j], x0 + (x1 - x0) * u, y)
    if k == 'crawl':
        tt = t - a; fr = CRAWL[g][1] if tt < 0.06 else CRAWL[g][2] if tt < 0.12 else CRAWL[g][3 + int(DIST[g][f] / 4.0) % 6]
        return place(fr, x, SURF[li], REF[('crawl', g)])
    if k == 'stuck':
        fr = CRAWL[g][3 + int(t * 9) % 6]; sh = (1 if (f // 2) % 2 else -1)
        return place(fr, x + sh, SURF[li], REF[('crawl', g)])
    if k in ('free', 'standup'): return place(RUN[g][0], x, SURF[li], REF[('run', g)])
    if k == 'nap':
        tt = t - a; j = min(6, int(tt / 0.09)) if tt < 0.6 else 7 + int((tt - 0.6) * 5) % 6
        return place(NAP[j], x, SURF[li], REF['nap'])
    if k == 'win':
        fr = IDLE_J[int(t * 6) % len(IDLE_J)]; return bottom_place(fr, x, SURF[li])
    return place(RUN[g][0], x, SURF[li], REF[('run', g)])
DIST = {}
for g in GS:
    d = np.concatenate([[0], np.cumsum(np.abs(np.diff(X[g][:NF + 1])))]); DIST[g] = d
# slime segments (need sprite_for for head positions)
SL += []
sl_hops(ground_pts(2, _a1), 2.9, 5.1)
SL.append((5.1, 5.6, 'hop', ((_a1[-1], SURF[2]), None)))           # last hop: onto Rayleigh's head (filled below)
SL.append((5.6, 5.95, 'hop', (None, (xat('ray', 5.6) + 40, SURF[2]))))
_p = [xat('ray', 5.6) + 40]
SL.append((5.95, 6.4, 'hop', ((_p[0], SURF[2]), (_p[0] + 44, SURF[1]))))
SL.append((6.4, 6.85, 'hop', ((_p[0] + 44, SURF[1]), (_p[0] + 92, SURF[0]))))
_cx = [cam(7.3) + 0.40 * NW, cam(7.75) + 0.48 * NW]
SL.append((6.85, 7.3, 'hop', ((_p[0] + 92, SURF[0]), (_cx[0], SURF[0]))))
SL.append((7.3, 7.75, 'hop', ((_cx[0], SURF[0]), (_cx[1], SURF[0]))))
SL.append((7.75, 8.4, 'hop', ((_cx[1], SURF[0]), 'cyr')))
SL.append((8.4, 11.3, 'ride', 'cyrus'))
_b = [cam(25.3) - 20 + k * ((xat('cyrus', 27.6) - 30) - (cam(25.3) - 20)) / 5 for k in range(6)]
sl_hops(ground_pts(0, _b), 25.3, 27.6)
SL.append((27.6, 28.1, 'hop', ((_b[-1], SURF[0]), 'cyrhit')))
SL.append((28.1, 28.5, 'hop', ('cyrhit', (xat('cyrus', 28.1) - 20, SURF[0]))))
SL.append((28.5, 99, 'sit', (xat('cyrus', 28.1) - 20, SURF[0])))
def _resolve(p, t):
    if p is None: return ray_head(5.55)
    if p == 'cyr': return cyr_head(8.4)
    if p == 'cyrhit': return (xat('cyrus', 28.1) - 10, SURF[0] - 34)
    return p
def slime_at(t):
    for a, b, k, d in SL:
        if a <= t < b:
            if k == 'hop':
                p0, p1 = _resolve(d[0], t), _resolve(d[1], t); x, y = ballistic(p0, p1, b - a, t - a)
                return x, y, 'squash' if (b - t) < 0.06 or (t - a) < 0.05 else 'air'
            if k == 'ride': hx, hy = cyr_head(t); return hx, hy, 'ride'
            if k == 'sit': return d[0], d[1], 'sit'
    return None
# ------------------------------------------------------------------ drawing (native)
_N = np.random.RandomState(5).rand(96, 256)
def track(img, cam_):
    """castle training-yard path: packed earth and pebbles (Liza-palette dirt from the grass tile), rope lane lines on stakes"""
    a = np.array(img); Gt = ENV.GRASS
    for li in range(NL):
        y0, y1 = LT[li] + 1, LT[li] + LH
        ys = np.arange(y0, y1); xs = (np.arange(NW) + int(cam_)) % 64
        rows = Gt[26 + (ys - y0 + li * 9) % 36][:, xs, :3].astype(np.float32)
        depth = ((ys - y0) / (y1 - y0))[:, None, None]
        col = rows * (1.18 - 0.12 * depth) + np.array([10, 6, 0])
        a[y0:y1, :, :3] = np.clip(col, 0, 255).astype(np.uint8); a[y0:y1, :, 3] = 255
    img = Image.fromarray(a); d = ImageDraw.Draw(img)
    for li in range(1, NL):                                          # rope lane lines on little stakes
        y = LT[li]; d.line([0, y + 1, NW, y + 1], fill=(70, 46, 30)); d.line([0, y, NW, y], fill=(204, 168, 110))
        off = int(cam_) % 40
        for xx in range(-off, NW + 40, 40):
            d.rectangle([xx - 1, y - 4, xx + 1, y + 3], fill=(60, 38, 24)); d.line([xx, y - 3, xx, y + 2], fill=(150, 104, 62))
    return img
def draw_hurdle(d, x, y, fallen_u=None):
    """wooden training hurdle: two posts and a log bar"""
    if fallen_u is None:
        for px in (x - 6, x + 6):
            d.rectangle([px - 1, y - 16, px + 1, y + 1], fill=(56, 34, 20)); d.line([px, y - 15, px, y], fill=(150, 100, 58))
        d.rectangle([x - 9, y - 18, x + 9, y - 14], fill=(56, 34, 20)); d.rectangle([x - 8, y - 17, x + 8, y - 15], fill=(160, 108, 62))
        d.line([x - 8, y - 17, x + 8, y - 17], fill=(206, 156, 98)); d.ellipse([x - 10, y - 18, x - 7, y - 14], fill=(196, 150, 96))
        d.rectangle([x - 7, y - 9, x + 7, y - 8], fill=(110, 72, 40))
    else:                                                            # knocked over: tips forward and lies flat
        ang = min(1.0, fallen_u) * math.pi / 2; L = 17
        tx, ty = x + math.sin(ang) * L, y - math.cos(ang) * L
        d.line([x, y, tx, ty], fill=(56, 34, 20), width=3); d.line([x, y, tx, ty], fill=(150, 100, 58), width=1)
        d.ellipse([tx - 4, ty - 3, tx + 4, ty + 3], fill=(56, 34, 20)); d.ellipse([tx - 3, ty - 2, tx + 3, ty + 2], fill=(160, 108, 62))
def draw_cone(d, x, y, fallen_u=None):
    """small wooden barrel (the reference's cones)"""
    if fallen_u is None:
        d.rounded_rectangle([x - 6, y - 13, x + 6, y], 3, fill=(46, 26, 16)); d.rounded_rectangle([x - 5, y - 12, x + 5, y - 1], 3, fill=(150, 92, 48))
        d.line([x - 3, y - 11, x - 3, y - 2], fill=(196, 132, 74)); d.line([x + 3, y - 11, x + 3, y - 2], fill=(116, 68, 34))
        for yy in (y - 10, y - 4): d.line([x - 5, yy, x + 5, yy], fill=(150, 150, 160)); d.line([x - 5, yy + 1, x + 5, yy + 1], fill=(70, 70, 82))
    else:                                                            # tips over and rolls a little
        dx = 12 * min(1, fallen_u)
        d.ellipse([x + dx - 7, y - 11, x + dx + 7, y], fill=(46, 26, 16)); d.ellipse([x + dx - 6, y - 10, x + dx + 6, y - 1], fill=(150, 92, 48))
        d.line([x + dx - 3, y - 10, x + dx - 3, y - 1], fill=(150, 150, 160)); d.line([x + dx + 3, y - 10, x + dx + 3, y - 1], fill=(150, 150, 160))
def draw_wall(img, d, li, cam_):
    x0 = int(WX - cam_); y0, y1 = SURF[li] - WH, SURF[li] + 4
    if x0 > NW + 4 or x0 + WW < -4: return
    for k in range(0, WW, 6):                                     # vertical logs
        d.rectangle([x0 + k, y0 + (k % 12 == 0) * 2 - 3, x0 + k + 5, y1], fill=(64, 40, 24))
        d.rectangle([x0 + k + 1, y0 + (k % 12 == 0) * 2 - 2, x0 + k + 4, y1 - 1], fill=(132, 88, 52))
        d.line([x0 + k + 1, y0 + 2, x0 + k + 1, y1 - 2], fill=(170, 120, 74)); d.line([x0 + k + 4, y0, x0 + k + 4, y1 - 1], fill=(98, 62, 36))
        d.ellipse([x0 + k + 1, y0 + (k % 12 == 0) * 2 - 4, x0 + k + 4, y0 + (k % 12 == 0) * 2 - 1], fill=(196, 150, 96))
    d.rectangle([x0 - 1, y0 + 8, x0 + WW, y0 + 10], fill=(80, 56, 34)); d.rectangle([x0 - 1, y1 - 10, x0 + WW, y1 - 8], fill=(80, 56, 34))
    rs = random.Random(li)
    for k in range(7):
        hx, hy = x0 + 3 + rs.randint(0, WW - 6), y0 + 4 + rs.randint(0, WH - 6); c = rs.choice([(232, 96, 96), (96, 160, 232), (240, 196, 64), (110, 200, 110)])
        d.rectangle([hx - 1, hy - 1, hx + 2, hy + 1], fill=(30, 20, 14)); d.rectangle([hx, hy - 1, hx + 1, hy], fill=c)
    ENV.shadow(d, x0 + WW / 2, SURF[li] + 4, WW + 6, 60)
def draw_net(img, li, cam_, t, stuck=False):
    d = ImageDraw.Draw(img); x0 = NX - cam_; x1 = x0 + NLEN; yb = SURF[li] + 1; yt = SURF[li] - NHGT
    if x1 < -4 or x0 > NW + 4: return
    wob = 0
    if stuck and 21.75 <= t < 24.5: wob = 2 * math.sin(t * 22)
    if stuck and 24.5 <= t < 24.8: wob = -3 * math.exp(-(t - 24.5) * 12) * math.cos((t - 24.5) * 40)
    for px in (x0, x1):
        d.rectangle([px - 2, yt - 4, px + 1, yb], fill=(60, 40, 26)); d.rectangle([px - 1, yt - 3, px, yb - 1], fill=(200, 130, 60))
    def ytop(xx):
        u = (xx - x0) / NLEN; return yt + 4 * math.sin(math.pi * u) + wob * math.sin(math.pi * u)
    col = (54, 50, 46)
    for xx in np.arange(x0, x1 + 0.1, 5):
        d.line([xx, ytop(xx), xx + 1, yb], fill=col)
    for k in range(0, NHGT, 5):
        pts = [(xx, ytop(xx) + k * (yb - ytop(xx)) / NHGT) for xx in np.arange(x0, x1 + 0.1, 3)]
        d.line(pts, fill=col)
    d.line([(xx, ytop(xx)) for xx in np.arange(x0, x1 + 0.1, 2)], fill=(120, 110, 96), width=1)
def draw_finish(img, d, cam_):
    fx = FX - cam_
    if fx > NW + 70: return
    for li in range(NL):
        for yy in range(LT[li] + 2, LT[li] + LH - 1, 3):
            for kk in range(2):
                d.rectangle([fx - 6 + kk * 3, yy, fx - 4 + kk * 3, yy + 2], fill=(240, 240, 236) if (yy // 3 + kk) % 2 else (30, 30, 34))
def draw_start(d, cam_):
    sx = START_LINE - cam_
    if sx < -3: return
    d.rectangle([sx - 1, BT, sx + 1, BB - 1], fill=(245, 245, 240))
    for li in range(NL):
        d.rectangle([sx - 30, SURF[li] + 4, sx - 3, SURF[li] + 5], fill=(232, 228, 214))
FX_ = []
def puff(t0, x, y, big=False): FX_.append((t0, 'puff_b' if big else 'puff', x, y))
def zzz(d, x, y, t, t0):
    for k in range(3):
        u = ((t - t0) * 0.6 + k / 3) % 1.0; zx = x + 4 + k * 3 + 6 * u; zy = y - 6 - 22 * u; s = 2 + k
        a = int(255 * (1 - u))
        if a < 30: continue
        c = (238, 240, 255, a)
        ENV.blend(d._image, zx - 1, zy - 1, s + 3, s + 3, lambda dd, s=s, c=c: (dd.line([1, 1, s + 1, 1], fill=c), dd.line([s + 1, 1, 1, s + 1], fill=c), dd.line([1, s + 1, s + 1, s + 1], fill=c)))
def draw_fx(img, cam_, t):
    for t0, kind, x, y in FX_:
        u = t - t0
        if 0 <= u < 0.45:
            n = 10 if kind == 'puff_b' else 7; rs = random.Random(int(t0 * 100) + int(x))
            for i in range(n):
                ang = rs.uniform(math.pi, 2 * math.pi); sp_ = rs.uniform(20, 46) * (1.5 if kind == 'puff_b' else 1)
                px = x + math.cos(ang) * sp_ * u - cam_; py = y + math.sin(ang) * sp_ * u * 0.5 + 30 * u * u; r = 2 + 3 * (1 - u / 0.45)
                a = int(220 * (1 - u / 0.45))
                ENV.blend(img, px - r - 1, py - r - 1, 2 * r + 3, 2 * r + 3, lambda dd, r=r, a=a: dd.ellipse([1, 1, 2 * r + 1, 2 * r + 1], fill=(236, 220, 190, a)))
def top_slime(img, sl, cam_, t):
    x, y, k = sl; fr = SLIME[int(t * 10) % len(SLIME)]
    if k == 'air': fr = SLIME[2]
    if k == 'squash': fr = SLIME[5]
    if k == 'sit': fr = SLIME[int(t * 6) % len(SLIME)]
    bb = fr.getbbox(); img.alpha_composite(fr, (int(round(x - cam_ - (bb[0] + bb[2]) / 2)), int(round(y - bb[3]))))
# scripted fx
for g, t0 in GETUP: puff(t0, xat(g, t0), SURF[LANE[g]])
puff(3.7, xat('ray', 3.8), SURF[2]); puff(3.98, xat('joy', 4.05), SURF[3]); puff(5.62, xat('ray', 5.62), SURF[2], True)
puff(15.86, WX - 8, SURF[1], True); for_ = [puff(17.47, WX + WW + 16, SURF[LANE[g]], True) for g in ('cleo', 'ray', 'joy')]
puff(17.82, WX + WW + 16, SURF[0]); puff(24.5, NX + 26, SURF[1], True); puff(27.62, xat('joy', 27.6), SURF[3], True)
puff(27.5, xat('ray', 27.5), SURF[2]); puff(28.1, xat('cyrus', 28.1), SURF[0] - 20, True); puff(28.56, xat('cyrus', 28.55), SURF[0])
puff(28.8, xat('cleo', 28.8), SURF[1]); puff(31.25, FX - 30, SURF[2], True); puff(32.42, FX + 40, SURF[3] - 30, True)
for (g, s0, s1) in [('ray', 22.8, 0), ('joy', 22.8, 0), ('cyrus', 22.9, 0)]: puff(s0, xat(g, s0), SURF[LANE[g]])
# ------------------------------------------------------------------ text
def ctext(d, x, y, t, f, fill, sw=8, sf=(20, 15, 35)):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=sf)
def strip(img, lines, cols, px, a=1.0):
    HY0 = 250; gap = 18; y1 = HY0 + 36 + len(lines) * px + (len(lines) - 1) * gap
    L_ = Image.new('RGBA', img.size, (0, 0, 0, 0)); D_ = ImageDraw.Draw(L_); D_.rectangle([0, HY0, W, y1], fill=(10, 8, 20, int(170 * a)))
    y = HY0 + 18
    for l, c in zip(lines, cols):
        w = D_.textlength(l, font=F(px)); D_.text((W / 2 - w / 2, y), l, font=F(px), fill=c + (int(255 * a),), stroke_width=7, stroke_fill=(20, 15, 35, int(255 * a))); y += px + gap
    img.alpha_composite(L_)
T_CD = [(0.2, 0.7, '3'), (0.9, 1.35, '2'), (1.6, 2.1, '1'), (2.3, 2.75, 'GO!')]
T_CROWN = 32.5; T_WIN = 32.8; T_HOOK = (7.3, 7.6)
BUBBLES = [(3.68, 0.85, 'ray', 'OOF!', 'right'), (8.45, 1.0, 'cyrus', 'AAAH!', 'right'), (15.2, 0.9, 'cleo', 'NOOO!', 'right'),
           (22.9, 1.0, 'cleo', 'STUCK!', 'right'), (31.65, 0.8, 'ray', 'ZZZ...', 'up'), (33.05, 1.2, 'joy', 'YAY?', 'right')]
def head_screen(g, f, cam_):
    fr, ox, oy = sprite_for(g, f); hx, hy = head(fr); return ((ox - cam_ + hx) * K, (oy + hy) * K)
JOY_END = FX + 40
_jf = IDLE_J[0]; _jb = _jf.getbbox()
def joy_head_pt(fr, x, y):
    """crown anchor: centre of the face (skin pixels) under the hair top"""
    a = np.array(fr); al = a[..., 3] > 0; R, Gc, B = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    top = np.where(al.any(1))[0][0]
    skin = al & (R > 170) & (Gc > 95) & (Gc < 205) & (B < 150) & (R - B > 70)
    ys, xs = np.where(skin[top:top + 50]); return x + (xs.min() + xs.max()) / 2, y + top + 3
OCC = {}; OVL = []
def render(f):
    t = f / FPS; cam_ = CAM[f]
    img = Image.new('RGBA', (NW, NH), (0, 0, 0, 0)); img = track(img, cam_); d = ImageDraw.Draw(img)
    ENV.ledge(d, BT - 4, BT, NW, cam_); ENV.ledge(d, BB - 1, BB + 2, NW, cam_)              # edges first: nothing that rises above the band is cut by them
    draw_start(d, cam_); draw_finish(img, d, cam_)
    sprites = {li: [] for li in range(NL)}
    for g in GS:
        fr, ox, oy = sprite_for(g, f); sp = span(g, t); sprites[LANE[g]].append((fr, ox - cam_, oy, g, sp[2] if sp else ('air' if hop_at(g, t) else 'run')))
    sl = slime_at(t)
    fx = FX - cam_
    if fx < NW + 70: img.alpha_composite(ENV.ARCH, (int(fx - 3 - ENV.ARCH.width / 2), int(BT + 2 - ENV.ARCH.height)))   # behind everyone
    d = ImageDraw.Draw(img)
    for li in range(NL):                                       # pass 1: all scenery
        for o in OB[li]:
            sx = o['x'] - cam_
            if -12 < sx < NW + 12:
                fu = None if (o['fall'] is None or t < o['fall']) else (t - o['fall']) / 0.18
                (draw_hurdle if o['kind'] == 'hurdle' else draw_cone)(d, sx, SURF[li], fu)
        draw_wall(img, d, li, cam_)
    chars = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))
    for li in range(NL):                                       # pass 2: characters always in front of the scenery
        for fr, x, y, gg, k in sprites[li]:                   # soft shadows on the track
            bb = fr.getbbox(); cx = x + (bb[0] + bb[2]) / 2; bot = y + bb[3]
            ground_y = SURF[li] - (WH if k == 'top' else 0)
            hgt = ground_y - bot
            if k in ('climb', 'climb2', 'slide', 'wallbottom'): continue
            if 0 <= hgt < 50: ENV.shadow(d, cx, ground_y + 1, max(8, (bb[2] - bb[0]) * 0.7 - hgt / 4), 70 - hgt)
        for fr, x, y, gg, k in sprites[li]:
            img.alpha_composite(fr, (int(round(x)), int(round(y)))); chars.alpha_composite(fr, (int(round(x)), int(round(y))))
        if sl and sl[2] in ('ride',) and li == 0: top_slime(img, sl, cam_, t); top_slime(chars, sl, cam_, t)
    if sl and sl[2] != 'ride': top_slime(img, sl, cam_, t); top_slime(chars, sl, cam_, t)
    a0 = np.array(img); ca = np.array(chars); full = ca[..., 3] == 255; full[BB + 3:] = False
    OCC[f] = int((full & (np.abs(a0[..., :3].astype(int) - ca[..., :3].astype(int)).sum(2) > 6)).sum())
    for li in range(NL): draw_net(img, li, cam_, t, stuck=(GS[li] == 'cleo'))   # nets drape over the crawlers on purpose
    d = ImageDraw.Draw(img)
    for fr, x, y, gg, k in sprites[2]:
        if gg == 'ray' and k == 'nap' and t > 31.6: zzz(d, x + fr.getbbox()[2] - 30, y + fr.getbbox()[1], t, 31.6)
    draw_fx(img, cam_, t)
    # crown: drops from above under gravity onto Joy's head
    if t >= T_CROWN:
        fr, ox, oy = sprite_for('joy', f); hx, hy = joy_head_pt(fr, ox - cam_, oy)
        cy_end = hy - CROWN.height + 6; T = 0.3; u = min(1.0, (t - T_CROWN) / T)
        cy = cy_end - 0.5 * G * T * T * (1 - u) ** 2 * 1.0 if u < 1 else cy_end
        img.alpha_composite(CROWN, (int(hx - CROWN.width / 2), int(cy)))
    a_ = np.array(img); a_[BB + 3:] = 0; img = Image.fromarray(a_); d = ImageDraw.Draw(img)
    over = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))
    for fr, x, y, gg, k in sprites[0]: over.alpha_composite(fr, (int(round(x)), int(round(y))))
    if sl and sl[1] < BT: top_slime(over, sl, cam_, t)
    over = over.crop((0, 98, NW, BT)).resize((W, (BT - 98) * K), Image.NEAREST)
    big = ENV.backdrop(t, cam_, BT - 4, BB + 3, K).convert('RGBA'); big.alpha_composite(img.resize((W, H), Image.NEAREST)); D = ImageDraw.Draw(big)
    if t < T_HOOK[1]:
        strip(big, HOOK, HOOK_COL, 52, 1.0 if t < T_HOOK[0] else (T_HOOK[1] - t) / (T_HOOK[1] - T_HOOK[0])); big.alpha_composite(over, (0, 98 * K))
    for t0, dur, g, txt, side in BUBBLES:                          # speech bubbles: on-screen text only, one at a time
        if t0 <= t < t0 + dur:
            r = BUB.draw(big, txt, head_screen(g, f, cam_), side, t, t0, dur, K)
            for gg in GS:
                if gg == g or not r: continue
                fr_, ox_, oy_ = sprite_for(gg, f); bb_ = fr_.getbbox()
                q = ((ox_ - cam_ + bb_[0]) * K, (oy_ + bb_[1]) * K, (ox_ - cam_ + bb_[2]) * K, (oy_ + bb_[3]) * K)
                if q[0] < r[2] and q[2] > r[0] and q[1] < r[3] and q[3] > r[1]: OVL.append((round(t, 2), txt, gg))
    for a, b, txt in T_CD:
        if a <= t < b:
            u = t - a; sc = 1.0 + 0.35 * max(0, 1 - u / 0.12)
            fs = int((190 if txt != 'GO!' else 150) * sc); ctext(D, 600, 1000 - fs // 2, txt, F(fs), (232, 52, 52), 12, (255, 255, 255))
    if t >= T_WIN:
        u = t - T_WIN; sc = min(1.0, 0.4 + u / 0.12) if u < 0.12 else 1.0 + 0.06 * max(0, 1 - (u - 0.12) / 0.15)
        fs = int(96 * sc); ctext(D, 450, 600 - fs // 2, WIN_TXT, F(fs), (255, 214, 40), 10, (40, 24, 10))
        if u < 0.9:
            rs = random.Random(5)
            for i in range(26):
                vx = rs.uniform(-520, 520); vy = rs.uniform(-700, -150); c = rs.choice([(120, 230, 210), (255, 120, 150), (255, 220, 80), (150, 180, 255)])
                px = 450 + vx * u; py = 600 + vy * u + 900 * u * u; D.rectangle([px, py, px + 11, py + 11], fill=c)
    return big, img
def write_events():
    ev = [(0.2, 'tick_8bit'), (0.9, 'tick_8bit'), (1.6, 'tick_8bit'), (2.3, 'go_8bit')]
    for g in GS:
        for a, b, ox in HOPS[g]: ev.append((a, 'jump'))
    for a, b, k, dd in SL:
        if k == 'hop': ev.append((b - 0.02, 'jump'))
    ev += [(3.64, 'punch'), (3.66, 'brick_8bit'), (3.75, 'squish'), (3.9, 'punch'), (3.92, 'brick_8bit'), (4.0, 'squish'), (4.1, 'poof'),
           (5.6, 'squish'), (5.61, 'punch'), (5.66, 'boing'), (8.4, 'squish'), (8.42, 'boing'),
           (15.15, 'slip_r01'), (15.2, 'whoosh_8bit'), (15.85, 'stomp_8bit'), (17.0, 'whoosh_8bit'), (17.45, 'stomp_8bit'), (17.47, 'punch'), (17.75, 'poof'),
           (21.75, 'boing'), (22.6, 'boing'), (23.4, 'boing'), (24.5, 'poof'), (24.52, 'boing'),
           (27.1, 'punch'), (27.12, 'whoosh_8bit'), (27.6, 'stomp_8bit'), (27.4, 'punch'), (27.45, 'squish'), (28.1, 'punch'), (28.11, 'squish'), (28.12, 'boom_short'),
           (28.7, 'punch'), (28.75, 'squish'), (30.94, 'whoosh_8bit'), (31.2, 'stomp_8bit'), (31.25, 'squish'),
           (32.0, 'ding_8bit'), (32.42, 'twinkle'), (32.5, 'whoosh_8bit'), (32.8, 'win_sting'), (32.82, 'victory'), (32.9, 'cheer')] + [(t0, 'reeltick_8bit') for t0, dur, g, txt, side in BUBBLES]
    ev = sorted([(round(a, 3), b) for a, b in ev if 0 <= a < END - 0.1])
    json.dump({'events': ev, 'end': END, 'FX': FX, 'WX': WX, 'NX': NX}, open(OUTD + '/r02_events.json', 'w'), indent=1)
if __name__ == '__main__':
    STILLS = [float(v) for v in os.environ.get('STILLS', '').split(',') if v]
    if STILLS:
        for s in STILLS: render(int(round(s * FPS)))[0].convert('RGB').save(OUTD + f'/st_{s:.2f}.png')
        sys.exit()
    out = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + '/r02_noaudio_tmp.mp4'], stdin=subprocess.PIPE)
    low = 0
    for f in range(NF):
        big, nat = render(f); out.stdin.write(big.convert('RGB').tobytes())
    out.stdin.close(); out.wait(); os.replace(OUTD + '/r02_noaudio_tmp.mp4', OUTD + '/r02_noaudio.mp4')
    print('bubble overlaps:', OVL[:20]); print('done', NF, 'frames with occluded character pixels:', sum(1 for v in OCC.values() if v > 0), 'max', max(OCC.values()))
    write_events()
