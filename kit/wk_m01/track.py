import sys, glob, numpy as np
from PIL import Image
COLS = {'yellow': (250, 216, 56), 'cyan': (2, 181, 213), 'green': (1, 122, 88), 'red': (214, 0, 3)}
def find(a, c, tol=18, region=None):
    m = (np.abs(a - np.array(c)).sum(2) < tol)
    if region: x0, y0, x1, y1 = region; mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; m = mm
    ys, xs = np.where(m)
    if len(xs) < 30: return None
    # largest compact blob ~ 25x25: take median then bbox of pixels within 25px
    cx, cy = np.median(xs), np.median(ys); k = (np.abs(xs - cx) < 22) & (np.abs(ys - cy) < 22)
    return (xs[k].min() + xs[k].max()) / 2, (ys[k].min() + ys[k].max()) / 2, xs[k].max() - xs[k].min() + 1
if __name__ == '__main__':
    fs = sorted(glob.glob(sys.argv[1]))
    for f in fs[:int(sys.argv[2])]:
        a = np.array(Image.open(f).convert('RGB')).astype(int)
        print(f[-8:], {n: (None if r is None else tuple(round(v, 1) for v in r)) for n, r in ((n, find(a, c)) for n, c in COLS.items())})
