# cmp.py new.mp4 old.mp4 y0 t1 t2 ... -> mean abs diff of region y>=y0 per time
import sys, subprocess, numpy as np, tempfile, os
from PIL import Image
new, old, y0 = sys.argv[1], sys.argv[2], int(sys.argv[3]); td = tempfile.mkdtemp()
def fr(v, t, n):
    p = os.path.join(td, n); subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', v, '-frames:v', '1', p]); return np.asarray(Image.open(p).convert('RGB')).astype(int)
for t in sys.argv[4:]:
    a, b = fr(new, t, 'a.png'), fr(old, t, 'b.png'); print(t, round(float(np.abs(a[y0:] - b[y0:]).mean()), 2))
for v in (new, old): print(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout.strip(), v)
