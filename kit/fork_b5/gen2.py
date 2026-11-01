import sys; sys.path.insert(0,'../pixellab')
import jobs
ups=jobs.upload(['hollow_side128.png'])
J=[('hollow_punch','animate_image_pixminimax',{'first_frame_url':ups['hollow_side128.png'],'description':'winds up and throws a powerful flaming punch forward to the right with a burst of orange fire around the fist, then returns to a ready stance','frame_count':12,'seed':41,'direction':'east','view':'side','subject_description':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'},'hollow_punch'),
   ('hollow_punch2','animate_image_pixminimax',{'first_frame_url':ups['hollow_side128.png'],'description':'leaps forward and throws a big fiery punch to the right, golden fire trailing the fist, then lands back in stance','frame_count':12,'seed':42,'direction':'east','view':'side','subject_description':'a small shadow creature, a dark purple silhouette of a child with glowing white eyes'},'hollow_punch2')]
print(jobs.run_many(J,2))
