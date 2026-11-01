import sys,re,time,json,urllib.request,threading; sys.path.insert(0,'../pixellab')
import jobs,mcp
T=open('../pixellab/.token').read().strip()
S='../syeda_src/'; R='../pixellab/race/in/'
def tileset(name,lower,upper,ts=1.0):
    sid=mcp.session()
    r=mcp.call('create_topdown_tileset',{'lower_description':lower,'upper_description':upper,'transition_size':ts,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'},sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t); tid=m.group(1); print('tileset',name,tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print('TILESET FAIL',t[:300]); return
    for path,out in (('image?inline=true',f'{name}_sheet.png'),('metadata',f'{name}_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print('tileset done',name,flush=True)
th=threading.Thread(target=tileset,args=('hedge','pale moonlit flagstone garden path, soft blue grey stones','tall dark green leafy hedge wall with a rounded leafy top')); th.start()
ups=jobs.upload([R+'joy_side.png',S+'char1/char11.png',S+'char4/char9.png',S+'char3/char6.png',S+'char2/char4.png',S+'hollow/char1.png','../pixellab/gummies/pick_mel.png'])
u=lambda p: ups[p]
SUBJ={'joy':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff','cyrus':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit','cleo':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail','ray':'a young wizard with dark skin in a purple wizard hat and purple robe holding a golden staff','hollow':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'}
J=[
 ('joy_fall','animate_image_pixminimax',{'first_frame_url':u(R+'joy_side.png'),'description':'running to the right, trips over a ledge and tumbles forward head over heels falling down out of frame','frame_count':12,'seed':31,'direction':'east','view':'side','subject_description':SUBJ['joy']},'joy_fall'),
 ('joy_plant','animate_image_pixminimax',{'first_frame_url':u(S+'char1/char11.png'),'description':'kneels down, plants a seed in the ground with both hands, pats the soil, then stands back up and smiles','frame_count':12,'seed':32,'direction':'south','view':'side','subject_description':SUBJ['joy']},'joy_plant'),
 ('cyrus_dance','animate_image_pixminimax',{'first_frame_url':u(S+'char4/char9.png'),'description':'dancing to the beat, bouncing up and down and pumping one fist in the air then the other, looping','frame_count':8,'seed':33,'direction':'south','view':'side','subject_description':SUBJ['cyrus']},'cyrus_dance'),
 ('joy_clap','animate_image_pixminimax',{'first_frame_url':u(S+'char1/char11.png'),'description':'clapping hands together to the beat and bobbing her head, looping','frame_count':8,'seed':34,'direction':'south','view':'side','subject_description':SUBJ['joy']},'joy_clap'),
 ('cleo_stomp','animate_image_pixminimax',{'first_frame_url':u(S+'char3/char6.png'),'description':'stomping one foot on the ground to the beat and nodding, looping','frame_count':8,'seed':35,'direction':'south','view':'side','subject_description':SUBJ['cleo']},'cleo_stomp'),
 ('ray_dance','animate_image_pixminimax',{'first_frame_url':u(S+'char2/char4.png'),'description':'swaying side to side to the music and waving the glowing staff overhead, looping','frame_count':8,'seed':36,'direction':'south','view':'side','subject_description':SUBJ['ray']},'ray_dance'),
 ('hollow_dance','animate_image_pixminimax',{'first_frame_url':u(S+'hollow/char1.png'),'description':'happily bouncing and waving both arms side to side to the music, looping','frame_count':8,'seed':37,'direction':'south','view':'side','subject_description':SUBJ['hollow']},'hollow_dance'),
 ('hollow_think','animate_image_pixminimax',{'first_frame_url':u(S+'hollow/char1.png'),'description':'thinking hard, scratching its head with one hand and tilting its head, looping','frame_count':8,'seed':38,'direction':'south','view':'side','subject_description':SUBJ['hollow']},'hollow_think'),
 ('boot','create_image_pro',{'description':'a single brown leather adventurer boot stomping, rhythm game icon, bold outline','width':32,'height':32},'boot'),
 ('clap','create_image_pro',{'description':'two cartoon hands clapping together with small motion lines, rhythm game icon, bold outline','width':32,'height':32},'clap'),
 ('scroll','create_image_pro',{'description':'a large open parchment scroll quest board with wooden rods top and bottom, blank aged paper in the middle, JRPG UI frame','width':240,'height':300,'no_background':True},'scroll'),
 ('sapling','create_image_pro',{'description':'a tiny green sapling sprout with two leaves growing from a small mound of soil, side view','width':32,'height':32},'sapling'),
 ('smalltree','create_image_pro',{'description':'a young leafy green tree, side view, round canopy, thin trunk, JRPG forest prop','width':64,'height':64},'smalltree'),
 ('bigtree','create_image_pro',{'description':'a big lush round fruit tree full of shiny orange gumdrop candies hanging among the leaves, side view, thick trunk, JRPG forest prop','width':128,'height':128,'reference_images':[{'url':u('../pixellab/gummies/pick_mel.png'),'usage':'the candies hanging in the tree look like this gummy'}]},'bigtree'),
 ('moongate','create_image_pro',{'description':'a glowing silver moon gate archway made of pale stone with a crescent moon on top and white light inside, high top-down view, JRPG garden maze exit','width':64,'height':64},'moongate'),
 ('lantern','create_image_pro',{'description':'a small glowing paper lantern on a short wooden post, warm yellow light, high top-down view, JRPG garden prop','width':32,'height':32},'lantern'),
 ('spirit','create_image_pro',{'description':'a cute round friendly shadow spirit blob, dark purple and black smoke body with two big glowing white eyes, JRPG creature','width':32,'height':32},'spirit'),
 ('pedestal','create_image_pro',{'description':'an ornate round stone pedestal with gold trim and a soft glow on top, side view, JRPG treasure display','width':64,'height':64},'pedestal'),
]
print(jobs.run_many(J,8)); th.join()
