import os, sys; os.environ['NB']='7'
import script20 as S
from sim import dist, legal_wall, N, nbrs
from story import hpath_step
cy = [S.CY[0]] + [tuple(x.split(':')) if ':' in x else x for x in sys.argv[1:]]
cy = [S.CY[0]] + [(int(a), int(b), o) for a, b, o in [x.split(':') for x in sys.argv[1:]]]
# play script then report options for next Cyrus wall
H, C = (N - 1, N // 2), (0, N // 2); walls = set(); ci = 0; turn = 0
while True:
    if turn % 2 == 0:
        H = hpath_step(H, walls, C)
        if H[0] == 0: print('H wins at turn', turn); break
    else:
        if ci >= len(cy): break
        a = cy[ci]; ci += 1
        if a[0] == 'm': C = a[1]
        else: assert legal_wall(a, walls), a; walls.add(a); assert dist(H, 0, walls) < 999, 'seal'
    turn += 1
print('turn', turn, 'H', H, 'C', C, 'Hdist', dist(H, 0, walls))
print(S.ascii(H, C, walls))
opts = []
for r in range(N - 1):
    for c in range(N - 1):
        for o in 'hv':
            w = (r, c, o)
            if not legal_wall(w, walls): continue
            d0 = dist(H, 0, walls); walls.add(w); d1 = dist(H, 0, walls); walls.discard(w)
            if d1 < 999 and d1 > d0: opts.append((d1 - d0, w))
print(sorted(opts, reverse=True)[:30])
