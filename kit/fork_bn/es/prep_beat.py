# prep_beat.py TRACKID REEL D_S TARGET_BPM BEAT0_S [prefer_start_s]
# Epidemic loopable edit (PREFER strongest section), time-stretched to TARGET_BPM (atempo, <2%), then rotated (circular, loop stays seamless)
# so a downbeat lands on BEAT0_S. Saves WAV to epidemic/tracks/<name>__<reel>.wav and fork_bn/es/tmp/prep_<reel>.json
import sys,os,json,time,subprocess,urllib.request,re
import numpy as np, librosa, soundfile as sf
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import esx
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
TR=S+'/epidemic/tracks/'; TMP=S+'/fork_bn/es/tmp/'
tid,reel=sys.argv[1],sys.argv[2]; D=float(sys.argv[3]); TB=float(sys.argv[4]); B0=float(sys.argv[5]); fs=float(sys.argv[6]) if len(sys.argv)>6 else None
r=json.load(open(os.path.dirname(os.path.abspath(__file__))+'/cache.json'))[tid]
art=', '.join(c['artist']['name'] for c in r['credits'] if c['role']=='MAIN_ARTIST')
name=re.sub(r'[^a-z0-9]+','_',r['title'].lower()).strip('_')[:40]
ratio=TB/r['bpm']; assert abs(ratio-1)<0.025, ratio
Le=D*ratio
pv=TMP+tid+'.mp3'; urllib.request.urlretrieve(r['audioFile']['lqmp3Url'],pv)
y,sr=librosa.load(pv,sr=22050,mono=True); os.remove(pv)
rms=librosa.feature.rms(y=y,hop_length=512)[0]; ot=librosa.frames_to_time(np.arange(len(rms)),sr=sr,hop_length=512); ref=np.percentile(rms,95); dur=len(y)/sr
L=max(Le,10.0)
def seg(a,b):
    i,j=np.searchsorted(ot,a),np.searchsorted(ot,b); return rms[i:max(j,i+1)].mean()/ref
best=max(((seg(t,t+L),t) for t in np.arange(0.5,dur-L-1,0.5)),default=(0,0.5)); st=fs if fs is not None else best[1]
print(f"{r['title']} / {art} {r['bpm']}bpm; strongest section {best[1]:.1f}s ({best[0]:.2f}); prefer {st:.1f}s; edit {Le:.3f}s -> stretch x{1/ratio:.4f}")
args={'id':tid,'input':{'targetDurationMs':int(round(Le*1000)),'loopable':True,'forceDuration':True,'downloadAudioFormat':'WAV','skipStems':True,'maxResults':1,
      'preferenceRegions':[{'startMs':int(st*1000),'endMs':int(min(dur,st+L+4)*1000),'preferenceType':'PREFER'}]}}
job=esx.call('EditRecording',args); jid=list(job.get('data',job).values())[0]['id']
for i in range(100):
    p=list(esx.call('PollEditRecordingJob',{'id':jid}).get('data',{}).values())[0]
    if p['status'] in ('COMPLETED','FAILED'): break
    time.sleep(4)
if p['status']!='COMPLETED': print('EDIT',p['status']); sys.exit(2)
e=(p.get('edits') or [p['edit']])[0]
print('poll keys',list(p.keys()),'edit',{k:v for k,v in e.items() if k!='stems'} if isinstance(e,dict) else e)
for _k in range(6):
    try:
        d=esx.call('DownloadRecordingEdit',{'input':{'jobId':jid,'editId':e['id']}}); url=list(d.get('data',d).values())[0]['assetUrl']; break
    except RuntimeError as ex:
        print('dl retry',str(ex)[:120]); time.sleep(8)
raw=TMP+e['id']+'.wav'; urllib.request.urlretrieve(url,raw)
st_wav=TMP+e['id']+'_st.wav'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',raw,'-af',f'atempo={ratio:.6f}','-ar','48000',st_wav],check=True); os.remove(raw)
a,sr2=sf.read(st_wav); os.remove(st_wav)
if a.ndim==1: a=np.stack([a,a],1)
N=int(round(D*sr2)); a=a[:N] if len(a)>=N else np.concatenate([a,a[:N-len(a)]])
m=a.mean(1).astype(np.float32)
# beat phase: onset envelope folded on the target beat period; downbeat = strongest beat of 4
yy=librosa.resample(m,orig_sr=sr2,target_sr=22050); oenv=librosa.onset.onset_strength(y=yy,sr=22050,hop_length=256)
tt=librosa.frames_to_time(np.arange(len(oenv)),sr=22050,hop_length=256); BP=60/TB
ph=np.linspace(0,BP,200,endpoint=False)
sc=[np.interp((np.arange(0,D-BP,BP)+p),tt,oenv).mean() for p in ph]; p0=ph[int(np.argmax(sc))]
bars=[np.interp((np.arange(0,D-4*BP,4*BP)+p0+k*BP),tt,oenv).mean() for k in range(4)]; kd=int(np.argmax(bars)); pd=p0+kd*BP
shift=(pd-B0)%(4*BP)   # rotate left so the downbeat at pd moves to B0
sh=int(round(shift*sr2)); a=np.roll(a,-sh,axis=0)
outf=TR+f"{name}__{reel}.wav"; sf.write(outf,a,sr2,subtype='PCM_16')
# verify
m=a.mean(1).astype(np.float32); yy=librosa.resample(m,orig_sr=sr2,target_sr=22050); oenv=librosa.onset.onset_strength(y=yy,sr=22050,hop_length=256)
sc2=[np.interp((np.arange(0,D-BP,BP)+p),tt[:len(oenv)],oenv).mean() for p in ph]; p1=ph[int(np.argmax(sc2))]
print(f'beat phase {p0:.3f}s, downbeat beat {kd} ({bars}), rotated {shift:.3f}s; after: beat phase {p1:.3f}s (target {B0%BP:.3f})')
out={'reel':reel,'id':tid,'title':r['title'],'artist':art,'bpm':r['bpm'],'prefer_from_s':round(st,2),'D':D,'mode':'epidemic_loop_edit+atempo+beat_align','job':jid,'edit_id':e['id'],
     'atempo':round(ratio,6),'rotate_s':round(shift,3),'beat_phase_after':round(p1,3),'file':outf}
json.dump(out,open(TMP+f'prep_{reel}.json','w')); print(json.dumps(out))
