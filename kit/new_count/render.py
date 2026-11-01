import numpy as np, subprocess, math, random
import pymunk
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
rng=random.Random(8)
NG=47
T_POUR0,DT_DROP=1.2,0.12
T_POUR1=T_POUR0+NG*DT_DROP          # last drop
T_GUESS=T_POUR1+1.4                 # "comment your guess" beat
T_REVEAL=T_GUESS+3.0
T_COUNT=2.2                         # counter tick duration
DUR=T_GUESS+2.8; N=int(DUR*FPS)
# jar geometry (screen px, y down)
JL,JR,JB,JT=215,865,1720,760
R=53
# ---------- physics
space=pymunk.Space(); space.gravity=(0,2600)
st=space.static_body
segs=[pymunk.Segment(st,(JL,JT-40),(JL,JB-60),6),pymunk.Segment(st,(JL,JB-60),(JL+60,JB),6),pymunk.Segment(st,(JL+60,JB),(JR-60,JB),6),
      pymunk.Segment(st,(JR-60,JB),(JR,JB-60),6),pymunk.Segment(st,(JR,JB-60),(JR,JT-40),6)]
for s in segs: s.elasticity=0.05; s.friction=0.7
space.add(*segs)
KINDS=['acv','cre','mush','mel']
bodies=[]   # (body, kind, t_drop)
drops=[(T_POUR0+i*DT_DROP, rng.uniform(JL+R+40,JR-R-40), KINDS[i%4] if rng.random()<0.7 else rng.choice(KINDS)) for i in range(NG)]
SUB=8; TRACK=[]   # per video frame: list of (x,y,angle) per body index
di=0
for f in range(int(DUR*FPS)):
    t=f/FPS
    while di<NG and drops[di][0]<=t:
        td,x,k=drops[di]
        b=pymunk.Body(1,pymunk.moment_for_circle(1,0,R)); b.position=(x,-80); b.angle=rng.uniform(-0.6,0.6); b.angular_velocity=rng.uniform(-3,3); b.velocity=(rng.uniform(-60,60),900)
        c=pymunk.Circle(b,R); c.elasticity=0.08; c.friction=0.6
        space.add(b,c); bodies.append((b,k)); di+=1
    for _ in range(SUB): space.step(1/(FPS*SUB))
    TRACK.append([(b.position.x,b.position.y,b.angle) for b,_ in bodies])
final=TRACK[-1]
inside=[(JL<x<JR and JT-20<y<JB) for x,y,_ in final]
print('dropped',len(final),'inside',sum(inside),'top y',min(y for _,y,_ in final))
assert len(final)==NG and all(inside)
# count order: bottom row first, left to right
order=sorted(range(NG),key=lambda i:(-round(final[i][1]/60),final[i][0]))
# ---------- art
g=Image.open(A+'hub.gif'); BGF=[]
for i in range(0,g.n_frames,2):
    g.seek(i); fr=g.convert('RGB'); s=H/fr.height; fr=fr.resize((int(fr.width*s),H),Image.LANCZOS); ox=(fr.width-W)//2
    BGF.append(ImageEnhance.Brightness(fr.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.5).convert('RGBA'))
def ld(n,w):
    p='../gummy/mel_gummy_red.png' if n=='mel' else f'../gummy/{n}_gummy_single.png'
    im=Image.open(p).convert('RGBA'); a=np.array(im)[:,:,3]; ys,xs=np.nonzero(a>40); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    k=w/max(im.width,im.height); return im.resize((int(im.width*k),int(im.height*k)),Image.LANCZOS)
SP={k:ld(k,int(R*2.15)) for k in KINDS}
ROT={}
def sprite(k,ang):
    a=int(round(math.degrees(ang)/3))*3%360
    key=(k,a)
    if key not in ROT: ROT[key]=SP[k].rotate(-a,resample=Image.BICUBIC,expand=True)
    return ROT[key]
# jar back + front glass
back=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(back)
bd.rounded_rectangle([JL-14,JT-60,JR+14,JB+14],radius=70,fill=(200,225,240,40),outline=(220,240,255,120),width=8)
front=Image.new('RGBA',(W,H),(0,0,0,0)); fd=ImageDraw.Draw(front)
fd.rounded_rectangle([JL-14,JT-60,JR+14,JB+14],radius=70,outline=(235,248,255,200),width=10)
fd.rectangle([JL+20,JT+10,JL+44,JB-120],fill=(255,255,255,70)); fd.rectangle([JL+60,JT+10,JL+70,JB-200],fill=(255,255,255,45))
fd.rectangle([JR-50,JT+40,JR-38,JB-260],fill=(255,255,255,40))
fd.ellipse([JL-30,JT-85,JR+30,JT-35],outline=(235,248,255,220),width=10)
shadow=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(shadow).ellipse([JL-40,JB-10,JR+40,JB+50],fill=(0,0,0,110)); shadow=shadow.filter(ImageFilter.GaussianBlur(14))
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGF[int(t*5)%len(BGF)].copy()
    img.alpha_composite(shadow); img.alpha_composite(back)
    pos=TRACK[min(f,len(TRACK)-1)]
    ncount=0
    if t>=T_REVEAL: ncount=min(NG,int((t-T_REVEAL)/T_COUNT*NG)+1)
    counted=set(order[:ncount])
    for i,(x,y,a) in enumerate(pos):
        sp=sprite(bodies[i][1],a); img.alpha_composite(sp,(int(x-sp.width/2),int(y-sp.height/2)))
    img.alpha_composite(front)
    d=ImageDraw.Draw(img)
    if t>=T_REVEAL:
        for i in counted:
            x,y,_=pos[i]; d.ellipse([x-12,y-12,x+12,y+12],fill=(255,214,60),outline=(20,15,35),width=4)
        if ncount<NG:
            x,y,_=pos[order[ncount-1]]; d.ellipse([x-R,y-R,x+R,y+R],outline=(255,255,255),width=6)
    # text
    if t<T_GUESS:
        ctext(img,W/2,230,'HOW MANY',F(84)); ctext(img,W/2,340,'GUMMIES?',F(84),(255,214,60))
    elif t<T_REVEAL:
        ctext(img,W/2,230,'COMMENT',F(76)); ctext(img,W/2,330,'YOUR GUESS',F(76),(255,214,60))
    else:
        sc=1.0
        if ncount==NG: sc=1+0.35*max(0,1-(t-(T_REVEAL+T_COUNT))/0.25)
        ctext(img,W/2,260,str(ncount),F(int(150*sc)),(255,214,60),10)
        if ncount==NG and t>T_REVEAL+T_COUNT+0.3: ctext(img,W/2,460,'Did you get it?',F(48))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%45==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done',round(DUR,2))
