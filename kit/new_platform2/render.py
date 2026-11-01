import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=10.0; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
SH=210
IDLE=gif('idle_8.gif',SH); SIDE=gif('cyrus-walk-side.gif',SH)
GUM=Image.open('../gummy/mush_gummy_single.png').convert('RGBA'); GUM=GUM.resize((96,int(GUM.height*96/GUM.width)),Image.LANCZOS)
# background: Thornberry forest, crisp
g=Image.open(A+'found_hd.gif'); BGS=[]; S=H/1080; cw=int(W/S)
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB').crop((960-cw//2,0,960-cw//2+cw,1080)).resize((W,H),Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.7).convert('RGBA'))
TOPY=1320; LEDGE_X1=270; PIT_X0=270
# terrain layer (pixel tiles)
TER=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(TER); P=6
def block(x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(92,58,34,255))
    for yy in range(y0+30,y1,36):
        for xx in range(x0+((yy//36)%2)*24,x1,48): d.rectangle([xx,yy,xx+P*2,yy+P],fill=(74,44,26,255))
    d.rectangle([x0,y0,x1,y0+26],fill=(96,178,64,255)); d.rectangle([x0,y0+20,x1,y0+30],fill=(58,120,40,255))
    for xx in range(x0,x1,18): d.rectangle([xx,y0-6,xx+6,y0],fill=(120,200,80,255))
block(0,TOPY,LEDGE_X1,H)
# pit with spikes
d.rectangle([PIT_X0,TOPY+40,W,H],fill=(14,10,22,235))
for xx in range(PIT_X0,W,40):
    d.polygon([(xx,1800),(xx+20,1740),(xx+40,1800)],fill=(200,205,220,255)); d.polygon([(xx+20,1740),(xx+40,1800),(xx+28,1800)],fill=(140,145,165,255))
d.rectangle([PIT_X0,1800,W,H],fill=(40,36,52,255))
PW,PHh=170,34
def plank():
    p=Image.new('RGBA',(PW,PHh),(0,0,0,0)); dd=ImageDraw.Draw(p)
    dd.rectangle([0,0,PW-1,PHh-1],fill=(60,36,20,255)); dd.rectangle([4,4,PW-5,PHh-5],fill=(196,146,84,255))
    for xx in range(4,PW,42): dd.rectangle([xx,4,xx+3,PHh-5],fill=(140,96,52,255))
    dd.rectangle([4,4,PW-5,9],fill=(226,186,120,255))
    return p
PLANK=plank()
# jumps
AIR=0.6; XS=170; XL=700; PEAK=330
import itertools
rng=random.Random(5)
ts=np.arange(0,DUR,0.02)
best=None
for trial in range(400):
    pers=[rng.uniform(0.85,1.2) for _ in range(9)]
    J=[1.0]
    for p in pers[:-1]: J.append(J[-1]+p)
    if J[-1]+1.0>DUR: continue
    MK=rng.choice([4,5,6]); TMf=round((J[MK]+AIR)*FPS)/FPS
    f1,f2=rng.choice([(0.71,1.67),(0.61,1.41),(0.53,1.67)]); A1,A2=rng.choice([(210,90),(190,110)])
    for ph in np.linspace(0,2*math.pi,120):
        ph2=rng.uniform(0,6.28)
        bx=lambda t: 700+A1*np.sin(2*math.pi*f1*t+ph)+A2*np.sin(2*math.pi*f2*t+ph2)
        off=XL-bx(TMf); xs=bx(ts)+off
        if xs.min()<370 or xs.max()>1030: continue
        v=abs(bx(TMf+1/FPS)-bx(TMf-1/FPS))*FPS/2
        if v<900: continue
        miss=min(abs(bx(Jk+AIR)+off-XL) for k,Jk in enumerate(J) if k!=MK)
        if best is None or miss>best[0]: best=(miss,v,J,MK,f1,f2,A1,A2,ph,ph2,off)
miss,VEL,JUMPS,MATCH_K,f1,f2,A1,A2,ph,ph2,OFF=best
print('plank: miss margin',round(miss),'speed at match',round(VEL),'jumps',[round(j,2) for j in JUMPS],'match k',MATCH_K)
TM=JUMPS[MATCH_K]+AIR; FM=round(TM*FPS); TM=FM/FPS
def base_x(t): return 700+A1*math.sin(2*math.pi*f1*t+ph)+A2*math.sin(2*math.pi*f2*t+ph2)
def plank_x(t): return base_x(t)+OFF
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    dd=ImageDraw.Draw(img); w=dd.textlength(t,font=f); dd.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGS[int(t*5)%len(BGS)].copy(); img.alpha_composite(TER)
    px=plank_x(t)
    img.alpha_composite(PLANK,(int(px-PW/2),TOPY))
    img.alpha_composite(GUM,(int(px+PW/2-GUM.width-10),TOPY-GUM.height+6))
    # which jump are we in
    k=max([i for i,J in enumerate(JUMPS) if J<=t],default=-1)
    u=t-JUMPS[k] if k>=0 else -1
    if f==FM:
        sp=SIDE[0]; img.alpha_composite(sp,(int(XL-sp.width/2),TOPY-sp.height+2))
    elif k<0 or u>=0.95:
        sp=IDLE[int(t*8)%len(IDLE)]; a=1.0
        if k>=0 and u<1.05: pass
        img.alpha_composite(sp,(int(XS-sp.width/2),TOPY-sp.height+2))
    elif u<AIR:
        v=u/AIR; x=XS+(XL-XS)*v; y=TOPY-PEAK*4*v*(1-v)
        sp=SIDE[2]; img.alpha_composite(sp,(int(x-sp.width/2),int(y-sp.height+2)))
    elif u<0.9:
        # missed: keep falling into the spikes
        v=(u-AIR)/0.3; y=TOPY+ (1800-TOPY+60)*v*v; x=XL+40*v
        sp=SIDE[2].rotate(-120*v,resample=Image.NEAREST,expand=True); img.alpha_composite(sp,(int(x-sp.width/2),int(y-sp.height+2)))
    else:
        dd=ImageDraw.Draw(img); v=(u-0.9)/0.05
        for a_ in range(8):
            r=30+50*v; xx=XL+40+math.cos(a_*0.785)*r; yy=1760+math.sin(a_*0.785)*r*0.5
            dd.rectangle([xx-8,yy-8,xx+8,yy+8],fill=(240,240,240))
    ctext(img,W/2,300,'PAUSE WHEN HE',F(64)); ctext(img,W/2,395,'LANDS IT',F(64),(255,214,60))
    ctext(img,W/2,500,'Only 1 frame works',F(34))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (FM-1,FM,FM+1): img.convert('RGB').crop((0,900,W,1920)).resize((360,340)).save(f'm_{f-FM:+d}.png')
    if f%20==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done match frame',FM)
