import sys, os
src=open('r93.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
g={'__file__':os.path.abspath('r93.py')}
exec(compile(src,'r93','exec'),g)
for sd in range(int(sys.argv[1]), int(sys.argv[2])):
    r=g['score'](sd)
    if not r: continue
    fr,ev,win,st,ld,used,den=g['sim'](sd)
    pts=[e[0] for e in ev if e[1] in ('power','blocked')]
    cl=[e[0] for e in ev if e[1]=='power' and e[2]=='cleo' and e[0] < win[1]-1.2]
    iso=[c for c in cl if all(abs(p-c)>1.2 for p in pts if p!=c)]
    print(sd, r, 'iso' if iso else '', [(round(e[0],2),e[1],e[2]) for e in ev if e[1] in ('power','denied','blocked')], flush=True)
