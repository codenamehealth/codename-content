import json,sys
ab={'facebook':'FB','instagram':'IG','youtube':'YT','tiktok':'TT','twitter':'X','linkedin':'LI','pinterest':'PI','threads':'TH','bluesky':'BS','gmb':'GMB'}
for f in sys.argv[1:]:
    raw=json.load(open(f))
    if isinstance(raw,list): raw=json.loads(raw[0]['text'])
    for p in sorted(raw['data'],key=lambda p:p['publicationDate']['dateTime']):
        dt=p['publicationDate']['dateTime']
        nets='+'.join(ab.get(x['network'],x['network']) for x in p['providers'])
        st=','.join(sorted(set(x.get('status','') for x in p['providers'])))
        med=p.get('media') or []
        kind='vid' if any(m.endswith('.mp4') or m.endswith('.mov') for m in med) else ('img%d'%len(med) if med else 'none')
        t=p.get('text','') or ''
        fc=p.get('firstCommentText','') or ''
        tt=(p.get('tiktokData') or {}).get('title','') or ''
        yt=(p.get('youtubeData') or {}).get('title','') or ''
        flags=[]
        if '#' in t+fc+tt+yt: flags.append('HASH')
        if nets=='TT' and 'Comment QUEST' in t+fc+tt: flags.append('TTONLY-COMMENTQUEST')
        if 'TT' in nets and 'Comment QUEST' in t+fc+tt: flags.append('TT+commentQUEST')
        if 'Link in bio' in t+fc+tt: flags.append('LIB')
        print(f"{'D' if p.get('draft') else '-'}|{dt}|{nets}|{kind}|{st}|{p['id']}|{p['uuid']}|{t.splitlines()[0] if t else ''}|{' '.join(flags)}")
