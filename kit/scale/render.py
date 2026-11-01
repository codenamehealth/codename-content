import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
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
SH=200
HOL=gif('idle_9.gif',SH); CYR=gif('idle_8.gif',SH); JOY=gif('idle_5.gif',SH)
# outer background: castle, blurred
def bgframes(p,crop_w=None,blur=0,bright=1.0,size=(W,H)):
    g=Image.open(A+p); out=[]
    for i in range(0,g.n_frames,2):
        g.seek(i); f=g.convert('RGB'); s=size[1]/f.height; f=f.resize((int(f.width*s),size[1]),Image.NEAREST if not blur else Image.LANCZOS); ox=(f.width-size[0])//2
        f=f.crop((ox,0,ox+size[0],size[1]))
        if blur: f=f.filter(ImageFilter.GaussianBlur(blur))
        out.append(ImageEnhance.Brightness(f).enhance(bright).convert('RGBA'))
    return out
OUT=bgframes('vit_hd.gif',blur=14,bright=0.5)
PW,PH=500,580; GX,GY=30,560; GAP=20
PANELS=[('hub.gif',[HOL,HOL,HOL],'30'),('found_hd.gif',[HOL,HOL,CYR],'35'),('sun_hd.gif',[CYR,JOY,JOY],'31'),('recov_hd.gif',[JOY],'?')]
PBG=[bgframes(p,bright=0.95,size=(PW,PH)) for p,_,_ in PANELS]
def scale(d,x0,y0,w,val):
    # platform + body + green LCD
    d.rectangle([x0+20,y0,x0+w-20,y0+22],fill=(30,30,40)); d.rectangle([x0+24,y0+3,x0+w-24,y0+18],fill=(150,154,170))
    d.polygon([(x0,y0+22),(x0+w,y0+22),(x0+w-14,y0+150),(x0+14,y0+150)],fill=(20,24,50))
    d.polygon([(x0+6,y0+26),(x0+w-6,y0+26),(x0+w-18,y0+144),(x0+18,y0+144)],fill=(36,46,90))
    lx0,lx1,ly0,ly1=x0+w//2-130,x0+w//2+130,y0+48,y0+122
    d.rectangle([lx0-6,ly0-6,lx1+6,ly1+6],fill=(10,12,20)); d.rectangle([lx0,ly0,lx1,ly1],fill=(150,205,90))
    f=F(46); tw=d.textlength(val,font=f)
    d.text((lx0+150-tw,ly0+16),val,font=f,fill=(200,30,30) if val=='?' else (25,40,20))
    d.text((lx0+168,ly0+28),'kg',font=F(24),fill=(25,40,20))
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=OUT[int(t*5)%len(OUT)].copy()
    d=ImageDraw.Draw(img)
    d.rectangle([GX-10,GY-10,GX+2*PW+GAP+10,GY+2*PH+GAP+10],fill=(15,12,25))
    for k,(bgp,chars,val) in enumerate(PANELS):
        px=GX+(k%2)*(PW+GAP); py=GY+(k//2)*(PH+GAP)
        pan=PBG[k][int(t*5)%len(PBG[k])].copy(); pd=ImageDraw.Draw(pan)
        sy=PH-185; scale(pd,20,sy,PW-40,val)
        n=len(chars); tot=sum(c[0].width for c in chars)-18*(n-1); x=(PW-tot)//2
        for j,c in enumerate(chars):
            fr=c[int(t*8+j*2+k)%len(c)]; pan.alpha_composite(fr,(x,sy+8-fr.height)); x+=fr.width-18
        img.alpha_composite(pan,(px,py))
    ctext(img,W/2,330,"WHAT'S THE",F(76)); ctext(img,W/2,430,'ANSWER?',F(76),(255,214,60))
    ctext(img,W/2,GY+2*PH+GAP+70,'Comment your answer',F(40))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f==60: img.convert('RGB').save('frame.png')
ff.stdin.close(); ff.wait(); print('done')
