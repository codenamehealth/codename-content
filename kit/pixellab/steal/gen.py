import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'..')
import jobs,mcp
T=open('../.token').read().strip()
def tileset():
    sid=mcp.session()
    r=mcp.call('create_topdown_tileset',{'lower_description':'warm sandy cobblestone village plaza, light tan and beige rounded stones','upper_description':'lush green grass with tiny yellow and white flowers','transition_size':0.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t); tid=m.group(1); print('tileset',tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('TILESET FAIL',t[:300]); return
    for path,out in (('image?inline=true','plaza_sheet.png'),('metadata','plaza_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print('tileset done',flush=True)
th=threading.Thread(target=tileset); th.start()
J=[('basket','create_image_pro',{'description':'an empty round woven wicker basket seen from a high top-down angle, warm brown, JRPG village prop','width':48,'height':48},'basket'),
('blanket','create_image_pro',{'description':'a round red and white checkered picnic blanket lying flat on the ground, seen from directly above, JRPG village prop','width':64,'height':64},'blanket'),
('barrel','create_image_pro',{'description':'a wooden barrel with iron bands seen from a high top-down angle, JRPG village prop','width':40,'height':40},'barrel'),
('crate','create_image_pro',{'description':'a wooden market crate full of oranges seen from a high top-down angle, JRPG village prop','width':48,'height':48},'crate'),
('flowers','create_image_pro',{'description':'a small round clay pot with pink and yellow flowers seen from a high top-down angle, JRPG village prop','width':32,'height':32},'flowers')]
print(jobs.run_many(J,5)); th.join()
