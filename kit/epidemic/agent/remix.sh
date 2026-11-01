#!/bin/bash
# remix.sh REEL EVENTS.json TRACK.wav VOL  -> work/REEL_es.mp4 (current batch_v3 video, untouched stream, + new mix at -14 LUFS)
set -e
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
A=$S/epidemic/agent; W=$A/work; mkdir -p $W
R=$1; EV=$2; TRK=$3; VOL=${4:-0.5}
SRC=$(ls $S/pixellab/batch_v3/${R}_*.mp4)
python3 $A/mix_es.py "$SRC" "$EV" "$TRK" 0 $W/${R}_mix.mp4 $VOL >/dev/null
bash $A/loudfix_es.sh $W/${R}_mix.mp4
bash $S/fork_hfg5/mux2.sh "$SRC" $W/${R}_mix.mp4 $W/${R}_es.mp4
rm -f $W/${R}_mix.mp4
# video stream must be bit-identical to the current file
a=$(ffmpeg -loglevel error -i "$SRC" -map 0:v -c copy -f md5 -); b=$(ffmpeg -loglevel error -i $W/${R}_es.mp4 -map 0:v -c copy -f md5 -)
fa=$(ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 "$SRC"); fb=$(ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 $W/${R}_es.mp4)
echo "video md5 src=$a out=$b frames $fa/$fb"; [ "$a" == "$b" ] && [ "$fa" == "$fb" ] || { echo VIDEO MISMATCH; exit 3; }
ffmpeg -nostats -i $W/${R}_es.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tr -s ' ' | tr '\n' ' '; echo
python3 $A/check.py $W/${R}_es.mp4 "$EV"
