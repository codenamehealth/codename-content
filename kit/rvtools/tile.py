import sys,os
from PIL import Image, ImageDraw, ImageFont
# usage: tile.py dir t0 t1 x0 y0 x1 y1 scale cols out [fps]
d,t0,t1,x0,y0,x1,y1,sc,cols,out=sys.argv[1:11]; fps=float(sys.argv[11]) if len(sys.argv)>11 else 10
t0,t1,sc=float(t0),float(t1),float(sc); x0,y0,x1,y1,cols=map(int,(x0,y0,x1,y1,cols))
pat=sys.argv[12] if len(sys.argv)>12 else 'f_%04d.jpg'
idx=[i for i in range(int(round(t0*fps))+1,int(round(t1*fps))+2,int(os.environ.get("STEP","1"))) if os.path.exists(os.path.join(d,pat%i))]
W=int((x1-x0)*sc);H=int((y1-y0)*sc);rows=(len(idx)+cols-1)//cols
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
sh=Image.new('RGB',(cols*W,rows*(H+24)),(20,20,20));dr=ImageDraw.Draw(sh)
for k,i in enumerate(idx):
    im=Image.open(os.path.join(d,pat%i)).crop((x0,y0,x1,y1)).resize((W,H),Image.NEAREST)
    x=(k%cols)*W;y=(k//cols)*(H+24);sh.paste(im,(x,y+24));dr.text((x+4,y+2),f'{(i-1)/fps:.2f}s',fill=(255,230,0),font=font)
sh.save(out,quality=88);print(out,len(idx),sh.size)
