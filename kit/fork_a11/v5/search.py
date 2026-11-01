import sys; from sim import *
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, cnt, ld, T = run(seed, record=False)
    s = sorted(cnt.values(), reverse=True); win = max(cnt, key=cnt.get)
    grown = sum(1 for v in cnt.values() if v > 8)
    if win == 'cyrus' and 13 < T < 31 and s[0] > s[1] and s[1] >= 0.72 * s[0] and len(ld) >= 3 and grown >= 3:
        print('HIT', seed, round(T, 1), win, cnt, ld, flush=True)
    else: print(seed, round(T, 1), win, cnt, len(ld), flush=True)
