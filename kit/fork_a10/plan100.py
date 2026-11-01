import random
from sim100b import neighbors, dist, region, R, C
GOAL = (9, 3); START = (0, 4)
ORDER = [('h', 7, c) for c in (7, 6, 5, 4, 3, 2, 1)] + [('v', 5, 0), ('v', 6, 0), ('v', 7, 0)]
def plan(seed):
    import sim100b; sim100b.GOAL = GOAL
    rnd = random.Random(seed); walls = set(); pos = START; steps = []; oi = 0; sealed = 0
    for turn in range(40):
        placed = None
        if oi < len(ORDER): placed = ORDER[oi]; oi += 1
        elif sealed == 0 and pos[1] == 0 and 5 <= pos[0] <= 7: placed = ('h', 7, 0); sealed = 1
        elif sealed == 1: placed = ('h', 4, 0); sealed = 2
        if placed: walls.add(placed)
        d = dist(pos, walls)
        move = None
        if d is not None and d > 0:
            cand = [y for y in neighbors(pos, walls) if dist(y, walls) == d - 1]
            move = rnd.choice(cand)
        steps.append((placed, pos, move))
        if move: pos = move
        if sealed == 2: return steps, pos, walls
    return None, pos, walls
for s in range(20):
    st, pos, walls = plan(s)
    if st: print(s, len(st), pos, [x[1] for x in st])
