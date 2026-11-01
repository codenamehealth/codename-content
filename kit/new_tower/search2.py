from sim import run, fallen
import math
seq=['ACV','CREATINE','MUSHROOM','MELATONIN','ACV','MUSHROOM','CREATINE','MELATONIN']
times=[0.6,1.5,2.4,3.3,4.2,5.1,6.0,6.9]
for d in [6,7,8,9]:
    for fat in [50,80,110]:
        offs=[k*d for k in range(7)]+[6*d+fat]
        out=run(seq,offs,times,7,1.8,DUR=12.5)
        tilt=max(abs(math.degrees(p[2])) for p in out[int(8.65*30)] if p)
        post=fallen(out[int(12.3*30)])
        # when collapse starts
        st=next((f/30 for f in range(int(8.7*30),len(out)) if max(abs(math.degrees(p[2])) for p in out[f][:7])>8),None)
        print(d,fat,'tilt@release',round(tilt,1),'collapse start',st,'fallen end',post,flush=True)
