# logline.py REEL OLDTRACK EVENTS VOL LUFS TP FRAMES RANKNOTE [extra]
import sys,json,os,glob
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
R,old,ev,vol,lufs,tp,fr,rank=sys.argv[1:9]; extra=sys.argv[9] if len(sys.argv)>9 else ''
p=json.load(open(f'{S}/epidemic/agent/tmp/prep_{R}.json'))
name=os.path.basename(glob.glob(f'{S}/pixellab/batch_v3/{R}_*.mp4')[0])[:-4]
rot=f", rotated {p['rotate_bars']} bars ({p['rotate_s']}s) so it opens on a downbeat" if p.get('rotate_bars') else ', no rotation'
line=(f"{R} | Oct 29 Epidemic music pass: {old} -> Epidemic \"{p['title']}\" by {p['artist']} (id {p['id']}, {rank}), Epidemic EditRecording loopable {p['D']}s edit "
 f"(job {p['job']}, edit {p['edit_id']}, PREFER from {p['prefer_from_s']}s{rot}), file epidemic/tracks/{os.path.basename(p['file'])}, offset 0 | "
 f"SFX from {ev} via epidemic/agent/mix_es.py (pixellab/mix.py without the 1s music fade-out so the loop seam stays musical, and without its dynamic loudnorm) music vol {vol} (Oct 29 level rule: bed about 3 dB under the first Epidemic mixes), epidemic/agent/loudfix_es.sh (linear gain to -15 LUFS, limiter 0.71), mux2 onto the current video (video stream md5 identical, {fr} frames) | "
 f"{lufs} LUFS, true peak {tp} dBTP | previous file prev/{name}_preepidemic.mp4{(' | '+extra) if extra else ''}")
open(f'{S}/pixellab/batch_v3/log.txt','a').write(line+'\n'); print(line)
