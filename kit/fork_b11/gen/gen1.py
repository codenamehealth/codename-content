import sys,os; sys.path.insert(0,'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab')
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11')
import jobs
P='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
files=['ref/style_forest.png','ref/style_village.png']+[f'ref/mush_{k}.png' for k in range(8)]+[f'ref/acv_{k}.png' for k in (0,2,5,6,7)]+[P+'pixellab/race/in/cyrus_side.png',P+'pixellab/race/in/joy_side.png',P+'syeda_src/hollow/char2.png']
U=jobs.upload(files)
J=[]
bgs=[('bg_grove','cozy enchanted mushroom forest clearing at golden hour, giant orange and brown mushrooms, mossy fallen logs, tall trees with warm sunbeams, soft grass and a dirt path across the lower third, side-view 2D game background, no characters','ref/style_forest.png'),
('bg_garden','cozy cottage kitchen garden on a sunny morning, an apple tree and a pomegranate tree, raised soil beds with beets and purple carrots, wooden fence and flowers, dirt path across the lower third, side-view 2D game background, no characters','ref/style_village.png'),
('bg_shop','interior of a cozy fantasy item shop, a long wooden shop counter across the lower middle, wooden shelves full of colorful potion bottles and candy jars, hanging lanterns, warm candle light, front view 2D game background, no characters','ref/style_village.png')]
for name,d,st in bgs:
    for s in (1,2):
        J.append((f'{name}_{s}','create_image_pro',{'description':d,'width':360,'height':640,'no_background':False,'style_image_url':U[st],'seed':s*7},f'gen/{name}_{s}'))
mn=['shaggy white lion\'s mane mushroom','glossy red reishi mushroom shelf','lumpy dark brown chaga mushroom chunk','orange cordyceps mushroom sprigs','brown and tan striped turkey tail mushroom fan','brown frilly maitake mushroom cluster','brown cremini mushroom','shiitake mushroom with a pale stem']
for k,d in enumerate(mn):
    J.append((f'mush_{k}','create_image_pro',{'description':f'a single {d}, cute JRPG ingredient item icon, game sprite','width':48,'height':48,'reference_images':[{'url':U[f'ref/mush_{k}.png'],'usage':'the exact ingredient, shape and colors to draw'}],'style_image_url':U[f'ref/mush_{k}.png'],'style_copy':['outline','shading']},f'gen/mush_{k}'))
an=[(0,'a small glass bottle of amber apple cider vinegar with a cork'),(2,'a single bright green leaf'),(5,'a halved red pomegranate showing its seeds'),(6,'a fresh red beetroot with green leaves'),(7,'a purple carrot with green leaves')]
for k,d in an:
    J.append((f'acv_{k}','create_image_pro',{'description':f'{d}, cute JRPG ingredient item icon, game sprite','width':48,'height':48,'reference_images':[{'url':U[f'ref/acv_{k}.png'],'usage':'the exact ingredient, shape and colors to draw'}],'style_image_url':U[f'ref/acv_{k}.png'],'style_copy':['outline','shading']},f'gen/acv_{k}'))
J.append(('cyrus_pick','animate_image_pixminimax',{'first_frame_url':U[P+'pixellab/race/in/cyrus_side.png'],'description':'crouches down, picks something up from the ground with both hands, then stands up and lifts it overhead happily','frame_count':8,'seed':31,'direction':'east','view':'side','subject_description':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit'},'gen/cyrus_pick'))
J.append(('joy_pick','animate_image_pixminimax',{'first_frame_url':U[P+'pixellab/race/in/joy_side.png'],'description':'crouches down, picks something up from the ground with one hand, then stands up and lifts it overhead happily','frame_count':8,'seed':32,'direction':'east','view':'side','subject_description':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff'},'gen/joy_pick'))
J.append(('hollow_pouch','animate_image_pixminimax',{'first_frame_url':U[P+'syeda_src/hollow/char2.png'],'description':'takes out a tiny coin pouch, peeks inside it, then his shoulders droop in disappointment','frame_count':8,'seed':33,'direction':'east','view':'side','subject_description':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'},'gen/hollow_pouch'))
print(jobs.run_many(J,8))
