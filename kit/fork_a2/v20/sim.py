import random, collections
N = 9
def dist(pos, goal_row, walls):
    # walls: set of (r, c, o) intersection at lower-right of cell (r,c); o 'h' blocks between rows r,r+1 for cols c,c+1; 'v' blocks between cols c,c+1 for rows r,r+1
    q = collections.deque([pos]); D = {pos: 0}
    while q:
        r, c = q.popleft()
        if r == goal_row: return D[(r, c)]
        for nr, nc in nbrs(r, c, walls):
            if (nr, nc) not in D: D[(nr, nc)] = D[(r, c)] + 1; q.append((nr, nc))
    return 999
def blocked(r, c, nr, nc, walls):
    if nr == r + 1: return (r, c, 'h') in walls or (r, c - 1, 'h') in walls
    if nr == r - 1: return (r - 1, c, 'h') in walls or (r - 1, c - 1, 'h') in walls
    if nc == c + 1: return (r, c, 'v') in walls or (r - 1, c, 'v') in walls
    if nc == c - 1: return (r, c - 1, 'v') in walls or (r - 1, c - 1, 'v') in walls
def nbrs(r, c, walls):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < N and not blocked(r, c, nr, nc, walls): yield nr, nc
def legal_wall(w, walls):
    r, c, o = w
    if w in walls: return False
    if o == 'h' and ((r, c - 1, 'h') in walls or (r, c + 1, 'h') in walls or (r, c, 'v') in walls): return False
    if o == 'v' and ((r - 1, c, 'v') in walls or (r + 1, c, 'v') in walls or (r, c, 'h') in walls): return False
    return True
def play(seed, walls_each=(7, 7), aggr=(1.0, 1.0)):
    rnd = random.Random(seed)
    P = {'hollow': [N - 1, 4], 'cyrus': [0, 4]}; GOAL = {'hollow': 0, 'cyrus': N - 1}
    left = {'hollow': walls_each[0], 'cyrus': walls_each[1]}; walls = set(); log = []
    order = ['hollow', 'cyrus']; th = {'hollow': rnd.uniform(0.5, 1.5), 'cyrus': rnd.uniform(0.0, 1.0)}
    for turn in range(120):
        me = order[turn % 2]; op = order[(turn + 1) % 2]
        dm = dist(tuple(P[me]), GOAL[me], walls); do = dist(tuple(P[op]), GOAL[op], walls)
        acted = False
        if left[me] > 0 and do <= dm + th[me] and rnd.random() < 0.85:
            best = None
            cands = [(r, c, o) for r in range(N - 1) for c in range(N - 1) for o in 'hv']
            rnd.shuffle(cands)
            for w in cands:
                if not legal_wall(w, walls): continue
                walls.add(w)
                ndo = dist(tuple(P[op]), GOAL[op], walls); ndm = dist(tuple(P[me]), GOAL[me], walls)
                walls.discard(w)
                if ndo >= 999 or ndm >= 999: continue
                sc = (ndo - do) - (ndm - dm) + rnd.uniform(0, 0.3)
                if best is None or sc > best[0]: best = (sc, w, ndo)
            if best and best[0] >= 0.95:
                walls.add(best[1]); left[me] -= 1; log.append(('wall', me, best[1], best[2] - do)); acted = True
        if not acted:
            r, c = P[me]; opts = []
            for nr, nc in nbrs(r, c, walls):
                if [nr, nc] == P[op]: continue
                d = dist((nr, nc), GOAL[me], walls)
                opts.append((d, rnd.random(), nr, nc))
            if opts:
                d, _, nr, nc = min(opts); P[me] = [nr, nc]; log.append(('move', me, (r, c), (nr, nc)))
            else: log.append(('wait', me))
        if P[me][0] == GOAL[me]: return me, log, left
    return None, log, left
def stats(seed):
    win, log, left = play(seed)
    # track gap over time
    return win, len(log), left
