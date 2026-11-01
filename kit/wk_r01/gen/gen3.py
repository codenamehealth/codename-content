import sys; sys.path.insert(0,'../../pixellab')
import jobs
S='../../syeda_src/'; P='../../pixellab/race/in/'
F={'cyf':S+'char4/char9.png','cys':P+'cyrus_side.png','cls':P+'cleo_side.png','ras':P+'ray_side.png'}
ups=jobs.upload(list(F.values()))
CY='a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit'
J=[('cyrus_panic_f','animate_image_pixminimax',{'first_frame_url':ups[F['cyf']],'description':'panicking: grabs his head with both hands, eyes wide in shock, mouth closed in a small worried line, knees wobbling, shaking in place, looping','frame_count':8,'seed':71,'direction':'south','view':'side','subject_description':CY},'cyrus_panic_f'),
 ('cyrus_panic_s','animate_image_pixminimax',{'first_frame_url':ups[F['cys']],'description':'panicking: flails both arms wildly above his head and clutches his head, eyes wide in shock, mouth closed, stumbling in place, looping','frame_count':8,'seed':72,'direction':'east','view':'side','subject_description':CY},'cyrus_panic_s'),
 ('cleo_slip','animate_image_pixminimax',{'first_frame_url':ups[F['cls']],'description':'hangs from an overhead bar with both hands raised above her head, then one hand slips off and she dangles by one hand, legs kicking and free arm flailing, facing right','frame_count':8,'seed':73,'direction':'east','view':'side','subject_description':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail'},'cleo_slip'),
 ('ray_reach','animate_image_pixminimax',{'first_frame_url':ups[F['ras']],'description':'kneels down at the edge and reaches down low in front of him with one hand, grabs a hand below and pulls it up while standing back up, facing right','frame_count':8,'seed':74,'direction':'east','view':'side','subject_description':'a young wizard with dark skin in a big purple pointed wizard hat and purple robe holding a golden staff'},'ray_reach')]
print(jobs.run_many(J,4))
