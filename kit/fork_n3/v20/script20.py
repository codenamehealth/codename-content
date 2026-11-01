# Oct 29 #20: hand-scripted turns (BFS-verified). Hollow (player) moves every turn along a shortest path; Cyrus: one move, then
# a barrier every turn. A barrier may never seal the Hollow's last way out (checked).
import os, sys
os.environ.setdefault('NB', '7')
from sim import N, dist, nbrs, legal_wall
from story import hpath_step
CY = [('m', (1, 3)), (3, 2, 'h'), (3, 4, 'h'), (3, 5, 'v'), (4, 4, 'h'), (1, 5, 'h')] + [tuple(x.split(':')) for x in os.environ.get('MORE', '').split(',') if x]
def build(cy=CY):
    H, C = (N - 1, N // 2), (0, N // 2); walls = set(); log = []; ci = 0
    for turn in range(80):
        if turn % 2 == 0:
            n = hpath_step(H, walls, C); log.append(('move', 'hollow', H, n)); H = n
            if H[0] == 0: return log
        else:
            a = cy[ci] if ci < len(cy) else None; ci += 1
            if a is None or a[0] == 'm':
                tgt = a[1] if a else None
                if tgt is None:   # out of script: Cyrus heads for his own row
                    tgt = min(((dist(p, N - 1, walls), p) for p in nbrs(*C, walls) if p != H))[1]
                assert tgt in set(nbrs(*C, walls)); log.append(('move', 'cyrus', C, tgt)); C = tgt
                assert C[0] != N - 1, 'cyrus wins'
            else:
                w = (int(a[0]), int(a[1]), a[2]); assert legal_wall(w, walls), w
                d0 = dist(H, 0, walls); walls.add(w); d1 = dist(H, 0, walls); assert d1 < 999 and dist(C, N - 1, walls) < 999, ('seals', w)
                log.append(('wall', 'cyrus', w, d1 - d0))
    raise SystemExit('no finish')
def ascii(H, C, walls):
    out = []
    for r in range(N):
        row = ''
        for c in range(N):
            ch = 'H' if (r, c) == H else ('C' if (r, c) == C else '.')
            row += ch + ('|' if c < N - 1 and ((r, c, 'v') in walls or (r - 1, c, 'v') in walls) else ' ')
        out.append(row)
        if r < N - 1: out.append(''.join(('--' if ((r, c, 'h') in walls or (r, c - 1, 'h') in walls) else '  ') for c in range(N)))
    return '\n'.join(out)
if __name__ == '__main__':
    log = build(); H, C = (N - 1, N // 2), (0, N // 2); walls = set()
    for i, e in enumerate(log):
        if e[0] == 'move':
            if e[1] == 'hollow': H = e[3]
            else: C = e[3]
        else: walls.add(e[2])
        print(i, e, 'Hdist', dist(H, 0, walls))
        if '-v' in sys.argv or i == len(log) - 1 or (e[0] == 'wall'): print(ascii(H, C, walls))
    print('turns', len(log), 'Hmoves', sum(1 for e in log if e[1] == 'hollow'), 'walls', sum(1 for e in log if e[0] == 'wall'))
