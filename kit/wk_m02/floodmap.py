# per half-cell flood arrival time from the reference frames (10fps): first frame the half-cell is >50% purple
import sys, glob, json, numpy as np
from PIL import Image
d, X0, Y0, U, C, R = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
fs = sorted(glob.glob(d + '/*.png')); P = np.array([60, 49, 139])
T = {}
for i, f in enumerate(fs):
    a = np.array(Image.open(f).convert('RGB')).astype(int)
    m = np.abs(a - P).sum(2) < 60
    for r in range(R * 2):
        for c in range(C * 2):
            if (r, c) in T: continue
            x0, y0 = int(X0 + c * U / 2 + 4), int(Y0 + r * U / 2 + 4); x1, y1 = int(X0 + (c + 1) * U / 2 - 4), int(Y0 + (r + 1) * U / 2 - 4)
            if m[y0:y1, x0:x1].mean() > 0.5: T[(r, c)] = round(i / 10, 1)
json.dump({'%d,%d' % k: v for k, v in T.items()}, open(sys.argv[7], 'w'))
for r in range(R * 2): print('%2d' % r, ' '.join(('%4.0f' % T[(r, c)]) if (r, c) in T else '   .' for c in range(C * 2)))
