import sys; sys.path.insert(0,'../pixellab')
import jobs
ups=jobs.upload(['../syeda_src/char4/char9.png'])
J=[('cyrus_dig2','animate_image_pixminimax',{'first_frame_url':ups['../syeda_src/char4/char9.png'],'description':'winds up and punches straight down into the ground with a glowing orange fist, bare hands, no weapon, looping','frame_count':8,'seed':41,'direction':'south','view':'side','subject_description':'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit, bare-handed brawler'},'cyrus_dig2')]
print(jobs.run_many(J,1))
