import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=10.0; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
g=Image.open(A+'recov_hd.gif'); BGF=[]
for i in range(g.n_frames):
    g.seek(i); f=g.convert('RGB'); s=H/f.height; f=f.resize((int(f.width*s),H),Image.LANCZOS); ox=(f.width-W)//2
    BGF.append(ImageEnhance.Brightness(f.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(10))).enhance(0.7).convert('RGBA'))
src=Image.open('../screenshot/mel_bottle_only.png')
CUT=690  # remove the cap: keep the jar from the shoulder down
body=src.crop((1394,CUT,3047,3830)); cap=src.crop((1394,179,3047,CUT))
k=1000/ (3830-179); body=body.resize((int(body.width*k),int(body.height*k)),Image.LANCZOS); cap=cap.resize((int(cap.width*k),int(cap.height*k)),Image.LANCZOS)
BX=W//2-body.width//2; BY=H-140-body.height
# rim at the opening
rim=Image.new('RGBA',(body.width,40),(0,0,0,0)); ImageDraw.Draw(rim).ellipse([18,4,body.width-18,36],outline=(235,235,245,220),width=6)
gum=Image.open('../gummy/mel_gummy_single.png'); GW=190; gum=gum.resize((GW,int(gum.height*GW/gum.width)),Image.LANCZOS)
TX=W//2; TY=BY-15   # target centre: gummy sinking into the opening
# dashed outline of the gummy at the target
a=gum.split()[3].point(lambda v:255 if v>100 else 0)
ring=ImageChops.subtract(a.filter(ImageFilter.MaxFilter(9)),a.filter(ImageFilter.MaxFilter(3)))
ring=np.array(ring)>0; yy,xx=np.nonzero(ring); cy,cx=np.mean(yy),np.mean(xx)
ang=np.arctan2(yy-cy,xx-cx); dash=((ang*12/np.pi)%2)<1.1
outl=np.zeros((gum.height,gum.width,4),np.uint8); outl[yy[dash],xx[dash]]=(255,255,255,235)
OUTL=Image.fromarray(outl)
HW,HH=gum.width/2+6,gum.height/2+6
XMIN,XMAX,YMIN,YMAX=HW,W-HW,420,H-HH-40
def fold(u,lo,hi):
    L=hi-lo; v=(u-lo)%(2*L); return lo+(2*L-v if v>L else v)
TM=6.5
def pos(t):
    if t<3.0:  # slow drift down toward the opening, stopping just short
        u=t/3.0; e=1-(1-u)**1.6; return (TX, 430+(TY-210-430)*e, 0)
    vx,vy=1210,-1730
    def bp(tt): dt=tt-TM; return (fold(TX+vx*dt,XMIN,XMAX), fold(TY+vy*dt,YMIN,YMAX))
    if t<3.45:  # blend from the hover point into the bounce path
        u=(t-3.0)/0.45; e=u*u*(3-2*u); bx,by=bp(t); return (TX+(bx-TX)*e, (TY-40-170)+(by-(TY-40-170))*e, 0)
    bx,by=bp(t); return (bx,by,0)
# make the 3.0-3.2 handoff continuous: start bounce from where the drift ended
x32,y32,_=(TX+60,TY-70,0)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
front=body.copy(); fa=np.array(front.split()[3]); fa[:14]=0; front.putalpha(Image.fromarray(fa))   # jar below the rim, drawn over the gummy
match=[]
for f in range(N):
    t=f/FPS; img=BGF[int(t*10)%len(BGF)].copy()
    img.alpha_composite(cap.rotate(-18,resample=Image.BICUBIC,expand=True),(80,560+int(10*math.sin(t*2))))
    img.alpha_composite(body,(BX,BY)); img.alpha_composite(rim,(BX,BY-14))
    img.alpha_composite(OUTL,(TX-gum.width//2,TY-gum.height//2))
    x,y,_=pos(t)
    if f==round(TM*FPS): x,y=TX,TY; match.append(f)
    img.alpha_composite(gum,(int(x-gum.width/2),int(y-gum.height/2)))
    if abs(y-TY)<gum.height and abs(x-TX)<body.width/2: img.alpha_composite(front,(BX,BY))
    d=ImageDraw.Draw(img)
    for yy_,tx_ in ((170,'PUT THE GUMMY'),(250,'IN THE BOTTLE')):
        w=d.textlength(tx_,font=F(62)); d.text(((W-w)/2,yy_),tx_,font=F(62),fill=(255,255,255),stroke_width=7,stroke_fill=(20,15,35))
    w=d.textlength('Pause when it drops in',font=F(32)); d.text(((W-w)/2,345),'Pause when it drops in',font=F(32),fill=(255,214,90),stroke_width=5,stroke_fill=(20,15,35))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (30,95,150,195,250): img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('match',match)
