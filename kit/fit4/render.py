import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from scipy import ndimage
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=20.0; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
g=Image.open(A+'vit_hd.gif'); g.seek(0); g=g.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(12))).enhance(0.6).convert('RGBA')
def ld(p,w):
    im=Image.open(p); im=im.crop(im.getbbox()); return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
GS=[ld('../gummy/acv_gummy_single.png',400),ld('../gummy/cre_gummy_single.png',420),ld('../gummy/mush_gummy_single.png',400),ld('../gummy/mel_gummy_single.png',360)]
CEN=[(290,760),(790,760),(290,1250),(790,1250)]
# bite cut per gummy: an ellipse slicing in from the side facing the grid centre (like the reference)
CUTS=[(1.0,0.55,0.42,0.75),(0.0,0.55,0.42,0.75),(1.0,0.45,0.42,0.75),(0.0,0.45,0.42,0.75)]
def split(o,c):
    w,h=o.size; m=Image.new('L',(w,h),0); cx,cy,rx,ry=c
    ImageDraw.Draw(m).ellipse([cx*w-rx*w,cy*h-ry*h,cx*w+rx*w,cy*h+ry*h],fill=255)
    a=np.array(o.split()[3]); mm=np.array(m)>0
    piece=o.copy(); pa=a.copy(); pa[~mm]=0; piece.putalpha(Image.fromarray(pa))
    rest=o.copy(); ra=a.copy(); ra[mm]=0; rest.putalpha(Image.fromarray(ra))
    inside=(a>100)&mm; hole=np.zeros((h,w,4),np.uint8); hole[inside]=(255,255,255,255)
    edge=inside&~ndimage.binary_erosion(inside,iterations=5); hole[edge]=(60,50,120,255)
    return rest,Image.fromarray(hole),piece
P=[split(GS[i],CUTS[i]) for i in range(4)]
PER=6.0; ALIGN=[4.0,10.0,16.0]
HARM=[(1,2,1),(2,1,3),(3,1,2),(1,3,2)]       # integer harmonics: everything returns to 0 every PER seconds
AMP=[(150,170,40),(160,150,45),(150,160,40),(165,150,45)]
PH=[(0.0,0.0,0.0),(0.0,0.0,0.0),(0.0,0.0,0.0),(0.0,0.0,0.0)]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
match=[]
for f in range(N):
    t=f/FPS; img=BG.copy(); dt=t-ALIGN[0]
    exact=any(f==round(a*FPS) for a in ALIGN)
    if exact: match.append(f)
    for i in range(4):
        rest,hole,piece=P[i]; cx,cy=CEN[i]; w,h=rest.size; x0,y0=cx-w//2,cy-h//2
        img.alpha_composite(hole,(x0,y0)); img.alpha_composite(rest,(x0,y0))
        hx,hy,hr=HARM[i]; ax,ay,ar=AMP[i]; om=2*math.pi/PER
        dx=ax*math.sin(om*hx*dt); dy=ay*math.sin(om*hy*dt+ (i*0.0)); ang=ar*math.sin(om*hr*dt)
        # extra drift so pieces wander more (still 0 at every alignment)
        dx+=60*math.sin(om*(hx+2)*dt); dy+=50*math.sin(om*(hy+2)*dt)
        if exact: dx=dy=ang=0
        pc=Image.new('RGBA',(w*3,h*3),(0,0,0,0)); pc.alpha_composite(piece,(w,h)); pr=pc.rotate(ang,resample=Image.BICUBIC,center=(w*1.5,h*1.5))
        img.alpha_composite(pr,(int(x0-w+dx),int(y0-h+dy)))
    d=ImageDraw.Draw(img)
    for k,(tx,fs,col) in enumerate([('PAUSE WHEN ALL 4',58,(255,255,255)),('FIT PERFECTLY',58,(255,255,255))]):
        w_=d.textlength(tx,font=F(fs)); d.text(((W-w_)/2,170+k*85),tx,font=F(fs),fill=col,stroke_width=7,stroke_fill=(20,15,35))
    tx='90 out of 100 people fail'; w_=d.textlength(tx,font=F(34)); d.text(((W-w_)/2,1600),tx,font=F(34),fill=(255,214,90),stroke_width=5,stroke_fill=(20,15,35))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (30,120,200,300): img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('match',match)
