import numpy as np, subprocess, sys, glob
def load(p, ss=0, t=None):
    cmd=['ffmpeg','-v','error','-ss',str(ss)]+(['-t',str(t)] if t else [])+['-i',p,'-ac','1','-ar','4000','-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,dtype=np.float32)
v=load(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
v=(v-v.mean())/(v.std()+1e-9)
res=[]
for m in sorted(glob.glob('music_adobe/*.wav')+glob.glob('music/*.wav')):
    a=load(m); 
    if len(a)<len(v): continue
    n=1<<int(np.ceil(np.log2(len(a)+len(v))))
    c=np.fft.irfft(np.fft.rfft(a,n)*np.conj(np.fft.rfft(v,n)),n)[:len(a)-len(v)]
    # normalize by local energy
    cs=np.concatenate([[0],np.cumsum(a**2)]); en=np.sqrt(np.maximum(cs[len(v):len(v)+len(c)]-cs[:len(c)], 0.3*len(v)*np.mean(a**2)))
    r=c/en/np.sqrt(len(v)); i=int(np.argmax(r)); res.append((float(r[i]),m,i/4000))
for r in sorted(res,reverse=True)[:4]: print(r)
