import sys,glob
from PIL import Image, ImageDraw
out,cols,t0,dt=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]); files=sorted(sys.argv[5:])
ims=[Image.open(f) for f in files]; w,h=ims[0].size
rows=(len(ims)+cols-1)//cols
G=Image.new('RGB',(cols*w,rows*(h+18)),'black'); d=ImageDraw.Draw(G)
for i,im in enumerate(ims):
    x,y=(i%cols)*w,(i//cols)*(h+18); G.paste(im,(x,y+18)); d.text((x+3,y+3),f"t={t0+i*dt:.2f}",fill='yellow')
G.save(out,quality=88)
