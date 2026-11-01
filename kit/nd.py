import json,sys
s=open(sys.argv[1]).read()
raw=json.loads(s)
if isinstance(raw,list): raw=json.loads(raw[0]['text'])
d=raw['data']
nd=[p for p in d if not p.get('draft')]
print("total",len(d),"nondraft",len(nd))
for p in sorted(nd,key=lambda p:p['publicationDate']['dateTime']):
    q={k:p.get(k) for k in ['id','uuid','text','firstCommentText','media','videoCoverMilliseconds','videoThumbnailUrl','facebookData','instagramData','youtubeData','tiktokData']}
    q['date']=p['publicationDate']['dateTime']; q['prov']=[x['network'] for x in p['providers']]
    if q.get('tiktokData') and q['tiktokData'].get('title')==p['text']: q['tiktokData']=dict(q['tiktokData'],title='=TEXT')
    extra=set(p)-set(['id','uuid','text','firstCommentText','media','videoCoverMilliseconds','videoThumbnailUrl','facebookData','instagramData','youtubeData','tiktokData','publicationDate','creationDate','providers','autoPublish','saveExternalMediaFiles','mediaAltText','shortener','draft','imageVariants','twitterData','hasNotReadNotes','creatorUserMail','creatorUserId','brandTags'])
    if extra: q['EXTRA']={k:p[k] for k in extra}
    print(json.dumps({k:v for k,v in q.items() if v is not None},ensure_ascii=False)); print()
