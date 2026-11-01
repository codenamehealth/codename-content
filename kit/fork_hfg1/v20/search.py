import os, sys
from sim2 import play2, trace, P0
P0['trig'] = 1
res = []
for seed in range(int(sys.argv[1]), int(sys.argv[2])):
    win, log, left = play2(seed, P0)
    if win != 'hollow': continue
    tr = trace(log)
    i_lead = next((i for i, (h, c) in enumerate(tr) if h <= 1), None)
    if i_lead is None: continue
    lead_c = tr[i_lead][1]
    worst = max(h - c for h, c in tr[i_lead:]); cmin = min(c for h, c in tr[i_lead + 1:])
    cw = sum(1 for e in log if e[0] == 'wall' and e[1] == 'cyrus'); hw = sum(1 for e in log if e[0] == 'wall' and e[1] == 'hollow')
    hw_after = sum(1 for e in log[i_lead:] if e[0] == 'wall' and e[1] == 'hollow')
    res.append((len(log), seed, i_lead, lead_c, worst, cmin, hw, cw, hw_after))
res.sort()
for r in res[:40]: print(r)
print(len(res))
