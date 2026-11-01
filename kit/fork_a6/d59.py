import sys
src=open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; exec(src)
print('rows',NROW,'slimepads',SLIMEPAD,'gums',GUMS)
for sd in range(8):
    fr,ev,ld,res=sim(sd)
    print(sd,{n:(round(a,1) if a else None, round(b,1) if b else None) for n,(a,b) in res.items()},'ld',len(ld),'gum',sum(1 for e in ev if e[1]=='gum'),'boing',sum(1 for e in ev if e[1]=='boing'))
