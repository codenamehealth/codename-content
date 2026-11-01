import sys; sys.path.insert(0,'../pixellab')
import jobs
ups=jobs.upload(['../fork3/tavern3/00.png','../syeda_src/char1/char11.png'])
shop=ups['../fork3/tavern3/00.png']; sty=ups['../syeda_src/char1/char11.png']
J=[('jar','create_image_pro',{'description':'a large empty clear glass candy jar with a wide mouth and a cork lid, side view, see-through glass with white highlights and a thin outline, JRPG shop item','width':128,'height':160,'style_image_url':shop,'style_copy':['outline','shading','detail']},'jar'),
('door','create_image_pro',{'description':'a huge ornate double stone boss door set in a castle wall, closed, iron studs, glowing purple runes around the arch, front view, JRPG dungeon','width':128,'height':160},'door'),
('altar','create_image_pro',{'description':'a golden sun temple altar table with a white marble base and sun engravings, front view, JRPG temple prop','width':112,'height':72},'altar'),
('banner','create_image_pro',{'description':'a hanging orange cloth banner with a golden sun emblem and gold tassels at the bottom, front view, JRPG temple decoration','width':48,'height':96},'banner'),
('flag','create_image_pro',{'description':'a small wooden flag pole with a plain white cloth flag waving, JRPG map marker','width':32,'height':48,'style_image_url':sty,'style_copy':['outline','shading']},'flag')]
print(jobs.run_many(J,5))
