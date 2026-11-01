#!/bin/bash
# mux2.sh video_noaudio src_with_audio out : like batch_v2/mux.sh but keeps every video frame (no -shortest)
set -e
ffmpeg -y -loglevel error -i "$1" -i "$2" -map 0:v -map 1:a -c:v copy -c:a copy "$3"
for f in "$1" "$2" "$3"; do echo "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f") $f"; done
