import sys; from sim import *
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, cnt, ld, T = run(seed, record=False)
    s = sorted(cnt.values(), reverse=True)
    grown = sum(1 for v in cnt.values() if v > 10)
    if 22 < T < 31 and s[0] >= 1.0 * s[0] and s[1] >= 0.72 * s[0] and len(ld) >= 3 and grown >= 3:
        print(seed, round(T, 1), cnt, ld, flush=True)
