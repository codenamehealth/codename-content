import sys; sys.path.insert(0,'..')
import jobs
S='../../'
ups=jobs.upload([S+'gummy/mush_gummy_single.png',S+'gummy/acv_gummy_single.png',S+'gummy/mel_gummy_single.png',S+'gummy/cre_gummy_single.png',S+'syeda_src/char1/char11.png'])
u=lambda k: ups[S+k]; style=u('syeda_src/char1/char11.png')
specs=[('mush','gummy/mush_gummy_single.png','a single glossy translucent dark amber-brown gummy candy, rounded dome shape with a flat bottom, bright highlight on top, cute JRPG item icon'),
('acv','gummy/acv_gummy_single.png','a single soft orange-red apple shaped gummy candy with a little stem, cute JRPG item icon'),
('mel','gummy/mel_gummy_single.png','a single orange gumdrop gummy candy, sugar coated dome, cute JRPG item icon'),
('cre','gummy/cre_gummy_single.png','a single pink-red sugar coated round dome gummy candy with sparkly sugar crystals, cute JRPG item icon'),
('gold','gummy/mush_gummy_single.png','a single shiny golden gummy candy, dome shape, glowing gold with sparkle highlights, legendary JRPG item icon')]
J=[(k,'create_image_pro',{'description':d,'width':48,'height':48,'reference_images':[{'url':u(p),'usage':'shape and color of the gummy candy'}],'style_image_url':style,'style_copy':['outline','shading','detail']},k) for k,p,d in specs]
print(jobs.run_many(J,5))
