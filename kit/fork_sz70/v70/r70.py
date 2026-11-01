import sys, os; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import math, random
G = SP + 'fork_a7/gen/'
LW0 = 4700; DY = 240           # world shifted down DY px so the start sits under the hook
LW = LW0 + DY
HS = 2                          # half-res build, upscaled 2x
w2, h2 = W // HS, LW // HS
T = wang(G + 'cave_meta.json', G + 'cave_sheet.png')
rng = random.Random(7)
KX = 0.88
def TX(x): return 478 + (x - 540) * KX          # full-res x map
def TXh(x): return TX(x * HS) / HS               # half-res x map
# ---------- floor: dirt band with rocky walls (corner grid at 32px half-res)
GC, GR = w2 // 32 + 2, h2 // 32 + 2
def lowc(i, j):
    x = i * 32 - 16; y = j * 32
    jj = j - DY // HS // 32
    edge = 50 + 22 * math.sin(jj * 0.55) + 14 * math.sin(jj * 1.7 + 1)
    redge = w2 - (50 + 22 * math.sin(jj * 0.47 + 2) + 14 * math.sin(jj * 1.3))
    return TXh(edge) < x < TXh(redge)
CORN = [[lowc(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
world = Image.new('RGBA', (w2, h2), (20, 16, 14, 255))
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1])
        tl = T[key]
        if all(key) or not any(key):
            if (i * 7 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
            if (i + j * 5) % 3 == 0: tl = tl.transpose(Image.FLIP_TOP_BOTTOM)
        world.alpha_composite(tl, (i * 32 - 16, j * 32))
# ---------- three mine-rail tracks
COL = [(222, 72, 60), (150, 92, 225), (72, 196, 96)]
Y0, Y1 = (760 + DY) // HS, (LW - 1500) // HS
SX = [300 // HS, 540 // HS, 780 // HS]; EX = [270 // HS, 540 // HS, 810 // HS]
PERM = [2, 0, 1]                    # start i -> end PERM[i]
def xpath(i, y): return TXh(xpath0(i, y))
def xpath0(i, y):
    s = (y - Y0) / (Y1 - Y0); base = SX[i] + (EX[PERM[i]] - SX[i]) * (s * s * (3 - 2 * s))
    env = math.sin(math.pi * s) ** 0.8
    wig = 150 * math.sin(2 * math.pi * (1.6 + 0.35 * i) * s + i * 2.1) + 60 * math.sin(2 * math.pi * 3.7 * s + i * 1.3)
    return max(70, min(w2 - 70, base + env * wig / HS * 1.0))
PTS = []
for i in range(3):
    pts = [(TXh(SX[i]), Y0 - 90 // HS)] + [(xpath(i, y), y) for y in range(Y0, Y1 + 1, 2)] + [(TXh(EX[PERM[i]]), Y1 + 120 // HS)]
    PTS.append(pts)
def resample(pts, step):
    out = [pts[0]]; acc = 0
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1]); acc += d
        if acc >= step: out.append(b); acc = 0
    return out
trk = Image.new('RGBA', (w2, h2), (0, 0, 0, 0)); td = ImageDraw.Draw(trk)
def draw_track(i):
    pts = resample(PTS[i], 1.0); c = COL[i]; dark = tuple(int(v * 0.55) for v in c)
    td.line(pts, fill=(12, 8, 6, 150), width=56)
    for k in range(0, len(pts) - 2, 11):
        (x0, y0), (x1, y1) = pts[k], pts[min(len(pts) - 1, k + 2)]
        tx, ty = x1 - x0, y1 - y0; L = math.hypot(tx, ty) or 1; nx, ny = -ty / L, tx / L; ux, uy = tx / L, ty / L
        hw, hl = 23, 4
        quad = [(x0 + nx * hw + ux * hl, y0 + ny * hw + uy * hl), (x0 - nx * hw + ux * hl, y0 - ny * hw + uy * hl),
                (x0 - nx * hw - ux * hl, y0 - ny * hw - uy * hl), (x0 + nx * hw - ux * hl, y0 + ny * hw - uy * hl)]
        td.polygon(quad, fill=c + (255,), outline=dark + (255,))
    for side in (-1, 1):
        rail = []
        for k in range(0, len(pts) - 1):
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]; L = math.hypot(x1 - x0, y1 - y0) or 1
            rail.append((x0 - (y1 - y0) / L * 14 * side, y0 + (x1 - x0) / L * 14 * side))
        td.line(rail, fill=(40, 38, 48, 255), width=6); td.line(rail, fill=(168, 168, 182, 255), width=4)
        td.line([(x, y - 1) for x, y in rail], fill=(230, 230, 240, 255), width=1)
# draw tracks: order shuffles visually per crossing by drawing in segments alternating
for i in (0, 1, 2): draw_track(i)
world.alpha_composite(trk)
# arrow tips + start signs (half res)
wd = ImageDraw.Draw(world)
for i in range(3):
    ex = TXh(EX[PERM[i]]); ey = Y1 + 120 // HS
    wd.polygon([(ex - 26, ey - 6), (ex + 26, ey - 6), (ex, ey + 26)], fill=COL[i] + (255,), outline=(30, 20, 20, 255))
# ---------- props
def pick(d, i): return crop(Image.open(f'{G}{d}/{i:02d}.png').convert('RGBA'))
CRY = [pick('crystal', k) for k in (0, 9, 19, 22)] if os.path.isdir(G + 'crystal') else []
LAN = [pick('lantern', k) for k in (2, 6, 16)] if os.path.isdir(G + 'lantern') else []
props = []
for j in range(0, h2, 150):
    for side in (0, 1):
        x = (22 + rng.randint(0, 20)) if side == 0 else (w2 - 22 - rng.randint(0, 20)); y = j + rng.randint(0, 120)
        if y < 300 // HS: continue
        im = rng.choice(CRY + LAN) if (CRY or LAN) else None
        if im: world.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2))); props.append((x, y, im))
# scattered gummies near the tracks
GUMS = []
for k in range(26):
    y = rng.randint(Y0 + 80, Y1 - 60); kind = rng.choice(['mush', 'acv', 'mel', 'cre', 'gold'])
    xs = [xpath0(i, y) for i in range(3)]
    for _ in range(20):
        x = rng.randint(60, w2 - 60)
        if min(abs(x - v) for v in xs) > 34: break
    if kind == 'gold': kind = ['mush', 'acv', 'mel', 'cre'][k % 4]   # no gold pickups
    GUMS.append((TX(x * HS), y * HS, kind, rng.uniform(0, 6)))
WORLD = up(world, HS)
# light vignette pools around lanterns
# ---------- sprites
CART = up(pick('minecart', 2), 3) if os.path.isdir(G + 'minecart') else None
HOL = idle('hollow', 3)
SL = slime_frames(5)
DRG = gif_frames(A + 'dragon.gif', h=300)
JAR = up(crop(Image.open(A + 'jar_acv.png').convert('RGBA')), 0.55)
GUMI = {k: gummy(k, 2) for k in GUMK}
ENDY = (Y1 + 120 // HS) * HS + 150
PRIZE_X = [TX(EX[0] * HS), TX(EX[1] * HS), TX(EX[2] * HS)]
LABEL = ['CHARM', 'SLIMED', 'TREASURE']
# ---------- timeline
DUR = 17.2; T_SCROLL0, T_SCROLL1 = 2.6, 13.6
CAM_END = LW0 - H
def cam(t):
    if t < T_SCROLL0: return 0
    u = min(1, (t - T_SCROLL0) / (T_SCROLL1 - T_SCROLL0)); u = u * u * (3 - 2 * u)
    return u * CAM_END
HOOK_A, HB = hook_layer(['CHOOSE YOUR', 'PATH'], accent=1, sub='FOLLOW IT WITH YOUR EYES')
HOOK_B, _ = hook_layer(['WHAT DID', 'YOU GET?'], accent=1, sub='COMMENT YOUR NUMBER')
# soft dim below the safe zone so the eye stays on the in-zone track
DIM = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(DIM)
for yy in range(1440, H): _d.line([(0, yy), (W, yy)], fill=(10, 6, 14, int(min(150, (yy - 1440) * 1.5))))
wr = Writer('v70_noaudio.mp4'); ev = []
NF = int(DUR * FPS)
for f in range(NF):
    t = f / FPS; cy = int(cam(t))
    img = WORLD.crop((0, cy, W, cy + H)).copy()
    # gummies bob + sparkle
    for (gx, gy, kind, ph) in GUMS:
        sy = gy - cy
        if -60 < sy < H + 60:
            g = GUMI[kind]; b = int(4 * math.sin(t * 3 + ph))
            img.alpha_composite(g, (int(gx - g.width / 2), int(sy - g.height / 2 + b)))
    # start: hollow in minecart
    sy = 560 + DY - cy
    if sy > -300:
        hf = HOL[int(t * 8) % len(HOL)]
        img.alpha_composite(hf, (478 - hf.width // 2, sy - 78 * 3 + 30))
        if CART: img.alpha_composite(CART, (478 - CART.width // 2, sy - CART.height // 2 + 20))
        d = ImageDraw.Draw(img)
        for i in range(3):
            x = TX(SX[i] * HS); yy = Y0 * HS - 150 - cy
            layer(img, lambda dd, x=x, yy=yy, i=i: dd.ellipse([x - 34, yy - 34, x + 34, yy + 34], fill=COL[i] + (255,), outline=(255, 255, 255, 255), width=5))
            text_layer(img, [(x, yy - 16, str(i + 1), 34, (255, 255, 255), 4, 255)])
    # prizes
    py = ENDY - cy
    if py < H + 400:
        for k, x in enumerate(PRIZE_X):
            if k == 0:
                img.alpha_composite(JAR, (int(x - JAR.width / 2), int(py - 20)))
                gg = GUMI['acv']
                for q in range(3): img.alpha_composite(gg, (int(x - 70 + q * 50), int(py + JAR.height - 30 + 6 * math.sin(t * 4 + q))))
            elif k == 1:
                sf = SL[int(t * 8) % len(SL)]; img.alpha_composite(sf, (int(x - sf.width / 2), int(py + 260 - 62 * 5)))
            else:
                df = DRG[int(t * 6) % len(DRG)]; img.alpha_composite(df, (int(x - df.width / 2 + 10), int(py)))
            layer(img, lambda dd, x=x: dd.rounded_rectangle([x - 120, py + 300, x + 120, py + 352], 12, fill=(16, 12, 24, 220), outline=(255, 214, 60, 255), width=3))
            text_layer(img, [(x, py + 314, LABEL[k], 24, (255, 255, 255), 0, 255)])
    # header
    # countdown
    if t < T_SCROLL0:
        n = 3 - int(t / 0.65)
        txt = str(n) if n > 0 else 'START!'; col = (255, 255, 255) if n > 0 else (255, 214, 60)
        u = (t % 0.65) / 0.65; sz = int(110 - 30 * u) if n > 0 else 86
        text_layer(img, [(478, 1000 + DY - cy, txt, sz, col, 10, 255)])
        key = f'cd{n}'
        if not any(e[1].startswith('tick') and abs(e[0] - int(t / 0.65) * 0.65) < 0.01 for e in ev):
            ev.append((round(int(t / 0.65) * 0.65, 3), 'tick_8bit' if n > 0 else 'go_8bit'))
    if t >= T_SCROLL1 + 0.3:
        a = int(255 * min(1, (t - T_SCROLL1 - 0.3) / 0.4))
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_SCROLL1 + 0.3, 3), 'ding_8bit'))
    img.alpha_composite(DIM)
    img.alpha_composite(HOOK_B if t >= T_SCROLL1 + 0.3 else HOOK_A)
    wr.write(img)
wr.close()
# whoosh at scroll start
ev.append((T_SCROLL0, 'whoosh_8bit'))
json.dump(ev, open('v70_ev.json', 'w')); print('done', len(ev))
