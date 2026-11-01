# r01: 1:1 recreation of igref/DerujF_BHAA (side-scrolling obstacle race over water) with Code Name's guides.
# Roles: Cyrus = axolotl (slime victim x2), Joy = lane 2 (rope slip, lies flat, Rayleigh walks over her),
# Rayleigh = penguin (knocked in by the slime, swims, rolls down the hill, WINNER), Cleo = octopus (drops off the
# monkey bars, swims out; rolls off the hill into the water). Slime = the duck (hops ballistically, never flies).
# World is drawn at native pixel scale (270x480) and upscaled 4x NEAREST (v2: guides 4x, winner pose 8x); text is drawn at 1080x1920.
import numpy as np, glob, math, random, subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont
from scipy.interpolate import PchipInterpolator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import env as ENV
OUTD = os.path.dirname(os.path.abspath(__file__)); S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
FONT = S_ + 'npmfont/ps/package/files/PressStart2P.ttf'
HOOK = ['WHO MAKES IT', 'ACROSS FIRST?']          # hook wording (pending Bennett): edit here only
HOOK_COL = [(255, 255, 255), (255, 214, 60)]
WIN_TXT = 'WINNER!'
W, H, FPS, K = 1080, 1920, 30, 4
NW, NH = W // K, H // K
END = 37.1; NF = int(round(END * FPS))
G = 1400.0                                         # gravity, native px/s^2 (= 4200 screen px/s^2)
_fc = {}
def F(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
# ------------------------------------------------------------------ sprites (native px, Syeda/PixelLab only)
def load(d):
    return [Image.open(f).convert('RGBA') for f in sorted(glob.glob(d + '/*.png'))]
def gif(p, size=92):
    im = Image.open(p); fr = []
    for i in range(im.n_frames):
        im.seek(i); fr.append(im.convert('RGBA').resize((size, size), Image.NEAREST))
    return fr
GS = ['cyrus', 'joy', 'ray', 'cleo']
LANE = {'cyrus': 0, 'joy': 1, 'ray': 2, 'cleo': 3}
P = S_ + 'pixellab/'
RUN = {g: load(P + f'race/{g}_run') for g in GS}
KO = {g: load(P + f'king/{g}_ko') for g in GS}
JUMP = {'joy': load(OUTD + '/gen/joy_jump'), 'ray': load(OUTD + '/gen/ray_jump'), 'cleo': load(OUTD + '/gen/cleo_jump'), 'cyrus': load(P + 'plat/cyrus_jump')}
JAIR = {'joy': (6, 10), 'ray': (6, 10), 'cleo': (6, 10), 'cyrus': (5, 9)}
JLAND = {'joy': [11, 12], 'ray': [11, 12], 'cleo': [11, 12], 'cyrus': [10, 11]}
HANG = {'joy': load(OUTD + '/gen/joy_hang')[2:], 'ray': load(OUTD + '/gen/ray_hang62')[2:], 'cleo': load(OUTD + '/gen/cleo_hang')[2:], 'cyrus': load(OUTD + '/gen/cyrus_hang')[2:]}
SWIM = {'ray': load(S_ + 'fork4/ray_swim')[4:8], 'cleo': load(S_ + 'fork4/cleo_swim3')[4:]}
SWROW = {'ray': 41, 'cleo': 62}      # v3: Cleo's prone body half under the surface (her set's own drawn waterline sits at row ~71)      # the row of each swim set's own drawn waterline -> lane waterline
PANIC = {'cyrus': load(OUTD + '/gen/cyrus_panic_f')}          # v2: PixelLab from Syeda's front Cyrus: hands on head, wide eyes, mouth closed
SLIP = load(OUTD + '/gen/cleo_slip2')                              # v2: Cleo loses one hand on the bar
from PIL import ImageOps
REACH = [ImageOps.mirror(f) for f in load(OUTD + '/gen/ray_reach')]   # v2: Rayleigh kneels, reaches down, pulls up (mirrored: he faces back toward Cleo)
VIC = [f.resize((184, 184), Image.NEAREST) for f in gif(S_ + 'pause/assets/vic_victoryPose_1.gif')]   # winner card 2x
SLIME = [f.crop((0, 0, 64, 64)) for f in load(P + 'race/slime_idle_c')]
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
SLIME = [nored(f) for f in SLIME]
def foot(fr):                                      # (centre x, bottom y) of a frame's opaque box
    b = fr.getbbox(); return ((b[0] + b[2]) / 2, b[3])
REF = {}                                           # one anchor per animation set = its first (standing) frame
for g in GS:
    REF[('run', g)] = foot(RUN[g][0]); REF[('ko', g)] = foot(KO[g][0]); REF[('jump', g)] = foot(JUMP[g][0])
    REF[('hang', g)] = foot(HANG[g][0])
REF[('reach', 'ray')] = foot(REACH[0])
def head(fr):                                      # top-of-head point (centre of the top 8 rows of the box)
    a = np.array(fr)[..., 3] > 0; ys = np.where(a.any(1))[0]; top = ys[0]
    xs = np.where(a[top:top + 8].any(0))[0]; return ((xs.min() + xs.max()) / 2, top)
# ------------------------------------------------------------------ camera (measured from the reference, native px)
CV = np.clip(np.load(OUTD + '/camv.npy'), 0, None) / K * 1.0
CAM0 = np.concatenate([[0.0], np.cumsum(CV)])[:NF + 60]
def cam0(t): return float(np.interp(t * FPS, np.arange(len(CAM0)), CAM0))
# ------------------------------------------------------------------ layout (native)
BT, LH, NL = 116, 64, 4
LT = [BT + LH * i for i in range(NL)]
SURF = [lt + 46 for lt in LT]                       # standing line on platforms
WL = [s + 11 for s in SURF]                         # waterline for swimmers
BB = BT + LH * NL                                  # band bottom 498 (1494 screen): clear of the caption zone
DOCK_X = 88
# ------------------------------------------------------------------ runner tracks: screen-fraction keyframes (from the reference)
def fk(t, f): return (t, 'f', f)
def wk(t, x): return (t, 'w', x)
KEYS = {
 'ray':   [wk(0, 44), wk(2.36, 44), fk(2.9, .31), fk(4.0, .42), fk(4.75, .50), fk(5.62, .55), ('rel', 5.86, 24), ('rel', 7.2, 46), ('rel', 8.2, 70),
           fk(8.6, -.08), fk(9.0, .12), fk(9.4, .30), fk(10.2, .32), fk(11.0, .36), fk(12.0, .37), fk(13.0, .30), fk(13.95, .27), fk(14.75, .56),
           fk(15.3, .60), fk(16.2, .48), fk(17.2, .46), fk(18.2, .50), fk(19.2, .55), fk(20.2, .44), fk(21.2, .40), ('W', 22.95, 60), ('rel', 23.17, 2), ('hold', 23.6), ('rel', 23.95, 40),
           fk(24.6, .48), fk(25.2, .52), fk(26.0, .56), fk(27.0, .58), fk(28.0, .58), fk(29.0, .55), fk(30.0, .58), fk(30.7, .60),
           fk(31.2, .56), fk(31.7, .56), fk(32.2, .62), fk(32.6, .80), fk(33.0, 1.12)],
 'cyrus': [wk(0, 44), wk(2.36, 44), fk(2.9, .28), fk(4.0, .60), fk(4.5, .70), fk(5.0, .75), fk(5.5, .70), fk(5.95, .66), ('hold', 9.6),
           fk(10.55, -.10), fk(11.0, .10), fk(11.9, .45), fk(12.5, .60), fk(13.0, .70), fk(13.6, .72), fk(14.4, .78), fk(15.0, .70), fk(16.0, .58),
           fk(17.0, .55), fk(18.0, .55), fk(19.0, .60), fk(20.0, .62), fk(21.0, .60), fk(22.0, .58), fk(23.0, .55), fk(24.0, .46), fk(25.0, .45),
           fk(26.0, .48), fk(27.0, .50), fk(28.0, .55), fk(29.15, .50), ('hold', 33.5)],
 'joy':   [wk(0, 44), wk(2.36, 44), fk(2.9, .25), fk(4.0, .40), fk(5.0, .38), fk(6.0, .42), fk(7.0, .56), fk(8.0, .60), fk(9.0, .50), fk(10.0, .42),
           fk(11.0, .45), fk(12.0, .50), fk(13.0, .55), fk(13.45, .55), ('hold', 13.72), ('rel', 13.98, 4), ('hold', 15.3), ('rel', 15.75, 26),
           fk(16.4, .50), fk(17.2, .42), fk(18.2, .40), fk(19.2, .45), fk(20.2, .50), fk(21.2, .54), fk(22.2, .55), fk(23.0, .50), fk(24.0, .40),
           fk(25.0, .42), fk(26.0, .45), fk(27.0, .45), fk(28.0, .42), fk(29.0, .35), fk(30.0, .24), fk(31.0, .10), fk(32.0, -.08), fk(33.0, -.2)],
 'cleo':  [wk(0, 44), wk(2.36, 44), fk(2.9, .22), fk(4.0, .42), fk(5.0, .55), fk(5.5, .62), fk(6.0, .66), fk(7.0, .72), fk(8.0, .76), fk(8.6, .74),
           fk(9.0, .55), fk(10.0, .46), fk(11.0, .55), fk(12.0, .55), fk(13.0, .55), fk(14.0, .56), fk(15.0, .40), fk(16.0, .30), fk(17.0, .32),
           fk(18.0, .38), fk(19.0, .40), fk(20.0, .52), fk(21.0, .66), fk(21.6, .76), ('hold', 22.88), ('rel', 23.3, 16), ('W', 23.76, 31), ('W', 23.96, 64), ('hold', 24.05),
           fk(24.4, .40), fk(25.2, .45), fk(26.2, .55), fk(27.0, .66), fk(28.0, .68), fk(29.0, .62), fk(30.0, .64), fk(30.7, .66),
           fk(31.2, .66), fk(31.7, .66), fk(32.02, .68), ('rel', 32.2, 10), ('rel', 33.5, 30)],
}
TT = np.arange(NF + 60) / FPS
def build_track(keys, cam):
    ts, xs = [], []
    for k in keys:
        if k[0] == 'hold': ts.append(k[1]); xs.append(xs[-1]); continue
        if k[0] == 'rel': ts.append(k[1]); xs.append(xs[-1] + k[2]); continue
        if k[0] == 'W': ts.append(k[1]); xs.append(XCF + k[2]); continue            # world x relative to Cleo's bar-drop spot
        t, kind, v = k; ts.append(t); xs.append(v if kind == 'w' else cam(t) + v * NW)
    xs = np.maximum.accumulate(np.array(xs))       # never backwards
    return PchipInterpolator(ts, xs, extrapolate=True)(np.clip(TT, ts[0], ts[-1] + 5))
# camera tail: the reference camera catches up with the winner and settles; end with Rayleigh at screen x ~250 native
X = {}
X['cleo'] = None
def cam_fn(t): return CAMF[min(len(CAMF) - 1, max(0, int(round(t * FPS))))]
CAMF = CAM0.copy()
_kc = KEYS['cleo'][:next(i for i, k in enumerate(KEYS['cleo']) if k[0] == 'W')]
_tmp = build_track(_kc, cam0); XCF = float(np.interp(21.6 * FPS, np.arange(len(_tmp)), _tmp))
X['cleo'] = build_track(KEYS['cleo'], cam0)
X['ray'] = build_track(KEYS['ray'], cam0)
i0 = int(33.0 * FPS); i1 = int(34.3 * FPS); x0 = X['ray'][i0]; v0 = (X['ray'][i0] - X['ray'][i0 - 1]) * FPS; Tq = (i1 - i0) / FPS
def herm(u, x1):
    h00, h10, h01 = 2 * u**3 - 3 * u**2 + 1, u**3 - 2 * u**2 + u, -2 * u**3 + 3 * u**2
    return h00 * x0 + h10 * Tq * v0 + h01 * x1
uc = (33.85 - 33.0) / Tq
D_ = min(range(60, 900), key=lambda D: abs(herm(uc, x0 + D) - (x0 + D - 58)))
X_RFIN = x0 + D_; FIN_X = int(X_RFIN - 58)
for i in range(i0, len(X['ray'])): X['ray'][i] = herm(min(1.0, (i - i0) / (i1 - i0)), X_RFIN)
CAM_END = X_RFIN - 168
c = CAM0[int(32.6 * FPS)]; v = (CAM0[int(32.6 * FPS)] - CAM0[int(32.6 * FPS) - 1]) * FPS
for i in range(int(32.6 * FPS), len(CAMF)):
    tgt = min(CAM_END, X['ray'][i] - 168)
    a = 30.0 * (tgt - c) - 11.0 * v; a = max(-900.0, min(900.0, a))
    v = max(0.0, v + a / FPS); c = min(CAM_END, c + v / FPS); CAMF[i] = c
for g in ['cyrus', 'joy']: X[g] = build_track(KEYS[g], cam0)
def xat(g, t): return float(np.interp(t * FPS, np.arange(len(X[g])), X[g]))
# ------------------------------------------------------------------ course (per lane solids)
class Solid:
    def __init__(s, kind, x0, x1, **kw): s.kind, s.x0, s.x1 = kind, x0, x1; s.__dict__.update(kw)
    def top(s, x):
        if s.kind == 'rope':
            u = (x - s.x0) / max(1, s.x1 - s.x0); return s.y + 3.0 * (1 - (2 * u - 1) ** 2)
        if s.kind == 'hill': return s.f(x)
        if s.kind == 'dome':                               # v5: the rock prop's own top contour
            c = int(x - s.x0); c = max(0, min(len(ENV.ROCK_TOP) - 1, c)); return s.y - 1 + (ENV.ROCK_TOP[c] - ENV.ROCK_TOP.min())
        return s.y
rng = random.Random(7)
T_SEC = [2.36, 9.0, 10.0, 10.6, 14.45, 16.3, 19.3, 23.6, 26.3, 30.7]   # A pills | B long | C pads | C ropes | D pads | E stones | F bars | G long | H hill
def bound(li, t):
    g = GS[li]
    if g == 'cyrus' and 6.0 < t < 10.7: return cam0(t) + .55 * NW
    if g == 'ray' and t == 23.6: return XCF + 84
    return xat(g, t)
COURSE = []
BARY = [s - 74 for s in SURF]
for li in range(NL):
    s0 = SURF[li]; L = [Solid('startdock', -60, DOCK_X, y=s0)]
    b = [bound(li, t) for t in T_SEC]
    x = DOCK_X + 22
    while x < b[1] - 60:                                # A: short floating pills
        w = rng.randint(66, 86); L.append(Solid('pill', x, x + w, y=s0)); x += w + rng.randint(26, 34)
    L.append(Solid('long', x, b[2] - 14, y=s0)); x = b[2] + 12                     # B: long pill
    while x < b[3] - 30: L.append(Solid('pad', x, x + 34, y=s0)); x += 34 + 20      # C: orange pads with gaps
    L.append(Solid('pad', x, x + 30, y=s0)); x += 30
    while x < b[4] - 20:                                # C: ropes strung pad to pad
        rl = rng.randint(100, 120); L.append(Solid('rope', x, x + rl, y=s0)); x += rl
        L.append(Solid('pad', x, x + 30, y=s0)); x += 30
    x += 16
    while x < b[5] - 20: L.append(Solid('pad', x, x + 34, y=s0)); x += 34 + rng.randint(16, 20)   # D: pads with gaps
    k = li
    while x < b[6] - 30:                                # E: domes and tall pillars, staggered by lane
        if k % 3 == 2: L.append(Solid('pillar', x, x + 26, y=s0 - 30)); x += 26 + 20
        else: L.append(Solid('dome', x + 3, x + 3 + ENV.ROCK.width, y=s0 - 2)); x += 32 + 18
        k += 1
    bx0 = x + 16; bx1 = b[7] - 10
    L.append(Solid('bar', bx0, bx1, y=BARY[li] + 64))   # F: monkey bars (virtual feet line while hanging)
    gx = bx0 - 6; greens = []
    while gx < bx1 - 30: greens.append(Solid('green', gx, gx + 42, y=s0)); gx += 42 + 34
    x = bx1 + 26
    while x < b[8] - 40:                                # G: long flat pills
        w = rng.randint(150, 190); L.append(Solid('long', x, min(x + w, b[8] - 20), y=s0)); x += w + 24
    L.append(Solid('greens', 0, 0, items=greens))
    COURSE.append(L)
# H: hill per lane (climb to a crest, long taper toward the finish); lane 4's ends early into the water
HILL_H = 40
for li in range(NL):
    g = GS[li]; s0 = SURF[li]
    hx0 = bound(li, 26.3) + 10
    xc = xat(g, 30.7) if g in ('ray', 'cleo') else bound(li, 30.7) + 40
    xe = FIN_X - 1 if li != 3 else xat('cleo', 32.02) + 4
    def mk(hx0=hx0, xc=xc, xe=(FIN_X - 1), s0=s0, HILL_H=(12 if li == 0 else HILL_H)):   # lane 1 lower: keeps Cyrus + slime below the top 250px
        def f(x):
            if x <= xc: u = (x - hx0) / (xc - hx0); return s0 - HILL_H * (0.5 - 0.5 * math.cos(math.pi * min(1, max(0, u))))
            u = (x - xc) / (xe - xc); return s0 - HILL_H * (1 - min(1, max(0, u))) ** 2
        return f
    f = mk(xe=xe)
    COURSE[li].append(Solid('hill', hx0, xe, f=f, xc=xc))
    COURSE[li].append(Solid('dock', FIN_X, FIN_X + 900, y=s0))
# ---- patches so every scripted beat stands on something solid (or is over open water)
def solids(li): return [s for s in COURSE[li] if s.kind not in ('greens',)]
def greens(li): return [s for s in COURSE[li] if s.kind == 'greens'][0].items
def ensure_on(li, xa, xb):
    for s in solids(li):
        if s.kind in ('pill', 'long', 'pad') and s.x0 <= xb and s.x1 >= xa:
            s.x0 = min(s.x0, xa - 2); s.x1 = max(s.x1, xb + 2); return
    COURSE[li].append(Solid('pill', xa - 8, xb + 8, y=SURF[li]))
def clear(li, xa, xb, keep_before=None):
    for s in list(COURSE[li]):
        if s.kind in ('pill', 'long', 'pad') and s.x0 < xb and s.x1 > xa:
            if s.x0 < xa - 24: s.x1 = xa
            elif s.x1 > xb + 24: s.x0 = xb
            else: COURSE[li].remove(s)
# Rayleigh is knocked off the end of his pill at 5.62 and swims in open water
XK = xat('ray', 5.62)
for s in solids(2):
    if s.kind == 'pill' and s.x0 < XK < s.x1 + 40: s.x1 = XK + 3
clear(2, XK + 4, XK + 140)
# Cyrus panics on a pill (5.95 ->), and again on the hill (no patch needed)
XC = xat('cyrus', 5.95); ensure_on(0, XC - 16, XC + 16)
# Joy lies on lane 3's rope: make sure that rope runs under her
XJ = xat('joy', 13.98)
for li in (1, 2):
    ropes = [s for s in COURSE[li] if s.kind == 'rope' and s.x0 < XJ]
    rp = max(ropes, key=lambda s: s.x0); rp.x1 = max(rp.x1, XJ + 30)
    for s in list(COURSE[li]):
        if s is rp or s.kind not in ('pad', 'rope'): continue
        if s.x0 < rp.x1 and s.x1 > rp.x0:
            if s.x1 <= rp.x1 + 12: COURSE[li].remove(s)
            else: s.x0 = rp.x1
    nxt = [s for s in COURSE[li] if s.x0 >= rp.x1 and s.kind not in ('greens',)]
    if not nxt or min(q.x0 for q in nxt) > rp.x1 + 1: COURSE[li].append(Solid('pad', rp.x1, rp.x1 + 30, y=SURF[li]))
for li in range(NL):
    L = sorted([s for s in COURSE[li] if s.kind != 'greens'], key=lambda s: s.x0); out = []
    for s in L:
        if out and s.kind in ('pad',) and out[-1].kind == 'rope' and s.x0 < out[-1].x1: s.x0 = out[-1].x1
        if out and s.kind == 'rope' and out[-1].kind == 'pad' and s.x0 < out[-1].x1: s.x0 = out[-1].x1
        out.append(s)
    COURSE[li] = out + [Solid('greens', 0, 0, items=GREENS) for GREENS in [None]]
GREEN = {}
for li in range(NL):                                    # rebuild green lists after sorting
    bar = [s for s in COURSE[li] if s.kind == 'bar'][0]; gx = bar.x0 - 6; gl = []
    while gx < bar.x1 - 30: gl.append(Solid('green', gx, gx + 42, y=SURF[li])); gx += 42 + 34
    GREEN[li] = gl
    COURSE[li] = [s for s in COURSE[li] if s.kind != 'greens']
# Cleo drops off the bars into open water at 22.65 and climbs out onto a green pad at ~23.55
XCL = xat('cleo', 23.62)
GREEN[3] = [s for s in GREEN[3] if s.x1 < XCF - 50 or s.x0 > XCF + 110]
GREEN[3] += [Solid('green', XCF + 33, XCF + 110, y=SURF[3])]; GREEN[3].sort(key=lambda s: s.x0)   # Rayleigh's pad, just ahead of her splash
XRU = xat('ray', 23.95)                                  # Rayleigh hops back up into his lane here: a pad under him
GREEN[2] = [s for s in GREEN[2] if s.x1 < XRU - 26 or s.x0 > XRU + 40]
GREEN[2].append(Solid('green', XRU - 12, XRU + 30, y=SURF[2])); GREEN[2].sort(key=lambda s: s.x0)
gx = GREEN[3][-1].x1 + 30
BAR = {li: [s for s in COURSE[li] if s.kind == 'bar'][0] for li in range(NL)}
def surface(li, x, solid_list=None, t=None):
    best = None
    for s in (solid_list or COURSE[li]):
        if s.x0 <= x <= s.x1:
            y = s.top(x)
            if best is None or y < best[0]: best = (y, s)
    return best
# ------------------------------------------------------------------ states per runner (scripted beats)
T_GO = 2.36
TMAX = 0.42
EV = []                                              # sfx events
_s8 = SLIP[8]; _a8 = np.array(_s8)[..., 3] > 0; _top8 = np.where(_a8.any(1))[0][0]
TC = 22.65 + math.sqrt(2 * (WL[3] - (BARY[3] + 1 - _top8 + _s8.getbbox()[3])) / G)   # v4: the frame her boots reach the surface
TC = math.ceil(TC * FPS) / FPS
SPANS = {
 'ray':  [(5.62, 5.86, 'knock'), (5.86, 8.3, 'swim'), (22.95, 23.17, 'dropdown'), (23.17, 23.6, 'reach'), (23.6, 23.95, 'hopup'), (34.32, 99, 'win')],
 'cyrus':[(5.95, 9.6, 'panic'), (29.15, 99, 'panic')],
 'joy':  [(13.45, 13.72, 'wobble'), (13.72, 13.98, 'slipfall'), (13.98, 15.3, 'lie'), (15.3, 15.75, 'getup')],
 'cleo': [(21.6, 22.65, 'slip'), (22.65, TC, 'barfall'), (TC, 23.3, 'swim'), (23.3, 23.6, 'lift'), (23.6, 23.76, 'edge'), (23.76, 23.96, 'climbout'), (32.02, 32.22, 'rolloff'), (32.22, 99, 'tread')],
}
def span(g, t):
    for a, b, k in SPANS[g]:
        if a <= t < b: return a, b, k
    return None
# Joy's body as a bump on lane 3's rope while she lies there (Rayleigh steps up onto her, never through her)
def joy_bump(x, t):
    if not (13.98 <= t < 15.3): return 0.0
    u = (x - (XJ - 19)) / 38.0
    return 7.0 * math.sin(math.pi * u) if 0 < u < 1 else 0.0
# ------------------------------------------------------------------ per-frame pose solver (terrain driven)
def lane_list(li, g, t):
    L = list(COURSE[li])
    if (g == 'cleo' and 23.62 <= t < 30) or (g == 'ray' and 23.95 <= t < 30): L = [s for s in L if s.kind != 'bar'] + GREEN[li]
    return L
POSE = {g: [None] * NF for g in GS}
def solve(g):
    li = LANE[g]; xs = X[g]; dist = 0.0; air = None; land_t = -9
    for f in range(NF):
        t = f / FPS; x = xs[f]
        if f > 0: dist += abs(x - xs[f - 1])
        sp = span(g, t)
        if t < T_GO:
            POSE[g][f] = ('stand', x, SURF[li] if x > DOCK_X else SURF[li], 0); continue
        if sp:
            a, b, k = sp; u = (t - a) / (b - a) if b < 90 else t - a
            POSE[g][f] = (k, x, u, dist); air = None; continue
        L = lane_list(li, g, t)
        if air is not None:                               # continue a ballistic hop already planned
            t0, t1, y0, y1, tgt, xa, xb = air
            if t < t0:                                    # slow approach: plant at the edge until the hop
                POSE[g][f] = ('wait', xa, y0, dist, t0); continue
            if t < t1:
                u = (t - t0) / (t1 - t0); T = t1 - t0
                y = y0 + (y1 - y0) * u - 0.5 * G * T * T * u * (1 - u)
                POSE[g][f] = ('air', xa + (xb - xa) * u, y, u, tgt); continue
            air = None; land_t = t1
        hit = surface(li, x, L)
        if hit is None or hit[1].kind not in ('bar',) and False: pass
        if hit is not None:
            y, s = hit; y -= joy_bump(x, t) if (li == 2 and g == 'ray') else 0
            # look ahead: is there a gap right after this solid?  plan a hop that takes off near its end
            if x >= s.x1 - 3 or (s.kind != 'bar' and False):
                pass
            nxt = [q for q in L if q.x0 > s.x1 - 1 and q is not s]
            nx = min(nxt, key=lambda q: q.x0) if nxt else None
            gap = (nx.x0 - s.x1) if nx else 0
            take = s.x1 - (4 if s.kind != 'bar' else 2)
            if nx and gap > 3 and x >= take:
                land = nx.x0 + (7 if nx.kind != 'bar' else 4)
                fl = next((ff for ff in range(f, NF) if xs[ff] >= land), None)
                if fl is not None and fl > f:
                    y1 = nx.top(land); t0 = max(t, fl / FPS - TMAX); air = (t0, fl / FPS, y, y1, nx.kind, x, xs[fl])
                    POSE[g][f] = ('wait' if t0 > t else 'air', x, y, 0.0 if t0 <= t else dist, nx.kind if t0 <= t else t0); EV.append((t0, 'hop', g)); continue
            mode = {'bar': 'hang', 'rope': 'walk', 'hill': 'climb' if x <= getattr(s, 'xc', 1e9) else 'tumble'}.get(s.kind, 'run')
            if s.kind == 'bar' and ((g == 'cleo' and 23.62 <= t < 30) or (g == 'ray' and 23.95 <= t < 30)): mode = 'run'
            if g == 'ray' and t >= 30.7: mode = 'tumble'
            POSE[g][f] = (mode, x, y, dist, t - land_t); continue
        # nothing under the runner (should only happen inside scripted spans)
        POSE[g][f] = ('run', x, SURF[li], dist, 9)
for g in GS: solve(g)
# ------------------------------------------------------------------ slime path (hops; on heads)
def head_world(g, f):
    p = POSE[g][f]; fr, ox, oy = sprite_for(g, f)
    hx, hy = head(fr); return ox + hx, oy + hy
SL = {}
# ------------------------------------------------------------------ sprite selection
def place(fr, ax, ay, ref):                           # frame placed so its set anchor lands on (ax, ay)
    return fr, ax - ref[0], ay - ref[1]
def sprite_for(g, f):
    t = f / FPS; p = POSE[g][f]; k = p[0]; li = LANE[g]
    if k == 'stand': return place(RUN[g][0], p[1], p[2], REF[('run', g)])
    if k in ('run', 'walk', 'climb'):
        x, y, dist, since = p[1], p[2], p[3], p[4]
        if since < 0.1 and since >= 0:
            j = JLAND[g][0 if since < 0.05 else 1]; return place(JUMP[g][j], x, y, REF[('jump', g)])
        step = {'run': 6.5, 'walk': 6.0, 'climb': 9.0}[k]          # v2: slow, effortful climb cadence on the hill
        return place(RUN[g][1 + int(dist / step) % 8], x, y, REF[('run', g)])
    if k == 'hang':
        x, y, dist = p[1], p[2], p[3]
        return place(HANG[g][int(dist / 6.0) % len(HANG[g])], x, y, REF[('hang', g)])
    if k == 'wait':
        if p[4] - t < 0.1: return place(JUMP[g][3 if g == 'cyrus' else 4], p[1], p[2], REF[('jump', g)])
        return place(RUN[g][0], p[1], p[2], REF[('run', g)])
    if k == 'air':
        x, y, u, tgt = p[1], p[2], p[3], p[4]
        if tgt == 'bar' and u > 0.82: return place(HANG[g][0], x, y, REF[('hang', g)])
        a, b = JAIR[g]; j = a + min(b - a, int(u * (b - a + 1)))
        fr = JUMP[g][j]; bb = fr.getbbox(); return fr, x - (bb[0] + bb[2]) / 2, y - bb[3]
    if k == 'tumble':
        x, y, dist = p[1], p[2], p[3]
        fr = KO[g][3 + int(dist / 6.0) % 6]; bb = fr.getbbox(); r = (bb[3] - bb[1]) / 2
        return fr, x - (bb[0] + bb[2]) / 2, y + 1 - bb[3]          # v2: the rolling body rests on the slope (was sunk half its height)
    return special(g, f)
def special(g, f):
    t = f / FPS; p = POSE[g][f]; k, x, u = p[0], p[1], p[2]; li = LANE[g]
    if g == 'ray':
        if k == 'knock':                                # hit from above: recoil, pitch forward off the pill into the water
            T = 5.86 - 5.62; tt = u * T; y0 = SURF[2]; y = y0 + 0.5 * G * tt * tt * 0.9
            fr = KO[g][1] if tt < 0.06 else (KO[g][2] if tt < 0.13 else KO[g][3])
            y = min(y, WL[2] + 10)
            return place(fr, x, y, REF[('ko', g)])
        if k == 'swim':
            fr = SWIM[g][int((t - 5.86) * 10) % len(SWIM[g])]; bb = fr.getbbox()
            bob = 1.5 * math.sin(t * 7)
            return fr, x - (bb[0] + bb[2]) / 2, WL[2] + bob - SWROW['ray']
        if k == 'dropdown':                             # lets go of his bar and drops onto the pad beside Cleo's splash
            T = 23.17 - 22.95; y0 = BAR[2].y; y1 = SURF[3]
            y = y0 + (y1 - y0) * u - 0.5 * G * T * T * u * (1 - u) * 0.3
            if u < 0.12: return place(HANG[g][0], x, BAR[2].y, REF[('hang', g)])
            fr = JUMP[g][9 if u < 0.6 else 10]; bb = fr.getbbox(); return fr, x - (bb[0] + bb[2]) / 2, y - bb[3]
        if k == 'reach':                                # kneels at the edge, reaches down, hauls her up
            tt = t - 23.17
            j = 1 if tt < 0.06 else 2 if tt < 0.12 else (3 + min(3, int((tt - 0.12) / 0.06))) if tt < 0.32 else 7 if tt < 0.47 else 8
            return place(REACH[j], x, SURF[3], REF[('reach', g)])
        if k == 'hopup':                                # hops back up into his own lane
            T = 23.95 - 23.6; hit = surface(2, x, lane_list(2, 'ray', 24.0)); y1 = hit[0] if hit else SURF[2]
            xs_ = xat('ray', 23.6); x = xs_ + (xat('ray', 23.95) - xs_) * (1 - (1 - u) ** 2)   # pushes off up and away from her (ease-out)
            y = SURF[3] + (y1 - SURF[3]) * u - 0.5 * G * T * T * u * (1 - u)
            a, b = JAIR[g]; j = a + min(b - a, int(u * (b - a + 1)))
            fr = JUMP[g][j]; bb = fr.getbbox(); return fr, x - (bb[0] + bb[2]) / 2, y - bb[3]
        if k == 'win':
            fr = VIC[int((t - 34.32) * 8) % len(VIC)]; bb = fr.getbbox()
            return fr, x - (bb[0] + bb[2]) / 2, SURF[2] - bb[3]
    if g == 'cyrus' and k == 'panic':
        hit = surface(0, x); y = hit[0] if hit else SURF[0]
        a0 = 5.95 if t < 20 else 29.15
        fr = PANIC['cyrus'][1] if t - a0 < 0.1 else PANIC['cyrus'][2 + int(t * 10) % 7]; bb = fr.getbbox()
        sh = (1 if (f // 2) % 2 else -1)                     # small shake while he's stuck
        return fr, x - (bb[0] + bb[2]) / 2 + sh, y - bb[3]
    if g == 'joy':
        y2 = SURF[1]; rope3 = surface(2, x); y3 = rope3[0] if rope3 else SURF[2]
        if k == 'wobble':
            hit = surface(1, x); y = hit[0] if hit else y2
            fr = KO[g][min(2, int(u * 3))]                  # side-view stumble (no front-facing face: Joy's teeth never show)
            return place(fr, x, y, REF[('ko', g)])
        if k == 'slipfall':                              # slips off her rope and drops onto lane 3's rope (gravity)
            T = 13.98 - 13.72; tt = u * T; hit = surface(1, x); ys = hit[0] if hit else y2
            vy0 = (y3 - ys - 0.5 * G * T * T) / T; y = ys + vy0 * tt + 0.5 * G * tt * tt
            fr = KO[g][min(7, 3 + int(u * 5))]; bb = fr.getbbox()
            return fr, x - (bb[0] + bb[2]) / 2, y - bb[3]
        if k == 'lie':
            fr = KO[g][8]; bb = fr.getbbox()
            return fr, XJ - (bb[0] + bb[2]) / 2, y3 + 2 - bb[3]
        if k == 'getup':                                  # springs back up into her own lane
            T = 0.45; hit = surface(1, x); yl = hit[0] if hit else y2
            y = y3 + (yl - y3) * u - 0.5 * G * T * T * u * (1 - u)
            a, b = JAIR[g]; j = a + min(b - a, int(u * (b - a + 1)))
            fr = JUMP[g][j]; bb = fr.getbbox(); return fr, x - (bb[0] + bb[2]) / 2, y - bb[3]
    if g == 'cleo':
        bar = BAR[3]
        if k == 'slip':                                   # one hand slips off the bar: she dangles by the other
            tt = t - 21.6
            j = 1 if tt < 0.12 else (2 if tt < 0.24 else 3 + int((tt - 0.24) * 8) % 6)
            fr = SLIP[j]; a = np.array(fr)[..., 3] > 0; top = np.where(a.any(1))[0][0]; hx = np.where(a[top:top + 3].any(0))[0].mean()
            drop = 0 if tt < 0.1 else 2
            return fr, x - hx, BARY[3] - 1 + drop - top
        if k == 'barfall':                                # lets go of the bar: free fall into open water
            T = 22.88 - 22.65; tt = u * T
            fr = SLIP[8]; a = np.array(fr)[..., 3] > 0; top = np.where(a.any(1))[0][0]; hx = np.where(a[top:top + 3].any(0))[0].mean()
            T = TC - 22.65; tt = u * T
            y = BARY[3] + 1 - top + 0.5 * G * tt * tt                     # straight free fall until her boots reach the surface (TC)
            bb = fr.getbbox(); return fr, x - (bb[0] + bb[2]) / 2, y
        if k == 'swim':
            fr = SWIM[g][int((t - TC) * 10) % len(SWIM[g])]; bb = fr.getbbox(); bob = 1.5 * math.sin(t * 7)
            sink = 6 * math.exp(-(t - TC) * 8)                                # plunges in at the splash, settles to the swim line
            return fr, x - (bb[0] + bb[2]) / 2, WL[3] + bob + sink - SWROW['cleo']
        if k == 'lift':                                   # grabs Rayleigh's hand; hangs from it (body under water) as he hauls her up
            hx_, hy_ = cleo_hand(t)
            fr = HANG[g][0 if int((t - 23.3) * 7) % 2 == 0 else 1]; a = np.array(fr)[..., 3] > 0; top = np.where(a.any(1))[0][0]
            fx_ = np.where(a[top:top + 3].any(0))[0].mean()
            return fr, hx_ - fx_, hy_ - top
        if k == 'edge':                                   # he lets go and hops away; she hangs on the pad edge, kicking
            hx_, hy_ = cleo_hand(23.6)
            fr = HANG[g][0 if int((t - 23.3) * 7) % 2 == 0 else 1]; a = np.array(fr)[..., 3] > 0; top = np.where(a.any(1))[0][0]
            fx_ = np.where(a[top:top + 3].any(0))[0].mean()
            return fr, hx_ - fx_, hy_ - top
        if k == 'climbout':                               # pulls herself out onto the pad, clear of him
            hx_, hy_ = cleo_hand(23.6); fr0 = HANG[g][0]; a0 = np.array(fr0)[..., 3] > 0; top0 = np.where(a0.any(1))[0][0]
            fx0 = np.where(a0[top0:top0 + 3].any(0))[0].mean(); b0 = fr0.getbbox()
            feet0 = hy_ - top0 + b0[3]; cx0 = hx_ - fx0 + (b0[0] + b0[2]) / 2
            x1 = XCF + 64; T = 0.2; y = feet0 + (SURF[3] - feet0) * u - 0.5 * G * T * T * u * (1 - u)
            xx = cx0 + (x1 - cx0) * (1 - (1 - u) ** 2)                    # most of the sideways move happens early, over the pad
            a, b = JAIR[g]; j = a + min(b - a, int(u * (b - a + 1)))
            fr = JUMP[g][j]; bb = fr.getbbox(); return fr, xx - (bb[0] + bb[2]) / 2, y - bb[3]
        if k == 'rolloff':                                # rolls off the end of her hill into the water
            T = 0.2; tt = u * T; y0 = SURF[3] - 2; y = y0 + 0.5 * G * tt * tt
            fr = KO[g][3 + int((t - 30.7) * 14) % 6]; bb = fr.getbbox()
            return fr, x - (bb[0] + bb[2]) / 2, min(y, WL[3] + 8) - bb[3]
        if k == 'tread':                                   # pops back up and treads water
            fr = SWIM[g][int((t - 32.2) * 8) % len(SWIM[g])]; bb = fr.getbbox()
            sink = 10 * math.exp(-(t - 32.22) * 5); bob = 1.5 * math.sin(t * 6)
            return fr, x - (bb[0] + bb[2]) / 2, WL[3] + sink + bob - SWROW['cleo']
    fr = RUN[g][0]; return place(fr, x, SURF[li], REF[('run', g)])

def bob_c(t): return 1.5 * math.sin(t * 7)
_RH = {}
for _j, _fr in enumerate(REACH):
    _a = np.array(_fr)[..., 3] > 0; _xs = np.where(_a.any(0))[0]; _xl = _xs.min(); _ys = np.where(_a[:, _xl:_xl + 3].any(1))[0]
    _RH[_j] = (_xl + 1 - REF[('reach', 'ray')][0], _ys.max() - REF[('reach', 'ray')][1])   # hand offset from his anchor (native)
def ray_reach_j(t):
    tt = t - 23.17
    return 1 if tt < 0.06 else 2 if tt < 0.12 else (3 + min(3, int((tt - 0.12) / 0.06))) if tt < 0.32 else 7 if tt < 0.47 else 8
def cleo_hand(t):
    """Cleo's hands at the pad edge in Rayleigh's reaching hand: held at the surface while he braces (23.3-23.42),
    then hauled up with his rising frames (23.42-23.58, eased), feet still under water when he lets go"""
    u = min(1.0, max(0.0, (t - 23.42) / 0.16)); e = u * u * (3 - 2 * u)
    return XCF + 31, SURF[3] + 3 - 21 * e
# Cleo's pad hops under the bars: own terrain pass over the green pads
PADP = {}
def build_pads():
    g = 'cleo'; li = 3; L = [s for s in COURSE[3] if s.kind != 'bar'] + GREEN[3]; L.sort(key=lambda s: s.x0)
    air = None; dist = 0
    for f in range(int(23.62 * FPS), int(30 * FPS)):
        t = f / FPS; x = X[g][f]; dist += X[g][f] - X[g][f - 1]
        if air:
            t0, t1, y0, y1 = air
            if t < t1:
                u = (t - t0) / (t1 - t0); T = t1 - t0; PADP[f] = ('air', x, y0 + (y1 - y0) * u - 0.5 * G * T * T * u * (1 - u), u, 'pad'); continue
            air = None
        hit = surface(li, x, L)
        if hit:
            y, s = hit; nxt = [q for q in L if q.x0 > s.x1 - 1]; nx = min(nxt, key=lambda q: q.x0) if nxt else None
            if nx and nx.x0 - s.x1 > 3 and x >= s.x1 - 4:
                land = nx.x0 + 7; fl = next((ff for ff in range(f, NF) if X[g][ff] >= land), None)
                if fl and fl > f: air = (t, fl / FPS, y, nx.top(land)); PADP[f] = ('air', x, y, 0.0, 'pad'); continue
            PADP[f] = ('run', x, y, dist, 9)
        else: PADP[f] = ('run', x, SURF[3], dist, 9)
def pads_pose(f):
    p = PADP.get(f); g = 'cleo'
    if p[0] == 'air':
        a, b = JAIR[g]; j = a + min(b - a, int(p[3] * (b - a + 1))); fr = JUMP[g][j]; bb = fr.getbbox(); return fr, p[1] - (bb[0] + bb[2]) / 2, p[2] - bb[3]
    return place(RUN[g][1 + int(p[3] / 8.0) % 8], p[1], p[2], REF[('run', g)])
# ------------------------------------------------------------------ slime path (world, native): hops on platforms, lands on heads
def ballistic(p0, p1, T, tt):
    u = tt / T; return p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - 0.5 * G * T * T * u * (1 - u)
def headpt(g, t):
    f = min(NF - 1, int(round(t * FPS))); fr, ox, oy = sprite_for(g, f); hx, hy = head(fr); return ox + hx, oy + hy + 3
def slime_plan():
    segs = []                                          # (t0, t1, kind, data)
    # act 1: hops in from the left along lane 3 (pill to pill) and lands on Rayleigh's head at 4.75
    pills = [s for s in COURSE[2] if s.kind == 'pill']
    tA, tB = 2.75, 4.75
    xstart = cam0(tA) - 30
    pts = [(xstart, SURF[2] - 20)]
    cands = [s for s in pills if xstart + 40 < (s.x0 + s.x1) / 2 < headpt('ray', tB)[0] - 30]
    for s in cands: pts.append(((s.x0 + s.x1) / 2, SURF[2]))
    pts.append(headpt('ray', tB))
    n = len(pts) - 1; dts = [max(0.25, abs(pts[i + 1][0] - pts[i][0])) for i in range(n)]; tot = sum(dts)
    tc = tA
    for i in range(n):
        d = (tB - tA) * dts[i] / tot; segs.append((tc, tc + d, 'hop', (pts[i], pts[i + 1]))); tc += d
    # act 2: bounces on his head twice, the third landing knocks him off (5.62)
    for a, b in [(4.75, 5.18), (5.18, 5.62)]: segs.append((a, b, 'headhop', ('ray', 9)))
    # act 3: rebounds off him and arcs up onto Cyrus's head (6.2), rides it
    segs.append((5.62, 6.2, 'fly', (headpt('ray', 5.62), headpt('cyrus', 6.2))))
    segs.append((6.2, 10.0, 'ride', 'cyrus'))
    # act 4: back at 27.8 from the left, hops along lane 1 and lands on Cyrus's head on the hill (29.3)
    tC, tD = 27.75, 29.3
    p0 = (cam0(tC) - 30, SURF[0] - 10); p3 = headpt('cyrus', tD)
    mids = [(p0[0] + (p3[0] - p0[0]) * k / 3, None) for k in (1, 2)]
    pts = [p0] + [(mx, (surface(0, mx)[0] if surface(0, mx) else SURF[0])) for mx, _ in mids] + [p3]
    tc = tC
    for i in range(3):
        d = (tD - tC) / 3; segs.append((tc, tc + d, 'hop', (pts[i], pts[i + 1]))); tc += d
    segs.append((tD, 99, 'ride', 'cyrus'))
    return segs
SLSEG = slime_plan()
for a, b, k, d in SLSEG:
    if k in ('hop', 'fly'): EV.append((b, 'slime_land' if k == 'hop' else 'slime_head', 'slime'))
def slime_at(t):
    for a, b, k, d in SLSEG:
        if a <= t < b:
            if k == 'hop':
                x, y = ballistic(d[0], d[1], b - a, t - a); land = (b - t) < 0.07 or (t - a) < 0.05
                return x, y, 'air' if not land else 'squash'
            if k == 'headhop':
                hx, hy = headpt(d[0], t); u = (t - a) / (b - a); return hx, hy - 4 * d[1] * u * (1 - u), 'air' if 0.1 < u < 0.9 else 'squash'
            if k == 'fly':
                x, y = ballistic(d[0], d[1], b - a, t - a); return x, y, 'air'
            if k == 'ride':
                hx, hy = headpt(d, t); return hx, hy, 'ride'
    return None
# ------------------------------------------------------------------ drawing helpers (native)
C_BG = (236, 233, 247); C_BG2 = (228, 224, 243)
C_W1 = (122, 178, 245); C_W2 = (104, 160, 236); C_WL = (214, 236, 255)
C_RED = (214, 64, 64); C_RED2 = (150, 36, 44)
OUT = (88, 52, 30)
def outline_rect(d, x0, y0, x1, y1, fill, hi, sh, ol=OUT):
    d.rectangle([x0, y0, x1, y1], fill=ol)
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=fill)
    d.line([x0 + 2, y0 + 1, x1 - 2, y0 + 1], fill=hi); d.line([x0 + 1, y1 - 1, x1 - 1, y1 - 1], fill=sh)
def pill(d, x0, y0, x1, y1, fill, hi, sh):
    r = min(5, (y1 - y0) // 2)
    d.rounded_rectangle([x0, y0, x1, y1], r, fill=OUT)
    d.rounded_rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], max(1, r - 1), fill=fill)
    d.line([x0 + r, y0 + 2, x1 - r, y0 + 2], fill=hi); d.line([x0 + r, y1 - 2, x1 - r, y1 - 2], fill=sh)
YEL = ((255, 214, 92), (255, 240, 170), (226, 170, 56)); ORA = ((250, 168, 84), (255, 206, 140), (214, 120, 52))
GRN = ((176, 232, 98), (220, 252, 160), (122, 186, 66)); ORP = ((240, 134, 84), (255, 182, 130), (196, 92, 56))
def _paste(img, im, x, y): img.alpha_composite(im, (int(round(x)), int(round(y))))
def _water_shadow(d, x0, x1, y):
    if x1 - x0 < 10: return
    w = x1 - x0 + 6                                          # blended (not a hole in the water)
    ENV.blend(d._image, x0 - 3, y, w, 5, lambda dd: (dd.rectangle([4, 0, w - 4, 2], fill=(8, 30, 60, 70)), dd.line([1, 3, w - 1, 3], fill=(170, 220, 245, 90))))
def draw_solid(img, d, s, cam, li, t):
    x0, x1 = s.x0 - cam, s.x1 - cam
    if x1 < -8 or x0 > NW + 8: return
    y = int(s.y) if hasattr(s, 'y') else 0
    if s.kind in ('pill', 'long'):                          # wooden dock rafts
        im = ENV.sliced(ENV.DOCK, 10, x1 - x0); _paste(img, im, x0, y - 2); _water_shadow(d, x0, x1, y - 2 + im.height)
    elif s.kind == 'pad':                                   # mossy stone blocks
        im = ENV.sliced(ENV.STONE, 9, x1 - x0); _paste(img, im, x0, y - 5); _water_shadow(d, x0, x1, y - 5 + im.height)
    elif s.kind == 'green':                                 # log rafts
        im = ENV.sliced(ENV.LOG, 14, x1 - x0); _paste(img, im, x0, y - 4); _water_shadow(d, x0, x1, y - 4 + im.height)
    elif s.kind == 'dome':                                  # river boulders
        _paste(img, ENV.ROCK, x0, y - 1 - ENV.ROCK_TOP.min()); _water_shadow(d, x0 + 2, x1 - 2, y - 1 - ENV.ROCK_TOP.min() + ENV.ROCK.height - 1)
    elif s.kind == 'pillar':                                # tree-stump posts
        im = ENV.POST; cut = min(im.height, int(SURF[li] + 12 - (y - 1)))
        _paste(img, im.crop((0, 0, im.width, cut)), (x0 + x1) / 2 - im.width / 2, y - 1)
        _water_shadow(d, x0 + 3, x1 - 3, y - 1 + cut - 2)
    elif s.kind == 'rope':
        pts = [(int(xx - cam), int(s.top(xx) + 1)) for xx in np.arange(s.x0, s.x1 + 1, 2)]
        ENV.rope(d, pts)
def draw_hill(img, d, s, cam, li):
    if s.x1 - cam < -5 or s.x0 - cam > NW + 5: return img
    base = SURF[li] + 10
    img = ENV.hill_fill(img, s, cam, li, base, NW); d = ImageDraw.Draw(img)
    rs = random.Random(li * 7 + 3)
    for hx in range(int(s.x0), int(s.xc), 17):                     # climbing holds on the way up
        sx = hx - cam
        if 0 <= sx < NW:
            yy = s.top(hx) + 6 + rs.randint(0, 8)
            if yy < base - 3:
                c = rs.choice([(232, 96, 96), (96, 160, 232), (240, 160, 64)])
                d.rectangle([sx - 2, yy - 1, sx + 2, yy + 1], fill=(40, 24, 16)); d.rectangle([sx - 1, yy, sx + 1, yy], fill=c)
    _water_shadow(d, max(0, s.x0 - cam), min(NW, s.x1 - cam), base)
    return img
def draw_bar(d, bar, cam, li, t):
    x0, x1 = bar.x0 - cam, bar.x1 - cam; by = BARY[li]
    if x1 < -5 or x0 > NW + 5: return
    for px in (x0 - 2, x1 + 2): ENV.pole(d, px, by - 3, SURF[li] + 4)
    ENV.bar(d, x0 - 2, x1 + 2, by)
    for rx in np.arange(bar.x0 + 8, bar.x1 - 4, 18):
        sx = int(rx - cam)
        if -4 <= sx <= NW + 4: ENV.ring(d, sx, by + 1)
def draw_water(img, cam, t):
    a = np.array(img)
    for li in range(NL): ENV.water(a, 0, LT[li], NW, LH, cam, t, seed=li)
    img = Image.fromarray(a); d = ImageDraw.Draw(img)
    for li in range(1, NL): ENV.buoys(d, LT[li], cam, t, NW)
    return img
# ------------------------------------------------------------------ effects
FX = []                                              # (t0, kind, x, y)
def add_splash(t, x, y, big=True): FX.append((t, 'splash' if big else 'splash_s', x, y))
def draw_fx(d, cam, t):
    for t0, kind, x, y in FX:
        u = t - t0
        if kind.startswith('splash') and 0 <= u < 0.7:
            n = 12 if kind == 'splash' else 7; rs = random.Random(int(t0 * 100))
            for i in range(n):
                vx = rs.uniform(-55, 55); vy = rs.uniform(-150, -80)
                px = x + vx * u - cam; py = y + vy * u + 0.5 * G * 0.45 * u * u
                if py < y + 2: d.rectangle([int(px), int(py), int(px) + 1, int(py) + 1], fill=(240, 250, 255) if i % 3 else (170, 214, 255))
            r = int(4 + 26 * u); a = y + 1
            d.arc([int(x - cam - r), int(a - r / 4), int(x - cam + r), int(a + r / 4)], 0, 360, fill=(235, 246, 255))
        if kind == 'puff' and 0 <= u < 0.35:
            for i in range(5):
                ang = i * 1.25; px = x - cam + math.cos(ang) * 14 * u / 0.35; py = y - 2 - abs(math.sin(ang)) * 8 * u / 0.35
                d.rectangle([int(px), int(py), int(px) + 1, int(py) + 1], fill=(250, 246, 230))
# scripted fx
add_splash(5.84, XK + 6, WL[2]); add_splash(TC, XCF, WL[3]); add_splash(23.77, cleo_hand(23.6)[0] + 4, WL[3], False)
add_splash(32.2, xat('cleo', 32.2), WL[3])
# ------------------------------------------------------------------ text (full res)
def ctext(d, x, y, t, f, fill, sw=8, sf=(20, 15, 35)):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=sf)
def strip(img, lines, cols, px, a=1.0):
    HY0 = 250; gap = 18; y1 = HY0 + 36 + len(lines) * px + (len(lines) - 1) * gap
    L_ = Image.new('RGBA', img.size, (0, 0, 0, 0)); D_ = ImageDraw.Draw(L_); D_.rectangle([0, HY0, W, y1], fill=(10, 8, 20, int(170 * a)))
    y = HY0 + 18
    for l, c in zip(lines, cols):
        w = D_.textlength(l, font=F(px)); D_.text((W / 2 - w / 2, y), l, font=F(px), fill=c + (int(255 * a),), stroke_width=7, stroke_fill=(20, 15, 35, int(255 * a))); y += px + gap
    img.alpha_composite(L_)
T_CD = [(0.1, 0.6, '3'), (0.7, 1.25, '2'), (1.4, 1.75, '1'), (1.9, 2.35, 'GO!')]
T_WIN = 34.1
# ------------------------------------------------------------------ render
def render(f):
    t = f / FPS; cam = CAMF[f]
    img = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))
    img = draw_water(img, cam, t); d = ImageDraw.Draw(img)
    # start pier (wooden deck in every lane)
    dx = DOCK_X - cam
    if dx > 2:
        for li in range(NL):
            ENV.deck(img, 0, dx, LT[li] + 3, LT[li] + LH - 1)
            d.line([0, SURF[li] + 8, dx, SURF[li] + 8], fill=(70, 44, 26)); d.line([0, SURF[li] + 9, dx, SURF[li] + 9], fill=(70, 44, 26))
        d.rectangle([dx - 1, BT, dx + 1, BB - 1], fill=(245, 245, 240))
    # finish line
    fx = FIN_X - cam
    sprites = {li: [] for li in range(NL)}; top = []
    for g in GS:
        fr, ox, oy = sprite_for(g, f); p = POSE[g][f]
        li = LANE[g]
        if g == 'joy' and p[0] in ('slipfall',): li = 2 if p[2] > 0.5 else 1
        if g == 'joy' and p[0] == 'lie': li = 2
        if g == 'joy' and p[0] == 'getup': li = 2 if p[2] < 0.5 else 1
        if g == 'ray' and (p[0] == 'reach' or (p[0] == 'dropdown' and p[2] > 0.5) or (p[0] == 'hopup' and p[2] < 0.5)): li = 3
        sprites[li].append((fr, ox - cam, oy, g, p[0]))
    for li in range(NL):
        for s in COURSE[li]:
            if s.kind == 'hill': img = draw_hill(img, d, s, cam, li); d = ImageDraw.Draw(img)
            elif s.kind != 'bar': draw_solid(img, d, s, cam, li, t)
        for s in GREEN[li]: draw_solid(img, d, s, cam, li, t)
        draw_bar(d, BAR[li], cam, li, t)
        if fx < NW:                                               # finish lawn + checkered line
            img = ENV.lawn(img, max(fx, 0), NW, LT[li] + 3, SURF[li] + 4, LT[li] + LH - 1, cam); d = ImageDraw.Draw(img)
            for yy in range(LT[li] + 2, LT[li] + LH - 1, 3):
                for kk in range(2):
                    d.rectangle([fx - 6 + kk * 3, yy, fx - 4 + kk * 3, yy + 2], fill=(240, 240, 236) if (yy // 3 + kk) % 2 else (30, 30, 34))
        for fr, x, y, g, k in sprites[li]:
            if k not in ('swim', 'tread', 'barfall', 'knock', 'rolloff', 'lift', 'edge', 'climbout', 'air', 'slipfall', 'getup', 'dropdown', 'hopup', 'waterjump'):
                bb = fr.getbbox(); cx = x + (bb[0] + bb[2]) / 2; bot = y + bb[3]
                hit = surface(li, cx + cam)
                if hit and abs(hit[0] - bot) < 6: ENV.shadow(d, cx, hit[0] + 1, max(12, (bb[2] - bb[0]) * 0.7), 70)
            elif k in ('air', 'hopup', 'getup', 'dropdown'):
                bb = fr.getbbox(); cx = x + (bb[0] + bb[2]) / 2; bot = y + bb[3]
                hit = surface(li, cx + cam)
                if hit and 0 <= hit[0] - bot < 50: ENV.shadow(d, cx, hit[0] + 1, max(8, 16 - (hit[0] - bot) / 5), int(70 - (hit[0] - bot)))
        for fr, x, y, g, k in sprites[li]:
            if k in ('swim', 'tread', 'barfall', 'knock', 'rolloff', 'lift', 'edge', 'climbout'):
                lay = Image.new('RGBA', img.size, (0, 0, 0, 0)); lay.alpha_composite(fr, (int(round(x)), int(round(y))))
                wl = WL[li] + (1 if k in ('swim', 'tread') else 0)
                a = np.array(lay); cut = a[wl + 1:, :, 3]
                a[wl + 1:, :, 3] = (cut.astype(int) * 70 // 255).astype(np.uint8)     # under the surface: mostly hidden
                img.alpha_composite(Image.fromarray(a)); d = ImageDraw.Draw(img)
                if k in ('swim', 'tread'):
                    bb = fr.getbbox(); cx = x + (bb[0] + bb[2]) / 2
                    d.line([int(cx - 14), wl + 1, int(cx + 14), wl + 1], fill=(235, 246, 255))
            else:
                img.alpha_composite(fr, (int(round(x)), int(round(y))))
            if g == 'cyrus':
                sl = slime_at(t)
                if sl and sl[2] == 'ride': top_slime(img, sl, cam, t)
    d = ImageDraw.Draw(img)
    sl = slime_at(t)
    if sl and sl[2] != 'ride': top_slime(img, sl, cam, t)
    fxl = Image.new('RGBA', (NW, NH), (0, 0, 0, 0)); draw_fx(ImageDraw.Draw(fxl), cam, t)
    fxl.paste((0, 0, 0, 0), (0, BB + 2, NW, NH)); img.alpha_composite(fxl)       # splashes never spill into the caption zone
    if fx < NW + 70:                                              # finish arch over the line (stands on the top ledge)
        img.alpha_composite(ENV.ARCH, (int(fx - 3 - ENV.ARCH.width / 2), int(BT + 2 - ENV.ARCH.height)))
    a_ = np.array(img); a_[BB + 3:] = 0; img = Image.fromarray(a_)                    # anything below the band goes behind its bottom edge
    d = ImageDraw.Draw(img); ENV.ledge(d, BT - 4, BT, NW, cam); ENV.ledge(d, BB - 1, BB + 2, NW, cam)
    over = Image.new('RGBA', (NW, NH), (0, 0, 0, 0))            # top-lane sprites + slime, re-laid over the hook strip's lower edge
    for fr, x, y, g, k in sprites[0]: over.alpha_composite(fr, (int(round(x)), int(round(y))))
    if sl: top_slime(over, sl, cam, t)
    over = over.crop((0, 98, NW, BT)).resize((W, (BT - 98) * K), Image.NEAREST)
    # ---- upscale + text
    big = ENV.backdrop(t, cam, BT - 4, BB + 3, K).convert('RGBA'); big.alpha_composite(img.resize((W, H), Image.NEAREST)); D = ImageDraw.Draw(big)
    if t < 5.7:                                                   # v3: hook leaves before the slime lands on Cyrus's head (5.9)
        strip(big, HOOK, HOOK_COL, 52, 1.0 if t < 5.4 else (5.7 - t) / 0.3); big.alpha_composite(over, (0, 98 * K))
    for a, b, txt in T_CD:
        if a <= t < b:
            u = (t - a); sc = 1.0 + 0.35 * max(0, 1 - u / 0.12)
            fs = int((190 if txt != 'GO!' else 150) * sc); ctext(D, 560, 870 - fs // 2, txt, F(fs), (232, 52, 52), 12, (255, 255, 255))
    if t >= T_WIN:
        u = t - T_WIN; sc = min(1.0, 0.4 + u / 0.12) if u < 0.12 else 1.0 + 0.06 * max(0, 1 - (u - 0.12) / 0.15)
        fs = int(96 * sc); ctext(D, 418, 570 - fs // 2, WIN_TXT, F(fs), (255, 214, 40), 10, (40, 24, 10))
        if u < 0.9:
            rs = random.Random(5)
            for i in range(26):
                vx = rs.uniform(-520, 520); vy = rs.uniform(-700, -150); c = rs.choice([(120, 230, 210), (255, 120, 150), (255, 220, 80), (150, 180, 255)])
                px = 418 + vx * u; py = 570 + vy * u + 900 * u * u
                D.rectangle([px, py, px + 11, py + 11], fill=c)
    return big
def top_slime(img, sl, cam, t):
    x, y, k = sl
    fr = SLIME[int(t * 10) % len(SLIME)]
    if k == 'air': fr = SLIME[2]
    if k == 'squash': fr = SLIME[5]
    bb = fr.getbbox(); img.alpha_composite(fr, (int(round(x - cam - (bb[0] + bb[2]) / 2)), int(round(y - bb[3]))))
def write_events():
    ev = [(0.1, 'tick_8bit'), (0.7, 'tick_8bit'), (1.4, 'tick_8bit'), (1.9, 'go_8bit')]
    for a, b, k, d in SLSEG:
        if k == 'hop': ev.append((b - 0.02, 'jump'))
    ev += [(4.75, 'squish'), (5.18, 'boing'), (5.62, 'punch'), (5.63, 'boing'), (5.84, 'splash_big_r01'), (6.2, 'squish'),
           (13.45, 'slip_r01'), (13.98, 'stomp_8bit'), (15.3, 'boing'),
           (21.62, 'slip_r01'), (22.65, 'swish'), (TC, 'splash_small_r01'), (22.95, 'jump'), (23.3, 'squish'), (23.4, 'boing'), (23.6, 'whoosh_8bit'), (23.62, 'jump'), (23.76, 'jump'), (23.96, 'stomp_8bit'),
           (29.3, 'squish'), (29.32, 'boing'), (30.72, 'whoosh_8bit'), (32.2, 'splash_big_r01'),
           (33.85, 'ding_8bit'), (34.1, 'win_sting'), (34.32, 'victory'), (34.36, 'cheer')]
    tstep = next((f / FPS for f in range(int(14.0 * FPS), int(15.2 * FPS)) if X['ray'][f] >= XJ - 6), None)
    if tstep: ev.append((round(tstep, 2), 'squish'))
    ev = sorted([(round(a, 3), b) for a, b in ev if 0 <= a < END - 0.1])
    json.dump({'events': ev, 'end': END, 'fin_x': FIN_X}, open(OUTD + '/r01_events.json', 'w'), indent=1)
if __name__ == '__main__':
    STILLS = [float(v) for v in os.environ.get('STILLS', '').split(',') if v]
    if STILLS:
        for s in STILLS: render(int(round(s * FPS))).convert('RGB').save(OUTD + f'/st_{s:.2f}.png')
        sys.exit()
    out = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + '/r01_noaudio_tmp.mp4'], stdin=subprocess.PIPE)
    for f in range(NF): out.stdin.write(render(f).convert('RGB').tobytes())
    out.stdin.close(); out.wait(); os.replace(OUTD + '/r01_noaudio_tmp.mp4', OUTD + '/r01_noaudio.mp4')
    print('done', NF)
    write_events()
