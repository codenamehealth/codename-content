import sys, math; from sim import *
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, cnt, ld, T = run(seed, record=False)
    s = sorted(cnt.values(), reverse=True); win = max(cnt, key=cnt.get)
    if win == 'cyrus' and s[0] > s[1] and s[1] >= 0.8 * s[0] and min(cnt.values()) >= 7 and len(ld) >= 3 and 11 < T < 21:
        print('HIT', seed, round(T, 1), cnt, len(ld), ld, flush=True)
