import pymunk, math, random, os
NAMES = ['joy', 'cyrus', 'cleo', 'ray']   # Hollow removed: he is the player, never a racer/pick option (SPEC 8)
GX, GY, GR = 540, 1134, 336   # recut: globe 380->336 so the 2x scoreboard fits above it (balls keep their size)
SC = GR / 420           # globe
CUPX, CUPY = GX, GY - 80                  # cup rim centre
# FIX (gummies falling out): the old hub sat 110px above the bottom of the glass but each paddle arm reached 167px,
# so the arm swept ~57px OUTSIDE the glass every turn; it is a kinematic (unstoppable) body, so any gummy in its way
# was shoved straight through the glass. Now the hub is higher and the arms shorter, so the whole sweep stays inside
# with a gap bigger than a gummy (97px) to the glass AND to the cup, so nothing can be wedged and squeezed out.
HUBY = GY + int(os.environ.get('HUBH', '175'))   # agitator hub
ARM = int(os.environ.get('ARM', '135'))           # paddle arm length (+9 radius)
OMEGA = float(os.environ.get('OMEGA', '5.5'))
BR = int(os.environ.get('BR', '34'))                                # ball radius
FPS = 30
NUDGE = [0]
import os
CAP = int(os.environ.get('CAP', '66')); KLO = int(os.environ.get('KLO', '3')); KHI = int(os.environ.get('KHI', '6')); COOL = float(os.environ.get('COOL', '0.45')); B0 = float(os.environ.get('B0', '1.6')); B1 = float(os.environ.get('B1', '2.0'))
def run(seed, cap=CAP, tmax=31.0, record=True, settle=18):
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
    ag = pymunk.Body(body_type=pymunk.Body.KINEMATIC); ag.position = (GX, HUBY); ag.angular_velocity = OMEGA
    sp.add(ag)
    for k in range(2):
        a = k * math.pi
        s = pymunk.Segment(ag, (0, 0), (ARM * math.cos(a), ARM * math.sin(a)), 9); s.elasticity = 1.0; s.friction = 0.6; sp.add(s)
    balls = []; born = {}; T = 0.0
    def add(n, x, y, vx, vy):
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BR)); b.position = (x, y); b.velocity = (vx, vy)
        c = pymunk.Circle(b, BR); c.elasticity = 0.82; c.friction = 0.2; sp.add(b, c); balls.append((n, b, c)); born[id(b)] = T
    spots = [(GX + dx, GY - 170 + j * 68) for j in range(3) for dx in (-236, -172, -108, 108, 172, 236)]
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
        for _ in range(sub):
            sp.step(dt / sub)
            for n_, b_, c_ in balls:      # safety net: a gummy can never end up outside the glass
                dx, dy = b_.position.x - GX, b_.position.y - GY; dd = math.hypot(dx, dy); lim = GR - 6 - BR + 3
                if dd > lim:
                    nx, ny = dx / dd, dy / dd; b_.position = (GX + nx * lim, GY + ny * lim)
                    vn = b_.velocity.x * nx + b_.velocity.y * ny
                    if vn > 0: b_.velocity = (b_.velocity.x - 1.8 * vn * nx, b_.velocity.y - 1.8 * vn * ny)
                    NUDGE[0] += 1; NUDGE.append(dd - lim)
        if rnd.random() < 0.02: ag.angular_velocity = rnd.choice([OMEGA, OMEGA * 1.13, -OMEGA * 1.05])
        # cup hits
        for item in list(balls):
            n, b, c = item
            x, y = b.position
            if abs(x - CUPX) < 50 and CUPY - 40 < y < CUPY + 12 and T > cool and T - born[id(b)] > 1.2 and sum(counts.values()) < cap:
                sp.remove(b, c); balls.remove(item); counts[n] -= 1
                share = counts[n] / max(1, sum(counts.values())); k = max(2, round(rnd.randint(KLO, KHI) * (B0 - B1 * share)))   # recut: stronger catch-up so all four stay in it
                pending.append((n, k + 1)); events.append((round(T, 3), 'cup', n, k + 1)); cool = T + COOL
        tot = sum(counts.values())
        mx = max(counts.values()); ld = [n for n in NAMES if counts[n] == mx]
        if len(ld) == 1 and (not lead or lead[-1] != ld[0]): lead.append(ld[0])
        if record: frames.append(([(n, b.position.x, b.position.y) for n, b, c in balls], dict(counts), ag.angle))
        T += dt
        if tot >= cap: pending.clear()
        if tot >= cap and not pending:
            settle -= 1          # keep simulating ~0.6s after the last count so every score is settled before the win
            if settle <= 0: break
    return frames, events, counts, lead, T
if __name__ == '__main__':
    import sys
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        fr, ev, cnt, ld, T = run(seed, record=False)
        s = sorted(cnt.values(), reverse=True)
        print(seed, round(T, 1), len(ev), cnt, 'leads', len(ld), ld[-3:], flush=True)
