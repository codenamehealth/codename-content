import random, sys
from collections import deque
C, R = 8, 10
START = (0, 4); GOAL = (9, 3)
def edge(a, b):
    (r, c), (nr, nc) = a, b
    return ('h', min(r, nr), c) if r != nr else ('v', r, min(c, nc))
def neighbors(p, walls):
    r, c = p
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and edge(p, (nr, nc)) not in walls: yield (nr, nc)
def dist(p, walls):
    q = deque([p]); d = {p: 0}
    while q:
        x = q.popleft()
        if x == GOAL: return d[x]
        for y in neighbors(x, walls):
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return None
EDGES = [('h', r, c) for r in range(R - 1) for c in range(C)] + [('v', r, c) for r in range(R) for c in range(C - 1)]
def region(p, walls):
    q = deque([p]); seen = {p}
    while q:
        x = q.popleft()
        for y in neighbors(x, walls):
            if y not in seen: seen.add(y); q.append(y)
    return seen
def run(seed, PER=2, NOISE=2.5, SPRING=2, MAXREG=4):
    rnd = random.Random(seed); walls = set(); pos = START; log = []; ds = []
    for turn in range(30):
        for k in range(PER):
            dnow = dist(pos, walls); best = None; bs = -1e9
            for e in EDGES:
                if e in walls: continue
                d = dist(pos, walls | {e})
                if d is None:
                    reg = region(pos, walls | {e})
                    sc = (1000 - len(reg)) if (dnow <= SPRING and GOAL not in reg and len(reg) <= MAXREG) else -1e6
                else: sc = d + rnd.uniform(0, NOISE)
                if sc > bs: bs, best = sc, e
            walls.add(best); log.append(('wall', best))
            if dist(pos, walls) is None: return turn, log, ds, pos
        d = dist(pos, walls)
        cand = [y for y in neighbors(pos, walls) if dist(y, walls) == d - 1]
        pos = rnd.choice(cand); log.append(('move', pos)); ds.append(d - 1)
        if pos == GOAL: return None, log, ds, pos
    return None, log, ds, pos
if __name__ == '__main__':
    PER, NOISE, SPRING = int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        t, log, ds, pos = run(seed, PER, NOISE, SPRING, int(sys.argv[6]))
        if t is not None and 7 <= t <= 16: print(seed, 'trap turn', t, 'dists', ds[-6:], 'walls', sum(1 for l in log if l[0]=='wall'), 'at', pos, flush=True)
