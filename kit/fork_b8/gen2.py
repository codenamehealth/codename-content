import sys; sys.path.insert(0,'../pixellab')
import jobs
u=jobs.upload(['bonfire/00.png','lamppost/01.png'])
J=[('fire_anim','animate_image_pixminimax',{'first_frame_url':u['bonfire/00.png'],'last_frame_url':u['bonfire/00.png'],'description':'campfire flames flickering and dancing upward in a seamless loop, logs stay still','frame_count':8,'seed':5,'view':'high top-down','direction':'south','subject_description':'a campfire with logs and orange flames'},'fire_anim')]
print(jobs.run_many(J,2))
