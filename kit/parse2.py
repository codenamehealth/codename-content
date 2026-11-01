import json,sys
seen=set()
for f in sys.argv[1:]:
    d=json.loads(open(f).read())
    for p in sorted(d['data'],key=lambda p:p['publicationDate']['dateTime']):
        t=p['text']; k=(p['publicationDate']['dateTime'],t.split('\n')[0])
        if k in seen: continue
        seen.add(k)
        lines=[l for l in t.split('\n') if not l.startswith('Side Quest') and l.strip()]
        yt=(p.get('youtubeData') or {}).get('title','')
        print(p['publicationDate']['dateTime'][:16],'D' if p.get('draft') else '-', ' // '.join(lines)[:200], '|YT:',yt)
