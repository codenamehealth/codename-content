# m01: recreation of igref/DaG5nn5v8AP.mp4 ("Choose a Square" flood maze) with our guides. Run: python3 m01.py SEED
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); os.chdir(os.path.dirname(os.path.abspath(__file__)))
from m01_cfg import *
SEED = int(sys.argv[1])
HOOK_LINES = os.environ.get('HOOK', 'WHO ESCAPES|THE SHADOW?').split('|')     # swap here
M = Maze(CFG); U, X0, Y0, HS = M.U, M.X0, M.Y0, M.HS
XX, FR, EV, GUM, WIN, CT = M.sim(SEED, 62)
T_WIN, WANT = WIN if WIN else (float(os.environ.get("FAKEWIN", "55")), "joy")
print('win', WIN, 'outs', [(round(e[0], 2), e[2], e[3]) for e in EV if e[1] == 'out'], 'gum', GUM['who'], GUM['t'])
if len(sys.argv) > 2 and sys.argv[2] == 'info': sys.exit()
# steering self-check: direction change on a frame with no wall / brick / box / flood contact
st_ = {g: [0, 0] for g in G}
for i in range(1, len(FR)):
    for g in G:
        a, b = FR[i - 1][0][g], FR[i][0][g]
        if a[4] is not None or b[4] is not None or i / FPS < 0.3: continue
        st_[g][1] += 1
        if (a[2] > 0) != (b[2] > 0) or (a[3] > 0) != (b[3] > 0) or abs(math.hypot(a[2], a[3]) - math.hypot(b[2], b[3])) > 1e-6:
            if not FR[i][3][g]: st_[g][0] += 1
print('steering check (unexplained direction changes / frames):', {g: f'{a}/{b}' for g, (a, b) in st_.items()})
# teleport / wall check: no per-frame jump beyond box + flood speed, never inside a wall or an intact brick
MAXSTEP = (M.SPD + 3.2 * U) / FPS + 2; jumps = []; inwall = []
for i in range(1, len(FR)):
    for g in G:
        a, b = FR[i - 1][0][g], FR[i][0][g]
        if b[4] is not None and b[4] < i / FPS - 1e-6: continue
        if math.hypot(b[0] - a[0], b[1] - a[1]) > MAXSTEP: jumps.append((round(i / FPS, 2), g))
        r0, r1 = int((b[1] - HS + 0.5 - Y0) // U), int((b[1] + HS - 0.5 - Y0) // U); c0, c1 = int((b[0] - HS + 0.5 - X0) // U), int((b[0] + HS - 0.5 - X0) // U)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if M.is_wall(r, c) or ((r, c) in FR[i][2] and FR[i][2][(r, c)] > 0): inwall.append((round(i / FPS, 2), g, r, c))
print('teleport check (jumps >', round(MAXSTEP, 1), 'px/frame):', len(jumps), jumps[:5], '| inside wall/brick frames:', len(inwall), inwall[:5])
print('frame 0 vs first sim step:', {g: round(math.hypot(FR[min(7, len(FR)-1)][0][g][0] - FR[0][0][g][0], FR[min(7, len(FR)-1)][0][g][1] - FR[0][0][g][1]), 1) for g in G}, '(frames 0-7 travel, max', round(7 * M.SPD / FPS, 1), ')')
T_CARD = T_WIN + 1.0; T_END = T_WIN + 3.5; NF = int(round(T_END * FPS))
def frame_at(t): return FR[min(max(0, int(round(t * FPS))), len(FR) - 1)]
HOOK, HB = hook_fade(HOOK_LINES, accent=1, size=54, y=236, fade_to=398)
# ---------------- assets
wsheet = Image.open(S_ + 'pixellab/maze/walls_sheet.png').convert('RGBA')
BRICK = up(wsheet.crop((77, 13, 128, 56)), 2)
def tint(im, col, k=0.78):
    a = np.array(im).astype(float); g_ = a[..., :3].mean(2, keepdims=True) / 255.0
    a[..., :3] = a[..., :3] * (1 - k) + (np.array(col)[None, None, :] * (0.35 + 0.95 * g_)) * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
FACE24 = {}; FACE18 = {}
for g, fn in [('joy', 'idle_0.gif'), ('cyrus', 'idle_1.gif'), ('ray', 'idle_2.gif'), ('cleo', 'idle_3.gif')]:
    im = Image.open(A + fn); im.seek(0); im = im.convert('RGBA').resize((92, 92), Image.NEAREST)
    cx = 46 if g != 'cleo' else 47; FACE24[g] = im.crop((cx - 12, 15, cx + 12, 39)); FACE18[g] = up(im.crop((cx - 9, 18, cx + 9, 36)), 2)
def vic_frames(g, k):
    im = Image.open(A + VIC[g]); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), k))
    return out
VIC_W = vic_frames(WANT, 5)
GUMI = up(Image.open(PL + 'gummies/pick_cre.png').convert('RGBA'), 2); GUM_SMALL = Image.open(PL + 'gummies/pick_cre.png').convert('RGBA').resize((14, 12), Image.NEAREST)
STR_COL = (255, 92, 70)
sys.path.insert(0, S_ + 'm456')
from PIL import ImageChops
from rlib import castle_backdrop, flagstones, castle_bricks, sconce, torch_flame, portal_glow   # shared Code Name castle kit (m05/m06 look)
BG = [castle_backdrop()]
def _sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c)
MOSS = [(92, 132, 70), (110, 150, 80), (72, 108, 58)]
BX1_, BY1_ = X0 + M.COLS * U, Y0 + M.ROWS * U
WALLF = castle_bricks(X0, Y0, BX1_, BY1_, seed=7)
FLOORF = flagstones(X0, Y0, BX1_ - 1, BY1_ - 1, seed=3)
def floorish(r, c): return 0 <= r < M.ROWS and 0 <= c < M.COLS and M.MAP[r][c] != '#'
# ---------------- static layer
mw = Image.new('L', (W, H), 0); mf = Image.new('L', (W, H), 0); dw = ImageDraw.Draw(mw); df = ImageDraw.Draw(mf)
EXR = [(r, c) for r in range(M.ROWS) for c in range(M.COLS) if M.MAP[r][c] == 'E']
for r in range(M.ROWS):
    for c in range(M.COLS):
        x0, y0 = X0 + c * U, Y0 + r * U
        if M.MAP[r][c] == '#': dw.rectangle([x0, y0, x0 + U - 1, y0 + U - 1], fill=255)
        else: df.rectangle([x0, y0, x0 + U - 1, y0 + U - 1], fill=255)
MZ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); MZ.paste(WALLF, (0, 0), mw); MZ.paste(FLOORF, (0, 0), mf)
_bd = ImageDraw.Draw(MZ); _bd.rectangle([X0 - 4, Y0 - 4, BX1_ + 3, BY1_ + 3], outline=(40, 34, 40, 255), width=4)
ao = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ao)
for r in range(1, M.ROWS):
    for c in range(M.COLS):
        if M.MAP[r][c] != '#' and M.MAP[r - 1][c] == '#':
            for k in range(4): ad.rectangle([X0 + c * U, Y0 + r * U + 2 * k, X0 + c * U + U - 1, Y0 + r * U + 2 * k + 1], fill=(26, 14, 10, 92 - k * 22))
MZ.alpha_composite(ao)
TORCH = [(11, 9), (15, 6), (19, 11), (7, 15)]                          # wall cells that carry a torch
d = ImageDraw.Draw(MZ)
for (r, c) in TORCH: sconce(d, X0 + c * U + U // 2, Y0 + r * U + 12)
er0, er1 = min(r for r, c in EXR), max(r for r, c in EXR); ec0, ec1 = min(c for r, c in EXR), max(c for r, c in EXR)
GX0, GY0, GX1, GY1 = X0 + ec0 * U, Y0 + er0 * U, X0 + (ec1 + 1) * U, Y0 + (er1 + 1) * U
def exit_gate(img, t):
    """exit: golden light brightest at the far (right) end, stone arch at the mouth, raised portcullis"""
    tmp = Image.new('RGBA', (GX1 - GX0, GY1 - GY0)); portal_glow(tmp, 0, 0, GX1 - GX0, GY1 - GY0, t, 'left')
    img.alpha_composite(tmp.transpose(Image.FLIP_LEFT_RIGHT), (GX0, GY0)); dd = ImageDraw.Draw(img)
    for k, yy in enumerate(range(GY0 - 44, GY0 - 4, 12)): dd.rectangle([GX0 + 2, yy, GX0 + 15, yy + 10], fill=(200, 188, 170, 255) if k % 2 else (178, 166, 150, 255), outline=(90, 82, 86, 255))
    dd.rectangle([GX0, GY0, GX1 - 1, GY0 + 9], fill=(60, 56, 64, 255))
    for xx in range(GX0 + 6, GX1 - 4, 12): dd.rectangle([xx, GY0 + 9, xx + 3, GY0 + 17], fill=(70, 66, 76, 255)); dd.polygon([(xx, GY0 + 17), (xx + 3, GY0 + 17), (xx + 1, GY0 + 22)], fill=(70, 66, 76, 255))
BRICK_T = WALLF.crop((X0 + 3, Y0 + 5, X0 + 3 + U, Y0 + 5 + U))
def crack(dd):
    dd.line([(10, 0), (16, 12), (12, 22), (22, 32), (20, 45)], fill=(14, 8, 20, 255), width=3); dd.line([(16, 12), (30, 16), (36, 26)], fill=(14, 8, 20, 255), width=2)
    dd.rectangle([30, 2, 40, 9], fill=(22, 16, 30, 255))
def door_img():
    im = Image.new('RGBA', (U, U), (60, 38, 30, 255)); dd = ImageDraw.Draw(im); rr = random.Random(3)
    planks = [(132, 86, 58), (118, 76, 52), (140, 94, 64), (124, 80, 54)]; pw = U / 4
    for i in range(4):
        x0_, x1_ = int(i * pw) + 2, int((i + 1) * pw) - 1; dd.rectangle([x0_, 2, x1_, U - 3], fill=planks[i] + (255,))
        dd.line([(x0_, 2), (x0_, U - 3)], fill=_sh(planks[i], 1.15) + (255,))
        for _ in range(5): gy = 2 * rr.randint(2, (U - 6) // 2); dd.line([(x0_ + 2, gy), (x0_ + 5, gy)], fill=_sh(planks[i], 0.82) + (255,))
    for by in (9, U - 15):                                            # iron bands with rivets
        dd.rectangle([1, by, U - 2, by + 6], fill=(66, 64, 78, 255)); dd.line([(1, by), (U - 2, by)], fill=(126, 124, 140, 255))
        for i in range(4): rx = int((i + 0.5) * pw); dd.rectangle([rx - 1, by + 2, rx + 1, by + 4], fill=(184, 182, 196, 255))
    dd.rectangle([0, 0, U - 1, U - 1], outline=(30, 18, 16, 255), width=2)
    return im
DOORI = door_img()
def brick_img(col, hp, hp0):
    if col == DARK:
        im = DOORI.copy()
        if hp < hp0: crack(ImageDraw.Draw(im))
        return im
    im = Image.new('RGBA', (U, U)); im.alpha_composite(tint(BRICK_T, col, 0.62)); dd = ImageDraw.Draw(im)
    dd.rectangle([0, 0, U - 1, 3], fill=tuple(min(255, int(v * 1.3)) for v in col) + (255,)); dd.rectangle([0, 0, U - 1, U - 1], outline=(18, 12, 24, 255), width=2)
    if hp == 1: crack(dd)
    return im
WEDGE = Image.new('RGBA', (W, H), (0, 0, 0, 0)); wd = ImageDraw.Draw(WEDGE)        # light stone rims keep walls readable over the flood
for r in range(M.ROWS):
    for c in range(M.COLS):
        if M.MAP[r][c] != '#': continue
        x0, y0 = X0 + c * U, Y0 + r * U; ec = (206, 198, 190, 255); ed = (86, 78, 84, 255)
        if floorish(r - 1, c): wd.rectangle([x0, y0, x0 + U - 1, y0 + 2], fill=ec); wd.rectangle([x0, y0 + 3, x0 + U - 1, y0 + 3], fill=ed)
        if floorish(r + 1, c): wd.rectangle([x0, y0 + U - 3, x0 + U - 1, y0 + U - 1], fill=ec); wd.rectangle([x0, y0 + U - 4, x0 + U - 1, y0 + U - 4], fill=ed)
        if floorish(r, c - 1): wd.rectangle([x0, y0, x0 + 2, y0 + U - 1], fill=ec); wd.rectangle([x0 + 3, y0, x0 + 3, y0 + U - 1], fill=ed)
        if floorish(r, c + 1): wd.rectangle([x0 + U - 3, y0, x0 + U - 1, y0 + U - 1], fill=ec); wd.rectangle([x0 + U - 4, y0, x0 + U - 4, y0 + U - 1], fill=ed)
BIMG = {}
for k, b in M.BRK.items():
    for hp in range(1, b['hp0'] + 1): BIMG[(b['col'], hp, b['hp0'])] = brick_img(b['col'], hp, b['hp0'])
# ---------------- shadow
SW_, SH_ = M.COLS * U, M.ROWS * U; PADX = 8
_nz = np.array(Image.effect_noise(((SW_ + 2 * PADX) // 6 + 1, SH_ // 6 + 1), 80).filter(ImageFilter.GaussianBlur(1.2))).astype(float) / 255.0
_q = np.clip(np.floor(_nz * 4), 0, 3)                                  # 4 pixel-art tones of rich dark purple
SHPAL = np.array([[20, 9, 38], [28, 13, 52], [38, 17, 68], [48, 21, 86]], np.uint8)
FLB = mf.crop((X0, Y0, X0 + SW_, Y0 + SH_))
NZB = Image.effect_noise(((SW_ + 160) // 4, (SH_ + 160) // 4), 60).resize((SW_ + 160, SH_ + 160), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6)).point(lambda v: min(255, max(0, int((v - 60) * 1.6))))
_sc = np.zeros(_q.shape + (4,), np.uint8); _sc[..., :3] = SHPAL[_q.astype(int)]; _sc[..., 3] = 250
SHADOW_TEX = Image.fromarray(_sc).resize((_q.shape[1] * 6, _q.shape[0] * 6), Image.NEAREST).crop((0, 0, SW_ + 2 * PADX, SH_))
CREST = np.array([150, 96, 220], np.uint8)
def shadow_layer(t, prog):
    m = Image.new('L', (SW_, SH_), 0); md = ImageDraw.Draw(m); fronts = []
    for k, p in enumerate(prog):
        sg = M.SEGS[k]
        for (x0, y0, x1, y1) in M.seg_cover(k, p):
            md.rectangle([x0 - X0, y0 - Y0, max(x0 - X0, x1 - X0 - 1), max(y0 - Y0, y1 - Y0 - 1)], fill=255)
            if 0 < p < sg['len'] and x1 - x0 >= 4 and y1 - y0 >= 4: fronts.append((k, sg['dir'], int(x0 - X0), int(y0 - Y0), int(math.ceil(x1 - X0)), int(math.ceil(y1 - Y0))))
    ox = PADX + int(round(6 * math.sin(t)))                              # texture drifts, but always covers the whole mask (no edge seam)
    L = Image.new('RGBA', (SW_, SH_), (0, 0, 0, 0)); L.paste(SHADOW_TEX.crop((ox, 0, ox + SW_, SH_)), (0, 0), m)
    free = ImageChops.subtract(FLB, m)                                  # open floor the shadow borders (same edge treatment as m05/m06)
    ox_, oy_ = int(t * 23) % 160, int(t * 17) % 160; nzc = NZB.crop((ox_, oy_, ox_ + SW_, oy_ + SH_))
    glow = free.filter(ImageFilter.GaussianBlur(8)).point(lambda v: min(255, int(v * 2.4)))
    ga = ImageChops.multiply(ImageChops.multiply(glow, m), nzc)
    gl = Image.new('RGBA', (SW_, SH_), (150, 92, 236, 255)); gl.putalpha(ga.point(lambda v: int(v * 0.8))); L.alpha_composite(gl)
    edge = ImageChops.multiply(free.filter(ImageFilter.MaxFilter(5)), m)
    el = Image.new('RGBA', (SW_, SH_), (206, 164, 255, 255)); el.putalpha(ImageChops.multiply(edge, nzc).point(lambda v: int(v * 0.75))); L.alpha_composite(el)
    ma = np.array(m); dd = ImageDraw.Draw(L)
    if fronts:                                                       # one pair of eyes, just behind the newest front
        k, dd_, x0, y0, x1, y1 = max(fronts, key=lambda f: (f[0], (f[4] - f[2]) * (f[5] - f[3])))
        L_ = (y1 - y0) if dd_ in 'UD' else (x1 - x0)
        if L_ >= 56:
            if dd_ == 'D': ex, ey = (x0 + x1) // 2, y1 - 36
            elif dd_ == 'U': ex, ey = (x0 + x1) // 2, y0 + 30
            elif dd_ == 'R': ex, ey = x1 - 34, (y0 + y1) // 2
            else: ex, ey = x0 + 34, (y0 + y1) // 2
            if 0 <= ey - 6 and ey + 6 < SH_ and 0 <= ex - 12 and ex + 12 < SW_ and ma[ey, ex - 10] and ma[ey, ex + 10]:
                if (t % 3.2) < 0.14: dd.rectangle([ex - 11, ey, ex + 11, ey + 2], fill=(236, 226, 255, 235))
                else:
                    for sx in (-11, 5): dd.rectangle([ex + sx, ey - 4, ex + sx + 5, ey + 4], fill=(244, 238, 255, 250)); dd.rectangle([ex + sx + 2, ey - 1, ex + sx + 4, ey + 3], fill=(40, 16, 64, 255))
    return L
def box_img(g, dead=False):
    n = 2 * HS; b = Image.new('RGBA', (n, n), (14, 10, 20, 255))
    fz = FACE18[g]; bg_ = Image.new('RGBA', fz.size, tuple(int(v * 0.55) for v in COL[g]) + (255,)); bg_.alpha_composite(fz); b.alpha_composite(bg_, ((n - fz.width) // 2, (n - fz.height) // 2))
    dd = ImageDraw.Draw(b); dd.rectangle([0, 0, n - 1, n - 1], outline=COL[g] + (255,), width=2)
    if dead:
        b = Image.blend(b, Image.new('RGBA', b.size, (40, 36, 54, 255)), 0.45).copy(); b.putalpha(255); dd = ImageDraw.Draw(b)
        dd.line([4, 4, n - 5, n - 5], fill=(10, 6, 16, 255), width=4); dd.line([4, n - 5, n - 5, 4], fill=(10, 6, 16, 255), width=4)
    return b
BOXI = {g: box_img(g) for g in G}; DEADI = {g: box_img(g, True) for g in G}
ROSTER_FACE = {g: up(FACE24[g], 2) for g in G}
RX0, RX1 = 70, X0 + 3 * U - 6
def roster(img, t):
    for i, g in enumerate(G):
        y0 = Y0 + 6 + i * 88; y1 = y0 + 82
        out = XX[g]['out'] is not None and XX[g]['out'] <= t
        win = t >= T_WIN and g == WANT
        layer(img, lambda dd, y0=y0, y1=y1, win=win, g=g: dd.rounded_rectangle([RX0, y0, RX1, y1], 10, fill=(14, 10, 22, 235), outline=(255, 214, 60, 255) if win else COL[g] + (255,), width=5 if win else 3))
        fc = ROSTER_FACE[g]
        if out: fc = ImageEnhance.Brightness(ImageEnhance.Color(fc).enhance(0.15)).enhance(0.45)
        fx = (RX0 + RX1) // 2 - 24; img.alpha_composite(fc, (fx, y0 + 5))
        nm = NAME[g]; fs_ = 18 if len(nm) <= 4 else 15 if len(nm) <= 5 else 13
        d_ = ImageDraw.Draw(img); tw_ = d_.textlength(nm, font=F(fs_))
        d_.text(((RX0 + RX1) / 2 - tw_ / 2, y0 + 58), nm, font=F(fs_), fill=(120, 110, 130) if out else COL[g], stroke_width=3, stroke_fill=(10, 6, 16))
        if out:
            d_.line([fx - 4, y0 + 4, fx + 52, y0 + 56], fill=(230, 50, 60), width=6); d_.line([fx - 4, y0 + 56, fx + 52, y0 + 4], fill=(230, 50, 60), width=6)
            tw2 = d_.textlength('OUT', font=F(16)); d_.text(((RX0 + RX1) / 2 - tw2 / 2, y0 + 22), 'OUT', font=F(16), fill=(255, 80, 80), stroke_width=4, stroke_fill=(10, 6, 16))
SCHED = [(e[0], e[0] + 1.2, NAME[e[2]] + ': STRENGTH!') for e in EV if e[1] == 'pick']
BREAKS = [e for e in EV if e[1] == 'break']
STILLS = [float(x) for x in os.environ.get('STILLS', '').split(',') if x]
OUTV = os.environ.get('OUTV', 'm01_noaudio_tmp.mp4')
wr = None if STILLS else Writer(OUTV)
WXY = frame_at(T_WIN)[0][WANT][:2]
for f in range(NF):
    t = f / FPS
    if STILLS and not any(abs(t - x) < 0.5 / FPS for x in STILLS): continue
    tt = min(t, T_WIN); st, prog, hp, _ = frame_at(tt)
    img = BG[0].copy(); img.alpha_composite(MZ); exit_gate(img, t)
    for k, b in M.BRK.items():
        if hp[k] > 0: img.alpha_composite(BIMG[(b['col'], max(1, min(hp[k], b['hp0'])), b['hp0'])], (X0 + k[1] * U, Y0 + k[0] * U))
    if GUM['t'] is None or tt < GUM['t']:
        gx, gy = GUM['x'], GUM['y']; bob = 3 * math.sin(t * 4)
        layer(img, lambda dd: [dd.ellipse([gx - 30 + q * 8, gy - 30 + q * 8, gx + 30 - q * 8, gy + 30 - q * 8], fill=STR_COL + (30 + q * 22,)) for q in range(3)])
        img.alpha_composite(GUMI, (int(gx - GUMI.width / 2), int(gy - GUMI.height / 2 + bob)))
    for g in G:                                                       # knocked-out boxes stay where they fell (X), under the dark
        x, y, vx, vy, out, strong, how = st[g]
        if out is not None and out <= tt: img.alpha_composite(DEADI[g], (int(x - HS), int(y - HS)))
    if t < T_CARD:
        for g in G:                                                   # comet trails
            x, y, vx, vy, out, strong, how = st[g]
            if out is not None or tt < 0.25: continue
            for q in range(1, 7):
                s0 = frame_at(max(0, tt - q * 0.03))[0][g]; a_ = 120 - q * 17; s_ = int(HS * (1 - q * 0.11))
                layer(img, lambda dd, px_=s0[0], py_=s0[1], a_=a_, s_=s_, g=g, strong=strong: dd.rectangle([px_ - s_, py_ - s_, px_ + s_, py_ + s_], fill=(STR_COL if strong else COL[g]) + (a_,)))
    img.alpha_composite(shadow_layer(t, prog), (X0, Y0)); img.alpha_composite(WEDGE)
    for i_, (r_, c_) in enumerate(TORCH): torch_flame(img, X0 + c_ * U + U // 2, Y0 + r_ * U + 12, t, i_ * 1.7)
    for g in G:
        x, y, vx, vy, out, strong, how = st[g]
        if out is not None and out <= tt:
            if tt - out < 0.4:                                       # knock-out burst in the guide's colour
                u2 = (tt - out) / 0.4; rr = random.Random(hash(g) % 997); pts = [(rr.uniform(0, 6.283), rr.uniform(0.6, 1.0)) for _ in range(12)]
                layer(img, lambda dd, u2=u2, pts=pts, x=x, y=y, g=g: [dd.rectangle([x + (20 + 80 * u2 * sp) * math.cos(a) - 4, y + (20 + 80 * u2 * sp) * math.sin(a) - 4, x + (20 + 80 * u2 * sp) * math.cos(a) + 4, y + (20 + 80 * u2 * sp) * math.sin(a) + 4], fill=COL[g] + (int(255 * (1 - u2)),)) for a, sp in pts])
            continue
        if t >= T_CARD and g == WANT: continue
        if strong:
            pul = 0.5 + 0.5 * math.sin(t * 14)
            layer(img, lambda dd, x=x, y=y, pul=pul: dd.rectangle([x - HS - 5, y - HS - 5, x + HS + 4, y + HS + 4], outline=STR_COL + (int(140 + 100 * pul),), width=3))
        img.alpha_composite(BOXI[g], (int(x - HS), int(y - HS)))
        if strong: img.alpha_composite(GUM_SMALL, (int(x + HS - 16), int(y + HS - 14)))      # badge inside the box
    for e in BREAKS:                                                 # brick dust
        if 0 <= tt - e[0] < 0.4 and t < T_CARD:
            r, c = e[3]; u2 = (tt - e[0]) / 0.4; cx_, cy_ = X0 + c * U + U / 2, Y0 + r * U + U / 2; rr = random.Random(r * 31 + c)
            pts = [(rr.uniform(-1, 1), rr.uniform(-1, 1)) for _ in range(7)]; colb = M.BRK[e[3]]['col']
            layer(img, lambda dd, u2=u2, pts=pts, cx_=cx_, cy_=cy_, colb=colb: [dd.rectangle([cx_ + a * (10 + 40 * u2) - 5, cy_ + b * (10 + 40 * u2) - 5, cx_ + a * (10 + 40 * u2) + 5, cy_ + b * (10 + 40 * u2) + 5], fill=colb + (int(230 * (1 - u2)),)) for a, b in pts])
    for st0, en, text in SCHED:
        if st0 <= t < en and t < T_CARD:
            u = t - st0; al = int(255 * min(1, (en - t) / 0.2)); fs2 = int(40 * (1 + 0.15 * max(0, 1 - u / 0.12))); tw_ = len(text) * fs2; yy = Y0 + 11 * U + 4
            layer(img, lambda dd, tw_=tw_, fs2=fs2, al=al, yy=yy: dd.rounded_rectangle([540 - tw_ / 2 - 18, yy - 14, 540 + tw_ / 2 + 18, yy + fs2 + 14], 14, fill=(14, 8, 22, int(230 * al / 255))))
            text_layer(img, [(540, yy, text, fs2, STR_COL, 7, al)])
    if T_WIN <= t < T_CARD:
        u = (t - T_WIN) / (T_CARD - T_WIN); wx, wy = WXY
        layer(img, lambda dd, u=u: dd.rectangle([wx - HS - 6 - 30 * u, wy - HS - 6 - 30 * u, wx + HS + 6 + 30 * u, wy + HS + 6 + 30 * u], outline=(255, 214, 60, int(255 * (1 - u))), width=5))
    if t < T_CARD: roster(img, t)
    if t >= T_CARD:
        u = t - T_CARD; a_ = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([X0, Y0, X0 + SW_, Y0 + SH_], fill=(8, 6, 16, int(170 * a_))))
        vf = VIC_W[int(u * 8) % len(VIC_W)]; q = min(1.0, u / 0.25); sc = 0.3 + 0.7 * (1 - (1 - q) ** 3)
        vf2 = vf if sc >= 0.999 else vf.resize((max(2, int(vf.width * sc)), max(2, int(vf.height * sc))), Image.NEAREST)
        feet = 1250; cxp = WXY[0] + (540 - WXY[0]) * q; cyp = WXY[1] + (feet - WXY[1]) * q
        img.alpha_composite(vf2, (int(cxp - vf2.width / 2), int(cyp - vf2.height * (78 / 92))))
        fsw = min(80, int(860 / (len(NAME[WANT]) + 6)))
        text_layer(img, [(540, 800, NAME[WANT] + ' WINS!', fsw, COL[WANT], 10, int(255 * a_)),
                         (540, feet + 40, 'DID YOUR GUIDE WIN?', 34, (255, 255, 255), 7, int(255 * min(1, max(0, u - 0.12) / 0.2)))])
    if t >= T_CARD: roster(img, t)
    img.alpha_composite(HOOK)
    if STILLS: img.convert('RGB').save(f'st_{t:.2f}.png')
    else: wr.write(img)
if wr: wr.close()
if STILLS: sys.exit()
out_ev = []; last = -9
for (th, g, k) in sorted(CT, key=lambda z: z[0]):
    if k is None and th - last > 0.45 and th < T_WIN: out_ev.append((round(th, 3), 'reeltick_8bit')); last = th
for e in EV:
    if e[1] == 'crack': out_ev.append((round(e[0], 3), 'brick_8bit'))
    elif e[1] == 'break': out_ev += [(round(e[0], 3), 'crunch_loud'), (round(e[0], 3), 'crunch_loud'), (round(e[0] + 0.02, 3), 'brick_8bit')]
    elif e[1] == 'pick': out_ev += [(round(e[0], 3), 'powerup_8bit'), (round(e[0], 3), 'powerup_8bit')]
    elif e[1] == 'out':
        out_ev += [(round(e[0], 3), 'punch' if e[3] == 'hit' else 'squish'), (round(e[0], 3), 'ko_hit'), (round(e[0], 3), 'ko_hit'), (round(e[0] + 0.03, 3), 'buzz_loud')]
out_ev += [(round(T_WIN, 3), 'win_sting'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(e for e in out_ev if e[0] < T_END - 0.1)
json.dump({'events': out_ev, 'end': T_END}, open('m01_events.json', 'w'), indent=1)
print('done', round(T_END, 2), NF)
