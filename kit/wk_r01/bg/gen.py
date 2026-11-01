import sys; sys.path.insert(0,'../../pixellab')
import jobs
ST=', cozy fantasy JRPG pixel art, warm earthy palette, side view, clean single color dark outline, medium shading'
J=[
 ('dock','create_image_pixen',{'description':'a long thin floating wooden dock raft made of horizontal planks with rope lashings and small posts at the ends, seen exactly from the side, floating flat'+ST,'width':128,'height':32,'no_background':True,'view':'side','seed':201},'dock'),
 ('stone','create_image_pixen',{'description':'a flat mossy grey stepping stone slab floating on water, seen exactly from the side, green moss on top'+ST,'width':48,'height':32,'no_background':True,'view':'side','seed':202},'stone'),
 ('lily','create_image_pixen',{'description':'a small floating mossy log raft with grass and tiny flowers on top, seen exactly from the side'+ST,'width':48,'height':32,'no_background':True,'view':'side','seed':203},'lily'),
 ('boulder','create_image_pixen',{'description':'a round mossy boulder rock poking out of water, seen from the side, rounded top'+ST,'width':32,'height':32,'no_background':True,'view':'side','seed':204},'boulder'),
 ('post','create_image_pixen',{'description':'a single tall thick wooden tree stump post standing in water with moss on the flat top, seen from the side'+ST,'width':32,'height':64,'no_background':True,'view':'side','seed':205},'post'),
 ('grass','create_image_pixen',{'description':'seamless tileable texture of grassy earth: bright grass on top edge, rich brown dirt with small stones below, side view cross section'+ST,'width':64,'height':64,'no_background':False,'view':'side','seed':206},'grass'),
 ('arch','create_image_pixen',{'description':'a wooden finish line arch gate made of two log posts and a top beam with a hanging black and white checkered banner and small flags, seen from the front'+ST,'width':128,'height':128,'no_background':True,'view':'side','seed':207},'arch'),
]
print(jobs.run_many(J,7))
