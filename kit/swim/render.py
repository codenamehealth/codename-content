import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=22.6; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
P=6; rng=random.Random(3)
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
SH=300
RAC=[('JOY','idle_5.gif'),('CLEO','idle_7.gif'),('CYRUS','idle_8.gif'),('RAYLEIGH','idle_6.gif')]
SPR=[gif(p,SH) for _,p in RAC]
HOL=gif('idle_9.gif',SH)
GUM=Image.open('../gummy/mush_gummy_single.png'); GUM=GUM.resize((110,int(GUM.height*110/GUM.width)),Image.LANCZOS)
LANE_Y=[650,910,1170,1430]   # lane centre (waterline)
LANE_H=260
FIN=6000; DECK=300
# --- water texture (tileable, pixel art)
TW,TH=1080//P,H//P
wt=Image.new('RGB',(TW,TH),(78,160,222)); d=ImageDraw.Draw(wt)
for _ in range(220):
    x=rng.randrange(TW); y=rng.randrange(TH); w=rng.randint(4,12)
    for dx in (-TW,0,TW): d.line([(x+dx,y),(x+dx+w,y)],fill=(120,195,240)); d.line([(x+dx+2,y+1),(x+dx+w-2,y+1)],fill=(150,212,246))
WATER=wt.resize((1080,H),Image.NEAREST)
def rope(img,y,cam):
    d=ImageDraw.Draw(img); off=int(cam)%36
    for x in range(-off,W+36,36):
        k=((x+int(cam))//36)%2
        d.rectangle([x,y-9,x+24,y+9],fill=(30,20,40)); d.rectangle([x+3,y-6,x+21,y+6],fill=(232,60,70) if k else (250,245,240))
# --- race plan (t, x): piecewise-linear keyframes
KF={
 1:[(3.7,330),(7,1700),(10,2900),(13,4000),(16,5100),(18.0,5700),(18.5,6000)],                      # Cleo leads most of the way
 0:[(3.7,330),(7,1550),(10,2650),(12.9,3550),(13.5,3580),(14.0,3800),(17.0,6000)],                   # Joy: gummy power-up
 2:[(3.7,330),(7,1620),(8.2,2100),(9.9,2100),(13,3300),(16,4500),(18.5,5600),(19.4,6000)],           # Cyrus: dragged under
 3:[(3.7,330),(7,1500),(10,2700),(13,3800),(16,4950),(18.2,5800),(18.7,6000)]}
def xpos(i,t):
    k=KF[i]
    if t<=k[0][0]: return 150
    if t>=k[-1][0]: return k[-1][1]
    ts=[a for a,_ in k]; xs=[b for _,b in k]; return float(np.interp(t,ts,xs))
def campos(t):
    if t<3.7: return 0
    xs=[xpos(i,t) for i in range(4)]
    return min(max(0,(min(xs)+max(xs))/2-540),FIN+DECK+40-W)
def crown():
    c=Image.new('RGBA',(15,10),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.polygon([(0,9),(0,2),(4,5),(7,0),(10,5),(14,2),(14,9)],fill=(255,205,40)); d.rectangle([0,8,14,9],fill=(200,130,20))
    d.point((7,4),fill=(230,40,60)); d.point((3,7),fill=(80,160,255)); d.point((11,7),fill=(80,160,255))
    return c.resize((15*P,10*P),Image.NEAREST)
CROWN=crown()
def ctext(img,x,y,t,f,fill=(255,255,255),sw=6,center=True):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text(((x-w/2) if center else x,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
def deck(img,x0,x1):
    d=ImageDraw.Draw(img)
    if x1<0 or x0>W: return
    d.rectangle([x0,0,x1,H],fill=(176,180,192))
    for y in range(0,H,60):
        for x in range(int(x0)-((y//60)%2)*40,int(x1),80): d.rectangle([x,y,x+76,y+56],outline=(150,154,168),width=4)
    edge=x1 if x0<=0 else x0
    d.rectangle([edge-6,0,edge+6,H],fill=(110,114,130))
def swimmer(img,fr,x,y,t,ph,q=0.56,tilt=0):
    cut=fr.crop((0,0,fr.width,int(fr.height*q)))
    if tilt: cut=cut.rotate(tilt,resample=Image.NEAREST,expand=True)
    by=y+int(7*math.sin(2*math.pi*2.2*t+ph))
    img.alpha_composite(cut,(int(x-cut.width/2),by-cut.height+18))
    d=ImageDraw.Draw(img)
    # splash at the waterline and kick spray behind
    for k in range(7):
        sx=x-cut.width*0.45+k*cut.width*0.15; sy=by+14+int(4*math.sin(t*14+k))
        d.rectangle([sx,sy,sx+P*2,sy+P],fill=(235,248,255))
    for k in range(5):
        a=(t*3+k*0.37+ph)%1; sx=x-cut.width*0.5-40-a*110; sy=by+4-int(40*math.sin(a*math.pi))
        d.rectangle([sx,sy,sx+P,sy+P],fill=(235,248,255))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
FIN_T={i:KF[i][-1][0] for i in range(4)}
for f in range(N):
    t=f/FPS; cam=campos(t)
    img=Image.new('RGBA',(W,H)); ox=int(cam)%1080
    img.paste(WATER.crop((ox,0,1080,H)),(0,0)); img.paste(WATER.crop((0,0,ox,H)),(1080-ox,0)) if ox else None
    img=img.convert('RGBA')
    for k in range(5): rope(img,LANE_Y[0]-LANE_H//2-20+k*LANE_H+40-40,cam) if False else None
    for yb in [LANE_Y[0]-150]+[y+110 for y in LANE_Y]: rope(img,yb,cam)
    deck(img,-cam-10,DECK-cam); deck(img,FIN+180-cam,FIN+2000-cam)
    # finish wall flags
    fx=FIN+180-cam
    if -20<fx<W+20:
        d=ImageDraw.Draw(img)
        for y in range(0,H,40): d.rectangle([fx-26,y,fx-14,y+20],fill=(20,20,30) if (y//40)%2 else (250,250,250))
    # gummy power-up floating in Joy's lane
    if t<13.6:
        gx=3650-cam; gy=LANE_Y[0]-GUM.height+10+int(10*math.sin(2*math.pi*1.2*t))
        if t>=12.9: u=(t-12.9)/0.7; g2=GUM.resize((max(1,int(GUM.width*(1-u))),max(1,int(GUM.height*(1-u))))); gx+=-(3650-xpos(0,t))*u; img.alpha_composite(g2,(int(gx-g2.width/2),int(gy+GUM.height-g2.height)))
        elif -150<gx<W+150:
            glow=Image.new('RGBA',(220,220),(0,0,0,0)); ImageDraw.Draw(glow).ellipse([10,10,210,210],fill=(255,240,140,70))
            img.alpha_composite(glow,(int(gx-110),int(gy+GUM.height/2-110))); img.alpha_composite(GUM,(int(gx-GUM.width/2),int(gy)))
    for i in range(4):
        fr=SPR[i][int(t*8+i*2)%len(SPR[i])]; x=xpos(i,t)-cam; y=LANE_Y[i]
        if t<3.7:
            if t<3.3: img.alpha_composite(fr,(int(150-cam-fr.width/2),y-fr.height+60))
            else:   # dive
                u=(t-3.3)/0.4; dx=150+180*u; dy=-90*math.sin(u*math.pi)
                sp=fr.rotate(-70*u,resample=Image.NEAREST,expand=True); img.alpha_composite(sp,(int(dx-cam-sp.width/2),int(y+dy-sp.height+60*(1-u)+20*u)))
            continue
        if i==2 and 8.2<=t<9.9:
            # a Hollow surfaces and drags Cyrus under
            hx=x+110; hfr=HOL[int(t*8)%len(HOL)]
            if t<8.5: qh=0.75*(t-8.2)/0.3; qc=0.56
            elif t<9.0: qh=0.75*(1-(t-8.5)/0.5); qc=0.56*(1-(t-8.5)/0.5)
            else: qh=0; qc=0
            if qc>0.02: swimmer(img,fr,x,y,t,i,qc,tilt=int(10*math.sin(t*30)) if t>=8.5 else 0)
            if qh>0.02:
                hc=hfr.crop((0,0,hfr.width,int(hfr.height*qh))); img.alpha_composite(hc,(int(hx-hc.width/2),y-hc.height+18))
            if t>=8.5:
                d=ImageDraw.Draw(img)
                for k in range(8):
                    a=((t-8.5)*1.6+k*0.13)%1; bx=x+60+30*math.sin(k*2.1+t*5); by=y+10-a*120
                    d.ellipse([bx,by,bx+14+k%3*6,by+14+k%3*6],outline=(235,248,255),width=4)
            if 8.25<=t<8.9: ctext(img,x+40,y-230,'!!',F(56),(255,80,70))
            continue
        if i==2 and 9.9<=t<10.3: swimmer(img,fr,x,y,t,i,0.56*(t-9.9)/0.4); continue
        if t>=FIN_T[i]:
            # finished: bobbing at the wall
            swimmer(img,fr,x,y,t,i,0.62)
            if i==0:
                img.alpha_composite(CROWN,(int(x-CROWN.width/2),y-int(SH*0.62)-CROWN.height+10+int(7*math.sin(2*math.pi*2.2*t+i))))
                ctext(img,x,y-int(SH*0.62)-150,'WINNER',F(52),(255,214,60))
            continue
        swimmer(img,fr,x,y,t,i)
        if i==0 and 13.5<=t<17.0:
            d=ImageDraw.Draw(img)   # speed lines + sparkles after the gummy
            for k in range(6):
                a=(t*4+k*0.17)%1; lx=x-160-a*260; ly=y-100+k*22
                d.rectangle([lx,ly,lx+90,ly+P],fill=(255,240,150))
            if t<15.0: ctext(img,min(x+60,W-300),y-250,'ENERGY GUMMY!',F(36),(255,214,60))
    # text
    if t<3.3:
        ctext(img,W/2,230,'CHOOSE YOUR',F(64)); ctext(img,W/2,320,'CHAMPION!',F(64))
        n=3-int(t/1.1); ctext(img,W/2,420,str(max(1,n)),F(90),(255,214,60),8)
        for i,(nm,_) in enumerate(RAC): ctext(img,330,LANE_Y[i]-30,nm,F(36),center=False)
    elif t<4.0: ctext(img,W/2,330,'GO!',F(110),(255,214,60),8)
    if t>=17.6: ctext(img,W/2,1640,'DID YOUR',F(60)); ctext(img,W/2,1725,'CHAMPION WIN?',F(60))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (30,105,250,262,390,405,425,500,530,640): img.convert('RGB').resize((216,384)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done')
