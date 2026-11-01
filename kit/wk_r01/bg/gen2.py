import sys; sys.path.insert(0,'../../pixellab')
import jobs
ST=', cozy fantasy JRPG pixel art, side view profile, flat horizontal top surface, transparent background, single color dark outline, medium shading, no face, no eyes'
J=[
 ('stone2','create_image_pixen',{'description':'a short flat rectangular grey stone stepping block seen straight from the side like a platformer tile, thin green moss on the flat top edge, chunky stone texture'+ST,'width':48,'height':32,'no_background':True,'view':'side','seed':212},'stone2'),
 ('log2','create_image_pixen',{'description':'a short floating log raft of three tied logs seen straight from the side like a platformer tile, moss and a few leaves on the flat top'+ST,'width':48,'height':32,'no_background':True,'view':'side','seed':213},'log2'),
 ('rock2','create_image_pixen',{'description':'a plain round grey river boulder with a little moss on top seen from the side, simple rock'+ST,'width':32,'height':32,'no_background':True,'view':'side','seed':214},'rock2'),
 ('arch2','create_image_pixen',{'description':'a simple wooden finish line arch: two straight log posts and one top beam with a black and white checkered banner hanging from the beam and a small red flag on each post, plain, nothing else, isolated object on empty background, seen from the front'+ST,'width':128,'height':128,'no_background':True,'view':'side','seed':215},'arch2'),
]
print(jobs.run_many(J,4))
