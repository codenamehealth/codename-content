import sys; sys.path.insert(0,'../pixellab')
import jobs
S='../syeda_src/'
FRONT={'joy':S+'char1/char11.png','ray':S+'char2/char4.png','cleo':S+'char3/char6.png','cyrus':S+'char4/char9.png','hollow':S+'hollow/char1.png'}
SUBJ={'joy':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff',
 'ray':'a young wizard with dark skin in a purple wizard hat and purple robe holding a golden staff',
 'cleo':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail',
 'cyrus':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit',
 'hollow':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'}
ups=jobs.upload(list(FRONT.values())+['dragon_canvas.png','../fork_a2/gen/chest/01.png','found_style.png'])
def mm(name,g,desc,seed):
    return (name,'animate_image_pixminimax',{'first_frame_url':ups[FRONT[g]],'description':desc,'frame_count':8,'seed':seed,'direction':'south','view':'side','subject_description':SUBJ[g]},name)
J=[mm('joy_talk','joy','talking excitedly and fast, waving both hands while gesturing, mouth opening and closing',31),
   mm('hollow_nod','hollow','standing still listening politely, slowly nodding the head up and down',32),
   mm('cyrus_lift','cyrus','doing bicep curls, lifting a heavy dumbbell up and down with one arm, flexing',33),
   mm('joy_stretch','joy','waking up, stretching both arms high above the head with a big happy yawn',34),
   mm('cleo_read','cleo','holding an open paper scroll with both hands and reading it carefully, nodding',35),
   mm('cyrus_shrug','cyrus','shrugging with a carefree grin, palms up, bouncing on his feet',36),
   ('dragon_fire','animate_image_pixminimax',{'first_frame_url':ups['dragon_canvas.png'],'description':'the red dragon rears its head and breathes a big stream of orange fire forward to the left, then closes its mouth','frame_count':8,'seed':37,'view':'side','direction':'west','subject_description':'a friendly red dragon sitting on a pile of gold coins'},'dragon_fire'),
   ('chest_open','animate_image_pixminimax',{'first_frame_url':ups['../fork_a2/gen/chest/01.png'],'description':'the treasure chest lid swings open and bright golden light shines out','frame_count':8,'seed':38},'chest_open'),
   ('chest_closed','create_image_pro',{'description':'a closed wooden treasure chest with iron bands and a gold lock, JRPG treasure, front view','width':48,'height':48},'chest_closed'),
   ('stick','create_image_pro',{'description':'a plain crooked wooden stick, JRPG inventory item icon','width':32,'height':32},'stick'),
   ('shield','create_image_pro',{'description':'a round blue knight shield with a gold rim and a gold cross, JRPG inventory item icon','width':32,'height':32},'shield'),
   ('spinner','create_image_pro',{'description':'a wooden windmill cross made of four flat plank blades joined at a round iron hub, seen straight from the front, JRPG game prop','width':64,'height':64},'spinner'),
   ('orchard1','create_image_pro',{'description':'a sunny apple orchard clearing in a forest, apple trees full of red apples, a wooden cider press and baskets of apples, a dirt path, warm soft light, detailed JRPG pixel art background scene','width':360,'height':640,'no_background':False,'style_image_url':ups['found_style.png']},'orchard1'),
   ('orchard2','create_image_pro',{'description':'a peaceful apple orchard with tall apple trees heavy with red apples, wooden fence, barrels and baskets of apples, flowers on the grass, golden afternoon light, detailed JRPG pixel art background scene','width':360,'height':640,'no_background':False,'style_image_url':ups['found_style.png']},'orchard2')]
print(jobs.run_many(J,7))
