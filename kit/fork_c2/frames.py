# frames.py video out.jpg t1 t2 ... -> side by side full-res frames scaled to 540 wide each, with safe zone outline
import sys, subprocess, os
from PIL import Image, ImageDraw
v, out, ts = sys.argv[1], sys.argv[2], sys.argv[3:]
tmp = os.path.dirname(os.path.abspath(out)) + '/_f.png'; ims = []
for t in ts:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', t, '-i', v, '-frames:v', '1', tmp])
    im = Image.open(tmp).convert('RGB'); d = ImageDraw.Draw(im)
    d.line([(70, 250), (1025, 250), (1025, 1110), (887, 1110), (887, 1500), (70, 1500), (70, 250)], fill=(255, 0, 0), width=3)
    ims.append(im.resize((540, 960)))
s = Image.new('RGB', (540 * len(ims), 960))
for i, im in enumerate(ims): s.paste(im, (i * 540, 0))
s.save(out, quality=88)
