import glob, os, sys
from PIL import Image, ImageDraw, ImageFont
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
dirs = sys.argv[2:]
cells=[]
for d in dirs:
    fs=sorted(glob.glob(S+d+'/*.png'))
    if not fs: continue
    picks=[fs[0], fs[len(fs)//3], fs[2*len(fs)//3], fs[-1]]
    ims=[Image.open(p).convert('RGBA') for p in picks]
    cells.append((d+f' n={len(fs)} {ims[0].size}', ims))
cw=4*130; ch=150
out=Image.new('RGB',(cw*2, ch*((len(cells)+1)//2)),(70,90,70))
dr=ImageDraw.Draw(out)
for i,(name,ims) in enumerate(cells):
    x0=(i%2)*cw; y0=(i//2)*ch
    for j,im in enumerate(ims):
        bb=im.getbbox() or (0,0,1,1); im=im.crop(bb); k=min(125/im.width,125/im.height)
        im=im.resize((max(1,int(im.width*k)),max(1,int(im.height*k))),Image.NEAREST)
        out.paste(im,(x0+j*130,y0+18),im)
    dr.text((x0+2,y0+2),name,fill=(255,255,0))
out.save(sys.argv[1])
