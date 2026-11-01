import sys, os
src = open('r101.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g = {'__name__': 'x'}; exec(compile(src, 'r101', 'exec'), g)
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    rc, fr, gt = g['sim'](seed)
    print(seed, {n: (round(s['out'], 1) if s['out'] else None, round(s['caught'], 1) if s['caught'] else None) for n, s in rc.items()}, gt and (gt[0], round(gt[1], 1)), rc[gt[0]]['behind'] if gt else None)
