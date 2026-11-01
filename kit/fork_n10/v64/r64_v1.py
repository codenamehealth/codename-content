# #64 "Each ball has only 4 seconds to escape" - Oct 29 n10 physics rebuild.
# Bennett: "physics needs to be perfect on these types of videos. no weird movements".
# One continuous rigid-body sim per try: gravity, restitution < 1, collisions with the ring's inner wall, outer wall and the two
# moving gap end caps (relative velocity of the rotating ring), frozen balls as static obstacles, 16 substeps per frame.
# After the escape the bubble pops and the gummy keeps flying on the same ballistic path (same sim, smaller radius) into the
# Hollow's hands; the Hollow is placed where that real trajectory reaches his hands (no steering, no easing, no snapping).
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); SPD = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SPD + 'fork1'); from common import *
sys.path.insert(0, SPD + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
os.chdir(HERE)
CX, CY = 460, 930   # n10: ring up 55px so the Hollow can stand under any part of it and catch the gummy
RW, TH = 336, 18            # ring inner radius (contact surface = drawn inner edge) and wall thickness
r = 62                      # bubble radius (drawn radius too)
RG = 25                     # gummy radius after the pop (2x gummy sprite 48x52)
GAPW = 0.78; OMEGA = 1.35; GRAV = 1500
E_WALL, E_BALL = 0.95, 0.9
SUB = 16
KINDS = ['s1', 's2', 's3', 'gold']
GLOW = {'s1': (120, 220, 120), 's2': (110, 160, 255), 's3': (240, 120, 200), 'gold': (255, 160, 50)}
T0 = 0.0; TRY = 4.0; GAP_T = 0.25
GEM = (4.7, -89.8)          # gem/hands point of hollow_eat frame 1 relative to (HX, HY) (feet)
def gap_center(t): return -math.pi / 2 + OMEGA * t
def angdiff(a, b): return (a - b + math.pi) % (2 * math.pi) - math.pi

def collide_ring(x, y, vx, vy, rad, tt, hits):
    gc = gap_center(tt)
    dx, dy = x - CX, y - CY; d = math.hypot(dx, dy); a = math.atan2(dy, dx)
    in_gap = abs(angdiff(a, gc)) < GAPW / 2
    if not in_gap and d > 1e-6:
        nx, ny = dx / d, dy / d
        if d < RW and d + rad > RW:                       # inner wall, normal points to the centre
            pen = d + rad - RW; vn = -(vx * nx + vy * ny)
            if vn < 0: vx += (1 + E_WALL) * vn * nx; vy += (1 + E_WALL) * vn * ny; hits.append(('wall', tt, abs(angdiff(a, gc)) - GAPW / 2))
            x -= nx * pen; y -= ny * pen
        elif d > RW + TH and d - rad < RW + TH:           # outer wall (only after an escape)
            pen = RW + TH - (d - rad); vn = vx * nx + vy * ny
            if vn < 0: vx -= (1 + E_WALL) * vn * nx; vy -= (1 + E_WALL) * vn * ny; hits.append(('outer', tt, 0))
            x += nx * pen; y += ny * pen
        elif RW <= d <= RW + TH:
            hits.append(('INSIDE_WALL', tt, d))
    for ge in (gc - GAPW / 2, gc + GAPW / 2):              # moving end caps of the gap
        ux, uy = math.cos(ge), math.sin(ge)
        px, py = x - CX, y - CY; s = max(RW, min(RW + TH, px * ux + py * uy))
        qx, qy = CX + ux * s, CY + uy * s; ddx, ddy = x - qx, y - qy; dd = math.hypot(ddx, ddy)
        if 1e-6 < dd < rad:
            nx, ny = ddx / dd, ddy / dd
            wvx, wvy = -OMEGA * (qy - CY), OMEGA * (qx - CX)
            vn = (vx - wvx) * nx + (vy - wvy) * ny
            if vn < 0: vx -= (1 + E_WALL) * vn * nx; vy -= (1 + E_WALL) * vn * ny; hits.append(('cap', tt, 0))
            x += nx * (rad - dd); y += ny * (rad - dd)
    return x, y, vx, vy

def run_attempt(seed, frozen, tstart, last=False):
    rnd = random.Random(seed); ang = rnd.uniform(0, 2 * math.pi); spd = rnd.uniform(550, 900)
    x, y = CX + rnd.uniform(-40, 40), CY + rnd.uniform(-60, 20); vx, vy = spd * math.cos(ang), spd * math.sin(ang)
    if any(math.hypot(x - fx, y - fy) < 2 * r + 12 for fx, fy in frozen): return None
    dt = 1 / (FPS * SUB); path = []; hits = []; popped = None; rad = r
    nf = int(TRY * FPS) + (int(2.0 * FPS) if last else 0)
    for f in range(nf):
        t = tstart + f / FPS
        if not last and f >= int(TRY * FPS): break
        if last and popped is None and f >= int(TRY * FPS): return None   # must escape inside its 4 seconds
        for k in range(SUB):
            tt = t + (k + 1) * dt
            vy += GRAV * dt; x += vx * dt; y += vy * dt
            x, y, vx, vy = collide_ring(x, y, vx, vy, rad, tt, hits)
            for (fx, fy) in frozen:
                ddx, ddy = x - fx, y - fy; dd = math.hypot(ddx, ddy)
                if 1e-6 < dd < rad + r:
                    nx, ny = ddx / dd, ddy / dd; vn = vx * nx + vy * ny
                    if vn < 0: vx -= (1 + E_BALL) * vn * nx; vy -= (1 + E_BALL) * vn * ny; hits.append(('ball', tt, 0))
                    x += nx * (rad + r - dd); y += ny * (rad + r - dd)
        path.append((x, y, vx, vy))
        if popped is None and math.hypot(x - CX, y - CY) - r > RW + TH + 2:
            popped = len(path) - 1; rad = RG
            if not last: break
    return path, hits, popped

def vec_last(seeds, frozen, tstart):
    """try 4 for many seeds at once (numpy), same integrator/collisions as run_attempt; returns per seed (path, hits, popped)"""
    n = len(seeds); R = [random.Random(s) for s in seeds]
    ang = np.array([q.uniform(0, 2 * math.pi) for q in R]); spd = np.array([q.uniform(550, 900) for q in R])
    # same draw order as run_attempt: ang, spd, then x, y offsets
    R = [random.Random(s) for s in seeds]; xs = []; ys = []
    for q in R: q.uniform(0, 2 * math.pi); q.uniform(550, 900); xs.append(q.uniform(-40, 40)); ys.append(q.uniform(-60, 20))
    x = CX + np.array(xs); y = CY + np.array(ys); vx = spd * np.cos(ang); vy = spd * np.sin(ang)
    ok = np.ones(n, bool)
    for fx, fy in frozen: ok &= np.hypot(x - fx, y - fy) >= 2 * r + 12
    rad = np.full(n, float(r)); popped = np.full(n, -1); bad = np.zeros(n, bool)
    dt = 1 / (FPS * SUB); NF = int(TRY * FPS) + int(2.0 * FPS)
    P = np.zeros((NF, n, 4)); hits = [[] for _ in range(n)]
    def addhits(mask, kind, tt, extra=None):
        for i in np.nonzero(mask)[0]: hits[i].append((kind, tt, 0 if extra is None else float(extra[i])))
    for f in range(NF):
        t = tstart + f / FPS
        for k in range(SUB):
            tt = t + (k + 1) * dt; gc = gap_center(tt)
            vy = vy + GRAV * dt; x = x + vx * dt; y = y + vy * dt
            dx, dy = x - CX, y - CY; d = np.hypot(dx, dy); a = np.arctan2(dy, dx)
            adg = np.abs((a - gc + math.pi) % (2 * math.pi) - math.pi); in_gap = adg < GAPW / 2
            nx, ny = dx / d, dy / d
            m = ~in_gap & (d < RW) & (d + rad > RW)
            pen = d + rad - RW; vn = -(vx * nx + vy * ny); h = m & (vn < 0)
            vx = np.where(h, vx + (1 + E_WALL) * vn * nx, vx); vy = np.where(h, vy + (1 + E_WALL) * vn * ny, vy)
            if h.any(): addhits(h, 'wall', tt, adg - GAPW / 2)
            x = np.where(m, x - nx * pen, x); y = np.where(m, y - ny * pen, y)
            m2 = ~in_gap & ~m & (d > RW + TH) & (d - rad < RW + TH)
            pen = RW + TH - (d - rad); vn = vx * nx + vy * ny; h = m2 & (vn < 0)
            vx = np.where(h, vx - (1 + E_WALL) * vn * nx, vx); vy = np.where(h, vy - (1 + E_WALL) * vn * ny, vy)
            if h.any(): addhits(h, 'outer', tt)
            x = np.where(m2, x + nx * pen, x); y = np.where(m2, y + ny * pen, y)
            bad |= ~in_gap & ~m & ~m2 & (d >= RW) & (d <= RW + TH)
            for ge in (gc - GAPW / 2, gc + GAPW / 2):
                ux, uy = math.cos(ge), math.sin(ge)
                sproj = np.clip((x - CX) * ux + (y - CY) * uy, RW, RW + TH)
                qx, qy = CX + ux * sproj, CY + uy * sproj; ddx, ddy = x - qx, y - qy; dd = np.hypot(ddx, ddy)
                m3 = (dd > 1e-6) & (dd < rad); dds = np.where(m3, dd, 1.0)
                nx3, ny3 = ddx / dds, ddy / dds; wvx, wvy = -OMEGA * (qy - CY), OMEGA * (qx - CX)
                vn = (vx - wvx) * nx3 + (vy - wvy) * ny3; h = m3 & (vn < 0)
                vx = np.where(h, vx - (1 + E_WALL) * vn * nx3, vx); vy = np.where(h, vy - (1 + E_WALL) * vn * ny3, vy)
                if h.any(): addhits(h, 'cap', tt)
                x = np.where(m3, x + nx3 * (rad - dd), x); y = np.where(m3, y + ny3 * (rad - dd), y)
            for (fx, fy) in frozen:
                ddx, ddy = x - fx, y - fy; dd = np.hypot(ddx, ddy); m4 = (dd > 1e-6) & (dd < rad + r); dds = np.where(m4, dd, 1.0)
                nx4, ny4 = ddx / dds, ddy / dds; vn = vx * nx4 + vy * ny4; h = m4 & (vn < 0)
                vx = np.where(h, vx - (1 + E_BALL) * vn * nx4, vx); vy = np.where(h, vy - (1 + E_BALL) * vn * ny4, vy)
                if h.any(): addhits(h, 'ball', tt)
                x = np.where(m4, x + nx4 * (rad + r - dd), x); y = np.where(m4, y + ny4 * (rad + r - dd), y)
        P[f, :, 0], P[f, :, 1], P[f, :, 2], P[f, :, 3] = x, y, vx, vy
        newp = (popped < 0) & (np.hypot(x - CX, y - CY) - r > RW + TH + 2)
        popped = np.where(newp, f, popped); rad = np.where(newp, float(RG), rad)
        if f == int(TRY * FPS) - 1: ok &= popped >= 0
    out = []
    for i in range(n):
        if not ok[i] or bad[i]: out.append(None); continue
        path = [tuple(map(float, P[j, i])) for j in range(NF)]
        out.append((path, hits[i], int(popped[i])))
    return out

def fail_ok(path, hits):
    x, y = path[-1][:2]
    return math.hypot(x - CX, y - CY) <= RW - r + 1.5 and not any(h[0] == 'INSIDE_WALL' for h in hits)

def catch_info(path, popped, t0):
    """first frame after the pop where the gummy is descending through hand height; Hollow is placed under it"""
    for j in range(popped + 1, len(path)):
        x, y, vx, vy = path[j]
        if x < 40 or x > 1040 or y < 260: return None
        if vy > 0 and y >= 1395:
            HX, HY = x - GEM[0], y - GEM[1]
            if not (140 <= HX <= 870): return None
            if not (1430 <= HY <= 1525): return None
            if not (0.15 <= (j - popped) / FPS <= 1.3): return None
            # the bubble never touches the Hollow before it pops (he stands outside the ring, the bubble pops in the air)
            for (px, py, _, _) in path[:popped + 1]:
                qx, qy = max(HX - 51, min(HX + 60, px)), max(HY - 189, min(HY, py))
                if math.hypot(px - qx, py - qy) < r + 6: return None
            return j, HX, HY
    return None

def plan(base):
    frozen = []; seq_ = []; t = T0
    for i, k in enumerate(KINDS):
        if i == 3:
            seeds = list(range(500000 + base * 4000, 500000 + base * 4000 + 4000)); VR = []
            for c in range(0, len(seeds), 500): VR += vec_last(seeds[c:c + 500], frozen, t)
            print('base', base, 'try4 escapes', sum(1 for v in VR if v), flush=True)
        for si, s in enumerate(range(base * 1000 + i * 100, base * 1000 + i * 100 + 99) if i < 3 else seeds):
            res = run_attempt(s, frozen, t) if i < 3 else VR[si]
            if res is None: continue
            path, hits, popped = res
            bounces = [h[1] for h in hits if h[0] in ('wall', 'cap', 'ball')]
            near = [h[1] for h in hits if h[0] == 'cap' or (h[0] == 'wall' and h[2] < 0.10)]
            if i < 3:
                if popped is not None or not fail_ok(path, hits) or len(bounces) < 4: continue
                if i == 2 and not any(1.0 < x - t < 3.0 for x in near): continue
                if i < 2 and near: continue
                tend = t + TRY; seq_.append((k, t, 'fail', path, hits, tend, near, None)); frozen.append(path[-1][:2]); t = tend + GAP_T; break
            else:
                if popped is None or any(h[0] == 'INSIDE_WALL' for h in hits): continue
                tesc = t + (popped + 1) / FPS
                if not (1.0 < tesc - t < 3.6): continue
                ci = catch_info(path, popped, t)
                if ci is None: continue
                seq_.append((k, t, 'escape', path, hits, tesc, near, (popped, ci))); break
        else: return None
    return seq_

SEQ = None
for base in range(1, 400):
    SEQ = plan(base)
    if SEQ:
        print('plan base', base, [(k, round(t, 2), res, round(tend - t, 2)) for k, t, res, p, h, tend, nr, ex in SEQ]); break
assert SEQ, 'no plan'
k4, t4, _, PATH4, HITS4, T_ESC, _, (POPF, (CATF, HX, HY)) = SEQ[-1]
T_CATCH = t4 + (CATF + 1) / FPS
HX, HY = int(round(HX)), int(round(HY))
NEAR_T = [x for x in SEQ[2][6] if 1.0 < x - SEQ[2][1] < 3.0][0]
T_CARD = T_CATCH + 0.25; END = T_CARD + 1.6; N = int(round(END * FPS))
print('esc', round(T_ESC, 2), 'catch', round(T_CATCH, 2), 'HX HY', HX, HY, 'near', round(NEAR_T, 2), 'end', round(END, 2), 'N', N)
json.dump({'seq': [(k, t, res, tend, [list(map(float, p)) for p in path]) for k, t, res, path, h, tend, nr, ex in SEQ],
           'POPF': POPF, 'CATF': CATF, 'HX': HX, 'HY': HY}, open('plan.json', 'w'))
if os.environ.get('PLAN_ONLY'): sys.exit()

BG = bg_frames('found_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.45)
def nored(im):
    a = np.array(im); rr_, gg, bb_ = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(rr_ > 140) & (gg < 110) & (bb_ < 140)] = 0; return Image.fromarray(a)
SLM = up(crop(nored(Image.open(PL + 'race/slime_idle_c/00.png').convert('RGBA'))), 3)
GUM = {k: SLM for k in KINDS}; GUM['gold'] = gummy('mush', 2)     # mushroom gummy, 2x so the same sprite fits his hands
EAT_RAW = seq(SPD + 'fork3/hollow_eat', 3, 0, 13); HID = idle('hollow', 3)
EAT_IDX = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]   # frame 7 re-shows the gem after it was eaten: skipped
def gem_pos(im):
    a = np.array(im); m = (a[..., 0] > 150) & (a[..., 1] < 110) & (a[..., 3] > 0)
    if m.sum() < 20: return None
    ys, xs = np.nonzero(m); return xs.mean(), ys.mean()
EAT = [(EAT_RAW[i], gem_pos(EAT_RAW[i])) for i in EAT_IDX]
HOOK, HB = hook_fade(['EACH BALL HAS', 'ONLY 4 SECONDS'], accent=1); print('HB', HB)
ev = []
for k, t, res, path, hits, tend, nr, ex in SEQ:
    lb = -9
    for h in hits:
        bt = h[1]
        if h[0] in ('wall', 'cap', 'ball', 'outer') and bt - lb >= 0.3 and bt < tend - 0.1: ev.append((round(bt, 3), 'tick_8bit')); lb = bt
    ev.append((round(tend, 3), 'buzz_8bit' if res == 'fail' else 'powerup_8bit'))
ev += [(round(NEAR_T, 3), 'whoosh_8bit'), (round(T_ESC + 0.02, 3), 'poof'), (round(T_CATCH + 0.35, 3), 'crunch_8bit'), (round(T_CARD, 3), 'victory')]
def bubble(k, frozen=False):
    sz = 2 * r + 8; im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if frozen:
        d.ellipse([4, 4, sz - 4, sz - 4], fill=(150, 170, 200, 235), outline=(230, 240, 255, 255), width=4)
        g = ImageEnhance.Color(GUM[k]).enhance(0.25); g = ImageEnhance.Brightness(g).enhance(0.75)
        im.alpha_composite(g, (sz // 2 - g.width // 2, sz // 2 - g.height // 2))
        d.polygon([(sz * 0.3, sz * 0.2), (sz * 0.45, sz * 0.12), (sz * 0.4, sz * 0.35)], fill=(255, 255, 255, 160))
        d.line([(sz * 0.6, sz * 0.25), (sz * 0.75, sz * 0.5), (sz * 0.62, sz * 0.7)], fill=(255, 255, 255, 140), width=3)
    else:
        c = GLOW[k]
        d.ellipse([4, 4, sz - 4, sz - 4], fill=c + (70,), outline=(240, 250, 255, 230), width=4)
        g = GUM[k]; im.alpha_composite(g, (sz // 2 - g.width // 2, sz // 2 - g.height // 2))
        d.ellipse([sz * 0.25, sz * 0.18, sz * 0.42, sz * 0.32], fill=(255, 255, 255, 190))
    return im
BUB = {k: bubble(k) for k in KINDS}; FROZ = {k: bubble(k, True) for k in KINDS}
rng = random.Random(4); FLY = [(rng.uniform(40, 1040), rng.uniform(420, 1800), rng.uniform(0, 6.3)) for _ in range(30)]
def ring_poly(a0, a1, r0, r1, step=0.01):
    n = max(2, int((a1 - a0) / step)); out_ = [(CX + r1 * math.cos(a0 + (a1 - a0) * i / n), CY + r1 * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    inn = [(CX + r0 * math.cos(a0 + (a1 - a0) * i / n), CY + r0 * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n, -1, -1)]
    return out_ + inn
TRYX = 249 if HX >= 470 else 740
def pos_at(path, t0, t):
    """ball position at output time t: path[j] is the state at t0 + (j+1)/FPS; before the first step use the spawn"""
    j = int(round((t - t0) * FPS)) - 1
    if j < 0:   # the spawn frame: one step back along the first frame's motion (no one-frame stall at spawn)
        x, y, vx, vy = path[0]; return (x - vx / FPS, y - vy / FPS + 0.5 * GRAV / FPS ** 2, vx, vy - GRAV / FPS)
    return path[min(j, len(path) - 1)]
def frame(f):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    def bgfx(d):
        for fx, fy, ph in FLY:
            a = int(120 + 120 * math.sin(t * 2 + ph))
            if a > 60: d.ellipse([fx + 20 * math.sin(t + ph) - 4, fy - 4, fx + 20 * math.sin(t + ph) + 4, fy + 4], fill=(230, 255, 150, a))
        d.ellipse([CX - RW + 6, CY - RW + 6, CX + RW - 6, CY + RW - 6], fill=(10, 8, 24, 110))
    layer(img, bgfx)
    cur = None
    for i, (k, t0, res, path, h, tend, nr, ex) in enumerate(SEQ):
        if t0 <= t < tend + (GAP_T if res == 'fail' else 99): cur = i
    gc = gap_center(t)   # the ring keeps turning the whole video (it is the same rigid ring)
    def ring(d):
        a0, a1 = gc + GAPW / 2, gc - GAPW / 2 + 2 * math.pi
        d.polygon(ring_poly(a0, a1, RW - 6, RW + TH + 10), fill=(120, 90, 220, 90))
        d.polygon(ring_poly(a0, a1, RW, RW + TH), fill=(170, 140, 255, 255))
        d.polygon(ring_poly(a0, a1, RW, RW + 4), fill=(215, 200, 255, 255))
        for j in range(12):   # studs fixed to the ring (rotate rigidly with it)
            a = gc + GAPW / 2 + 0.18 + j * (2 * math.pi - GAPW - 0.36) / 11
            px, py = CX + (RW + TH / 2) * math.cos(a), CY + (RW + TH / 2) * math.sin(a)
            d.rectangle([px - 5, py - 5, px + 5, py + 5], fill=(255, 225, 140, 255))
        if cur is not None and t < SEQ[cur][5]:
            u = (t - SEQ[cur][1]) / TRY; rem = max(0, 1 - u)
            col = (90, 210, 90) if rem > 0.5 else ((240, 200, 60) if rem > 0.25 else (240, 80, 70))
            R2 = RW + TH + 40
            d.arc([CX - R2, CY - R2, CX + R2, CY + R2], -90, -90 + 360 * rem, fill=col + (255,), width=12)
    layer(img, ring)
    for i, (k, t0, res, path, h, tend, nr, ex) in enumerate(SEQ):
        if res == 'fail' and t >= tend:
            fx, fy = path[-1][:2]; fb = FROZ[k]; img.alpha_composite(fb, (int(round(fx - fb.width / 2)), int(round(fy - fb.height / 2))))
    if cur is not None:
        k, t0, res, path, h, tend, nr, ex = SEQ[cur]
        if t < tend:
            px, py = pos_at(path, t0, t)[:2]
            j0 = int(round((t - t0) * FPS)) - 1
            def trail(d):
                for j in range(max(0, j0 - 10), max(0, j0)):
                    qx, qy = path[j][:2]; a = int(30 + 15 * (j - j0 + 10))
                    d.ellipse([qx - 18, qy - 18, qx + 18, qy + 18], fill=GLOW[k] + (a,))
            layer(img, trail)
            u_sp = t - t0
            if u_sp < 0.15:   # spawn ring
                layer(img, lambda d: d.ellipse([px - r - 60 * u_sp / 0.15, py - r - 60 * u_sp / 0.15, px + r + 60 * u_sp / 0.15, py + r + 60 * u_sp / 0.15], outline=(255, 255, 255, int(220 * (1 - u_sp / 0.15))), width=6))
            bb = BUB[k]; img.alpha_composite(bb, (int(round(px - bb.width / 2)), int(round(py - bb.height / 2))))
            n = max(1, math.ceil(t0 + TRY - t))
            text_layer(img, [(CX, CY - 70, str(n), 120, (255, 255, 255), 9, 200)])
    # escape: the bubble popped as it cleared the ring; the gummy keeps flying on the sim path into the Hollow's hands
    FLIGHT = None
    if t >= T_ESC:
        u = t - T_ESC; ex_, ey_ = PATH4[POPF][:2]
        if u < 0.4:
            def popfx(d):
                for j in range(12):
                    a = j * 0.52; rr_ = 30 + 200 * u
                    d.rectangle([ex_ + rr_ * math.cos(a) - 6, ey_ + rr_ * math.sin(a) - 6, ex_ + rr_ * math.cos(a) + 6, ey_ + rr_ * math.sin(a) + 6], fill=(255, 235, 150, int(255 * (1 - u / 0.4))))
            layer(img, popfx)
        if t < T_CATCH:
            gx, gy = pos_at(PATH4, t4, t)[:2]; g = GUM['gold']
            j0 = int(round((t - t4) * FPS)) - 1
            def gtrail(d):
                for j in range(max(POPF, j0 - 6), j0):
                    qx, qy = PATH4[j][:2]; a = int(40 + 25 * (j - j0 + 6))
                    d.ellipse([qx - 12, qy - 12, qx + 12, qy + 12], fill=GLOW['gold'] + (a,))
            layer(img, gtrail)
            FLIGHT = (g, (int(round(gx - g.width / 2)), int(round(gy - g.height / 2))))
    # the Hollow: idle until the gummy reaches his hands, then the eat animation with the same gummy held
    HOLD = None
    if t >= T_CATCH:
        ei = min(len(EAT) - 1, 1 + int((t - T_CATCH) * 12)); hf, gp = EAT[ei]
        if gp is not None: g = GUM['gold']; HOLD = (g, (int(round(HX - 138 + gp[0] - g.width / 2)), int(round(HY - 234 + gp[1] - g.height / 2))))
    else: hf = HID[int(t * 6) % len(HID)]
    def draw_hollow(im):
        layer(im, lambda d: d.ellipse([HX - 70, HY - 14, HX + 70, HY + 14], fill=(0, 0, 0, 90)))
        im.alpha_composite(hf, (HX - 138, HY - 234))
        if HOLD: im.alpha_composite(*HOLD)
    draw_hollow(img)
    att = (cur + 1) if cur is not None else 1
    text_layer(img, [(TRYX, 1427, f'TRY {att}', 60, (255, 255, 255), 9, 255)])
    st = None
    for i, (k, t0, res, path, h, tend, nr, ex) in enumerate(SEQ):
        if res == 'fail' and 0 <= t - tend < 0.45: st = ('FROZEN!', (150, 220, 255), t - tend, 0.45)
    if 0 <= t - NEAR_T < 0.6 and st is None: st = ('SO CLOSE!', (255, 200, 70), t - NEAR_T, 0.6)
    if 0 <= t - T_ESC < 0.5: st = ('ESCAPED!', (120, 255, 120), t - T_ESC, 0.5)
    if st:
        txt, col, u, du = st; pop = 1.0 if u > 0.08 else 0.7 + 3.75 * u; a = int(255 * min(1, (du - u) / 0.1))
        fnt = F(int(96 * pop)); Ls = Image.new('RGBA', img.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(Ls); tw = ds.textlength(txt, font=fnt)
        ds.text((CX - tw / 2, CY - fnt.size / 2), txt, font=fnt, fill=col + (a,), stroke_width=10, stroke_fill=(10, 6, 18, a))
        img.alpha_composite(Ls)
    if t >= T_CARD:
        u = t - T_CARD; a = 1.0 if u > 0.1 else u / 0.1; pop = 1.0 if u > 0.1 else 0.8 + 2 * u
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(8, 6, 16, int(120 * a))))
        draw_hollow(img)   # keep the eating Hollow bright above the dim
        text_layer(img, [(CX, CY - 100, 'ESCAPED ON', int(76 * pop), (255, 214, 60), 10, int(255 * a)), (CX, CY - 4, f'TRY {len(SEQ)}!', int(76 * pop), (255, 214, 60), 10, int(255 * a))])
    if FLIGHT: img.alpha_composite(*FLIGHT)
    img.alpha_composite(HOOK)
    return img
if os.environ.get('FRAMES'):
    for f in [int(x) for x in os.environ['FRAMES'].split(',')]: frame(f).convert('RGB').save(f'k_{f}.png')
    sys.exit()
w = Writer('v64_noaudio.mp4')
for f in range(N): w.write(frame(f))
w.close(); json.dump({'events': sorted(ev)}, open('v64_ev.json', 'w')); print('done', END, N)
