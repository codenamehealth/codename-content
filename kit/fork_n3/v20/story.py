# Oct 29 #20 rule (Bennett): each turn is EITHER one move OR one barrier; barriers are unlimited. The Hollow (player) only moves and
# never quits; Cyrus moves once, then spends his turns walling the Hollow in (a barrier may never seal the last way out).
import os, random, sys
os.environ.setdefault('NB', '7')
from sim import N, dist, nbrs, legal_wall
def hpath_step(pos, walls, other):
    best = None
    for nr, nc in nbrs(*pos, walls):
        if (nr, nc) == other: continue
        d = dist((nr, nc), 0, walls)
        k = (d, 0 if nc == pos[1] else 1, abs(nc - N // 2))
        if best is None or k < best[0]: best = (k, (nr, nc))
    return best[1]
def near(w, p, R):
    r, c, o = w; cells = [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
    return min(abs(a - p[0]) + abs(b - p[1]) for a, b in cells) <= R
def play(seed, R=1, cmoves=1, maxw=99):
    rnd = random.Random(seed)
    H, C = (N - 1, N // 2), (0, N // 2); walls = set(); log = []; nw = 0
    for turn in range(80):
        if turn % 2 == 0:
            n = hpath_step(H, walls, C); log.append(('move', 'hollow', H, n)); H = n
            if H[0] == 0: return 'hollow', log
        else:
            dh = dist(H, 0, walls); best = None
            if turn // 2 >= cmoves and nw < maxw:
                cands = [(r, c, o) for r in range(N - 1) for c in range(N - 1) for o in 'hv']; rnd.shuffle(cands)
                for w in cands:
                    if not legal_wall(w, walls) or not near(w, H, R): continue
                    walls.add(w); nd = dist(H, 0, walls); ncd = dist(C, N - 1, walls); walls.discard(w)
                    if nd >= 999 or ncd >= 999: continue
                    if best is None or nd > best[0]: best = (nd, w)
            if best and best[0] > dh:
                walls.add(best[1]); nw += 1; log.append(('wall', 'cyrus', best[1], best[0] - dh))
            else:
                r, c = C; opts = [(dist((a, b), N - 1, walls), rnd.random(), (a, b)) for a, b in nbrs(r, c, walls) if (a, b) != H]
                n = min(opts)[2]; log.append(('move', 'cyrus', C, n)); C = n
                if C[0] == N - 1: return 'cyrus', log
    return None, log
def show(log):
    H, C = (N - 1, N // 2), (0, N // 2); walls = set()
    for e in log:
        if e[0] == 'move':
            if e[1] == 'hollow': H = e[3]
            else: C = e[3]
        else: walls.add(e[2])
    return walls
if __name__ == '__main__':
    R = int(sys.argv[1]); cm = int(sys.argv[2]); mw = int(sys.argv[3])
    for seed in range(200):
        win, log = play(seed, R, cm, mw)
        if win != 'hollow': continue
        hm = sum(1 for e in log if e[0] == 'move' and e[1] == 'hollow'); cw = sum(1 for e in log if e[0] == 'wall'); cmv = sum(1 for e in log if e[0] == 'move' and e[1] == 'cyrus')
        back = sum(1 for e in log if e[0] == 'move' and e[1] == 'hollow' and e[3][0] > e[2][0])
        print(seed, 'turns', len(log), 'Hmoves', hm, 'walls', cw, 'Cmoves', cmv, 'backsteps', back)
