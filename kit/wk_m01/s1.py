# stage 1: gate break schedule vs reference (col 6: 10.5s, col 9: 4.5s, col 12: 2.5s, col 15: 15.5s)
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m01_cfg import *
M = Maze(CFG); REF = {6: 10.5, 9: 4.5, 12: 2.5, 15: 15.5}
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
for seed in range(a0, a1):
    X, fr, ev, gum, win, ct = M.sim(seed, 18)
    gone = {}
    for c in REF:
        ts = [e[0] for e in ev if e[1] == 'break' and e[3][1] == c and e[3][0] in (4, 5, 6)]
        gone[c] = max(ts) if len(ts) == 3 else 99
    dev = max(abs(gone[c] - REF[c]) for c in REF)
    print(json.dumps(dict(seed=seed, dev=round(dev, 2), gone={c: round(v, 1) for c, v in gone.items()})), flush=True)
