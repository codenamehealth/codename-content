import numpy as np, math, json, subprocess, sys
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageChops
D='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/screenshot/'
W,H,FPS,DUR=1080,1920,30,10.9
N=int(FPS*DUR)
# --- background: Royal Castle scene (animated banners), Hollow painted out, blurred like the reference
BGF=[]
for i in range(24):
    g=Image.open(D+f'build/castle_clean_{i:02d}.png').convert('RGB')
    s_=H/g.height; g=g.resize((int(g.width*s_),H),Image.LANCZOS)
    ox=(g.width-W)//2+40; g=g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(9))
    g=Image.blend(g,Image.new('RGB',(W,H),(0,0,0)),0.12).convert('RGBA')
    BGF.append(g)
bg=BGF[0]
# --- bottle
b=Image.open(D+'creatine_bottle_only.png'); b=b.crop(b.getbbox())
BH=570; BW=int(b.width*BH/b.height); b=b.resize((BW,BH),Image.LANCZOS)
TX,TY=540,1003  # target center
# outline from alpha
a=b.split()[3].point(lambda v:255 if v>100 else 0)
pad=30; A=Image.new('L',(BW+2*pad,BH+2*pad),0); A.paste(a,(pad,pad))
outer=A.filter(ImageFilter.MaxFilter(9)); inner=A.filter(ImageFilter.MaxFilter(3))
ring=ImageChops.subtract(outer,inner).filter(ImageFilter.GaussianBlur(1.2))
outline=Image.new('RGBA',ring.size,(255,255,255,0)); outline.putalpha(ring)
glow=Image.new('RGBA',ring.size,(0,0,0,0)); glow.putalpha(ring.filter(ImageFilter.GaussianBlur(8)).point(lambda v:int(v*0.6)))
# shadow under bottle
def rot(img,ang):
    return img.rotate(ang,resample=Image.BICUBIC,expand=True)
# --- text
F=ImageFont.truetype(D+'../npmfont/package/files/anton-latin-400-normal.woff',66)
txt=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(txt)
lines=['SCREENSHOT FOR','FREE GUMMIES']; y=TY+BH//2+60
for ln in lines:
    w=d.textlength(ln,font=F); x=(W-w)/2
    d.text((x+3,y+4),ln,font=F,fill=(0,0,0,150))
    d.text((x,y),ln,font=F,fill=(255,255,255,255),stroke_width=3,stroke_fill=(20,20,20,255))
    y+=76
# --- motion script
def ease_out(t): return 1-(1-t)**3
def lerp(a,b,t): return a+(b-a)*t
hits=[]  # times of bounces for sfx
# Phase A: 0-4.5 slow fall
TA=4.5
startA=(TX,90,0.0); endA=(TX,TY-34,0.0)
# Motion captured frame-by-frame from the reference video, mapped 1.5x onto this canvas, 10.5s -> 10.0s
import json as _j
from scipy.ndimage import median_filter
TR=_j.load(open(D+'ref/track2.json'))
tr=np.array([v[:3] for v in TR],float)
tr[:,2]=median_filter(tr[:,2],5,mode='nearest')
AX,AY,ABIAS=370.5,738.0,12.8
# snap the near-miss at ref frame 195 into an exact line-up (blend the correction in/out over 4 frames)
dx,dy=AX-tr[195,0],AY-tr[195,1]
for k in range(-4,5):
    w=1-abs(k)/5; tr[195+k,0]+=dx*w; tr[195+k,1]+=dy*w
tr[195,0],tr[195,1]=AX,AY; tr[195,2]=ABIAS-360
def pos(t):
    tr_t=min(t*30,len(tr)-1.001)
    i=int(tr_t); u=tr_t-i
    xr,yr,ar=tr[i]*(1-u)+tr[i+1]*u
    if abs(u)<1e-6 or abs(u-1)<1e-6: pass
    return (TX+(xr-AX)*1.5, TY+(yr-AY)*1.5, -(ar-ABIAS))
hits=[]
json.dump(hits,open(D+'build/hits.json','w'))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',D+'build/video_noaudio.mp4'],stdin=subprocess.PIPE)
ox_,oy_=TX-ring.width//2,TY-ring.height//2
BASES=[]
for g in BGF:
    bb=g.copy(); bb.alpha_composite(glow,(ox_,oy_)); bb.alpha_composite(outline,(ox_,oy_)); BASES.append(bb)
prev=[]
for f in range(N):
    t=f/FPS
    x,y,ang=pos(t)
    fr=BASES[int(t/0.2)%24].copy()
    # ghosts when fast
    if prev:
        sp=math.hypot(x-prev[-1][0],y-prev[-1][1])
        if False:
            for gi,(gx,gy,ga) in enumerate(prev[-3:]):
                g=rot(b,ga); al=g.split()[3].point(lambda v,k=gi:int(v*(0.12+0.08*k)))
                g.putalpha(al); fr.alpha_composite(g,(int(gx-g.width/2),int(gy-g.height/2)))
    r=rot(b,ang)
    # drop shadow
    sh=Image.new('RGBA',r.size,(0,0,0,0)); sh.putalpha(r.split()[3].point(lambda v:int(v*0.35)).filter(ImageFilter.GaussianBlur(10)))
    fr.alpha_composite(sh,(int(x-r.width/2)+10,int(y-r.height/2)+18))
    fr.alpha_composite(r,(int(x-r.width/2),int(y-r.height/2)))
    fr.alpha_composite(txt)
    ff.stdin.write(fr.convert('RGB').tobytes())
    prev.append((x,y,ang))
ff.stdin.close(); ff.wait()
fr.convert('RGB').save(D+'build/last.jpg')
print('done',hits)
