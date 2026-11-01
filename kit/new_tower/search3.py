from sim import run, fallen
import math
seq=['ACV','CREATINE','MUSHROOM','MELATONIN','ACV','MUSHROOM','CREATINE','MELATONIN']
times=[0.6,1.5,2.4,3.3,4.2,5.1,6.0,6.9]
for d in [9]:
  for fat in [0,20,40]:
    for fv in [600,1200]:
      for fm in [1.0,1.6]:
        offs=[k*d for k in range(7)]+[6*d+fat]
        out=run(seq,offs,times,7,1.8,DUR=12.5,fv=fv,fm=fm)
        st=next((f/30 for f in range(int(8.7*30),len(out)) if max(abs(math.degrees(p[2])) for p in out[f][:7])>8),None)
        print(d,fat,fv,fm,'collapse start',st,'fallen end',fallen(out[int(12.3*30)]),flush=True)
