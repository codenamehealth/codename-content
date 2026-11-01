import os, itertools, importlib
GT='3.5,7,10.5,14,17.5,21,24.5,28,31.5,35,38.5'
K='mush,cre,mel,cre,mush,cre,mel,cre,mush,cre,mel'
for gd, sp, strn, alt in itertools.product([75,90],[900,1000],[25],[6,8]):
    os.environ['SPX']='1.5'
    os.environ.update(GAPDEG=str(gd), SPD=str(sp), ALT=str(alt), JIT='0.2', STRN=str(strn), GUMT=GT, KINDS=K, OMV='0')
    import sim103; importlib.reload(sim103)
    ok=[]; es=[]
    for s in range(60):
        fr,ev,cb,esc=sim103.sim(s)
        if esc is None: continue
        es.append(esc)
        br=[e[0] for e in ev if e[1] in('break','smash')]
        gaps=[b-a for a,b in zip([2.0]+br,br)]
        if 30<=esc<=37 and max(gaps)<3.2: ok.append((s,round(esc,1),round(max(gaps),1),max([c for _,c in cb]+[0]), sum(e[1]=='smash' for e in ev)))
    es.sort(); print(gd,sp,strn,alt,'median',es and round(es[len(es)//2],1),len(ok),ok[:5])
