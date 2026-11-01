import sys
from PIL import Image
d=sys.argv[1]; nums=[int(x) for x in sys.argv[2].split(',')]; out=sys.argv[3]
ims=[Image.open(f'{d}/frames/f_{n:03d}.png').convert('RGB') for n in nums]
w,h=ims[0].size; s=1.5
W,H=int(w*s),int(h*s)
o=Image.new('RGB',(W*len(ims),H))
for i,im in enumerate(ims): o.paste(im.resize((W,H),Image.NEAREST),(i*W,0))
o.save(out,quality=90)
