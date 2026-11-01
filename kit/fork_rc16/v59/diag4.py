import os, sys, collections
sys.argv = ['r59.py', 'noop']
src = open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src, 'r59', 'exec'))
C = collections.Counter(); K = collections.Counter()
print('GUMS', GUMS, 'pads', SLIMEPAD, [PLAT[i] for i in SLIMEPAD.values()])
for sd in range(int(os.environ.get('N', '300'))):
    fr, ev, ld, res = sim(sd, 22)
    picks = [e for e in ev if e[1] == 'pick']
    C[len(picks)] += 1
    for e in picks: K[e[3]] += 1
print(dict(C), dict(K))
