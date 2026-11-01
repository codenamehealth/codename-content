import sys
src=open('r35.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; exec(src)
print('TOTAL', round(TOTAL), 'GUM_S', GUM_S)
for sd in range(8):
    fr,win,gb,R=sim(sd)
    print(sd, win and (win[0],round(win[1],1)), gb and (gb[0],round(gb[1],1)), {n:(round(r['out'],1) if r['out'] else None) for n,r in R.items()}, {n:r.get('behind') for n,r in R.items() if r.get('behind') is not None})
