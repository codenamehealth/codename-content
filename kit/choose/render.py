import numpy as np, subprocess, math, random, sys
from PIL import Image, ImageDraw, ImageFont
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; N=269
def F(s): return ImageFont.truetype(FONT,s)
who=sys.argv[1]  # her / him
pr='she' if who=='her' else 'he'
rng=random.Random(5)
# pixel parchment + ornate gold arch frame, drawn at 1/6 res then nearest-upscaled
w,h=180,320; bg=Image.new('RGB',(w,h),(226,206,178)); d=ImageDraw.Draw(bg)
for _ in range(900):
    x,y=rng.randrange(w),rng.randrange(h); c=rng.choice([(218,196,166),(232,214,188),(212,190,160)]); d.point((x,y),fill=c)
def arch(y_base,y_tip,up=True):
    pts=[]
    for i in range(41):
        t=i/40; x=22+t*68
        s=math.sin(t*math.pi/2)
        yy=y_base-(y_base-y_tip)*(s**1.6) if up else y_base+(y_tip-y_base)*(s**1.6)
        pts.append((x,yy))
    return pts+[(180-x,y) for x,y in reversed(pts)]
G=(190,132,64); HL=(238,196,120); SH=(130,86,42)
for col,off in ((SH,1),(G,0),(HL,-1)):
    for pts in (arch(80,16,True),arch(262,306,False)):
        d.line([(x,y+off) for x,y in pts],fill=col,width=2)
    d.line([(22,80+off),(22,262+off)],fill=col,width=2); d.line([(158,80+off),(158,262+off)],fill=col,width=2)
    d.line([(30,92+off),(30,250+off)],fill=col,width=1); d.line([(150,92+off),(150,250+off)],fill=col,width=1)
for cx,cy in ((22,80),(158,80),(22,262),(158,262)):
    for col,off in ((SH,1),(G,0)):
        d.arc([cx-9,cy-9+off,cx+9,cy+9+off],0,360,fill=col,width=2)
    d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=HL)
for cx,cy in ((90,16),(90,306)): d.ellipse([cx-3,cy-3,cx+3,cy+3],fill=G)
BG=bg.resize((W,H),Image.NEAREST).convert('RGBA')
def gif(path):
    im=Image.open(A+path); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=880/fr[0].height
    return [f.resize((int(f.width*k),880),Image.NEAREST) for f in fr], im.info.get('duration',120)
GUIDES=[gif(p) for p in ['idle_5.gif','idle_7.gif','idle_8.gif','idle_6.gif']]
CUTS=[107,147,188,228,N]
def tc(img,y,t,f,fill):
    dd=ImageDraw.Draw(img); ww=dd.textlength(t,font=f); dd.text(((W-ww)/2,y),t,font=f,fill=fill,stroke_width=3,stroke_fill=(246,232,210))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',f'video_{who}.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    img=BG.copy(); t=f/FPS
    if f<CUTS[0]:
        f1=F(54); y=720
        for line in [f'If you know {who},','which guide is',f'{pr} choosing?']:
            tc(img,y,line,f1,(150,92,44)); y+=95
        tc(img,y+50,'(Hand drawn)',F(40),(150,92,44))
    else:
        k=max(i for i in range(4) if f>=CUTS[i]); fr,dur=GUIDES[k]; sp=fr[int(t*1000/dur)%len(fr)]
        sh=Image.new('RGBA',(int(sp.width*0.7),40),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([0,0,sh.width-1,39],fill=(90,60,30,70))
        img.alpha_composite(sh,(W//2-sh.width//2,1555)); img.alpha_composite(sp,(W//2-sp.width//2,1575-sp.height))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (30,120,200): img.convert('RGB').resize((360,640)).save(f'p_{who}_{f}.png')
ff.stdin.close(); ff.wait(); print('done',who)
