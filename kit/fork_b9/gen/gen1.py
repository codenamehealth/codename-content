import sys; sys.path.insert(0,'../../pixellab')
import jobs
J=[('slab','create_image_pro',{'description':'a square carved stone floor slab tile seen from directly above, mossy ancient temple stone with a thin carved border, flat and even, JRPG','width':32,'height':32,'no_background':False},'slab'),
('lantern','create_image_pro',{'description':'a spirit lantern orb, a softly glowing round glass bubble with a tiny shadowy creature with two glowing white eyes inside, JRPG item','width':32,'height':32},'orb'),
('arena','create_image_pro',{'description':'top-down view of a round sandy desert arena courtyard floor with sandstone tiles, palm trees and clay pots around the edge, warm sunset light, JRPG town','width':384,'height':384,'no_background':False},'arena')]
print(jobs.run_many(J,3))
