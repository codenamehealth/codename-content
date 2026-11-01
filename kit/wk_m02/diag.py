import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m02_cfg import *
M = Maze(CFG); seed = int(sys.argv[1]); X, fr, ev, pk, win, ct = M.sim(seed, float(sys.argv[2]))
U, X0, Y0 = M.U, M.X0, M.Y0
for i in range(1, len(fr)):
    for g in G:
        a, b = fr[i - 1][0][g], fr[i][0][g]
        if b[4] is not None and b[4] < i / FPS - 1e-6: continue
        if math.hypot(b[0] - a[0], b[1] - a[1]) > 18.7: print('jump', round(i / FPS, 2), g, [round(v, 1) for v in a[:4]] + [a[7]], '->', [round(v, 1) for v in b[:4]] + [b[7]], 'cell', M.cell(b[0], b[1]))
print([e for e in ev if e[1] in ('out', 'pick', 'win')])
