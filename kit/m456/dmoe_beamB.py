# stage B: re-roll the stream again at T on stage-A survivors; full summary + ok() from dmoe_search
import sys
from dmoe_search import summ, ok
bases = sys.argv[1].split(','); T = sys.argv[2]; a, b = int(sys.argv[3]), int(sys.argv[4])
for s3 in range(a, b):
    for base in bases:
        d, r = summ('%s:%s:%d' % (base, T, s3)); print(('OK ' if ok(d) else '   ') + str(d), flush=True)
