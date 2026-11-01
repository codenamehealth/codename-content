import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../../pixellab')
import jobs,mcp
T=open('../../pixellab/.token').read().strip()
def tileset():
    sid=mcp.session()
    r=mcp.call('create_topdown_tileset',{'lower_description':'dark brown cave dirt floor with small pebbles and cracks','upper_description':'rough grey cave rock wall with dark crevices and moss','transition_size':0.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t); tid=m.group(1); print('tileset',tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('TILESET FAIL',t[:300]); return
    for path,out in (('image?inline=true','cave_sheet.png'),('metadata','cave_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print('tileset done',flush=True)
th=threading.Thread(target=tileset); th.start()
ups=jobs.upload(['dragon256.png'])
D=ups['dragon256.png']
J=[('minecart','create_image_pro',{'description':'an empty wooden mine cart with iron bands and four wheels, seen from a high top-down angle, JRPG village prop','width':64,'height':64},'minecart'),
('crystal','create_image_pro',{'description':'a cluster of glowing blue and purple cave crystals growing from rock, seen from a high top-down angle, JRPG prop','width':48,'height':48},'crystal'),
('lantern','create_image_pro',{'description':'a warm glowing iron mining lantern hanging from a short wooden post, seen from a high top-down angle, JRPG prop','width':48,'height':48},'lantern'),
('scale','create_image_pro',{'description':'a large brass platform weighing scale with a flat wooden platform and a round dial gauge on a post, front view, JRPG shop prop','width':96,'height':96},'scale'),
('ddoze','animate_image_pixminimax',{'first_frame_url':D,'description':'slowly closes its eyes and lowers its head to doze, wings fold in, peaceful sleeping breath','frame_count':8,'seed':31,'direction':'east','view':'side','subject_description':'a red dragon sitting on a pile of gold coins and gems'},'ddoze'),
('dglare','animate_image_pixminimax',{'first_frame_url':D,'description':'snaps its head to face the viewer, eyes wide open, wings flare up in alert','frame_count':8,'seed':32,'direction':'east','view':'side','subject_description':'a red dragon sitting on a pile of gold coins and gems'},'dglare')]
print(jobs.run_many(J,6)); th.join()
