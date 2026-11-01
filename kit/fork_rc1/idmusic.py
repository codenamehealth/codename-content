import numpy as np, subprocess, sys, glob
def dec(p, ss=0, t=None, sr=8000):
    cmd=['ffmpeg','-v','error','-ss',str(ss)]+(['-t',str(t)] if t else [])+['-i',p,'-ac','1','-ar',str(sr),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32)
v=dec(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]))
v=v-v.mean()
res=[]
for m in glob.glob(sys.argv[4]):
  try:
      a=dec(m); a=a-a.mean()
      n=len(a)+len(v); N=1<<int(np.ceil(np.log2(n)))
      c=np.fft.irfft(np.fft.rfft(a,N)*np.conj(np.fft.rfft(v,N)),N)[:len(a)-len(v)]
      # normalize by local energy
      cs=np.concatenate([[0],np.cumsum(a.astype(np.float64)**2)]); e=np.sqrt(np.maximum(cs[len(v):len(v)+len(c)]-cs[:len(c)],0))+1e-9
      sc=c/(e*np.linalg.norm(v)); i=int(np.argmax(sc)); res.append((sc[i],m.split('/')[-1],i/8000))
  except Exception: pass
for r in sorted(res)[-4:]: print(r)
