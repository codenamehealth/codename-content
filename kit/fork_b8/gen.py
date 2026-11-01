import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../pixellab')
import jobs,mcp
T=open('../pixellab/.token').read().strip()
def tileset(name, lower, upper, ts=1.0):
    sid=mcp.session()
    r=mcp.call('create_topdown_tileset',{'lower_description':lower,'upper_description':upper,'transition_size':ts,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t); tid=m.group(1); print(name,'tileset',tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('TILESET FAIL',t[:300]); return
    for path,out in (('image?inline=true',f'{name}_sheet.png'),('metadata',f'{name}_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print(name,'tileset done',flush=True)
th=threading.Thread(target=tileset,args=('snow','packed snowy cobblestone path with light footprints','snow covered grey stone brick wall with a white snowy top',1.0)); th.start()
ups=jobs.upload(['../pixellab/race/in/liza_style.png'])
style=ups['../pixellab/race/in/liza_style.png']
J=[
('surfboard','create_image_pro',{'description':'a single wooden surfboard seen exactly from the side, flat horizontal, warm tan with a red stripe, JRPG item','width':96,'height':32},'surfboard'),
('ocean','create_image_pro',{'description':'side view tropical ocean horizon at golden sunset, distant green islands with palm trees, soft clouds, warm sky, pixel art game background, no characters','width':448,'height':256,'no_background':False,'style_image_url':style},'ocean'),
('lighthouse','create_image_pro',{'description':'a small red and white lighthouse on a wooden pier with a checkered finish banner, side view, JRPG prop','width':128,'height':160},'lighthouse'),
('bonfire','create_image_pro',{'description':'a warm cozy campfire bonfire with logs and bright orange flames, high top-down view, JRPG prop','width':64,'height':64},'bonfire'),
('shadowtex','create_image_pro',{'description':'seamless swirling dark purple and black shadow mist texture with faint glowing violet wisps, fills the whole square','width':64,'height':64,'no_background':False},'shadowtex'),
('brick','create_image_pro',{'description':'a single small grey castle stone brick block, front view, JRPG tile','width':32,'height':32},'brick'),
('mirror','create_image_pro',{'description':'an ornate empty golden magic mirror frame, tall rectangle, purple gems at the corners, front view, transparent center, JRPG prop','width':160,'height':200},'mirror'),
('cauldron','create_image_pro',{'description':'a big round black iron witch cauldron seen from directly above, filled with bubbling bright green potion, JRPG prop','width':128,'height':128},'cauldron'),
('pine','create_image_pro',{'description':'a snow covered pine tree, high top-down view, JRPG prop','width':64,'height':64},'pine'),
('lamppost','create_image_pro',{'description':'a glowing iron street lantern post with warm yellow light, high top-down view, JRPG village prop','width':48,'height':64},'lamppost'),
]
print(jobs.run_many(J,8)); th.join()
