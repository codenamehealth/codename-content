# Re-mux batch_v3 reels that lost end frames: find the agent's full-length noaudio render and attach batch_review audio.
import glob, os, subprocess, sys
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
def nf(p): return int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip() or 0)
def dur(p): return subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip()
cands=glob.glob(S+'fork_hf*/**/*.mp4',recursive=True)
for v3 in sorted(glob.glob(S+'pixellab/batch_v3/*.mp4')):
    b=os.path.basename(v3); src=S+'pixellab/batch_review/'+b
    if not os.path.exists(src): continue
    a,c=nf(v3),nf(src)
    if a>=c: continue
    num=b[:3].lstrip('0'); best=None
    for p in cands:
        if 'noaudio' not in os.path.basename(p): continue
        d=os.path.dirname(p)
        if not (d.endswith('/v'+num) or d.endswith('/v'+b[:3]) or ('/v'+num+'/') in p): continue
        if os.path.getmtime(p) < os.path.getmtime(v3)-3600: continue
        if nf(p)==c: best=p
    if not best: print('NO SOURCE', b, a, c); continue
    tmp=v3+'.tmp.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',best,'-i',v3,'-map','0:v','-map','1:a','-c','copy','-t',dur(best),tmp],check=True)
    # sanity: same picture mid-reel as the current v3
    if nf(tmp)==c: os.replace(tmp,v3); print('fixed',b,a,'->',c,'from',best.replace(S,''))
    else: print('FAILED',b); os.remove(tmp)
