import sys, math
sys.argv = ['r58.py', '0']
exec(open('r58.py').read().split("SEED = int(sys.argv[1])")[0])
import pymunk
FR, FIN, LEAD, BO = sim(2092)
def segd(p, a, b):
    ax, ay = a; bx, by = b; px, py = p; dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    u = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L)) if L else 0
    return math.hypot(px - ax - u * dx, py - ay - u * dy)
worst = {'ball': 0, 'stone(drawn)': 0, 'spoke(drawn)': 0, 'hub(drawn)': 0, 'peg': 0}
for fi, (pos, wang, traps, fin) in enumerate(FR):
    live = [n for n in NAMES if pos[n][1] <= JT + 95]
    for i, a in enumerate(live):
        for b in live[i + 1:]:
            worst['ball'] = max(worst['ball'], 2 * MR - math.hypot(pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]))
    for n in live:
        p = pos[n][:2]
        for (a, b, r, kind) in SEGS:
            half = r if kind == 'wall' else r + 5
            worst['stone(drawn)'] = max(worst['stone(drawn)'], MR + half - segd(p, a, b))
        for (wx, wy, R, w_), ang in zip(WHEELS, wang):
            for k in range(6):
                aa = ang + k * math.pi / 3
                worst['spoke(drawn)'] = max(worst['spoke(drawn)'], MR + 11 - segd(p, (wx, wy), (wx + R * math.cos(aa), wy + R * math.sin(aa))))
            worst['hub(drawn)'] = max(worst['hub(drawn)'], MR + 28 - math.hypot(p[0] - wx, p[1] - wy))
print({k: round(v, 1) for k, v in worst.items()}, '(px of overlap; <=1-2 is contact tolerance)')
