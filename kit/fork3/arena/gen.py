import sys,re,time,urllib.request; sys.path.insert(0,'../../pixellab')
import jobs,mcp
T=open('../../pixellab/.token').read().strip()
sid=mcp.session()
r=mcp.call('create_topdown_tileset',{'lower_description':'packed sandy dirt battle arena floor with small pebbles and footprints','upper_description':'lush green meadow grass with tiny white and yellow flowers','transition_size':0.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
t=jobs.txt(r); tid=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t).group(1); print('tileset',tid,flush=True)
while True:
    time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
    if 'status: completed' in t: break
    if 'fail' in t[:200].lower(): print('FAIL',t[:300]); sys.exit()
for path,out in (('image?inline=true','sheet.png'),('metadata','meta.json')):
    req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
    open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
print('done')
