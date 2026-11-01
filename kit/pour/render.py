import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from scipy import ndimage
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=9.4; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
hub=Image.open(A+'hub.gif'); hub.seek(0); g=hub.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(12))).enhance(0.7).convert('RGBA')
# rounds: potion art, liquid color, line height (0..1 of fillable height), time window, overshoot at end
R=[('acv',(120,200,70),0.50,0.25,2.71,9),('creatine',(80,170,235),0.62,2.71,4.54,3),('mushroom',(245,150,40),0.48,4.54,5.92,11),
   ('melatonin',(170,90,220),0.70,5.92,7.0,9),('acv',(255,205,60),0.60,7.0,9.4,5)]
VH=980; VCX=540; VBOT=1330; PX=10
def vessel(kind):
    w,h=90,98; inside=Image.new('L',(w,h),0); solid=Image.new('L',(w,h),0); di=ImageDraw.Draw(inside); ds=ImageDraw.Draw(solid)
    if kind=='tankard':
        di.rectangle([18,14,62,92],fill=255); ds.rectangle([62,28,80,34],fill=255); ds.rectangle([74,28,80,74],fill=255); ds.rectangle([62,68,80,74],fill=255)
        ds.rectangle([14,8,66,13],fill=255); ds.rectangle([14,40,66,43],fill=255); ds.rectangle([14,70,66,73],fill=255)
    elif kind=='goblet':
        di.pieslice([12,-20,78,60],0,180,fill=255); di.rectangle([12,8,78,20],fill=255)
        ds.rectangle([41,60,49,86],fill=255); ds.ellipse([24,84,66,96],fill=255)
    elif kind=='cauldron':
        di.ellipse([6,22,84,90],fill=255); di.rectangle([16,20,74,40],fill=0); di.rectangle([16,24,74,40],fill=255)
        ds.rectangle([10,16,80,23],fill=255); ds.rectangle([16,86,24,96],fill=255); ds.rectangle([66,86,74,96],fill=255)
    elif kind=='flask':
        di.polygon([(37,6),(53,6),(53,36),(80,90),(10,90),(37,36)],fill=255)
        ds.rectangle([33,2,57,7],fill=255)
    else:
        di.rectangle([38,4,52,34],fill=255); di.ellipse([10,26,80,94],fill=255)
        ds.rectangle([34,0,56,5],fill=255)
    a=np.array(inside)>0; so=np.array(solid)>0
    up=lambda z: np.kron(z,np.ones((PX,PX),bool))
    A_,S_=up(a),up(so)
    m=A_|S_
    rows=np.where(A_.any(1))[0]; top,bot=rows.min(),rows.max()
    edge=A_&~ndimage.binary_erosion(A_,iterations=PX)
    inner=ndimage.binary_erosion(A_,iterations=PX)
    neck=top+int((bot-top)*0.06)
    return m,edge,inner,neck,bot,S_
KINDS=['tankard','goblet','cauldron','flask','bottle']
V=[vessel(k) for k in KINDS]
POUR={}
for n in ['acv','creatine','mushroom','melatonin']:
    im=Image.open(A+f'jar_{n}.png').convert('RGBA'); im=im.crop(im.getbbox()); k=230/im.height
    POUR[n]=im.resize((int(im.width*k),230),Image.NEAREST).rotate(-125,resample=Image.NEAREST,expand=True)
def tbox(img,status,col,l1,l2):
    d=ImageDraw.Draw(img)
    x0,y0,x1,y1=70,1420,1010,1640
    d.rectangle([x0+8,y0+8,x1+8,y1+8],fill=(0,0,0,110)); d.rectangle([x0,y0,x1,y1],fill=(24,20,44,235),outline=(201,162,74),width=6)
    f1=F(40 if len(l1)<20 else 34); w=d.textlength(l1,font=f1); d.text(((W-w)/2,y0+55 if l2 else y0+90),l1,font=f1,fill=(255,255,255))
    if l2: f2=F(26); w=d.textlength(l2,font=f2); d.text(((W-w)/2,y0+140),l2,font=f2,fill=(255,214,90))
    if status:
        fs=F(30); w=d.textlength(status,font=fs); d.rectangle([x0-10,y0-50,x0+w+30,y0+8],fill=col,outline=(20,15,35),width=4); d.text((x0+10,y0-36),status,font=fs,fill=(255,255,255))
def feedback(diff,ri):
    p=abs(round(diff))
    if p==0: return 'PERFECT',(60,170,80),'On the line!','Send it to someone who cant'
    if diff<0:
        if p<=3: return 'SO CLOSE',(215,70,50),f'{p}% under the line','Hit the line? Screenshot it!'
        if p<=8: return 'CLOSE',(30,25,40),f'{p}% under the line','Hit the line? Screenshot it!'
        return 'TOO EARLY',(30,25,40),f'{p}% under the line','Wait for it'
    if p<=3: return 'JUST LATE',(215,70,50),f'{p}% over the line',"So close. Try the next one"
    if p<=9: return 'TOO LATE',(30,25,40),f'{p}% over the line','One last chance!' if ri==3 else ("Did you get all 5 rounds?" if ri==4 else "Its ok. Try the next one")
    return 'WAY OVER',(30,25,40),f'{p}% over the line',"Its ok. Try the next one"
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
perfect_frames=[]
for f in range(N):
    t=f/FPS; ri=max(i for i,r in enumerate(R) if t>=R[i][3] or i==0)
    name,col,line,t0,t1,over=R[ri]; m,edge,inner,neck,bot,SO=V[ri]
    vh,vw=m.shape; X0=VCX-vw//2; Y0=VBOT-vh
    fillh=bot-neck
    start= t0 if ri>0 else 0.0
    u=max(0,(t-start)/(t1-start)); target=line+over/100
    level=min(target, u*target) if ri>0 else (0 if t<0.25 else min(target,(t-0.25)/(t1-0.25)*target))
    if 'SNAP' not in globals(): SNAP={}
    key=ri
    tf=lambda ff_: None
    img=BG.copy()
    # snap: the frame whose level is closest to the line lands exactly on it
    if ri not in SNAP:
        best=None
        for g in range(N):
            tg=g/FPS
            if not (R[ri][3]<=tg<R[ri][4] or (ri==0 and tg<R[0][4])): continue
            ug=max(0,(tg-start)/(t1-start)); lg=min(target,ug*target) if ri>0 else (0 if tg<0.25 else min(target,(tg-0.25)/(t1-0.25)*target))
            if best is None or abs(lg-line)<best[0]: best=(abs(lg-line),g)
        SNAP[ri]=best[1]
    if f==SNAP[ri]: level=line
    liq=np.zeros((vh,vw),bool); ly=int(bot-level*fillh); liq[ly:,:]=True; liq&=inner
    # wobble surface
    L=np.zeros((vh,vw,4),np.uint8); L[liq]=col+(235,)
    surf=liq & ~np.roll(liq,6,axis=0); L[surf]=tuple(min(255,c+60) for c in col)+(255,)
    E=np.zeros((vh,vw,4),np.uint8); E[edge]=(245,240,230,255)
    ol=ndimage.binary_dilation(m,iterations=PX)&~m; O=np.zeros((vh,vw,4),np.uint8); O[ol]=(25,20,40,255); O[SO]=(150,105,55,255); O[SO&~ndimage.binary_erosion(SO,iterations=PX)]=(205,150,80,255)
    O[inner&~liq]=(255,255,255,45)
    img.alpha_composite(Image.fromarray(O),(X0,Y0)); img.alpha_composite(Image.fromarray(L),(X0,Y0)); img.alpha_composite(Image.fromarray(E),(X0,Y0))
    d=ImageDraw.Draw(img)
    # pour stream + tilted potion
    p=POUR[name]; px,py=VCX-p.width+40,Y0-p.height+70
    if level<target: d.rectangle([VCX-14,py+p.height-60,VCX+14,max(py+p.height,Y0+ly)],fill=col+(240,))
    img.alpha_composite(p,(px,py))
    # target line (hidden in round 5 after the reminder)
    show_line = not (ri==4 and t>R[4][3]+0.4)
    yl=Y0+int(bot-line*fillh)
    if show_line:
        rowx=np.where(inner[int(bot-line*fillh)])[0]
        xa,xb=(X0+rowx.min()-20,X0+rowx.max()+20) if len(rowx) else (X0,X0+vw)
        for x in range(xa,xb,40): d.rectangle([x,yl-5,x+24,yl+5],fill=(230,60,60))
    # round badge
    d.rectangle([800,140,1010,250],fill=(24,20,44,230),outline=(201,162,74),width=5)
    fb=F(30); d.text((835,160),'POUR',font=fb,fill=(255,214,90)); d.text((845,205),f'{ri+1}/5',font=F(34),fill=(255,255,255))
    diff=(level-line)*100
    if ri==0 and t<1.2: tbox(img,None,None,'Pause the video','when it hits the line')
    elif ri==4 and t<R[4][3]+0.7: tbox(img,None,None,'Remember the line!',None)
    else:
        st,c2,l1,l2=feedback(diff,ri); tbox(img,st,c2,l1,l2)
        if st=='PERFECT': perfect_frames.append(f)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (20,60,100,150,195,215,270): img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done; perfect frames:',perfect_frames)
