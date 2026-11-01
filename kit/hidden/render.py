import numpy as np, subprocess, random, math
from PIL import Image, ImageDraw, ImageFont, ImageOps
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=41.0; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
rng=random.Random(21)
# --- scene: Royal Castle courtyard, orig rows 200-900, cols 420-814, nearest-upscaled (pixel art stays crisp)
S=H/570; C0=470
BGS=[]
for i in range(24):
    g=Image.open(f'../screenshot/build/castle_clean_{i:02d}.png').convert('RGB').crop((C0,330,C0+int(W/S)+1,900))
    BGS.append(g.resize((int(g.width*S),H),Image.NEAREST).crop((0,0,W,H)).convert('RGBA'))
GROUND=int((585-330)*S)
def gif(path):
    im=Image.open(A+path); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    return [f.crop(bb) for f in fr]
GUIDES=[gif(p) for p in ['idle_5.gif','idle_7.gif','idle_8.gif','idle_6.gif','vic_Victory_Pose.gif','vic_victoryPose.gif','vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif','vic_victoryPose_1.gif']]
DECOY=[gif(p) for p in ['idle_9.gif','hollow-walk-side.gif','hollow-walk-front.gif']]
TARGET=gif('hollow-victory.gif')
POTS=[Image.open(A+f'jar_{n}.png').convert('RGBA') for n in ['acv','creatine','mushroom','melatonin']]
POTS=[p.crop(p.getbbox()) for p in POTS]
def sized(frames,h,flip):
    out=[]
    for f in frames:
        k=h/f.height; g=f.resize((max(1,int(f.width*k)),int(h)),Image.NEAREST)
        out.append(ImageOps.mirror(g) if flip else g)
    return out
def size_at(y): return 80+ (y-GROUND)/(H-GROUND)*70
# --- crowd placement (dense, painter's order by feet y)
items=[]; placed=[]
TX,TY=286,1395   # target feet position (next to the training dummy, behind a guide)
tries=0
while len(items)<240 and tries<40000:
    tries+=1
    y=rng.uniform(GROUND+60,H+40); x=rng.uniform(-10,W+10)
    h=size_at(y); w=h*0.65
    if any(abs(x-px)<w*0.62 and abs(y-py)<h*0.30 for px,py in placed): continue
    if abs(x-TX)<75 and abs(y-TY)<70: continue
    placed.append((x,y)); r=rng.random()
    if r<0.68: fr=sized(rng.choice(GUIDES),h,rng.random()<0.5); kind='g'
    elif r<0.93: fr=sized(rng.choice(DECOY),h*0.92,rng.random()<0.5); kind='d'
    else: fr=[ (lambda p: p.resize((int(p.width*h*0.5/p.height),int(h*0.5)),Image.NEAREST))(rng.choice(POTS)) ]; kind='p'
    items.append(dict(x=x,y=y,fr=fr,ph=rng.randrange(6),k=kind))
th=size_at(TY)*0.92
items.append(dict(x=TX,y=TY,fr=sized(TARGET,th,True),ph=2,k='T'))
# a guide standing just in front, covering the target's legs
items.append(dict(x=TX+28,y=TY+62,fr=sized(GUIDES[3],size_at(TY+62),False),ph=4,k='g'))
items.sort(key=lambda d:d['y'])
print('placed',len(items),'decoys',sum(1 for i in items if i['k']=='d'))
# --- banner
def banner(text1,text2):
    b=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(b)
    x0,y0,x1,y1=90,300,990,470
    d.rounded_rectangle([x0+6,y0+8,x1+6,y1+8],radius=26,fill=(0,0,0,90))
    d.rounded_rectangle([x0,y0,x1,y1],radius=26,fill=(255,255,255,250),outline=(30,30,40,255),width=4)
    f=F(36)
    for i,t in enumerate([text1,text2]):
        if not t: continue
        w=d.textlength(t,font=f); d.text((x0+(760-90-w)/2+60,y0+42+i*60),t,font=f,fill=(25,25,35))
    d.polygon([(800,385-14),(830,385),(800,385+14)],fill=(232,110,40)); d.rectangle([770,380,800,390],fill=(232,110,40))
    ic=sized(TARGET,120,True)[0]; b.alpha_composite(ic,(850,325))
    return b
B1=banner('Only 1% can find','this Hollow'); B2=banner('Follow for more','daily puzzles')
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
cache={}
for f in range(N):
    step=f//5
    key=(step%6, (f//6)%24, f>=N-45)
    if key not in cache:
        img=BGS[key[1]].copy()
        for it in items:
            fr=it['fr'][(key[0]+it['ph'])%len(it['fr'])]
            sh=Image.new('RGBA',(int(fr.width*0.8),max(6,int(fr.height*0.09))),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([0,0,sh.width-1,sh.height-1],fill=(0,0,0,70))
            img.alpha_composite(sh,(int(it['x']-sh.width/2),int(it['y']-sh.height/2)))
            img.alpha_composite(fr,(int(it['x']-fr.width/2),int(it['y']-fr.height)))
        img.alpha_composite(B2 if key[2] else B1)
        cache[key]=img.convert('RGB').tobytes()
        if len(cache)==1: img.convert('RGB').save('still.png')
    ff.stdin.write(cache[key])
ff.stdin.close(); ff.wait(); print('done',len(cache))
