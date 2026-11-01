#!/bin/bash
# mux.sh video music offset out [trim_start]
V=$1; M=$2; O=$3; OUT=$4; TS=${5:-0}
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
L=$(python3 -c "print(round($D-$TS,2))"); FO=$(python3 -c "print(round($L-0.8,2))")
ffmpeg -y -loglevel error -ss $TS -i "$V" -ss $O -i "music/$M.wav" -filter_complex "[1:a]atrim=0:$L,asetpts=PTS-STARTPTS,afade=t=out:st=$FO:d=0.8,loudnorm=I=-14[a]" -map 0:v -map "[a]" -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k "$OUT" && echo "$OUT $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
