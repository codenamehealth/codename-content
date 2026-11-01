import sys,glob
from PIL import Image, ImageDraw
out=sys.argv[1]; fs=sorted(sys.argv[2:],key=lambda f:float(f[3:-4])); sc=0.42; cols=4
ims=[Image.open(f).crop((0,380,1080,1560)) for f in fs]; w,h=int(1080*sc),int(1180*sc)
M=Image.new('RGB',(w*cols,(h+18)*((len(fs)+cols-1)//cols)),'white');D=ImageDraw.Draw(M)
for i,(f,im) in enumerate(zip(fs,ims)):
    x=(i%cols)*w;y=(i//cols)*(h+18);M.paste(im.resize((w,h)),(x,y+18));D.text((x+4,y+3),f,fill='black')
M.save(out)
