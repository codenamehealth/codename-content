import sys, math; from sim import *
import sim
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    sim.NUDGE[0] = 0
    fr, ev, cnt, ld, T = run(seed, record=True)
    s = sorted(cnt.values(), reverse=True); win = max(cnt, key=cnt.get)
    grown = sum(1 for v in cnt.values() if v > 8)
    out = max((math.hypot(x - GX, y - GY) for (balls, c, a) in fr for (n, x, y) in balls), default=0)
    tag = 'HIT' if (win == 'cyrus' and 12 < T < 22 and s[0] > s[1] and s[1] >= 0.8 * s[0] and len(ld) >= 4 and grown >= 3) else ('NEAR' if (win == 'cyrus' and s[1] >= 0.75 * s[0] and len(ld) >= 3 and T < 24) else '   ')
    print(tag, seed, round(T, 1), win, cnt, len(ld), ld[-4:], 'maxdist', round(out), flush=True)
