import sys,re,time,json,urllib.request,threading,os; sys.path.insert(0,'../pixellab')
import jobs,mcp
T=open('../pixellab/.token').read().strip()
S='../syeda_src/'; R='../pixellab/race/in/'
SIDE={'joy':R+'joy_side.png','ray':R+'ray_side.png','cleo':R+'cleo_side.png','cyrus':R+'cyrus_side.png','hollow':S+'hollow/char2.png'}
FRONT={'joy':S+'char1/char11.png','ray':S+'char2/char4.png','cleo':S+'char3/char6.png','cyrus':S+'char4/char9.png','hollow':S+'hollow/char1.png'}
SUBJ={'joy':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff',
 'ray':'a young wizard with dark skin in a purple wizard hat and purple robe holding a golden staff',
 'cleo':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail',
 'cyrus':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit',
 'hollow':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'}
ups=jobs.upload(list(SIDE.values())+list(FRONT.values()))
def tileset(name,args):
    sid=mcp.session(); r=mcp.call('create_topdown_tileset',args,sid)
    t=jobs.txt(r); m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',t)
    if not m: print(name,'ERR',t[:300],flush=True); return
    tid=m.group(1); print(name,'tileset',tid,flush=True)
    while True:
        time.sleep(15); sid=mcp.session(); t=jobs.txt(mcp.call('get_topdown_tileset',{'tileset_id':tid},sid))
        if 'status: completed' in t: break
        if 'fail' in t[:200].lower(): print(name,'FAIL',t[:300],flush=True); return
    for path,out in (('image?inline=true',f'{name}_sheet.png'),('metadata',f'{name}_meta.json')):
        req=urllib.request.Request(f'https://api.pixellab.ai/mcp/tilesets/{tid}/{path}',headers={'Authorization':'Bearer '+T})
        open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
    print(name,'done',flush=True)
ths=[threading.Thread(target=tileset,args=a) for a in [
 ('volc',{'lower_description':'dark basalt volcanic rock ground with small cracks and grey ash','upper_description':'black obsidian volcanic rock wall with glowing orange magma cracks','transition_size':1.0,'tile_size':{'width':32,'height':32},'mode':'pro','view':'high top-down'}),
 ('lava',{'lower_description':'bubbling bright orange molten lava with yellow glowing swirls','upper_description':'dark basalt rock','transition_size':0.0,'tile_size':{'width':32,'height':32}})]]
for t in ths: t.start()
J=[]
for g in SIDE:
    J.append((g+'_climb','animate_image_pixminimax',{'first_frame_url':ups[SIDE[g]],'description':'climbing straight up a vertical vine hand over hand, body facing the vine, arms reaching up alternately, looping climb cycle','frame_count':8,'seed':31,'direction':'east','view':'side','subject_description':SUBJ[g]},g+'_climb'))
    J.append((g+'_dig','animate_image_pixminimax',{'first_frame_url':ups[FRONT[g]],'description':'raises arms overhead and smashes downward at the ground in front of their feet, looping strike','frame_count':8,'seed':32,'direction':'south','view':'side','subject_description':SUBJ[g]},g+'_dig'))
J+=[('stalk','create_image_pro',{'description':'a vertical segment of a giant thick green beanstalk vine with big curled leaves, straight up and down, JRPG pixel art','width':64,'height':160},'stalk'),
('cloud','create_image_pro',{'description':'a fluffy white and pale pink cumulus cloud, soft shading, JRPG pixel art','width':64,'height':40},'cloud'),
('cloudtop','create_image_pro',{'description':'a wide flat fluffy cloud platform with a small golden flag on top, JRPG pixel art','width':128,'height':64},'cloudtop'),
('portal','create_image_pro',{'description':'a glowing cool blue stone archway portal exit seen from a high top-down angle, JRPG pixel art','width':64,'height':64},'portal'),
('block','create_image_pro',{'description':'a single square carved light grey stone brick block, front view, game tile with beveled edges','width':32,'height':32},'block'),
('cave','create_image_pro',{'description':'underground cave cross-section side view, warm brown earth and stone layers, glowing crystals, roots hanging, cozy JRPG pixel art background','width':384,'height':688,'no_background':False},'cave'),
('mslime','create_image_pro',{'description':'a cute friendly round orange magma slime blob with a happy face and small glowing ember spots, JRPG pixel art','width':40,'height':40},'mslime'),
('paper','create_image_pro',{'description':'a blank cream parchment document page with a decorative gold border and a red wax seal at the bottom corner, front view, JRPG pixel art','width':96,'height':128},'paper')]
print(jobs.run_many(J,8),flush=True)
for t in ths: t.join()
print('ALL DONE')
