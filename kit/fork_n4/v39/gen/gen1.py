import sys,os; sys.path.insert(0,'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import jobs
P='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
U=jobs.upload([P+'fork_b11/ref/style_forest.png'])
d=('a big friendly-looking swamp monster made of dark green mossy swamp sludge with lily pads and reeds on its head, two round glowing yellow eyes, '
   'no teeth, long dripping arms raised, only its upper body visible rising out of murky green water, front view, JRPG monster sprite')
J=[('monster','create_image_pro',{'description':d,'width':128,'height':128,'style_image_url':U[P+'fork_b11/ref/style_forest.png'],'style_copy':['outline','shading']},'monster')]
print(jobs.run_many(J,1))
