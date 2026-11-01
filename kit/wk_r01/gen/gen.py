import sys; sys.path.insert(0,'../../pixellab')
import jobs
P='../../pixellab/race/in/'
SIDE={g:P+g+'_side.png' for g in ['joy','ray','cleo','cyrus']}
SUBJ={'joy':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff',
 'ray':'a young wizard with dark skin in a purple wizard hat and purple robe holding a golden staff',
 'cleo':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail',
 'cyrus':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit'}
ups=jobs.upload(list(SIDE.values()))
J=[]
for g in ['joy','ray','cleo']:
    J.append((g+'_jump','animate_image_pixminimax',{'first_frame_url':ups[SIDE[g]],'description':'jumps forward to the right: crouches, springs up into the air with knees tucked, sails forward, then lands on the feet and stands up, facing right the whole time','frame_count':12,'seed':51,'direction':'east','view':'side','subject_description':SUBJ[g]},g+'_jump'))
for g in ['joy','ray','cleo','cyrus']:
    J.append((g+'_hang','animate_image_pixminimax',{'first_frame_url':ups[SIDE[g]],'description':'reaches both arms straight up and hangs from an overhead bar by the hands, feet off the ground, swinging hand over hand to the right along monkey bars, body dangling below the hands, looping','frame_count':8,'seed':52,'direction':'east','view':'side','subject_description':SUBJ[g]},g+'_hang'))
print(jobs.run_many(J,7))
