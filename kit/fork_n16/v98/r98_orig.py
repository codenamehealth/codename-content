# #98 The cleanest trap ever -- hook changed to WILL HE GET / SQUISHED? (fork_fix9899); otherwise identical to fork_sz94/v98. REDO (Bennett): the trap must always leave a way through.
# Stone blocks slam down and fill the castle courtyard around the Hollow (the player) as he walks to the gummy.
# Every slam lands right beside or right behind him, but the trap always leaves exactly one open path;
# the final blocks land on both sides of him at once (PERFECT GAP) and he ends on the only open tile, with the gummy.
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['WILL HE GET', 'SQUISHED?'], accent=1, size=72); HOOK2, _ = hook_fade(['WOULD YOU HAVE', 'SURVIVED?'], accent=1, size=72); print('hook bottom', HB)
OUT = SP + 'fork_hfg11/v98/'
# rc11 (review recut; Bennett approved #98 with the new hook, hook/concept/route unchanged): the Hollow walks from 0.2s and the
# first block slams at ~0.3s (GET THE GUMMY!/GOAL/GO! lead-in cut); CLOSE! 36px -> 60px on a dark plate beside the Hollow;
# PERFECT GAP! on a dark plate with a scale punch; end: MADE IT! + WOULD YOU HAVE / SURVIVED? (46px) held ~1.0s, then cut back
# to the empty board (loop).
G = SP + 'fork_a10/gen/'
CC, RR, S = 6, 7, 128
BX, BY = 94, 566
court = wang(G + 'court_meta.json', G + 'court_sheet.png')
GRASS = up(court[(False, False, False, False)], 3); FLAG = up(court[(True, True, True, True)], 3)
# hfg11 full-bleed: the flagstone courtyard runs edge to edge (tiles phase-aligned with the board), no frame border, no castle strip
BASE = Image.new('RGBA', (W, H), (30, 60, 30, 255))
ox_, oy_ = BX % FLAG.width - FLAG.width, BY % FLAG.height - FLAG.height
for y in range(oy_, H, FLAG.height):
    for x in range(ox_, W, FLAG.width):
        fl = FLAG if ((x - BX) // 96 + (y - BY) // 96) % 2 else FLAG.transpose(Image.FLIP_LEFT_RIGHT); BASE.alpha_composite(fl, (x, y))
def frame_board(d):
    for c in range(1, CC): d.line([BX + c * S, BY, BX + c * S, BY + RR * S], fill=(255, 255, 255, 45), width=2)
    for r in range(1, RR): d.line([BX, BY + r * S, BX + CC * S, BY + r * S], fill=(255, 255, 255, 45), width=2)
layer(BASE, frame_board)
# stone block (pixel art at 1/4 res, x4): 32x37 native, top face + front lip
def make_block():
    n = S // 4; lip = 5; im = Image.new('RGBA', (n, n + lip), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, n - 1, n + lip - 1], fill=(36, 34, 48, 255))
    d.rectangle([1, 1, n - 2, n - 2], fill=(132, 136, 156, 255))                       # top face
    d.rectangle([1, n - 1, n - 2, n + lip - 2], fill=(84, 86, 106, 255))              # front face
    d.line([1, 1, n - 2, 1], fill=(186, 190, 206, 255)); d.line([1, 1, 1, n - 2], fill=(170, 174, 192, 255))
    for (x0, y0, x1, y1) in ((4, 5, 13, 11), (17, 4, 27, 10), (6, 16, 16, 23), (20, 15, 27, 24), (9, 26, 24, 28)):
        d.rectangle([x0, y0, x1, y1], outline=(108, 110, 132, 255))
    d.rectangle([n // 2 - 3, n // 2 - 3, n // 2 + 2, n // 2 + 2], fill=(70, 130, 232, 255)); d.point((n // 2 - 2, n // 2 - 2), fill=(170, 210, 255, 255))
    d.rectangle([n // 2 - 4, n // 2 - 4, n // 2 + 3, n // 2 + 3], outline=(255, 214, 60, 255))
    return up(im, 4)
BLOCK = make_block(); LIP = BLOCK.height - S
def cell_xy(p): return (BX + p[1] * S + S / 2, BY + p[0] * S + S / 2)
HH = 190
HF = gif_frames(A + 'hollow-walk-front.gif', h=HH); HS = gif_frames(A + 'hollow-walk-side.gif', h=HH)
HSL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in HS]; HVIC = vic('hollow', 210)
GUM = gummy('cre', 4)
# ---- scripted route (down/left/right only)
P = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)]
GOAL = P[-1]; NS = len(P) - 1
T0, TURN = 0.2, 0.56
T_ARR = T0 + NS * TURN; END = T_ARR + 1.6
def at(i): return T0 + i * TURN          # time he reaches P[i]
def adj(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
pathset = set(P); DROP = {}
T_PERF = at(NS - 1) + 0.2   # he is standing in the last gap
for r in range(RR):
    for c in range(CC):
        q = (r, c)
        if q in pathset: continue
        near = [i for i, p in enumerate(P) if adj(p, q)]
        if near: DROP[q] = at(near[0]) + 0.22                 # slams right beside him as he arrives next to it
        else: DROP[q] = None
# cells he never touches: slam in early, far ones first, staggered
far = sorted([q for q, v in DROP.items() if v is None], key=lambda q: (q[0], q[1]))
for k, q in enumerate(far): DROP[q] = T0 + 0.1 + k * 0.33
# last stretch: everything still open beside the final gap slams at once while he is in it
for q in list(DROP):
    if DROP[q] > at(NS - 2) + 0.1: DROP[q] = T_PERF
for q in [(5, 3), (5, 5), (6, 3), (6, 5)]: DROP[q] = T_PERF
# the path closes behind him two steps back
for i, p in enumerate(P[:-1]): DROP[p] = min(at(i + 2) + 0.25, T_PERF + 0.5) if i + 2 <= NS else T_PERF + 0.5
assert GOAL not in DROP and all(DROP[q] > (at(P.index(q)) + 0.3 if q in pathset else 0) for q in DROP)
EVENTS = sorted((t, q) for q, t in DROP.items())
print('steps', NS, 'arrive', round(T_ARR, 2), 'perfect', round(T_PERF, 2), 'end', round(END, 2), 'blocks', len(DROP))
def hollow_state(t):
    if t < T0: return cell_xy(P[0]), None
    k = int((t - T0) / TURN)
    if k >= NS: return cell_xy(P[-1]), None
    u = (t - T0 - k * TURN) / TURN; u = min(1, u / 0.85); a, b = cell_xy(P[k]), cell_xy(P[k + 1])
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u), (P[k + 1][0] - P[k][0], P[k + 1][1] - P[k][1])
w = Writer(OUT + 'noaudio.mp4'); ev = []; NF = int(END * FPS)
last_pop = -9; pops = []
for td, q in EVENTS:
    if q in pathset and td < T_PERF and td - last_pop > 1.3:
        pops.append((td + 0.1, None, None, 'CLOSE!')); last_pop = td
FRS = [int(x) for x in os.environ['ONLY'].split(',')] if os.environ.get('ONLY') else range(NF)
for f in FRS:
    t = f / FPS
    img = BASE.copy()
    gx, gy = cell_xy(GOAL)
    if t < T_ARR:
        layer(img, lambda d2: d2.ellipse([gx - 58, gy - 58, gx + 58, gy + 58], fill=(120, 190, 255, int(70 + 30 * math.sin(t * 6)))))
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy + 40 - GUM.height)))
    (hx, hy), mv = hollow_state(t)
    hrow_y = hy
    # shadows of falling blocks first
    def shadows(d2):
        for td, q in EVENTS:
            u = t - td + 0.35
            if 0 <= u < 0.35:
                x, y = cell_xy(q); s = 20 + 40 * u / 0.35
                d2.ellipse([x - s, y - s * 0.6, x + s, y + s * 0.6], fill=(0, 0, 0, int(60 + 120 * u / 0.35)))
    layer(img, shadows)
    shake = 0
    def draw_block(q, td):
        global shake
        u = t - td; x, y = cell_xy(q); x0, y0 = int(x - S / 2), int(y - S / 2 - LIP)
        if u < -0.35: return
        if u < 0:   # falling in from above
            v = 1 + u / 0.35; yy_ = int(y0 - 520 * (1 - v) ** 2)
            if yy_ + BLOCK.height > HB:   # hfg11: falling blocks drop in from under the hook fade, never behind the hook words
                cut_ = max(0, HB - yy_); img.alpha_composite(BLOCK.crop((0, cut_, BLOCK.width, BLOCK.height)), (x0, yy_ + cut_))
        else:
            img.alpha_composite(BLOCK, (x0, y0))
            if u < 0.45:
                def dust(d2, x=x, y=y, u=u):
                    for k in range(8):
                        a = k * 0.785; rr = 60 + 70 * u
                        d2.rectangle([x + rr * math.cos(a) - 9, y + S / 2 - 10 + rr * 0.35 * math.sin(a) - 9, x + rr * math.cos(a) + 9, y + S / 2 - 10 + rr * 0.35 * math.sin(a) + 9], fill=(220, 210, 190, int(190 * (1 - u / 0.45))))
                layer(img, dust)
            if u < 0.12: shake = max(shake, 9 if abs(td - T_PERF) < 0.01 else 4)
    # depth order: blocks whose row is above his feet, then the Hollow, then the rest
    landed_below = []
    for td, q in EVENTS:
        if cell_xy(q)[1] <= hrow_y + 1: draw_block(q, td)
        else: landed_below.append((td, q))
    if t >= T_ARR:
        fr = HVIC[int((t - T_ARR) * 8) % len(HVIC)]
        img.alpha_composite(fr, (int(hx - fr.width / 2), int(hy + 50 - fr.height)))
    else:
        if mv is None: fr = HF[0]
        elif mv[0] > 0: fr = HF[int(t * 10) % 6]
        elif mv[1] > 0: fr = HS[int(t * 10) % 6]
        else: fr = HSL[int(t * 10) % 6]
        layer(img, lambda d2: d2.ellipse([hx - 40, hy + 38, hx + 40, hy + 56], fill=(0, 0, 0, 90)))
        img.alpha_composite(fr, (int(hx - fr.width / 2), int(hy + 50 - fr.height)))
    for td, q in landed_below: draw_block(q, td)
    for td, q in EVENTS:
        if f == int(round(td * FPS)) and abs(td - T_PERF) > 0.01: ev.append((round(t, 3), 'brick_8bit'))
    if f == int(round(T_PERF * FPS)): ev.append((round(t, 3), 'boom'))
    for tp, x, y, txt in pops:
        u = t - tp
        if 0 <= u < 0.75:
            a = int(255 * min(1, (0.75 - u) / 0.25)); k_ = 1.2 - 0.2 * min(1, u / 0.1); fs = int(60 * k_)
            px_ = min(max(hx, 120 + 190), 850 - 190)            # next to the Hollow, inside the zone
            py_ = hy - 260 if hy > 900 else hy + 90               # above his head, or under his feet near the top rows
            def cplate(d2, px_=px_, py_=py_, a=a, fs=fs):
                ctext(d2, px_, py_, txt, F(fs), (255, 90, 90), 9, a)
            layer(img, cplate)
    if T_PERF <= t < T_ARR + 0.3:
        u = t - T_PERF; s = 1.3 - 0.3 * min(1, u / 0.12); a = int(255 * min(1, u / 0.06)); fs = int(64 * s)
        def pplate(d2, fs=fs, a=a):
            ctext(d2, 478, 742, 'PERFECT GAP!', F(fs), (255, 214, 60), 10, a)
        layer(img, pplate)
    if t >= T_ARR:
        u = t - T_ARR; a = int(255 * min(1, max(0, u - 0.4) / 0.2))
        def sparks(d2):
            rr = random.Random(f)
            for _ in range(16):
                an = rr.uniform(0, 6.28); rad = 40 + 150 * min(1, u / 0.6) * rr.uniform(0.5, 1)
                d2.rectangle([gx + rad * math.cos(an) - 6, gy - 70 + rad * 0.8 * math.sin(an) - 6, gx + rad * math.cos(an) + 6, gy - 70 + rad * 0.8 * math.sin(an) + 6], fill=(150, 210, 255, int(230 * max(0, 1 - u / 1.2))))
        layer(img, sparks)
        if u < 1.0: img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - 250 - 50 * u)))
        text_layer(img, [(478, 724, 'MADE IT!', 80, (255, 214, 60), 10, a)])
        if f == int(round(T_ARR * FPS)): ev.append((round(t, 3), 'powerup_8bit'))
        if f == int(round((T_ARR + 0.4) * FPS)): ev.append((round(t, 3), 'victory'))
    if shake: img = img.transform(img.size, Image.AFFINE, (1, 0, random.Random(f).choice([-shake, shake]), 0, 1, 0))
    img.alpha_composite(HOOK2 if t >= T_ARR + 0.4 else HOOK)
    w.write(img)
    if os.environ.get('ONLY') or f in (0, 6, 12, 60, int(T_PERF * FPS) + 3, NF - 1) or any(abs(t - tp - 0.15) < 0.5 / FPS for tp, _, _, _ in pops[:1]): img.convert('RGB').save(OUT + f'k_{f:04d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev))
