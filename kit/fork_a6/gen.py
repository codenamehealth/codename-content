import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../pixellab')
import jobs,mcp
T=open('../pixellab/.token').read().strip()
def tileset(name, lower, upper):
    sid=mcp.session()
    r=mcp.call('create_topdown_tileset',{'lower_description':lower,'upper_description':upper,'transition_size':0.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t); tid=m.group(1); print(name,'tileset',tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('TILESET FAIL',name,t[:300]); return
    for path,out in (('image?inline=true',f'{name}_sheet.png'),('metadata',f'{name}_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print(name,'tileset done',flush=True)
ths=[threading.Thread(target=tileset,args=a) for a in [('track','packed red clay running track surface, smooth reddish brown','short bright green grass with a few tiny flowers'),('river','clear blue river water with gentle ripples and light sparkles','sandy pebble riverbank with small grass tufts')]]
for th in ths: th.start()
J=[('barrel','create_image_pro',{'description':'a round wooden barrel boat with the top open and empty inside, floating, seen from a high top-down angle, JRPG prop','width':64,'height':64},'barrel'),
('rock','create_image_pro',{'description':'a mossy grey river boulder seen from a high top-down angle, JRPG prop','width':48,'height':48},'rock'),
('ledge','create_image_pro',{'description':'a mossy ancient stone brick ledge platform with a flat walkable top, side view, JRPG platformer tile','width':128,'height':32},'ledge'),
('templebg','create_image_pro',{'description':'interior of a tall sunken ancient temple shaft, mossy stone brick walls with glowing teal runes, hanging vines, soft light beams from above, side view platformer game background, cozy JRPG pixel art','width':384,'height':688,'no_background':False},'templebg'),
('templebg2','create_image_pro',{'description':'tall vertical ancient stone tower interior seen from the side, mossy bricks, carved pillars, hanging green vines and small waterfalls, warm torchlight, cozy JRPG pixel art background','width':384,'height':688,'no_background':False},'templebg2'),
('dock','create_image_pro',{'description':'a small wooden river dock finish line with two posts and a checkered banner between them, seen from a high top-down angle, JRPG prop','width':96,'height':64},'dock')]
print(jobs.run_many(J,6))
for th in ths: th.join()
