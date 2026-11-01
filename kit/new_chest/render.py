import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
def gif(p,h,flip=False):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    fr=[f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
    return [f.transpose(Image.FLIP_LEFT_RIGHT) for f in fr] if flip else fr
rng=random.Random(4)
# backgrounds
def bg(p,blur,bright):
    g=Image.open(A+p); out=[]
    for i in range(0,g.n_frames,2):
        g.seek(i); f=g.convert('RGB'); s=H/f.height; f=f.resize((int(f.width*s),H),Image.NEAREST if not blur else Image.LANCZOS); ox=(f.width-W)//2
        f=f.crop((ox,0,ox+W,H))
        if blur: f=f.filter(ImageFilter.GaussianBlur(blur))
        out.append(ImageEnhance.Brightness(f).enhance(bright).convert('RGBA'))
    return out
BG_PICK=bg('vit_hd.gif',12,0.45)
BG_FIGHT=bg('vit_hd.gif',0,0.7)
CH=340
IDLE=gif('idle_8.gif',CH); SIDE=gif('cyrus-walk-side.gif',CH); VIC=gif('vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif',int(CH*1.08))
DRAG=gif('dragon.gif',540,flip=True)
DW=DRAG[0].width
FLOOR=1560; DX=W-DW+110   # dragon left edge
MOUTH=(DX+int(DW*0.24),FLOOR-540+int(540*0.24))
GUM=Image.open('../gummy/mush_gummy_single.png').convert('RGBA'); GUM=GUM.crop(GUM.getbbox())
def thumb(im,w): return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
GUM_BIG=thumb(GUM,190); GUM_S=thumb(GUM,90)
P=10
# ---------- pixel art: chest, stick, shield
def chest_parts():
    body=Image.new('RGBA',(26,13),(0,0,0,0)); d=ImageDraw.Draw(body)
    d.rectangle([0,0,25,12],fill=(40,22,12)); d.rectangle([1,0,24,11],fill=(140,82,38))
    for y in (3,7): d.line([(1,y),(24,y)],fill=(110,62,28))
    d.rectangle([3,0,5,11],fill=(90,90,105)); d.rectangle([20,0,22,11],fill=(90,90,105))
    d.rectangle([11,0,14,4],fill=(232,182,76)); d.rectangle([12,2,13,3],fill=(60,40,20))
    lid=Image.new('RGBA',(26,9),(0,0,0,0)); d=ImageDraw.Draw(lid)
    d.rounded_rectangle([0,0,25,8],radius=3,fill=(40,22,12)); d.rounded_rectangle([1,1,24,8],radius=3,fill=(160,96,44))
    d.line([(2,4),(23,4)],fill=(120,70,32)); d.rectangle([3,1,5,8],fill=(110,110,128)); d.rectangle([20,1,22,8],fill=(110,110,128))
    d.rectangle([11,6,14,8],fill=(232,182,76))
    inside=Image.new('RGBA',(26,9),(0,0,0,0)); d=ImageDraw.Draw(inside)
    d.rounded_rectangle([0,0,25,8],radius=3,fill=(40,22,12)); d.rounded_rectangle([1,0,24,7],radius=3,fill=(70,40,20))
    up=lambda im: im.resize((im.width*12,im.height*12),Image.NEAREST)
    return up(body),up(lid),up(inside)
BODY,LID,INSIDE=chest_parts()
def stick():
    c=Image.new('RGBA',(6,30),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rectangle([1,0,4,29],fill=(60,36,16)); d.rectangle([2,0,3,29],fill=(150,98,48)); d.point((2,8),fill=(90,56,24)); d.point((3,19),fill=(90,56,24))
    d.rectangle([4,11,5,12],fill=(60,36,16)); d.point((5,10),fill=(90,170,60))
    return c.resize((6*P,30*P),Image.NEAREST)
def shield():
    c=Image.new('RGBA',(22,26),(0,0,0,0)); d=ImageDraw.Draw(c)
    poly=[(1,1),(20,1),(20,13),(11,24),(1,13)]
    d.polygon(poly,fill=(40,30,40)); d.polygon([(2,2),(19,2),(19,13),(11,22),(2,13)],fill=(232,182,76))
    d.polygon([(4,4),(17,4),(17,12),(11,19),(4,12)],fill=(217,122,31))
    d.rectangle([10,6,11,15],fill=(255,230,150)); d.rectangle([7,9,14,10],fill=(255,230,150))
    return c.resize((22*P,26*P),Image.NEAREST)
STICK=stick(); SHIELD=shield()
ITEMS=[('WOODEN STICK',STICK.rotate(-35,expand=True,resample=Image.NEAREST)),('SHIELD',SHIELD),('ENERGY GUMMY',GUM_BIG)]
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
def draw_chest(img,cx,by,openu,t,dim=False,label=None):
    # by = bottom of chest; openu 0 closed -> 1 open
    bx=cx-BODY.width//2; img_body=BODY
    if openu>0:
        # light rays behind
        ray=Image.new('RGBA',(700,700),(0,0,0,0)); rd=ImageDraw.Draw(ray)
        for k in range(10):
            a=k*math.pi/9+math.pi; a0=a-0.06; a1=a+0.06
            rd.polygon([(350,350),(350+350*math.cos(a0),350+350*math.sin(a0)),(350+350*math.cos(a1),350+350*math.sin(a1))],fill=(255,230,140,int(90*openu)))
        ray=ray.filter(ImageFilter.GaussianBlur(6)); ray=ray.rotate(math.sin(t*2)*8)
        img.alpha_composite(ray,(cx-350,by-BODY.height-350))
        ins=INSIDE; img.alpha_composite(ins,(bx,by-BODY.height-ins.height+20))
        lh=int(LID.height*(1-openu*0.6)); lid=LID.resize((LID.width,max(4,lh)),Image.NEAREST)
        img.alpha_composite(lid,(bx,by-BODY.height-ins.height+20-lid.height-int(30*openu)))
    else:
        img.alpha_composite(LID,(bx,by-BODY.height-LID.height+10))
    img.alpha_composite(img_body,(bx,by-BODY.height))
    if label: ctext(img,cx,by+30,label,F(70),(255,214,60),8)
    if dim:
        sh=Image.new('RGBA',(BODY.width+20,BODY.height+LID.height+40),(10,8,20,150)); img.alpha_composite(sh,(bx-10,by-BODY.height-LID.height-20))
# ---------- timeline
T_HOOK=3.0
SEG=[(3.0,7.8),(7.8,12.4),(12.4,18.6)]
DUR=19.6; N=int(DUR*FPS)
CXS=[190,540,890]
fire=[]
def fire_layer(t,t0,t1,stop_x=None,rate=4,target=(300,1400)):
    lay=Image.new('RGBA',(W//P,H//P),(0,0,0,0)); d=ImageDraw.Draw(lay)
    rr=random.Random(int(t0*100))
    for k in range(int((t1-t0)*60)):
        st=t0+k/60; age=t-st
        if age<0 or age>0.9: continue
        vx=-(900+rr.uniform(-150,150)); vy=(target[1]-MOUTH[1])*900/max(50,MOUTH[0]-target[0])+rr.uniform(-110,110)
        x=MOUTH[0]+vx*age; y=MOUTH[1]+vy*age
        if stop_x is not None and x<stop_x:
            ty=MOUTH[1]+(target[1]-MOUTH[1])*(MOUTH[0]-stop_x)/max(50,MOUTH[0]-target[0]); over=(stop_x-x)/900; x=stop_x+30+over*300; y=ty+(1 if rr.random()<0.5 else -1)*(40+over*420)
        r=(22+95*age)/P; col=(255,240,120) if age<0.15 else (255,160,40) if age<0.4 else (220,60,30)
        al=int(255*max(0,1-age/0.9))
        d.ellipse([x/P-r,y/P-r,x/P+r,y/P+r],fill=col+(al,))
    return lay.resize((W,H),Image.NEAREST)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS
    seg=next((i for i,(a,b) in enumerate(SEG) if a<=t<b),None)
    if t<T_HOOK:
        img=BG_PICK[int(t*5)%len(BG_PICK)].copy()
        ctext(img,W/2,300,'PICK A',F(96)); ctext(img,W/2,420,'CHEST',F(96),(255,214,60))
        for k,cx in enumerate(CXS):
            sh=int(6*math.sin(t*20+k)) if t>2.2 else 0
            draw_chest(img,cx+sh,1150,0,t,label=str(k+1))
        fr=IDLE[int(t*8)%len(IDLE)]; img.alpha_composite(fr,(int(W/2-fr.width/2),1640-fr.height))
        ctext(img,W/2,1720,'Comment your number',F(42))
    elif t>=SEG[2][1]:
        # outro: all three shown
        img=BG_PICK[int(t*5)%len(BG_PICK)].copy()
        ctext(img,W/2,300,'WHICH ONE',F(80)); ctext(img,W/2,410,'DID YOU PICK?',F(72),(255,214,60))
        for k,cx in enumerate(CXS):
            draw_chest(img,cx,1300,1,t,label=str(k+1))
            nm,it=ITEMS[k]; s=thumb(it,int(it.width*0.85)) if k<2 else thumb(GUM,150)
            img.alpha_composite(s,(int(cx-s.width/2),int(980-s.height+8*math.sin(t*3+k))))
    else:
        a,b=SEG[seg]; u=t-a
        if u<1.6:
            # open this chest
            img=BG_PICK[int(t*5)%len(BG_PICK)].copy()
            ctext(img,W/2,300,f'CHEST {seg+1}',F(96),(255,214,60))
            op=min(1,max(0,(u-0.2)/0.3))
            draw_chest(img,540,1350,op,t)
            if u>0.45:
                nm,it=ITEMS[seg]; v=min(1,(u-0.45)/0.35); e=1-(1-v)**3
                s=it.resize((max(1,int(it.width*e)),max(1,int(it.height*e))),Image.NEAREST if seg<2 else Image.LANCZOS)
                img.alpha_composite(s,(int(540-s.width/2),int(1100-260*e-s.height/2+8*math.sin(t*4))))
                ctext(img,W/2,1480,nm,F(56),(255,255,255))
        else:
            # fight cut
            v=u-1.6; img=BG_FIGHT[int(t*5)%len(BG_FIGHT)].copy()
            ctext(img,W/2,230,f'CHEST {seg+1}: ' + ['STICK','SHIELD','ENERGY GUMMY'][seg],F(50),(255,214,60))
            dfr=DRAG[int(t*6)%len(DRAG)]; dragon_xy=[DX,FLOOR-dfr.height]
            cy_x=200; cfr=IDLE[int(t*8)%len(IDLE)]; rot=0; show_c=True; extra=[]
            if seg==0:
                if v<0.9: cfr=SIDE[int(t*10)%len(SIDE)]; cy_x=200+int(220*v/0.9)
                else: cy_x=420
                if 0.9<=v<1.2: ctext(img,cy_x+150,FLOOR-CH-140,'*tap*',F(40))
                if v>=1.25:
                    w_=v-1.25
                    img.alpha_composite(fire_layer(t,a+1.6+1.25,a+1.6+1.75,target=(420,FLOOR-CH/2)))
                    if w_>0.25:
                        q=w_-0.25; cy_x=420-int(900*q); rot=int(720*q); lift=int(1400*q-1200*q*q)
                        extra=['launch',lift]
                        if q<1.2: ctext(img,W/2,700,'LAUNCHED!',F(80),(255,90,80),8)
                if v<1.25 or (extra and extra[1]<2000):
                    pass
            elif seg==1:
                cy_x=240-int(30*min(1,max(0,v-0.4)/2.0))
                if v>=0.3: img.alpha_composite(fire_layer(t,a+1.6+0.3,a+1.6+2.8,stop_x=cy_x+250,target=(cy_x+170,FLOOR-CH+190)))
                if v>1.0: ctext(img,W/2,700,'STALEMATE...',F(70),(255,255,255),8)
            else:
                if v<0.6:
                    q=v/0.6; gx=int(560-(560-(cy_x+40))*q); gy=int(900+(FLOOR-CH*0.8-900)*q)
                    s=thumb(GUM,int(150-80*q)); img.alpha_composite(s,(gx-s.width//2,gy-s.height//2))
                if v>=0.6:
                    glow=Image.new('RGBA',(520,620),(0,0,0,0)); ImageDraw.Draw(glow).ellipse([0,0,519,619],fill=(255,220,90,int(120+60*math.sin(t*12))))
                    glow=glow.filter(ImageFilter.GaussianBlur(30)); extra=['glow',glow]
                    if v<1.5: ctext(img,W/2,700,'POWERED UP!',F(76),(255,214,60),8)
                if 1.3<=v<1.7:
                    q=(v-1.3)/0.4; cy_x=200+int(420*q); cfr=SIDE[int(t*14)%len(SIDE)]
                if v>=1.7: cy_x=620
                if v>=1.65:
                    q=v-1.65; dragon_xy=[DX+int(700*q),FLOOR-dfr.height-int(1500*q)]
                    dfr=dfr.rotate(-int(300*q),expand=True,resample=Image.NEAREST)
                    if q<0.15: img=Image.blend(img,Image.new('RGBA',(W,H),(255,255,255,255)),0.7*(1-q/0.15))
                if v>=2.3:
                    cfr=VIC[int(t*8)%len(VIC)]; cy_x=540
                    ctext(img,W/2,700,'VICTORY!',F(96),(255,214,60),9)
            if dragon_xy[1]>-dfr.height: img.alpha_composite(dfr,(dragon_xy[0],dragon_xy[1]))
            if extra and extra[0]=='glow': img.alpha_composite(extra[1],(int(cy_x-260),int(FLOOR-CH-140)))
            if extra and extra[0]=='launch':
                s=cfr.rotate(extra[2] if len(extra)>2 else rot,expand=True,resample=Image.NEAREST)
                img.alpha_composite(s,(int(cy_x-s.width/2),int(FLOOR-CH/2-extra[1]-s.height/2)))
            else:
                img.alpha_composite(cfr,(int(cy_x-cfr.width/2),FLOOR-cfr.height))
                if seg==0 and v<1.5:
                    st=STICK.rotate(-60 if 0.9<=v<1.2 else -20,expand=True,resample=Image.NEAREST); img.alpha_composite(st,(int(cy_x+40),FLOOR-CH+40))
                if seg==1: img.alpha_composite(SHIELD,(int(cy_x+60),FLOOR-CH+60))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%30==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done',DUR)
