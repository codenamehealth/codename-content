import json,glob,os,subprocess,sys
from PIL import Image, ImageDraw, ImageFont
P='pixellab'
num=json.load(open(P+'/numbering.json'))
CUT={4,74,94}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
def pick(n):
    for d in ('batch_final','batch_v2'):
        g=glob.glob(f'{P}/{d}/{n:03d}_*.mp4')
        if g: return g[0]
reels=[]
for e in num:
    n=e['num']
    if n in CUT: continue
    f=pick(n)
    if f: reels.append((f'r{n:03d}',f,e['hook']))
if os.path.exists(P+'/deliver/race_v2_16s.mp4'): reels.append(('race_v2',P+'/deliver/race_v2_16s.mp4','Choose your guide before the race starts 🏁 (PICK ONE!)'))
reels.append(('steal','pixellab/safezone/steal_safe.mp4','Whoever gets 3 gummies wins 🍬 (Stealing is allowed. Pick a player)'))
reels.append(('plat','pixellab/safezone/plat_safe.mp4','Pause when he lands it 🌿 (Only 1 frame works)'))
only=set(sys.argv[1:])
out=[]
for name,f,hook in reels:
    if only and name not in only: continue
    d=f'review/{name}'; os.makedirs(d+'/frames',exist_ok=True); os.makedirs(d+'/edges',exist_ok=True)
    stamp=f'{f}:{os.path.getmtime(f)}'
    if os.path.exists(d+'/src.txt') and open(d+'/src.txt').read()==stamp: out.append((name,f,hook)); continue
    for old in glob.glob(d+'/frames/*')+glob.glob(d+'/edges/*')+glob.glob(d+'/sheet_*.jpg'): os.remove(old)
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-vf','fps=2,scale=360:-1',d+'/frames/f_%03d.png'],check=True)
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    # every frame of first and last 0.5s
    subprocess.run(['ffmpeg','-v','error','-y','-t','0.5','-i',f,'-vf','scale=240:-1',d+'/edges/a_%02d.png'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-sseof','-0.5','-i',f,'-vf','scale=240:-1',d+'/edges/z_%02d.png'],check=True)
    fs=sorted(glob.glob(d+'/frames/f_*.png')); W,H=Image.open(fs[0]).size; cols,rows=6,2; n=12
    for k in range(0,len(fs),n):
        sh=Image.new('RGB',(cols*W,rows*(H+30)),(20,20,20)); dr=ImageDraw.Draw(sh)
        for i,ff in enumerate(fs[k:k+n]):
            x=(i%cols)*W; y=(i//cols)*(H+30)
            sh.paste(Image.open(ff),(x,y+30)); dr.text((x+8,y+4),f't={(k+i)/2:.1f}s',fill=(255,230,0),font=font)
        sh.save(d+f'/sheet_{k//n:02d}.jpg',quality=82)
    ed=sorted(glob.glob(d+'/edges/a_*.png'))[:8]+sorted(glob.glob(d+'/edges/z_*.png'))[-8:]
    w,h=Image.open(ed[0]).size; sh=Image.new('RGB',(8*w,2*(h+28)),(20,20,20)); dr=ImageDraw.Draw(sh)
    for i,ff in enumerate(ed):
        x=(i%8)*w; y=(i//8)*(h+28); sh.paste(Image.open(ff),(x,y+28))
        lab=('first' if i<8 else 'last')+f' #{i%8}'; dr.text((x+6,y+3),lab,fill=(0,255,200),font=font)
    sh.save(d+'/edges.jpg',quality=82)
    open(d+'/meta.txt','w').write(f'{dur:.2f}\n{hook}\n'); open(d+'/src.txt','w').write(stamp)
    out.append((name,f,hook))
json.dump(out,open('review/reels.json','w'),ensure_ascii=False)
print(len(out),'reels ready')
