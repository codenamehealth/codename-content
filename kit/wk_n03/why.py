import os, sys, collections
sys.argv=['x','search','0','0']; __file__='n03b.py'
src=open('n03b.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src,'n','exec'))
C_=collections.Counter(); wins=collections.Counter(); outsn=collections.Counter()
for seed in range(int(os.environ.get('A','0')), int(os.environ.get('B','300'))):
    X, fr, ev, gum, B, wh = sim(seed)
    w=[e for e in ev if e[1]=='win']
    outs=[e for e in ev if e[1]=='out']
    outsn[len(outs)]+=1
    if w: wins[(w[0][2], int(w[0][0]))]+=1
    else: C_['nowin']+=1
print(C_, 'outs', sorted(outsn.items()))
print(sorted(wins.items()))
