import sys; sys.path.insert(0,'../pixellab')
import jobs
S='../syeda_src/'
ups=jobs.upload(['style_forest.png',S+'char1/char11.png',S+'hollow/char1.png',S+'char4/char9.png'])
st=ups['style_forest.png']; JOY=ups[S+'char1/char11.png']; HOL=ups[S+'hollow/char1.png']; CYR=ups[S+'char4/char9.png']
J=[
('shrine1','create_image_pro',{'description':'vertical JRPG background: a peaceful forest clearing at dusk with an ancient mossy stone shrine pedestal in the middle (empty top), glowing fireflies, tall trees framing the sides, soft blue and green light, lush detailed pixel art','width':384,'height':688,'no_background':False,'style_image_url':st,'seed':3},'shrine1'),
('shrine2','create_image_pro',{'description':'vertical JRPG background: an enchanted forest grove at twilight, a round mossy stone altar in the center foreground (empty), mushrooms and ferns, hanging vines, fireflies, cozy detailed pixel art','width':384,'height':688,'no_background':False,'style_image_url':st,'seed':8},'shrine2'),
('crystal','create_image_pro',{'description':'a floating glowing pale blue diamond crystal with facets and a soft inner light, JRPG magic item','width':48,'height':48},'crystal'),
('ring','create_image_pro',{'description':'an ornate round golden picture frame ring with small sun engravings and gems, the center is empty and transparent, JRPG UI frame','width':128,'height':128},'ring'),
('parch','create_image_pro',{'description':'an ornate vertical parchment card frame with golden curled corners and a thin rope border, empty light parchment center, JRPG UI panel','width':112,'height':160},'parch'),
('cups','create_image_pro',{'description':'an upside down ornate golden temple cup with sun engravings, side view, JRPG prop','width':40,'height':40},'cups'),
('joy_cast','animate_image_pixminimax',{'first_frame_url':JOY,'description':'raises her flower staff high and casts a healing spell, green sparkles swirl around her, then she lowers the staff and smiles','frame_count':12,'seed':31,'direction':'south','view':'side','subject_description':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff'},'joy_cast'),
('hollow_chomp','animate_image_pixminimax',{'first_frame_url':HOL,'description':'leans forward and chomps rapidly, biting at the air, head bobbing up and down, hungry','frame_count':8,'seed':32,'direction':'south','view':'side','subject_description':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'},'hollow_chomp'),
('cyrus_hide','animate_image_pixminimax',{'first_frame_url':CYR,'description':'crouches down, places a small item on the ground in front of him, then stands back up and grins','frame_count':8,'seed':33,'direction':'south','view':'side','subject_description':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit'},'cyrus_hide'),
]
print(jobs.run_many(J,9))
