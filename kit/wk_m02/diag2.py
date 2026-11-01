import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m02_cfg import *
M = Maze(CFG)
for F in (53.5, 53.53, 53.57, 53.6):
    cov = M.cover_of(F)
    near = [(rc, tuple(round(v) for v in r), M.FDIR[rc], M.FT[rc], round(M.FW[rc], 2)) for rc, r in cov if r[2] > 940 and 740 < r[1] < 880]
    print(F, near)
