import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
g=Image.open(A+'found_hd.gif'); s=1920/1080; X0=586; BGF=[]
for i in range(g.n_frames):
    g.seek(i); f=g.convert('RGB').resize((int(1920*s),1920),Image.NEAREST).crop((X0,0,X0+W,H)); BGF.append(f.convert('RGBA'))
BG0=np.asarray(BGF[0].convert('RGB')).astype(float)
hol=Image.open(A+'idle_9.gif'); hol.seek(0); HOL=hol.convert('RGBA'); HOL=HOL.crop(HOL.getbbox())
# (cx, bottom_y, height, visible_top_fraction, clip_left_px, blend, label)
SPOTS=[
 (930, 520, 120, 0.50, 0, 0.74, 'canopy'),
 (880, 760, 135, 1.00, 0, 0.74, 'teal leaves'),
 (420, 880, 130, 0.48, 0, 0.62, 'door window'),
 (40,  1040,210, 1.00, 70,0.72, 'left trunk'),
 (965, 1060,110, 1.00, 0, 0.74, 'right root'),
 (238, 1180,150, 1.00, 0, 0.74, 'door seam'),
 (205, 1700,175, 0.52, 0, 0.72, 'fern'),
]
def make(cx,by,h,vis,clipl,blend):
    sp=HOL.resize((int(HOL.width*h/HOL.height),h),Image.NEAREST)
    a=np.asarray(sp).astype(float); rgb=a[:,:,:3]; al=a[:,:,3]
    x0=int(cx-sp.width/2); y0=by-h
    ys=slice(max(0,y0),min(H,y0+h)); xs=slice(max(0,x0),min(W,x0+sp.width))
    patch=BG0[ys,xs]; avg=patch.reshape(-1,3).mean(0)*0.82
    eyes=(rgb.mean(2)>170)
    out=rgb*(1-blend)+avg*blend
    out[eyes]=rgb[eyes]*0.5+avg*0.5       # dim the glowing eyes: the only tell
    keep=np.zeros(al.shape,bool); keep[:int(h*vis),:]=True; keep[:,:clipl]=False
    al=np.where(keep,al*0.88,0)
    im=Image.fromarray(np.dstack([out,al]).clip(0,255).astype(np.uint8),'RGBA')
    return im,(x0,y0)
LAYERS=[make(*sp[:6]) for sp in SPOTS]
# reveal circles centred on the visible part
CIRC=[]
for (cx,by,h,vis,clipl,_,_),(im,(x0,y0)) in zip(SPOTS,LAYERS):
    bb=im.getbbox(); CIRC.append(((x0+bb[0]+x0+bb[2])/2,(y0+bb[1]+y0+bb[3])/2,max(bb[2]-bb[0],bb[3]-bb[1])/2+28))
order=sorted(range(len(SPOTS)),key=lambda i:CIRC[i][1])
T_REV=7.0; STEP=0.55; T_DONE=T_REV+STEP*len(SPOTS); DUR=T_REV+2.4; N=int(DUR*FPS)
def ctext(img,x,y,t,f,fill=(255,255,255),sw=8):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text((x-w/2,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS; img=BGF[int(t*10)%len(BGF)].copy()
    for im,(x0,y0) in LAYERS: img.alpha_composite(im,(x0,y0)) if x0>=0 else img.alpha_composite(im.crop((-x0,0,im.width,im.height)),(0,y0))
    d=ImageDraw.Draw(img)
    if True:
        ctext(img,W/2,150,'HOW MANY',F(76)); ctext(img,W/2,250,'HOLLOWS DO',F(76)); ctext(img,W/2,350,'YOU SEE?',F(76),(255,214,60))
        if 4.0<=t<T_REV:
            n=3-int(t-4.0); ctext(img,W/2,1790,str(max(1,n)),F(80),(255,214,60))
        elif t>=T_REV: ctext(img,W/2,1790,'Comment your answer',F(46))
    if False:
        k=min(len(SPOTS),int((t-T_REV)/STEP)+1)
        for j in order[:k]:
            cx,cy,r=CIRC[j]; tj=T_REV+STEP*order.index(j); pop=1+0.35*max(0,1-(t-tj)/0.2)
            rr=r*pop
            d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=(20,15,35),width=16); d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=(255,60,60),width=9)
        sc=1+0.3*max(0,1-((t-T_REV)%STEP)/0.18) if t<T_DONE else 1+0.3*max(0,1-(t-T_DONE)/0.25)
        ctext(img,W/2,200,str(k),F(int(150*sc)),(255,214,60),10)
        if t>=T_DONE: ctext(img,W/2,1760,'How many did',F(52)); ctext(img,W/2,1830,'you find?',F(52))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (60,240,280,330,380): img.convert('RGB').save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done',round(DUR,2),'count',len(SPOTS))
