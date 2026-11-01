import pymunk, math, random, os
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
GX, GY, GR = 478, 1030, 380
SC = GR / 420           # globe
CUPX, CUPY = 478, 950                  # cup rim centre
HUBY = GY + GR - 110                   # agitator hub
BR = int(os.environ.get('BR', '34'))                                # ball radius
FPS = 30
import os
CAP = int(os.environ.get('CAP', '90')); KLO = int(os.environ.get('KLO', '3')); KHI = int(os.environ.get('KHI', '6')); COOL = float(os.environ.get('COOL', '0.55'))
def run(seed, cap=CAP, tmax=31.0, record=True):
    rnd = random.Random(seed)
    sp = pymunk.Space(); sp.gravity = (0, 1500); sp.iterations = 12
    st = sp.static_body
    N = 90
    for i in range(N):
        a1, a2 = 2 * math.pi * i / N, 2 * math.pi * (i + 1) / N
        s = pymunk.Segment(st, (GX + GR * math.cos(a1), GY + GR * math.sin(a1)), (GX + GR * math.cos(a2), GY + GR * math.sin(a2)), 6)
        s.elasticity = 0.85; s.friction = 0.3; sp.add(s)
    cupsegs = [((CUPX - 70, CUPY - 46), (CUPX - 52, CUPY + 14)), ((CUPX - 52, CUPY + 14), (CUPX + 52, CUPY + 14)), ((CUPX + 52, CUPY + 14), (CUPX + 70, CUPY - 46)),
               ((CUPX, CUPY + 14), (CUPX, HUBY - 8))]
    for a, b in cupsegs:
        s = pymunk.Segment(st, a, b, 6); s.elasticity = 0.6; s.friction = 0.4; sp.add(s)
    # agitator paddle (kinematic, spinning)
    ag = pymunk.Body(body_type=pymunk.Body.KINEMATIC); ag.position = (GX, HUBY); ag.angular_velocity = 5.5
    sp.add(ag)
    for k in range(2):
        a = k * math.pi
        s = pymunk.Segment(ag, (0, 0), (158 * math.cos(a), 158 * math.sin(a)), 9); s.elasticity = 1.0; s.friction = 0.6; sp.add(s)
    balls = []; born = {}; T = 0.0
    def add(n, x, y, vx, vy):
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BR)); b.position = (x, y); b.velocity = (vx, vy)
        c = pymunk.Circle(b, BR); c.elasticity = 0.82; c.friction = 0.2; sp.add(b, c); balls.append((n, b, c)); born[id(b)] = T
    spots = [(GX + dx, GY - 230 + j * 72) for j in range(3) for dx in (-260, -190, -120, 120, 190, 260)]
    rnd.shuffle(spots); si = 0
    for n in NAMES:
        for j in range(3):
            x, y = spots[si]; si += 1
            add(n, x + rnd.uniform(-1, 1), y + rnd.uniform(-1, 1), rnd.uniform(-250, 250), rnd.uniform(-100, 100))
    frames = []; events = []; counts = {n: 3 for n in NAMES}; lead = []; cool = 0.0
    T = 0.0; dt = 1 / FPS; sub = 4
    pending = []
    while T < tmax:
        # burst spawns queued over a few frames so they do not overlap
        if pending:
            n, left = pending[0]
            for _ in range(min(3, left)):
                sd = rnd.choice([-1, 1]); add(n, CUPX + sd * rnd.uniform(20, 50), CUPY - 80 + rnd.uniform(-10, 10), sd * rnd.uniform(350, 800), rnd.uniform(-1000, -600))
                counts[n] += 1; left -= 1
            if left: pending[0] = (n, left)
            else: pending.pop(0)
        for _ in range(sub): sp.step(dt / sub)
        if rnd.random() < 0.02: ag.angular_velocity = rnd.choice([5.5, 6.2, -5.8])
        # cup hits
        for item in list(balls):
            n, b, c = item
            x, y = b.position
            if abs(x - CUPX) < 50 and CUPY - 40 < y < CUPY + 12 and T > cool and T - born[id(b)] > 1.2 and sum(counts.values()) < cap:
                sp.remove(b, c); balls.remove(item); counts[n] -= 1
                share = counts[n] / max(1, sum(counts.values())); k = max(2, round(rnd.randint(KLO, KHI) * (1.25 - share)))
                pending.append((n, k + 1)); events.append((round(T, 3), 'cup', n, k + 1)); cool = T + COOL
        tot = sum(counts.values())
        mx = max(counts.values()); ld = [n for n in NAMES if counts[n] == mx]
        if len(ld) == 1 and (not lead or lead[-1] != ld[0]): lead.append(ld[0])
        if record: frames.append(([(n, b.position.x, b.position.y) for n, b, c in balls], dict(counts), ag.angle))
        T += dt
        if tot >= cap and not pending: break
        if tot >= cap: pending.clear()
    return frames, events, counts, lead, T
if __name__ == '__main__':
    import sys
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        fr, ev, cnt, ld, T = run(seed, record=False)
        s = sorted(cnt.values(), reverse=True)
        print(seed, round(T, 1), len(ev), cnt, 'leads', len(ld), ld[-3:], flush=True)
