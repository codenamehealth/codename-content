import sys,os,itertools
src=open('r48.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search'")[0]
sys.argv=['x']; exec(src)
res=[]
for look,k,lat,keep in itertools.product([230,300,380],[2.5,4,6],[110],[{11},{8},{14}]):
    DODGE={'cleo':keep}; DODGE_LOOK=look; DODGE_K=k
    # patch lateral window
    globals()['LAT']=lat
    rc,fr,ld=sim(33)
    outs=sorted((s['out'],n) for n,s in rc.items() if s['out'] is not None)
    if outs[0][1]!='joy': continue
    hits=0; slides=set(); lead_end=None
    for f,(st,rank,taken) in enumerate(fr):
        t=f/30; s=st['cleo']
        if t>2.4 and not s['sliding'] and any(-10<oy-s['p']<40 and abs(ol-s['l'])<48 for oy,ol,kk in OBST): hits+=1
        if s['sliding']: slides.add(round(s['slide'],2))
        if t>5 and rank[0]=='cleo': lead_end=t-2.4
    pos=[n for _,n in outs].index('cleo')+1
    res.append((hits, -round(lead_end or 0,2), pos, round(outs[0][0],2), round(outs[1][0]-outs[0][0],2), look,k,lat,sorted(keep), sorted(round(x-2.4,2) for x in slides)))
for r in sorted(res)[:15]: print(r)
