import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=10.0; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
g=Image.open(A+'recov_hd.gif'); BGF=[]
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB'); s=H/f.height; f=f.resize((int(f.width*s),H),Image.LANCZOS); ox=(f.width-W)//2
    BGF.append(ImageEnhance.Brightness(f.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.5).convert('RGBA'))
def ld(p,h):
    im=Image.open(p).convert('RGBA'); im=im.crop(im.getbbox()); return im.resize((int(im.width*h/im.height),h),Image.LANCZOS)
NAMES=['MELATONIN','MUSHROOM','CREATINE','ACV']
FILES=['mel_gummy_red.png','mush_gummy_single.png','cre_gummy_single.png','acv_gummy_single.png']
GH=250
GS=[ld('../gummy/'+p,GH) for p in FILES]
TARGET=2
# silhouette of the target, bigger, dark fill + dashed white outline
SIL_H=390
src=ld('../gummy/'+FILES[TARGET],SIL_H)
a=src.split()[3].point(lambda v:255 if v>110 else 0)
pad=40; A2=Image.new('L',(a.width+2*pad,a.height+2*pad),0); A2.paste(a,(pad,pad))
sil=Image.new('RGBA',A2.size,(18,14,30,0)); sil.putalpha(A2.point(lambda v:215 if v else 0))
big=A2.filter(ImageFilter.MaxFilter(9)); ring=ImageChops.subtract(big.filter(ImageFilter.MaxFilter(9)),big)
r=np.array(ring)>0; yy,xx=np.nonzero(r); cy,cx=yy.mean(),xx.mean(); ang=np.arctan2(yy-cy,xx-cx)
dash=((ang*22/np.pi)%2)<1.15; o=np.zeros(r.shape+(4,),np.uint8); o[yy[dash],xx[dash]]=(255,255,255,245)
sil.alpha_composite(Image.fromarray(o)); SIL=sil
glow=Image.new('L',(W,H),0); ImageDraw.Draw(glow).ellipse([W//2-330,690-330,W//2+330,690+330],fill=120); glow=glow.filter(ImageFilter.GaussianBlur(110))
GL=Image.new('RGBA',(W,H),(255,230,170,0)); GL.putalpha(glow)
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
SLOTS=[(280,1250),(800,1250),(280,1680),(800,1680)]   # gummy bottom-centre
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGF[int(t*5)%len(BGF)].copy(); img.alpha_composite(GL)
    ctext(img,W/2,190,'WHICH GUMMY',F(70)); ctext(img,W/2,285,'FITS THE OUTLINE?',F(56),(255,214,60))
    sc=1+0.03*math.sin(2*math.pi*0.8*t)
    s2=SIL.resize((int(SIL.width*sc),int(SIL.height*sc)),Image.LANCZOS)
    img.alpha_composite(s2,(W//2-s2.width//2,690-s2.height//2))
    d=ImageDraw.Draw(img)
    for k,((x,yb),gm,nm) in enumerate(zip(SLOTS,GS,NAMES)):
        # card behind each option
        d.rounded_rectangle([x-235,yb-GH-50,x+235,yb+110],radius=28,fill=(25,20,40),outline=(255,214,60),width=5)
        bob=int(8*math.sin(2*math.pi*0.9*t+k*1.3))
        img.alpha_composite(gm,(x-gm.width//2,yb-gm.height+bob))
        ctext(img,x,yb+40,nm,F(36),(255,255,255),6)
    ctext(img,W/2,1835,'Comment your answer',F(38))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f==30: img.convert('RGB').save('frame.png')
ff.stdin.close(); ff.wait(); print('done')
