import sys, os
from dox_search import summ
for s in range(int(sys.argv[1]), int(sys.argv[2])):
    d, r = summ(s)
    gk = [o for o in d['outs'] if o[2] == 'gummy']
    ok = d['win'] and d['win'][1] in ('joy', 'cyrus') and d['win'][0] <= 57.8 and d['block'] and len(gk) >= 2 and all(o[0] > 40 for o in d['outs'] if o[0] < d['win'][0])
    print(('OK ' if ok else '   ') + str(d), flush=True)
