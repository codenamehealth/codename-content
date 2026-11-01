# chk.py NNN new.mp4 frames... : full-size frames + diff of the area below the hook vs the current batch_v3 file
import sys, glob, subprocess, numpy as np
from PIL import Image
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
n, new = sys.argv[1], sys.argv[2]; old = glob.glob(S + f'pixellab/batch_v3/{n}_*.mp4')[0]; ylo = int(sys.argv[3]); fr = [int(x) for x in sys.argv[4:]]
def grab(p, f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'select=eq(n\\,{f})', '-vsync', '0', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3)
for f in fr:
    a, b = grab(old, f), grab(new, f)
    d = np.abs(a.astype(int) - b.astype(int)).max(axis=2)
    rows = np.where(d.max(axis=1) > 24)[0]
    print(f'frame {f}: diff rows {rows.min() if len(rows) else "-"}..{rows.max() if len(rows) else "-"}; mean diff below y{ylo}: {d[ylo:].mean():.2f}')
    Image.fromarray(b).save(f'chk_{n}_{f}.png')
