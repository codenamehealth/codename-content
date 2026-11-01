import json
st=json.load(open('state.json')); src=st['src']; slots=st['slots']
H=json.load(open('hosted.json'))
plan=json.load(open('../pixellab/safezone/schedule_plan.json'))
S_ONLY={38,58}
CL="Characters by Syeda Humna, the Realm painted by Liza 🎨"; CS="Characters hand drawn by Syeda Humna 🎨"
L1="Our characters and labels are hand drawn by Syeda Humna, and the Realm is painted by Liza 🎨"
fixes={40:{'l1':'NPCs blocking the only path 🛡️','yt':'NPCs blocking the only path 🛡️ Which NPC blocked your path the longest?'},
66:{'l2':'Melatonin, Mushroom, ACV or Creatine 👇'},
75:{'l2':'Pause when the gummy fits the shield 👇'},
85:{'l2':'4 fighters, one arena. Pick one 👇','yt':'Arena war: 4 fighters, one arena ⚔️'}}
out=[]
for slot,n,cat in plan:
    if not isinstance(n,int): continue
    s=dict(src[str(n)]); s.update(fixes.get(n,{}))
    cred=CS if n in S_ONLY else CL
    sqb="Side Quest: free to enter, five winners each month win free gummies." if s.get('sq')=='wfg' else "Side Quest: free to enter, five winners each month."
    tail=[s['music']] if s.get('music') else []
    fb="\n".join([s['l1'],s['l2'],cred,sqb+" Comment QUEST to get in 🎁"]+tail)
    tt="\n".join([s['l1'],s['l2'],cred,sqb+" DM us QUEST to get in 🎁"]+tail)
    yt="\n".join([s['l1'],s['l2'],cred]+tail)
    d,t=slot.split(); off='-04:00' if d<'2026-11-01' else '-05:00'
    pd={"dateTime":f"{d}T{t}:00","timezone":"America/New_York"}
    url=H[str(n)]['url']
    common=dict(autoPublish=True,descendants=[],draft=False,hasNotReadNotes=False,media=[url],mediaAltText=[],publicationDate=pd,shortener=False,smartLinkData={"ids":[]},videoCoverMilliseconds=300)
    main=dict(common,text=fb,firstCommentText=L1+"\nWant in on Side Quest, our free monthly giveaway? Comment QUEST and we'll DM you 🎁",providers=[{"network":"facebook"},{"network":"instagram"}],facebookData={"type":"REEL"},instagramData={"type":"REEL","showReelOnFeed":True,"isAiGenerated":False})
    tk=dict(common,text=tt,firstCommentText=L1+"\nWant in on Side Quest, our free monthly giveaway? DM us QUEST 🎁",providers=[{"network":"tiktok"}],tiktokData={"privacyOption":"PUBLIC_TO_EVERYONE","title":tt,"photoCoverIndex":0})
    ytp=dict(common,text=yt,firstCommentText=L1,providers=[{"network":"youtube"}],youtubeData={"title":s['yt'],"type":"short","privacy":"public","category":"GAMING","madeForKids":False,"isAiGeneratedContent":False})
    for x in (fb,tt,yt,s['yt']): assert '—' not in x and '#' not in x and 'No AI' not in x
    assert 'QUEST' not in yt and 'Side Quest' not in s['yt']
    out.append(dict(slot=slot,num=n,cat=cat,cred='Syeda+Liza' if cred==CL else 'Syeda only',date=f"{d}T{t}:00{off}",slotposts=slots.get(slot),url=url,main=main,tt=tk,yt=ytp,changes=list(fixes.get(n,{}))))
json.dump(out,open('payloads.json','w'),ensure_ascii=False,indent=1)
print(len(out), 'missing slots:',[o['slot'] for o in out if not o['slotposts']])
