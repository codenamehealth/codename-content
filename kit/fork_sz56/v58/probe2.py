import sys
g={}
src=open('r58.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(compile(src,'r58','exec'),g)
for sd in (6,8):
    fr,fin,ld,bo=g['sim'](sd,record=True)
    for tt in (10,20,30,44):
        p=fr[min(len(fr)-1,tt*30)][0]
        print(sd,tt,{n:(int(v[0]),int(v[1])) for n,v in p.items()})
print('wheels',g['WHEELS'],'shelves',g['SHELVES'])
print([s for s in g['SEGS'] if s[0][1]>3000+520 and s[0][1]<5000+520])
