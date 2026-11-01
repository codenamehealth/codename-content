import math, random, json, sys
FPS=30; N=240; FSTAR=int(sys.argv[1]) if len(sys.argv)>1 else 176
def ang(p,f):
    t=(f-FSTAR)/FPS; w,A,nu,ph=p
    return (w*t + A*(math.sin(nu*t+ph)-math.sin(ph)))
def err(a): a=(a+180)%360-180; return abs(a)
best=None
rnd=random.Random(1)
for trial in range(20000):
    ps=[(rnd.choice([1,-1])*rnd.uniform(90,260), rnd.uniform(10,40), rnd.uniform(1.5,4.0), rnd.uniform(0,6.28)) for _ in range(3)]
    E=[[err(ang(p,f)) for f in range(N)] for p in ps]
    bad=False; minother=999
    for f in range(N):
        if f==FSTAR: continue
        m=max(E[i][f] for i in range(3)); minother=min(minother,m)
    if minother<6.5: continue
    ind=[sum(1 for f in range(N) if E[i][f]<3 and abs(f-FSTAR)>4) for i in range(3)]
    if min(ind)<2: continue
    sc=minother+min(ind)
    if best is None or sc>best[0]: best=(sc,minother,ind,ps)
print(best[:3]); json.dump(best[3],open('dials.json','w'))
