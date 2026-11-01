import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=10.6; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
rng=random.Random(21)
g=Image.open(A+'vit_hd.gif'); BGF=[]
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB'); s=H/f.height; f=f.resize((int(f.width*s),H),Image.LANCZOS); ox=(f.width-W)//2
    BGF.append(ImageEnhance.Brightness(f.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.45).convert('RGBA'))
gm=Image.open('../gummy/mush_gummy_single.png').convert('RGBA')
a=np.array(gm)[:,:,3]; ys,xs=np.nonzero(a>40); gm=gm.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
COLS,ROWS=8,10; CW=122; GW=104
GUM=gm.resize((GW,int(gm.height*GW/gm.width)),Image.LANCZOS)
ODD_RC=(6,5)   # row, col of the odd one (0-indexed)
ODD=gm.rotate(-9,resample=Image.BICUBIC,expand=True); k=GW/gm.width; ODD=ODD.resize((int(ODD.width*k),int(ODD.height*k)),Image.LANCZOS)
GX0=(W-COLS*CW)//2; GY0=560
board=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(board)
bd.rounded_rectangle([GX0-24,GY0-24,GX0+COLS*CW+24,GY0+ROWS*CW+24],radius=30,fill=(236,224,198,255),outline=(255,214,60,255),width=6)
CENT={}
for r in range(ROWS):
    for c in range(COLS):
        cx=GX0+c*CW+CW//2+rng.randint(-3,3); cy=GY0+r*CW+CW//2+rng.randint(-3,3)
        im=ODD if (r,c)==ODD_RC else GUM
        board.alpha_composite(im,(cx-im.width//2,cy-im.height//2)); CENT[(r,c)]=(cx,cy)
BOARD=board
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
T_GO=2.4; T_UP=T_GO+5.0
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGF[int(t*5)%len(BGF)].copy(); d=ImageDraw.Draw(img)
    ctext(img,W/2,150,'FIND THE ODD',F(70)); ctext(img,W/2,245,'GUMMY IN',F(70)); ctext(img,W/2,340,'5 SECONDS',F(70),(255,214,60))
    if t<T_GO:
        d.rounded_rectangle([GX0-24,GY0-24,GX0+COLS*CW+24,GY0+ROWS*CW+24],radius=30,fill=(236,224,198,255),outline=(255,214,60,255),width=6)
        n=3-int(t/0.8); sc=1+0.35*max(0,1-((t%0.8)/0.2))
        ctext(img,W/2,GY0+ROWS*CW//2-90,str(n),F(int(180*sc)),(255,214,60),10)
    else:
        img.alpha_composite(BOARD)
        # countdown bar
        bx0,bx1,by=GX0,GX0+COLS*CW,460
        rem=max(0,min(1,(T_UP-t)/5.0))
        d.rounded_rectangle([bx0-6,by-6,bx1+6,by+56],radius=16,fill=(20,15,35))
        col=(110,220,110) if rem>0.5 else ((255,200,60) if rem>0.2 else (240,70,60))
        if rem>0: d.rounded_rectangle([bx0,by,bx0+int((bx1-bx0)*rem),by+50],radius=12,fill=col)
        secs=math.ceil((T_UP-t)) if t<T_UP else 0
        tw=d.textlength(str(secs),font=F(36)); d.text((W/2-tw/2,by+8),str(secs),font=F(36),fill=(255,255,255),stroke_width=5,stroke_fill=(20,15,35))
        if t>=T_UP:
            u=t-T_UP
            cx,cy=CENT[ODD_RC]
            if False:
                v=min(1,(u-0.5)/0.3); r=int(78+30*(1-v)+4*math.sin(t*8))
                for wdt,colr in ((16,(20,15,35)),(10,(255,60,60))):
                    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=colr,width=wdt)
            if u<1.2: ctext(img,W/2,GY0+ROWS*CW+60,"TIME'S UP!",F(60),(255,90,80))
            else: ctext(img,W/2,GY0+ROWS*CW+60,'Comment where it is',F(42))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (30,100,200,250,300): img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done')
