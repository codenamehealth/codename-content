import sys; from sim5 import *
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    fr, ev, cnt, ld, T = run(seed, record=False)
    s = sorted(cnt.values(), reverse=True); win = max(cnt, key=cnt.get)
    ts = [0.0] + [e[0] for e in ev]; gap = max(b - a for a, b in zip(ts, ts[1:])) if ev else 99
    cleo_early = any(e[2] == 'cleo' and e[0] < 5.0 for e in ev)
    if s[1] >= 0.7 * s[0] and len(ld) >= 3:
        print(seed, win, round(T, 1), 'gap', round(gap, 1), cnt, ld, 'cleoE', cleo_early, 'first', ev[0][0], flush=True)
