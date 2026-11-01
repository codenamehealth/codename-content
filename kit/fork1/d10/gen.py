import sys; sys.path.insert(0,'../../pixellab')
import jobs
ups=jobs.upload(['hollow128.png'])
u=ups['hollow128.png']
subj='a small shadow creature, a dark purple silhouette of a child with glowing white eyes'
J=[('fall','animate_image_pixminimax',{'first_frame_url':u,'description':'wobbles dizzily, loses balance and falls forward flat onto his face on the ground, lying face down at the end','frame_count':12,'seed':31,'direction':'south','view':'side','subject_description':subj},'fall'),
('fall2','animate_image_pixminimax',{'first_frame_url':u,'description':'gets knocked over, tips backwards and falls flat on his back onto the ground, lying still at the end','frame_count':12,'seed':32,'direction':'south','view':'side','subject_description':subj},'fall2'),
('crater','create_image_pro',{'description':'a small round impact crater in sandy dirt ground with cracks radiating out and little rocks, seen from a low top-down angle, JRPG pixel art','width':96,'height':48},'crater')]
print(jobs.run_many(J,3))
