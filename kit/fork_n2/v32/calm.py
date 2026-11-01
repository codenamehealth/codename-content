# #32 Oct 29 notes: the Hollow looked angry and showed teeth. Edit the existing chomp sprite's face only (same pixels/palette):
# teeth (white pixels in the mouth) -> the sprite's own outline colour, so the jaw still chomps but no teeth ever show;
# squinted/angled eyes -> the round eyes the same sprite has in its calm frames (00/03/06): 3-5-5-5-5-3 white with the highlight ring.
import glob, os, numpy as np
from PIL import Image
from scipy import ndimage
SRC = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a3/hollow_chomp/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hollow_calm/')
WH, OL, HI = (227, 230, 255, 255), (6, 6, 8, 255), (64, 51, 83, 255)
ROWS = [(-1, 1), (-2, 2), (-2, 2), (-2, 2), (-2, 2), (-1, 1)]    # round eye, top to bottom, dx ranges around the centre
for f in sorted(glob.glob(SRC + '*.png')):
    a = np.array(Image.open(f).convert('RGBA'))
    isw = np.all(a == WH, axis=2); lab, n = ndimage.label(isw)
    comps = [np.argwhere(lab == k + 1) for k in range(n)]
    comps.sort(key=lambda c: c[:, 0].min())
    eyes = [c for c in comps if c[:, 0].min() <= comps[0][:, 0].min() + 2 and len(c) >= 8][:2]
    eye_bot = max(c[:, 0].max() for c in eyes)
    teeth = [c for c in comps if c[:, 0].min() > eye_bot + 1]
    for c in teeth:
        for y, x in c: a[y, x] = OL
    for c in eyes:
        h = c[:, 0].max() - c[:, 0].min() + 1
        if h >= 6: continue                      # already a round eye
        ys = c[:, 0]; wide = max(set(ys), key=lambda y: (ys == y).sum()); xs = c[ys == wide][:, 1]
        cx = int(round((xs.min() + xs.max()) / 2)); bot = ys.max(); top = bot - 5
        ok = lambda y, x: a[y, x, 3] > 0 and not np.all(a[y, x] == OL)
        eye = np.zeros(isw.shape, bool)
        for i, (l, r) in enumerate(ROWS): eye[top + i, cx + l:cx + r + 1] = True
        ring = ndimage.binary_dilation(eye) & ~eye           # 1px highlight ring like the calm frames
        old = (lab == lab[c[0][0], c[0][1]])
        for y, x in np.argwhere(ring | (old & ~eye)):
            if ok(y, x): a[y, x] = HI
        for y, x in np.argwhere(eye):
            if ok(y, x): a[y, x] = WH
    Image.fromarray(a).save(OUT + os.path.basename(f))
    print(os.path.basename(f), 'teeth px', sum(len(c) for c in teeth), 'eyes h', [int(np.ptp(c[:, 0]) + 1) for c in eyes])
