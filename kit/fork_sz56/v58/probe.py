import sys, runpy
A1,A2=int(sys.argv[1]),int(sys.argv[2])
g={}
src=open('r58.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src,'r58','exec'),g)
for sd in range(A1,A2):
    fr,fin,ld,bo=g['sim'](sd,record=False)
    o=sorted(fin,key=lambda n:fin[n])
    print(sd,len(fin),[(n,round(fin[n],2)) for n in o],len(ld),flush=True)
