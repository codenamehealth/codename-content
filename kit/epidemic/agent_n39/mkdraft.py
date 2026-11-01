import json,sys
ps=json.load(open('tmp/posts_3to8.json'))
for pid in sys.argv[1:]:
    p=[x for x in ps if str(x['id'])==pid][0]
    nets=[x['network'] for x in p['providers']]
    info={'publicationDate':p['publicationDate'],'text':p['text'],'firstCommentText':p.get('firstCommentText',''),
          'providers':[{'network':n} for n in nets],'media':p['media'],'autoPublish':True,'mediaAltText':p.get('mediaAltText',[None]),
          'shortener':False,'draft':True,'hasNotReadNotes':False,'descendants':[],'smartLinkData':{'ids':[]}}
    if 'videoCoverMilliseconds' in p: info['videoCoverMilliseconds']=p['videoCoverMilliseconds']
    for k in ('facebookData','tiktokData','youtubeData'):
        if k in p: info[k]=p[k]
    if 'instagram' in nets: info['instagramData']=p['instagramData']
    print('##',pid,p['uuid'],','.join(nets))
    print(json.dumps(info,ensure_ascii=False))
