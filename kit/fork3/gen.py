import sys; sys.path.insert(0,'../pixellab')
import jobs
S='../syeda_src/'
ups=jobs.upload([S+'hollow/char1.png',S+'char2/char4.png','hub_style.png','moon_style.png'])
H=ups[S+'hollow/char1.png']; R=ups[S+'char2/char4.png']
subjH='a small shadow creature, a dark purple silhouette of a child with glowing white eyes'
subjR='a young wizard with dark skin in a purple wizard hat and purple robe holding a golden staff with a purple orb'
J=[('hollow_eat','animate_image_pixminimax',{'first_frame_url':H,'last_frame_url':H,'description':'lifts a small round gummy candy to its mouth with both hands, chomps it happily, then lowers its hands and bounces with joy','frame_count':12,'seed':31,'direction':'south','view':'side','subject_description':subjH},'hollow_eat'),
('ray_cast','animate_image_pixminimax',{'first_frame_url':R,'last_frame_url':R,'description':'raises the staff and channels magic, the orb on the staff glows and pulses, robe sways, looping spell cast','frame_count':8,'seed':32,'direction':'south','view':'side','subject_description':subjR},'ray_cast'),
('tavern1','create_image_pro',{'description':'cozy fantasy tavern interior at night, warm candle and fireplace light, wooden beams, round wooden tables, barrels, shelves of jars, a small wooden stage in the center foreground, JRPG pixel art background, no people','width':360,'height':640,'no_background':False,'style_image_url':ups['hub_style.png']},'tavern1'),
('tavern2','create_image_pro',{'description':'cozy fantasy tavern interior, warm golden lantern light, wooden floor, hearth fireplace, hanging plants, tables with mugs, empty open floor in the lower middle, JRPG pixel art background, no people','width':360,'height':640,'no_background':False,'style_image_url':ups['hub_style.png']},'tavern2'),
('tavern3','create_image_pro',{'description':'inside a magical candy shop in a fantasy village, shelves of glowing gummy jars, warm lights, wooden counter, empty wooden floor in the lower middle, JRPG pixel art background, no people','width':360,'height':640,'no_background':False,'style_image_url':ups['hub_style.png']},'tavern3')]
print(jobs.run_many(J,5))
