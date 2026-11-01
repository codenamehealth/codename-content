import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m01_cfg import *
M = Maze(CFG); REF = {6: 10.5, 9: 4.5, 12: 2.5, 15: 15.5}; HS = M.HS
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
for seed in range(a0, a1):
    X, fr, ev, gum, win, ct = M.sim(seed, 18)
    gone = {}
    for c in REF:
        ts = [e[0] for e in ev if e[1] == 'break' and e[3][1] == c and e[3][0] in (4, 5, 6)]
        gone[c] = max(ts) if len(ts) == 3 else 99
    dev = max(abs(gone[c] - REF[c]) for c in REF)
    if dev > 1.5: continue
    X, fr, ev, gum, win, ct = M.sim(seed, 57)
    outs = [(round(e[0], 1), e[2], e[3]) for e in ev if e[1] == 'out']
    print(json.dumps(dict(seed=seed, win=win and (round(win[0], 2), win[1]), outs=outs, gum=(gum['who'], gum['t'] and round(gum['t'], 1)))), flush=True)
