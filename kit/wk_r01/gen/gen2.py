import sys; sys.path.insert(0,'../../pixellab')
import jobs
P='../../pixellab/race/in/ray_side.png'
ups=jobs.upload([P])
S='a young wizard with dark skin in a big purple pointed wizard hat and purple robe, the hat stays on his head'
D='hangs from an overhead bar with both hands raised straight above his head, his purple wizard hat stays on his head and his face stays visible in profile facing right, feet dangling, swinging hand over hand to the right, looping'
J=[('ray_hang2','animate_image_pixminimax',{'first_frame_url':ups[P],'description':D,'frame_count':8,'seed':s,'direction':'east','view':'side','subject_description':S},'ray_hang%d'%s) for s in (61,62)]
print(jobs.run_many(J,2))
