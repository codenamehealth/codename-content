import json,subprocess,sys
# usage: mix.py video events.json music.wav music_offset out.mp4 [music_vol]
V,EV,M,MO,OUT=sys.argv[1:6]; MV=float(sys.argv[6]) if len(sys.argv)>6 else 0.55
SFXD='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/sfx_adobe/'
TRIM={'squish':0.28,'punch':0.0,'swish':0.0,'vg02':0.0,'whistle':0.0,'rewind':0.25}
DUR={'rewind':0.55}
VOL={'tick_8bit':0.35,'whoosh_8bit':0.45,'crunch_8bit':0.3,'poof':0.35,'cheer':0.3,'boing':0.55,'twinkle':0.7,'victory':0.9,'jump':0.3,'powerup_8bit':0.75,'coin_8bit':0.6,'squish':0.9,'punch':0.8,'swish':0.9,'vg02':0.55,'whistle':5.0,'rewind':1.4,'buzz_8bit':0.5,'ding_8bit':0.6}
ev=json.load(open(EV)); events=ev['events']
D=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',V],capture_output=True,text=True).stdout)
inputs=['-i',V,'-stream_loop','-1','-ss',str(MO),'-i',M]; fc=[f"[1:a]atrim=0:{D},asetpts=PTS-STARTPTS,afade=t=out:st={D-0.35:.2f}:d=0.35,volume={MV}[m]"]
labels=['[m]']
for i,(t,name) in enumerate(events):
    inputs+=['-i',SFXD+name+'.wav']; k=i+2
    tr=TRIM.get(name,0.0); end=f':end={tr+DUR[name]}' if name in DUR else ''
    fc.append(f"[{k}:a]atrim=start={tr}{end},asetpts=PTS-STARTPTS,volume={VOL.get(name,0.8)},adelay={int(t*1000)}|{int(t*1000)}[s{i}]"); labels.append(f'[s{i}]')
fc.append(''.join(labels)+f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.95,loudnorm=I=-14[a]")
cmd=['ffmpeg','-y','-loglevel','error']+inputs+['-filter_complex',';'.join(fc),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',OUT]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.stderr[-800:]); print(OUT)
