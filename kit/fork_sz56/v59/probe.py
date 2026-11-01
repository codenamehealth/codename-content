import sys
g={}
src=open('r59.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src,'r59','exec'),g)
for sd in range(1,25):
    fr,ev,ld,res=g['sim'](sd)
    print(sd,{n:(None if a is None else round(a,1),None if b is None else round(b,1)) for n,(a,b) in res.items()},len(ld))
