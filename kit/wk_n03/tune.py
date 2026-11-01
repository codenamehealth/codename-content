import os, sys, itertools
seeds = [int(x) for x in sys.argv[1].split(',')]
sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03b.py'
os.environ['SIMDUR'] = '21'; os.environ['TW0'] = '12'; os.environ['TW1'] = '20'
src = open('n03b.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
res = []
for seed in seeds:
    best = []
    for a, v, c in itertools.product([4.5, 5, 5.5, 6, 6.5, 7], [1.0, 1.3, 1.6, 1.9, 2.2, 2.5], [0.0, 0.06, 0.12, 0.2, 0.3]):
        os.environ['SH0'], os.environ['SHV'], os.environ['SHA'] = str(a), str(v), str(c)
        r = score(seed)
        if not r: continue
        tw, outs, gum, who, near, _, gap = r[:7]
        if outs[0] > 8.0: continue
        sp = min(b - a_ for a_, b in zip(outs, outs[1:]))
        q = len(outs) * 3 + min(sp, 3) - gap / 6 - abs(outs[0] - 6.5) - max(0, tw - outs[-1] - 1.5)
        best.append((round(q, 2), seed, a, v, c, r))
    best.sort(reverse=True)
    for b in best[:3]: print(*b, flush=True)
