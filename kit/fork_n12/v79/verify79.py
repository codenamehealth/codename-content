# verify79.py: count the Hollows that actually move in #79's statue field (statue layer only, no fireflies/hook/timer),
# and list which animation each mover uses. Usage: python3 verify79.py
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'r79.py')).read().split("w = Writer('v79_noaudio.mp4')")[0]
__file__ = os.path.join(HERE, 'r79.py')
exec(src)
import numpy as np
from scipy import ndimage
def statues(t):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    for i in sorted(ACTIVE, key=lambda i: spots[i][1]):
        x, y = spots[i]
        if i in MV:
            fr, ph = MV[i]; tb = t + ph * PER / 3.0; nb = int(tb // PER); u = (tb % PER) / PER
            n = len(fr); pp = u / 0.62 if u < 0.62 else 0.0
            k = int(round((1 - abs(1 - 2 * pp)) * (n - 1))) if u < 0.62 else 0
            spr = fr[k]
            if nb % 2: spr = FLIP[id(spr)]
        else: spr = STAT[i]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
    return np.array(img.convert('RGB')).astype(int)
base = statues(0.0); moving = np.zeros(base.shape[:2], bool)
for f in range(N): moving |= np.abs(statues(f / FPS) - base).sum(-1) > 0
lab, nlab = ndimage.label(ndimage.binary_dilation(moving, iterations=6))
print('moving regions', nlab)
for r in range(1, nlab + 1):
    ys, xs = np.where(lab == r); cx, cy = xs.mean(), ys.max()
    near = min(MV, key=lambda i: (spots[i][0] - cx) ** 2 + (spots[i][1] - cy) ** 2)
    print(' region', r, 'bbox', xs.min(), ys.min(), xs.max(), ys.max(), '-> mover at', tuple(int(v) for v in spots[near]))
NAMES_ = ['hollow_nod', 'hollow_think', 'hollow_panic', 'hollow_dance', 'hollow_frun', 'hollow_sit']
for k, i in enumerate(sorted(MV, key=lambda i: [id(MOV[j]) for j in range(6)].index(id(MV[i][0])))):
    print(' mover', [id(MOV[j]) for j in range(6)].index(id(MV[i][0])), NAMES_[[id(MOV[j]) for j in range(6)].index(id(MV[i][0]))], 'at', tuple(int(v) for v in spots[i]))
print('static statues', len(ACTIVE) - len(MV), 'total', len(ACTIVE))
