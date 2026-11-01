import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; T=10.0; INTRO=2.4; REVEAL=2.5; N=int((INTRO+T+REVEAL)*FPS)
def F(s): return ImageFont.truetype(FONT,s)
hub=Image.open(A+'sun_hd.gif'); FR=[]
for i in range(hub.n_frames): hub.seek(i); FR.append(np.array(hub.convert('RGB')))
def edit(a):
    a=a.copy()
    # 1) right base window filled in with the wall colour next to it
    a[553:614,1312:1352]=a[553:614,1272:1312]
    # 2) left roof turret removed: sky copied from just left of it
    a[136:202,520:580]=a[136:202,455:515]
    # 3) right inner column turned red
    c=a[250:500,1145:1205].astype(int); c[...,1]=(c[...,1]*0.62).astype(int); c[...,2]=(c[...,2]*0.7).astype(int); a[250:500,1145:1205]=c.clip(0,255).astype(np.uint8)
    return a
CROP=(240,0,1680,1080); PW,PH=900,675
def panel(a): return Image.fromarray(a).crop(CROP).resize((PW,PH),Image.NEAREST)
TOPS=[panel(f) for f in FR]; BOTS=[panel(edit(f)) for f in FR]
bgsrc=Image.open(A+'recov_hd.gif'); bgsrc.seek(0); g=bgsrc.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.55).convert('RGBA')
d=ImageDraw.Draw(BG)
for yy,t,f,c in ((140,'Find 3 differences',F(48),(255,255,255)),(210,'in 10 seconds',F(48),(255,255,255)),(280,"or you're an NPC",F(40),(255,214,90))):
    w=d.textlength(t,font=f); d.text(((W-w)/2,yy),t,font=f,fill=c,stroke_width=6,stroke_fill=(20,15,35))
X=(W-PW)//2; Y1=360; Y2=Y1+PH+30
for y in (Y1,Y2): d.rectangle([X-8,y-8,X+PW+7,y+PH+7],fill=(201,162,74))
ANS=[(1030,420,1185,478),(1025,250,1115,365),(518,202,596,272)]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for fn in range(N):
    k=int(fn/FPS*1000/hub.info.get('duration',100))%len(FR)
    img=BG.copy(); img.paste(TOPS[k],(X,Y1)); img.paste(BOTS[k],(X,Y2))
    t=fn/FPS-INTRO; dd=ImageDraw.Draw(img)
    if t<0:
        ti=fn/FPS; k_=int(ti/0.6); lab=['3','2','1','GO!'][min(k_,3)]; u=(ti-k_*0.6)/0.6
        if lab!='GO!':
            sh=Image.new('RGBA',(PW,PH*2+30),(10,6,24,200)); img.alpha_composite(sh,(X,Y1))
        fz=int(260*(1.25-0.25*u)) if lab!='GO!' else int(200*(1.25-0.25*u)); fb=F(fz); w=dd.textlength(lab,font=fb)
        dd.text(((W-w)/2,Y1+PH+15-fz//2),lab,font=fb,fill=(255,214,90) if lab!='GO!' else (110,220,90),stroke_width=10,stroke_fill=(20,15,35))
        t=0.0
    # countdown bar under the panels
    by=Y2+PH+40; dd.rectangle([X-8,by,X+PW+7,by+80],fill=(24,20,44),outline=(201,162,74),width=5)
    left=max(0.0,1-t/T); col=(110,200,90) if left>0.5 else ((255,200,60) if left>0.2 else (235,70,60))
    if left>0: dd.rectangle([X+4,by+10,X+4+int((PW-8)*left),by+70],fill=col)
    sec=max(0,int(math.ceil(T-t))); fs=F(44); st=f'{sec}' if t<T else "TIME'S UP"
    w=dd.textlength(st,font=fs); dd.text(((W-w)/2,by+18),st,font=fs,fill=(255,255,255),stroke_width=6,stroke_fill=(20,15,35))
    if False:
        for b in ANS:
            for (yy) in (Y2,):
                x0=X+(b[0]-400)*PW/1440-18; x1=X+(b[2]-400)*PW/1440+18; y0=yy+b[1]*PH/1080-18; y1=yy+b[3]*PH/1080+18
                dd.ellipse([x0,y0,x1,y1],outline=(255,40,40),width=7)
    ff.stdin.write(img.convert('RGB').tobytes())
    if fn in (10,80,200,420): img.convert('RGB').resize((360,640)).save(f't_{fn}.png')
ff.stdin.close(); ff.wait()
print('done')
