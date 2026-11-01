import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m02_cfg import *
M = Maze(CFG)
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    X, fr, ev, pk, win, ct = M.sim(seed, 61)
    gates = {}
    for c in (2, 5, 8, 11):
        ts = [e[0] for e in ev if e[1] == 'break' and e[3][1] == c and e[3][0] in (12, 13, 14)]
        gates[c] = round(max(ts), 1) if len(ts) == 3 else None
    dk = {'%d,%d' % e[3]: round(e[0], 1) for e in ev if e[1] == 'break' and e[3][0] < 12}
    print(json.dumps(dict(seed=seed, win=win and (round(win[0], 2), win[1]), outs=[(round(e[0], 1), e[2], e[4]) for e in ev if e[1] == 'out'],
                          pk=[(p['who'], p['t'] and round(p['t'], 1)) for p in pk], gates=gates, dark=dk, lag=round(fr[-1][1] - len(fr) / FPS, 2))), flush=True)
