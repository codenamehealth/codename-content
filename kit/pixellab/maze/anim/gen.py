import sys; sys.path.insert(0,'../..')
import jobs
S='../../../syeda_src/'
FRONT={'joy':S+'char1/char11.png','ray':S+'char2/char4.png','cleo':S+'char3/char6.png','cyrus':S+'char4/char9.png','hollow':S+'hollow/char1.png'}
SIDE={'joy':'../../race/in/joy_side.png','ray':'../../race/in/ray_side.png','cleo':'../../race/in/cleo_side.png','cyrus':'../../race/in/cyrus_side.png','hollow':S+'hollow/char2.png'}
SUBJ={'joy':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff',
 'ray':'a young wizard with dark skin in a purple wizard hat and purple robe holding a golden staff',
 'cleo':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail',
 'cyrus':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit',
 'hollow':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'}
ups=jobs.upload(list(FRONT.values())+list(SIDE.values()))
J=[]
for g in FRONT:
    J.append((g+'_frun','animate_image_pixminimax',{'first_frame_url':ups[FRONT[g]],'description':'running fast towards the camera in a looping run cycle, legs alternating quickly, arms pumping','frame_count':8,'seed':21,'direction':'south','view':'side','subject_description':SUBJ[g]},g+'_frun'))
    J.append((g+'_panic','animate_image_pixminimax',{'first_frame_url':ups[FRONT[g]],'description':'stuck in place and panicking, waving both arms frantically above the head, bouncing on the spot, shocked face','frame_count':8,'seed':22,'direction':'south','view':'side','subject_description':SUBJ[g]},g+'_panic'))
    J.append((g+'_slide','animate_image_pixminimax',{'first_frame_url':ups[SIDE[g]],'description':'drops into a fast feet-first baseball slide along the ground to the right, leaning back low, then pops back up to standing','frame_count':8,'seed':23,'direction':'east','view':'side','subject_description':SUBJ[g]},g+'_slide'))
J.append(('hollow_srun','animate_image_pixminimax',{'first_frame_url':ups[SIDE['hollow']],'description':'running fast to the right in a looping run cycle, legs alternating quickly, arms pumping','frame_count':8,'seed':24,'direction':'east','view':'side','subject_description':SUBJ['hollow']},'hollow_srun'))
print(jobs.run_many(J,8))
