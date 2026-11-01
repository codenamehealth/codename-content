import os, sys
sys.argv=['n03b.py','search','0','0']
src=open('n03b.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src,'n03b','exec'))
import statistics
res=[]
for seed in range(int(os.environ.get('A','0')), int(os.environ.get('B','40'))):
    X, fr, ev, gum, B, wh = sim(seed, dur=60)
    w=[e for e in ev if e[1]=='win']; gates=[B['gate%d'%k]['broke'] for k in range(4)]
    res.append((seed, round(w[0][0],1) if w else None, w[0][2] if w else None, [round(g[0],1) if g else None for g in gates], round(B['exit']['broke'][0],1) if B['exit']['broke'] else None, gum['t'] and round(gum['t'],1)))
for r in res: print(r)
