import sys; sys.path.insert(0,'../../pixellab')
import jobs
F='cleo_hang/04.png'
ups=jobs.upload([F])
J=[('cleo_slip2','animate_image_pixminimax',{'first_frame_url':ups[F],'description':'hanging from a bar by both hands, then one hand slips off the bar and she dangles by only one raised hand, body swinging, legs kicking, free arm waving down, facing right','frame_count':8,'seed':81,'direction':'east','view':'side','subject_description':'a young knight girl in silver plate armour with a blue shield, black ponytail'},'cleo_slip2')]
print(jobs.run_many(J,1))
