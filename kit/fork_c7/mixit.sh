#!/bin/bash
# mixit.sh dir video_noaudio events_list.json track offset out.mp4
set -e
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
cd $1
python3 -c "import json,sys; e=json.load(open('$3')); e=e['events'] if isinstance(e,dict) else e; json.dump({'events':sorted([list(x) for x in e])},open('ev_mix.json','w'))"
python3 $S/pixellab/mix.py $2 ev_mix.json $S/music_adobe/$4.wav $5 $6 ${7:-0.55}
ffmpeg -nostats -i $6 -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1
ffprobe -v error -show_entries format=duration -of csv=p=0 $6
