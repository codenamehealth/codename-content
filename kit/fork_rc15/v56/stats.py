import sys, os
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc15/v56')
src=open('r56.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g={'__name__':'x'}; exec(compile(src,'r56','exec'),g)
from collections import Counter
a,b=int(sys.argv[1]),int(sys.argv[2])
for sd in range(a,b):
    fr, ev, obs, ld, fin, mc = g['sim'](sd)
    c=Counter(e[1] for e in ev)
    order=sorted([n for n in fin if fin[n]], key=lambda n: fin[n])
    print(sd, order[:2], {k:(round(v,1) if v else v) for k,v in fin.items()}, dict(c), len(ld), len(set(e[2] for e in ev if e[1]=='pick')))
