import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
from PIL import Image
K=1.08; X0=100; TOP=450; SX0=300-X0/K; SW=W/K; SH=int(1080*K)
src=Image.open('found0.png').convert('RGBA')
f=src.crop((int(SX0),0,int(SX0)+int(SW),1080)).resize((W,SH),Image.NEAREST)
EH=H-TOP-SH
def ext(shift):
    es=int(EH/K)+1
    r=src.crop((int(SX0)+shift,1080-es,int(SX0)+shift+int(SW),1080)).resize((W,int(es*K)),Image.NEAREST).crop((0,0,W,EH)) if False else None
    x0=int(SX0)+shift; x0=max(0,min(1920-int(SW),x0))
    r=src.crop((x0,1080-es,x0+int(SW),1080)).resize((W,int(round(es*K))),Image.NEAREST)
    r=r.crop((0,r.height-EH,W,r.height)).transpose(Image.FLIP_TOP_BOTTOM)
    mir=f.crop((0,SH-EH,W,SH)).transpose(Image.FLIP_TOP_BOTTOM)
    a=Image.new('L',(1,EH)); [a.putpixel((0,y),int(255*min(1,y/70))) for y in range(EH)]
    o=Image.composite(r,mir,a.resize((W,EH)))
    g=Image.new('L',(1,EH)); [g.putpixel((0,y),int(255*(1-0.45*y/EH))) for y in range(EH)]
    return Image.composite(o,Image.new('RGBA',o.size,(10,20,12,255)),g.resize(o.size))
out=Image.new('RGB',(1080*3//2,(H-1200)//2))
for i,sh in enumerate((300,700,900)):
    im=Image.new('RGBA',(W,H)); im.alpha_composite(f,(0,TOP)); im.alpha_composite(ext(sh),(0,TOP+SH))
    out.paste(im.crop((0,1200,W,H)).convert('RGB').resize((540,(H-1200)//2)),(i*540//1*1,0)) if i<3 else None
out.save('ext_test.jpg')
