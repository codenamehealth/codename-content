import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
HT=6200; YB=HT-700; YT=640
T_IN,T_SCROLL,T_HOLD=2.6,13.5,3.4; DUR=T_IN+T_SCROLL+T_HOLD; N=int(DUR*FPS)
rng=random.Random(11); np.random.seed(11)
XS=[300,540,780]; ENDX={0:780,1:300,2:540}   # A->gummy, B->Hollow, C->gold
PRIZE_AT={300:'hollow',540:'gold',780:'gummy'}
COLS=[((255,196,60),(150,95,10)),((176,112,236),(80,40,130)),((80,214,190),(20,110,100))]
def curve(i):
    s=np.linspace(0,1,4000)
    sm=s*s*(3-2*s)
    env=np.sin(np.pi*s)**0.6
    x=XS[i]+(ENDX[i]-XS[i])*sm
    for _ in range(3):
        a=rng.uniform(170,300); fq=rng.uniform(2.5,5.5); ph=rng.uniform(0,6.28); x=x+a*env*np.sin(2*np.pi*fq*s+ph)
    y=YB-(YB-YT)*s
    span=YB-YT
    for _ in range(2):   # little loops
        sc=rng.uniform(0.15,0.85); w=0.035; r=rng.uniform(80,105); dr=rng.choice([-1,1])
        u=(s-sc)/w; m=(u>=0)&(u<=1); th=2*np.pi*u[m]
        x[m]+=dr*r*(1-np.cos(th)); y[m]+=r*np.sin(th)
    x=540+470*np.tanh((x-540)/470)
    return np.stack([x,y],1)
CURVES=[curve(i) for i in range(3)]
# ---- world image
world=Image.new('RGBA',(W,HT),(34,28,52,255)); d=ImageDraw.Draw(world)
for x in range(0,W,90): d.rectangle([x,0,x+44,HT],fill=(40,33,61,255))
# decor: sparkles, coins and the four gummies, small
G={n:Image.open(f'../gummy/{n}_gummy_single.png').convert('RGBA') for n in ('acv','cre','mush','mel')}
def thumb(im,w): return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
coin=Image.new('RGBA',(7,7),(0,0,0,0)); dc=ImageDraw.Draw(coin); dc.ellipse([0,0,6,6],fill=(160,100,10,255)); dc.ellipse([1,1,5,5],fill=(255,205,40,255)); dc.point((2,2),fill=(255,250,210,255))
COIN=coin.resize((42,42),Image.NEAREST)
for k in range(70):
    x=rng.uniform(40,W-90); y=rng.uniform(YT+200,YB-100); kind=rng.random()
    if kind<0.35: world.alpha_composite(thumb(G[rng.choice(list(G))],rng.randint(60,85)),(int(x),int(y)))
    elif kind<0.65: world.alpha_composite(COIN,(int(x),int(y)))
    else:
        c=(255,230,120,255); s_=rng.choice([6,8]); d.rectangle([x,y-2*s_,x+s_,y+3*s_],fill=c); d.rectangle([x-2*s_,y,x+3*s_,y+s_],fill=c)
# paths: outline, fill, highlight; drawn in order so they weave by layering
for i in (1,0,2):
    pts=[tuple(p) for p in CURVES[i][::4]]
    fill,dark=COLS[i]
    d.line(pts,fill=(20,14,30,255),width=58,joint='curve')
    d.line(pts,fill=dark+(255,),width=46,joint='curve')
    d.line(pts,fill=fill+(255,),width=34,joint='curve')
    hp=[(x-7,y) for x,y in pts]; d.line(hp,fill=tuple(min(255,c+60) for c in fill)+(255,),width=8,joint='curve')
    for (x,y) in (pts[0],pts[-1]): d.ellipse([x-34,y-34,x+34,y+34],fill=(20,14,30,255)); d.ellipse([x-26,y-26,x+26,y+26],fill=fill+(255,))
# start letters
for i,x in enumerate(XS):
    y=YB+70; d.ellipse([x-48,y-48,x+48,y+48],fill=(20,14,30,255)); d.ellipse([x-40,y-40,x+40,y+40],fill=COLS[i][0]+(255,))
    f=F(44); tw=d.textlength('ABC'[i],font=f); d.text((x-tw/2,y-22),'ABC'[i],font=f,fill=(20,14,30))
WORLD=world
HOL=gif('idle_9.gif',290); CYR=gif('idle_8.gif',210)
GOLD=thumb(Image.open('../gummy/gold_cut.png').convert('RGBA'),270)
GUMMY=thumb(G['mush'],200)
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    dd=ImageDraw.Draw(img); w=dd.textlength(t,font=f); dd.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
def camy(t):
    top0=HT-H
    if t<T_IN: return top0
    u=min(1,(t-T_IN)/T_SCROLL); e=u if 0.04<u<0.96 else u   # constant speed
    e=u*u*(3-2*u)*0.12+u*0.88
    return top0-(top0-0)*e
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; cy=camy(t)
    img=WORLD.crop((0,int(cy),W,int(cy)+H)).copy()
    # prizes at the top of each path end
    for x,kind in PRIZE_AT.items():
        y=YT-60-cy
        if y<-400: continue
        if kind=='hollow':
            fr=HOL[int(t*8)%len(HOL)]; img.alpha_composite(fr,(int(x-fr.width/2),int(y-fr.height+20)))
        elif kind=='gold': img.alpha_composite(GOLD,(int(x-GOLD.width/2),int(y-GOLD.height+20)))
        else:
            gl=Image.new('RGBA',(260,260),(0,0,0,0)); ImageDraw.Draw(gl).ellipse([0,0,260,260],fill=(255,235,120,int(70+30*math.sin(t*5))))
            gy=int(y-GUMMY.height+10+10*math.sin(t*3)); img.alpha_composite(gl,(int(x-130),gy+GUMMY.height//2-130)); img.alpha_composite(GUMMY,(int(x-GUMMY.width/2),gy))
    # start: Cyrus + title
    sy=YB+150-cy
    if sy<H+300:
        fr=CYR[int(t*8)%len(CYR)]; img.alpha_composite(fr,(int(W/2-fr.width/2),int(sy+525-fr.height)))
        ctext(img,W/2,sy+100,'CHOOSE YOUR PATH',F(62)); ctext(img,W/2,sy+185,'START!',F(62),(255,214,60))
    if t>=T_IN+T_SCROLL-0.2:
        u=t-(T_IN+T_SCROLL-0.2); sc=1+0.2*max(0,1-u/0.25)
        ctext(img,W/2,1180,'WHAT DID',F(int(70*sc))); ctext(img,W/2,1280,'YOU GET?',F(int(70*sc)),(255,214,60))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%60==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done',DUR)
