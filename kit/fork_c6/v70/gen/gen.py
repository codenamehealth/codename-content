import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab')
import os; os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab')
import jobs
OUT = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c6/v70/gen/'
J = [('cartfront', 'create_image_pro', {'description': 'an empty wooden mine cart seen straight from the front, facing the viewer, symmetrical, open top so you can see a little of the dark inside, iron bands and rivets, two iron wheels at the bottom left and right corners, JRPG pixel art prop, no background', 'width': 64, 'height': 64}, OUT + 'cartfront')]
print(jobs.run_many(J, 1))
