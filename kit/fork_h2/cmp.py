# cmp.py old.mp4 new.mp4 hook_bottom frames... : mean abs diff above / below the hook bottom per frame, saves side-by-side of first frame
import sys, subprocess, numpy as np
from PIL import Image
old, new, hb = sys.argv[1], sys.argv[2], int(sys.argv[3]); frs = [int(x) for x in sys.argv[4:]]
def grab(v, n):
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', v, '-vf', f'select=eq(n\\,{n})', '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(1920, 1080, 3).astype(int)
for n in frs:
    a, b = grab(old, n), grab(new, n)
    print(n, 'above %.2f' % np.abs(a[:hb] - b[:hb]).mean(), 'below %.2f' % np.abs(a[hb:] - b[hb:]).mean(), 'below max-row %.2f' % np.abs(a[hb:] - b[hb:]).mean(axis=(1, 2)).max())
    if n == frs[0]:
        Image.fromarray(np.concatenate([a, b], 1).astype(np.uint8)).resize((1080, 960)).save(f'cmp_{n}.jpg')
