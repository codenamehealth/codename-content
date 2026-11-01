import subprocess, sys, numpy as np
def fr(p, n):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'select=eq(n\\,%d)' % n, '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(out, np.uint8).reshape(1920, 1080, 3).astype(int)
a_, b_ = sys.argv[1], sys.argv[2]
for n in map(int, sys.argv[3].split(',')):
    a = fr(a_, n); b = fr(b_, n); d = np.abs(a - b).max(2) > 40; ys, xs = np.nonzero(d)
    print(n, int(d.sum()), (ys.min(), ys.max(), xs.min(), xs.max()) if len(ys) else None)
