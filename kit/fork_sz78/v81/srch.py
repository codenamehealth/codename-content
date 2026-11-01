import os, sys
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(compile(src, 'r81', 'exec'))
import collections
lo, hi = int(os.environ['LO']), int(os.environ['HI'])
stats = collections.Counter()
for seed in range(lo, hi):
    rc, fr, bu = sim(seed)
    outs = sorted((s['out'], n) for n, s in rc.items() if s['out'] is not None)
    caught = sorted(s['caught'] for s in rc.values() if s['caught'] is not None)
    stuck = 4 - len(outs) - len(caught)
    stats[(len(outs), len(caught), stuck)] += 1
    if len(outs) == 1 and len(caught) == 3:
        tw, win = outs[0]
        print(os.environ.get('SA'), os.environ.get('SB'), os.environ.get('VB'), seed, win, round(tw, 1), [round(c, 1) for c in caught], len(bu), flush=True)
print(dict(stats))
