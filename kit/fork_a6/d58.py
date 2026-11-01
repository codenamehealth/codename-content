import sys
src=open('r58.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; exec(src)
for sd in range(6):
    fr,fin,ld,bo=sim(sd,record=True)
    last=fr[-1][0]
    print(sd,{n:round(v,1) for n,v in fin.items()}, 'leaders',len(ld),'bounces',len(bo), {n:(int(p[0]),int(p[1])) for n,p in last.items()})
