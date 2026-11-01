import sys,os; sys.path.insert(0,'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import jobs
U=jobs.upload(['monster/00.png'])
subj='a big green swamp monster made of mossy sludge with lily pads and reeds on its head and glowing yellow eyes, standing waist deep in swamp water'
J=[(f'grab{s}','animate_image_pixminimax',{'first_frame_url':U['monster/00.png'],'description':'swings both raised arms down and forward to grab something in front of it, hugs it close, then sinks straight down into the water until only bubbles are left','frame_count':8,'seed':s,'view':'side','direction':'south','subject_description':subj},f'grab{s}') for s in (61,62)]
print(jobs.run_many(J,2))
