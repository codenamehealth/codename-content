import sys,glob
from PIL import Image,ImageDraw
rows=sys.argv[2:]; out=sys.argv[1]; sc=2
ims=[[Image.open(f).convert('RGBA') for f in sorted(glob.glob(d+'/*.png'))] for d in rows]
cw=max(i.width for r in ims for i in r)*sc; ch=max(i.height for r in ims for i in r)*sc
mx=max(len(r) for r in ims)
S=Image.new('RGB',(mx*cw+200,len(rows)*ch),(70,80,110));D=ImageDraw.Draw(S)
for y,(d,r) in enumerate(zip(rows,ims)):
    D.text((2,y*ch+4),d.split('/')[-2][-8:]+'/'+d.split('/')[-1],fill='white')
    for x,im in enumerate(r):
        S.alpha_composite if False else None
        S.paste(im.resize((im.width*sc,im.height*sc),Image.NEAREST),(200+x*cw,y*ch),im.resize((im.width*sc,im.height*sc),Image.NEAREST))
S.save(out)
