import numpy as np, math, subprocess
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=8.0; N=int(DUR*FPS); SC=10
def native(n,i=0):
    im=Image.open(A+n); im.seek(i); return np.array(im.convert('RGBA'))[5::10,5::10].copy()
SKIN=(149,82,32,255); DARK=(6,6,8,255)
r=native('idle_6.gif',0)
staff=r[:, 58:].copy(); r[:,58:]=0          # take the staff off him
for x0 in (41,48):
    r[31:34,x0:x0+3]=SKIN; r[32,x0:x0+3]=DARK  # closed eyes
r=r[14:80, 28:60]                            # crop head..feet
head=Image.fromarray(r).rotate(90,expand=True)  # lying down, head on the left
staff_img=Image.fromarray(staff[18:76]); staff_img=staff_img.crop(staff_img.getbbox()).rotate(-12,expand=True,resample=Image.NEAREST)
jar=Image.open(A+'jar_melatonin.png').convert('RGBA'); jar=jar.crop(jar.getbbox())
jar=jar.resize((jar.width*14//54, jar.height*14//54), Image.NEAREST)   # ~native scale
# ---- scene drawn at native scale (canvas CW x CH)
SC=9; CW,CH=120,100
M=72                    # mattress top y
BX0,BX1=12,116          # bed extent
def bed():
    c=Image.new('RGBA',(CW,CH),(0,0,0,0)); d=ImageDraw.Draw(c)
    wood=(92,54,30,255); wood2=(52,30,16,255); hi=(128,80,44,255)
    d.rectangle([BX0,M-30,BX0+7,CH-1],fill=wood2); d.rectangle([BX0+1,M-29,BX0+6,CH-2],fill=wood); d.rectangle([BX0+2,M-28,BX0+3,CH-4],fill=hi)
    d.rectangle([BX1-7,M-14,BX1,CH-1],fill=wood2); d.rectangle([BX1-6,M-13,BX1-1,CH-2],fill=wood); d.rectangle([BX1-5,M-12,BX1-4,CH-4],fill=hi)
    d.rectangle([BX0+7,M+8,BX1-7,M+18],fill=wood2); d.rectangle([BX0+8,M+9,BX1-8,M+17],fill=wood)
    d.rectangle([BX0+8,M,BX1-7,M+8],fill=(230,226,240,255)); d.line([(BX0+8,M+8),(BX1-7,M+8)],fill=(170,166,190,255))
    d.rounded_rectangle([BX0+8,M-10,BX0+26,M+1],radius=3,fill=(240,238,250,255),outline=(170,166,190,255))
    return c
def blanket(breath):
    c=Image.new('RGBA',(CW,CH),(0,0,0,0)); d=ImageDraw.Draw(c)
    x0=44; top=M-25-breath
    pts=[(x0,M-9),(x0+4,top+2),(x0+14,top),(x0+40,top+1),(x0+52,top+5),(BX1-6,M-4),(BX1-6,M+7),(x0,M+7)]
    d.polygon(pts,fill=(56,22,78,255))
    pts2=[(x0+1,M-8),(x0+5,top+3),(x0+14,top+1),(x0+40,top+2),(x0+51,top+6),(BX1-7,M-3),(BX1-7,M+6),(x0+1,M+6)]
    d.polygon(pts2,fill=(104,48,140,255))
    for x in range(x0+6,BX1-8,7):
        yy=top+6+int(3*(x-x0)/70); d.point((x,yy),fill=(255,205,60,255)); d.point((x+3,yy+6),fill=(255,205,60,255))
    d.rectangle([x0-2,M-10,x0+3,M+7],fill=(232,214,140,255)); d.line([(x0-2,M-10),(x0-2,M+7)],fill=(150,120,60,255))
    return c
BED=bed()
g=Image.open(A+'recov_hd.gif'); BGS=[]; S=H/1080; cw=int(W/S)
for i in range(0,g.n_frames,2):
    g.seek(i); f=g.convert('RGB').crop((960-cw//2,0,960-cw//2+cw,1080)).resize((W,H),Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.6).convert('RGBA'))
FZ=ImageFont.truetype(FONT,10)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','sleep_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS
    breath=1 if math.sin(2*math.pi*t/2.4)>0 else 0
    can=Image.new('RGBA',(CW,CH),(0,0,0,0))
    can.alpha_composite(staff_img,(1,CH-staff_img.height-1))
    can.alpha_composite(BED)
    hx,hy=BX0+9, M+5-head.height+breath*0
    can.alpha_composite(head,(hx,hy))
    can.alpha_composite(blanket(breath))
    for k in range(3):
        u=((t*0.45)+k/3)%1
        x=hx+20+u*24+3*math.sin(u*6); y=hy-2-u*36; a=int(255*min(1,u*4)*(1-u))
        zl=Image.new('RGBA',can.size,(0,0,0,0)); ImageDraw.Draw(zl).text((x,y),['z','z','Z'][k],font=FZ,fill=(230,230,255,a)); can.alpha_composite(zl)
    big=can.resize((CW*SC,CH*SC),Image.NEAREST)
    img=BGS[int(t*5)%len(BGS)].copy()
    fy=1250; floor=Image.new('RGBA',(W,H-fy),(28,22,44,240)); img.alpha_composite(floor,(0,fy))
    img.alpha_composite(big,(0,fy+120-CH*SC))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (0,40,100): img.convert('RGB').resize((360,640)).save(f's_{f}.png')
ff.stdin.close(); ff.wait(); print('done')
