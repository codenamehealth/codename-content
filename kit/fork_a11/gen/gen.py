import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab')
import jobs
S='side view, cozy JRPG village pixel art, warm 16-bit style'
J=[('dock','create_image_pro',{'description':'a long wooden fishing pier deck made of planks with posts going down into water, seen from the side, '+S,'width':160,'height':48},'dock'),
('mjar','create_image_pro',{'description':'a round glass jar with a cork lid filled with shiny golden gummy candies, JRPG treasure item','width':48,'height':48},'mjar'),
('fish','create_image_pro',{'description':'a small cute round orange fish swimming, side view, JRPG pixel creature','width':32,'height':32},'fish'),
('kelp','create_image_pro',{'description':'a tall wavy strand of green seaweed kelp growing from sand, side view','width':40,'height':80},'kelp'),
('pedestal','create_image_pro',{'description':'an ornate grey stone display pedestal with a blue cloth top, side view, castle treasure stand','width':64,'height':64},'pedestal'),
('hook','create_image_pro',{'description':'a small iron crane hook hanging on chain links, side view, JRPG prop','width':32,'height':48},'hook'),
('snow','create_image_pro',{'description':'a single tiny white snowflake','width':16,'height':16},'snow'),
('petal','create_image_pro',{'description':'a single tiny pink cherry blossom petal','width':16,'height':16},'petal'),
('leaf','create_image_pro',{'description':'a single tiny orange autumn maple leaf','width':16,'height':16},'leaf'),
('rock','create_image_pro',{'description':'a small mossy round lakebed rock with pebbles, side view','width':48,'height':32},'rock')]
print(jobs.run_many(J,6))
