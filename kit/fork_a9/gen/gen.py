import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../../pixellab')
import jobs,mcp
T=open('../../pixellab/.token').read().strip()
def tileset(name,args):
    for attempt in range(5):
        try:
            sid=mcp.session(); r=mcp.call('create_topdown_tileset',args,sid)
            t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t)
            if m: break
            print(name,'retry',t[:200],flush=True); time.sleep(20)
        except Exception as e: print(name,'err',e,flush=True); time.sleep(20)
    tid=m.group(1); print(name,'tileset',tid,flush=True)
    while True:
        time.sleep(15)
        try: sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        except Exception as e: continue
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print(name,'FAIL',t[:300]); return
    for path,out in (('image?inline=true',f'{name}_sheet.png'),('metadata',f'{name}_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print(name,'done',flush=True)
TS=[('sky',{'lower_description':'fluffy white and pale blue cloud sea','upper_description':'lush green grass meadow with tiny flowers','transition_size':0.25,'transition_description':'rocky brown earth cliff edge','tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'}),
('sand',{'lower_description':'pale sandstone temple floor tiles','upper_description':'golden sandstone temple wall with carved sun glyphs and a dark top','transition_size':1.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'}),
('deck',{'lower_description':'weathered wooden plank deck','upper_description':'sparkling clear blue lake water','transition_size':0.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'})]
ths=[threading.Thread(target=tileset,args=a) for a in TS]
for t in ths: t.start()
J=[('pylon','create_image_pro',{'description':'a glowing white crystal obelisk on a round carved stone base, high top-down view, JRPG prop','width':48,'height':64},'pylon'),
('dial','create_image_pro',{'description':'a round carved grey stone rune dial wheel seen from the front, ornate gold rim, runes around the edge, JRPG puzzle object','width':80,'height':80},'dial'),
('vault','create_image_pro',{'description':'an ornate stone treasure vault wall with gold trim and glowing runes, front view, JRPG castle interior','width':170,'height':128,'no_background':False},'vault')]
print(jobs.run_many(J,3))
for t in ths: t.join()
