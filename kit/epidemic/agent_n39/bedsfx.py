import sys,subprocess,numpy as np
def ld(f):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-map','0:a','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
f=sys.argv[1]; a0,a1=float(sys.argv[2]),float(sys.argv[3]); ts=[float(t) for t in sys.argv[4].split(',')]
x=ld(f); sr=16000; db=lambda v:20*np.log10(v+1e-9)
bed=np.sqrt((x[int(a0*sr):int(a1*sr)]**2).mean())
pk=[max(np.sqrt((x[int((t+o)*sr):int((t+o+0.05)*sr)]**2).mean()) for o in np.arange(0,0.25,0.025)) for t in ts]
print(f'bed {db(bed):.1f} dBFS; sfx peaks', ' '.join(f'{db(p):.1f}({db(p)-db(bed):+.1f})' for p in pk))
