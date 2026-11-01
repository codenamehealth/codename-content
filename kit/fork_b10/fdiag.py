import sys, os
src=open('render_flood.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; exec(src)
for seed in range(10):
    fr,ev,g=sim(seed)
    print(seed,{n:(round(s['caught'],1) if s['caught'] else None, round(s['out'],1) if s['out'] else None, s['d']) for n,s in g.items()})
