import numpy as np, subprocess, math, random, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from sim import run, SHAPES, PED_Y, PED_L, PED_R
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=13.5; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
seq=['ACV','CREATINE','MUSHROOM','MELATONIN','ACV','MUSHROOM','CREATINE','MELATONIN']
times=[0.6,1.5,2.4,3.3,4.2,5.1,6.0,6.9]; HOLD=1.8; REL=times[7]+HOLD
d=9; offs=[k*d for k in range(7)]+[6*d+40]
out=run(seq,offs,times,7,HOLD,DUR=DUR,fv=1200,fm=1.6)
# landing / crash times for thuds
thuds=[]
for i in range(8):
    prev=None
    for f in range(1,len(out)):
        a,b=out[f-1][i],out[f][i]
        if a is None or b is None: continue
        vy=(b[1]-a[1])*FPS
        if prev is not None and prev>350 and vy<prev*0.4: thuds.append(round(f/FPS,3))
        prev=vy
crash=[]
for i in range(8):
    ff_=next((f for f in range(len(out)) if out[f][i] and out[f][i][1]>PED_Y+60 and f/FPS>REL),None)
    if ff_: crash.append(round(ff_/FPS,3))
thuds+=crash
f1=next(f for f in range(int(times[0]*FPS)+2,len(out)) if out[f][0] and abs(out[f][0][1]-out[f-1][0][1])<1.5); thuds.append(round(f1/FPS,3))
json.dump(sorted(thuds),open('thuds.json','w')); print('thuds',sorted(thuds))
COLLAPSE=next(f/FPS for f in range(int(REL*FPS),len(out)) if max(abs(math.degrees(p[2])) for p in out[f][:7])>8)
print('collapse',COLLAPSE)
g=Image.open(A+'recov_hd.gif'); BGF=[]
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB'); s=H/f.height; f=f.resize((int(f.width*s),H),Image.LANCZOS); ox=(f.width-W)//2
    BGF.append(ImageEnhance.Brightness(f.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(10))).enhance(0.6).convert('RGBA'))
# stone pedestal + floor, pixel art
P=6
def stone(w,h):
    c=Image.new('RGBA',(w//P,h//P),(0,0,0,0)); dd=ImageDraw.Draw(c); ww,hh=c.size
    dd.rectangle([0,0,ww-1,hh-1],fill=(40,36,52)); dd.rectangle([1,1,ww-2,hh-2],fill=(132,128,150))
    for y in range(3,hh,6):
        for x in range(1-(y//6)%2*4,ww,8): dd.rectangle([x,y,x+7,y+5],outline=(96,92,112))
    dd.rectangle([1,1,ww-2,2],fill=(176,172,196))
    return c.resize((w,h),Image.NEAREST)
PED=stone(PED_R-PED_L+24,1880-PED_Y+6)
FLOOR=stone(W+12,H-1880+12)
IMG={n:SHAPES[n][0] for n in SHAPES}
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    dd=ImageDraw.Draw(img); w=dd.textlength(t,font=f); dd.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
def sway(t):
    if t<times[7] or t>=REL: return 0.0
    e=min(1,(t-times[7])/0.5)*min(1,(REL-t)/0.3)
    return 1.3*e*math.sin(2*math.pi*1.4*(t-times[7]))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGF[int(t*5)%len(BGF)].copy()
    img.alpha_composite(FLOOR,(-6,1880)); img.alpha_composite(PED,(PED_L-12,PED_Y))
    fr=out[min(f,len(out)-1)]
    sa=math.radians(sway(t))
    for i,p in enumerate(fr):
        if p is None: continue
        x,y,a=p
        if i<7 and sa:
            dx,dy=x-540,y-PED_Y; x=540+dx*math.cos(sa)-dy*math.sin(sa); y=PED_Y+dx*math.sin(sa)+dy*math.cos(sa); a+=sa
        if i==7 and t<REL: y+=6*math.sin(t*9)   # hovering jitter
        im=IMG[seq[i]].rotate(-math.degrees(a),resample=Image.BICUBIC,expand=True)
        img.alpha_composite(im,(int(x-im.width/2),int(y-im.height/2)))
        # name tag while it drops in
        if i<7 and times[i]<=t<times[i]+0.9:
            ctext(img,x,int(y-im.height/2-60),f'#{i+1} {seq[i]}',F(36),(255,214,60),5)
        if i==7 and t>=times[7] and t<REL+0.5:
            ctext(img,x,int(y-im.height/2-60),f'#8 {seq[i]}',F(36),(255,214,60),5)
    ctext(img,W/2,150,'WHICH GUMMY',F(76)); ctext(img,W/2,250,'MAKES IT FALL?',F(64),(255,214,60))
    if times[7]<=t<REL:
        ctext(img,W/2,1730,'Comment your guess',F(46))
    if t>=COLLAPSE+0.5:
        u=t-(COLLAPSE+0.5); sc=1+0.35*max(0,1-u/0.25)
        ctext(img,W/2,760,'TIMBER!',F(int(110*sc)),(255,90,70),9)
        if u>0.8: ctext(img,W/2,900,'Did you guess right?',F(44))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%30==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done')
