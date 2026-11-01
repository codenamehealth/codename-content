import sys, glob, json, numpy as np
from PIL import Image
d, X0, Y0, U = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]); cells = json.loads(sys.argv[5])
fs = sorted(glob.glob(d + '/*.png'))
a0 = np.array(Image.open(fs[0]).convert('RGB')).astype(int)
ref = {}
for (r, c) in cells:
    x, y = int(X0 + (c + 0.5) * U), int(Y0 + (r + 0.5) * U); ref[(r, c)] = a0[y - 10:y + 10, x - 10:x + 10].reshape(-1, 3)
gone = {}
for i, f in enumerate(fs):
    a = np.array(Image.open(f).convert('RGB')).astype(int)
    for (r, c) in cells:
        if (r, c) in gone: continue
        x, y = int(X0 + (c + 0.5) * U), int(Y0 + (r + 0.5) * U); p = a[y - 10:y + 10, x - 10:x + 10].reshape(-1, 3)
        if np.abs(p - ref[(r, c)]).sum(1).mean() > 120: gone[(r, c)] = i / 10
print({'%d,%d' % k: v for k, v in sorted(gone.items())})
