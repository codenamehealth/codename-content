import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from sim import run, R, FIN
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
SEED=3; T_GO=3.4
frames,fin,statics,bumps,xs=run(SEED)
WIN=min(fin,key=fin.get); TW=fin[WIN]
T_RACE_END=TW+1.3; REVEAL=3.4; DUR=T_RACE_END+REVEAL; N=int(DUR*FPS)
print('winner',WIN,TW,'dur',DUR)
NAMES=['JOY','CLEO','CYRUS','RAYLEIGH']; FILES=['idle_5.gif','idle_7.gif','idle_8.gif','idle_6.gif']
COL=[(90,190,70),(90,140,230),(245,140,40),(170,80,200)]
# ---- marble art: guide face in a glass marble
def face(p):
    im=Image.open(A+p); im.seek(0); f=im.convert('RGBA').crop((330,165,590,425)); return f.resize((2*R-10,2*R-10),Image.NEAREST)
def marble(i):
    S=2*R; m=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(m)
    d.ellipse([0,0,S-1,S-1],fill=(20,14,30,255)); d.ellipse([4,4,S-5,S-5],fill=COL[i]+(255,))
    d.ellipse([9,9,S-10,S-10],fill=(235,225,210,255))
    fc=face(FILES[i]); mask=Image.new('L',(S,S),0); ImageDraw.Draw(mask).ellipse([9,9,S-10,S-10],fill=255)
    lay=Image.new('RGBA',(S,S),(0,0,0,0)); lay.paste(fc,(5,5)); m.paste(lay,(0,0),Image.composite(lay.split()[3],Image.new('L',(S,S),0),mask))
    return m
MARB=[marble(i) for i in range(4)]
GLINT=Image.new('RGBA',(2*R,2*R),(0,0,0,0)); dg=ImageDraw.Draw(GLINT)
dg.arc([10,10,2*R-11,2*R-11],200,250,fill=(255,255,255,220),width=7); dg.ellipse([26,24,38,36],fill=(255,255,255,200))
# ---- static world
HT=6700
cg=Image.open(A+'vit_hd.gif'); cg.seek(0); g=cg.convert('RGB'); s_=H/g.height; g=g.resize((int(g.width*s_),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.45).convert('RGBA')
world=Image.new('RGBA',(W,HT),(0,0,0,0)); d=ImageDraw.Draw(world)
d.rectangle([54,0,1026,HT],fill=(30,24,48,215))
rng=random.Random(2)
for _ in range(260):
    x=rng.uniform(60,1020); y=rng.uniform(0,HT); s=rng.choice([4,6]); d.rectangle([x,y,x+s,y+s],fill=(255,240,180,rng.randint(60,160)))
WALL=(150,112,78,255); WALL2=(70,46,30,255)
def thick(a,b,r):
    d.line([a,b],fill=WALL2,width=int(2*r+8)); d.line([a,b],fill=WALL,width=int(2*r))
    for p in (a,b): d.ellipse([p[0]-r-4,p[1]-r-4,p[0]+r+4,p[1]+r+4],fill=WALL2); d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=WALL)
G=[Image.open(f'../gummy/{n}').convert('RGBA') for n in ('acv_gummy_single.png','cre_gummy_single.png','mush_gummy_single.png','mel_gummy_red.png')]
G=[g_.crop(g_.getbbox()) for g_ in G]
bk=0
for st in statics:
    if st[0] in ('wall','ramp','floor'): thick(st[1],st[2],st[3])
    elif st[0]=='peg':
        (x,y),r=st[1],st[2]; d.ellipse([x-r-4,y-r-4,x+r+4,y+r+4],fill=(90,55,10,255)); d.ellipse([x-r,y-r,x+r,y+r],fill=(255,200,50,255)); d.ellipse([x-r*0.5,y-r*0.6,x,y-r*0.1],fill=(255,245,200,255))
    elif st[0]=='bump':
        (x,y),r=st[1],st[2]
        d.ellipse([x-r-10,y-r-10,x+r+10,y+r+10],outline=(255,214,60,200),width=6)
        gm=G[bk%4]; k=(2*r)/max(gm.size); gm=gm.resize((int(gm.width*k),int(gm.height*k)),Image.LANCZOS); world.alpha_composite(gm,(int(x-gm.width/2),int(y-gm.height/2))); bk+=1
        d=ImageDraw.Draw(world)
# finish line
for k,x in enumerate(range(470,612,22)):
    for j in range(3): d.rectangle([x,FIN+20+j*22,x+22,FIN+42+j*22],fill=(245,245,245,255) if (k+j)%2 else (20,20,30,255))
def sign(y,txt):
    f=F(30); w=d.textlength(txt,font=f); d.rectangle([540-w/2-22,y-14,540+w/2+22,y+44],fill=(20,14,30,230),outline=(255,214,60,255),width=4); d.text((540-w/2,y),txt,font=f,fill=(255,214,60))
sign(600,'PEG FOREST'); sign(1840,'THE SLIDES'); sign(3300,'GUMMY BUMPERS'); sign(4420,'SPINNERS'); sign(5180,'FINAL STRETCH')
WORLD=world
SPIN=[(300,4600),(780,4600),(540,4950)]
def ctext(img,x,y,t,f,fill=(255,255,255),sw=6):
    dd=ImageDraw.Draw(img); w=dd.textlength(t,font=f); dd.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
WSPR=gif(FILES[WIN],640)
def crown():
    c=Image.new('RGBA',(15,10),(0,0,0,0)); dd=ImageDraw.Draw(c)
    dd.polygon([(0,9),(0,2),(4,5),(7,0),(10,5),(14,2),(14,9)],fill=(255,205,40)); dd.rectangle([0,8,14,9],fill=(200,130,20))
    dd.point((7,4),fill=(230,40,60)); dd.point((3,7),fill=(80,160,255)); dd.point((11,7),fill=(80,160,255))
    return c.resize((15*8,10*8),Image.NEAREST)
CROWN=crown()
conf=[(rng.uniform(0,W),rng.uniform(-1800,0),rng.uniform(250,420),rng.choice([(255,90,90),(255,214,60),(90,200,255),(140,255,140),(220,120,255)])) for _ in range(90)]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
cam=0.0
for f in range(N):
    t=f/FPS
    if t<T_RACE_END:
        fr=frames[min(f,len(frames)-1)]
        ys=[fr[i][1] for i in range(4)]
        if t<T_GO: target=0
        else:
            # follow the leader among marbles still racing
            lead=max(ys) if TW>t else fr[WIN][1]
            target=min(max(0,lead-0.56*H),HT-H)
        cam+= (target-cam)*0.18
        img=BG.copy(); img.alpha_composite(WORLD.crop((0,int(cam),W,int(cam)+H)))
        dd=ImageDraw.Draw(img)
        if t<T_GO:   # start gate
            dd.rectangle([50,470-cam-10,1030,470-cam+10],fill=(255,214,60));
        elif t<T_GO+0.25:
            dd.rectangle([50,470-cam-10,1030,470-cam+10],fill=(255,255,255))
        for k,(sx,sy) in enumerate(SPIN):
            a=fr[4+k][0]; dx,dy=190*math.cos(a),190*math.sin(a); y=sy-cam
            if -300<y<H+300:
                dd.line([(sx-dx,y-dy),(sx+dx,y+dy)],fill=(40,26,16),width=44); dd.line([(sx-dx,y-dy),(sx+dx,y+dy)],fill=(200,150,90),width=32)
                dd.ellipse([sx-16,y-16,sx+16,y+16],fill=(255,214,60))
        for i in range(4):
            x,y,a=fr[i]; y-=cam
            if -150<y<H+150:
                m=MARB[i].rotate(-math.degrees(a),resample=Image.BICUBIC); img.alpha_composite(m,(int(x-R),int(y-R))); img.alpha_composite(GLINT,(int(x-R),int(y-R)))
                ctext(img,x,int(y-R-42),NAMES[i],F(28),COL[i] if t>=T_GO else (255,255,255),5)
        if t<T_GO:
            ctext(img,W/2,110,'PICK YOUR',F(72)); ctext(img,W/2,205,'MARBLE!',F(72),(255,214,60))
            n=3-int(t/1.0)
            ctext(img,W/2,860,str(n) if t<3.0 else 'GO!',F(150),(255,214,60),10)
        else:
            done_=lambda i: fin.get(i,99)<=t
            order=sorted(range(4),key=lambda i:(0 if done_(i) else 1, fin[i] if done_(i) else 0, -fr[i][1]))
            ld=order[0]
            dd=ImageDraw.Draw(img); dd.rectangle([0,70,W,170],fill=(20,14,30,255)); dd.rectangle([0,166,W,172],fill=COL[ld])
            ctext(img,W/2,98,('WINNER: ' if t>=TW else 'LEADER: ')+NAMES[ld],F(48),COL[ld] if t<TW else (255,214,60),5)
        if TW<=t<TW+0.12: img=Image.blend(img,Image.new('RGBA',(W,H),(255,255,255,255)),0.6*(1-(t-TW)/0.12))
    else:
        u=t-T_RACE_END; img=BG.copy(); dd=ImageDraw.Draw(img)
        if u<0.12: img=Image.blend(img,Image.new('RGBA',(W,H),(255,255,255,255)),0.8*(1-u/0.12)); dd=ImageDraw.Draw(img)
        sc=1+0.3*max(0,1-u/0.25)
        ctext(img,W/2,330,'WINNER',F(int(110*sc)),(255,214,60),9)
        ctext(img,W/2,480,NAMES[WIN],F(70),COL[WIN],7)
        sp=WSPR[int(t*8)%len(WSPR)]; img.alpha_composite(sp,(int(W/2-sp.width/2),1520-sp.height))
        img.alpha_composite(CROWN,(int(W/2-CROWN.width/2),1520-sp.height-70+int(8*math.sin(t*4))))
        mb=MARB[WIN].resize((180,180),Image.LANCZOS); img.alpha_composite(mb,(W-260,1340+int(10*math.sin(t*3))));
        for x,y0,v,col in conf:
            y=y0+v*u*2.2
            if 0<y<H: dd.rectangle([x,y,x+14,y+20],fill=col)
        if u>1.0: ctext(img,W/2,1650,'DID YOUR',F(56)); ctext(img,W/2,1730,'MARBLE WIN?',F(56))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%30==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done',DUR)
