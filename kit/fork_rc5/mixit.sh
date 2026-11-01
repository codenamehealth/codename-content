#!/bin/bash
# mixit.sh noaudio.mp4 events.json music_name offset out.mp4 [vol]
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
python3 $S/pixellab/mix.py $1 $2 $S/music_adobe/$3.wav $4 $5 ${6:-0.55} >/dev/null
I=$(ffmpeg -i $5 -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
echo "LUFS $I"
if python3 -c "import sys; sys.exit(0 if $I < -14.5 else 1)"; then bash $S/fork_rc2/loudfix.sh $5; fi
ffprobe -v error -show_entries format=duration -of csv=p=0 $5
