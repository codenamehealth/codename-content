import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=7.2; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
FORT=['Rare drop','Respawn','Pay raise','Lag spike','Glow up','Phone gone','Main character','Lost save file','Lucky','Final boss','Level up','8 hrs of sleep','Cursed','Found money']
g=Image.open(A+'recov_hd.gif'); g.seek(0); g=g.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(10))).enhance(0.45).convert('RGBA')
vg=Image.new('L',(W,H),0); ImageDraw.Draw(vg).ellipse([-200,300,W+200,H+300],fill=255); vg=vg.filter(ImageFilter.GaussianBlur(160))
dark=Image.new('RGBA',(W,H),(8,4,20,255)); dark.putalpha(Image.eval(vg,lambda v:int((255-v)*0.85))); BG.alpha_composite(dark)
# table with dark purple cloth
TT=1240
tb=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(tb); d.rectangle([0,TT,W,H],fill=(52,18,60,255)); d.rectangle([0,TT,W,TT+14],fill=(25,10,35,255))
for x in range(0,W,60): d.rectangle([x,TT+14,x+30,TT+22],fill=(201,162,74,255))
glowt=Image.new('L',(W,H),0); ImageDraw.Draw(glowt).ellipse([140,TT-40,940,TT+420],fill=150); glowt=glowt.filter(ImageFilter.GaussianBlur(90))
gt=Image.new('RGBA',(W,H),(170,110,240,0)); gt.putalpha(glowt)
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr], im.info.get('duration',120)
RAY,dR=gif('idle_6.gif',860)
# pixel crystal ball, drawn at 1/8 res
P=8; R=34
def orb(text):
    o=Image.new('RGBA',(2*R+6,2*R+14),(0,0,0,0)); d=ImageDraw.Draw(o)
    d.ellipse([3,3,3+2*R,3+2*R],fill=(20,12,36,255))
    d.ellipse([5,5,1+2*R,1+2*R],fill=(232,222,250,255))
    d.ellipse([9,9,2*R-3,2*R-3],fill=(246,240,255,255))
    d.ellipse([16,12,30,22],fill=(255,255,255,255))
    d.rectangle([R-26,2*R+2,R+32,2*R+12],fill=(201,162,74,255)); d.rectangle([R-26,2*R+2,R+32,2*R+3],fill=(120,85,40,255))
    big=o.resize((o.width*P,o.height*P),Image.NEAREST)
    dd=ImageDraw.Draw(big); words=text.split(' ')
    f=F(44 if len(text)<=9 else 36)
    lines=[text] if dd.textlength(text,font=f)<430 else [' '.join(words[:len(words)//2+len(words)%2]),' '.join(words[len(words)//2+len(words)%2:])]
    cy=(3+R)*P-len(lines)*30
    for i,ln in enumerate(lines):
        w=dd.textlength(ln,font=f); dd.text(((big.width-w)/2,cy+i*60),ln,font=f,fill=(48,20,70))
    return big
ORBS=[orb(t) for t in FORT]
og=Image.new('L',(ORBS[0].width+200,ORBS[0].height+200),0); ImageDraw.Draw(og).ellipse([60,60,og.width-60,og.width-60],fill=200); og=og.filter(ImageFilter.GaussianBlur(45))
OG=Image.new('RGBA',og.size,(190,140,255,0)); OG.putalpha(og)
TXT=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(TXT)
for y,t,f,c in ((150,'Rayleigh knows all...',F(40),(210,190,240)),(235,'PAUSE TO SEE',F(58),(255,255,255)),(320,'YOUR FATE',F(58),(255,255,255))):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c,stroke_width=5,stroke_fill=(15,8,30))
rng=random.Random(2); seq=[]; last=-1
while len(seq)<N:
    k=rng.randrange(len(FORT))
    if k!=last: seq+= [k]*rng.choice([2,3]); last=k
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BG.copy()
    sp=RAY[int(t*1000/dR)%len(RAY)]
    img.alpha_composite(sp,(W//2-sp.width//2,450))
    img.alpha_composite(tb); img.alpha_composite(gt)
    ob=ORBS[seq[f]]; pulse=int(6*math.sin(t*5))
    img.alpha_composite(OG,(W//2-OG.width//2,TT-ob.height+200-100+pulse//2))
    img.alpha_composite(ob,(W//2-ob.width//2,TT-ob.height+200))
    img.alpha_composite(TXT)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f==30: img.convert('RGB').save('still.png')
ff.stdin.close(); ff.wait(); print('done')
