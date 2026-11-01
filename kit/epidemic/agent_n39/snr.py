# snr.py video events music offset vol : SFX-only vs music-only RMS in each event window (0.2s)
import sys,subprocess,json,numpy as np,os
V,EV,M,MO,MV=sys.argv[1:6]
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
def ld(f):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-map','0:a','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
mixer=S+'/epidemic/agent_n39/mix_es.py'
subprocess.run(['python3',mixer,V,EV,M,MO,'/tmp/_m.mp4',MV],capture_output=True)
ev=json.load(open(EV)); json.dump({'events':[]},open('/tmp/_e.json','w'))
subprocess.run(['python3',mixer,V,'/tmp/_e.json',M,MO,'/tmp/_mo.mp4',MV],capture_output=True)
a=ld('/tmp/_m.mp4'); m=ld('/tmp/_mo.mp4'); n=min(len(a),len(m)); s=a[:n]-m[:n]; m=m[:n]; sr=16000
r=lambda x,t:np.sqrt((x[int(t*sr):int((t+0.2)*sr)]**2).mean()+1e-12)
out=[f"{t:.1f}{nm[:5]}:{20*np.log10(r(s,t)/r(m,t)):+.1f}" for t,nm in ev['events']]
print(f'vol {MV}: SFX/music dB', ' '.join(out))
for f in ['/tmp/_m.mp4','/tmp/_mo.mp4','/tmp/_e.json']: os.remove(f)
