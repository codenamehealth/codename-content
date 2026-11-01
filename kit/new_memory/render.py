import numpy as np, subprocess, math, random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=14.2; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
g=Image.open(A+'vit_hd.gif'); BGF=[]
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB'); s=H/f.height; f=f.resize((int(f.width*s),H),Image.LANCZOS); ox=(f.width-W)//2
    BGF.append(ImageEnhance.Brightness(f.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(12))).enhance(0.5).convert('RGBA'))
GUIDES=[('JOY','idle_5.gif',(74,124,58)),('CLEO','idle_7.gif',(46,93,168)),('CYRUS','idle_8.gif',(217,122,31)),('RAYLEIGH','idle_6.gif',(107,45,107))]
CW,CH=400,560; P=5
def darker(c,k): return tuple(int(v*k) for v in c)
def card_face(name,spr,col):
    c=Image.new('RGBA',(CW,CH),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([0,0,CW-1,CH-1],radius=26,fill=(20,15,30))
    d.rounded_rectangle([8,8,CW-9,CH-9],radius=22,fill=col)
    d.rounded_rectangle([22,22,CW-23,CH-23],radius=14,fill=(20,15,30))
    inner=[28,28,CW-29,CH-110]
    # inner panel: vertical gradient of the guild colour
    for y in range(inner[1],inner[3]):
        u=(y-inner[1])/(inner[3]-inner[1]); d.line([(inner[0],y),(inner[2],y)],fill=darker(col,0.55+0.35*(1-u)))
    for k in range(6):   # pixel sparkles
        x=40+((k*97)%(CW-90)); y=50+((k*61)%220); d.rectangle([x,y,x+P,y+P],fill=(255,240,180))
    d.rectangle([28,CH-104,CW-29,CH-29],fill=darker(col,0.35))
    f=F(36 if len(name)<8 else 30); w=d.textlength(name,font=f)
    d.text(((CW-w)/2,CH-82),name,font=f,fill=(255,255,255),stroke_width=4,stroke_fill=(20,15,30))
    return c
def card_back():
    c=Image.new('RGBA',(CW,CH),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([0,0,CW-1,CH-1],radius=26,fill=(20,15,30))
    d.rounded_rectangle([8,8,CW-9,CH-9],radius=22,fill=(232,182,76))
    d.rounded_rectangle([22,22,CW-23,CH-23],radius=14,fill=(52,36,82))
    for y in range(40,CH-40,40):
        for x in range(40,CW-40,40):
            if ((x+y)//40)%2==0: d.polygon([(x,y-9),(x+9,y),(x,y+9),(x-9,y)],fill=(74,54,112))
    d.ellipse([CW/2-95,CH/2-95,CW/2+95,CH/2+95],fill=(20,15,30)); d.ellipse([CW/2-85,CH/2-85,CW/2+85,CH/2+85],fill=(232,182,76))
    f=F(32)
    for i,t in enumerate(('CODE','NAME')):
        w=d.textlength(t,font=f); d.text(((CW-w)/2,CH/2-36+i*42),t,font=f,fill=(20,15,30))
    return c
SPR=[gif(p,330) for _,p,_ in GUIDES]
FACES=[card_face(n,s,c) for (n,_,c),s in zip(GUIDES,SPR)]
BACK=card_back()
SLOT=[(285,770),(795,770),(285,1380),(795,1380)]
CLEO=1
# shuffle plan: single swaps slowing->fast, finishing with double swaps
rng=random.Random(9)
plan=[]; t0=3.4
durs=[0.6,0.55,0.48,0.42,0.38,0.34,0.31,0.29,0.27,0.26,0.26,0.26,0.26,0.26]
gaps=[0.08,0.07,0.07,0.06,0.06,0.05,0.05,0.05,0.04,0.04,0.04,0.04,0.04,0.04]
PAIRS=[(0,1),(2,3),(0,2),(1,3),(0,3),(1,2)]
def mk(seed):
    r=random.Random(seed); out=[]; t=3.4; prev=None
    for k,(d_,g_) in enumerate(zip(durs,gaps)):
        if k>=10:   # double swaps at the end
            opts=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]; sw=r.choice([o for o in opts if o!=prev]); prev=sw
            out.append((t,t+d_,list(sw)))
        else:
            sw=r.choice([p for p in PAIRS if (p,) != prev]); prev=(sw,); out.append((t,t+d_,[sw]))
        t+=d_+g_
    return out
def final_slots(plan):
    slot=[0,1,2,3]
    for _,_,sws in plan:
        new=slot[:]
        for a,b in sws:
            ca=slot.index(a); cb=slot.index(b); new[ca]=b; new[cb]=a
        slot=new
    return slot
for seed in range(500):
    PLAN=mk(seed); fs=final_slots(PLAN)
    if fs[CLEO]==2 and len(set(fs))==4:
        # Cleo must move a lot
        moves=sum(1 for _,_,sws in PLAN for a,b in sws if True)
        break
SEND=PLAN[-1][1]; print('seed',seed,'shuffle end',round(SEND,2),'final',fs)
def card_pos(t):
    slot=[0,1,2,3]
    for t0,t1,sws in PLAN:
        if t<t0: break
        if t<t1:
            u=(t-t0)/(t1-t0); e=u*u*(3-2*u); pos={c:(*SLOT[slot[c]],1.0) for c in range(4)}
            for a,b in sws:
                ca=slot.index(a); cb=slot.index(b)
                (xa,ya),(xb,yb)=SLOT[a],SLOT[b]; dx,dy=xb-xa,yb-ya; L=math.hypot(dx,dy); nx,ny=-dy/L,dx/L
                arc=math.sin(e*math.pi)*90
                pos[ca]=(xa+dx*e+nx*arc, ya+dy*e+ny*arc, 1+0.06*math.sin(e*math.pi))
                pos[cb]=(xb-dx*e-nx*arc, yb-dy*e-ny*arc, 1-0.04*math.sin(e*math.pi))
            return pos,slot
        new=slot[:]
        for a,b in sws:
            ca=slot.index(a); cb=slot.index(b); new[ca]=b; new[cb]=a
        slot=new
    return {c:(*SLOT[slot[c]],1.0) for c in range(4)},slot
T_DOWN=2.7; T_Q=SEND+0.25; T_REVEAL=T_Q+2.0; T_ALL=T_REVEAL+1.0
def flip_state(c,t):
    # returns (x-scale, show_face)
    if t<T_DOWN:   # face up (flip in at start)
        u=min(1,max(0,(t-0.15*c)/0.35)); return (abs(math.cos((1-u)*math.pi/2)) if u<1 else 1.0), True
    if t<T_DOWN+0.4+0.08*c:
        u=min(1,max(0,(t-T_DOWN-0.08*c)/0.4)); return abs(math.cos(u*math.pi)), u<0.5
    rev=T_REVEAL if c==CLEO else T_ALL+0.12*c
    if t<rev: return 1.0, False
    u=min(1,(t-rev)/0.4); return abs(math.cos(u*math.pi)) if u<1 else 1.0, u>=0.5
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGF[int(t*5)%len(BGF)].copy()
    pos,slot=card_pos(t)
    order=sorted(range(4),key=lambda c:pos[c][2])
    for c in order:
        x,y,sc=pos[c]; xs,face=flip_state(c,t)
        if face:
            base=FACES[c].copy(); spr=SPR[c][int(t*8+c)%len(SPR[c])]
            base.alpha_composite(spr,((CW-spr.width)//2,CH-112-spr.height))
        else:
            base=BACK.copy()
            if t>=T_Q:
                lab='ABCD'[slot[c]]; d=ImageDraw.Draw(base); f2=F(70); w=d.textlength(lab,font=f2)
                d.text(((CW-w)/2,40),lab,font=f2,fill=(255,255,255),stroke_width=7,stroke_fill=(20,15,30))
        cw=max(2,int(CW*xs*sc)); ch=int(CH*sc)
        im=base.resize((cw,ch),Image.NEAREST if xs>0.99 and abs(sc-1)<0.001 else Image.BILINEAR)
        if c==CLEO and t>=T_REVEAL:
            gl=Image.new('RGBA',(CW+140,CH+140),(0,0,0,0)); ImageDraw.Draw(gl).rounded_rectangle([0,0,CW+139,CH+139],radius=60,fill=(255,230,120,int(110*min(1,(t-T_REVEAL)/0.3))))
            gl=gl.filter(ImageFilter.GaussianBlur(24)); img.alpha_composite(gl,(int(x-gl.width/2),int(y-gl.height/2)))
        img.alpha_composite(im,(int(x-cw/2),int(y-ch/2)))
    if t<T_DOWN+0.5: ctext(img,W/2,180,'REMEMBER',F(76)); ctext(img,W/2,285,'THE GUIDES',F(76),(255,214,60))
    elif t<T_Q: ctext(img,W/2,230,'WATCH CLOSELY',F(66))
    elif t<T_REVEAL: ctext(img,W/2,180,"WHERE'S",F(84)); ctext(img,W/2,295,'CLEO?',F(84),(110,170,255))
    else:
        ctext(img,W/2,180,"WHERE'S",F(84)); ctext(img,W/2,295,'CLEO?',F(84),(110,170,255))
        if t>=T_REVEAL+0.4: ctext(img,W/2,1765,'Did you get it right?',F(40))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%30==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done', 'Q',round(T_Q,2),'reveal',round(T_REVEAL,2),'dur',DUR)
