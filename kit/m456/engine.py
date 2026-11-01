# Shared pure-physics engine for the m04-m06 reference recreations.
# World = screen px. Grid of C px cells (walls / breakables / hazards). Boxes: constant speed, straight lines, reflect only on
# contact (walls, intact breakables, other boxes, the moving flood front). Flood = list of rectangular segments, each with a
# straight front moving in one direction at its own speed on a shared flood clock that pauses while an intact flood-stopping
# breakable lies under the front. A box pinned so the front would overlap it is crushed.
import math, random, zlib
import numpy as np

class World:
    def __init__(self, cols, rows, C, OX, OY):
        self.cols, self.rows, self.C, self.OX, self.OY = cols, rows, C, OX, OY
        self.wall = np.ones((rows, cols), bool)
        self.brk = np.zeros((rows, cols), np.int16)      # breakable id (1-based) or 0
        self.haz = np.zeros((rows, cols), np.int16)      # hazard id (1-based) or 0
        self.B = []                                      # breakables
        self.H = []                                      # hazards
        self.segs = []                                   # flood segments
        self.exits = []                                  # exit rects (world px) -> win when the box is fully inside
    # ---- building (u = cell units)
    def floor(self, x0, y0, x1, y1): self.wall[y0:y1, x0:x1] = False
    def solid(self, x0, y0, x1, y1): self.wall[y0:y1, x0:x1] = True
    def breakable(self, x0, y0, x1, y1, hp, owner=None, kind='block', stops_flood=True, regen=False, stop_at=None):
        self.wall[y0:y1, x0:x1] = False
        self.B.append(dict(rect=(x0, y0, x1, y1), hp=hp, hp0=hp, owner=owner, kind=kind, stops=stops_flood, regen=regen, stop_at=stop_at))
        self.brk[y0:y1, x0:x1] = len(self.B); return len(self.B) - 1
    def hazard(self, x0, y0, x1, y1, name):
        self.H.append(dict(rect=(x0, y0, x1, y1), name=name)); self.haz[y0:y1, x0:x1] = len(self.H)
    def seg(self, x0, y0, x1, y1, d, t0, v):
        """flood segment over cells [x0,x1)x[y0,y1): front enters from the side opposite to d ('+x','-x','+y','-y') at flood-clock
        t0 and moves at v px/s. Returns the clock time it is full."""
        L = ((x1 - x0) if d[1] == 'x' else (y1 - y0)) * self.C
        self.segs.append(dict(r=(x0, y0, x1, y1), d=d, t0=t0, v=v, L=L)); return t0 + L / v
    def px(self, x0, y0, x1, y1): C = self.C; return (self.OX + x0 * C, self.OY + y0 * C, self.OX + x1 * C, self.OY + y1 * C)
    # ---- flood geometry at flood-clock tau
    def flood_rects(self, tau):
        out = []
        for s in self.segs:
            if tau <= s['t0']: continue
            k = min(s['L'], (tau - s['t0']) * s['v'])
            X0, Y0, X1, Y1 = self.px(*s['r'])
            if s['d'] == '+x': out.append((X0, Y0, X0 + k, Y1, s['d']))
            elif s['d'] == '-x': out.append((X1 - k, Y0, X1, Y1, s['d']))
            elif s['d'] == '+y': out.append((X0, Y0, X1, Y0 + k, s['d']))
            else: out.append((X0, Y1 - k, X1, Y1, s['d']))
        return out
    def seg_time_at(self, s, cx, cy):
        """flood-clock time the front of segment s reaches cell (cx, cy) (cell's first edge)"""
        x0, y0, x1, y1 = s['r']; C = self.C
        if s['d'] == '+x': k = (cx - x0) * C
        elif s['d'] == '-x': k = (x1 - 1 - cx) * C
        elif s['d'] == '+y': k = (cy - y0) * C
        else: k = (y1 - 1 - cy) * C
        return s['t0'] + k / s['v']
    def brk_flood_time(self, i):
        """earliest flood-clock time any segment reaches breakable i"""
        x0, y0, x1, y1 = self.B[i]['rect']; best = 1e9
        for s in self.segs:
            sx0, sy0, sx1, sy1 = s['r']
            ax0, ay0, ax1, ay1 = max(x0, sx0), max(y0, sy0), min(x1, sx1), min(y1, sy1)
            if ax0 >= ax1 or ay0 >= ay1: continue
            for cy in (ay0, ay1 - 1):
                for cx in (ax0, ax1 - 1): best = min(best, self.seg_time_at(s, cx, cy))
        return best

def sim(Wd, boxes, seed, dur, SPD, HS, FPS=30, SUB=8, t_go=0.0, flood_t0=0.0, jitter=0.026, gummy=None, gum_cool=0.4,
        win_rule='exit', hit_cool=0.05, LP=100000, stop_on_win=False, post_win=2.6, regen_rate=0.0, keep_winner=True, seed2=None, t_split=None):
    """boxes: list of dict(g, x, y, vx, vy). Returns dict with frames + events."""
    rnd = random.Random(seed); C, OX, OY = Wd.C, Wd.OX, Wd.OY
    B = [dict(b) for b in Wd.B]
    for b in B: b['hits'] = []; b['broke'] = None
    X = {b['g']: dict(x=b['x'], y=b['y'], vx=b['vx'], vy=b['vy'], out=None, how=None, last={}, hold=False, won=None) for b in boxes}
    G = [b['g'] for b in boxes]
    brk_tf = [b['stop_at'] if b.get('stop_at') is not None else Wd.brk_flood_time(i) for i, b in enumerate(B)]
    gum = dict(gummy) if gummy else None
    if gum: gum.update(holder=None, t_drop=-9, picks=[], kills=[])
    ev = []; frames = []; contacts = []; tau = 0.0; win = None; t_end = dur
    def solid_cell(r, c):
        if r < 0 or c < 0 or r >= Wd.rows or c >= Wd.cols: return 'wall'
        if Wd.wall[r, c]: return 'wall'
        k = Wd.brk[r, c]
        if k and B[k - 1]['hp'] > 0: return k - 1
        return None
    def overl_solid(x, y):
        r0, r1 = int((y - HS - OY) // C), int((y + HS - OY - 1e-6) // C); c0, c1 = int((x - HS - OX) // C), int((x + HS - OX - 1e-6) // C)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if solid_cell(r, c) is not None: return True
        return False
    def behind_ok(p, x0, y0, x1, y1, d):
        # a segment only acts on a box whose centre is past the segment's start edge (the source side belongs to the previous segment)
        if d == '-y': return p['y'] < y1
        if d == '+y': return p['y'] > y0
        if d == '+x': return p['x'] > x0
        return p['x'] < x1
    def jit(p, key):
        # bounce jitter stream: `seed`, switching to `seed2` from t_split on (a seed spec 'A:T:B'); same physics either way
        if seed2 is None or t < t_split[0] if isinstance(t_split, (list, tuple)) else (seed2 is None or t < t_split): sd = seed
        elif isinstance(t_split, (list, tuple)): sd = (seed,) + tuple(b_ for T_, b_ in zip(t_split, seed2) if t >= T_)
        else: sd = (seed, seed2)
        a = ((zlib.crc32(repr((sd, key)).encode()) % 10007) / 10007.0 - 0.5) * 2 * jitter
        vx, vy = p['vx'], p['vy']; p['vx'], p['vy'] = vx * math.cos(a) - vy * math.sin(a), vx * math.sin(a) + vy * math.cos(a)
    nf = int(dur * FPS)
    for f in range(nf):
        t = f / FPS; dt = 1.0 / FPS / SUB; CF = {g: False for g in G}
        for _ in range(SUB if t >= t_go else 0):
            # flood clock: pauses while an intact flood-stopping breakable lies at the front
            if t >= flood_t0:
                nt = tau + dt
                for i, b in enumerate(B):
                    if b['hp'] > 0 and b['stops'] and brk_tf[i] < nt: nt = min(nt, max(tau, brk_tf[i] - 1e-4))
                tau = nt
            live = [g for g in G if X[g]['out'] is None and X[g]['won'] is None]
            for g in live:
                p = X[g]
                for ax in ('x', 'y'):
                    v = p['v' + ax]; p[ax] += v * dt
                    if v == 0: continue
                    if ax == 'x':
                        edge = p['x'] + HS if v > 0 else p['x'] - HS
                        c = int((edge - OX - (1e-6 if v > 0 else 0)) // C) if v > 0 else int((edge - OX) // C)
                        r0, r1 = int((p['y'] - HS - OY) // C), int((p['y'] + HS - OY - 1e-6) // C); cells = [(r, c) for r in range(r0, r1 + 1)]
                    else:
                        edge = p['y'] + HS if v > 0 else p['y'] - HS
                        r = int((edge - OY - 1e-6) // C) if v > 0 else int((edge - OY) // C)
                        c0, c1 = int((p['x'] - HS - OX) // C), int((p['x'] + HS - OX - 1e-6) // C); cells = [(r, c) for c in range(c0, c1 + 1)]
                    hit = None
                    for (r, c) in cells:
                        k = solid_cell(r, c)
                        if k is None: continue
                        if hit is None or hit == 'wall': hit = k
                    if hit is None: continue
                    # snap to the cell boundary (exact AABB contact) and reflect
                    if ax == 'x': p['x'] = (OX + c * C - HS) if v > 0 else (OX + (c + 1) * C + HS)
                    else: p['y'] = (OY + r * C - HS) if v > 0 else (OY + (r + 1) * C + HS)
                    p['v' + ax] = -v; CF[g] = True
                    jit(p, (ax, round(p['x'] - OX) if ax == 'y' else 0, round(p['y'] - OY) % LP if ax == 'x' else 0, v > 0))
                    if hit != 'wall':
                        b = B[hit]
                        if b['owner'] is None or b['owner'] == g:
                            if t - p['last'].get(hit, -9) > hit_cool:
                                p['last'][hit] = t; b['hits'].append((t, g, p['x'], p['y'])); ev.append((t, 'hit', g, hit))
                                if not b['regen']:
                                    b['hp'] -= 1
                                    if b['hp'] <= 0: b['broke'] = t; ev.append((t, 'break', g, hit))
                        else:
                            ev.append((t, 'bounce_gate', g, hit))
            # flood front pushes (moving wall)
            FR = Wd.flood_rects(tau)
            for g in live:
                p = X[g]
                for (x0, y0, x1, y1, d) in FR:
                    if p['x'] + HS <= x0 or p['x'] - HS >= x1 or p['y'] + HS <= y0 or p['y'] - HS >= y1: continue
                    if not behind_ok(p, x0, y0, x1, y1, d): continue
                    if d == '+x': p['x'] = x1 + HS; (p['vx'] < 0) and p.update(vx=-p['vx'])
                    elif d == '-x': p['x'] = x0 - HS; (p['vx'] > 0) and p.update(vx=-p['vx'])
                    elif d == '+y': p['y'] = y1 + HS; (p['vy'] < 0) and p.update(vy=-p['vy'])
                    else: p['y'] = y0 - HS; (p['vy'] > 0) and p.update(vy=-p['vy'])
                    CF[g] = True
                    if overl_solid(p['x'], p['y']): p['out'] = t; p['how'] = 'crush'; ev.append((t, 'out', g, 'crush'))
            live = [g for g in G if X[g]['out'] is None and X[g]['won'] is None]
            # box-box: each reflects off the other like off a wall (own speed and angle)
            for i in range(len(live)):
                for j in range(i + 1, len(live)):
                    a_, b_ = X[live[i]], X[live[j]]
                    px_, py_ = 2 * HS - abs(a_['x'] - b_['x']), 2 * HS - abs(a_['y'] - b_['y'])
                    if px_ <= 0 or py_ <= 0: continue
                    ax = 'x' if px_ < py_ else 'y'; pen = px_ if ax == 'x' else py_
                    s = 1 if a_[ax] < b_[ax] else -1
                    # separate: half each, but a box against a wall stays put and the other takes the whole gap
                    a0, b0 = a_[ax], b_[ax]
                    a_[ax] = a0 - s * pen / 2; b_[ax] = b0 + s * pen / 2
                    if overl_solid(a_['x'], a_['y']): a_[ax] = a0; b_[ax] = b0 + s * pen
                    elif overl_solid(b_['x'], b_['y']): b_[ax] = b0; a_[ax] = a0 - s * pen
                    if overl_solid(a_['x'], a_['y']) or overl_solid(b_['x'], b_['y']): a_[ax], b_[ax] = a0, b0   # pinched: leave it (crush check decides)
                    if a_['v' + ax] * s > 0: a_['v' + ax] = -a_['v' + ax]
                    if b_['v' + ax] * s < 0: b_['v' + ax] = -b_['v' + ax]
                    CF[live[i]] = CF[live[j]] = True
                    ev.append((t, 'bump', live[i], live[j]))
                    if gum and gum['holder'] in (live[i], live[j]):          # STRENGTH: the holder's next contact knocks the other out
                        h = gum['holder']; vic = live[j] if h == live[i] else live[i]
                        X[vic]['out'] = t; X[vic]['how'] = 'gummy'; ev.append((t, 'out', vic, 'gummy', h))
                        gum['holder'] = None; gum['x'], gum['y'] = X[vic]['x'], X[vic]['y']; gum['t_drop'] = t; gum['kills'].append((t, h, vic))
            # crush check: a box still overlapping the flood or a solid after all resolutions is pinned
            FR = Wd.flood_rects(tau)
            for g in [g for g in G if X[g]['out'] is None and X[g]['won'] is None]:
                p = X[g]
                pin = False
                for (x0, y0, x1, y1, d) in FR:
                    if not behind_ok(p, x0, y0, x1, y1, d): continue
                    ox = min(x1, p['x'] + HS) - max(x0, p['x'] - HS); oy = min(y1, p['y'] + HS) - max(y0, p['y'] - HS)
                    if ox > 1.5 and oy > 1.5: pin = True
                if pin: p['out'] = t; p['how'] = 'crush'; ev.append((t, 'out', g, 'crush'))
            # constant speed (reflections and jitter preserve it; guard float drift only)
            for g in G:
                p = X[g]; v = math.hypot(p['vx'], p['vy'])
                if v: p['vx'] *= SPD / v; p['vy'] *= SPD / v
        # per-frame: hazards, gummy, exits
        for g in G:
            p = X[g]
            if p['out'] is not None or p['won'] is not None or t < t_go: continue
            r0, r1 = int((p['y'] - HS - OY) // C), int((p['y'] + HS - OY - 1e-6) // C); c0, c1 = int((p['x'] - HS - OX) // C), int((p['x'] + HS - OX - 1e-6) // C)
            hz = Wd.haz[max(0, r0):r1 + 1, max(0, c0):c1 + 1]
            if hz.any():
                hid = int(hz.max()) - 1; hx0, hy0, hx1, hy1 = Wd.px(*Wd.H[hid]['rect'])
                sub = any(y0 <= hy0 and x0 <= hx0 < x1 for (x0, y0, x1, y1, d) in Wd.flood_rects(tau))
                if not sub: p['out'] = t; p['how'] = 'hazard'; ev.append((t, 'out', g, 'hazard', hid))
            if gum and gum['holder'] is None and t - gum['t_drop'] > gum_cool and abs(p['x'] - gum['x']) < HS + gum['r'] and abs(p['y'] - gum['y']) < HS + gum['r']:
                gum['holder'] = g; gum['picks'].append((t, g)); ev.append((t, 'pick', g))
            for (ex0, ey0, ex1, ey1) in Wd.exits:
                if win is None and ex0 <= p['x'] - HS and p['x'] + HS <= ex1 and ey0 <= p['y'] - HS and p['y'] + HS <= ey1:
                    p['won'] = t; win = (t, g); ev.append((t, 'win', g)); t_end = min(dur, t + post_win)
        if win_rule == 'last':
            alive = [g for g in G if X[g]['out'] is None]
            if win is None and len(alive) == 1: win = (t, alive[0]); ev.append((t, 'win', alive[0])); t_end = min(dur, t + post_win)
        contacts.append(CF)
        frames.append(({g: (X[g]['x'], X[g]['y'], X[g]['vx'], X[g]['vy'], X[g]['out'], X[g]['won']) for g in G}, tau,
                       [b['hp'] for b in B], None if not gum else (gum['x'], gum['y'], gum['holder'])))
        if t >= t_end or all(X[g]['out'] is not None for g in G): break
    return dict(X=X, frames=frames, ev=ev, B=B, gum=gum, win=win, contacts=contacts, t_end=t_end)

def selfcheck(res, G, HS, FPS=30):
    """direction changes on frames with no contact must be 0; also max overlap between boxes"""
    fr = res['frames']; cont = res['contacts']; bad = {g: 0 for g in G}; changes = {g: 0 for g in G}; ovl = 0.0
    for i in range(1, len(fr)):
        for g in G:
            a, b = fr[i - 1][0][g], fr[i][0][g]
            if a[4] is not None or b[4] is not None or a[5] is not None or b[5] is not None: continue
            ang = math.atan2(b[3], b[2]) - math.atan2(a[3], a[2]); ang = abs((ang + math.pi) % (2 * math.pi) - math.pi)
            if ang > 1e-6:
                changes[g] += 1
                if not cont[i][g]: bad[g] += 1
        live = [g for g in G if fr[i][0][g][4] is None and fr[i][0][g][5] is None]
        for x in range(len(live)):
            for y in range(x + 1, len(live)):
                p, q = fr[i][0][live[x]], fr[i][0][live[y]]
                ovl = max(ovl, min(2 * HS - abs(p[0] - q[0]), 2 * HS - abs(p[1] - q[1])))
    return bad, changes, ovl

def parse_seed(seed):
    """seed spec: int, or 'A:T:B' = jitter stream A until T seconds, then stream B, or 'A:T1:B1:T2:B2...' (streams chained).
    Returns (A, B or [B..] or None, T or [T..] or None)."""
    if isinstance(seed, str) and ':' in seed:
        p = seed.split(':'); a = int(p[0]); Ts = [float(x) for x in p[1::2]]; Bs = [int(x) for x in p[2::2]]
        if len(Ts) == 1: return a, Bs[0], Ts[0]
        return a, Bs, Ts
    return int(seed), None, None
