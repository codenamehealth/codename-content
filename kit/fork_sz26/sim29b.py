import math, random, json, sys
NAMES = ['joy', 'ray', 'cleo', 'cyrus']
NT = 4
ALIVE = [True] * NT
CNT = [1] * NT
def nxt(a):
    for s in range(1, NT):
        if ALIVE[(a + s) % NT]: return (a + s) % NT
    return None
def beats(a, b):
    if nxt(a) != b: return False
    if sum(ALIVE) == 2: return CNT[a] >= CNT[b]   # final duel: the bigger army presses
    return True
#       # a converts the next living army in the cycle joy > cyrus > cleo > ray > joy
AX0, AY0, AX1, AY1 = 75, 640, 1010, 1500
NOTCH_Y, NOTCH_X = 1100, 862
FPS = 30
def sim(seed, N=16, dur=62.0):
    global ALIVE, CNT
    ALIVE = [True] * NT; CNT = [N] * NT
    rnd = random.Random(seed)
    U = []
    for k in range(NT):
        ang = -math.pi * 3 / 4 + k * math.pi / 2
        cx = AX0 + (AX1 - AX0 - 150) * (0.5 + 0.33 * math.cos(ang)); cy = AY0 + 60 + (AY1 - AY0 - 60) * (0.5 + 0.33 * math.sin(ang))
        for i in range(N):
            U.append(dict(t=k, x=cx + rnd.uniform(-90, 90), y=cy + rnd.uniform(-90, 90), vx=0.0, vy=0.0, sp=rnd.uniform(120, 175), ph=rnd.uniform(0, 6.3), shield=-9, flash=-9, dist=0.0))
    gums = []; nextg = 4.0; frames = []; events = []; leaders = []; end = None
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= nextg and len(gums) < 2:
            gy_ = rnd.uniform(AY0 + 100, AY1 - 60); gums.append(dict(x=rnd.uniform(AX0 + 80, (NOTCH_X if gy_ > NOTCH_Y - 40 else AX1) - 80), y=gy_, k=rnd.choice(['mush', 'acv', 'mel', 'cre', 'gold']), t0=t)); nextg = t + rnd.uniform(4.5, 7.0)
        if end is None:
            for u in U:
                # nearest prey / predator
                bp, bd = None, 1e9; pp, pd = None, 1e9
                for o in U:
                    if o is u: continue
                    d = math.hypot(o['x'] - u['x'], o['y'] - u['y'])
                    if beats(u['t'], o['t']) and d < bd and t - o['shield'] > 4.0: bp, bd = o, d
                    if beats(o['t'], u['t']) and d < pd: pp, pd = o, d
                ax = ay = 0.0
                if bp is not None: ax += (bp['x'] - u['x']) / (bd + 1); ay += (bp['y'] - u['y']) / (bd + 1)
                if pp is not None and pd < 260 and t - u['shield'] > 4.0: k = 1.3 * (1 - pd / 260); ax -= k * (pp['x'] - u['x']) / (pd + 1); ay -= k * (pp['y'] - u['y']) / (pd + 1)
                for g in gums:
                    d = math.hypot(g['x'] - u['x'], g['y'] - u['y'])
                    if d < 220: ax += 0.8 * (g['x'] - u['x']) / (d + 1); ay += 0.8 * (g['y'] - u['y']) / (d + 1)
                a = t * 0.9 + u['ph']; ax += 0.35 * math.cos(a); ay += 0.35 * math.sin(a * 1.3)
                L = math.hypot(ax, ay) or 1; sp = u['sp'] * (1.5 if t - u['shield'] < 4.0 else 1.0)
                u['vx'] += (ax / L * sp - u['vx']) * 0.1; u['vy'] += (ay / L * sp - u['vy']) * 0.1
                nx = min(AX1 - 20, max(AX0 + 20, u['x'] + u['vx'] * dt)); ny = min(AY1 - 10, max(AY0 + 60, u['y'] + u['vy'] * dt))
                if ny > NOTCH_Y: nx = min(nx, NOTCH_X)
                u['dist'] += math.hypot(nx - u['x'], ny - u['y']); u['x'], u['y'] = nx, ny
            # separation
            for i, u in enumerate(U):
                for o in U[i + 1:]:
                    dx, dy = u['x'] - o['x'], u['y'] - o['y']; d = math.hypot(dx, dy)
                    if 0 < d < 34 and u['t'] == o['t']: p = (34 - d) / 2; u['x'] += dx / d * p; u['y'] += dy / d * p; o['x'] -= dx / d * p; o['y'] -= dy / d * p
            # conversions
            for u in U:
                for o in U:
                    if o is u or not beats(u['t'], o['t']) or t - o['shield'] < 4.0: continue
                    if math.hypot(o['x'] - u['x'], o['y'] - u['y']) < 30 and t - o['flash'] > 0.4:
                        o['t'] = u['t']; o['flash'] = t; events.append((round(t, 3), 'conv', o['x'], o['y'], u['t']))
            for g in list(gums):
                for u in U:
                    if math.hypot(g['x'] - u['x'], g['y'] - u['y']) < 36:
                        u['shield'] = t; gums.remove(g); events.append((round(t, 3), 'gum', u['x'], u['y'], u['t'])); break
            cnt = [sum(1 for u in U if u['t'] == k) for k in range(NT)]
            ALIVE = [c > 0 for c in cnt]; CNT = cnt
            mx = max(cnt); ld = [k for k in range(NT) if cnt[k] == mx]
            if len(ld) == 1 and (not leaders or leaders[-1] != ld[0]): leaders.append(ld[0])
            if mx == len(U): end = (t, ld[0])
        frames.append(([(u['t'], u['x'], u['y'], u['vx'], u['dist'], t - u['shield'] < 4.0, u['flash']) for u in U], [dict(g) for g in gums]))
        if end and t > end[0] + 3.5: break
    return frames, events, end, leaders
if __name__ == '__main__':
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        fr, ev, end, ld = sim(seed)
        conv = sum(1 for e in ev if e[1] == 'conv')
        print(seed, end and (round(end[0], 1), NAMES[end[1]]), 'conv', conv, 'leaders', len(ld), [NAMES[k] for k in ld[-4:]], flush=True)
