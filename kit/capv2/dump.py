import json,sys
d=json.load(open(sys.argv[1]))['data']
d.sort(key=lambda p:(p['publicationDate']['dateTime'],str([x['network'] for x in p['providers']])))
for p in d:
    nets='+'.join(x['network'] for x in p['providers'])
    st=set(x['status'] for x in p['providers'])
    print('###',p['publicationDate']['dateTime'],nets,'id',p['id'],'uuid',p['uuid'],'draft',p['draft'],'status',st, 'media',p['media'][0].split('/')[-1] if p['media'] else None)
    if p['draft']: print('  TEXT1:',p['text'].split('\n')[0][:90]); continue
    print('  TEXT:',json.dumps(p['text'],ensure_ascii=False))
    print('  FC:',json.dumps(p.get('firstCommentText',''),ensure_ascii=False))
    if 'youtubeData' in p: print('  YT:',p['youtubeData'].get('title'))
