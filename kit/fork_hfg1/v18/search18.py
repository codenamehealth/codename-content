import numpy as np, random, math, sys
DUR=6.0; N=180; T=np.arange(N)/30; HALF=170
def mk(rng):
    P={}
    for key,amp in (('s',0.22),('dx',80),('dy',48)):
        k1,k2=rng.sample([2,3,4,5,6,7],2); a2=rng.uniform(0.2,0.6); p1,p2=rng.uniform(0,6.28),rng.uniform(0,6.28)
        P[key]=(amp,k1,k2,a2,p1,p2)
    return P
def f(P,key,t,TM):
    amp,k1,k2,a2,p1,p2=P[key]; w=2*math.pi/DUR
    g=lambda tt: np.sin(k1*w*tt+p1)+a2*np.sin(k2*w*tt+p2)
    v=g(t)-g(TM); return amp*v/(1+a2)
def miss(P,TM):
    s=1+f(P,'s',T,TM); dx=f(P,'dx',T,TM); dy=f(P,'dy',T,TM)
    return np.hypot(dx,dy)+np.abs(s-1)*HALF, s, dx, dy
best=[]
for seed in range(20000):
    rng=random.Random(seed); P=mk(rng)
    for fm in (84,87,90):
        TM=fm/30; m,s,dx,dy=miss(P,TM)
        o=np.sort(np.delete(m,fm))
        if m[0]<90 or m[-1]<90: continue
        if s.max()>1.25 or s.min()<0.75 or np.abs(dx).max()>92 or np.abs(dy).max()>58: continue
        # neighbours must miss by >=20 too, nearest elsewhere >=24
        best.append((o[0],seed,fm,round(m[0],1),round(m[fm-1],1),round(m[fm+1],1)))
best.sort(reverse=True); print(best[:8])
