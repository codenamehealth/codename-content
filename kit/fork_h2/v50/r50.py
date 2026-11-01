import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); sys.path.insert(0, SP0 + 'pixellab/safezone')
from common import *
import hook as _hk
sys.path.insert(0, SP + 'fork_rc1'); import hook2 as _h2
_f0 = _hk._fit; _h2._fit = lambda lines, maxw, hi=80, lo=48: _f0(lines, maxw, min(hi, 64), lo)
sys.path.insert(0, SP + 'fork_c7'); from degold import dragon_gummy
import numpy as np
from PIL import ImageFilter
os.chdir(HERE)
B5 = SP + 'fork_b5/'
# ---------------------------------------------------------------- layout (world = tall static map, camera scrolls up)
# hfg5: soft fade, no box; 'Comment your prize' sub cut from both hooks (caption asks). End swap to WHAT DID YOU GET? kept (it replaces the
# hook once the prizes are out, no extra line).
HK1, HB1 = _hk.hook_fade(['CHOOSE YOUR PATH', 'A, B OR C?'], accent=1)
# fork_h2 Oct 29 hook swap (bottom edge kept)
import sys as _s; _s.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h2'); import hookx
HK1, HB1 = hookx.fade_keep(['CHOOSE YOUR PATH', 'A, B OR C?'], ['WHICH ROPE GETS', [('THE ', None), ('CROWN?', hookx.GOLD)]], old_accent=1)
HK2, HB2 = _hk.hook_fade(['WHAT DID', 'YOU GET?'], accent=1)
print('hook bottoms', HB1, HB2)
LS = 4
Y_L = 520                    # world y of the prize ledge top (paths end here)
Y_S = 2300                   # world y of the start orbs (shorter climb: 2680 -> 1780px, fewer crossings, easier to trace)
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
    if not (6 <= len(cross) <= 8): return None
    ys = sorted(c[0] for c in cross)
    gaps = np.diff(ys)
    if len(gaps) and gaps.min() < 140: return None
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
# n6: travelling sparks (Bennett: 'icons or shooting stars or something to keep attention on the journey')
ARC = []
for i in range(3):
    seg = np.hypot(np.diff(PATHS[i]), np.diff(YS)); ARC.append(np.concatenate([[0], np.cumsum(seg)]))
SPK_V = 720.0; SPK_GAP = 470.0; SPK_PH = [0.0, 160.0, 320.0]
def spark_pos(i, s_):
    k = min(N - 1, int(np.searchsorted(ARC[i], s_))); return PATHS[i][k], YS[k]
def sparks(dd, t, c):
    for i in range(3):
        L_ = ARC[i][-1]; base = (t * SPK_V + SPK_PH[i]) % SPK_GAP
        for m in range(int(L_ / SPK_GAP) + 2):
            s_ = base + m * SPK_GAP
            if s_ > L_: break
            u = s_ / L_; a = min(1.0, u / 0.04, (1 - u) / 0.05)
            if a <= 0: continue
            for q in range(6, -1, -1):          # trail behind (down the rope), head last
                x, y = spark_pos(i, max(0, s_ - q * 20)); sy = y - c
                if not (-40 < sy < H + 40): continue
                x4, y4 = int(x) // 4 * 4, int(sy) // 4 * 4
                lc = tuple(min(255, v + 110) for v in COL[i])
                if q == 0:
                    dd.ellipse([x4 - 38, y4 - 38, x4 + 38, y4 + 38], fill=COL[i] + (int(90 * a),))
                    dd.ellipse([x4 - 24, y4 - 24, x4 + 24, y4 + 24], fill=lc + (int(170 * a),))
                    dd.rectangle([x4 - 4, y4 - 30, x4 + 4, y4 + 30], fill=(255, 255, 255, int(220 * a)))
                    dd.rectangle([x4 - 30, y4 - 4, x4 + 30, y4 + 4], fill=(255, 255, 255, int(220 * a)))
                    dd.rectangle([x4 - 12, y4 - 12, x4 + 12, y4 + 12], fill=(255, 255, 255, int(255 * a)))
                else:
                    r_ = 13 - q * 1.5
                    dd.rectangle([x4 - r_, y4 - r_, x4 + r_, y4 + r_], fill=lc + (int(a * (230 - q * 28)),))
_sr = random.Random(77)
STARS = []                                   # shooting stars in the sky behind the ropes (screen space)
for t0 in (0.35, 1.25, 2.1, 3.0, 3.85, 4.7, 5.6, 6.45, 7.6, 8.5):
    sx_ = _sr.uniform(150, 930); sy_ = _sr.uniform(480, 1150); dr = _sr.choice([-1, 1])
    STARS.append((t0, sx_, sy_, dr, _sr.uniform(0.9, 1.2)))
STARS = [st_ for st_ in STARS if st_[0] < 6.0]   # n6: none near the pedestals once they are on screen (no star 'pointing' at a prize) or over the reveal
def shooting(dd, t):
    for t0, sx_, sy_, dr, sp in STARS:
        u = (t - t0) / 0.7
        if not (0 <= u < 1): continue
        hx = sx_ + dr * 620 * sp * u; hy = sy_ + 300 * sp * u
        fa = min(1.0, u / 0.15, (1 - u) / 0.3)
        for q in range(16):
            tx, ty = hx - dr * q * 22, hy - q * 10.6
            r_ = max(2, 10 - q // 2); al = int(fa * 240 * (1 - q / 16))
            dd.rectangle([int(tx) // 4 * 4 - r_, int(ty) // 4 * 4 - r_, int(tx) // 4 * 4 + r_, int(ty) // 4 * 4 + r_], fill=(255, 248, 210, al))
        hx4, hy4 = int(hx) // 4 * 4, int(hy) // 4 * 4
        dd.ellipse([hx4 - 26, hy4 - 26, hx4 + 26, hy4 + 26], fill=(255, 240, 190, int(fa * 90)))
        dd.rectangle([hx4 - 4, hy4 - 22, hx4 + 4, hy4 + 22], fill=(255, 255, 255, int(fa * 240))); dd.rectangle([hx4 - 22, hy4 - 4, hx4 + 22, hy4 + 4], fill=(255, 255, 255, int(fa * 240)))
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
BMASK = Image.new('L', (W, H), 255); _bd = ImageDraw.Draw(BMASK)
for yy in range(1460, H): _bd.line([(0, yy), (W, yy)], fill=max(0, int(255 * (1 - (yy - 1460) / 44))))
VMASK = Image.new('L', (W, H), 0); _vd = ImageDraw.Draw(VMASK)
for yy in range(VT, H): _vd.line([(0, yy), (W, yy)], fill=min(255, int(255 * (yy - VT) / 34)))
PED = crop(Image.open(SP + 'fork2/pedestal/00.png').convert('RGBA')); PED = up(PED, 3)
RAY = idle('ray', 4)
PR_DRAGON = dragon_gummy([up(Image.open(B5 + 'dragon128L.png').convert('RGBA'), 2)], 150, 1)[0]   # gold coin hoard -> pile of the four gummies (no gold anywhere)
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
T1 = 7.0; TA = 5.6                # steady scroll from frame 0, eases out onto the terrace
T_PRIZE = 7.2; T_SWAP = 8.1; PRE = 0.3; T_LOOP = T_SWAP + 1.2; DUR = T_LOOP + PRE; NF = int(round(DUR * FPS))
VCAM = (SCR_START - SCR_END) / (TA + (T1 - TA) / 2)
def cam(t):
    if t >= T1: s_ = SCR_START - SCR_END
    elif t >= TA: s_ = VCAM * TA + VCAM * (t - TA) - VCAM * (t - TA) ** 2 / (2 * (T1 - TA))
    else: s_ = VCAM * t                             # t < 0 = pre-roll below the start (loop)
    return SCR_START - s_
ev = [(0.05, 'swish')]
wr = Writer('v50_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    loop = t >= T_LOOP - 1e-6
    if loop: t = t - DUR             # pre-roll: camera rising into the opening shot, so the loop is seamless
    c = cam(t); prog = (SCR_START - c) / (SCR_START - SCR_END)
    bg = BG[int((t % 30) * 6) % len(BG)]; by = int(-(BGH - H) * (1 - min(1, max(0, prog))))
    img = Image.new('RGBA', (W, H), (8, 6, 20, 255)); img.alpha_composite(bg, (0, by))
    def motes_l(dd):
        for x, y, s, p in motes:
            yy = y - c * 0.6
            yy = yy % (H + 200) - 100
            dd.rectangle([x, yy, x + 4 * s, yy + 4 * s], fill=(200, 220, 255, int(110 + 90 * math.sin(t * 3 + p))))
    layer(img, motes_l)
    layer(img, lambda dd: shooting(dd, t))      # n6
    base = img.copy()
    # world window
    y0 = int(c); y1 = y0 + H
    def wcrop(im, oy=0):
        return im.crop((0, y0 - oy, W, y1 - oy))
    pl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pl.alpha_composite(wcrop(GLOW)); pl.alpha_composite(wcrop(PATH_IMG))
    def runes(dd):
        for k_, (x, y, i) in enumerate(RUNES):
            sy = y - c
            if -20 < sy < H + 20:
                al = int(170 + 85 * math.sin(t * 4 + k_ * 0.7))
                dd.polygon([(x, sy - 6), (x + 6, sy), (x, sy + 6), (x - 6, sy)], fill=(255, 255, 255, al))
    layer(pl, runes)
    layer(pl, lambda dd: sparks(dd, t, c))     # n6: sparks ride each rope in its own colour, all the same speed
    img.alpha_composite(pl)          # hfg5 full-bleed: paths run the full height of the frame (no fade-out at y1460-1500)
    # start dais, orbs, Rayleigh
    sy = DAIS_Y - c
    if sy < H:
        img.alpha_composite(DAIS, (0, int(sy)))
        def orbs(dd):
            for i in range(3):
                X, Y = SX[i], Y_S - c
                dd.ellipse([X - 40, Y - 40, X + 40, Y + 40], fill=(20, 14, 34, 240), outline=COL[i] + (255,), width=7)
        pz = 1.0 + 0.35 * max(0, math.sin(math.pi * (t + 0.3) / 0.8)) if -0.3 <= t < 0.5 else 1.0   # A/B/C pulse once so viewers lock in a pick
        def orbs(dd, pz=pz):
            for i in range(3):
                X, Y = SX[i], Y_S - c; r_ = 46 * pz
                dd.ellipse([X - r_, Y - r_, X + r_, Y + r_], fill=(20, 14, 34, 240), outline=COL[i] + (255,), width=8)
        layer(img, orbs)
        text_layer(img, [(SX[i], Y_S - c - int(24 * pz), LBL[i], int(48 * pz), COL[i], 6, 255) for i in range(3)])
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
                qa = max(0.0, min(1.0, (top - 140 - (HB1 + 128)) / 70))   # n6 review: ? bubbles only fade in once below the hook (no scrolling through the title)
                if qa > 0:
                    layer(img, lambda dd, X=X, top=top, qa=qa: dd.ellipse([X - 62, top - 140, X + 62, top - 16], fill=(20, 14, 34, int(210 * qa)), outline=(255, 214, 60, int(230 * qa)), width=5))
                    text_layer(img, [(X, top - 106, '?', 60, (255, 214, 60), 6, int(255 * qa))])
            else:
                u = min(1, (t - T_PRIZE - k_ * 0.25) / 0.35)
                if u > 0:
                    im, nm = PRIZES[k_]; s = 0.4 + 0.6 * u
                    pim = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
                    layer(img, lambda dd, X=X, top=top: dd.ellipse([X - 130, top - 250, X + 130, top + 10], fill=(255, 214, 60, int(45 * u))))
                    img.alpha_composite(pim, (int(X - pim.width / 2), int(top - pim.height)))
                    tt = round(T_PRIZE + k_ * 0.25, 3)
                    if not any(e[1] == 'chime' and abs(e[0] - tt) < 0.01 for e in ev): ev.append((tt, 'chime'))
    # hfg5 full-bleed: world no longer clipped to a viewport under the hook; it runs edge to edge behind the fade
    img.alpha_composite(HK2 if (t >= T_SWAP and not loop) else HK1)
    wr.write(img)
    if f % 60 == 0 or f in (NF - 1, int(T_PRIZE * FPS) + 20, int(T_SWAP * FPS) + 15): img.convert('RGB').save(f'p_{f:04d}.png')
wr.close()
ev += [(T_SWAP, 'twinkle')]
json.dump({'events': ev}, open('ev50.json', 'w')); print('done', DUR)
