import json,subprocess,os,glob
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'
ps=json.load(open('tmp/posts_3to8.json'))
nov9={'11-09T16:00':['6346924956148573655','1526083380613812977','18372027182802719583'],
      '11-09T18:00':['2739271972860065700','7038255193090837557','11364137254317899746'],
      '11-09T20:00':['12351783797630242963','9877579712005497111','11766207565140595703']}
slots={'11-03T10:00':'038','11-03T16:00':'030','11-03T20:00':'040','11-04T10:00':'044','11-04T16:00':'036','11-04T20:00':'043',
 '11-05T10:00':'049','11-05T16:00':'042','11-05T18:00':'082','11-05T20:00':'045','11-06T10:00':'057','11-06T16:00':'075','11-06T20:00':'047',
 '11-07T10:00':'060','11-07T16:00':'083','11-07T18:00':'100','11-07T20:00':'090','11-08T16:00':'087','11-08T20:00':'095',
 '11-09T16:00':'096','11-09T18:00':'093','11-09T20:00':'072'}
for t,r in slots.items():
    f=glob.glob(f'{S}/pixellab/batch_v3/{r}_*.mp4')[0]
    ids=nov9.get(t) or [p['media'][0].split('file-')[1][:-4] for p in ps if p['publicationDate']['dateTime'][5:16]==t and not p['draft']]
    res=[]
    for u in ids:
        o=f'vf/{u}.mp4'; subprocess.run(['curl','-s','-o',o,f'https://static.metricool.com/planner/202610/7178389-file-{u}.mp4'])
        same=subprocess.run(['cmp','-s',o,f]).returncode==0; res.append('Y' if same else f'N({os.path.getsize(o)})'); os.remove(o)
    print(t,r,os.path.basename(f),os.path.getsize(f),len(ids),' '.join(res),flush=True)
