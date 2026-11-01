import numpy as np, subprocess, math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
CHAR=sys.argv[1] if len(sys.argv)>1 else 'joy'
SPR={'joy':'idle_5.gif','hollow':'idle_9.gif'}[CHAR]
W,H,FPS=1080,1920,30; DUR=7.8; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
# village background, crisp nearest upscale
hg=Image.open(A+'hub.gif'); BGS=[]; S=H/1080; cw=int(W/S)
for i in range(hg.n_frames):
    hg.seek(i); g=hg.convert('RGB').crop((960-cw//2,0,960-cw//2+cw,1080)).resize((W+80,H+80),Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(g).enhance(0.8).convert('RGBA'))
im=Image.open(A+SPR); FR=[]
for i in range(im.n_frames): im.seek(i); FR.append(im.convert('RGBA'))
bb=None
for f in FR:
    b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
SH=520; FR=[f.crop(bb) for f in FR]; FR=[f.resize((int(f.width*SH/f.height),SH),Image.NEAREST) for f in FR]
CX,CY=540,1500   # character center
# slam keyframes (t, x, y, angle): bounces off every edge, then craters in the middle
KF=[(4.10,540,1500,0),(4.19,-30,1050,85),(4.28,560,1990,175),(4.37,1110,760,-95),(4.46,520,-70,190),
    (4.55,60,420,40),(4.64,1010,1520,-70),(4.72,300,1700,120),(4.82,540,1510,0)]
HITS=[k[0] for k in KF[1:-1]]; IMPACT=KF[-1][0]
def slam(t):
    for a,b in zip(KF,KF[1:]):
        if a[0]<=t<b[0]:
            u=(t-a[0])/(b[0]-a[0]); return [a[i]+(b[i]-a[i])*u for i in (1,2,3)]
    return [KF[-1][1],KF[-1][2],0]
rng=random.Random(7)
# crater art drawn at 1/6 scale then nearest-upscaled so it matches the pixel sprites
P=6
def crater():
    w,h=120,60; c=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(c)
    cx,cy=w//2,h//2
    for k in range(16):
        a=2*math.pi*k/16+rng.uniform(-.15,.15); r1=rng.uniform(1.0,1.5)
        x0,y0=cx+math.cos(a)*44,cy+math.sin(a)*19; x1,y1=cx+math.cos(a)*58*r1,cy+math.sin(a)*28*r1
        d.line([(x0,y0),(x1,y1)],fill=(45,28,20,255),width=1)
    d.ellipse([cx-46,cy-21,cx+46,cy+21],fill=(60,38,26,255))
    d.ellipse([cx-43,cy-19,cx+43,cy+19],fill=(150,110,80,255))
    d.ellipse([cx-40,cy-16,cx+40,cy+17],fill=(105,70,48,255))
    d.ellipse([cx-34,cy-11,cx+34,cy+14],fill=(78,50,34,255))
    d.arc([cx-43,cy-19,cx+43,cy+19],200,340,fill=(210,170,125,255))
    return c.resize((w*P,h*P),Image.NEAREST)
CRATER=crater()
def star(col=(255,220,60)):
    c=Image.new('RGBA',(7,7),(0,0,0,0)); d=ImageDraw.Draw(c)
    for (x,y) in [(3,0),(3,1),(0,3),(1,3),(2,2),(3,2),(4,2),(2,3),(3,3),(4,3),(5,3),(6,3),(2,4),(3,4),(4,4),(1,5),(5,5),(1,6),(5,6),(3,5)]:
        d.point((x,y),fill=col+(255,))
    return c.resize((7*P,7*P),Image.NEAREST)
STAR=star()
puffs=[]
def ctext(img,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',f'video_{CHAR}.mp4'],stdin=subprocess.PIPE)
debris=[(rng.uniform(-1,1)*900,-rng.uniform(500,1300),rng.randint(2,4)) for _ in range(22)]
for f in range(N):
    t=f/FPS
    # camera shake: small on each wall hit, big on impact
    sh=0
    for h in HITS:
        if 0<=t-h<0.1: sh=max(sh,22*(1-(t-h)/0.1))
    if 0<=t-IMPACT<0.45: sh=max(sh,48*(1-(t-IMPACT)/0.45))
    if 3.4<=t<4.1: sh=max(sh,6)
    ox,oy=int(40+rng.uniform(-sh,sh)),int(40+rng.uniform(-sh,sh))
    img=BGS[int(t*10)%len(BGS)].crop((ox,oy,ox+W,oy+H))
    fr=FR[int(t*8)%len(FR)]
    if t<4.1:
        amp=1.5+2.2*t if t<3.4 else 9
        ang=amp*math.sin(2*math.pi*(6 if t<3.4 else 11)*t)
        jx=rng.uniform(-1,1)*(0 if t<3.4 else 10)
        sp=fr.rotate(ang,resample=Image.NEAREST,expand=True)
        img.alpha_composite(sp,(int(CX+jx-sp.width/2),int(CY-sp.height/2)))
        ctext(img,300,'SHAKE YOUR PHONE',F(60)); ctext(img,400,'FOR A SURPRISE',F(60)); ctext(img,500,'IN...',F(60))
        k=int(t/0.85)
        lab=['4','3','2','1'][k] if k<4 else 'NOW!'
        sc=1+0.25*max(0,1-((t-0.85*min(k,4))/0.18))
        ctext(img,640,lab,F(int(130*sc)),(255,70,60),9)
    elif t<IMPACT:
        x,y,a=slam(t)
        sp=FR[0].rotate(a,resample=Image.NEAREST,expand=True)
        img.alpha_composite(sp,(int(x-sp.width/2),int(y-sp.height/2)))
    else:
        dt=t-IMPACT
        # smoke behind the crater and the squashed guide
        if f%3==0: puffs.append([t,rng.uniform(-70,70),rng.uniform(0.7,1.35),rng.uniform(0,6.28),rng.uniform(120,230)])
        lay=Image.new('RGBA',(W//P,H//P),(0,0,0,0)); d=ImageDraw.Draw(lay)
        live=[]
        for t0,jit,rk,ph,vx in puffs:
            age=t-t0
            if age>2.8: continue
            r=rk*(45+85*age)/P*(1 if age<2.2 else max(0,1-(age-2.2)/0.6)); x=(CX+jit+vx*age+40*math.sin(ph+3*age))/P; y=(CY+40-(520+60*rk)*age)/P
            live.append((x,y,r))
        for x,y,r in live: d.ellipse([x-r-1.5,y-r-1.5,x+r+1.5,y+r+1.5],fill=(40,40,52,255))
        for x,y,r in live: d.ellipse([x-r,y-r,x+r,y+r],fill=(92,92,108,255))
        for x,y,r in live: d.ellipse([x-r*0.7,y-r*0.8,x+r*0.1,y-r*0.15],fill=(118,118,134,255))
        img.alpha_composite(lay.resize((W,H),Image.NEAREST))
        img.alpha_composite(CRATER,(CX-CRATER.width//2,CY+120-CRATER.height//2))
        sq=min(1,dt/0.08)
        sw_,sh_=int(FR[0].width*(1+0.45*sq)),int(SH*(1-0.6*sq))
        flat=FR[0].resize((sw_,sh_),Image.NEAREST)
        img.alpha_composite(flat,(CX-sw_//2,CY+150-sh_))
        # debris
        if dt<0.9:
            d=ImageDraw.Draw(img)
            for vx,vy,s in debris:
                px=CX+vx*dt; py=CY+120+vy*dt+1600*dt*dt
                d.rectangle([px,py,px+s*P,py+s*P],fill=(90,60,40))
        # dizzy stars
        if dt>0.35:
            for k in range(3):
                a=2*math.pi*(k/3+dt*0.9)
                img.alpha_composite(STAR,(int(CX+math.cos(a)*150-STAR.width/2),int(CY+30+math.sin(a)*40-STAR.height/2)))
    if t>=IMPACT:
        dt=t-IMPACT
        if dt<0.1: img=Image.blend(img,Image.new('RGBA',(W,H),(255,255,255,255)),0.7*(1-dt/0.1))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (20,110,128,134,140,150,175,215): img.convert('RGB').resize((270,480)).save(f'p_{CHAR}_{f}.png')
ff.stdin.close(); ff.wait(); print('done',CHAR)
