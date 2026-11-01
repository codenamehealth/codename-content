import sys; sys.path.insert(0,'../pixellab')
import jobs
p='../pixellab/race/in/ray_side.png'
ups=jobs.upload([p])
J=[('ray_climb2','animate_image_pixminimax',{'first_frame_url':ups[p],'description':'grabs a vertical green vine with both hands and climbs straight up it hand over hand, legs pushing, robe swaying, looping climb cycle','frame_count':8,'seed':57,'direction':'east','view':'side','subject_description':'a young wizard with dark skin in a purple wizard hat and purple robe, staff on his back'},'ray_climb2')]
print(jobs.run_many(J,1))
