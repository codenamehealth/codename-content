# usage: sheet.py out.jpg video [n]  -> n frames evenly spaced, with time labels
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw
out, v = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
ts = sys.argv[4].split(',') if len(sys.argv) > 4 else None
d = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v],capture_output=True,text=True).stdout)
times = [float(t) for t in ts] if ts else [d*(i+0.5)/n for i in range(n)]
tw, th = 270, 480; sh = Image.new('RGB', (tw*len(times), th+24), (0,0,0)); dr = ImageDraw.Draw(sh)
tmp = os.path.join(tempfile.mkdtemp(), 'a.png')
for i, t in enumerate(times):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(t),'-i',v,'-frames:v','1',tmp])
    sh.paste(Image.open(tmp).convert('RGB').resize((tw,th)), (i*tw, 24)); dr.text((i*tw+4,4), f'{t:.2f}s', fill=(255,255,0))
sh.save(out, quality=85); print(d)
