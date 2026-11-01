import os, sys, math, collections, re
sys.argv = ['r81.py', 'none']
full = open('r81.py').read()
src = full.split("if sys.argv[1] == 'search':")[0]
a = src.index('def score(seed):'); b = src.index('\n', src.index('    return round(race', a))
sc = src[a:b]
lines = sc.split('\n'); out = []
for i, l in enumerate(lines):
    out.append(l.replace('return None', "return 'L%d'" % i))
src = src[:a] + '\n'.join(out) + src[b:]
exec(src)
C_ = collections.Counter()
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    r = score(seed)
    if isinstance(r, str): C_[r] += 1
    else: print('OK', seed, r, flush=True)
print(C_)
for i, l in enumerate(lines):
    if 'return None' in l: print(i, l.strip()[:110])
