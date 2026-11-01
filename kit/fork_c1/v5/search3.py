import sys; from sim import *
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, cnt, ld, T = run(seed, record=False)
    s = sorted(cnt.values(), reverse=True); win = max(cnt, key=cnt.get)
    ts = [0.0] + [e[0] for e in ev]; gap = max(b - a for a, b in zip(ts, ts[1:])) if ev else 99
    grown = sum(1 for v in cnt.values() if v > 8)
    if win == 'cyrus' and s[0] > s[1] and s[1] >= 0.8 * s[0] and gap <= 2.3 and 11 < T < 19 and len(ld) >= 3 and grown >= 3:
        print('HIT', seed, round(T, 1), 'gap', round(gap, 1), cnt, ld, flush=True)
