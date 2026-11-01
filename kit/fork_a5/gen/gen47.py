import sys; sys.path.insert(0, '../../pixellab')
import jobs
P = '../../pixellab/race/in/'
ups = jobs.upload([P + 'cyrus_side.png', P + 'cleo_side.png'])
cy, cl = ups[P + 'cyrus_side.png'], ups[P + 'cleo_side.png']
SC = 'a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit'
SL = 'a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail'
J = [('cyrus_sleep', 'animate_image_pixminimax', {'first_frame_url': cy, 'description': 'stops, yawns with a big stretch, then lies down flat on his back on the ground and falls asleep', 'frame_count': 12, 'seed': 31, 'direction': 'east', 'view': 'side', 'subject_description': SC}, 'cyrus_sleep'),
     ('cleo_walk', 'animate_image_pixminimax', {'first_frame_url': cl, 'description': 'walking steadily to the right in a calm determined looping walk cycle, legs alternating', 'frame_count': 8, 'seed': 32, 'direction': 'east', 'view': 'side', 'subject_description': SL}, 'cleo_walk'),
     ('cleo_win', 'animate_image_pixminimax', {'first_frame_url': cl, 'description': 'raises her sword high above her head in victory and holds the pose proudly', 'frame_count': 8, 'seed': 33, 'direction': 'east', 'view': 'side', 'subject_description': SL}, 'cleo_win'),
     ('flag', 'create_image_pro', {'description': 'a tall wooden finish flag pole with a waving golden checkered banner, side view, JRPG prop', 'width': 64, 'height': 64}, 'flag')]
print(jobs.run_many(J, 4))
