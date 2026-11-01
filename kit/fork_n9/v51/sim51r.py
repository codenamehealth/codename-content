# r051 recut sim: bigger marbles (R 34->51), gate open at t=0, 1 zigzag (was 3),
# gummy bumpers -> neutral bumpers, gold boosts -> 4 typed product gummy pickups (one each, shuffled), consumed on touch.
import pymunk, math, random
W = 1080; R = 51
FPS = 30; SUB = 6
T_START = 0.0
DY = 1440  # two zigzags removed
def build(seed):
    rnd = random.Random(seed)
    sp = pymunk.Space(); sp.gravity = (0, 1800); sp.damping = 0.995
    st = sp.static_body
    segs = []; pegs = []; bumpers = []; spinners = []
    def seg(a, b, r=9, e=0.45, fr=0.6, kind='plank'):
        s = pymunk.Segment(st, a, b, r); s.elasticity = e; s.friction = fr; sp.add(s); segs.append((a, b, r, kind)); return s
    def peg(x, y, r=12, e=0.6, kind='peg'):
        c = pymunk.Circle(st, r, (x, y)); c.elasticity = e; c.friction = 0.4; sp.add(c); pegs.append([x, y, r, kind, c]); return c
    BOT = 6450 - DY
    seg((40, -400), (40, BOT + 400), 12, kind='wall'); seg((1040, -400), (1040, BOT + 400), 12, kind='wall')
    seg((40, 60), (430, 330)); seg((1040, 60), (650, 330))
    y = 520
    for row in range(9):
        off = 75 if row % 2 else 0
        for x in range(175 + off, 920, 150): peg(x, y)
        y += 110
    y = 1560
    seg((40, y), (760, y + 300), fr=0.15); seg((1040, y + 360), (320, y + 660), fr=0.15)
    y = 3850 - DY
    for k, (x, w) in enumerate([(340, 2.2), (740, -2.4), (340, -2.0), (740, 2.6)]):
        b = pymunk.Body(body_type=pymunk.Body.KINEMATIC); b.position = (x, y + k * 260); b.angular_velocity = w
        arms = []
        for a in range(4):
            ang = a * math.pi / 2; ex = (math.cos(ang) * 165, math.sin(ang) * 165)
            s = pymunk.Segment(b, (0, 0), ex, 10); s.elasticity = 0.5; s.friction = 0.5; arms.append(s)
        sp.add(b, *arms); spinners.append(b)
        if k < 3: peg(540, y + k * 260 + 130, 16)
    for ky in (5130, 5660, 5900):
        ky -= DY; seg((40, ky), (150, ky + 70), fr=0.2, kind='kick'); seg((1040, ky + 60), (930, ky + 130), fr=0.2, kind='kick')
    y = 4950 - DY
    pos = [(212, y), (540, y + 40), (868, y), (370, y + 260), (710, y + 260), (212, y + 520), (540, y + 560), (868, y + 520)]
    for (x, yy) in pos:
        c = pymunk.Circle(st, 46, (x, yy)); c.elasticity = 1.05; c.friction = 0.2; sp.add(c); bumpers.append([x, yy, 'bumper', c])
    kinds = ['mush', 'cre', 'mel', 'acv']; rnd.shuffle(kinds)
    ppos = [(430, 1680), (640, 2018), (370, y + 125), (710, y + 400)]
    pickups = [(x, yy, k) for (x, yy), k in zip(ppos, kinds)]
    y = 5750 - DY
    for row in range(3):
        off = 135 if row % 2 else 0
        for x in range(200 + off, 960, 270): peg(x, y + row * 150, 40, 0.5, 'ball')
    seg((40, 6180 - DY), (470, 6340 - DY)); seg((1040, 6180 - DY), (610, 6340 - DY))
    FIN = 6400 - DY
    marbles = {}
    xs = [480, 600]; rnd.shuffle(xs)
    for n, x in zip(['cleo', 'cyrus'], xs):
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, R)); b.position = (x + rnd.uniform(-6, 6), 200)
        c = pymunk.Circle(b, R); c.elasticity = 0.55; c.friction = 0.5; sp.add(b, c); marbles[n] = b
    return sp, segs, pegs, bumpers, spinners, pickups, marbles, FIN
def sim(seed, maxt=40):
    rnd = random.Random(seed * 7 + 1)
    sp, segs, pegs, bumpers, spinners, pickups, marbles, FIN = build(seed)
    frames = []; ev = []; fin = {}; used = {}  # pickup idx -> (t, who)
    lead = None; leads = []; bump_cool = {}
    strong = {}; frozen = {}; shield = {}; broken = {}  # broken: ('peg'|'bump', idx) -> t
    for f in range(int(maxt * FPS)):
        t = f / FPS
        for _ in range(SUB):
            sp.step(1 / FPS / SUB)
            for n, (t1, p) in frozen.items():
                if t < t1: marbles[n].position = p; marbles[n].velocity = (0, 0); marbles[n].angular_velocity = 0
        for n, b in marbles.items():
            if n in fin: continue
            v = b.velocity
            if abs(v.x) < 4 and abs(v.y) < 4 and t > 1 and not (n in frozen and t < frozen[n][0]): b.apply_impulse_at_local_point((rnd.choice([-1, 1]) * rnd.uniform(90, 160), -40))
            for i, (x, y, k) in enumerate(pickups):
                if i not in used and math.hypot(b.position.x - x, b.position.y - y) < R + 38:
                    used[i] = (t, n); ev.append((t, 'pick', n, k))
                    other = [m for m in marbles if m != n][0]
                    if k == 'mush': b.velocity = (b.velocity.x * 0.5, max(b.velocity.y, 0) + 700)
                    elif k == 'cre': strong[n] = t + 2.5
                    elif k == 'acv': shield[n] = t
                    elif k == 'mel' and other not in fin:
                        if other in shield: ev.append((t, 'block', other)); del shield[other]
                        else: frozen[other] = (t + 1.0, marbles[other].position); ev.append((t, 'sleep', other))
            if n in strong and t < strong[n]:
                for j, (x, y, r, kind, c) in enumerate(pegs):
                    if kind == 'ball' and ('peg', j) not in broken and math.hypot(b.position.x - x, b.position.y - y) < R + r + 8:
                        sp.remove(c); broken[('peg', j)] = t; ev.append((t, 'smash', n, x, y))
                for j, (x, y, kind, c) in enumerate(bumpers):
                    if ('bump', j) not in broken and math.hypot(b.position.x - x, b.position.y - y) < R + 46 + 8:
                        sp.remove(c); broken[('bump', j)] = t; ev.append((t, 'smash', n, x, y))
            for i, (x, y, kind, c) in enumerate(bumpers):
                if ('bump', i) not in broken and math.hypot(b.position.x - x, b.position.y - y) < R + 50 and t - bump_cool.get((n, i), -9) > 0.3:
                    bump_cool[(n, i)] = t; ev.append((t, 'bump', n))
            if b.position.y > FIN: fin[n] = t; ev.append((t, 'finish', n))
        order = sorted(marbles, key=lambda n: -(marbles[n].position.y if n not in fin else 1e9 - fin[n]))
        if order[0] != lead and (lead is None or abs(marbles[order[0]].position.y - marbles[order[1]].position.y) > 40 or order[0] in fin):
            lead = order[0]; leads.append((t, lead))
        frames.append(({n: (b.position.x, b.position.y, b.angle) for n, b in marbles.items()}, [s.angle for s in spinners], lead, dict(used),
                       {n: v for n, v in strong.items() if t < v}, {n: v[0] for n, v in frozen.items() if t < v[0]}, set(shield), dict(broken)))
        if len(fin) == 2 and t > max(fin.values()) + 0.1: break
    return frames, ev, fin, leads, segs, pegs, bumpers, spinners, pickups, FIN
def score(seed):
    fr, ev, fin, leads, *_ = sim(seed)
    if len(fin) < 2: return None
    w = min(fin, key=fin.get); tw = fin[w]; gap = abs(fin['cleo'] - fin['cyrus'])
    picks = [e for e in ev if e[1] == 'pick']
    return round(tw, 2), w, round(gap, 2), len(leads), len(picks), [(round(e[0], 1), e[2], e[3]) for e in picks], len([e for e in ev if e[1] == 'sleep']), len([e for e in ev if e[1] == 'smash'])
if __name__ == '__main__':
    import sys
    for s in range(int(sys.argv[1]), int(sys.argv[2])):
        r = score(s)
        if r: print(s, r, flush=True)
