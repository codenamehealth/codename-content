import mcp,json,time,re,urllib.request,os,sys
W='upload:0a73ecda-bf23-46be-b563-c6789bba659e'; A='upload:21fdacae-c527-444a-bfa1-ccc0ffcef508'
subj='a young knight girl in silver plate armour with a blue shield with a gold crest and a short steel sword, black ponytail'
jobs=[
 ('walk_mm','animate_image_pixminimax',{'first_frame_url':W,'description':'walking forward to the right in a looping walk cycle, legs alternating, holding shield and sword','frame_count':8,'seed':11,'direction':'east','view':'side','subject_description':subj}),
 ('attack_ai','animate_image',{'first_frame_url':A,'action':'raises the sword overhead and slashes down in front of her to the right, then returns to ready stance','frame_count':12,'seed':12}),
 ('attack_mm','animate_image_pixminimax',{'first_frame_url':A,'description':'raises the sword overhead and slashes down in front of her to the right, then returns to ready stance','frame_count':12,'seed':12,'direction':'east','view':'side','subject_description':subj}),
 ('eat_ai','animate_image',{'first_frame_url':W,'action':'lifts a small red gummy candy to her mouth with her free hand, eats it, then lowers her hand and smiles','frame_count':10,'seed':13}),
 ('eat_mm','animate_image_pixminimax',{'first_frame_url':W,'description':'lifts a small red gummy candy to her mouth, eats it, then lowers her hand and smiles','frame_count':12,'seed':13,'direction':'east','view':'side','subject_description':subj}),
]
def fetch(name,jid,sid):
    while True:
        r=mcp.call('get_image',{'job_id':jid},sid)
        t=''.join(c.get('text','') for c in r['result']['content'] if c.get('type')=='text')
        if 'status: completed' in t:
            n=int(re.search(r'frames: (\d+)',t).group(1)); os.makedirs(f'cleo/{name}',exist_ok=True)
            for i in range(n):
                urllib.request.urlretrieve(f'https://api.pixellab.ai/mcp/images/{jid}/download?index={i}',f'cleo/{name}/{i:02d}.png')
            print(name,'done',n,re.search(r'charged: .*',t).group(0) if 'charged' in t else '',flush=True); return
        if 'fail' in t[:200].lower(): print(name,'FAILED',t[:500],flush=True); return
        time.sleep(15)
sid=mcp.session()
fetch('walk_ai','96f483e0-0819-40e8-a1a7-bb1c31b0dbab',sid)
for name,tool,args in jobs:
    while True:
        sid=mcp.session()
        r=mcp.call(tool,args,sid); t=''.join(c.get('text','') for c in r['result']['content'] if c.get('type')=='text')
        if 'rate limit' in t: time.sleep(10); continue
        m=re.search(r'job_id: (\S+)',t)
        if not m: print(name,'ERR',t[:600],flush=True); break
        print(name,'submitted',re.search(r'cost: .*',t).group(0) if 'cost:' in t else '',flush=True)
        fetch(name,m.group(1),sid); break
print('ALL DONE',flush=True)
