import sys
from PIL import Image
out,cols,sc=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]); files=sys.argv[4:]
ims=[Image.open(f) for f in files]; w,h=ims[0].size; w2,h2=int(w*sc),int(h*sc)
rows=(len(ims)+cols-1)//cols
G=Image.new('RGB',(cols*w2+(cols-1)*6,rows*h2+(rows-1)*6),'white')
for i,im in enumerate(ims): G.paste(im.resize((w2,h2)),((i%cols)*(w2+6),(i//cols)*(h2+6)))
G.save(out,quality=85)
