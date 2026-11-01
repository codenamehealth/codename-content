import sys,glob,subprocess,os
from PIL import Image, ImageDraw, ImageFont
for n in sys.argv[1:]:
    f=(glob.glob(f'batch_v3/{n}_*.mp4')+glob.glob(f'batch_v3/{n}.mp4'))[0]; d=f'review2/{n}'
    os.makedirs(d+'/frames',exist_ok=True); os.makedirs(d+'/edges',exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-vf','fps=2,scale=360:-1',d+'/frames/f_%03d.png'])
    subprocess.run(['ffmpeg','-v','error','-y','-t','0.5','-i',f,'-vf','scale=240:-1',d+'/edges/a_%02d.png'])
    subprocess.run(['ffmpeg','-v','error','-y','-sseof','-0.5','-i',f,'-vf','scale=240:-1',d+'/edges/z_%02d.png'])
    fs=sorted(glob.glob(d+'/frames/f_*.png')); W,H=Image.open(fs[0]).size; cols,rows=6,2; k_=cols*rows
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
    for k in range(0,len(fs),k_):
        sh=Image.new('RGB',(cols*W,rows*(H+30)),(20,20,20)); dr=ImageDraw.Draw(sh)
        for i,ff in enumerate(fs[k:k+k_]):
            x=(i%cols)*W; y=(i//cols)*(H+30); sh.paste(Image.open(ff),(x,y+30)); dr.text((x+8,y+4),f't={(k+i)/2:.1f}s',fill=(255,230,0),font=font)
        sh.save(d+f'/sheet_{k//k_:02d}.jpg',quality=85)
    a=sorted(glob.glob(d+'/edges/a_*.png'))[:8]; z=sorted(glob.glob(d+'/edges/z_*.png'))[-8:]
    w,h=Image.open(a[0]).size; e=Image.new('RGB',(8*w,2*h))
    for i,ff in enumerate(a): e.paste(Image.open(ff),(i*w,0))
    for i,ff in enumerate(z): e.paste(Image.open(ff),(i*w,h))
    e.save(d+'/edges.jpg',quality=85)
    dur=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout.strip()
    print(n,dur)
