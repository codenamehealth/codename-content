import numpy as np, math, subprocess, random
from PIL import Image, ImageDraw, ImageEnhance
from parts import *
W,H,FPS=1080,1920,30; DUR=6.6; N=int(DUR*FPS)
SC=10   # screen px per native pixel
def clean(im):
    a=np.array(im); al=a[:,:,3]>0
    nb=sum(np.roll(np.roll(al,dy,0),dx,1) for dy in (-1,0,1) for dx in (-1,0,1))-al
    a[al&(nb<2)]=0; return Image.fromarray(a)
asm,ap=assembly(-35)
an=np.array(asm); ys,xs=np.nonzero(an[:,:,3]>0)
d=np.hypot(xs-ap[0],ys-ap[1]); TIP=(xs[d.argmax()]-ap[0], ys[d.argmax()]-ap[1])
def tip_at(ang):
    t=math.radians(ang); dx,dy=TIP
    return (math.cos(t)*dx-math.sin(t)*dy, math.sin(t)*dx+math.cos(t)*dy)
# background
g=Image.open(A+'found_hd.gif'); BGS=[]; S=H/1080; cw=int(W/S)
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB').crop((960-cw//2,0,960-cw//2+cw,1080)).resize((W,H),Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.85).convert('RGBA'))
# timeline of arm angle
def ease(u): return u*u*(3-2*u)
KEYS=[(0,-12),(1.0,-12),(1.45,-165),(1.57,-15),(2.2,-15),(2.6,-40),(2.85,-170),(2.97,-10),(3.6,-10),(3.9,-35),(4.35,-178),(4.5,-5),(5.2,-5),(5.7,-160),(6.6,-158)]
SLASH=[(1.45,1.57),(2.85,2.97),(4.35,4.5)]
def ang_at(t):
    for (t0,a0),(t1,a1) in zip(KEYS,KEYS[1:]):
        if t0<=t<=t1:
            u=(t-t0)/(t1-t0) if t1>t0 else 1
            fast=any(abs(t0-s0)<1e-6 for s0,_ in SLASH)
            return a0+(a1-a0)*(u if fast else ease(u))
    return KEYS[-1][1]
OX,OY=(W-160*SC)//2+ (160*SC-92*SC)//2 - 34*SC, 880   # place body
OX=int(W/2-46*SC-40*SC+ 34*SC); OY=520
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
rng=random.Random(3); trail=[]
for f in range(N):
    t=f/FPS
    # native canvas
    can=Image.new('RGBA',(160,130),(0,0,0,0)); bx,by=34,10
    body=Image.fromarray(BODY[int(t*8)%NF])
    a=ang_at(t)
    r,rp=rot_pixel(asm,a,ap); r=clean(r)
    px,py=bx+PIV[0], by+PIV[1]
    # smear arc for slashes
    insl=[s for s in SLASH if s[0]-0.01<=t<=s[1]+0.12]
    if not insl: can.alpha_composite(body,(bx,by))
    if insl:
        s0,s1=insl[0]; aa=ang_at(min(t,s1)); a_start=ang_at(s0)
        lay=Image.new('RGBA',can.size,(0,0,0,0)); dd=ImageDraw.Draw(lay)
        fade=1.0 if t<=s1 else max(0,1-(t-s1)/0.12)
        steps=14; pts_out=[]; pts_in=[]
        lo=max(a_start, aa-120)
        for k in range(steps+1):
            ak=lo+(aa-lo)*k/steps; tx,ty=tip_at(ak); L=math.hypot(tx,ty)
            pts_out.append((px+tx,py+ty)); pts_in.append((px+tx*0.55,py+ty*0.55))
        poly=pts_out+pts_in[::-1]
        dd.polygon(poly,fill=(235,245,255,int(150*fade)))
        dd.line(pts_out,fill=(255,255,255,int(255*fade)),width=1)
        can.alpha_composite(lay)
    can.alpha_composite(body,(bx,by))
    can.alpha_composite(r,(int(round(px-rp[0])),int(round(py-rp[1]))))
    # impact sparks right after each slash
    for s0,s1 in SLASH:
        dt=t-s1
        if 0<=dt<0.25:
            tx,ty=tip_at(ang_at(s1)); d2=ImageDraw.Draw(can)
            for k in range(6):
                th=k*1.047+0.3; rr=2+dt*40
                x=px+tx+math.cos(th)*rr; y=py+ty+math.sin(th)*rr*0.6
                d2.point((x,y),fill=(255,240,160,255)); d2.point((x+1,y),fill=(255,240,160,255))
    sprite=can.resize((160*SC,130*SC),Image.NEAREST)
    # camera shake
    sh=0
    for s0,s1 in SLASH:
        if 0<=t-s1<0.15: sh=max(sh,(14 if s0>4 else 7)*(1-(t-s1)/0.15))
    img=BGS[int(t*5)%len(BGS)].copy()
    sx,sy=int(rng.uniform(-sh,sh)),int(rng.uniform(-sh,sh))
    # shadow
    shd=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(shd).ellipse([W//2-260+sx,OY+76*SC-30+sy,W//2+180+sx,OY+76*SC+40+sy],fill=(0,0,0,70))
    img.alpha_composite(shd)
    img.alpha_composite(sprite,(int(W/2-(bx+46)*SC)+sx,OY+sy))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%15==0 or any(abs(t-(s1-0.04))<0.017 for _,s1 in SLASH): img.convert('RGB').resize((270,480)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done')
