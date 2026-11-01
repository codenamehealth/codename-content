# usage: audit.py out.jpg video1 [video2 ...]  -> 4 frames per video, safe zone overlaid (red = unsafe)
import sys, subprocess, json
from PIL import Image, ImageDraw
W, H = 1080, 1920
def mask():
    m = Image.new('RGBA', (W, H), (255, 0, 0, 90)); d = ImageDraw.Draw(m)
    d.rectangle([70, 250, W - 55, 1110], fill=(0, 0, 0, 0)); d.rectangle([70, 1110, W - 193, 1500], fill=(0, 0, 0, 0))
    d.line([(70, 250), (W - 55, 250), (W - 55, 1110), (W - 193, 1110), (W - 193, 1500), (70, 1500), (70, 250)], fill=(255, 40, 40, 255), width=6)
    return m
M = mask(); out = sys.argv[1]; vids = sys.argv[2:]
tw, th = 270, 480; sheet = Image.new('RGB', (tw * 4, th * len(vids)), (0, 0, 0))
for r, v in enumerate(vids):
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout)
    for c, frac in enumerate((0.08, 0.4, 0.7, 0.95)):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(d * frac), '-i', v, '-frames:v', '1', '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c4/_a.png'])
        im = Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c4/_a.png').convert('RGBA'); im.alpha_composite(M)
        sheet.paste(im.convert('RGB').resize((tw, th)), (c * tw, r * th))
sheet.save(out, quality=85)
