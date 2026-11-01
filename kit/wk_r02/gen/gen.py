import sys; sys.path.insert(0,'../../pixellab')
import jobs
P='../../pixellab/race/in/'
SIDE={g:P+g+'_side.png' for g in ['joy','ray','cleo','cyrus']}
SUBJ={'joy':'a young ranger girl with brown hair, a green hood and cape and a wooden flower staff, mouth closed',
 'ray':'a young wizard with dark skin in a big purple pointed wizard hat and purple robe holding a golden staff',
 'cleo':'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail',
 'cyrus':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit'}
ups=jobs.upload(list(SIDE.values()))
J=[]
for g in SIDE:
    J.append((g+'_climb','animate_image_pixminimax',{'first_frame_url':ups[SIDE[g]],'description':'climbs straight up a tall flat wall directly in front of them, seen from the side facing right, hands reaching up and gripping holds hand over hand, knees and boots pushing against the wall, body pressed close to the wall, looping climb cycle','frame_count':8,'seed':91,'direction':'east','view':'side','subject_description':SUBJ[g]},g+'_climb'))
    J.append((g+'_crawl','animate_image_pixminimax',{'first_frame_url':ups[SIDE[g]],'description':'drops flat onto the belly and army-crawls forward to the right along the ground, body low and horizontal, elbows and knees pulling alternately, head low, looping crawl cycle','frame_count':8,'seed':92,'direction':'east','view':'side','subject_description':SUBJ[g]},g+'_crawl'))
J.append(('ray_nap','animate_image_pixminimax',{'first_frame_url':ups[SIDE['ray']],'description':'trips and belly-flops forward onto the ground face down to the right, then lies flat on his belly fast asleep with eyes closed, hat tipped over, breathing slowly, lying still','frame_count':12,'seed':93,'direction':'east','view':'side','subject_description':SUBJ['ray']},'ray_nap'))
print(jobs.run_many(J,9))
