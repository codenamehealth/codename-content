import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../../pixellab')
import jobs,mcp
T=open('../../pixellab/.token').read().strip()
def tileset(name,lower,upper):
    sid=mcp.session()
    r=mcp.call('create_topdown_tileset',{'lower_description':lower,'upper_description':upper,'transition_size':0.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t); tid=m.group(1); print(name,'tileset',tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('TILESET FAIL',t[:300]); return
    for path,out in (('image?inline=true',name+'_sheet.png'),('metadata',name+'_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print(name,'tileset done',flush=True)
th=threading.Thread(target=tileset,args=('hall','polished checkered cream and grey marble castle hall floor','royal red carpet with gold trim')); th.start()
J=[('shield','create_image_pro',{'description':'a large ornate blue and silver knight kite shield seen straight from the front, with a gold rim and an empty gummy-shaped dome hollow carved in the center, JRPG item','width':128,'height':128},'shield'),
('cardback','create_image_pro',{'description':'the back of a fantasy trading card, deep purple with tiny gold stars, an ornate gold border and a round gold medallion emblem in the center, front view, JRPG','width':96,'height':128},'cardback'),
('table','create_image_pro',{'description':'top-down view of a dark wooden tavern table surface made of wide planks with a few candle wax drips, seamless texture','width':128,'height':128,'no_background':False},'table'),
('stool','create_image_pro',{'description':'a round wooden stool with a red velvet cushion seen from a high top-down angle, JRPG castle prop','width':40,'height':40},'stool'),
('tray','create_image_pro',{'description':'an ornate golden display tray with deep purple velvet lining, seen from directly above, empty, JRPG treasure prop','width':128,'height':128},'tray'),
('candle','create_image_pro',{'description':'a lit candle in a small brass holder seen from a high top-down angle, JRPG prop','width':32,'height':32},'candle'),
('statue_base','create_image_pro',{'description':'a small square grey stone plinth seen from a high top-down angle, JRPG garden prop','width':32,'height':32},'plinth')]
print(jobs.run_many(J,6)); th.join()
