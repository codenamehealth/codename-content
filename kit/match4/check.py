import numpy as np
P=4*650; V=np.array([610,-480,730,-550]); TM=192/30
best=[]
for f in range(300):
    t=f/30; off=(V*(t-TM))%P; off=np.where(off>P/2,off-P,off)
    spread=np.ptp(off) if True else 0
    # circular spread around col0
    rel=((V-V[0])*(t-TM))%P; rel=np.where(rel>P/2,rel-P,rel)
    best.append((np.abs(rel).max(),f))
best.sort(); print(best[:8])
