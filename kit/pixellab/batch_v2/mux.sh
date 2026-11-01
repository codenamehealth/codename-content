#!/bin/bash
# mux.sh new_video_noaudio.mp4 source_with_audio.mp4 out.mp4  (reuses the already mixed, -14 LUFS audio)
set -e
ffmpeg -y -loglevel error -i "$1" -i "$2" -map 0:v -map 1:a -c:v copy -c:a copy -shortest "$3"
for f in "$1" "$2" "$3"; do echo "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f") $f"; done
