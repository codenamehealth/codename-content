import sys, subprocess, os
from PIL import Image
v, out = sys.argv[1], sys.argv[2]; frames = [int(x) for x in sys.argv[3:]]
sel = '+'.join(f'eq(n\\,{n})' for n in frames)
d = os.path.dirname(out) or '.'
for f in os.listdir(d):
    if f.startswith('_q_'): os.remove(os.path.join(d, f))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', v, '-vf', f'select={sel}', '-vsync', '0', os.path.join(d, '_q_%02d.png')])
ims = [Image.open(os.path.join(d, f'_q_{i+1:02d}.png')).resize((432, 768)) for i in range(len(frames))]
s = Image.new('RGB', (432 * len(ims), 768))
for i, im in enumerate(ims): s.paste(im, (i * 432, 0))
s.save(out, quality=85)
