# mkinfo.py posts.json "slot=reel" ... : print update payloads for the non-draft posts in each slot
import json,sys
raw=json.load(open(sys.argv[1]))
d=json.loads(raw[0]['text'])['data'] if isinstance(raw,list) else raw['data']
media=json.load(open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/epidemic/agent_n39/tmp/media.json'))
for spec in sys.argv[2:]:
    slot,reel=spec.split('=')
    ps=[p for p in d if p['publicationDate']['dateTime'].startswith(slot) and not p['draft']]
    print(f'## {reel} {slot} live={len(ps)}')
    for p in ps:
        nets=[x['network'] for x in p['providers']]
        info={'publicationDate':p['publicationDate'],'text':p['text'],'firstCommentText':p.get('firstCommentText',''),
              'providers':[{'network':n} for n in nets],'media':[f"https://d2ol7oe51mr4n9.cloudfront.net/user_3JL1Gr5rHOzCnvQ5HbpmsPan7mx/{media[reel]}.mp4"],
              'autoPublish':True,'mediaAltText':[None],'shortener':False,'draft':False,'videoCoverMilliseconds':p.get('videoCoverMilliseconds',300),
              'hasNotReadNotes':False,'descendants':[],'smartLinkData':{'ids':[]}}
        for k in ('facebookData','tiktokData','youtubeData'):
            if k in p: info[k]=p[k]
        if 'instagram' in nets: info['instagramData']=p['instagramData']
        print(p['id'],p['uuid'],','.join(nets),'MUSICLINE' if 'Music:' in p['text'] or '🎵' in p['text'] else '')
        print(json.dumps(info,ensure_ascii=False))
