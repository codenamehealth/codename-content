import os, sys
sys.argv=['x','search','0','0']; __file__='n03b.py'
src=open('n03b.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src,'n','exec'))
ws=[];ex=[]
for seed in range(int(os.environ.get('B','100'))):
    X, fr, ev, gum, B, wh = sim(seed)
    w=[e for e in ev if e[1]=='win']; ws.append(w[0][0] if w else 99)
    ex.append(B['exit']['broke'][0] if B['exit']['broke'] else 99)
import numpy as np; ws=np.array(ws); ex=np.array(ex)
print('win pct', [round(float(np.percentile(ws,q)),1) for q in (10,25,50,75)], 'exitbreak', [round(float(np.percentile(ex,q)),1) for q in (10,25,50,75)])
