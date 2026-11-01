import esx,json,time,sys,urllib.request,numpy as np,soundfile as sf,os
tid=sys.argv[1]; D=int(sys.argv[2]); variants=json.loads(sys.argv[3])
for v in variants:
    inp={'targetDurationMs':D,'downloadAudioFormat':'WAV','skipStems':True,'maxResults':2}; inp.update(v)
    j=esx.call('EditRecording',{'id':tid,'input':inp}); j=list(j.get('data',j).values())[0]['id']
    for i in range(90):
        p=list(esx.call('PollEditRecordingJob',{'id':j}).get('data',{}).values())[0]
        if p['status'] in ('COMPLETED','FAILED'): break
        time.sleep(4)
    print('##',json.dumps(v),p['status'],[ (e['id'][:8],e['durationMs']) for e in (p.get('edits') or [p.get('edit')]) if e])
    if p['status']!='COMPLETED': continue
    for e in (p.get('edits') or [p['edit']])[:2]:
        d=esx.call('DownloadRecordingEdit',{'input':{'jobId':j,'editId':e['id']}}); u=list(d.get('data',d).values())[0]['assetUrl']
        f='tmp/t_'+e['id']+'.wav'; urllib.request.urlretrieve(u,f); a,sr=sf.read(f); m=a.mean(1); os.remove(f)
        w=int(0.25*sr); print('  ',e['id'][:8],len(m)/sr,[round(float(np.sqrt((m[i:i+w]**2).mean())),2) for i in range(0,len(m),w)])
