import os, sys
sys.argv=['x','search','0','0']; __file__='n03b.py'
src=open('n03b.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src,'n','exec'))
for seed in range(12):
    X, fr, ev, gum, B, wh = sim(seed)
    outs=[(round(e[0],1), e[2], int((X[e[2]]['y']-OY)//C)) for e in ev if e[1]=='out']
    gates=[round(B['gate%d'%k]['broke'][0],1) if B['gate%d'%k]['broke'] else None for k in range(4)]
    print(seed, 'gates', gates, 'outs(t,g,row)', outs)
