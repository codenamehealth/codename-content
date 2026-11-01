import sys; sys.path.insert(0,'../../pixellab')
import jobs
J=[('gb_base','create_image_pro',{'description':'the base of a classic red gumball machine: shiny red metal body with a silver coin slot, a silver turning crank and a small chute flap, front view, no glass globe on top, JRPG pixel art item','width':128,'height':96},'gb_base'),
('gb_cap','create_image_pro',{'description':'the round red metal lid of a gumball machine with a small silver knob on top, front view, JRPG pixel art','width':96,'height':48},'gb_cap'),
('cup','create_image_pro',{'description':'a small shiny golden trophy bowl with two handles, front view, JRPG item icon','width':48,'height':48},'cup'),
('slot','create_image_pro',{'description':'a fantasy arcade slot machine cabinet seen from the front, purple and gold trim with little gems, three large empty black rectangular reel windows side by side in the middle, a lever with a red ball on the right side, JRPG pixel art','width':160,'height':160},'slot')]
print(jobs.run_many(J,4))
