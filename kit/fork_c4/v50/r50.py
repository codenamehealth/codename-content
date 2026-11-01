import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE + '/../../fork1'); sys.path.insert(0, HERE + '/../../pixellab/safezone')
from common import *
from hook import hook_layer
import numpy as np
from PIL import ImageFilter
os.chdir(HERE)
B5 = SP + 'fork_b5/'
# ---------------------------------------------------------------- layout (world = tall static map, camera scrolls up)
HK1, HB1 = hook_layer(['CHOOSE YOUR', 'PATH'], accent=1, sub='A, B OR C?')
HK2, HB2 = hook_layer(['WHAT DID', 'YOU GET?'], accent=1, sub='COMMENT YOUR PRIZE')
print('hook bottoms', HB1, HB2)
LS = 4
Y_L = 520                    # world y of the prize ledge top (paths end here)
Y_S = 3200                   # world y of the start orbs (paths start here)
WH = Y_S + 720               # world height (start dais runs off the bottom of the screen)
SX = [170, 370, 570]         # start orbs A, B, C
TX = [230, 480, 730]         # prize pedestals (dragon, crown, gummy)
PERM = [2, 0, 1]             # A->gummy, B->dragon, C->crown (same mapping as before, never shown)
COL = [(255, 206, 70), (80, 220, 255), (255, 100, 210)]
DARK = [(96, 60, 8), (8, 60, 100), (100, 16, 72)]
LBL = ['A', 'B', 'C']
XMIN, XMAX = 112, 848
N = 900
US = np.linspace(0, 1, N)
YS = Y_S + (Y_L - Y_S) * US
def make_path(i, prm):
    s, e = SX[i], TX[PERM[i]]
    x = s + (e - s) * (3 * US ** 2 - 2 * US ** 3)
    env = np.sin(np.pi * US) ** 0.55 * np.clip(np.minimum(US, 1 - US) / 0.05, 0, 1) ** 1.5   # paths leave the orbs / enter the sockets straight
    for a, f, ph in prm: x = x + a * env * np.sin(2 * np.pi * f * US + ph)
    c, hw = (XMIN + XMAX) / 2, (XMAX - XMIN) / 2
    return c + hw * np.tanh((x - c) / hw)
def evaluate(P):
    dy = (Y_L - Y_S) / (N - 1)
    cross = []; ok = True; minang = 9
    for i in range(3):
        for j in range(i + 1, 3):
            d = P[i] - P[j]; sl = np.gradient(d) / abs(dy)
            near = np.abs(d) < 80
            if (near & (np.abs(sl) < 0.55) & (US > 0.04) & (US < 0.96)).any(): return None
            k = np.where(np.sign(d[1:]) != np.sign(d[:-1]))[0]
            for kk in k:
                cross.append((YS[kk], i, j)); minang = min(minang, abs(sl[kk]))
    if not (10 <= len(cross) <= 14): return None
    ys = sorted(c[0] for c in cross)
    gaps = np.diff(ys)
    if len(gaps) and gaps.min() < 110: return None
    if ys[0] > Y_S - 260 or ys[-1] < Y_L + 260: return None      # crossings start early and run to the top
    return minang + gaps.min() / 400, cross
rng = np.random.RandomState(50); best = None
for trial in range(25000):
    prm = [[(rng.uniform(120, 300), rng.uniform(1.2, 3.6), rng.uniform(0, 6.3)) for _ in range(2)] for _ in range(3)]
    P = [make_path(i, prm[i]) for i in range(3)]
    r = evaluate(P)
    if r and (best is None or r[0] > best[0]): best = (r[0], P, r[1], prm)
assert best, 'no path set found'
_, PATHS, CROSS, PRM = best
print('crossings', len(CROSS), 'score', round(best[0], 2))
json.dump({'prm': PRM, 'cross': [(round(float(y)), i, j) for y, i, j in CROSS]}, open('paths.json', 'w'))
# ---------------------------------------------------------------- static path art (low-res grid, chunky pixels)
LW, LH = W // LS, WH // LS
def pts(i, a=0, b=N): return [(PATHS[i][k] / LS, YS[k] / LS) for k in range(a, b)]
def stroke(d, P, i):
    d.line(P, fill=(18, 10, 30, 255), width=11, joint='curve')
    d.line(P, fill=DARK[i] + (255,), width=8, joint='curve')
    d.line(P, fill=COL[i] + (255,), width=5, joint='curve')
    d.line([(x - 1, y) for x, y in P], fill=tuple(min(255, c + 90) for c in COL[i]) + (255,), width=1)
PL_ = Image.new('RGBA', (LW, LH), (0, 0, 0, 0)); d = ImageDraw.Draw(PL_)
for i in range(3): stroke(d, pts(i), i)
# weave: alternate which path is on top at successive crossings so each line can be followed through
over = {}
for n_, (yc, i, j) in enumerate(sorted(CROSS)):
    top = i if n_ % 2 == 0 else j
    if top == j: continue                                           # j is drawn after i already
    k = int(np.argmin(np.abs(YS - yc))); a, b = max(0, k - 22), min(N, k + 22)
    stroke(d, pts(top, a, b), top)
# rune marks along each path (static), drawn after the weave so they sit on the visible stroke
RUNES = []
for i in range(3):
    seg = np.hypot(np.diff(PATHS[i]), np.diff(YS)); arc = np.concatenate([[0], np.cumsum(seg)])
    for s_ in np.arange(90, arc[-1] - 60, 120):
        k = int(np.searchsorted(arc, s_)); RUNES.append((PATHS[i][k], YS[k], i))
PATH_IMG = up(PL_, LS)
GLOW = up(PL_.filter(ImageFilter.GaussianBlur(5)), LS); GLOW.putalpha(GLOW.getchannel('A').point(lambda v: int(v * 0.75)))
# ---------------------------------------------------------------- stone start dais + prize ledge (world layer, static)
def stone_block(w, h, k=4):
    L = Image.new('RGBA', (w // k, h // k), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
    dd.rectangle([0, 0, w // k - 1, h // k - 1], fill=(40, 34, 60, 255))
    dd.rectangle([1, 1, w // k - 2, h // k - 1], fill=(92, 96, 132, 255))
    dd.rectangle([1, 1, w // k - 2, 2], fill=(150, 160, 200, 255)); dd.line([(1, 3), (w // k - 2, 3)], fill=(60, 60, 92, 255))
    for r, yy in enumerate(range(9, h // k, 7)):
        dd.line([(1, yy), (w // k - 2, yy)], fill=(70, 72, 104, 255))
        for xx in range(4 + (6 if r % 2 else 0), w // k - 2, 12): dd.line([(xx, yy - 6), (xx, yy - 1)], fill=(70, 72, 104, 255))
    for xx in range(8, w // k - 6, 23): dd.point([(xx, 5), (xx + 1, 5)], fill=(170, 200, 255, 255))
    return up(L, k)
DAIS_Y = Y_S + 70
DAIS = stone_block(1080, WH - DAIS_Y + 8); LEDGE = stone_block(1080, 120)
VT = HB1 + 6
VMASK = Image.new('L', (W, H), 0); _vd = ImageDraw.Draw(VMASK)
for yy in range(VT, H): _vd.line([(0, yy), (W, yy)], fill=min(255, int(255 * (yy - VT) / 34)))
PED = crop(Image.open(SP + 'fork2/pedestal/00.png').convert('RGBA')); PED = up(PED, 3)
RAY = idle('ray', 4)
PR_DRAGON = up(Image.open(B5 + 'dragon128L.png').convert('RGBA'), 2)
cr = crop(Image.open(SP + 'pixellab/ref/crown_cands/01.png').convert('RGBA')); PR_CROWN = up(cr, max(1, 200 // cr.width))
PR_GUM = gummy('mel', 5)
PRIZES = [(PR_DRAGON, 'DRAGON'), (PR_CROWN, 'CROWN'), (PR_GUM, 'GUMMY')]
# ---------------------------------------------------------------- background: tall parallax of Liza's moon temple
src = Image.open(A + 'recov_hd.gif'); BG = []
BGH = 2700
for k_ in range(0, src.n_frames, 2):
    src.seek(k_); f_ = src.convert('RGB').crop((744, 0, 1176, 1080)).resize((W, BGH), Image.NEAREST)
    from PIL import ImageEnhance
    BG.append(ImageEnhance.Brightness(f_).enhance(0.40).convert('RGBA'))
random.seed(4)
motes = [(random.uniform(0, W), random.uniform(0, WH), random.uniform(0.6, 1.6), random.uniform(0, 6.3)) for _ in range(140)]
# ---------------------------------------------------------------- timing / camera
SCR_START = Y_S - 1290          # camera so the orbs sit at screen y 1290
LEDGE_SCREEN = 1180
SCR_END = Y_L - LEDGE_SCREEN
T0, T1 = 0.0, 10.8              # scroll (ease in/out), motion from frame 0
T_PRIZE = 11.0; T_SWAP = 11.9; T_LOOP = 14.0; DUR = 14.3; NF = int(round(DUR * FPS))
def cam(t):
    u = min(1, max(0, (t - T0) / (T1 - T0)))
    e = u * u * (3 - 2 * u)
    e = 0.88 * e + 0.12 * u                     # never fully stops at the start
    return SCR_START + (SCR_END - SCR_START) * e
ev = [(0.05, 'whoosh_8bit')]
wr = Writer('v50_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    loop = t >= T_LOOP
    if loop: t = 0.0
    c = cam(t); prog = (SCR_START - c) / (SCR_START - SCR_END)
    bg = BG[int(t * 6) % len(BG)]; by = int(-(BGH - H) * (1 - prog))
    img = Image.new('RGBA', (W, H), (8, 6, 20, 255)); img.alpha_composite(bg, (0, by))
    def motes_l(dd):
        for x, y, s, p in motes:
            yy = y - c * 0.6
            yy = yy % (H + 200) - 100
            dd.rectangle([x, yy, x + 4 * s, yy + 4 * s], fill=(200, 220, 255, int(110 + 90 * math.sin(t * 3 + p))))
    layer(img, motes_l)
    base = img.copy()
    # world window
    y0 = int(c); y1 = y0 + H
    def wcrop(im, oy=0):
        return im.crop((0, y0 - oy, W, y1 - oy))
    img.alpha_composite(wcrop(GLOW)); img.alpha_composite(wcrop(PATH_IMG))
    def runes(dd):
        for k_, (x, y, i) in enumerate(RUNES):
            sy = y - c
            if -20 < sy < H + 20:
                al = int(170 + 85 * math.sin(t * 4 + k_ * 0.7))
                dd.polygon([(x, sy - 6), (x + 6, sy), (x, sy + 6), (x - 6, sy)], fill=(255, 255, 255, al))
    layer(img, runes)
    # start dais, orbs, Rayleigh
    sy = DAIS_Y - c
    if sy < H:
        img.alpha_composite(DAIS, (0, int(sy)))
        def orbs(dd):
            for i in range(3):
                X, Y = SX[i], Y_S - c
                dd.ellipse([X - 40, Y - 40, X + 40, Y + 40], fill=(20, 14, 34, 240), outline=COL[i] + (255,), width=7)
        layer(img, orbs)
        text_layer(img, [(SX[i], Y_S - c - 18, LBL[i], 38, COL[i], 5, 255) for i in range(3)])
        rf = RAY[int(t * 8) % len(RAY)]; img.alpha_composite(rf, (int(760 - rf.width / 2), int(DAIS_Y + 4 - c - 78 * 4)))
    # prize ledge + pedestals
    ly = Y_L - c
    if ly > -400:
        lt = ly - 112                                   # ledge top; the paths run up into its face
        img.alpha_composite(LEDGE, (0, int(lt)))
        for k_ in range(3):
            X = TX[k_]
            layer(img, lambda dd, X=X: dd.rounded_rectangle([X - 30, ly - 34, X + 30, ly + 6], 8, fill=(20, 14, 34, 255), outline=(255, 214, 60, 255), width=4))
            ped = PED; img.alpha_composite(ped, (int(X - ped.width / 2), int(lt + 10 - ped.height)))
            top = lt + 10 - ped.height + 12
            if t < T_PRIZE:
                layer(img, lambda dd, X=X, top=top: dd.ellipse([X - 62, top - 140, X + 62, top - 16], fill=(20, 14, 34, 210), outline=(255, 214, 60, 230), width=5))
                text_layer(img, [(X, top - 106, '?', 60, (255, 214, 60), 6, 255)])
            else:
                u = min(1, (t - T_PRIZE - k_ * 0.25) / 0.35)
                if u > 0:
                    im, nm = PRIZES[k_]; s = 0.4 + 0.6 * u
                    pim = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
                    layer(img, lambda dd, X=X, top=top: dd.ellipse([X - 130, top - 250, X + 130, top + 10], fill=(255, 214, 60, int(45 * u))))
                    img.alpha_composite(pim, (int(X - pim.width / 2), int(top - pim.height)))
                    text_layer(img, [(X, lt + 30, nm, 28, (255, 255, 255), 5, int(255 * u))])
                    tt = round(T_PRIZE + k_ * 0.25, 3)
                    if not any(e[1] == 'chime' and abs(e[0] - tt) < 0.01 for e in ev): ev.append((tt, 'chime'))
    img = Image.composite(img, base, VMASK)          # world (paths, dais, ledge, prizes) only inside the safe viewport
    img.alpha_composite(HK2 if (t >= T_SWAP and not loop) else HK1)
    wr.write(img)
    if f % 60 == 0 or f in (NF - 1, int(T_PRIZE * FPS) + 20, int(T_SWAP * FPS) + 15): img.convert('RGB').save(f'p_{f:04d}.png')
wr.close()
ev += [(T_SWAP, 'twinkle')]
json.dump(ev, open('ev50.json', 'w')); print('done', DUR)
