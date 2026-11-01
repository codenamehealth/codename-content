import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=16.0; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
g=Image.open(A+'sun_hd.gif'); g.seek(0); g=g.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.8).convert('RGBA')
def load(p,h):
    im=Image.open(p).convert('RGBA'); im=im.crop(im.getbbox()); k=h/im.height; return im.resize((int(im.width*k),h),Image.LANCZOS)
OBJ=[load('../screenshot/acv_bottle_only.png',720), load('../gummy/acv_gummy_single.png',420)]
HOME=[(300,1000),(800,1180)]
K=2.5/4.0
LV=[('NOOB',(110,200,90),0.0,4.0,1.0*K,0.9),('PRO',(90,150,255),4.0,8.0,1.5*K,1.0),('HACKER',(235,80,70),8.0,12.0,2.1*K,1.1),('GOD',(255,214,90),12.0,16.0,2.8*K,1.2)]
# cut per level per object: circle (cx,cy,r) in fractions of the object size
CUT=[[(1.05,0.95,0.75),(1.0,0.0,0.75)],[(-0.05,0.0,0.7),(0.0,1.0,0.7)],[(1.0,0.5,0.55),(0.0,0.4,0.55)],[(0.5,-0.15,0.5),(1.0,1.0,0.5)]]
def split(o,c):
    w,h=o.size; m=Image.new('L',(w,h),0); ImageDraw.Draw(m).ellipse([c[0]*w-c[2]*max(w,h),c[1]*h-c[2]*max(w,h),c[0]*w+c[2]*max(w,h),c[1]*h+c[2]*max(w,h)],fill=255)
    a=np.array(o.split()[3]); mm=np.array(m)>0
    piece=o.copy(); pa=a.copy(); pa[~mm]=0; piece.putalpha(Image.fromarray(pa))
    rest=o.copy(); ra=a.copy(); ra[mm]=0; rest.putalpha(Image.fromarray(ra))
    hole=Image.new('RGBA',(w,h),(12,10,18,255)); ha=a.copy(); ha[~mm]=0; hole.putalpha(Image.fromarray(ha))
    return rest,hole,piece
PARTS=[[split(OBJ[i],CUT[l][i]) for i in range(2)] for l in range(4)]
FR=[(1.0,1.37,0.83),(1.21,0.77,1.13)]   # per-object x/y/rotation frequency multipliers (incommensurate)
AMP=[(230,260,55),(200,230,70)]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
MATCH=[]
for f in range(N):
    t=f/FPS; li=min(3,int(t/4.0)); name,col,t0,t1,spd,ampk=LV[li]
    tm=t0+2.24  # both pieces lock in exactly here (frame-aligned)
    tm=round(tm*FPS)/FPS
    img=BG.copy(); d=ImageDraw.Draw(img)
    for i in range(2):
        rest,hole,piece=PARTS[li][i]; hx,hy=HOME[i]; w,h=rest.size; x0,y0=hx-w//2,hy-h//2
        img.alpha_composite(hole,(x0,y0)); img.alpha_composite(rest,(x0,y0))
        dt=t-tm; fx,fy,fr=FR[i]; ax,ay,ar=AMP[i]
        dx=ax*ampk*math.sin(2*math.pi*0.55*spd*fx*dt); dy=ay*ampk*math.sin(2*math.pi*0.55*spd*fy*dt+ (0 if i==0 else 0)); ang=ar*ampk*math.sin(2*math.pi*0.55*spd*fr*dt)
        if f==round(tm*FPS): dx=dy=ang=0
        pc=Image.new('RGBA',(w*3,h*3),(0,0,0,0)); pc.alpha_composite(piece,(w,h)); pr=pc.rotate(ang,resample=Image.BICUBIC,center=(w*1.5,h*1.5))
        img.alpha_composite(pr,(int(x0-w+dx),int(y0-h+dy)))
    fs=F(56)
    for k,tx in enumerate(['PAUSE WHEN BOTH','FIT PERFECTLY']):
        tw=d.textlength(tx,font=fs); d.text(((W-tw)/2,160+k*80),tx,font=fs,fill=(255,255,255),stroke_width=7,stroke_fill=(20,15,35))
    fl=F(84); tw=d.textlength(name,font=fl); d.text(((W-tw)/2,1560),name,font=fl,fill=col,stroke_width=8,stroke_fill=(20,15,35))
    if f==round(tm*FPS): MATCH.append(f)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (20,round(1.4*30),100,round(6.4*30),280): img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('match frames',MATCH)
