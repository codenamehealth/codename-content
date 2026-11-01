# sheet.py out.jpg frac vid... -> clean frames (no mask) at given fraction, side by side
import sys, subprocess, tempfile, os
from PIL import Image
out, frac = sys.argv[1], float(sys.argv[2]); vids = sys.argv[3:]
t = tempfile.mkdtemp(); tw, th = 360, 640
sh = Image.new('RGB', (tw * len(vids), th))
for i, v in enumerate(vids):
    d = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v],capture_output=True,text=True).stdout)
    p = os.path.join(t, f'{i}.png'); subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(d*frac),'-i',v,'-frames:v','1',p])
    sh.paste(Image.open(p).convert('RGB').resize((tw, th)), (i * tw, 0))
sh.save(out, quality=85)
