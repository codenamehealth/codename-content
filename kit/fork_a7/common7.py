import sys, os
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
import numpy as np
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
def slime_frames(k=2):
    return [up(nored(Image.open(p).convert('RGBA')), k) for p in sorted(glob.glob(PL + 'race/slime_idle_c/*.png'))]
def wang(meta_path, sheet_path):
    meta = json.load(open(meta_path)); sheet = Image.open(sheet_path).convert('RGBA'); T = {}
    for t in meta['tileset_data']['tiles']:
        c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
        T[key] = sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height']))
    return T
def loudness(mp4):
    r = subprocess.run(['ffmpeg', '-i', mp4, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    import re
    m = re.findall(r'I:\s+(-?[\d.]+) LUFS', r); return float(m[-1]) if m else None
def louder(src, dst):
    I = loudness(src); g = round(-14.2 - I, 2)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-c:v', 'copy', '-af', f'volume={g}dB,alimiter=limit=0.95:level=disabled', '-c:a', 'aac', '-b:a', '192k', dst])
    return loudness(dst)
