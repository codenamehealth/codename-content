p='r64.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a; s=s.replace(a,b)
rep("def fail_ok(path, hits):", '''def vec_last(seeds, frozen, tstart):
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

def fail_ok(path, hits):''')
rep("""    for i, k in enumerate(KINDS):
        for s in (range(base * 1000 + i * 100, base * 1000 + i * 100 + 99) if i < 3 else range(500000 + base * 5000, 500000 + base * 5000 + 5000)):
            res = run_attempt(s, frozen, t, last=(i == 3))""","""    for i, k in enumerate(KINDS):
        if i == 3:
            seeds = list(range(500000 + base * 4000, 500000 + base * 4000 + 4000)); VR = []
            for c in range(0, len(seeds), 500): VR += vec_last(seeds[c:c + 500], frozen, t)
            print('base', base, 'try4 escapes', sum(1 for v in VR if v), flush=True)
        for si, s in enumerate(range(base * 1000 + i * 100, base * 1000 + i * 100 + 99) if i < 3 else seeds):
            res = run_attempt(s, frozen, t) if i < 3 else VR[si]""")
open(p,'w').write(s)
