import sys; sys.path.insert(0,'../../pixellab')
import jobs
J=[('wall_amber','create_image_pro',{'description':'a long horizontal glowing amber orange crystal barrier wall lying on the ground, seen from a high top-down angle, JRPG game piece','width':128,'height':40},'wall_amber'),
('wall_violet','create_image_pro',{'description':'a long horizontal glowing violet purple shadow crystal barrier wall lying on the ground, seen from a high top-down angle, JRPG game piece','width':128,'height':40},'wall_violet'),
('floor','create_image_pro',{'description':'a single square warm sandstone floor tile with subtle cracks and worn edges, seen from directly above, JRPG temple floor','width':32,'height':32,'no_background':False},'floor'),
('gold','create_image_pro',{'description':'a pile of shiny gold coins with a few gems, JRPG treasure','width':64,'height':64},'gold'),
('chest','create_image_pro',{'description':'an open wooden treasure chest overflowing with gold coins, JRPG treasure','width':64,'height':64},'chest'),
('items','create_image_pro',{'description':'four JRPG inventory items in a row: a blue spellbook with a glowing crystal, a stack of gold coins, a brass hourglass, a leather adventurer backpack','width':128,'height':32},'items'),
('book','create_image_pro',{'description':'a magic spellbook with a glowing blue crystal on the cover, JRPG inventory item icon','width':48,'height':48},'book'),
('hourglass','create_image_pro',{'description':'an ornate brass hourglass with glowing golden sand, JRPG inventory item icon','width':48,'height':48},'hourglass'),
('backpack','create_image_pro',{'description':'a leather adventurer backpack with a bedroll and a lantern, JRPG inventory item icon','width':48,'height':48},'backpack'),
('coins','create_image_pro',{'description':'a small stack of shiny gold coins, JRPG inventory item icon','width':48,'height':48},'coins'),
('frame','create_image_pro',{'description':'an ornate golden picture frame border with gems at the corners, empty inside, JRPG UI','width':64,'height':64},'frame')]
print(jobs.run_many(J,6))
