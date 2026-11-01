import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../../pixellab')
import jobs,mcp
T=open('../../pixellab/.token').read().strip()
def tileset():
    sid=mcp.session()
    r=mcp.call('create_sidescroller_tileset',{'lower_description':'red clay terracotta roof tiles on a wooden beam','transition_description':'mossy stone ridge cap','transition_size':0.25,'mode':'pro','tile_size':{'width':32,'height':32}},sid)
    t=jobs.txt(r); print(t[:600],flush=True)
    tid=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t).group(1)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_sidescroller_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('FAIL',t[:300]); return
    print(t[:1500],flush=True); open('roof.txt','w').write(t)
    for path,out in (('image?inline=true','roof_sheet.png'),('metadata','roof_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        try: open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
        except Exception as e: print('dl fail',path,e)
    print('tileset done',flush=True)
th=threading.Thread(target=tileset); th.start()
J=[('chimney','create_image_pro',{'description':'a short brick chimney with a little smoke, side view, JRPG village rooftop prop','width':48,'height':48},'chimney'),
('crate','create_image_pro',{'description':'a wooden crate, side view, JRPG prop','width':40,'height':40},'crate'),
('flag','create_image_pro',{'description':'a tall glowing golden finish flag banner on a pole with a lantern, side view, JRPG prop','width':48,'height':64},'flag')]
print(jobs.run_many(J,3)); th.join()
