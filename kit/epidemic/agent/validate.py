# validate.py CURRENT.mp4 EVENTS.json OLDMUSIC.wav OFFSET [VOL] : rebuild the old mix with pixellab/mix.py and correlate with the current audio
import sys,subprocess,numpy as np,os
V,EV,M,MO=sys.argv[1:5]; MV=sys.argv[5] if len(sys.argv)>5 else '0.55'
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
out=S+'/epidemic/agent/work/val.mp4'
subprocess.run(['python3',S+'/pixellab/mix.py',V,EV,M,MO,out,MV],capture_output=True)
def env(f):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-map','0:a','-ac','1','-ar','8000','-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32); w=200; n=len(x)//w
    return np.sqrt((x[:n*w].reshape(n,w)**2).mean(1))
a,b=env(V),env(out); n=min(len(a),len(b)); a,b=a[:n],b[:n]
c=np.corrcoef(np.log(a+1e-4),np.log(b+1e-4))[0,1]
print(f'envelope correlation old-rebuild vs current: {c:.3f}')
os.remove(out)
