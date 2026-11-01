import sys,os
src=open('render_steal.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; exec(src)
res=[]
for seed in range(30):
    fr,ev,win,st,ld=sim(seed)
    res.append((round(win[1],1) if win else None, st))
print(os.environ['N0'], res)
