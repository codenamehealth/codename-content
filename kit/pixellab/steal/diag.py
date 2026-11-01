import sys
src=open('render_steal.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; exec(src)
for seed in range(10):
    fr,ev,win,st,ld=sim(seed)
    print(seed, win and (win[0],round(win[1],1)), 'steals',st,'leaders',ld[:8], {n:len(b) for n,b in fr[-1][2].items()})
