import numpy as np, subprocess, math, random
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
P=6
def gif(p,h):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    fr=[f.crop(bb) for f in fr]; k=h/fr[0].height
    return [f.resize((int(f.width*k),h),Image.NEAREST) for f in fr]
R,C,CS=7,26,172          # rows, cols, cell size
MY=560                   # maze top on screen
MX0=320                  # world x of maze left edge (start area to its left)
RAC=[('JOY','idle_5.gif'),('CLEO','idle_7.gif'),('CYRUS','idle_8.gif'),('RAYLEIGH','idle_6.gif')]
START_ROWS=[0,2,4,6]
SPR=[gif(p,150) for _,p in RAC]
HOL=gif('idle_9.gif',160)
WIN=2   # Cyrus
VIC=gif('vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif',640)
GUM=Image.open('../gummy/mush_gummy_single.png'); GUM=GUM.resize((112,int(GUM.height*112/GUM.width)),Image.LANCZOS)
# ---------- maze: perfect maze + extra openings (braided), right edge open
def build(seed):
    rng=random.Random(seed)
    right=np.ones((R,C),bool); down=np.ones((R,C),bool); seen=np.zeros((R,C),bool)
    st=[(rng.randrange(R),0)]; seen[st[0]]=True
    while st:
        r,c=st[-1]; nb=[(r+dr,c+dc) for dr,dc in ((0,1),(1,0),(0,-1),(-1,0)) if 0<=r+dr<R and 0<=c+dc<C and not seen[r+dr,c+dc]]
        if not nb: st.pop(); continue
        # bias toward horizontal corridors
        nb.sort(key=lambda q: rng.random()*(0.6 if q[0]==r else 1.0))
        nr,nc=nb[0]
        if nr==r: right[r,min(c,nc)]=False
        else: down[min(r,nr),c]=False
        seen[nr,nc]=True; st.append((nr,nc))
    for _ in range(int(R*C*0.22)):
        r,c=rng.randrange(R),rng.randrange(C-1)
        if rng.random()<0.6: right[r,c]=False
        elif r<R-1: down[r,c]=False
    right[:,C-1]=False
    return right,down
def nbrs(r,c,right,down):
    if c<C-1 and not right[r,c]: yield (r,c+1)
    if c>0 and not right[r,c-1]: yield (r,c-1)
    if r<R-1 and not down[r,c]: yield (r+1,c)
    if r>0 and not down[r-1,c]: yield (r-1,c)
def bfs(s,right,down):
    prev={s:None}; q=deque([s])
    while q:
        u=q.popleft()
        if u[1]==C-1:
            path=[];
            while u: path.append(u); u=prev[u]
            return path[::-1]
        for v in nbrs(*u,right,down):
            if v not in prev: prev[v]=u; q.append(v)
for seed in range(200):
    RIGHT,DOWN=build(seed)
    PATHS=[bfs((r,0),RIGHT,DOWN) for r in START_ROWS]
    L=[len(p) for p in PATHS]
    if max(L)-min(L)<=8 and min(L)>=C+6: break
print('seed',seed,'path lens',L)
def cxy(cell): r,c=cell; return MX0+c*CS+CS/2, MY+r*CS+CS/2
# full route: start pad -> path -> run out past the exit to the finish flag
FINX=MX0+C*CS+170
def route(i):
    p=PATHS[i]; pts=[(MX0-150,cxy(p[0])[1])]+[cxy(c) for c in p]+[(FINX,cxy(p[-1])[1])]
    return pts
ROUTES=[route(i) for i in range(4)]
# items placed on cells only one racer uses
used=[set(p) for p in PATHS]
def solo_cell(i,frac):
    p=PATHS[i]; k0=int(len(p)*frac)
    for d in range(0,len(p)):
        for k in (k0+d,k0-d):
            if 1<k<len(p)-2 and all(p[k] not in used[j] for j in range(4) if j!=i): return k
    return k0
K_HOL=solo_cell(0,0.42)     # Joy runs into a Hollow
K_GUM=solo_cell(WIN,0.50)   # Cyrus grabs a mushroom gummy
K_TRAP=solo_cell(1,0.70)    # Cleo also runs into a Hollow late
print('items',K_HOL,K_GUM,K_TRAP)
# ---------- timing: distance along route (in route points) as a function of time
T_GO=3.6
BASE=[3.35,3.55,3.05,3.4]   # cells per second
def make_s(i):
    n=len(ROUTES[i]); ts=[T_GO]; ss=[0.0]; s=0.0; t=T_GO; dt=1/120
    stun=None; boost=1.0
    while s<n-1:
        v=BASE[i]*boost
        if i==0 and stun is None and s>=K_HOL+1: stun=t
        if i==1 and stun is None and s>=K_TRAP+1: stun=t
        if stun is not None and t-stun<1.3: v=0
        if i==WIN and s>=K_GUM+1: boost=1.75
        s=min(n-1,s+v*dt); t+=dt; ts.append(t); ss.append(s)
    return np.array(ts),np.array(ss)
S=[make_s(i) for i in range(4)]
FIN=[s[0][-1] for s in S]; print('finish',[round(x,2) for x in FIN],'winner',int(np.argmin(FIN)))
assert int(np.argmin(FIN))==WIN
T_END_RACE=min(FIN)+0.9
DUR=T_END_RACE+3.6; N=int(DUR*FPS)
def sat(i,t):
    ts,ss=S[i]; return float(np.interp(t,ts,ss)) if t>=T_GO else 0.0
def pos(i,t):
    s=sat(i,t); pts=ROUTES[i]; k=int(s); u=s-k
    if k>=len(pts)-1: return pts[-1]
    (x0,y0),(x1,y1)=pts[k],pts[k+1]; return x0+(x1-x0)*u, y0+(y1-y0)*u
def stunned(i,t):
    for kk,ii in ((K_HOL,0),(K_TRAP,1)):
        if i==ii:
            ts,ss=S[i]; idx=np.argmax(ss>=kk+1)
            if ss[idx]>=kk+1 and 0<=t-ts[idx]<1.3: return True
    return False
def boosted(i,t):
    if i!=WIN: return False
    ts,ss=S[i]; idx=np.argmax(ss>=K_GUM+1); return ss[idx]>=K_GUM+1 and t>=ts[idx]
# ---------- static art
cg=Image.open(A+'vit_hd.gif'); cg.seek(0); g=cg.convert('RGB'); s_=H/g.height; g=g.resize((int(g.width*s_),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(12))).enhance(0.55).convert('RGBA')
MW=MX0+C*CS+600
maze=Image.new('RGBA',(MW,R*CS+40),(0,0,0,0)); d=ImageDraw.Draw(maze); oy=20
d.rectangle([MX0-260,oy,MW,oy+R*CS],fill=(54,46,70,255))
rng=random.Random(5)
for r in range(R):
    for c in range(-2,C+4):
        x=MX0+c*CS; y=oy+r*CS
        d.rectangle([x+4,y+4,x+CS-4,y+CS-4],outline=(64,56,82,255),width=3)
WALL=(150,112,78,255); WALL2=(92,62,40,255)
def wall(x0,y0,x1,y1):
    d.rectangle([min(x0,x1)-11,min(y0,y1)-11,max(x0,x1)+11,max(y0,y1)+11],fill=WALL2)
    d.rectangle([min(x0,x1)-7,min(y0,y1)-7,max(x0,x1)+7,max(y0,y1)+7],fill=WALL)
for r in range(R):
    for c in range(C):
        x=MX0+c*CS; y=oy+r*CS
        if RIGHT[r,c] and c<C-1: wall(x+CS,y,x+CS,y+CS)
        if DOWN[r,c] and r<R-1: wall(x,y+CS,x+CS,y+CS)
    if r not in START_ROWS: wall(MX0,oy+r*CS,MX0,oy+(r+1)*CS)
wall(MX0-260,oy,MX0+C*CS,oy); wall(MX0-260,oy+R*CS,MX0+C*CS,oy+R*CS)
# start-lane dividers
for r in range(R-1):
    if r in START_ROWS or r+1 in START_ROWS: wall(MX0-260,oy+(r+1)*CS,MX0,oy+(r+1)*CS)
# finish flag stripe
for k,y in enumerate(range(oy,oy+R*CS,32)):
    for j in range(2): d.rectangle([FINX-16+j*16,y,FINX+j*16,y+32],fill=(245,245,245,255) if (k+j)%2 else (20,20,30,255))
MAZE=maze
# coins on ~45% of path cells
allcells=set().union(*used)
COINS={c for c in allcells if rng.random()<0.55 and c not in (PATHS[0][K_HOL],PATHS[WIN][K_GUM],PATHS[1][K_TRAP])}
coin=Image.new('RGBA',(7,7),(0,0,0,0)); dc=ImageDraw.Draw(coin); dc.ellipse([0,0,6,6],fill=(160,100,10,255)); dc.ellipse([1,1,5,5],fill=(255,205,40,255)); dc.point((2,2),fill=(255,250,210,255))
COIN=coin.resize((7*P,7*P),Image.NEAREST)
def first_pass(cell):
    best=1e9
    for i in range(4):
        if cell in used[i]:
            k=PATHS[i].index(cell)+1; ts,ss=S[i]; idx=np.argmax(ss>=k)
            if ss[idx]>=k: best=min(best,ts[idx])
    return best
COIN_T={c:first_pass(c) for c in COINS}
def star(col=(255,230,80)):
    c=Image.new('RGBA',(5,5),(0,0,0,0)); dd=ImageDraw.Draw(c)
    for q in [(2,0),(0,2),(1,2),(2,2),(3,2),(4,2),(2,1),(2,3),(1,4),(3,4)]: dd.point(q,fill=col+(255,))
    return c.resize((5*P,5*P),Image.NEAREST)
STAR=star()
def crown():
    c=Image.new('RGBA',(15,10),(0,0,0,0)); dd=ImageDraw.Draw(c)
    dd.polygon([(0,9),(0,2),(4,5),(7,0),(10,5),(14,2),(14,9)],fill=(255,205,40)); dd.rectangle([0,8,14,9],fill=(200,130,20))
    dd.point((7,4),fill=(230,40,60)); dd.point((3,7),fill=(80,160,255)); dd.point((11,7),fill=(80,160,255))
    return c.resize((15*8,10*8),Image.NEAREST)
CROWN=crown()
def ctext(img,x,y,t,f,fill=(255,255,255),sw=6,center=True):
    dd=ImageDraw.Draw(img); w=dd.textlength(t,font=f); dd.text(((x-w/2) if center else x,y),t,font=f,fill=fill,stroke_width=sw,stroke_fill=(20,15,35))
def campos(t):
    if t<T_GO: return 0
    xs=[pos(i,t)[0] for i in range(4)]
    return min(max(0,(min(xs)+max(xs))/2-540,max(xs)-820),MW-W-200)
conf=[(rng.uniform(0,W),rng.uniform(-1800,0),rng.uniform(250,420),rng.choice([(255,90,90),(255,214,60),(90,200,255),(140,255,140),(220,120,255)])) for _ in range(90)]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for f in range(N):
    t=f/FPS
    if t<T_END_RACE:
        cam=campos(t); img=BG.copy()
        img.alpha_composite(MAZE.crop((int(cam),0,int(cam)+W,MAZE.height)),(0,MY-20))
        dd=ImageDraw.Draw(img)
        for c,tc in COIN_T.items():
            if t<tc:
                x,y=cxy(c); x-=cam
                if -60<x<W+60: img.alpha_composite(COIN,(int(x-COIN.width/2),int(y-COIN.height/2+4*math.sin(t*5+x*0.01))))
        # items
        for (ii,kk,kind) in ((0,K_HOL,'hol'),(1,K_TRAP,'hol'),(WIN,K_GUM,'gum')):
            x,y=cxy(PATHS[ii][kk]); x-=cam
            ts,ss=S[ii]; idx=np.argmax(ss>=kk+1); tt=ts[idx] if ss[idx]>=kk+1 else 1e9
            if kind=='gum' and t<tt-0.12:
                gl=Image.new('RGBA',(200,200),(0,0,0,0)); ImageDraw.Draw(gl).ellipse([0,0,200,200],fill=(255,235,120,int(60+30*math.sin(t*6))))
                img.alpha_composite(gl,(int(x-100),int(y-100)))
                img.alpha_composite(GUM,(int(x-GUM.width/2),int(y-GUM.height/2+6*math.sin(t*4))))
            if kind=='hol' and t<tt+1.3:
                fr=HOL[int(t*8)%len(HOL)]; img.alpha_composite(fr,(int(x+CS*0.05-fr.width/2),int(y+CS/2-6-fr.height)))
        order=sorted(range(4),key=lambda i:pos(i,t)[1])
        for i in order:
            x,y=pos(i,t); x-=cam
            fr=SPR[i][int(t*8+i*2)%len(SPR[i])]
            hop=0 if t<T_GO or stunned(i,t) else int(abs(math.sin(t*12+i))*10)
            img.alpha_composite(fr,(int(x-fr.width/2),int(y+CS/2-10-fr.height-hop)))
            if stunned(i,t):
                for k in range(3):
                    a=2*math.pi*(k/3+t*1.3); img.alpha_composite(STAR,(int(x+math.cos(a)*70-15),int(y-CS*0.62+math.sin(a)*16)))
            if boosted(i,t) and t<FIN[i]:
                for k in range(4):
                    a=(t*4+k*0.25)%1; dd.rectangle([x-90-a*120,y-40+k*20,x-40-a*120,y-40+k*20+P],fill=(255,240,150))
            lab=f'{i+1} {RAC[i][0]}' if t<T_GO else str(i+1)
            ctext(img,x,int(y+CS/2-10-fr.height-hop)-40,lab,F(26 if t<T_GO else 30),(255,214,60),5)
        # popups
        for (ii,kk,txt,col) in ((0,K_HOL,'BONK!',(255,90,80)),(1,K_TRAP,'BONK!',(255,90,80)),(WIN,K_GUM,'ENERGY GUMMY!',(255,214,60))):
            ts,ss=S[ii]; idx=np.argmax(ss>=kk+1)
            if ss[idx]>=kk+1 and 0<=t-ts[idx]<0.9:
                x,y=pos(ii,t); ctext(img,x-cam,int(y-250),txt,F(34),col,5)
        if t<T_GO:
            ctext(img,W/2,250,"WHO'S IN",F(66)); ctext(img,W/2,345,'FIRST PLACE?',F(66))
            n=3-int(t/1.0)
            if t<3.0: ctext(img,W/2,420,str(n),F(100),(255,214,60),8)
            else: ctext(img,W/2,420,'GO!',F(100),(255,214,60),8)
            for i,(nm,_) in enumerate(RAC):
                y=MY+START_ROWS[i]*CS+CS//2-18; pass
        else:
            ctext(img,W/2,300,"WHO'S IN",F(60)); ctext(img,W/2,390,'FIRST PLACE?',F(60))
    else:
        u=t-T_END_RACE; img=BG.copy(); dd=ImageDraw.Draw(img)
        if u<0.12: img=Image.blend(img,Image.new('RGBA',(W,H),(255,255,255,255)),0.8*(1-u/0.12))
        dd=ImageDraw.Draw(img)
        # podium
        px0,px1,py=300,780,1500
        dd.rectangle([px0-8,py-8,px1+8,py+260],fill=(40,40,55)); dd.rectangle([px0,py,px1,py+252],fill=(170,174,190)); dd.rectangle([px0,py,px1,py+30],fill=(205,208,220))
        ctext(img,W/2,py+90,'1',F(110),(255,214,60),8)
        fr=VIC[int(t*8)%len(VIC)]; img.alpha_composite(fr,(int(W/2-fr.width/2),py-fr.height+10))
        cy=py-fr.height-60+int(8*math.sin(t*4)); img.alpha_composite(CROWN,(int(W/2-CROWN.width/2),cy))
        sc=1+0.3*max(0,1-u/0.25)
        ctext(img,W/2,380,'WINNER',F(int(110*sc)),(255,214,60),9)
        ctext(img,W/2,530,f'#{WIN+1} {RAC[WIN][0]}',F(56))
        for x,y0,v,col in conf:
            y=y0+v*u*2.2
            if 0<y<H: dd.rectangle([x,y,x+14,y+20],fill=col)
        if u>1.2: ctext(img,W/2,1810,'DID YOU PICK RIGHT?',F(44))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f%45==0: img.convert('RGB').resize((216,384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait(); print('done',DUR)
