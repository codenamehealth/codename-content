import sys,glob
from PIL import Image, ImageDraw
out=sys.argv[1]; fs=sorted(sys.argv[2:],key=lambda f:float(f[3:-4])); cols=4; w,h=405,420
M=Image.new('RGB',(w*cols,(h+16)*((len(fs)+cols-1)//cols)),'white');D=ImageDraw.Draw(M)
for i,f in enumerate(fs):
    x=(i%cols)*w;y=(i//cols)*(h+16);M.paste(Image.open(f).crop((0,300,1080,1420)).resize((w,h)),(x,y+16));D.text((x+4,y+2),f,fill='black')
M.save(out)
