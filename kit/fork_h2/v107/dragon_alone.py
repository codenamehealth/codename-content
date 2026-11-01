"""The Dragon without his gold-coin hoard (VETTING r107 / r050: gummy pile or dragon alone; the pile reads as noise at wheel size)."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c7')
from degold import hoard_mask, clean
from PIL import Image
import numpy as np
from scipy import ndimage
def dragon_alone(path):
    im = Image.open(path); im.seek(0); f = im.convert('RGBA').resize((300, 300), Image.NEAREST)
    m = clean(hoard_mask(f, 186), 30); m = ndimage.binary_dilation(m, iterations=1) & (np.arange(300)[:, None] >= 186)
    a = np.array(f).copy(); a[..., 3][m] = 0
    lab, n = ndimage.label(a[..., 3] > 0); sizes = ndimage.sum(a[..., 3] > 0, lab, range(1, n + 1))
    a[..., 3][lab != (1 + int(np.argmax(sizes)))] = 0        # keep the dragon body only (drops stray coin/gem bits)
    out = Image.fromarray(a); return out.crop(out.getbbox())
if __name__ == '__main__':
    d = dragon_alone(sys.argv[1]); kk = 64 / max(d.size)
    c = d.resize((int(d.width * kk), int(d.height * kk)), Image.NEAREST); c = c.resize((c.width * 3, c.height * 3), Image.NEAREST)
    bg = Image.new('RGBA', (c.width + 40, c.height + 40), (40, 90, 110, 255)); bg.alpha_composite(c, (20, 20)); bg.save(sys.argv[2])
