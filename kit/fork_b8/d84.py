import sys,os
sys.argv=['x','none']
src=open('r84.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
for s in range(12):
    fr, br, bo, esc, gums = sim(s)
    print(s, esc and round(esc,1), len(bo), sum(1 for g in gums if g['got']), fr[-1][2][:20])
