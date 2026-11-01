import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
g=Image.open(A+'hub.gif'); BGF=[]
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB'); s=H/f.height; f=f.resize((int(f.width*s),H),Image.LANCZOS); ox=(f.width-W)//2
    BGF.append(ImageEnhance.Brightness(f.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(12))).enhance(0.45).convert('RGBA'))
# guild data: name, guide, sprite, colour, light colour, product, jar
GU={'F':('FOUNDATION','JOY','idle_5.gif',(74,124,58),(143,214,96),'ACV','jar_acv.png'),
    'V':('VITALITY','CLEO','idle_7.gif',(46,93,168),(110,170,255),'CREATINE','jar_creatine.png'),
    'E':('ENERGY','CYRUS','idle_8.gif',(217,122,31),(255,170,70),'MUSHROOM','jar_mushroom.png'),
    'R':('RECOVERY','RAYLEIGH','idle_6.gif',(107,45,107),(200,140,230),'MELATONIN','jar_melatonin.png')}
SPR_S={k:gif(v[2],150) for k,v in GU.items()}
SPR_L={k:gif(v[2],230) for k,v in GU.items()}
def jar(p,h):
    im=Image.open(A+p).convert('RGBA'); im=im.crop(im.getbbox()); return im.resize((int(im.width*h/im.height),h),Image.NEAREST)
JAR={k:jar(v[6],190) for k,v in GU.items()}
QS=[(('NIGHT OWL','R'),('EARLY BIRD','F')),
    (('TANK','V'),('SPEEDRUNNER','E')),
    (('COZY FARM GAME','F'),('BOSS RUSH','V')),
    (('ONE MORE LEVEL','E'),('SAVE AND LOG OFF','R')),
    (('GYM FIRST','V'),('COFFEE FIRST','E'))]
T0=2.6; QD=4.0; TR=T0+QD*len(QS); DUR=TR+4.6; N=int(DUR*FPS)
def ctext(img,x,y,t,f,fill=(255,255,255),sw=7):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
def fit_font(d,t,maxw,start):
    s=start
    while d.textlength(t,font=F(s))>maxw and s>24: s-=2
    return F(s)
def option_card(txt,gk,t):
    g_=GU[gk]; cw,ch=960,430
    c=Image.new('RGBA',(cw,ch),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([0,0,cw-1,ch-1],radius=30,fill=(20,15,30))
    d.rounded_rectangle([8,8,cw-9,ch-9],radius=26,fill=g_[3])
    d.rounded_rectangle([20,20,cw-21,ch-21],radius=20,fill=(28,22,42))
    f=fit_font(d,txt,cw-80,66); w=d.textlength(txt,font=f)
    d.text(((cw-w)/2,70),txt,font=f,fill=(255,255,255),stroke_width=6,stroke_fill=(20,15,30))
    # guild tag: guide sprite + guild name
    spr=SPR_S[gk][int(t*8)%len(SPR_S[gk])]
    tag=g_[0]+' GUILD'; f2=F(34); tw=d.textlength(tag,font=f2)
    total=spr.width+24+tw; x0=(cw-total)/2
    c.alpha_composite(spr,(int(x0),ch-40-spr.height))
    d.text((x0+spr.width+24,ch-40-spr.height/2-17),tag,font=f2,fill=g_[4],stroke_width=5,stroke_fill=(20,15,30))
    return c
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGF[int(t*5)%len(BGF)].copy(); d=ImageDraw.Draw(img)
    if t<T0:
        ctext(img,W/2,330,'WHICH GUILD',F(80)); ctext(img,W/2,440,'ARE YOU?',F(80),(255,214,60))
        ctext(img,W/2,600,'Pick one. Count your colors.',F(36))
        for k,gk in enumerate('FVER'):
            g_=GU[gk]; x=150+k*260; y=1180
            pop=min(1,max(0,(t-0.15*k)/0.25))
            spr=SPR_L[gk][int(t*8+k)%len(SPR_L[gk])]
            if pop>0:
                s=spr.resize((max(1,int(spr.width*pop)),max(1,int(spr.height*pop))),Image.NEAREST)
                d.rounded_rectangle([x-115,y-270,x+115,y+70],radius=20,fill=(20,15,30),outline=g_[3],width=8)
                img.alpha_composite(s,(int(x-s.width/2),int(y-s.height)))
                f2=F(22); w=d.textlength(g_[0],font=f2); d.text((x-w/2,y+22),g_[0],font=f2,fill=g_[4])
    elif t<TR:
        q=int((t-T0)/QD); u=(t-T0-q*QD)/QD
        (a,ga),(b,gb)=QS[q]
        ctext(img,W/2,300,f'QUESTION {q+1}/5',F(44),(255,214,60))
        # progress pips
        for k in range(5):
            x=W/2-180+k*90; d.rectangle([x-24,390,x+24,412],fill=(255,214,60) if k<=q else (70,60,90))
        slide=min(1,u/0.12); e=1-(1-slide)**3
        ca=option_card(a,ga,t); cb=option_card(b,gb,t)
        img.alpha_composite(ca,(int(60-(1-e)*1100),520))
        img.alpha_composite(cb,(int(60+(1-e)*1100),1130))
        if slide>=1: ctext(img,W/2,1000,'OR',F(70),(255,255,255),8)
        # timer bar
        d.rectangle([60,1640,1020,1672],fill=(40,32,58)); d.rectangle([60,1640,60+int(960*(1-u)),1672],fill=(255,214,60))
    else:
        u=t-TR
        ctext(img,W/2,170,'MOST PICKED COLOR',F(46)); ctext(img,W/2,240,'= YOUR GUILD',F(46),(255,214,60))
        for k,gk in enumerate('FVER'):
            g_=GU[gk]; x=60+(k%2)*500; y=360+(k//2)*640
            pop=min(1,max(0,(u-0.12*k)/0.25))
            if pop<=0: continue
            tile=Image.new('RGBA',(460,600),(0,0,0,0)); td=ImageDraw.Draw(tile)
            td.rounded_rectangle([0,0,459,599],radius=26,fill=(20,15,30)); td.rounded_rectangle([8,8,451,591],radius=22,fill=g_[3]); td.rounded_rectangle([20,20,439,579],radius=16,fill=(28,22,42))
            f2=F(34); w=td.textlength(g_[0],font=f2); td.text(((460-w)/2,48),g_[0],font=f2,fill=g_[4],stroke_width=4,stroke_fill=(20,15,30))
            spr=SPR_L[gk][int(t*8+k)%len(SPR_L[gk])]; tile.alpha_composite(spr,(int(125-spr.width/2),470-spr.height))
            j=JAR[gk]; tile.alpha_composite(j,(int(340-j.width/2),470-j.height))
            f3=F(20); w=td.textlength(g_[1],font=f3); td.text((125-w/2,500),g_[1],font=f3,fill=(255,255,255))
            w=td.textlength(g_[5],font=f3); td.text((340-w/2,500),g_[5],font=f3,fill=(255,255,255))
            if pop<1: tile=tile.resize((int(460*pop),int(600*pop)),Image.BILINEAR)
            img.alpha_composite(tile,(int(x+230-tile.width/2),int(y+300-tile.height/2)))
        if u>0.6: ctext(img,W/2,1680,'COMMENT YOUR GUILD',F(48),(255,214,60))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%30==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done',DUR)
