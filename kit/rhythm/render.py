import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=27.6; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
# --- beat chart (timed off the reference: stomp, stomp, clap every 1.342s)
import json as _j
_c=_j.load(open('chart_new.json')); STOMP=_c['stomp']; CLAP=_c['clap']; END=_c['end']
# --- stage: Sun Temple, light dim + spotlight cones + floor shade
g=Image.open(A+'scene_sun.png').convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
g=g.crop((ox,0,ox+W,H)); g=g.filter(ImageFilter.GaussianBlur(2)); g=ImageEnhance.Brightness(g).enhance(0.78).convert('RGBA')
cones=Image.new('RGBA',(W,H),(0,0,0,0)); cd=ImageDraw.Draw(cones)
for cx in (150,410,670,930):
    cd.polygon([(cx-25,40),(cx+25,40),(cx+150,900),(cx-150,900)],fill=(255,240,190,26))
    cd.ellipse([cx-16,24,cx+16,56],fill=(255,240,200,230))
g.alpha_composite(cones.filter(ImageFilter.GaussianBlur(5)))
fl=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(fl).rectangle([0,1330,W,H],fill=(40,20,50,120)); g.alpha_composite(fl)
STAGE=g
# --- pixel icons
BOOT=["XXXXXX.......","XXXXXX.......","XXXXXX.......","XXXXXX.......","XXXXXX.......","XXXXXXX......","XXXXXXXXXX...","XXXXXXXXXXXX.","XXXXXXXXXXXXX","XXXXXXXXXXXXX","XXXXXXXXXXXXX","SSSSSSSSSSSSS","SSSSSSSSSSSSS"]
HAND=["..X.X.......X.X..",".XX.XX.X..XXXX.X.",".XXXXXXX.XXXXXXX.",".XXXXXXX.XXXXXXX.",".XXXXXXX.XXXXXXX.","XXXXXXXX.XXXXXXXX","XXXXXXX...XXXXXXX",".XXXXXX...XXXXXX.","..XXXXX...XXXXX..","...XXX.....XXX..."]
def icon(rows,col,px=8):
    h=len(rows); w=max(len(r) for r in rows); im=Image.new('RGBA',(w*px,h*px),(0,0,0,0)); d=ImageDraw.Draw(im)
    for y,r in enumerate(rows):
        for x,c in enumerate(r):
            if c=='S': d.rectangle([x*px,y*px,x*px+px-1,y*px+px-1],fill=tuple(int(v*0.6) for v in col))
            if c=='X': d.rectangle([x*px,y*px,x*px+px-1,y*px+py-1] if False else [x*px,y*px,x*px+px-1,y*px+px-1],fill=col)
    return im
RED=(232,87,78); BLUE=(126,132,232)
IB=icon(BOOT,RED,8); IH=icon(HAND,BLUE,7)
LX,RX,BY,BR=270,810,1480,98
def button(img,cx,ic,pressed,burst):
    d=ImageDraw.Draw(img)
    fill=(205,205,210) if pressed else (255,255,255)
    if burst>0:
        r1,r2=BR+10,BR+10+int(70*burst)
        for k in range(10):
            a=k*math.pi*2/10
            d.polygon([(cx+r1*math.cos(a-0.12),BY+r1*math.sin(a-0.12)),(cx+r2*math.cos(a),BY+r2*math.sin(a)),(cx+r1*math.cos(a+0.12),BY+r1*math.sin(a+0.12))],fill=(255,255,255,int(220*burst)))
    d.ellipse([cx-BR,BY-BR,cx+BR,BY+BR],fill=fill,outline=(60,40,70),width=6)
    i=ic if not pressed else Image.blend(ic,Image.new('RGBA',ic.size,(120,110,120,0)),0.45)
    img.alpha_composite(i,(cx-ic.width//2,BY-ic.height//2+(6 if pressed else 0)))
# --- characters
def gif(path):
    im=Image.open(A+path); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    return [f.crop(bb) for f in fr], im.info.get('duration',100)
def sc(fr,h):
    k=h/fr[0].height; return [f.resize((int(f.width*k),int(f.height*k)),Image.NEAREST) for f in fr]
CY_IDLE,dI=gif('idle_8.gif'); CY_VIC,dV=gif('vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif')
CY_IDLE=sc(CY_IDLE,470); CY_VIC=sc(CY_VIC,505)
JOY,dJ=gif('idle_5.gif'); JOY=sc(JOY,300)
CLE,dC=gif('idle_7.gif'); CLE=sc(CLE,300)
def mic(img,x,y):
    d=ImageDraw.Draw(img)
    d.rectangle([x-5,y,x+5,y+260],fill=(30,30,36)); d.rectangle([x-50,y+255,x+50,y+268],fill=(30,30,36))
    d.rounded_rectangle([x-22,y-60,x+22,y+6],radius=18,fill=(45,45,55),outline=(15,15,20),width=4)
    for k in range(3): d.line([x-18,y-44+k*14,x+18,y-44+k*14],fill=(90,90,100),width=3)
def last_hit(ts,t):
    p=[x for x in ts if x<=t]; return t-p[-1] if p else 99
def ctext(img,y,t,f,fill,stroke=(40,20,40)):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill,stroke_width=5,stroke_fill=stroke)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
FALL=1.6; SPEED=(BY+120)/FALL
spark=random.Random(3)
for f in range(N):
    t=f/FPS; img=STAGE.copy()
    # lane glow during the intro, like the reference
    if t<3.0:
        lane=Image.new('RGBA',(W,H),(0,0,0,0)); ld=ImageDraw.Draw(lane); a=int(90*(1-t/3.0))
        ld.rectangle([LX-38,0,LX+38,H],fill=RED+(a,)); ld.rectangle([RX-38,0,RX+38,H],fill=BLUE+(a,)); img.alpha_composite(lane)
    # performer: Cyrus slides in after the countdown and pumps on every clap
    CXc,CYfeet=555,1290
    if t>=3.6:
        enter=min(1,(t-3.6)/0.8); x=int(-300+(CXc+300)*(1-(1-enter)**3)); hop=int(abs(math.sin(t*math.pi/0.335))*18) if enter<1 else 0
        dc=last_hit(CLAP,t); ds=last_hit(STOMP,t)
        if t>END+0.2: spr=CY_VIC[int(t*1000/dV)%len(CY_VIC)]
        elif enter>=1 and dc<0.25: spr=CY_VIC[1%len(CY_VIC)]
        else: spr=CY_IDLE[int(t*1000/dI)%len(CY_IDLE)]
        bounce=int(14*max(0,1-ds/0.15)) if enter>=1 and t<END+0.2 else 0
        img.alpha_composite(spr,(x-spr.width//2,CYfeet-spr.height+bounce-hop))
    mic(img,CXc+10,1040)
    # falling notes
    nl=Image.new('RGBA',(W,H),(0,0,0,0)); nd=ImageDraw.Draw(nl)
    for ts,cx,col,hgt in ((STOMP,LX,RED,96),(CLAP,RX,BLUE,170)):
        for th in ts:
            dt=th-t
            if -0.05<dt<FALL:
                y=BY-dt*SPEED
                nd.rounded_rectangle([cx-48,y-hgt,cx+48,y],radius=6,fill=col+(215,),outline=tuple(min(255,c+60) for c in col)+(255,),width=4)
    img.alpha_composite(nl)
    # lane reactors bounce when their beat lands
    for spr_set,cx,ts,d_ in ((JOY,LX-150,STOMP,dJ),(CLE,RX+150,CLAP,dC)):
        dh=last_hit(ts,t); jump=int(60*math.sin(min(1,dh/0.28)*math.pi)) if dh<0.28 else 0
        sp=spr_set[int(t*1000/d_)%len(spr_set)]; img.alpha_composite(sp,(cx-sp.width//2,BY-BR-sp.height+40-jump))
    ds=last_hit(STOMP,t); dc=last_hit(CLAP,t)
    button(img,LX,IB,ds<0.18,max(0,1-ds/0.22) if ds<0.22 else 0)
    button(img,RX,IH,dc<0.18,max(0,1-dc/0.22) if dc<0.22 else 0)
    if t<4.0: ctext(img,560,'play along',F(54),(255,255,255)); ctext(img,640,'with the beat!',F(54),(255,255,255))
    if t<2.68: ctext(img,760,str(4-int(t/0.67)),F(110),(255,90,80),(255,255,255))
    if t>END+0.15:
        e=min(1,(t-END-0.15)/0.25); fb=F(int(40+50*e)); ctext(img,600,'BRAVO!!',fb,(255,214,90))
        d=ImageDraw.Draw(img)
        for _ in range(14):
            x=spark.randint(220,860); y=spark.randint(520,760); r=spark.randint(4,12)
            d.polygon([(x,y-r*2),(x+r//2,y),(x,y+r*2),(x-r//2,y)],fill=(255,255,220,220)); d.polygon([(x-r*2,y),(x,y-r//2),(x+r*2,y),(x,y+r//2)],fill=(255,255,220,220))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (30,150,300,800): img.convert('RGB').resize((540,960)).save(f'prev_{f}.png')
ff.stdin.close(); ff.wait()
import json; print('done',END)
