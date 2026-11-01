import os, sys, collections
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
a, b = int(os.environ['A']), int(os.environ['B'])
for seed in range(a, b):
    rc, fr, bu, po = sim(seed)
    outs = sorted((round(s['out'] - T_START, 1), n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted((round(s['caught'] - T_START, 1), n) for n, s in rc.items() if s['caught'] is not None)
    print(seed, 'outs', outs, 'caught', caught, 'eat', [(round(x[0] - T_START, 1), x[1], x[4]) for x in bu], 'pops', [(round(p[0] - T_START, 1), p[1]) for p in po], flush=True)
