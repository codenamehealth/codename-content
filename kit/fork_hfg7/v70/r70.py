# #70 Choose your path: Bennett "change to 3 guides riding a minecart down".
# Rebuilt from fork_sz70/v70/r70.py: 3 guides (Cyrus, Rayleigh, Joy) each ride a front-view minecart (PixelLab, 4x) down
# their own numbered track; wheels sit on the rails (track gauge widened to the cart's wheel spacing), guides at 4x
# visible from the waist up inside the cart. Same mine, same mapping 1->TREASURE, 2->CHARM, 3->SLIMED.
import sys, os; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer, hook_fade
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import math, random
PREVIEW = len(sys.argv) > 1
G = SP + 'fork_a7/gen/'
LW0 = 4700; DY = 240; LW = LW0 + DY
HS = 2; w2, h2 = W // HS, LW // HS
T = wang(G + 'cave_meta.json', G + 'cave_sheet.png')
rng = random.Random(7)
KX = 0.88
def TX(x): return 478 + (x - 540) * KX
def TXh(x): return TX(x * HS) / HS
GC, GR = w2 // 32 + 2, h2 // 32 + 2
def lowc(i, j):
    x = i * 32 - 16; jj = j - DY // HS // 32
    edge = 50 + 22 * math.sin(jj * 0.55) + 14 * math.sin(jj * 1.7 + 1)
    redge = w2 - (50 + 22 * math.sin(jj * 0.47 + 2) + 14 * math.sin(jj * 1.3))
    return TXh(edge) < x < TXh(redge)
CORN = [[lowc(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
world = Image.new('RGBA', (w2, h2), (20, 16, 14, 255))
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1]); tl = T[key]
        if all(key) or not any(key):
            if (i * 7 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
            if (i + j * 5) % 3 == 0: tl = tl.transpose(Image.FLIP_TOP_BOTTOM)
        world.alpha_composite(tl, (i * 32 - 16, j * 32))
# ---------- three tracks (track colour = rider's guild colour)
COL = [(240, 128, 40), (150, 92, 225), (72, 196, 96)]      # 1 Cyrus orange, 2 Rayleigh purple, 3 Joy green
RIDER = ['cyrus', 'ray', 'joy']
Y0, Y1 = (760 + DY) // HS, (LW - 1500) // HS
SX = [200 // HS, 540 // HS, 880 // HS]; EX = [220 // HS, 540 // HS, 860 // HS]   # wider so 4x carts never touch side by side
PERM = [2, 0, 1]                    # start i -> end PERM[i]  (1->TREASURE, 2->CHARM, 3->SLIMED, unchanged)
WIG = 0.7
def xpath0(i, y):
    s = (y - Y0) / (Y1 - Y0); s = max(0, min(1, s)); base = SX[i] + (EX[PERM[i]] - SX[i]) * (s * s * (3 - 2 * s))
    env = math.sin(math.pi * s) ** 0.8
    wig = WIG * (150 * math.sin(2 * math.pi * (1.6 + 0.35 * i) * s + i * 2.1) + 60 * math.sin(2 * math.pi * 3.7 * s + i * 1.3))
    return max(70, min(w2 - 70, base + env * wig / HS))
def xpath(i, y): return TXh(xpath0(i, y))
YS, YE = Y0 - 140 // HS, Y1 + 70 // HS          # track start / end (half res)
def trackx_full(i, yf):                          # full-res x of track i at full-res y
    return xpath(i, yf / HS) * HS
PTS = [[(xpath(i, y), y) for y in range(YS, YE + 1, 1)] for i in range(3)]
def resample(pts, step):
    out = [pts[0]]; acc = 0
    for a, b in zip(pts, pts[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= step: out.append(b); acc = 0
    return out
GAUGE = 28        # half-res rail offset = cart wheel spacing (4x cart: wheels +-56px full res)
trk = Image.new('RGBA', (w2, h2), (0, 0, 0, 0)); td = ImageDraw.Draw(trk)
def draw_track(i):
    pts = resample(PTS[i], 1.0); c = COL[i]; dark = tuple(int(v * 0.55) for v in c)
    td.line(pts, fill=(12, 8, 6, 150), width=96)
    for k in range(0, len(pts) - 2, 12):
        (x0, y0), (x1, y1) = pts[k], pts[min(len(pts) - 1, k + 2)]
        tx, ty = x1 - x0, y1 - y0; L = math.hypot(tx, ty) or 1; nx, ny = -ty / L, tx / L; ux, uy = tx / L, ty / L
        hw, hl = 40, 4
        quad = [(x0 + nx * hw + ux * hl, y0 + ny * hw + uy * hl), (x0 - nx * hw + ux * hl, y0 - ny * hw + uy * hl),
                (x0 - nx * hw - ux * hl, y0 - ny * hw - uy * hl), (x0 + nx * hw - ux * hl, y0 + ny * hw - uy * hl)]
        td.polygon(quad, fill=c + (255,), outline=dark + (255,))
    for side in (-1, 1):
        rail = []
        for k in range(0, len(pts) - 1):
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]; L = math.hypot(x1 - x0, y1 - y0) or 1
            rail.append((x0 - (y1 - y0) / L * GAUGE * side, y0 + (x1 - x0) / L * GAUGE * side))
        td.line(rail, fill=(40, 38, 48, 255), width=7); td.line(rail, fill=(168, 168, 182, 255), width=5)
        td.line([(x, y - 1) for x, y in rail], fill=(230, 230, 240, 255), width=1)
for i in (0, 1, 2): draw_track(i)
world.alpha_composite(trk)
# buffer stops at the track ends (wooden beam with a red/white plate across both rails)
wd = ImageDraw.Draw(world)
for i in range(3):
    ex = xpath(i, YE); ey = YE
    wd.rectangle([ex - 46, ey - 4, ex + 46, ey + 10], fill=(96, 60, 32), outline=(40, 24, 14))
    for q in range(-46, 46, 16): wd.rectangle([ex + q, ey - 2, ex + q + 7, ey + 8], fill=(220, 50, 40))
    wd.rectangle([ex - 46, ey - 4, ex + 46, ey - 3], fill=(150, 104, 60))
# ---------- side props (crystals, lanterns on posts), as before
def pick(d, i): return crop(Image.open(f'{G}{d}/{i:02d}.png').convert('RGBA'))
CRY = [pick('crystal', k) for k in (0, 9, 19, 22)]; LAN = [pick('lantern', k) for k in (2, 6, 16)]
for j in range(0, h2, 150):
    for side in (0, 1):
        x = (22 + rng.randint(0, 20)) if side == 0 else (w2 - 22 - rng.randint(0, 20)); y = j + rng.randint(0, 120)
        if y < 300 // HS: continue
        im = rng.choice(CRY + LAN); world.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
WORLD = up(world, HS)
# ---------- sprites
CART = up(Image.open(SP + 'fork_c6/v70/gen/cartfront/00.png').convert('RGBA'), 4)     # PixelLab front-view cart, wheels at x 18.5/46.5, contact row 61
CW = CART.width; CONTACT = 61 * 4 + 2; RIM = 16 * 4
IDL = {g: idle(g, 4) for g in RIDER}
VIC = {g: [up(f.resize((92, 92), Image.NEAREST), 4) for f in gif_frames(A + {'cyrus': 'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', 'ray': 'vic_victoryPose_1.gif', 'joy': 'vic_Victory_Pose.gif'}[g])] for g in RIDER}   # same 920->92 canvas and 4x as the idle, so size and feet match
GCX = {'cyrus': 184, 'ray': 196, 'joy': 196}             # body centre x in the 368px idle canvas
SL = slime_frames(5)
DRG = gif_frames(A + 'dragon.gif', h=300)
sys.path.insert(0, SP + 'fork_c7'); from degold import dragon_gummy
DRG = dragon_gummy([f.convert('RGBA') for f in DRG], int(os.environ.get('DYT', '186')), 1)   # recut: gold-coin hoard -> pile of the four gummies (no coins anywhere)
JAR = up(crop(Image.open(A + 'jar_acv.png').convert('RGBA')), 0.55)
GUMI = {k: gummy(k, 2) for k in GUMK}
def medal(i):
    m = Image.new('RGBA', (76, 76), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
    d.ellipse([2, 2, 73, 73], fill=COL[i] + (255,), outline=(255, 255, 255, 255), width=5)
    ctext(d, 38, 20, str(i + 1), F(36), (255, 255, 255), 5); return m
MED = [medal(i) for i in range(3)]
# ---------- timeline
YSTART = YS * HS + 120          # wheel contact y at the start (full res)
YEND = YE * HS - 14             # stop just before the buffer
DEP = [float(v) for v in os.environ.get('DEP', '1.04,0.1,0.54').split(',')]         # Rayleigh leaves first, then Joy, Cyrus last (spaced so carts never touch where tracks meet)
ARR = [float(v) for v in os.environ.get('ARR', '5.74,5.31,5.52').split(',')]
REV = [7.1, 5.7, 6.4]   # recut: ride compressed x0.62 (same paths/spacing), reveals 0.7s apart from 5.7s   # reveal (stamp + reaction) per rider, one at a time after they pull in: CHARM 8.9, SLIMED 9.6, TREASURE 10.3
       # arrivals: CHARM 8.45, SLIMED 9.15, TREASURE 9.85 (one stamp at a time)
def ease(u):
    # quick start (0.12 of the run), cruise, soft brake (last 0.14)
    u = max(0, min(1, u)); a, b = 0.12, 0.14; v = 1 / (1 - a / 2 - b / 2)
    if u < a: return v * u * u / (2 * a)
    if u < 1 - b: return v * (a / 2 + (u - a))
    r = 1 - u; return 1 - v * r * r / (2 * b)
def cart_y(i, t): return YSTART + (YEND - YSTART) * ease((t - DEP[i]) / (ARR[i] - DEP[i]))
PRIZE_X = [TX(EX[0] * HS), TX(EX[1] * HS), TX(EX[2] * HS)]
LABEL = ['SHIELD', 'SLIMED', 'HOARD']
PY = YEND + 60                  # prize tops (full-res world)
CAM_END = YEND - 920            # final camera: carts stop at screen y920, prizes y~1000-1300
def cam_target(t):
    ys = [cart_y(i, t) for i in range(3)]
    return max(0, min(CAM_END, min(ys) - 920))    # last cart pinned at screen y920 (its rider's head clears the hook)
DUR = 9.4; T_HOOKB = 7.8; T_LOOP = DUR - 0.2   # recut: end hold 1.4s, last 0.2s = opening state (loop)
CAMS = []; c = 0
for f in range(int(DUR * FPS)):
    tg = cam_target(f / FPS); c = tg if f == 0 else c + (tg - c) * 0.3; CAMS.append(c)
HOOK_A, HB = hook_fade(['CHOOSE', 'YOUR PATH'], accent=1)   # hfg7: soft fade; 'PICK 1, 2 OR 3' cut (the hook is the ask, carts carry 1-3)
HOOK_B, _ = hook_fade(['WHAT DID', 'YOU GET?'], accent=1)   # end question replaces the hook in the same fade
DIM = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(DIM)
for yy in range(1440, H): _d.line([(0, yy), (W, yy)], fill=(10, 6, 14, int(min(150, (yy - 1440) * 1.5))))
STAMP = {0: ('SHIELD!', (120, 255, 140)), 1: ('SLIMED!', (150, 255, 60)), 2: ('GUMMY HOARD!', (255, 214, 60))}   # by prize index
ARRP = {PERM[i]: (REV[i], i) for i in range(3)}   # prize index -> (arrival time, rider)
def draw_cart(img, i, t, cy):
    yb = cart_y(i, t); moving = DEP[i] < t < ARR[i]
    bob = (4 if (int(t * 15) + i) % 2 else 0) if moving else 0
    x = trackx_full(i, yb); sy = yb - cy
    if sy < -400 or sy > H + 300: return
    layer(img, lambda d: d.ellipse([x - 112, sy - 18, x + 112, sy + 14], fill=(0, 0, 0, 110)))
    top = int(sy - CONTACT - bob); left = int(x - CW / 2)
    img.alpha_composite(CART, (left, top))
    g = RIDER[i]; arrived = t >= REV[i] and PERM[i] != 1
    if arrived: fr = VIC[g][int((t - REV[i]) * 8) % len(VIC[g])]; fx = int(x - GCX[g]); fy = top + RIM + 120 - 312
    else:
        fr = IDL[g][int(t * 8 + i * 3) % len(IDL[g])]; fx = int(x - GCX[g]); fy = top + RIM + 120 - 312
    rim = top + RIM + 4 - (bob and 0)
    keep = rim - fy
    if keep > 0: img.alpha_composite(fr.crop((0, 0, fr.width, min(fr.height, keep))), (fx, fy))
    img.alpha_composite(MED[i], (int(x - 38), top + 112))
    if PERM[i] == 0 and t >= REV[i]:   # ACV SHIELD: green bubble around the rider
        u = min(1, (t - REV[i]) / 0.2); r = int(150 * (0.6 + 0.4 * u)); cxb, cyb = int(x), int(top + RIM - 40)
        L = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(L)
        rx = int(r * 0.84); cxb = max(cxb, 72 + rx)
        d.ellipse([cxb - rx, cyb - r, cxb + rx, cyb + r], fill=(110, 240, 120, 55), outline=(150, 255, 160, 230), width=7)
        d.arc([cxb - rx + 22, cyb - r + 26, cxb + rx - 22, cyb + r - 26], 200, 250, fill=(240, 255, 240, 220), width=8)
        img.alpha_composite(L)
    if moving and t - DEP[i] > 0.15:   # wheel sparks
        rr = random.Random(int(t * 30) * 7 + i)
        L = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(L)
        for wxo in (-56, 56):
            for _ in range(3):
                px, py = x + wxo + rr.uniform(-10, 10), sy - 8 - rr.uniform(0, 26); d.rectangle([px, py, px + 4, py + 4], fill=(255, 220, 120, 230))
        img.alpha_composite(L)
wr = None if PREVIEW else Writer('v70_noaudio.mp4'); ev = []
NF = int(DUR * FPS); minsep = 1e9
frames_to_check = [int(x * FPS) for x in [float(v) for v in os.environ.get('PV', '0.2,3,6,7.5,8.6,9.3,10,11.5').split(',')]]
for f in range(NF):
    t = f / FPS; cy = int(CAMS[f])
    if t >= T_LOOP: t = 0.0; cy = int(CAMS[0])   # cut back to the opening state
    # overlap check (cart boxes incl. rider heads)
    for a in range(3):
        for b in range(a + 1, 3):
            ya, yb_ = cart_y(a, t), cart_y(b, t); xa, xb = trackx_full(a, ya), trackx_full(b, yb_)
            if abs(xa - xb) < 228 and abs(ya - yb_) < minsep: minsep = abs(ya - yb_); worst = (round(t, 2), a, b, round(ya), round(xa), round(xb))
    if PREVIEW and f not in frames_to_check: continue
    img = WORLD.crop((0, cy, W, cy + H)).copy()
    py = PY - cy
    # prizes
    if py < H + 400:
        for k, x in enumerate(PRIZE_X):
            ta, rider = ARRP[k]; hit = t >= ta
            if k == 0:
                bounce = int(-30 * math.sin(min(1, (t - ta) / 0.35) * math.pi)) if 0 <= t - ta < 0.35 else 0
                img.alpha_composite(JAR, (int(x - JAR.width / 2), int(py - 20 + bounce)))
                for q in range(3):
                    gx, gy = int(x - 70 + q * 50), int(py + JAR.height - 30 + 6 * math.sin(t * 4 + q) + bounce)
                    img.alpha_composite(GUMI['acv'], (gx, gy))
                    if int(t * 4 + q) % 3 == 0:   # gummy shine
                        layer(img, lambda dd, gx=gx, gy=gy: (dd.rectangle([gx + 12, gy + 10, gx + 18, gy + 16], fill=(255, 255, 255, 230)), dd.rectangle([gx + 20, gy + 6, gx + 23, gy + 9], fill=(255, 255, 255, 200))))
                # hfg7: ACV GUMMY tag cut (consistency rule, #037)
            elif k == 1:
                sf = SL[int(t * 8) % len(SL)]; hop = 0
                if 0 <= t - ta < 0.45: hop = int(-120 * math.sin((t - ta) / 0.45 * math.pi))
                img.alpha_composite(sf, (int(x - sf.width / 2), int(py + 260 - 62 * 5 + hop)))
            else:
                df = DRG[int(t * 6) % len(DRG)]; img.alpha_composite(df, (int(x - df.width / 2 + 10), int(py)))
            # hfg7: '?' plates and the SHIELD / SLIMED / HOARD labels under the prizes cut (the prizes and the big stamps say it)
    # carts: farther (smaller y) first
    for i in sorted(range(3), key=lambda i: cart_y(i, t)): draw_cart(img, i, t, cy)
    # slime splat on Joy's cart (track 3 -> SLIMED)
    tj = REV[2] - 0.3
    if t >= tj + 0.3:
        yb = cart_y(2, t); x = trackx_full(2, yb); sy = yb - cy; top = sy - CONTACT
        L = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(L); rr = random.Random(5)
        blobs = [(x + rr.uniform(-105, 105), top + RIM + rr.uniform(-6, 26)) for _ in range(9)]            # goo along the rim
        blobs += [(x + s_ * rr.uniform(62, 100), top + RIM - rr.uniform(20, 90)) for s_ in (-1, 1) for _ in range(3)]   # on the shoulders/sides
        blobs += [(x + rr.uniform(-40, 40), top + RIM - 130 - rr.uniform(0, 10)) for _ in range(2)]          # on top of the hair (face stays clear)
        for (px, pyy) in blobs:
            r = rr.uniform(10, 22)
            d.ellipse([px - r, pyy - r, px + r, pyy + r], fill=(120, 220, 70, 235), outline=(40, 110, 30, 255), width=3)
        for _ in range(7):
            px = x + rr.uniform(-95, 95); L0 = rr.uniform(30, 70) * min(1, (t - tj - 0.3) / 0.6)
            d.rectangle([px - 5, top + RIM, px + 5, top + RIM + L0], fill=(120, 220, 70, 235))
        img.alpha_composite(L)
    # big stamp, one at a time (each until the next arrival)
    order = sorted(ARRP.items(), key=lambda kv: kv[1][0])
    for n, (k, (ta, rider)) in enumerate(order):
        tn = order[n + 1][1][0] if n + 1 < len(order) else T_HOOKB
        if ta <= t < tn:
            u = t - ta; sc = 1 + 0.35 * max(0, 1 - u / 0.18)
            text_layer(img, [(478, 1392 - int(20 * (sc - 1)), STAMP[k][0], int((64 if len(STAMP[k][0]) > 10 else 68) * sc), STAMP[k][1], 10, 255)])
            if u < 0.5 / FPS: ev.append((round(ta, 3), {0: 'powerup_8bit', 1: 'squish', 2: 'victory'}[k]))
    for i in range(3):
        if abs(t - DEP[i]) < 0.5 / FPS: ev.append((round(DEP[i], 3), 'whoosh_8bit'))
    if t >= T_HOOKB and not any(e[1] == 'ding_8bit' for e in ev): ev.append((T_HOOKB, 'ding_8bit'))
    if t >= T_HOOKB:
        pass   # hfg7: COMMENT 1, 2 OR 3 plate cut (caption asks)
    img.alpha_composite(DIM)
    img.alpha_composite(HOOK_B if T_HOOKB <= t < T_LOOP else HOOK_A)
    if PREVIEW: img.convert('RGB').resize((540, 960)).save(f'pv_{t:05.2f}.png'); continue
    wr.write(img)
if wr: wr.close()
print('min y-sep when x-overlapping', round(minsep), worst, 'HB', HB, 'CAM_END', CAM_END, 'cam start', round(CAMS[0]))
for tt in (0, 2, 4, 6, 7, 8, 8.5, 8.9, 9.6, 10.3):
    f = min(NF - 1, int(tt * FPS)); print(tt, [round(cart_y(i, tt) - CAMS[f]) for i in range(3)], 'py', round(PY - CAMS[f]))
if not PREVIEW: json.dump({'events': ev}, open('v70_ev.json', 'w')); print('events', ev)
