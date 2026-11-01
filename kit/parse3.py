import json,sys
seen=set()
for f in sys.argv[1:]:
    d=json.loads(open(f).read())
    if isinstance(d,list): d=json.loads(d[0]['text'])
    for p in sorted(d['data'],key=lambda p:p['publicationDate']['dateTime']):
        t=p['text']; k=(p['publicationDate']['dateTime'],t.split('\n')[0][:40])
        if k in seen: continue
        seen.add(k)
        lines=[l for l in t.split('\n') if not l.startswith(('Side Quest','Every Code Name','Our labels','🎵','Code Name:','Gummies for')) and l.strip()]
        yt=(p.get('youtubeData') or {}).get('title','')
        ext=p['media'][0].split('.')[-1] if p.get('media') else ''
        print(p['publicationDate']['dateTime'][5:16],'D' if p.get('draft') else '-',ext,p.get('videoCoverMilliseconds',''), ' // '.join(lines)[:150], '|YT:',yt[:60])
