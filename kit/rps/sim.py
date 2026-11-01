import numpy as np, json, sys
# 4 guides in a cycle: Joy>Cleo>Cyrus>Rayleigh>Joy; opposite pairs (Joy-Cyrus, Cleo-Rayleigh) coin-flip
def run(seed,N=20,FR=2400):
    r=np.random.default_rng(seed)
    BOX=(60,560,1020,1520); R=26
    pos=[];typ=[]
    corners=[(240,740),(840,740),(840,1340),(240,1340)]
    for k,(cx,cy) in enumerate(corners):
        for i in range(N):
            pos.append([cx+r.normal(0,55),cy+r.normal(0,55)]); typ.append(k)
    pos=np.array(pos); typ=np.array(typ); ang=r.uniform(0,2*np.pi,len(pos)); sp=2.4
    vel=np.stack([np.cos(ang),np.sin(ang)],1)*sp
    hist=[];counts=[];events=[]
    for f in range(FR):
        vel+=r.normal(0,0.25,vel.shape); n=np.linalg.norm(vel,axis=1,keepdims=True); vel=vel/n*sp
        pos+=vel
        for d,(lo,hi) in enumerate([(BOX[0]+R,BOX[2]-R),(BOX[1]+R,BOX[3]-R)]):
            m=pos[:,d]<lo; pos[m,d]=lo; vel[m,d]*=-1
            m=pos[:,d]>hi; pos[m,d]=hi; vel[m,d]*=-1
        D=np.linalg.norm(pos[:,None]-pos[None],axis=2); ii,jj=np.where(np.triu(D<2*R,1))
        for i,j in zip(ii,jj):
            a,b=typ[i],typ[j]
            if a==b: continue
            if (a+1)%4==b: typ[j]=a; events.append(f)
            elif (b+1)%4==a: typ[i]=b; events.append(f)
            else:
                if r.random()<0.5: typ[j]=a
                else: typ[i]=b
                events.append(f)
        c=np.bincount(typ,minlength=4); counts.append(c.tolist()); hist.append((pos.copy(),typ.copy()))
        if c.max()==len(typ): return f,counts,hist
    return None,counts,hist
if __name__=='__main__':
    res=[]
    for s in range(int(sys.argv[1]),int(sys.argv[2])):
        end,counts,_=run(s)
        if end is None: continue
        c=np.array(counts); leader=c.argmax(1); changes=int((np.diff(leader)!=0).sum()); winner=int(c[-1].argmax())
        mins=c.min(1); elim=[int(np.argmax(c[:,k]==0)) if (c[:,k]==0).any() else -1 for k in range(4)]
        res.append((s,end,changes,winner,sorted(elim)))
        print(s,end,round(end/30,1),'lead changes',changes,'winner',winner,'elim',sorted(elim),flush=True)
