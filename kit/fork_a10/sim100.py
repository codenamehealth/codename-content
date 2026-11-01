import random, sys
from collections import deque
C, R = 8, 10
START = (0, 4); GOAL = (9, 3)
def neighbors(p, walls):
    r, c = p
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C:
            e = ('h', min(r, nr), c) if dr else ('v', r, min(c, nc))
            if e not in walls: yield (nr, nc)
def dist(p, walls):
    q = deque([p]); d = {p: 0}
    while q:
        x = q.popleft()
        if x == GOAL: return d[x], d
        for y in neighbors(x, walls):
            if y not in d: d[y] = d[x] + 1; q.append(y)
    return None, d
def segs():
    out = []
    for r in range(R - 1):
        for c in range(C - 1): out.append((('h', r, c), ('h', r, c + 1)))
    for r in range(R - 1):
        for c in range(C - 1): out.append((('v', r, c), ('v', r + 1, c)))
    return out
SEGS = segs()
def run(seed, verbose=False):
    rnd = random.Random(seed); walls = set(); NOISE = 4.0; pos = START; log = []; mind = 99
    for turn in range(40):
        # cleo places a 2-long wall
        best = []; bscore = -1
        for s in SEGS:
            if s[0] in walls or s[1] in walls: continue
            w2 = walls | set(s)
            d, _ = dist(pos, w2)
            sc = 1000 if d is None else d
            dnow, _ = dist(pos, walls)
            if d is None and dnow > 3: sc = -1   # Cleo springs the trap only at the last moment
            sc += rnd.uniform(0, NOISE)
            if sc > bscore - 1e-9:
                if sc > bscore + 0.5: best = []
                bscore = max(bscore, sc); best.append((sc, s))
        sc, s = max(best)
        walls |= set(s); log.append(('wall', s))
        d, dd = dist(pos, walls)
        if d is None: return turn, log, mind, pos
        # hollow steps along a shortest path
        nxt = [y for y in neighbors(pos, walls) if y in dd or True]
        cand = []
        for y in neighbors(pos, walls):
            dy, _ = dist(y, walls)
            if dy is not None and dy == d - 1: cand.append(y)
        pos = rnd.choice(cand); log.append(('move', pos)); mind = min(mind, d - 1)
        if pos == GOAL: return None, log, mind, pos
    return None, log, mind, pos
if __name__ == '__main__':
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        t, log, mind, pos = run(seed)
        if t is not None and t >= 8 and mind <= 3: print(seed, 'trapped turn', t, 'closest', mind, 'at', pos, flush=True)
