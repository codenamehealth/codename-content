# kept for compatibility: same criteria as dox_search.ok (one source of truth)
import sys
from dox_search import summ, ok
for s in range(int(sys.argv[1]), int(sys.argv[2])):
    d, r = summ(s); print(('OK ' if ok(d) else '   ') + str(d), flush=True)
