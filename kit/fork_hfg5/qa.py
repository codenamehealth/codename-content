# qa.py video.mp4 outdir [t_busy] -> audit sheet, full frame at t_busy, LUFS, first-vs-last frame diff
import sys, subprocess, os, re
from PIL import Image, ImageChops, ImageStat
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
v, od = sys.argv[1], sys.argv[2]; tb = sys.argv[3] if len(sys.argv) > 3 else None
os.makedirs(od, exist_ok=True)
subprocess.run(['python3', S + 'pixellab/safezone/audit.py', od + '/audit.jpg', v])
r = subprocess.run(['ffmpeg', '-nostats', '-i', v, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = re.findall(r'I:\s+(-?[\d.]+) LUFS', r); print('LUFS', m[-1] if m else '?')
n = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', v], capture_output=True, text=True).stdout.strip())
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', v, '-vf', f'select=eq(n\\,0)+eq(n\\,{n-1})', '-vsync', '0', od + '/fl_%d.png'])
a = Image.open(od + '/fl_1.png').convert('L'); b = Image.open(od + '/fl_2.png').convert('L')
print('frames', n, 'first-vs-last mean abs diff', round(ImageStat.Stat(ImageChops.difference(a, b)).mean[0], 2))
if tb:
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', tb, '-i', v, '-frames:v', '1', od + '/busy.png'])
