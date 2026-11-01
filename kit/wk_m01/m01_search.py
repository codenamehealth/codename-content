import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m01_cfg import *
M = Maze(CFG)
a0, a1 = int(sys.argv[1]), int(sys.argv[2])
for seed in range(a0, a1):
    X, fr, ev, gum, win, ct = M.sim(seed, 60)
    outs = [(round(e[0], 1), e[2], e[3]) for e in ev if e[1] == 'out']
    brk = [(round(e[0], 1), e[3]) for e in ev if e[1] == 'break']
    print(json.dumps(dict(seed=seed, win=win and (round(win[0], 2), win[1]), outs=outs, gum=(gum['who'], gum['t'] and round(gum['t'], 1)),
                          nbreak=len(brk), lastbrk=brk[-1] if brk else None, alive_end=[g for g in G if X[g]['out'] is None])), flush=True)
