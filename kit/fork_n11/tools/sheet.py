# sheet.py video out.jpg step_s [t0 t1] -> grid of frames every step seconds, labelled with time
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw
v, out, step = sys.argv[1], sys.argv[2], float(sys.argv[3])
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v],capture_output=True,text=True).stdout)
t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0; t1 = float(sys.argv[5]) if len(sys.argv) > 5 else dur - 0.01
td = tempfile.mkdtemp()
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(t0),'-to',str(t1),'-i',v,'-vf',f'fps=1/{step},scale=270:480',os.path.join(td,'f%04d.png')])
fs = sorted(os.listdir(td)); cols = 6; rows = (len(fs)+cols-1)//cols
sh = Image.new('RGB',(270*cols,480*rows))
for i,f in enumerate(fs):
    im = Image.open(os.path.join(td,f)).convert('RGB'); d = ImageDraw.Draw(im); d.rectangle([0,0,70,18],fill=(0,0,0)); d.text((3,3),f'{t0+i*step:.1f}s',fill=(255,255,0))
    sh.paste(im,((i%cols)*270,(i//cols)*480))
sh.save(out, quality=80); print(out, len(fs), dur)
