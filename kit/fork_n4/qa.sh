#!/bin/bash
# qa.sh video.mp4 outprefix t1 t2 ... : audit sheet, a strip of frames at the given times, last+first frame pair
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
v=$1; o=$2; shift 2
python3 $S/pixellab/safezone/audit.py ${o}_audit.jpg "$v"
n=$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 "$v")
ffmpeg -y -loglevel error -i "$v" -vf "select=eq(n\,$((n-1)))" -frames:v 1 ${o}_last.png
ffmpeg -y -loglevel error -i "$v" -frames:v 1 ${o}_first.png
i=0; for t in "$@"; do ffmpeg -y -loglevel error -ss $t -i "$v" -frames:v 1 ${o}_k$i.png; i=$((i+1)); done
python3 - "$o" "$#" <<'EOF'
import sys; from PIL import Image
o, k = sys.argv[1], int(sys.argv[2])
c = Image.new('RGB', (360 * k, 640))
for i in range(k): c.paste(Image.open(f'{o}_k{i}.png').resize((360, 640)), (i * 360, 0))
c.save(f'{o}_keys.jpg', quality=85)
c = Image.new('RGB', (720, 640)); c.paste(Image.open(f'{o}_last.png').resize((360, 640)), (0, 0)); c.paste(Image.open(f'{o}_first.png').resize((360, 640)), (360, 0))
c.save(f'{o}_loop.jpg', quality=85)
EOF
echo "frames $n"
