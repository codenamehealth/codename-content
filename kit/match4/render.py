import numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS,N=1080,1920,30,300
TM=192; SP=650; P=4*SP; V=[610,-480,730,-550]
def F(s): return ImageFont.truetype(FONT,s)
g=Image.open(A+'scene_forest.png').convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2+300
g=g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(12)); g=ImageEnhance.Brightness(g).enhance(0.75).convert('RGBA')
BG=g
OW,OH=0,600
NAMES=['FOUNDATION','VITALITY','ENERGY','RECOVERY']; COLS=[(143,214,96),(110,170,255),(255,170,70),(200,140,230)]
PH=500; NF=F(44)
RAW=[]
for n in ['acv','creatine','mushroom','melatonin']:
    im=Image.open(A+f'jar_{n}.png').convert('RGBA'); im=im.crop(im.getbbox()); k=PH/im.height; RAW.append(im.resize((int(im.width*k),PH),Image.NEAREST))
_d=ImageDraw.Draw(Image.new('RGBA',(10,10)))
OW=max(max(r.width for r in RAW), max(int(_d.textlength(n,font=NF)) for n in NAMES)+24); OW+=(4-OW%4)%4
OBJ=[]
for im,nm,col in zip(RAW,NAMES,COLS):
    c=Image.new('RGBA',(OW,OH),(0,0,0,0)); c.paste(im,((OW-im.width)//2,0),im)
    d=ImageDraw.Draw(c); w=d.textlength(nm,font=NF); d.text(((OW-w)/2,PH+30),nm,font=NF,fill=col,stroke_width=5,stroke_fill=(20,15,35))
    OBJ.append(c)
CW=OW//4; X0=(W-OW)//2; YC=1150
def ctext(d,y,t,f):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=(255,255,255),stroke_width=6,stroke_fill=(25,20,45))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=(f-TM)/FPS; img=BG.copy()
    for c in range(4):
        off=(V[c]*t)%P
        strip=Image.new('RGBA',(CW,H),(0,0,0,0))
        for k in range(-3,8):
            y=int(YC-OH/2+k*SP+off)-2*P//2*0
            for wrap in (-P,0,P):
                yy=y+wrap
                if -OH<yy<H: strip.alpha_composite(OBJ[k%4].crop((c*CW,0,(c+1)*CW,OH)),(0,yy)) if 0<=yy and yy+OH<=H else strip.paste(OBJ[k%4].crop((c*CW,0,(c+1)*CW,OH)),(0,yy),OBJ[k%4].crop((c*CW,0,(c+1)*CW,OH)))
        img.alpha_composite(strip,(X0+c*CW,0))
    d=ImageDraw.Draw(img)
    ctext(d,520,'PAUSE & MATCH ALL 4',F(50)); ctext(d,600,'TO REVEAL YOUR GUILD',F(50))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (60,TM,TM+1): img.convert('RGB').resize((360,640)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done')
