import sys; sys.path.insert(0,'../pixellab')
import jobs
S='../syeda_src/'
SIDE={'joy':'../pixellab/race/in/joy_side.png','ray':'../pixellab/race/in/ray_side.png','cleo':'../pixellab/race/in/cleo_side.png','cyrus':'../pixellab/race/in/cyrus_side.png','hollow':S+'hollow/char2.png'}
SUBJ={'joy':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff',
 'ray':'a young wizard with dark skin in a purple wizard hat and purple robe holding a golden staff',
 'cleo':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail',
 'cyrus':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit',
 'hollow':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'}
ups=jobs.upload(list(SIDE.values())+['moon_style.png','hub_style.png','forest_style.png','castle_style.png'])
J=[]
for g,p in SIDE.items():
    J.append((g+'_swim','animate_image_pixminimax',{'first_frame_url':ups[p],'description':'swimming freestyle to the right through water, body horizontal, arms taking big alternating strokes over the head, legs kicking, head turning to breathe, looping swim cycle','frame_count':8,'seed':41,'direction':'east','view':'side','subject_description':SUBJ[g]},g+'_swim'))
st=lambda k: ups[k+'.png']
J+= [
 ('mountain_a','create_image_pro',{'description':'side view of a tall dark rocky mountain cliff face at night under a big full moon, starry deep blue and purple sky, distant misty peaks, JRPG pixel art background, no people','width':360,'height':640,'no_background':False,'style_image_url':st('moon_style')},'mountain_a'),
 ('mountain_b','create_image_pro',{'description':'a towering fantasy mountain peak at twilight, rocky cliffs and pine trees, glowing full moon, stars, purple and teal sky, JRPG pixel art background, no people','width':360,'height':640,'no_background':False,'style_image_url':st('moon_style'),'seed':7},'mountain_b'),
 ('ledge','create_image_pro',{'description':'a long flat mossy stone brick ledge platform, side view, flat walkable top with grass tufts, rough rock underside','width':160,'height':40},'ledge'),
 ('lake_a','create_image_pro',{'description':'a calm clear blue forest lake seen from directly above, sandy shore with grass and flowers along the left and right edges, a few lily pads and reeds, sparkling water, JRPG pixel art, no people','width':360,'height':640,'no_background':False,'style_image_url':st('forest_style')},'lake_a'),
 ('lake_b','create_image_pro',{'description':'top down view of a bright turquoise river flowing upward through a lush fantasy forest, mossy rocks and lily pads at the banks, JRPG pixel art, no people','width':360,'height':640,'no_background':False,'style_image_url':st('forest_style'),'seed':9},'lake_b'),
 ('lilypad','create_image_pro',{'description':'a single green lily pad with a small pink flower floating on water, seen from directly above','width':32,'height':32},'lilypad'),
 ('buoy','create_image_pro',{'description':'a small round red and white lane rope float buoy seen from directly above','width':16,'height':16},'buoy'),
 ('banner','create_image_pro',{'description':'a wooden finish line arch with a checkered banner and colorful pennant flags, front view','width':128,'height':64},'banner'),
 ('dummy','create_image_pro',{'description':'a wooden straw training dummy on a post with a round target painted on its chest, side view, JRPG prop','width':64,'height':64},'dummy'),
 ('swamp','create_image_pro',{'description':'a wide murky green swamp bog pit with bubbles, reeds and lily pads, side view, ground level','width':160,'height':48},'swamp'),
 ('stair','create_image_pro',{'description':'a single grey stone brick stair step block, side view, clean pixel art tile','width':32,'height':32},'stair'),
 ('signpost','create_image_pro',{'description':'a wooden signpost with two arrow signs pointing in different directions, side view','width':48,'height':48},'signpost'),
]
print(jobs.run_many(J,8))
