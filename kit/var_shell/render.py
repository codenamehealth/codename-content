import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=14.4; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
rng=random.Random(21)
th=Image.open(A+'vit_hd.gif'); th.seek(0); g=th.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2-150
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.75).convert('RGBA')
im=Image.open(A+'idle_7.gif'); HF=[]
for i in range(im.n_frames): im.seek(i); HF.append(im.convert('RGBA'))
bb=None
for f in HF:
    b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
HH=330; HF=[f.crop(bb) for f in HF]; HF=[f.resize((int(f.width*HH/f.height),HH),Image.NEAREST) for f in HF]
GUM=Image.open('../gummy/mel_gummy_red.png'); GUM=GUM.resize((120,int(GUM.height*120/GUM.width)),Image.LANCZOS)
FLOOR=1250; SLOTS=[(250,FLOOR),(540,FLOOR),(830,FLOOR)]
EXTRA=[(250,FLOOR),(540,FLOOR),(830,FLOOR),(395,FLOOR-230),(685,FLOOR-230),(540,FLOOR-430),(250,FLOOR-430),(830,FLOOR-430),(395,FLOOR+170),(685,FLOOR+170)]
# formations: each step every 0.45s from 1.6s to 9.6s
T0,T1,STEP=1.6,9.6,0.45
steps=int((T1-T0)/STEP)
forms=[[SLOTS[0],SLOTS[1],SLOTS[2]]]
for k in range(steps-1):
    pts=rng.sample(EXTRA,3); forms.append(pts)
final=[SLOTS[0],SLOTS[1],SLOTS[2]]; order=[0,1,2]; rng.shuffle(order)
while order[2]!=1: rng.shuffle(order)   # gummy keeper (hollow 1) ends at B
forms.append([final[order.index(i)] for i in range(3)])
def place(t):
    if t<T0: return [SLOTS[0],SLOTS[1],SLOTS[2]],[0,0,0]
    if t>=T0+steps*STEP: return forms[-1],[0,0,0]
    k=int((t-T0)/STEP); u=((t-T0)-k*STEP)/STEP; e=u*u*(3-2*u)
    a,b=forms[k],forms[min(k+1,len(forms)-1)]
    return [(a[i][0]+(b[i][0]-a[i][0])*e, a[i][1]+(b[i][1]-a[i][1])*e) for i in range(3)],[math.sin(e*math.pi)*70]*3
def ctext(img,y,t,f,fill=(255,255,255)):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill,stroke_width=6,stroke_fill=(20,15,35))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BG.copy()
    P,hop=place(t); fr=HF[int(t*10)%len(HF)]
    lift=[0,0,0]
    if t<1.0: lift[1]=260
    elif t<1.5: lift[1]=int(260*(1-(t-1.0)/0.5)**2)
    if t>=12.3: lift[1]=int(260*min(1,(t-12.3)/0.4))
    showg = t<1.5 or t>=12.3
    if showg: gs=SLOTS[1] if t<1.5 else SLOTS[2]; img.alpha_composite(GUM,(gs[0]-GUM.width//2,FLOOR-GUM.height-6))
    for i in sorted(range(3),key=lambda i:P[i][1]):
        x,y=P[i]; y=y-hop[i]-lift[i]
        img.alpha_composite(fr,(int(x-fr.width/2),int(y-fr.height)))
    if t<1.6: ctext(img,300,'Remember the gummy',F(46))
    elif t<9.8: ctext(img,300,'Watch carefully!!',F(54))
    elif t<12.3: ctext(img,300,'Where is the gummy?',F(48))
    else: ctext(img,300,'Comment your answer',F(46))
    if t>=9.8:
        for lab,(x,_) in zip('ABC',SLOTS): ctext_x=x; d=ImageDraw.Draw(img); w=d.textlength(lab,font=F(60)); d.text((x-w/2,FLOOR+40),lab,font=F(60),fill=(255,214,90),stroke_width=6,stroke_fill=(20,15,35))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (15,100,330,375,420): img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done',steps)
