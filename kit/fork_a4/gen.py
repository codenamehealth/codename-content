import sys; sys.path.insert(0,'../pixellab')
import jobs
S='../syeda_src/'
ups=jobs.upload([S+'hollow/char2.png','cleo_side_w.png',S+'hollow/char1.png'])
H='a small shadow creature, a dark purple silhouette of a child with glowing white eyes'
C='a young knight girl in silver plate armour with a blue shield and a short sword, black ponytail'
J=[('hollow_bonk','animate_image_pixminimax',{'first_frame_url':ups[S+'hollow/char2.png'],'description':'walks forward to the right, bumps face first into an invisible wall, recoils backward and falls flat on his back','frame_count':12,'seed':41,'direction':'east','view':'side','subject_description':H},'hollow_bonk'),
('cleo_block','animate_image_pixminimax',{'first_frame_url':ups['cleo_side_w.png'],'description':'steps forward and raises her shield up in front of her to block, bracing firmly, then holds the block','frame_count':8,'seed':42,'direction':'west','view':'side','subject_description':C},'cleo_block'),
('hollow_sit','animate_image_pixminimax',{'first_frame_url':ups[S+'hollow/char1.png'],'description':'exhausted, slumps down and sits on the ground with relief, shoulders dropping, then breathes slowly','frame_count':8,'seed':43,'direction':'south','view':'side','subject_description':H},'hollow_sit')]
print(jobs.run_many(J,3))
