import numpy as np, subprocess, math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=10.0; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
P=6
# Thornberry forest, crisp
bg=Image.open(A+'found_hd.gif'); BGS=[]; S=H/1080; cw=int(W/S)
for i in range(0,bg.n_frames,2):
    bg.seek(i); g=bg.convert('RGB').crop((960-cw//2,0,960-cw//2+cw,1080)).resize((W,H),Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(g).enhance(0.8).convert('RGBA'))
im=Image.open(A+'cyrus-walk-side.gif'); CF=[]
for i in range(im.n_frames): im.seek(i); CF.append(im.convert('RGBA').crop((290,130,570,800)))
CH=300
CF=[f.resize((int(f.width*CH/f.height),CH),Image.NEAREST) for f in CF]
JUMP=CF[3]; STAND=CF[1]
FEETPAD=4   # sprite bottom is the feet
GUM=Image.open('../gummy/mush_gummy_single.png').convert('RGBA'); GUM=GUM.crop(GUM.getbbox()); GUM=GUM.resize((120,int(GUM.height*120/GUM.width)),Image.LANCZOS)
# level geometry
LEDGE_Y=1520; PIT_L,PIT_R=290,910
PLAT_Y=1250; PW=324; PH=48
XL,XR=430,770          # platform centre range
X0=150; XC=560          # jump start x, crossing x
CYC=24; F0=12; KC=13    # frames per jump, first jump frame, crossing frame within cycle
TC=KC/FPS; G=6000.0
VX=(XC-X0)/TC; VY0=(LEDGE_Y-PLAT_Y+0.5*G*TC*TC)/TC
MATCH_CYCLE=int(sys.argv[1]) if len(sys.argv)>1 else 8
TMF=F0+MATCH_CYCLE*CYC+KC; TM=TMF/FPS
VP=float(sys.argv[2]) if len(sys.argv)>2 else 1310.0
def fold(u,lo,hi):
    L=hi-lo; v=(u-lo)%(2*L); return lo+(2*L-v if v>L else v)
# hand-keyed platform path: offsets from the landing spot at each jump's crossing frame
OFFS=[300,-262,240,-330,236,-250,322,-238,0,262,-300,245]
assert OFFS[MATCH_CYCLE]==0
rk=random.Random(4)
KEYS=[(-0.6,XC-250,0.0)]
for k,o in enumerate(OFFS):
    tk=(F0+k*CYC+KC)/FPS
    nxt=OFFS[k+1] if k+1<len(OFFS) else -o
    sgn=1 if nxt>o else -1          # head toward the next crossing side
    KEYS.append((tk,XC+o,sgn*rk.uniform(1300,1700)))
    ext=XC+(1 if sgn>0 else -1)*rk.uniform(320,340)
    KEYS.append((tk+0.4,min(900,max(200,ext)),0.0))
KEYS.append((KEYS[-1][0]+0.6,XC,0.0))
def plat_x(t):
    import bisect
    ts=[k[0] for k in KEYS]; i=max(0,min(len(KEYS)-2,bisect.bisect_right(ts,t)-1))
    (t0,x0,v0),(t1,x1,v1)=KEYS[i],KEYS[i+1]; h=t1-t0; u=(t-t0)/h
    h00=2*u**3-3*u**2+1; h10=u**3-2*u**2+u; h01=-2*u**3+3*u**2; h11=u**3-u**2
    return min(1010-PW/2,max(70+PW/2,h00*x0+h10*h*v0+h01*x1+h11*h*v1))
def cyr(f):
    """returns (x, feet_y, pose, alpha) for frame f"""
    if f<F0: return X0,LEDGE_Y,STAND,1
    k=(f-F0)//CYC; j=(f-F0)%CYC; tau=j/FPS
    x=X0+VX*tau; y=LEDGE_Y-VY0*tau+0.5*G*tau*tau
    if j==0: return X0,LEDGE_Y,STAND,1
    return x,y,JUMP,1
# report how close each crossing is
for k in range(12):
    f=F0+k*CYC+KC
    if f<N: print('cycle',k,'frame',f,'offset',round(plat_x(f/FPS)-XC))
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
# pixel ground / platform art
def block(w,h,top=(110,190,70),body=(120,82,50),dark=(60,38,22)):
    c=Image.new('RGBA',(w//P,h//P),(0,0,0,0)); d=ImageDraw.Draw(c); ww,hh=c.size
    d.rectangle([0,0,ww-1,hh-1],fill=dark); d.rectangle([1,1,ww-2,hh-2],fill=body)
    d.rectangle([0,0,ww-1,min(3,hh-1)],fill=top); d.rectangle([0,0,ww-1,0],fill=(170,230,110))
    rng=random.Random(w*h)
    for _ in range(ww*hh//14): x=rng.randrange(1,ww-1); y=rng.randrange(5,max(6,hh-1)); d.point((x,y),fill=dark)
    return c.resize((w,h),Image.NEAREST)
LEFT=block(PIT_L+12,H-LEDGE_Y+12); RIGHT=block(W-PIT_R+12,H-LEDGE_Y+12)
def plat():
    c=Image.new('RGBA',(PW//P,PH//P+1),(0,0,0,0)); d=ImageDraw.Draw(c); ww,hh=c.size
    d.rectangle([0,0,ww-1,hh-1],fill=(40,26,16)); d.rectangle([1,1,ww-2,hh-2],fill=(200,150,90)); d.rectangle([1,1,ww-2,2],fill=(240,200,130))
    for x in range(4,ww,8): d.line([(x,1),(x,hh-2)],fill=(140,95,50))
    return c.resize((PW,(PH//P+1)*P),Image.NEAREST)
PLAT=plat()
def spikes():
    c=Image.new('RGBA',((PIT_R-PIT_L)//P,12),(0,0,0,0)); d=ImageDraw.Draw(c)
    for x in range(0,c.width,6): d.polygon([(x,11),(x+3,1),(x+6,11)],fill=(200,205,215),outline=(60,60,75))
    return c.resize((PIT_R-PIT_L,72),Image.NEAREST)
SPK=spikes()
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGS[int(t*5)%len(BGS)].copy(); d=ImageDraw.Draw(img)
    # pit darkness + spikes
    d.rectangle([PIT_L,LEDGE_Y+40,PIT_R,H],fill=(14,10,24))
    img.alpha_composite(SPK,(PIT_L,H-72))
    img.alpha_composite(LEFT,(-12,LEDGE_Y)); img.alpha_composite(RIGHT,(PIT_R,LEDGE_Y))
    px=plat_x(t)
    x,y,pose,_=cyr(f)
    if f==TMF:   # the one frame he lands it: exact pose on the platform
        x,y,pose=px,PLAT_Y,STAND
    behind = (f!=TMF) and y>PLAT_Y+6 and abs(x-px)<PW/2+40
    if behind: img.alpha_composite(pose,(int(x-pose.width/2),int(y-pose.height+FEETPAD)))
    img.alpha_composite(PLAT,(int(px-PW/2),PLAT_Y))
    img.alpha_composite(GUM,(int(px+PW/2-GUM.width-14),PLAT_Y-GUM.height+4))
    if not behind: img.alpha_composite(pose,(int(x-pose.width/2),int(y-pose.height+FEETPAD)))
    # respawn puff on the ledge
    j=(f-F0)%CYC
    if f>=F0+CYC and j<3:
        r=40+j*18; d=ImageDraw.Draw(img); d.ellipse([X0-r,LEDGE_Y-150-r,X0+r,LEDGE_Y-150+r],outline=(255,255,255),width=8)
    ctext(img,W/2,300,'PAUSE WHEN HE',F(72)); ctext(img,W/2,400,'LANDS IT',F(72),(255,214,60))
    ctext(img,W/2,530,'Only 1 frame works',F(40))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f==TMF: img.convert('RGB').save('match.png')
    if f in (TMF-1,TMF+1): img.convert('RGB').save(f'nb_{f-TMF:+d}.png')
    if f%20==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done TMF',TMF,'TM',round(TM,3))
