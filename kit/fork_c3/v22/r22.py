import sys, math, json, random, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
import numpy as np
from PIL import ImageFilter
# #22 Choose your path A, B or C: content pass (Bennett: "overcooked. Static path, camera scrolls up so you see the journey like the
# original video, just more detailed"). The three vines are now fixed in place and several screens tall; the camera starts on the
# A/B/C start in Liza's forest clearing and scrolls up the whole journey into the night sky, ending on the three prizes.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1
MODE = sys.argv[2] if len(sys.argv) > 2 else 'render'
HOOK, HB = hook_layer(['CHOOSE YOUR PATH'], accent=0, sub='A, B OR C?')
HOOK2, HB2 = hook_layer(['WHAT DID YOU GET?'], accent=0, sub='COMMENT YOUR LETTER')
# ---------------- world geometry (world y grows downward; camera 0 = final view)
PCY = HB + 18 + 124                     # prize frame centres (final view, under the hook)
TOPY = PCY + 124 + 26                   # vine tops
SPAN = int(os.environ.get('SPAN', '3800'))
BOTY = TOPY + SPAN                      # A/B/C nodes
NODE_SCREEN0 = 1130                     # nodes' screen y in the opening view
CAM0 = BOTY - NODE_SCREEN0
WH = CAM0 + H
SX = [230, 490, 750]; PRX = [230, 490, 750]
PERM = [1, 2, 0]                        # A->prize1 (chest), B->prize2 (gold gummy), C->prize0 (mushroom jar); never revealed
COL = [((255, 205, 60), (150, 100, 10)), ((180, 110, 255), (80, 40, 140)), ((70, 225, 200), (20, 110, 100))]
XL, XR = 112, 868                       # vines stay inside the safe zone (incl. the lower-right button notch)
# ---------------- static paths
def make_paths(seed):
    rng = random.Random(seed); P = []
    n = 2400
    for i in range(3):
        x0, x1 = SX[i], PRX[PERM[i]]
        terms = [(rng.uniform(140, 230), rng.uniform(2.6, 4.2), rng.uniform(0, 6.28)), (rng.uniform(60, 120), rng.uniform(5.5, 8.5), rng.uniform(0, 6.28))]
        def xpre(s):
            env = min(1, s / 0.06, (1 - s) / 0.06) ** 1.5
            return x0 + (x1 - x0) * (3 * s * s - 2 * s ** 3) + sum(a * math.sin(2 * math.pi * fq * s + ph) for a, fq, ph in terms) * env
        cands = [0.14 + 0.02 * k for k in range(36)]
        cands = [c for c in cands if abs(xpre(c + 130 / SPAN) - 490) < 150]
        loops = []
        for c in rng.sample(cands, len(cands)):
            if all(abs(c - l) > 0.22 for l in loops): loops.append(c)
            if len(loops) == 2: break
        loops.sort()
        c = (XL + XR) / 2; hw = (XR - XL) / 2
        T_ = lambda x: c + hw * math.tanh((x - c) / hw)
        def xc(s):     # soft clamp, with the ends pinned exactly on the A/B/C node and the prize dot
            sm = s * s * (3 - 2 * s); return T_(xpre(s)) + (x0 - T_(x0)) * (1 - sm) + (x1 - T_(x1)) * sm
        bx = np.array([xc(k / n) for k in range(n + 1)]); by = np.array([BOTY - SPAN * k / n for k in range(n + 1)])
        ox = np.zeros(n + 1); oy = np.zeros(n + 1)
        for sL in loops:
            # a real loop in the path's own frame (tangent/normal at the loop), so it never shears into a kink
            k0, k1 = int(sL * n), int((sL + 300 / SPAN) * n); km = (k0 + k1) // 2
            tx, ty = bx[km + 3] - bx[km - 3], by[km + 3] - by[km - 3]; L = math.hypot(tx, ty); tx, ty = tx / L, ty / L
            nx, ny = -ty, tx
            if nx * (c - bx[km]) < 0: nx, ny = -nx, -ny
            b = 80
            for k in range(k0, k1 + 1):
                u = (k - k0) / (k1 - k0); th = 2 * math.pi * (u * u * (3 - 2 * u))     # eased phase: no cusp where the loop starts/ends
                ox[k] += tx * (-b * math.sin(th)) + nx * b * (1 - math.cos(th))
                oy[k] += ty * (-b * math.sin(th)) + ny * b * (1 - math.cos(th))
        pts = [(float(min(XR + 6, max(XL - 6, bx[k] + ox[k]))), float(by[k] + oy[k])) for k in range(n + 1)]
        P.append((pts, loops))
    return P
def score(P):
    # sample x by y on the loop-free parts; crossings per pair and near-parallel overlap
    ys = np.arange(TOPY + 60, BOTY - 60, 4)
    X = []
    for pts, _ in P:
        a = np.array(pts); order = np.argsort(a[:, 1]); X.append(np.interp(ys, a[order, 1], a[order, 0]))
    cross = []; bad = 0
    for i in range(3):
        for j in range(i + 1, 3):
            dx = X[i] - X[j]; cross.append(int(np.sum(np.sign(dx[1:]) != np.sign(dx[:-1]))))
            close = np.abs(dx) < 46; run = 0
            for c in close:
                run = run + 1 if c else 0
                if run * 4 > 70: bad += 1
    return cross, bad
if MODE == 'search':
    for sd in range(1, 80):
        P = make_paths(sd); c, b = score(P); print(sd, c, b)
    sys.exit()
PATHS = make_paths(SEED); print('seed', SEED, 'crossings/overlap', score(PATHS))
# ---------------- camera
T_ARR = float(os.environ.get('TARR', '13.4')); T_SWAP = T_ARR + 0.8; DUR = T_ARR + 3.4
def vprof(t):
    if t >= T_ARR: return 0.0
    a = 0.22 + 0.78 * min(1, t / 1.3)                      # already moving on frame 0
    d = min(1, (T_ARR - t) / 1.7); d = d * d * (3 - 2 * d)
    return a * d
_ts = np.arange(0, T_ARR + 1e-9, 1 / (FPS * 8)); _v = np.array([vprof(t) for t in _ts]); _cum = np.concatenate([[0], np.cumsum((_v[1:] + _v[:-1]) / 2) / (FPS * 8)])
_cum /= _cum[-1]
def cam(t): return CAM0 * (1 - np.interp(min(t, T_ARR), _ts, _cum))
print('scroll px', CAM0, 'cruise px/s', round(CAM0 / np.trapezoid(_v, _ts), 1))
# ---------------- world art (pre-rendered once)
rng = random.Random(5)
SKY = Image.new('RGBA', (W, WH), (0, 0, 0, 255)); sk = np.zeros((WH, W, 4), np.uint8)
yv = np.linspace(0, 1, WH)[:, None]
top, mid, bot = np.array([14, 10, 34]), np.array([34, 20, 62]), np.array([16, 36, 44])
c = np.where(yv < 0.55, top + (mid - top) * (yv / 0.55), mid + (bot - mid) * ((yv - 0.55) / 0.45))
q = (np.floor(c / 4) * 4).astype(np.uint8)                  # banded, pixel-art style gradient
sk[..., :3] = q[:, None, :].repeat(W, 1) if q.ndim == 2 else q; sk[..., 3] = 255
SKY = Image.fromarray(sk, 'RGBA')
sd = ImageDraw.Draw(SKY)
STARS = []
for _ in range(260):
    x, y = rng.uniform(0, W), rng.uniform(0, WH - 1500); s = rng.choice([3, 3, 3, 6]); STARS.append((x, y, s, rng.uniform(0, 6.28)))
    sd.rectangle([x, y, x + s, y + s], fill=(200, 200, 235, 255) if s == 3 else (255, 245, 210, 255))
# pixel moon (behind the vines, upper right of the final view)
MX, MY, MR = 880, PCY + 520, 74
for r_, col in ((MR + 30, (60, 50, 90, 255)), (MR + 14, (110, 100, 150, 255)), (MR, (245, 236, 200, 255))):
    sd.ellipse([MX - r_, MY - r_, MX + r_, MY + r_], fill=col)
for dx, dy, r_ in ((-22, -12, 14), (18, 20, 10), (26, -26, 7)): sd.ellipse([MX + dx - r_, MY + dy - r_, MX + dx + r_, MY + dy + r_], fill=(220, 208, 170, 255))
# soft pixel clouds
def cloud(d, x, y, w, col):
    for k in range(5):
        cx = x + (k - 2) * w / 5; r_ = w / 5 * (1.0 if k in (1, 2, 3) else 0.7)
        d.ellipse([cx - r_, y - r_ * 0.8, cx + r_, y + r_ * 0.6], fill=col)
    d.rectangle([x - w / 2, y, x + w / 2, y + w / 10], fill=col)
CLOUDS = [(rng.uniform(80, 1000), rng.uniform(PCY + 300, WH - 2300), rng.uniform(220, 380)) for _ in range(10)]
cl = Image.new('RGBA', (W, WH), (0, 0, 0, 0)); cd = ImageDraw.Draw(cl)
for x, y, w in CLOUDS: cloud(cd, x, y, w, (70, 60, 110, 120)); cloud(cd, x - 10, y - 8, w * 0.8, (96, 84, 140, 110))
SKY.alpha_composite(cl)
# forest clearing (Liza's found_hd, the clean version without the Hollow) at the bottom of the world
FW = 540; FX = 500
fg = Image.open(A + 'found_hd.gif'); FOREST = []
FMASK = Image.new('L', (W, 2160), 255); fm = ImageDraw.Draw(FMASK)
for y in range(0, 300): fm.line([(0, y), (W, y)], fill=int(255 * (y / 300) ** 1.4))
for i in range(0, fg.n_frames, 2):
    fg.seek(i); f = fg.convert('RGB').crop((FX, 0, FX + FW, 1080)).resize((W, 2160), Image.NEAREST)
    f = ImageEnhance.Brightness(f).enhance(0.62).convert('RGBA'); f.putalpha(FMASK); FOREST.append(f)
FY = WH - 2160
# vines: glow + body + leaves + flowers, drawn at half res and doubled (chunky pixels)
VL = Image.new('RGBA', (W // 2, WH // 2), (0, 0, 0, 0)); vd = ImageDraw.Draw(VL)
GLOW = Image.new('RGBA', (W // 2, WH // 2), (0, 0, 0, 0)); gd = ImageDraw.Draw(GLOW)
for i, (pts, _) in enumerate(PATHS):
    hp = [(x / 2, y / 2) for x, y in pts]; c_, dk = COL[i]
    gd.line(hp, fill=c_ + (90,), width=34, joint='curve')
GLOW = GLOW.filter(ImageFilter.GaussianBlur(7))
for i, (pts, _) in enumerate(PATHS):
    hp = [(x / 2, y / 2) for x, y in pts]; c_, dk = COL[i]
    lt = tuple(min(255, v + 70) for v in c_)
    vd.line(hp, fill=(18, 10, 28, 255), width=22, joint='curve')
    vd.line(hp, fill=dk + (255,), width=17, joint='curve')
    vd.line(hp, fill=c_ + (255,), width=11, joint='curve')
    vd.line([(x - 2.5, y - 1.5) for x, y in hp], fill=lt + (255,), width=3, joint='curve')
    # leaves in pairs along the vine + small flowers
    acc = 0; side = 1
    for k in range(1, len(hp) - 1):
        acc += math.hypot(hp[k][0] - hp[k - 1][0], hp[k][1] - hp[k - 1][1])
        if acc < 26 or k < 30 or k > len(hp) - 30: continue
        acc = 0; side = -side
        x, y = hp[k]; tx, ty = hp[k + 1][0] - hp[k - 1][0], hp[k + 1][1] - hp[k - 1][1]; L = math.hypot(tx, ty) or 1; tx, ty = tx / L, ty / L
        nx, ny = -ty * side, tx * side
        bx, by = x + nx * 9, y + ny * 9
        tipx, tipy = bx + nx * 9 - tx * 6, by + ny * 9 - ty * 6
        leaf = [(bx, by), (bx + nx * 4 + tx * 4, by + ny * 4 + ty * 4), (tipx, tipy), (bx + nx * 4 - tx * 5, by + ny * 4 - ty * 5)]
        vd.polygon(leaf, fill=(46, 120, 60, 255), outline=(14, 40, 22, 255))
        vd.line([(bx, by), ((bx + tipx) / 2, (by + tipy) / 2)], fill=(110, 190, 90, 255), width=1)
        if rng.random() < 0.22:
            fx_, fy_ = x - nx * 10, y - ny * 10
            vd.rectangle([fx_ - 3, fy_ - 1, fx_ + 3, fy_ + 1], fill=lt + (255,)); vd.rectangle([fx_ - 1, fy_ - 3, fx_ + 1, fy_ + 3], fill=lt + (255,))
            vd.point((fx_, fy_), fill=(255, 255, 255, 255))
VINES = Image.alpha_composite(GLOW, VL).resize((W, WH), Image.NEAREST)
if MODE == 'world':
    wv = SKY.copy(); wv.alpha_composite(VINES); wv = wv.crop((0, TOPY - 200, W, BOTY + 100)).convert('RGB')
    wv.resize((wv.width // 4, wv.height // 4)).save(f'world_{SEED}.png'); wv.save(f'worldfull_{SEED}.png'); sys.exit()
# scattered product gummies in the world (fixed, give the scroll a sense of travel), kept off the vines
GK = ['mush', 'acv', 'mel', 'cre']; GSM = {k: gummy(k, 2) for k in GK}
allpts = np.array([p for pts, _ in PATHS for p in pts[::6]])
DECO = []
while len(DECO) < 26:
    x, y = rng.uniform(100, 980), rng.uniform(TOPY + 120, BOTY - 160)
    if np.min(np.hypot(allpts[:, 0] - x, allpts[:, 1] - y)) > 70 and all(math.hypot(x - a, y - b) > 220 for a, b, _, _ in DECO):
        DECO.append((x, y, rng.choice(GK), rng.uniform(0, 6.28)))
# prizes
FRM = up(crop(Image.open(SP0 + 'fork_a2/gen/frame/00.png').convert('RGBA')), 4)
CHEST = up(crop(Image.open(SP0 + 'fork_a2/gen/chest/01.png').convert('RGBA')), 3)
# gummies-not-coins: the chest's coin heap is covered with a pile of product gummies
G2 = {k: gummy(k, 2) for k in GK}
for k, (dx, dy) in zip(['cre', 'mush', 'acv', 'mel', 'cre', 'acv'], [(30, 44), (92, 34), (60, 22), (122, 52), (8, 66), (104, 70)]):
    g = G2[k]; CHEST.alpha_composite(g, (dx, dy))
GOLDG = gummy('gold', 5)
_J = Image.open(A + 'jar_mushroom.png').convert('RGBA'); _J = _J.crop(_J.getbbox()); JAR = _J.resize((_J.width * 2 // 5, _J.height * 2 // 5), Image.NEAREST)
CYR = idle('cyrus', 3)
if MODE == 'chest':
    t_ = Image.new('RGBA', (400, 300), (30, 20, 50, 255)); t_.alpha_composite(CHEST, (100, 50)); t_.save('chest_chk.png'); sys.exit()
# ---------------- render
wr = Writer('v22_noaudio.mp4'); events = [(0.0, 'whoosh_8bit'), (round(T_ARR, 3), 'chime'), (round(T_SWAP, 3), 'ding_8bit')]
NF = int(DUR * FPS); SAVE = {0, int(4 * FPS), int(9 * FPS), int((T_ARR + 0.4) * FPS), NF - 5}
for f in range(NF):
    t = f / FPS; cy = int(round(cam(t)))
    img = SKY.crop((0, cy, W, cy + H))
    # twinkle a few stars
    def tw(d):
        for x, y, s, ph in STARS[::4]:
            sy = y - cy
            if -10 < sy < H + 10:
                a = int(255 * max(0, math.sin(t * 2.4 + ph)))
                if a > 40: d.rectangle([x - 3, sy + s / 2 - 1, x + s + 3, sy + s / 2 + 1], fill=(255, 250, 220, a)); d.rectangle([x + s / 2 - 1, sy - 3, x + s / 2 + 1, sy + s + 3], fill=(255, 250, 220, a))
    layer(img, tw)
    if FY - cy < H:
        fr = FOREST[int(t * 6) % len(FOREST)]; img.alpha_composite(fr, (0, FY - cy))
    for x, y, k, ph in DECO:
        sy = y - cy
        if -80 < sy < H + 80:
            g = GSM[k]; img.alpha_composite(g, (int(x - g.width / 2), int(sy - g.height / 2 + 6 * math.sin(t * 1.6 + ph))))
    img.alpha_composite(VINES.crop((0, cy, W, cy + H)))
    # A B C nodes + START
    ny = BOTY - cy
    if ny < H + 60:
        for i, x in enumerate(SX):
            c_ = COL[i][0]
            layer(img, lambda d, x=x, c_=c_: (d.ellipse([x - 44, ny - 44, x + 44, ny + 44], fill=(20, 12, 30, 255)), d.ellipse([x - 36, ny - 36, x + 36, ny + 36], fill=c_ + (255,))))
            text_layer(img, [(x, ny - 20, 'ABC'[i], 40, (30, 20, 40), 0, 255)])
        pul = 1 + 0.08 * math.sin(t * 9)
        text_layer(img, [(490, ny + 62, 'START!', int(40 * pul), (255, 255, 255), 6, 255)])
        cs = CYR[int(t * 8) % len(CYR)]; fy_ = ny + 366
        layer(img, lambda d: d.ellipse([490 - 70, fy_ - 12, 490 + 70, fy_ + 10], fill=(0, 0, 0, 90)))
        img.alpha_composite(cs, (490 - cs.width // 2, fy_ - 78 * 3))
    # prizes at the top of the journey
    py = PCY - cy
    if py > -200:
        pr = min(1, max(0, (t - T_ARR) / 0.35))
        for j, px in enumerate(PRX):
            layer(img, lambda d, px=px: d.rounded_rectangle([px - 122, py - 122, px + 122, py + 122], 18, fill=(16, 10, 30, 235)))
            img.alpha_composite(FRM, (int(px - FRM.width / 2), int(py - FRM.height / 2)))
            if pr > 0:
                sc = 0.5 + 0.5 * pr + 0.12 * math.sin(math.pi * pr)
                bob = int(5 * math.sin(t * 3 + j)) if pr >= 1 else 0
                it = [JAR, CHEST, GOLDG][j]; it2 = up(it, sc) if pr < 1 else it
                img.alpha_composite(it2, (int(px - it2.width / 2), int(py - it2.height / 2 + bob)))
                if pr < 1:
                    layer(img, lambda d, px=px: [d.rectangle([px + math.cos(k * 1.047) * (90 + 120 * pr) - 6, py + math.sin(k * 1.047) * (90 + 120 * pr) - 6,
                                                               px + math.cos(k * 1.047) * (90 + 120 * pr) + 6, py + math.sin(k * 1.047) * (90 + 120 * pr) + 6], fill=(255, 240, 160, int(255 * (1 - pr)))) for k in range(6)])
            else:
                text_layer(img, [(px, py - 36, '?', 80, (255, 214, 60), 7, 255)])
            layer(img, lambda d, x=PRX[j]: d.ellipse([x - 16, TOPY - cy - 16, x + 16, TOPY - cy + 16], fill=(255, 240, 200, 255)))
    img.alpha_composite(HOOK if t < T_SWAP else HOOK2)
    wr.write(img)
    if f in SAVE: img.convert('RGB').save(f'f_{f}.png')
wr.close()
json.dump({'events': events}, open('v22_events.json', 'w')); print('done', DUR)
