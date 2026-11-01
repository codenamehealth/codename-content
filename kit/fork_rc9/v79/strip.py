import sys; SP0='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0+'fork_a7'); from common7 import *
ds=['fork_b5/hollow_nod','fork3/hollow_eat','pixellab/maze/anim/hollow_panic','fork_a3/hollow_chomp','pixellab/maze/anim/hollow_frun','fork_a4/hollow_sit']
rows=[[up(Image.open(p).convert('RGBA'),1) for p in sorted(glob.glob(SP0+d+'/*.png'))] for d in ds]
c=Image.new('RGBA',(13*100,6*100),(60,80,60,255))
for r,fr in enumerate(rows):
    for i,f in enumerate(fr): c.alpha_composite(f.resize((92,92)),(i*100,r*100))
c.convert('RGB').resize((1300*2//2*1,600)).save('strip.png')
print([f.size for f in rows[0][:1]])
