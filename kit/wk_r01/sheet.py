import sys,glob
from PIL import Image, ImageDraw
d,start,n,cols,out,fps=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5],float(sys.argv[6])
fs=sorted(glob.glob(d+'/*.png'))[start:start+n]
im0=Image.open(fs[0]);w,h=im0.size
rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*(h+14)),'white');D=ImageDraw.Draw(S)
for i,f in enumerate(fs):
    x=(i%cols)*w;y=(i//cols)*(h+14)
    S.paste(Image.open(f).convert('RGB'),(x,y+14));D.text((x+2,y),'%.2fs'%((start+i)/fps),fill='black')
S.save(out)
