import os, sys, runpy
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(compile(src, 'r81', 'exec'))
for seed in range(6):
    rc, fr, bu = sim(seed)
    print(os.environ.get('SA'), os.environ.get('SB'), seed, {n: (round(s['out'], 1) if s['out'] else None, round(s['caught'], 1) if s['caught'] else None) for n, s in rc.items()}, len(bu), flush=True)
