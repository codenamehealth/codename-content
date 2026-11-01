#!/bin/bash
# usage: frames.sh file.mp4 outprefix  -> outprefix_sheet.jpg with 4 frames
f=$1; o=$2
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
i=0
for p in 0.05 0.35 0.65 0.95; do
  t=$(awk -v d="$d" -v p="$p" 'BEGIN{printf "%.2f", d*p}')
  ffmpeg -v error -y -ss "$t" -i "$f" -frames:v 1 -vf scale=240:-1 "${o}_$i.jpg"
  i=$((i+1))
done
ffmpeg -v error -y -i ${o}_0.jpg -i ${o}_1.jpg -i ${o}_2.jpg -i ${o}_3.jpg -filter_complex "[0][1][2][3]hstack=4" ${o}_sheet.jpg
echo "$f $d"
