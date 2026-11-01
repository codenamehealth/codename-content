# re-roll the bounce-jitter stream after T seconds on a base seed whose opening matches the reference (seed spec 'A:T:B')
import sys
from dmoe_search import summ, ok
base = sys.argv[1]; Ts = [float(x) for x in sys.argv[2].split(',')]; a, b = int(sys.argv[3]), int(sys.argv[4])
for s2 in range(a, b):
    for T in Ts:
        d, r = summ('%s:%g:%d' % (base, T, s2)); print(('OK ' if ok(d) else '   ') + str(d), flush=True)
