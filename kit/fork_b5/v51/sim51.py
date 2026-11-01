import pymunk, math, random
W = 1080; R = 34
FPS = 30; SUB = 6
T_START = 3.2
def build(seed):
    rnd = random.Random(seed)
    sp = pymunk.Space(); sp.gravity = (0, 1800); sp.damping = 0.995
    st = sp.static_body
    segs = []; pegs = []; bumpers = []; spinners = []; boosts = []
    def seg(a, b, r=9, e=0.45, fr=0.6, kind='plank'):
        s = pymunk.Segment(st, a, b, r); s.elasticity = e; s.friction = fr; sp.add(s); segs.append((a, b, r, kind)); return s
    def peg(x, y, r=12, e=0.6, kind='peg'):
        c = pymunk.Circle(st, r, (x, y)); c.elasticity = e; c.friction = 0.4; sp.add(c); pegs.append((x, y, r, kind)); return c
    TOP = 0; BOT = 6450
    seg((40, -400), (40, BOT + 400), 12, kind='wall'); seg((1040, -400), (1040, BOT + 400), 12, kind='wall')
    # start funnel + gate
    seg((40, 60), (455, 330)); seg((1040, 60), (625, 330))
    gate = pymunk.Segment(st, (440, 345), (640, 345), 9); gate.elasticity = 0.2; sp.add(gate)
    # 1 plinko
    y = 520
    for row in range(9):
        off = 60 if row % 2 else 0
        for x in range(110 + off, 1000, 120): peg(x, y)
        y += 110
    # 2 zigzag planks
    y = 1560
    for k in range(3):
        seg((40, y), (760, y + 300), fr=0.15); seg((1040, y + 360), (320, y + 660), fr=0.15); y += 720
    # 3 spinners
    y = 3850
    for k, (x, w) in enumerate([(310, 2.2), (770, -2.4), (310, -2.0), (770, 2.6)]):
        b = pymunk.Body(body_type=pymunk.Body.KINEMATIC); b.position = (x, y + k * 260); b.angular_velocity = w
        arms = []
        for a in range(4):
            ang = a * math.pi / 2; ex = (math.cos(ang) * 165, math.sin(ang) * 165)
            s = pymunk.Segment(b, (0, 0), ex, 10); s.elasticity = 0.5; s.friction = 0.5; arms.append(s)
        sp.add(b, *arms); spinners.append(b)
        if k < 3: peg(540, y + k * 260 + 130, 16)
    # wall kickers so nobody hugs the wall through the gummy field
    for ky in (4870, 5130, 5390, 5660, 5900):
        seg((40, ky), (230, ky + 110), fr=0.2, kind='kick'); seg((1040, ky + 60), (850, ky + 170), fr=0.2, kind='kick')
    # 4 gummy bumpers + boosts
    y = 4950
    kinds = ['mush', 'cre', 'acv', 'mel', 'mush', 'cre', 'mel', 'acv']
    pos = [(200, y), (540, y + 40), (880, y), (360, y + 260), (720, y + 260), (200, y + 520), (540, y + 560), (880, y + 520)]
    for (x, yy), kd in zip(pos, kinds):
        c = pymunk.Circle(st, 46, (x, yy)); c.elasticity = 1.05; c.friction = 0.2; sp.add(c); bumpers.append((x, yy, kd))
    boosts = [(360, y + 120, 'gold'), (720, y + 400, 'gold'), (540, y - 230, 'gold')]
    # 5 big pegs
    y = 5750
    for row in range(3):
        off = 135 if row % 2 else 0
        for x in range(170 + off, 960, 270): peg(x, y + row * 150, 40, 0.5, 'ball')
    # 6 funnel to finish
    seg((40, 6180), (470, 6340)); seg((1040, 6180), (610, 6340))
    FIN = 6400
    marbles = {}
    xs = [490, 590]; rnd.shuffle(xs)
    for n, x in zip(['cleo', 'cyrus'], xs):
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, R)); b.position = (x + rnd.uniform(-6, 6), 230)
        c = pymunk.Circle(b, R); c.elasticity = 0.55; c.friction = 0.5; sp.add(b, c); marbles[n] = b
    return sp, gate, segs, pegs, bumpers, spinners, boosts, marbles, FIN
def sim(seed, maxt=60):
    rnd = random.Random(seed * 7 + 1)
    sp, gate, segs, pegs, bumpers, spinners, boosts, marbles, FIN = build(seed)
    frames = []; ev = []; fin = {}; used = set(); boosted = {}
    lead = None; leads = []; gate_open = False; bump_cool = {}
    for f in range(int(maxt * FPS)):
        t = f / FPS
        if t >= T_START and not gate_open: sp.remove(gate); gate_open = True; ev.append((t, 'go'))
        for _ in range(SUB):
            sp.step(1 / FPS / SUB)
        for n, b in marbles.items():
            if n in fin: continue
            v = b.velocity
            if abs(v.x) < 4 and abs(v.y) < 4 and t > T_START + 1: b.apply_impulse_at_local_point((rnd.uniform(-60, 60), -20))
            for i, (x, y, k) in enumerate(boosts):
                if (n, i) not in used and math.hypot(b.position.x - x, b.position.y - y) < R + 30:
                    used.add((n, i)); b.velocity = (b.velocity.x * 0.5, max(b.velocity.y, 0) + 650); boosted[n] = t; ev.append((t, 'boost', n))
            for i, (x, y, k) in enumerate(bumpers):
                if math.hypot(b.position.x - x, b.position.y - y) < R + 50 and t - bump_cool.get((n, i), -9) > 0.3:
                    bump_cool[(n, i)] = t; ev.append((t, 'bump', n))
            if b.position.y > FIN: fin[n] = t; ev.append((t, 'finish', n))
        if gate_open:
            order = sorted(marbles, key=lambda n: -(marbles[n].position.y if n not in fin else 1e9 - fin[n]))
            if order[0] != lead and (lead is None or abs(marbles[order[0]].position.y - marbles[order[1]].position.y) > 40 or order[0] in fin):
                lead = order[0]; leads.append((t, lead))
        frames.append(({n: (b.position.x, b.position.y, b.angle) for n, b in marbles.items()}, [s.angle for s in spinners], lead, set(used)))
        if len(fin) == 2 and t > max(fin.values()) + 0.1: break
    return frames, ev, fin, leads, segs, pegs, bumpers, spinners, boosts, FIN
def score(seed):
    fr, ev, fin, leads, *_ = sim(seed)
    if len(fin) < 2: return None
    w = min(fin, key=fin.get); tw = fin[w]; gap = abs(fin['cleo'] - fin['cyrus'])
    nl = len(leads)
    nb = len([e for e in ev if e[1] == 'boost']); nbump = len([e for e in ev if e[1] == 'bump'])
    if not (22 < tw < 30) or nl < 4 or gap > 0.8 or nb < 1 or nbump < 4: return None
    return round(tw, 2), w, round(gap, 2), nl, nb, nbump
if __name__ == '__main__':
    import sys
    for s in range(int(sys.argv[1]), int(sys.argv[2])):
        fr, ev, fin, leads, *_ = sim(s)
        print(s, {k: round(v, 1) for k, v in fin.items()}, len(leads), flush=True)
