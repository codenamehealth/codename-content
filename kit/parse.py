import json,sys
for f in sys.argv[1:]:
    raw=open(f).read()
    try: d=json.loads(raw)
    except Exception:
        # maybe wrapped
        d=json.loads(raw[raw.index('{'):])
    if isinstance(d,list): d=d[0]
    if 'text' in d and isinstance(d['text'],str) and d['text'].startswith('{'): d=json.loads(d['text'])
    rows=[]
    for p in d['data']:
        nets=','.join(x['network'][:2] for x in p['providers'])
        fn=p['media'][0].split('/')[-1] if p.get('media') else ''
        ext=fn.split('.')[-1] if fn else ''
        t=p['text'].split('\n')[0][:90]
        rows.append((p['publicationDate']['dateTime'],nets,ext,'D' if p.get('draft') else '',t))
    for r in sorted(rows): print(' | '.join(r))
