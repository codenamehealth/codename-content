# check.py video.mp4 events.json : SFX peak over bed at each event, first-0.5s level
import sys,json,subprocess,numpy as np
V,EV=sys.argv[1:3]
raw=subprocess.run(['ffmpeg','-loglevel','error','-i',V,'-map','0:a','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
x=np.frombuffer(raw,dtype=np.float32); sr=16000
def rms(a,b):
    s=x[max(0,int(a*sr)):max(int(a*sr)+1,int(b*sr))]; return np.sqrt((s**2).mean()+1e-12)
tot=rms(0,len(x)/sr)
db=lambda v:20*np.log10(v+1e-12)
ev=json.load(open(EV))['events']
out=[]
for t,n in ev:
    pk=max(rms(t+o,t+o+0.05) for o in np.arange(0,0.25,0.025))
    bed=np.median([rms(t+o,t+o+0.05) for o in np.arange(-0.6,-0.1,0.05) if t+o>=0] or [rms(t+0.3,t+0.8)])
    out.append(f"{t:.2f}{n[:6]}:{db(pk)-db(bed):+.1f}dB")
print('first0.5s vs whole:',f"{db(rms(0,0.5))-db(tot):+.1f}dB",'| SFX peak over preceding bed:',' '.join(out))
