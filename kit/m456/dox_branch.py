# re-roll the bounce-jitter stream after T seconds on a base seed (seed spec 'A:T:B'); jobs = base@T,base@T,...
import sys
from dox_search import summ, ok
jobs = [(j.split('@')[0], float(j.split('@')[1])) for j in sys.argv[1].split(',')]; a, b = int(sys.argv[2]), int(sys.argv[3])
for s2 in range(a, b):
    for base, T in jobs:
        d, r = summ('%s:%g:%d' % (base, T, s2)); print(('OK ' if ok(d) else '   ') + str(d), flush=True)
