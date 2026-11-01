import json,sys,subprocess,os,re
R='/root/.claude/projects/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/tool-results/'
posts=[]
for f in ['toolu_0193AgoePhU38JD1D5PhQFFf.json','toolu_01TZCRwYPY4zvVg8jqAnBu11.json','toolu_017rLA99qHJBLEqRN6W48rEK.json']:
    d=json.load(open(R+f)); posts+=json.loads(d[0]['text'])['data']
seen=set(); ps=[]
for p in posts:
    if p['id'] in seen: continue
    seen.add(p['id']); ps.append(p)
slots={'14':'2026-10-30T10:00','12':'2026-10-30T20:00','16':'2026-10-31T10:00','18':'2026-10-31T16:00','21':'2026-11-01T16:00','34':'2026-11-02T10:00','26':'2026-11-02T16:00','27':'2026-11-02T20:00','38':'2026-11-03T10:00','30':'2026-11-03T16:00','36':'2026-11-04T16:00'}
V='pixellab/batch_v3/'
files={n:[x for x in os.listdir(V) if x.startswith(n.zfill(3)+'_')][0] for n in slots}
for n,t in slots.items():
    live=[p for p in ps if p['publicationDate']['dateTime'].startswith(t) and not p['draft']]
    sz=os.path.getsize(V+files[n])
    out=[]
    for p in live:
        u=p['media'][0]
        cl=subprocess.run(['curl','-sIL',u],capture_output=True,text=True).stdout
        m=re.findall(r'content-length:\s*(\d+)',cl,re.I)
        net=','.join(x['network'][:2] for x in p['providers'])
        yt='QUEST' in (p.get('text','')+(p.get('firstCommentText') or '')) and 'youtube' in net
        hs='#' in p.get('text','')
        out.append(f"{net}:{'OK' if m and int(m[-1])==sz else 'BAD '+str(m)} ap={p['autoPublish']}{' YTQUEST!' if yt else ''}{' HASH!' if hs else ''}")
    print('#'+n,t,len(live),'live |',' ; '.join(out))
