import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A='assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(sz): return ImageFont.truetype(FONT,sz)
GUILD={'Foundation':('forest','acv',(74,124,58)),'Vitality':('castle','creatine',(46,93,168)),
       'Energy':('sun','mushroom',(217,122,31)),'Recovery':('moon','melatonin',(107,45,107))}
# ---- backgrounds: scene cropped to portrait, blurred, darkened, guild-tinted, light beam + floor band like the reference
FLOOR=1395
def make_bg(scene,tint):
    g=Image.open(A+f'scene_{scene}.png').convert('RGB')
    s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2; g=g.crop((ox,0,ox+W,H))
    g=g.filter(ImageFilter.GaussianBlur(10))
    g=Image.blend(g,Image.new('RGB',(W,H),tint),0.22)
    g=Image.blend(g,Image.new('RGB',(W,H),(0,0,0)),0.30).convert('RGBA')
    beam=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(beam)
    d.polygon([(760,0),(W,0),(W,1580),(330,FLOOR)],fill=(255,240,210,38))
    g.alpha_composite(beam.filter(ImageFilter.GaussianBlur(6)))
    fl=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(fl).rectangle([0,FLOOR,W,H],fill=(0,0,0,70))
    g.alpha_composite(fl)
    return g
BG={k:make_bg(v[0],v[2]) for k,v in GUILD.items()}
# ---- sprites
def load_gif(path):
    im=Image.open(A+path); fr=[]
    for i in range(getattr(im,'n_frames',1)):
        im.seek(i); fr.append(im.convert('RGBA'))
    return fr,im.info.get('duration',100)
def fit(frames,target_h,integer=True):
    bb=None
    for f in frames:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in frames]; h=fr[0].height
    k=max(1,round(target_h/h)) if integer else target_h/h
    return [f.resize((int(f.width*k),int(f.height*k)),Image.NEAREST) for f in fr]
def glow(img,color,radius=28,strength=1.6):
    a=img.split()[3].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(radius))
    a=a.point(lambda v:min(255,int(v*strength)))
    g=Image.new('RGBA',img.size,color+(0,)); g.putalpha(a); return g
def pad(img,p):
    c=Image.new('RGBA',(img.width+2*p,img.height+2*p),(0,0,0,0)); c.paste(img,(p,p)); return c
POT={k:pad(fit([Image.open(A+f'jar_{v[1]}.png').convert('RGBA')],560)[0],80) for k,v in GUILD.items()}
IDLE={'Joy':'idle_5.gif','Cleo':'idle_7.gif','Cyrus':'idle_8.gif','Rayleigh':'idle_6.gif','The Hollow':'idle_9.gif'}
VIC={'Joy':'vic_Victory_Pose.gif','Cleo':'vic_victoryPose.gif','Cyrus':'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif','Rayleigh':'vic_victoryPose_1.gif'}
CG={'Joy':'Foundation','Cleo':'Vitality','Cyrus':'Energy','Rayleigh':'Recovery','The Hollow':None,'The Dragon':None}
SPR={}
for n,f in IDLE.items(): fr,d=load_gif(f); SPR[('idle',n)]=([pad(x,60) for x in fit(fr,760)],d)
for n,f in VIC.items(): fr,d=load_gif(f); SPR[('vic',n)]=([pad(x,60) for x in fit(fr,760)],d)
fr,d=load_gif('dragon.gif'); SPR[('idle','The Dragon')]=([pad(x,60) for x in fit(fr,820,integer=False)],d)
DRAGON_BG=make_bg('sun',(150,40,30)); HOLLOW_BG=make_bg('castle',(40,40,60))
# ---- UI
def text_c(img,y,s,font,fill,shadow=True):
    d=ImageDraw.Draw(img); w=d.textlength(s,font=font); x=(W-w)/2
    if shadow: d.text((x+4,y+4),s,font=font,fill=(0,0,0,170))
    d.text((x,y),s,font=font,fill=fill); return x,w
def title(img,pre,key,post):
    f=F(40); d=ImageDraw.Draw(img); parts=[(pre,(255,255,255)),(key,(255,214,90)),(post,(255,255,255))]
    tw=sum(d.textlength(p,font=f) for p,_ in parts); x=(W-tw)/2; y=236
    for p,c in parts:
        d.text((x+4,y+4),p,font=f,fill=(0,0,0,170)); d.text((x,y),p,font=f,fill=c); x+=d.textlength(p,font=f)
def button(img,cx,cy,w,h,label,font):
    b=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(b)
    x0,y0,x1,y1=cx-w//2,cy-h//2,cx+w//2,cy+h//2
    d.rectangle([x0,y0,x1,y1],fill=(30,30,34,200),outline=(200,200,200,120),width=3)
    for sx in (x0+14,x1-34):  # little bracket ornaments like the reference button
        d.rectangle([sx,y0+12,sx+20,y1-12],outline=(220,220,220,150),width=3)
    img.alpha_composite(b)
    d=ImageDraw.Draw(img); tw=d.textlength(label,font=font); bb=font.getbbox(label)
    d.text((cx-tw/2,cy-(bb[3]+bb[1])/2),label,font=font,fill=(255,255,255))
def label(img,s): text_c(img,1490,s,F(40),(255,255,255))
# ---- timeline (matches the reference cut-for-cut: new pick every 3 frames)
R1=['Foundation','Vitality','Energy','Recovery']
R2=['Joy','Cleo','Cyrus','Rayleigh','The Dragon','The Hollow']
R3=['Cleo','Cyrus','The Dragon','Rayleigh','Joy','The Hollow']
N=289
def item_at(f):
    if f<84:  k=0 if f<4 else 1+(f-4)//3; return ('r1',R1[k%len(R1)])
    if f<174: k=(f-84)//3; return ('r2',R2[k%len(R2)])
    if f<267: k=(f-174)//3; return ('r3',R3[k%len(R3)])
    return ('end',None)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; kind,name=item_at(f)
    if kind=='end':
        img=make_bg.cache if hasattr(make_bg,'cache') else None
        if img is None: make_bg.cache=make_bg('moon',(60,60,70)); img=make_bg.cache
        img=img.copy(); e=f-267
        text_c(img,650,'DID YOU',F(44),(255,255,255))
        text_c(img,895,'OR',F(40),(255,255,255))
        if e>=2: button(img,W//2,800,450,110,'WIN',F(60))
        else: button(img,W//2,800,450,110,'',F(60))
        if e>=2: button(img,W//2,1075,450,110,'LOSE',F(60))
        else: button(img,W//2,1075,450,110,'',F(60))
    else:
        if kind=='r1':
            img=BG[name].copy(); pot=POT[name]; col=GUILD[name][2]
            img.alpha_composite(glow(pot,tuple(min(255,c+90) for c in col),34,2.2),(W//2-pot.width//2,FLOOR-pot.height+40))
            img.alpha_composite(pot,(W//2-pot.width//2,FLOOR-pot.height+40))
            title(img,'What is your ','guild','?'); label(img,name)
        else:
            g=CG[name]
            img=(BG[g] if g else (DRAGON_BG if name=='The Dragon' else HOLLOW_BG)).copy()
            if g:
                pot=POT[g]; gl=glow(pot,tuple(min(255,c+90) for c in GUILD[g][2]),34,2.0)
                big=pot.resize((int(pot.width*1.6),int(pot.height*1.6)),Image.NEAREST); bgl=gl.resize(big.size)
                px=W//2-big.width//2; py=FLOOR-big.height+110
                img.alpha_composite(bgl,(px,py)); a=big.copy(); a.putalpha(big.split()[3].point(lambda v:int(v*0.8))); img.alpha_composite(a,(px,py))
            kindk='vic' if (kind=='r3' and ('vic',name) in SPR) else 'idle'
            frs,dur=SPR[(kindk,name)]; sp=frs[int(t*1000/dur)%len(frs)]
            if not g: img.alpha_composite(glow(sp,(255,120,60) if name=='The Dragon' else (160,160,220),30,1.4),(W//2-sp.width//2,FLOOR-sp.height+60))
            img.alpha_composite(sp,(W//2-sp.width//2,FLOOR-sp.height+60))
            if kind=='r2': title(img,'Who is your ','opponent','?')
            else: title(img,'Who helps you ','mid-fight','?')
            label(img,name)
        button(img,W//2,345,470,62,'Pause Game',F(24))
        if f<24: text_c(img,470,'Can you WIN?',F(52),(255,255,255))
    ff.stdin.write(img.convert('RGB').tobytes())
ff.stdin.close(); ff.wait(); print('done')
