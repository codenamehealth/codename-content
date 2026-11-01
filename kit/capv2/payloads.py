import json
posts={}
for f in ('raw_oct30_31.txt','raw_nov01_02.txt','raw_nov03_04.txt'):
    for p in json.load(open(f))['data']: posts[p['id']]=p
D=json.load(open('drafts.json'))
EXCL={'2026-10-31 10:00','2026-10-31 16:00','2026-10-31 19:00','2026-10-31 22:00'}
out=[];miss=[]
KEEP=['autoPublish','draft','hasNotReadNotes','media','mediaAltText','publicationDate','shortener','videoCoverMilliseconds','videoThumbnailUrl']
for d in D:
    s=d['slot']
    if not s.startswith('2026-') or s in EXCL or s>'2026-11-04 23:59' or s<'2026-10-30 19:00': continue
    for net,key in (('fbig','fb'),('tt','tt'),('yt','yt')):
        if not d.get(net): continue
        pid,uuid=d[net]
        p=posts.get(pid)
        if not p or p['uuid']!=uuid or p['draft']: miss.append((s,net,pid)); continue
        info={k:p[k] for k in KEEP if k in p}
        info['descendants']=[]; info['smartLinkData']={'ids':[]}
        info['autoPublish']=True
        info['providers']=[{'network':x['network']} for x in p['providers']]
        nets={x['network'] for x in p['providers']}
        if 'facebook' in nets: info['facebookData']=p['facebookData']
        if 'instagram' in nets: info['instagramData']=p['instagramData']
        if 'tiktok' in nets:
            td=dict(p['tiktokData']); td['title']=d['tt_title']; info['tiktokData']=td
        if 'youtube' in nets: info['youtubeData']=p['youtubeData']
        info['text']=d[key+'_cap']; info['firstCommentText']=d[key+'_pin']
        out.append(dict(slot=s,net=net,id=pid,uuid=uuid,info=info))
json.dump(out,open('push.json','w'),ensure_ascii=False,indent=0)
print(len(out),'payloads; missing',miss)
