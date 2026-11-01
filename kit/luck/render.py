import numpy as np, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
# Sun Temple, nearest-upscaled (crisp pixel art), centered on the altar/floor
sg=Image.open(A+'sun_hd.gif'); SB=[]
S=H/1080; cw=int(W/S)
for i in range(sg.n_frames):
    sg.seek(i); g=sg.convert('RGB').crop((960-cw//2,0,960-cw//2+cw,1080)).resize((W,H),Image.NEAREST)
    SB.append(ImageEnhance.Brightness(g).enhance(0.85).convert('RGBA'))
FLOOR=1430
def gif(p,h,crop=None):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames):
        im.seek(i); f=im.convert('RGBA')
        if crop: f=f.crop(crop)
        fr.append(f)
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
CH=470
SIDE=gif('cyrus-walk-side.gif',CH); FRONT=gif('cyrus-walk-front.gif',CH); IDLE=gif('idle_8.gif',CH); VIC=gif('vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif',int(CH*1.08))
HOLD=Image.open(A+'cyrus_hold.png'); HOLD=HOLD.crop(HOLD.getbbox()); HOLD=HOLD.resize((int(HOLD.width*CH/HOLD.height),CH),Image.NEAREST)
GUM=Image.open('../gummy/mush_gummy_single.png'); GUM=GUM.resize((150,int(GUM.height*150/GUM.width)),Image.LANCZOS)
def bob(t): return int(12*math.sin(2*math.pi*1.1*t))
# pixel cup, gold pile and gem drawn at 1/8 scale
P=8
def cup():
    c=Image.new('RGBA',(22,20),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.polygon([(4,1),(17,1),(20,19),(1,19)],fill=(20,12,8,255))
    d.polygon([(5,2),(16,2),(19,18),(2,18)],fill=(217,122,31,255))
    d.polygon([(5,2),(8,2),(6,18),(2,18)],fill=(240,160,70,255))
    d.rectangle([2,15,19,17],fill=(160,80,20,255)); d.rectangle([4,1,17,2],fill=(120,60,15,255))
    d.rectangle([9,7,12,10],fill=(255,214,90,255))
    return c.resize((22*P,20*P),Image.NEAREST)
CUP=cup()
def gold():
    c=Image.new('RGBA',(18,10),(0,0,0,0)); d=ImageDraw.Draw(c)
    for (x,y) in [(1,6),(6,6),(11,6),(3,3),(8,3),(6,0)]:
        d.rectangle([x,y,x+5,y+3],fill=(120,80,10,255)); d.rectangle([x,y,x+4,y+2],fill=(255,200,40,255)); d.point((x+1,y),fill=(255,250,200,255))
    return c.resize((18*P,10*P),Image.NEAREST)
def gem():
    c=Image.new('RGBA',(12,11),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.polygon([(2,0),(9,0),(11,3),(5,10),(0,3)],fill=(30,60,120,255)); d.polygon([(3,1),(8,1),(10,3),(5,9),(1,3)],fill=(110,190,255,255))
    d.polygon([(3,1),(5,1),(3,3)],fill=(230,250,255,255))
    return c.resize((12*P,11*P),Image.NEAREST)
def cutimg(p,w):
    im=Image.open(p).convert('RGBA'); return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
GOLD=cutimg('../gummy/gold_cut.png',240); GEM=cutimg('../gummy/gem_cut.png',175)
CX=[290,540,790]
def ctext(img,y,t,f,fill):
    d=ImageDraw.Draw(img); w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill,stroke_width=6,stroke_fill=(20,15,35))
# shuffle plan: list of (t0,t1,i,j) swaps of cup slots; gummy cup ends in the middle
import random
DURS=[0.8,0.68,0.56,0.46,0.38,0.32,0.28,0.25,0.23,0.22,0.21,0.21,0.21,0.21]; GAPS=[0.1,0.09,0.08,0.07,0.06,0.05,0.04,0.04,0.03,0.03,0.03,0.03,0.03,0.03]
def mk(seed):
    r=random.Random(seed); out=[]; t0=5.2; prev=None
    for d,g in zip(DURS,GAPS):
        p=r.choice([q for q in [(0,1),(1,2),(0,2)] if q!=prev]); prev=p
        out.append((t0,t0+d,p[0],p[1])); t0+=d+g
    return out
def final_slot(sw):
    slot=[0,1,2]
    for _,_,i,j in sw:
        ci=slot.index(i); cj=slot.index(j); slot[ci],slot[cj]=j,i
    return slot
seed=0
while True:
    SW=mk(seed); fs=final_slot(SW)
    # gummy cup must end in the middle, and must have moved off-center at least twice
    if fs[1]==1 and sum(1 for _,_,i,j in SW if 1 in (i,j))>=8: break
    seed+=1
SEND=SW[-1][1]; PAUSE=0.8; D=SEND-8.4+PAUSE
def remap(t):
    if t<5.2: return t
    if t<SEND: return 5.2+(t-5.2)*(2.9/(SEND-5.2))
    return t-D
print('seed',seed,'shuffle end',round(SEND,2),'shift',round(D,2))
def cup_pos(t):
    slot=[0,1,2]  # slot[c] for cup c
    pos={c:(CX[slot[c]],0) for c in range(3)}
    for t0,t1,i,j in SW:
        if t<t0: break
        ci=slot.index(i); cj=slot.index(j)
        if t<t1:
            u=(t-t0)/(t1-t0); e=u*u*(3-2*u)
            xi=CX[i]+(CX[j]-CX[i])*e; xj=CX[j]+(CX[i]-CX[j])*e; arc=math.sin(e*math.pi)*90
            pos={c:(CX[slot[c]],0) for c in range(3)}; pos[ci]=(xi,-arc); pos[cj]=(xj,arc*0.4)
            return pos,slot
        slot[ci],slot[cj]=j,i
    return {c:(CX[slot[c]],0) for c in range(3)},slot
# make sure the gummy cup (cup 1, starts middle) ends in the middle
_,fs=cup_pos(99); assert fs[1]==1, fs
DUR=10.4+D; N=int(DUR*FPS)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
def anim(fr,t,ms=100): return fr[int(t*1000/ms)%len(fr)]
for f in range(N):
    rt=f/FPS; img=SB[int(rt*10)%len(SB)].copy(); t=remap(rt)
    cupY=FLOOR-CUP.height
    lift=[0,0,0]; show_gummy=False; show_side=False; cupsvis=True
    # --- Cyrus
    cy=None
    if t<1.6: cy=(anim(IDLE,t),540,FLOOR-140)
    elif t<2.4: cy=(anim(IDLE,t),540,FLOOR-140)
    elif t<4.0: u=(t-2.4)/1.6; cy=(anim(SIDE,t),540+int(u*700),FLOOR-140)
    elif t<5.0: u=(t-4.0)/1.0; cy=(anim(FRONT,t),540,int(FLOOR-140-(1-u)*260))
    elif t<8.6: cy=(anim(IDLE,t),540,FLOOR-140)
    elif t<10.0: cy=(anim(VIC,t),540,FLOOR-140)
    elif t<10.8: cy=(anim(IDLE,t),540,FLOOR-140)
    elif t<12.4: u=(t-10.8)/1.6; cy=(anim(SIDE,t),540+int(u*700),FLOOR-140)
    elif t<14.4: cy=None
    else: u=min(1,(t-14.4)/0.6); cy=(anim(SIDE,t).transpose(Image.FLIP_LEFT_RIGHT),1240-int(u*700),FLOOR-60)
    behind = cy is not None and 2.4<=t<12.4
    if cy and behind:
        sp,x,yb=cy; img.alpha_composite(sp,(x-sp.width//2,yb-sp.height))
    # --- table items
    pos,slot=cup_pos(rt)
    if t>=8.6: lift[1]=1
    if t>=99: lift[0]=lift[2]=1
    gx,gy=540,FLOOR-GUM.height-34+bob(t)
    if 1.6<=t<14.4 or (t>=14.4 and t<14.8):
        if (t>=8.6 and t<14.9) or (1.6<=t<2.3): img.alpha_composite(GUM,(gx-GUM.width//2,gy))
    if False:
        img.alpha_composite(GEM,(CX[0]-GEM.width//2,FLOOR-GEM.height)); img.alpha_composite(GOLD,(CX[2]-GOLD.width//2,FLOOR-GOLD.height))
    if t<12.4 or True:
        for c in range(3):
            x,dy=pos[c]
            if t<1.6 and c==1: y=cupY-260   # middle cup waits above, then drops over the gummy
            elif 1.6<=t<2.2 and c==1: u=(t-1.6)/0.6; y=cupY-260+int(260*u*u)
            else: y=cupY+int(dy)
            if c==1 and t>=8.6:
                if t>=8.95: continue
                y=cupY-int(220*(t-8.6)/0.35)
            if c!=1 and t>=99:
                if t>=10.35: continue
                y=cupY-int(220*(t-10.0)/0.35)
            if t>=11.6 and c!=1: continue   # side cups gone with the loot
            img.alpha_composite(CUP,(int(x-CUP.width//2),int(y)))
    if cy and not behind:
        sp,x,yb=cy
        if t<1.6: img.alpha_composite(sp,(x-sp.width//2,yb-sp.height))
        else:
            img.alpha_composite(sp,(x-sp.width//2,yb-sp.height))
            if t>=14.4: img.alpha_composite(GUM,(x-GUM.width//2-60,yb-sp.height//2+bob(t)))
    if False:
        sp,x,yb=cy; img.alpha_composite(GOLD,(x-GOLD.width//2,yb-sp.height-GOLD.height+10)); img.alpha_composite(GEM,(x-GEM.width//2,yb-sp.height-GOLD.height-GEM.height+20))
    if False:
        ImageDraw.Draw(img).rectangle([536,FLOOR-140-CH-110,548,FLOOR-140-CH-40],fill=(235,60,50)); ImageDraw.Draw(img).rectangle([536,FLOOR-140-CH-30,548,FLOOR-140-CH-18],fill=(235,60,50))
    if t<1.6:
        u=min(1,max(0,(t-1.2)/0.4)); hy=FLOOR-140-CH//2+20; fy=int(hy+(gy-hy)*u*u)
        img.alpha_composite(GUM,(540-GUM.width//2+int(60*(1-u)),fy))
    ctext(img,250,'Find the gummy',F(72),(255,255,255))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%45==0: img.convert('RGB').resize((270,480)).save(f'p_{f}.png')
ff.stdin.close(); ff.wait(); print('done')
