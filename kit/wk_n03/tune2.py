import os, sys, itertools
seeds = [int(x) for x in sys.argv[1].split(',')]
sys.argv = ['x', 'search', '0', '0']; __file__ = 'n03c.py'
os.environ['SIMDUR'] = '18'; os.environ['TW0'] = '12.5'; os.environ['TW1'] = '17.2'; os.environ['T4MAX'] = '13.0'
src = open('n03c.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'n', 'exec'))
for seed in seeds:
    best = []
    for a, v, c in itertools.product([4.0, 4.5, 5.0, 5.5, 6.0], [2, 3, 4, 5, 6, 8], [0.2, 0.5, 0.8, 1.2, 1.6]):
        os.environ['SH0'], os.environ['SHV'], os.environ['SHA'] = str(a), str(v), str(c)
        r = score(seed)
        if not r: continue
        outs = r['outs']; tw = r['tw']
        q = len(outs) * 3 - abs(outs[0] - 5.6) - max(0, r['gap']) / 15 - abs(tw - 15.5) * 0.5 - max(0, tw - outs[-1] - 3) * 0.5
        best.append((round(q, 2), seed, a, v, c, r))
    best.sort(key=lambda z: -z[0])
    for b in best[:2]: print(*b, flush=True)
