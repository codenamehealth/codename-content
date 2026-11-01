import sys, glob, subprocess, numpy as np
from PIL import Image
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
n, new, f = sys.argv[1], sys.argv[2], int(sys.argv[3]); old = sys.argv[4] if len(sys.argv) > 4 else glob.glob(S + f'pixellab/batch_v3/{n}_*.mp4')[0]
def grab(p, f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'select=eq(n\\,{f})', '-vsync', '0', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3)
a, b = grab(old, f), grab(new, f); d = (np.abs(a.astype(int) - b.astype(int)).max(axis=2) > 24)
s = Image.new('RGB', (1620, 960)); s.paste(Image.fromarray(a).resize((540, 960)), (0, 0)); s.paste(Image.fromarray(b).resize((540, 960)), (540, 0)); s.paste(Image.fromarray((d * 255).astype(np.uint8)).resize((540, 960)), (1080, 0)); s.save(f'side_{n}_{f}.jpg')
