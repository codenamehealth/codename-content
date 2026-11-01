#!/bin/bash
# finish.sh dir noaudio.mp4 events.json music offset out.mp4
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
cd $1; python3 $S/pixellab/mix.py $2 $3 $S/music_adobe/$4.wav $5 $6 0.55 >/dev/null
I=$(ffmpeg -i $6 -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
echo "LUFS $I"
if python3 -c "import sys; sys.exit(0 if $I < -14.5 else 1)"; then bash $S/fork_rc2/loudfix.sh $6; fi
python3 $S/pixellab/safezone/audit.py audit.jpg $6
ffprobe -v error -show_entries format=duration -of csv=p=0 $6
n=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $6)
ffmpeg -y -loglevel error -i $6 -vf "select=eq(n\,0)+eq(n\,$((n-1)))" -vsync 0 fl_%d.png
python3 -c "
from PIL import Image
a=Image.open('fl_1.png').resize((405,720)); b=Image.open('fl_2.png').resize((405,720))
s=Image.new('RGB',(820,720)); s.paste(b,(0,0)); s.paste(a,(415,0)); s.save('lastfirst.jpg')"
echo frames $n
