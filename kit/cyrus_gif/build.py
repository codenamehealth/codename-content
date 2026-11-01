from PIL import Image, ImageDraw
import random, math
random.seed(7)
W,H,SC,GY=270,100,4,92   # native canvas, scale, ground y
def L(d,i): return Image.open(f'{d}/{i:02d}.png').convert('RGBA')
RUN=[L('run32',i) for i in range(2,8)]
STOP=[L('stop42',i) for i in range(1,9)]
BR=[L('breath51',i) for i in range(0,13)]
def foot_y(im):
    b=im.getbbox(); return b[3]
LIGHT=(242,232,206,255); MID=(214,196,158,255); SHADE=(168,144,108,255)
class Puff:
    def __init__(s,x,y,vx,vy,r0,r1,life):
        s.x,s.y,s.vx,s.vy,s.r0,s.r1,s.life,s.t=x,y,vx,vy,r0,r1,life,0
        s.subs=[(random.uniform(-1.1,1.1),random.uniform(-0.9,0.1),random.uniform(0.55,0.85)) for _ in range(4)]
    def alive(s): return s.t<s.life
    def draw(s,d):
        p=s.t/s.life
        r=s.r0+(s.r1-s.r0)*min(1,p/0.6)
        if p>0.7: r*= 1-(p-0.7)/0.3*0.75
        cx,cy=s.x+s.vx*s.t, s.y+s.vy*s.t
        blobs=[(cx,cy,r)]+[(cx+ox*r,cy+oy*r,r*k) for ox,oy,k in s.subs]
        for col,dx,dy,shr in ((SHADE,1,1,0),(MID,0,0,0),(LIGHT,-1,-1,1)):
            for bx,by,br in blobs:
                rr=max(0,round(br)-shr)
                if rr<1 and col!=SHADE: continue
                rr=max(rr,1)
                x0,y0=round(bx)+dx,round(by)+dy
                d.ellipse([x0-rr,y0-rr,x0+rr,y0+rr],fill=col)
    def step(s): s.t+=1
def frame(sprite,sx,puffs,front_puffs=()):
    c=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(c)
    for p in puffs: p.draw(d)
    if sprite.getbbox():
        fy=foot_y(sprite); L2=Image.new('RGBA',(W,H),(0,0,0,0)); L2.paste(sprite,(round(sx),GY-fy)); c.alpha_composite(L2)
    d=ImageDraw.Draw(c)
    for p in front_puffs: p.draw(d)
    return c
def heel_x(sprite,sx):
    b=sprite.getbbox(); return sx+b[0]+3
# ---------- GIF 1: run left to right with dust ----------
frames=[];durs=[]
puffs=[]; v=7; x=-92; i=0
while x<W+10:
    spr=RUN[i%6]
    if i%3==0:
        puffs.append(Puff(heel_x(spr,x),GY-3,-0.9,-0.45,2,7.5,15))
    frames.append(frame(spr,x,puffs)); durs.append(80)
    for p in puffs: p.step()
    puffs=[p for p in puffs if p.alive()]
    x+=v; i+=1
# let dust settle a few frames with him gone
for k in range(8):
    frames.append(frame(Image.new('RGBA',(92,92)),-200,puffs)); durs.append(80)
    for p in puffs: p.step()
    puffs=[p for p in puffs if p.alive()]
run_frames,run_durs=frames,durs
# ---------- GIF 2: run in, skid stop, turn to camera, catch breath ----------
frames=[];durs=[]; puffs=[]; fp=[]
TARGET=89; x=-92; i=0
skid_v=[7,6,5,4,3,2,1]   # for STOP frames 1..7
run_until=TARGET-sum(skid_v)
while x<run_until:
    spr=RUN[i%6]
    if i%3==0: puffs.append(Puff(heel_x(spr,x),GY-3,-0.9,-0.45,2,7.5,15))
    frames.append(frame(spr,x,puffs,fp)); durs.append(80)
    for p in puffs+fp: p.step()
    puffs=[p for p in puffs if p.alive()]; fp=[p for p in fp if p.alive()]
    x+=7; i+=1
x=run_until
for k in range(7):
    spr=STOP[k]
    b=spr.getbbox()
    if k>=2:  # skid: big dust kicked forward from the planted front foot
        for n in range(2 if k<5 else 1):
            fp.append(Puff(x+b[2]-4+random.uniform(-2,2),GY-2,random.uniform(0.8,1.8),random.uniform(-0.9,-0.4),2.5,random.uniform(7,10),random.randint(13,18)))
        puffs.append(Puff(x+b[0]+4,GY-2,-0.5,-0.4,2,6.5,13))
    frames.append(frame(spr,x,puffs,fp)); durs.append(90 if k<5 else 110)
    for p in puffs+fp: p.step()
    puffs=[p for p in puffs if p.alive()]; fp=[p for p in fp if p.alive()]
    x+=skid_v[k]
x=TARGET
def push(spr,ms):
    global puffs,fp
    frames.append(frame(spr,x,puffs,fp)); durs.append(ms)
    for p in puffs+fp: p.step()
    puffs=[p for p in puffs if p.alive()]; fp=[p for p in fp if p.alive()]
push(STOP[7],90)          # snaps to face camera
push(BR[0],160)
seq=[1,2,3,4,3,2,3,4,3,2,3,4,5,6,7,8,9,10,11,12]
ms ={1:120,2:170,3:170,4:170,5:130,6:130,7:150,8:150,9:150,10:150,11:130,12:130}
for s in seq: push(BR[s],ms[s])
push(BR[0],1200)          # hold, then loop
stop_frames,stop_durs=frames,durs
# ---------- write GIFs with one shared palette + 1-bit transparency ----------
def save(frs,ds,path):
    cols=set()
    for f in frs:
        for c,a in zip(f.convert('RGB').getdata(),f.getchannel('A').getdata()):
            if a>=128: cols.add(c)
    cols=sorted(cols); assert len(cols)<=255,len(cols)
    pal=[(1,2,3)]+cols  # index 0 transparent
    idx={c:i for i,c in enumerate(pal)}
    flat=[v for c in pal for v in c]+[0]*(768-3*len(pal))
    out=[]
    for f in frs:
        f=f.resize((W*SC,H*SC),Image.NEAREST)
        P=Image.new('P',f.size); P.putpalette(flat)
        P.putdata([idx[c] if a>=128 else 0 for c,a in zip(f.convert('RGB').getdata(),f.getchannel('A').getdata())])
        out.append(P)
    out[0].save(path,save_all=True,append_images=out[1:],duration=ds,loop=0,transparency=0,disposal=2,optimize=False)
    print(path,len(frs),'frames',sum(ds)/1000,'s',len(cols),'colors')
save(run_frames,run_durs,'out/cyrus_run_dust.gif')
save(stop_frames,stop_durs,'out/cyrus_stop_catch_breath.gif')
# preview sheets on a dark bg to check
for name,frs in (('run',run_frames),('stop',stop_frames)):
    n=len(frs); step=max(1,n//12); pick=frs[::step][:12]
    S=Image.new('RGBA',(W*3,H*4),(40,44,60,255))
    for k,f in enumerate(pick): S.alpha_composite(f,((k%3)*W,(k//3)*H))
    S.resize((S.width*2,S.height*2),Image.NEAREST).save(f'prev_{name}.png')
