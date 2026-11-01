from sim import run, fallen, PED_Y
import math, sys
seq=['ACV','CREATINE','MUSHROOM','MELATONIN','ACV','MUSHROOM','CREATINE','MELATONIN']
times=[0.6,1.5,2.4,3.3,4.2,5.1,6.0,6.9]
res=[]
for d in [10,13,16,19,22]:
    for fat in [40,70,100]:
        offs=[k*d for k in range(7)]+[6*d+fat]
        out=run(seq,offs,times,7,1.6,DUR=12.0)
        pre=fallen(out[int(8.4*30)]); post=fallen(out[int(11.8*30)])
        # max tilt of stack before fatal drop
        tilt=max(abs(math.degrees(p[2])) for p in out[int(8.4*30)] if p)
        print(d,fat,'fallen before',pre,'after',post,'tilt',round(tilt,1),flush=True)
