import os,sys
src=open('orig_render_safe.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search'")[0]
src=src.replace("os.chdir(os.path.dirname(os.path.abspath(__file__)))","os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/race')")
exec(src)
st,TL=run_sim(559)
for g in G:
    s=st[g]; print(g, 'fin',s['fin'] and round(s['fin'],2),'sneak',s['sneak'] and round(s['sneak'],2),'slimes',[round(x['x']) for x in s['slimes']], [(k,round(t,2)) for k,t in s['events']])
for t in [2.8,4,5,6,7,8,9,9.2,10.3,11,12,13,14,15,16,17,18,18.5]:
    f=int(t*FPS); print(t,{k:(round(v[0]),v[1]) for k,v in TL[f].items()})
