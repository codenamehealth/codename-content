import numpy as np, subprocess, random
from PIL import Image, ImageDraw, ImageFont, ImageOps
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; DUR=10.6; N=int(DUR*FPS)
def F(s): return ImageFont.truetype(FONT,s)
rng=random.Random(15)
hub=Image.open(A+'found_hd.gif'); hub.seek(0); g=hub.convert('RGB')
# village square ground: crop the lower part and nearest-upscale (stays crisp pixel art)
S=H/700; c0=560; src=g.crop((c0,380,c0+int(W/S)+1,1080)); BG=src.resize((int(src.width*S),H),Image.NEAREST).crop((0,0,W,H)).convert('RGBA')
def gif(p):
    im=Image.open(A+p); fr=[]
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb=None
    for f in fr:
        b=f.getbbox(); bb=b if bb is None else (min(bb[0],b[0]),min(bb[1],b[1]),max(bb[2],b[2]),max(bb[3],b[3]))
    return [f.crop(bb) for f in fr], im.info.get('duration',100)
SETS=[gif('idle_9.gif'),gif('hollow-walk-front.gif'),gif('hollow-walk-side.gif'),gif('hollow-victory.gif')]
def sized(fr,h,flip):
    o=[]
    for f in fr:
        k=h/f.height; z=f.resize((max(1,int(f.width*k)),int(h)),Image.NEAREST); o.append(ImageOps.mirror(z) if flip else z)
    return o
items=[]; placed=[]; tries=0
TOP=800
while len(items)<200 and tries<60000:
    tries+=1; y=rng.uniform(TOP,H+30); x=rng.uniform(0,W); h=88+(y-TOP)/(H-TOP)*55
    if any(abs(x-px)<h*0.42 and abs(y-py)<h*0.24 for px,py in placed): continue
    placed.append((x,y)); si=rng.choices([0,1,2,3],[5,2,2,1])[0]; fr,d=SETS[si]
    items.append(dict(x=x,y=y,fr=sized(fr,h,rng.random()<0.5),d=d,f0=rng.randrange(len(fr)),mv=False))
# 8 movers, spread out, none at the very edge or under the banner
cand=[i for i,it in enumerate(items) if 80<it['x']<W-80 and it['y']>900]
rng.shuffle(cand); movers=[]
for i in cand:
    if all(abs(items[i]['x']-items[j]['x'])>160 or abs(items[i]['y']-items[j]['y'])>200 for j in movers): movers.append(i)
    if len(movers)==6: break
for i in movers: items[i]['mv']=True
items.sort(key=lambda d:d['y'])
print('crowd',len(items),'movers',sum(it['mv'] for it in items))
ban=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ban)
d.rectangle([70,150,1010,350],fill=(255,226,60,255),outline=(25,20,40,255),width=6)
f=F(44)
for i,t in enumerate(["I bet you can't find","6 moving Hollows"]):
    w=d.textlength(t,font=f); d.text(((W-w)/2,195+i*80),t,font=f,fill=(25,20,40))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
cache={}
for fn in range(N):
    t=fn/FPS; key=int(t*1000/120)%6
    if key not in cache:
        img=BG.copy()
        for it in items:
            k=(it['f0']+key)%len(it['fr']) if it['mv'] else it['f0']
            sp=it['fr'][k]
            sh=Image.new('RGBA',(int(sp.width*0.8),max(6,int(sp.height*0.09))),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([0,0,sh.width-1,sh.height-1],fill=(0,0,0,60))
            img.alpha_composite(sh,(int(it['x']-sh.width/2),int(it['y']-sh.height/2)))
            img.alpha_composite(sp,(int(it['x']-sp.width/2),int(it['y']-sp.height)))
        img.alpha_composite(ban); cache[key]=img.convert('RGB').tobytes()
        if key==0: img.convert('RGB').save('still.png')
    ff.stdin.write(cache[key])
ff.stdin.close(); ff.wait()
import json; json.dump([(it['x'],it['y']) for it in items if it['mv']],open('movers.json','w')); print('done')
