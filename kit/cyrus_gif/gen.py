import sys; sys.path.insert(0,'../pixellab')
import jobs
S='../syeda_src/char4/'
SIDE=S+'char10.png'; FRONT=S+'char9.png'
subj='a young adventurer boy with spiky brown hair, a gold circlet and an orange and gold outfit with gold shoulder armour'
u=jobs.upload([SIDE,FRONT])
J=[]
for s in (31,32,33):
    J.append((f'run{s}','animate_image_pixminimax',{'first_frame_url':u[SIDE],'description':'sprinting fast to the right in a looping run cycle, leaning forward, legs alternating quickly with long strides, arms pumping hard','frame_count':8,'seed':s,'direction':'east','view':'side','subject_description':subj},f'run{s}'))
for s in (41,42,43):
    J.append((f'stop{s}','animate_image_pixminimax',{'first_frame_url':u[SIDE],'last_frame_url':u[FRONT],'description':'running to the right then skids to a sudden hard stop, leaning back with heels digging in, then quickly turns his body to face the camera','frame_count':8,'seed':s,'direction':'east','view':'side','subject_description':subj},f'stop{s}'))
for s in (51,52,53):
    J.append((f'breath{s}','animate_image_pixminimax',{'first_frame_url':u[FRONT],'last_frame_url':u[FRONT],'description':'out of breath after a long sprint: bends forward with both hands on his knees, panting heavily with shoulders rising and falling, wipes his brow, then straightens back up','frame_count':12,'seed':s,'direction':'south','view':'side','subject_description':subj},f'breath{s}'))
jobs.run_many(J,workers=9)
