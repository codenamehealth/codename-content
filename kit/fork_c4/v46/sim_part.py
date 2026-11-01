R = 22; SL = 0.5; T_START = 0.4
# ---------------- power gummies (SPEC 12): every gummy on the board does something
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'cre': ('STRONG!', (90, 160, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
SPEED_T, SPEED_K = 2.4, 1.6
STRONG_T = 2.8; SLEEP_T = 1.0; STUN_T = 0.75
POW_COLS = [int(c) for c in os.environ.get('PCOLS', '7,11,15,19,23,27,31,35').split(',')]
POW_TYPES = os.environ.get('PTYPES', 'cre,mush,acv,mel,mush,cre,mel,acv').split(',')
def traffic(seeds=(1, 2, 3)):
    tr = np.zeros((NR, NC))
    for sd in seeds:
        _, fr, _ = sim(sd, pows=[])
        for st, _, _ in fr[::3]:
            for s in st.values(): tr[min(NR - 1, max(0, int(round(s['y'] / C)))), min(NC - 1, max(0, int(round(s['x'] / C))))] += 1
    return tr
def place_pows(tr):
    out = []
    for c, k in zip(POW_COLS, POW_TYPES):
        best = None
        for cc in (c - 1, c, c + 1):
            for r in range(2, NR - 2):
                if CG[r, cc] and (r, cc) not in PROPS and all(CG[r + dr, cc + dc] for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                    if best is None or tr[r, cc] > best[0]: best = (tr[r, cc], r, cc)
        out.append((best[2] * C, best[1] * C, k))
    return out
def sim(seed, dur=24.0, pows=None):
    pows = POWS if pows is None else pows
    rnd = random.Random(seed); order = NAMES[:]; rnd.shuffle(order)
    rc = {}; props = set(PROPS); smashed = {}
    for i, n in enumerate(order):
        rc[n] = dict(x=1.4 * C, y=START_R[i] * C, vx=0.0, vy=0.0, base=rnd.uniform(255, 290), ph=rnd.uniform(0, 6.3), out=None, mode='side',
                     slide=-9, sdx=1.0, sdy=0.0, sliding=False, boost=None, dist=0.0, strong=None, shield=False, sleep=-9, stun=-9, hitcd={})
    taken = {}; frames = []; leaders = []; fx = []
    def pa(x, y): return cpt(x, y) in props
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        for n, s in rc.items():
            if s['out'] is not None or t < T_START: continue
            if t < s['sleep']: s['vx'] = s['vy'] = 0.0; s['sliding'] = False; continue
            stunned = t < s['stun']
            strong = s['strong'] is not None and t - s['strong'] < STRONG_T
            sliding = t - s['slide'] < SL or (s['slide'] > 0 and pa(s['x'], s['y']))
            sp = s['base'] * (1 + 0.28 * math.sin(0.8 * t + s['ph']) + 0.15 * math.sin(2.1 * t + 2 * s['ph']))
            if s['boost'] is not None and t - s['boost'] < SPEED_T: sp *= SPEED_K
            if stunned:
                s['vx'] *= 0.86; s['vy'] *= 0.86
            elif sliding:
                sp *= 1.2; s['vx'] += (s['sdx'] * sp - s['vx']) * 0.3; s['vy'] += (s['sdy'] * sp - s['vy']) * 0.3
            else:
                a, b = min(GR - 1, max(0, int(s['y'] // FC))), min(GCn - 1, max(0, int(s['x'] // FC)))
                gx, gy = -GX[a, b], -GY[a, b]; L = math.hypot(gx, gy) or 1
                wob = 0.4 * math.sin(3.3 * t + s['ph'] * 3); dx, dy = gx / L, gy / L
                tx, ty = dx - dy * wob, dy + dx * wob
                # gummies pull racers in when they are close and ahead (so every gummy gets used)
                for k, (px, py, kind) in enumerate(pows):
                    if k in taken: continue
                    ddx, ddy = px - s['x'], py - s['y']; dd = math.hypot(ddx, ddy)
                    if dd < 190 and ddx > -10:
                        w = 0.75 * (1 - dd / 190) + 0.25; tx, ty = tx * (1 - w) + ddx / dd * w, ty * (1 - w) + ddy / dd * w; break
                s['vx'] += (tx * sp - s['vx']) * 0.12; s['vy'] += (ty * sp - s['vy']) * 0.12
            v = math.hypot(s['vx'], s['vy']) or 1
            if not sliding and not stunned and t - s['slide'] > 1.0 and t > T_START + 0.6:
                ux, uy = s['vx'] / v, s['vy'] / v
                for d_ in (R + 10, R + 26):
                    cell = cpt(s['x'] + ux * d_, s['y'] + uy * d_)
                    if cell in props:
                        if strong:
                            props.discard(cell); smashed[cell] = t; fx.append((t, 'smash', n, cell))
                        else:
                            s['slide'] = t; s['sdx'], s['sdy'] = ux, uy; sliding = True
                        break
            nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
            for _ in range(2):
                for ax, ay in ((R, 0), (-R, 0), (0, R), (0, -R), (R * .7, R * .7), (-R * .7, R * .7), (R * .7, -R * .7), (-R * .7, -R * .7)):
                    if grass_at(nx + ax, ny + ay) or (not sliding and pa(nx + ax, ny + ay)):
                        if ax: nx -= ax * 0.18; s['vx'] *= -0.4
                        if ay: ny -= ay * 0.18; s['vy'] *= -0.4
            s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
            for m, o in rc.items():
                if m == n or o['out'] is not None: continue
                ddx, ddy = s['x'] - o['x'], (s['y'] - o['y']) * 1.6; dd = math.hypot(ddx, ddy)
                if strong and 0 < dd < 2 * R + 22 and t - s['hitcd'].get(m, -9) > 1.0 and t >= o['sleep']:
                    s['hitcd'][m] = t
                    if o['shield']:
                        o['shield'] = False; fx.append((t, 'block', m, n))
                    else:
                        o['stun'] = t + STUN_T; o['vx'] = -ddx / dd * 420; o['vy'] = -ddy / dd * 260; o['slide'] = -9
                        fx.append((t, 'hit', n, m))
                    continue
                if sliding or t - o['slide'] < SL: continue
                if 0 < dd < 2 * R + 8:
                    ahead = -(ddx * s['vx'] + ddy / 1.6 * s['vy']) > 0
                    if ahead and t - s['slide'] > 1.0 and t > T_START + 0.6 and not stunned:
                        s['slide'] = t; s['sdx'], s['sdy'] = s['vx'] / v, s['vy'] / v; sliding = True; continue
                    push = (2 * R + 8 - dd) / 2; s['x'] += ddx / dd * push * 0.8; s['y'] += ddy / dd * push * 0.5
            s['mode'] = 'down' if s['vy'] > 0.72 * v else 'side'; s['sliding'] = sliding and not stunned
            for k, (bx, by, kind) in enumerate(pows):
                if k not in taken and not stunned and math.hypot(s['x'] - bx, s['y'] - by) < 48:
                    taken[k] = (n, t); fx.append((t, 'pick', n, kind))
                    if kind == 'mush': s['boost'] = t
                    elif kind == 'cre': s['strong'] = t
                    elif kind == 'acv': s['shield'] = True; s['stun'] = -9
                    elif kind == 'mel':
                        vic, blk = [], []
                        for m, o in rc.items():
                            if m == n or o['out'] is not None: continue
                            if o['shield']: o['shield'] = False; blk.append(m); fx.append((t, 'block', m, n))
                            else: o['sleep'] = t + SLEEP_T; vic.append(m)
                        fx.append((t, 'sleepwave', n, vic))
            if s['x'] > FIN_X: s['out'] = t; s['shield'] = False
        def prog(s):
            if s['out'] is not None: return -1e6 + s['out']
            a, b = min(GR - 1, max(0, int(s['y'] // FC))), min(GCn - 1, max(0, int(s['x'] // FC)))
            return DEX[a, b] if not np.isinf(DEX[a, b]) else 1e5
        rank = sorted(rc, key=lambda n: prog(rc[n]))
        if t > T_START + 1 and (not leaders or leaders[-1] != rank[0]): leaders.append(rank[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], out=s['out'], mode=s['mode'], slide=s['slide'], sliding=s['sliding'],
                                boost=s['boost'], dist=s['dist'], strong=s['strong'], shield=s['shield'], sleep=s['sleep'], stun=s['stun']) for n, s in rc.items()}, rank, dict(taken)))
        if all(s['out'] is not None for s in rc.values()): break
    return rc, frames, leaders, fx, smashed
POWS = []
POWS = place_pows(traffic())
def score(seed):
    rc, fr, ld, fx, sm = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    if len(outs) < 4: return None
    t1, w = outs[0]; t2 = outs[1][0]
    if w != os.environ.get('WANT', 'cleo'): return None
    picks = [e for e in fx if e[1] == 'pick']
    if len(picks) < len(POWS): return None
    if not (9.0 < t1 < 14.5) or t2 - t1 > 0.6 or len(ld) < 5: return None
    if not any(e[1] == 'sleepwave' and len(e[3]) >= 2 for e in fx): return None
    nh = sum(e[1] == 'hit' for e in fx); nb = sum(e[1] == 'block' for e in fx)
    if nh < 1 or nb < 1: return None
    seq_ = [e[3] for e in picks]
    if seq_[:4] == seq_[4:8]: return None                       # never a fixed repeating order
    return round(t1, 2), w, round(t2 - t1, 2), len(ld), nh, nb, len(sm), seq_, [e[2] for e in picks]
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(sd)
        if r: print(sd, r, flush=True)
    sys.exit()
if len(sys.argv) > 1 and sys.argv[1] == 'map':
    print(POWS); sys.exit()
SEED = int(sys.argv[1])
RC, FR, LD, FX, SMASHED = sim(SEED)
OUTS = sorted((s['out'], n) for n, s in RC.items() if s['out'] is not None)
T_WIN, WIN = OUTS[0]
print('winner', WIN, round(T_WIN, 2), 'order', [(n, round(t, 2)) for t, n in OUTS], 'leaders', LD)
print('fx', [(round(e[0], 2), e[1], e[2], e[3]) for e in FX])
