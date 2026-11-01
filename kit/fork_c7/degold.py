"""Dragon hoard fix (Bennett: no gold/coins anywhere, dragon hoards become gummy piles).
Removes the gold coins + gems under the dragon and puts a pile of the four product gummies in their place.
dragon_gummy(frames, ytop, k) -> list of RGBA frames (same size)."""
import sys, random
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
import numpy as np
from matplotlib.colors import rgb_to_hsv
from scipy import ndimage

def hoard_mask(im, ytop):
    x = np.array(im).astype(float) / 255
    hsv = rgb_to_hsv(x[..., :3]); Hh = hsv[..., 0] * 360; S_ = hsv[..., 1]; V = hsv[..., 2]; A_ = x[..., 3] > 0.5
    gold = (Hh >= 20) & (Hh <= 62) & (V >= 0.55) & (S_ > 0.2)
    dkg = (Hh >= 20) & (Hh <= 34) & (V < 0.55) & (S_ > 0.45)          # brown coin outlines
    gem = (Hh > 62) & (Hh < 330) & (S_ > 0.25) & (V > 0.25)
    wht = (S_ < 0.15) & (V > 0.9)
    yy = np.arange(x.shape[0])[:, None] * np.ones((1, x.shape[1]))
    m = A_ & (gold | dkg | gem | wht) & (yy >= ytop)
    return m

def pile(mask, k, seed=5, kinds=('mush', 'acv', 'mel', 'cre')):
    """gummies packed over the mask (centres inside the mask), drawn back to front."""
    h, w = mask.shape
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # dark base so no background shows between gummies
    base = Image.fromarray((ndimage.binary_erosion(mask, iterations=1) * 255).astype(np.uint8), 'L')
    L.paste((70, 30, 40, 255), (0, 0), base)
    G = {kd: up(Image.open(PL + f'gummies/pick_{kd}.png').convert('RGBA'), k) for kd in kinds}
    rr = random.Random(seed)
    ys, xs = np.where(mask)
    if not len(ys): return L
    pts = []
    step = int(11 * k)
    for y in range(ys.min(), ys.max() + 1, max(4, step // 2)):
        for x in range(xs.min(), xs.max() + 1, max(4, step)):
            jx, jy = x + rr.randint(-step // 2, step // 2), y + rr.randint(-step // 3, step // 3)
            if 0 <= jy < h and 0 <= jx < w and mask[jy, jx]: pts.append((jy, jx))
    rr.shuffle(pts); pts.sort(key=lambda p: p[0])
    last = None
    for (y, x) in pts:
        kd = rr.choice([q for q in kinds if q != last]); last = kd
        g = G[kd]
        if rr.random() < 0.5: g = g.transpose(Image.FLIP_LEFT_RIGHT)
        L.alpha_composite(g, (int(x - g.width / 2), int(y - g.height * 0.6)))
    return L

def clean(m, minsz=30):
    m = ndimage.binary_closing(m, iterations=2) & m.copy() | m
    lab, n = ndimage.label(m); sizes = ndimage.sum(m, lab, range(1, n + 1))
    return np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > minsz])

def dragon_gummy(frames, ytop, k, seed=5):
    """per-frame gold mask (restricted to the frame-0 hoard area so fire is untouched), one stable pile behind."""
    m0 = clean(hoard_mask(frames[0], ytop), 30)
    zone = ndimage.binary_dilation(ndimage.binary_closing(m0, iterations=4), iterations=8)
    masks = []
    for f in frames:
        al = np.array(f)[..., 3] > 0
        m = hoard_mask(f, ytop) & zone
        m = ndimage.binary_closing(m, iterations=1) & al
        lab, n = ndimage.label(m); sizes = ndimage.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, [i + 1 for i, s_ in enumerate(sizes) if s_ > 6]); masks.append(m)
    um = np.zeros_like(masks[0])
    for m in masks: um |= m
    P = pile(um, k, seed)
    out = []
    for f, m in zip(frames, masks):
        a = np.array(f).copy(); a[..., 3][m] = 0
        fr = Image.new('RGBA', f.size, (0, 0, 0, 0)); fr.alpha_composite(P); fr.alpha_composite(Image.fromarray(a))
        out.append(fr)
    return out

if __name__ == '__main__':
    fr = [f.convert('RGBA').resize((300, 300), Image.NEAREST) for f in gif_frames(A + 'dragon.gif')]
    d1 = dragon_gummy(fr, 186, 1)
    df = [up(Image.open(p).convert('RGBA'), 3) for p in sorted(glob.glob(SP + 'fork_b5/dragon_fire/*.png'))]
    d2 = dragon_gummy(df, 3 * 74, 1)
    big = Image.new('RGBA', (300 * 2 + df[0].width + 40, 420), (60, 50, 70, 255))
    big.alpha_composite(d1[3], (0, 0)); big.alpha_composite(d1[0], (310, 0)); big.alpha_composite(d2[4], (630, 0))
    up(big, 2).save('tmp/degold.png')
