# prep.py TRACKID DURATION_S REEL [prefer_start_ms]
# -> Epidemic loopable edit (loopable+forceDuration, PREFER the track's strongest section), then rotated by whole bars
#    so the file opens on a strong downbeat (rotation keeps the loop seamless). Saves WAV to epidemic/tracks/.
import sys,os,json,time,subprocess,urllib.request,re
import numpy as np, librosa, soundfile as sf
import esx
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
TR=S+'/epidemic/tracks/'; TMP=S+'/epidemic/agent/tmp/'
os.makedirs(TR,exist_ok=True); os.makedirs(TMP,exist_ok=True)
tid=sys.argv[1]; D=float(sys.argv[2]); reel=sys.argv[3]; force_start=int(sys.argv[4]) if len(sys.argv)>4 else None
r=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache.json')))[tid]
art=', '.join(c['artist']['name'] for c in r['credits'] if c['role']=='MAIN_ARTIST')
name=re.sub(r'[^a-z0-9]+','_',r['title'].lower()).strip('_')[:40]
def get(url,path): urllib.request.urlretrieve(url,path); return path
# 1. strongest section of the full track (from the preview)
pv=get(r['audioFile']['lqmp3Url'],TMP+tid+'.mp3')
y,sr=librosa.load(pv,sr=22050,mono=True); os.remove(pv)
hop=512; rms=librosa.feature.rms(y=y,hop_length=hop)[0]; ot=librosa.frames_to_time(np.arange(len(rms)),sr=sr,hop_length=hop)
ref=np.percentile(rms,95); dur=len(y)/sr
L=max(D,10.0)
def seg(a,b):
    i,j=np.searchsorted(ot,a),np.searchsorted(ot,b); return rms[i:max(j,i+1)].mean()/ref
best=max(((seg(t,t+L),t) for t in np.arange(0.5,dur-L-1,0.5)),default=(0,0.5))
st=force_start/1000 if force_start is not None else best[1]
print(f"track {r['title']} / {art} bpm {r['bpm']} dur {dur:.1f}; strongest {L:.0f}s section starts {best[1]:.1f}s (level {best[0]:.2f}); prefer from {st:.1f}s")
# 2. Epidemic loopable edit
args={'id':tid,'input':{'targetDurationMs':int(round(D*1000)),'loopable':True,'forceDuration':True,'downloadAudioFormat':'WAV','skipStems':True,'maxResults':1,
      'preferenceRegions':[{'startMs':int(st*1000),'endMs':int(min(dur,st+L+4)*1000),'preferenceType':'PREFER'}]}}
out={'reel':reel,'id':tid,'title':r['title'],'artist':art,'bpm':r['bpm'],'prefer_from_s':round(st,2),'D':D}
job=esx.call('EditRecording',args); jid=list(job.get('data',job).values())[0]['id']
for i in range(100):
    p=list(esx.call('PollEditRecordingJob',{'id':jid}).get('data',{}).values())[0]
    if p['status'] in ('COMPLETED','FAILED'): break
    time.sleep(4)
if p['status']!='COMPLETED': print('EDIT',p['status']); sys.exit(2)
e=(p.get('edits') or [p['edit']])[0]
d=esx.call('DownloadRecordingEdit',{'input':{'jobId':jid,'editId':e['id']}}); url=list(d.get('data',d).values())[0]['assetUrl']
raw=get(url,TMP+e['id']+'.wav'); a,sr2=sf.read(raw); os.remove(raw)
if a.ndim==1: a=np.stack([a,a],1)
m=a.mean(1); N=len(m)
# 3. rotate by whole bars to open on the strongest downbeat
bar=4*60.0/r['bpm'] if r['bpm']>0 else 2.0
w=int(0.05*sr2); env=np.array([np.sqrt((m[i:i+w]**2).mean()) for i in range(0,N-w,w)]); emean=np.sqrt((m**2).mean())
def first05(sig): return np.sqrt((sig[:int(0.5*sr2)]**2).mean())/emean
def onset(sig): return np.sqrt((sig[:int(0.06*sr2)]**2).mean())/max(1e-6,np.sqrt((sig[-int(0.06*sr2):]**2).mean()))
cands=[]
k=0
while k*bar < D-0.5:
    sh=int(round(k*bar*sr2)); rot=np.roll(m,-sh)
    cands.append((first05(rot)+0.15*min(onset(rot),3)-(0.05 if k else 0),k,sh,first05(rot),onset(rot)))
    k+=1
cands.sort(reverse=True); sc,k,sh,f05,on=cands[0]
a=np.roll(a,-sh,axis=0)
outf=TR+f"{name}__{reel}.wav"; sf.write(outf,a,sr2,subtype='PCM_16')
print('rotation candidates (score,bars,first0.5,onsetratio):',[(round(c[0],2),c[1],round(c[3],2),round(c[4],2)) for c in cands[:5]])
out.update({'mode':'epidemic_loop_edit','job':jid,'edit_id':e['id'],'rotate_bars':k,'rotate_s':round(sh/sr2,3),'first05_ratio':round(f05,2),'file':outf,'edit_dur':N/sr2})
json.dump(out,open(TMP+f'prep_{reel}.json','w'))
print(json.dumps(out))
