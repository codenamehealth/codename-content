import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../../pixellab')
import jobs,mcp
T=open('../../pixellab/.token').read().strip()
def tileset(name, lower, upper):
    sid=mcp.session()
    r=mcp.call('create_topdown_tileset',{'lower_description':lower,'upper_description':upper,'transition_size':0.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t); tid=m.group(1); print('tileset',name,tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('TILESET FAIL',name,t[:300]); return
    for path,out in (('image?inline=true',name+'_sheet.png'),('metadata',name+'_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print('tileset done',name,flush=True)
ths=[threading.Thread(target=tileset,args=a) for a in [
 ('soil','rich brown underground soil with small pebbles and roots, cross section','grey layered bedrock stone with cracks'),
 ('deep','dark purple-grey deep cave rock with tiny glowing crystal specks','dark basalt rock with orange glowing magma veins'),
 ('court','light grey castle courtyard flagstones with thin moss lines','neat trimmed green castle lawn grass')]]
for t in ths: t.start()
J=[('apple','create_image_pro',{'description':'a single shiny crisp red apple with a green leaf, JRPG item icon','width':32,'height':32},'apple'),
('beet','create_image_pro',{'description':'a single purple-red beetroot with green leaves, JRPG item icon','width':32,'height':32},'beet'),
('b12','create_image_pro',{'description':'a glowing pink vitamin capsule pill with sparkles, JRPG item icon','width':32,'height':32},'b12'),
('folate','create_image_pro',{'description':'a bright green leafy spinach leaf bundle, JRPG item icon','width':32,'height':32},'folate'),
('vinegar','create_image_pro',{'description':'a small corked glass bottle of golden amber apple cider vinegar, JRPG item icon','width':32,'height':32},'vinegar'),
('cherry','create_image_pro',{'description':'a pair of dark red tart cherries on a stem, JRPG item icon','width':32,'height':32},'cherry'),
('moon','create_image_pro',{'description':'a glowing purple crescent moon charm with tiny stars, JRPG item icon','width':32,'height':32},'moon'),
('bench','create_image_pro',{'description':'a rustic wooden alchemy workbench with a stone mortar and pestle, dried herbs and small jars, side view, JRPG prop','width':128,'height':80},'bench'),
('drill','create_image_pro',{'description':'a spinning steel drill head pointing straight down with golden bands, JRPG mining tool icon','width':32,'height':32},'drill'),
('fossil','create_image_pro',{'description':'an old fossil skull bone half buried, JRPG underground prop','width':32,'height':32},'fossil'),
('coins','create_image_pro',{'description':'a small pile of shiny gold coins and a red gem, JRPG treasure icon','width':32,'height':32},'coins'),
('root','create_image_pro',{'description':'a twisted old tree root hanging down, JRPG underground prop','width':32,'height':48},'root'),
('watch','create_image_pro',{'description':'an ornate golden pocket watch, front view, white clock face with black roman numerals, no hands, gold chain at the top, JRPG item','width':128,'height':128},'watch'),
('banner','create_image_pro',{'description':'a long blue castle banner with a gold shield crest hanging from a pole, front view, JRPG prop','width':48,'height':96},'banner')]
print(jobs.run_many(J,7))
for t in ths: t.join()
