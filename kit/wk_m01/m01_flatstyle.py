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
moon = Image.open(A + 'bg_moon.gif'); BG = []
for i in range(0, moon.n_frames, 2):
    moon.seek(i); f_ = moon.convert('RGB').resize((3413, 1920), Image.LANCZOS).crop((1166, 0, 1166 + W, H)).filter(ImageFilter.GaussianBlur(6))
    BG.append(ImageEnhance.Brightness(f_).enhance(0.42).convert('RGBA'))
def stone_tile(tone, seed):
    rr = random.Random(seed); n_ = (U + 1) // 2; t_ = Image.new('RGBA', (n_, n_), tone + (255,)); px = t_.load()
    gr = tuple(int(v * 0.85) for v in tone); hi = tuple(min(255, int(v * 1.06)) for v in tone)
    for i in range(n_): px[i, n_ - 1] = gr + (255,); px[n_ - 1, i] = gr + (255,); px[i, 0] = hi + (255,); px[0, i] = hi + (255,)
    for n in range(18):
        x, y = rr.randint(2, n_ - 3), rr.randint(2, n_ - 3); px[x, y] = (tuple(int(v * 0.92) for v in tone) if n % 2 else tuple(min(255, int(v * 1.04)) for v in tone)) + (255,)
    return up(t_, 2).crop((0, 0, U, U))
TONES = [(226, 199, 152), (216, 187, 141)]
def floorish(r, c): return 0 <= r < M.ROWS and 0 <= c < M.COLS and M.MAP[r][c] != '#'
# ---------------- static layer
MZ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(MZ)
for r in range(M.ROWS):
    for c in range(M.COLS):
        x0, y0 = X0 + c * U, Y0 + r * U
        if M.MAP[r][c] == '#':
            if any(floorish(r + dr, c + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                d.rectangle([x0, y0, x0 + U - 1, y0 + U - 1], fill=(40, 36, 54, 255))
        elif M.MAP[r][c] == 'E':
            for i in range(2):
                for j in range(2):
                    h_ = U // 2; d.rectangle([x0 + j * h_, y0 + i * h_, x0 + (j + 1) * h_ - 1 + (U - 2 * h_) * j, y0 + (i + 1) * h_ - 1 + (U - 2 * h_) * i], fill=(236, 236, 236, 255) if (i + j) % 2 == 0 else (30, 30, 36, 255))
        else:
            MZ.alpha_composite(stone_tile(TONES[(r + c) % 2], r * 97 + c), (x0, y0))
d = ImageDraw.Draw(MZ)
for r in range(M.ROWS):
    for c in range(M.COLS):
        if M.MAP[r][c] != '#': continue
        x0, y0 = X0 + c * U, Y0 + r * U
        if floorish(r + 1, c):
            MZ.alpha_composite(BRICK.crop(((c % 2) * 40, 0, (c % 2) * 40 + U, 14)), (x0, y0 + U - 14))
            d.rectangle([x0, y0 + U - 16, x0 + U - 1, y0 + U - 15], fill=(150, 146, 168, 255))
        rim = (118, 114, 140, 255)
        if floorish(r - 1, c): d.rectangle([x0, y0, x0 + U - 1, y0 + 2], fill=rim)
        if floorish(r, c - 1): d.rectangle([x0, y0, x0 + 2, y0 + U - 1], fill=rim)
        if floorish(r, c + 1): d.rectangle([x0 + U - 3, y0, x0 + U - 1, y0 + U - 1], fill=rim)
ao = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ao)
for r in range(1, M.ROWS):
    for c in range(M.COLS):
        if M.MAP[r][c] != '#' and M.MAP[r - 1][c] == '#':
            for k in range(4): ad.rectangle([X0 + c * U, Y0 + r * U + 2 * k, X0 + c * U + U - 1, Y0 + r * U + 2 * k + 1], fill=(10, 6, 20, 80 - k * 18))
MZ.alpha_composite(ao)
def brick_img(col, hp):
    im = Image.new('RGBA', (U, U)); bt = tint(BRICK, col)
    im.alpha_composite(bt.crop((0, 0, U, U)) if bt.width >= U and bt.height >= U else bt.resize((U, U), Image.NEAREST))
    dd = ImageDraw.Draw(im)
    dd.rectangle([0, 0, U - 1, 3], fill=tuple(min(255, int(v * 1.3)) for v in col) + (255,)); dd.rectangle([0, 0, U - 1, U - 1], outline=(18, 12, 24, 255), width=2)
    if hp == 1:
        dd.line([(10, 0), (16, 12), (12, 22), (22, 32), (20, 45)], fill=(14, 8, 20, 255), width=3); dd.line([(16, 12), (30, 16), (36, 26)], fill=(14, 8, 20, 255), width=2)
        dd.rectangle([30, 2, 40, 9], fill=(22, 16, 30, 255))
    return im
WEDGE = Image.new('RGBA', (W, H), (0, 0, 0, 0)); wd = ImageDraw.Draw(WEDGE)        # wall edges stay readable over the flood
for r in range(M.ROWS):
    for c in range(M.COLS):
        if M.MAP[r][c] != '#': continue
        x0, y0 = X0 + c * U, Y0 + r * U; ec = (150, 146, 176, 255)
        if floorish(r - 1, c): wd.rectangle([x0, y0, x0 + U - 1, y0 + 2], fill=ec)
        if floorish(r + 1, c): wd.rectangle([x0, y0 + U - 3, x0 + U - 1, y0 + U - 1], fill=ec)
        if floorish(r, c - 1): wd.rectangle([x0, y0, x0 + 2, y0 + U - 1], fill=ec)
        if floorish(r, c + 1): wd.rectangle([x0 + U - 3, y0, x0 + U - 1, y0 + U - 1], fill=ec)
BIMG = {}
for k, b in M.BRK.items():
    for hp in (1, 2): BIMG[(b['col'], hp)] = brick_img(b['col'], hp)
# ---------------- shadow
SW_, SH_ = M.COLS * U, M.ROWS * U
NZ = Image.effect_noise((SW_ // 4, SH_ // 4), 60).resize((SW_, SH_), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
NZa = np.array(NZ).astype(float) / 255.0
SHC = np.zeros((SH_, SW_, 4), np.uint8)
SHC[..., 0] = (44 + 26 * NZa).astype(np.uint8); SHC[..., 1] = (30 + 16 * NZa).astype(np.uint8); SHC[..., 2] = (100 + 46 * NZa).astype(np.uint8); SHC[..., 3] = 250
SHADOW_TEX = Image.fromarray(SHC)
EYES = [(r, c) for r in range(M.ROWS) for c in range(M.COLS) if M.MAP[r][c] != '#' and (r * 7 + c * 13) % 11 == 0]
def shadow_layer(t, prog):
    m = Image.new('L', (SW_, SH_), 0); md = ImageDraw.Draw(m); rims = []; full = set()
    for k, p in enumerate(prog):
        for (x0, y0, x1, y1) in M.seg_cover(k, p):
            md.rectangle([x0 - X0, y0 - Y0, max(x0 - X0, x1 - X0 - 1), max(y0 - Y0, y1 - Y0 - 1)], fill=255)
            sg = M.SEGS[k]
            if p < sg['len']:
                dd_ = sg['dir']
                if x1 - x0 < 4 or y1 - y0 < 4: continue
                rims.append([x0 - X0, y1 - Y0 - 3, x1 - X0 - 1, y1 - Y0 - 1] if dd_ == 'D' else [x0 - X0, y0 - Y0, x1 - X0 - 1, y0 - Y0 + 2] if dd_ == 'U' else
                            [x1 - X0 - 3, y0 - Y0, x1 - X0 - 1, y1 - Y0 - 1] if dd_ == 'R' else [x0 - X0, y0 - Y0, x0 - X0 + 2, y1 - Y0 - 1])
    L = Image.new('RGBA', (SW_, SH_), (0, 0, 0, 0)); L.paste(SHADOW_TEX, (int(6 * math.sin(t)), 0), m)
    dd = ImageDraw.Draw(L); ma = np.array(m)
    for b_ in rims: dd.rectangle(b_, fill=(175, 115, 255, 225))
    for (r, c) in EYES:
        ex, ey = c * U + 13, r * U + 17
        if ma[min(SH_ - 1, ey - 8), min(SW_ - 1, ex - 6)] == 0 or ma[min(SH_ - 1, ey + 20), min(SW_ - 1, ex + 30)] == 0: continue
        if (int(t * 1.7 + r * 3 + c) % 9) == 0: dd.rectangle([ex, ey + 4, ex + 20, ey + 6], fill=(230, 220, 255, 230))
        else: dd.rectangle([ex, ey, ex + 5, ey + 8], fill=(240, 235, 255, 245)); dd.rectangle([ex + 15, ey, ex + 20, ey + 8], fill=(240, 235, 255, 245))
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
    img = BG[int(t * 5) % len(BG)].copy(); img.alpha_composite(MZ)
    for k, b in M.BRK.items():
        if hp[k] > 0: img.alpha_composite(BIMG[(b['col'], min(2, hp[k]))], (X0 + k[1] * U, Y0 + k[0] * U))
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
