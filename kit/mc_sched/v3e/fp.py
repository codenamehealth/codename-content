import numpy as np, subprocess, glob, os, sys
SR=8000
def dec(p,dur=None):
    c=['ffmpeg','-v','error','-i',p]+(['-t',str(dur)] if dur else [])+['-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,dtype=np.float32).astype(np.float64)
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
lib={}
for p in sorted(glob.glob(S+'/music_adobe/*.wav')+glob.glob(S+'/music/*.wav')+glob.glob('/home/claude/tl/music/*.mp3')):
    x=dec(p,400); lib[p]=np.concatenate([x,x[:SR*30]])
def ncc(t,c):
    N=1<<int(np.ceil(np.log2(len(t)+len(c))))
    xc=np.fft.irfft(np.fft.rfft(t,N)*np.conj(np.fft.rfft(c,N)),N)[:len(t)-len(c)+1]
    c2=np.concatenate([[0],np.cumsum(t**2)]); e=np.sqrt(np.maximum(c2[len(c):]-c2[:-len(c)],1e-9))*np.linalg.norm(c)
    r=xc/e; i=int(np.argmax(np.abs(r))); return abs(float(r[i]))
for f in sys.argv[1:]:
    v=dec(f); wins=[v[s:s+3*SR] for s in range(0,max(1,len(v)-3*SR),2*SR)]
    wins=[w for w in wins if len(w)==3*SR and np.linalg.norm(w)>1e-3]
    res={os.path.basename(p):float(np.median([ncc(t,w) for w in wins])) for p,t in lib.items()}
    b=sorted(res.items(),key=lambda kv:-kv[1])[:3]
    print(os.path.basename(f),' | '.join(f'{k} {s:.2f}' for k,s in b),flush=True)
