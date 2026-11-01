import sys; from sim5 import *
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, cnt, ld, T = run(seed, record=False)
    s = sorted(cnt.values(), reverse=True); win = max(cnt, key=cnt.get)
    ts = [0.0] + [e[0] for e in ev]; gap = max(b - a for a, b in zip(ts, ts[1:])) if ev else 99
    if win == 'cyrus' and s[0] > s[1] and len(ld) >= 3 and ld[-1] == 'cyrus' and 9.5 < T < 13.5 and min(cnt.values()) >= 8:
        print('HIT', seed, round(T, 1), 'gap', round(gap, 1), cnt, ld, 'first', ev[0][0], flush=True)
