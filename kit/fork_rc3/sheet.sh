#!/bin/bash
# sheet.sh video out.jpg n  -> n frames tiled (n/2 per row? we use 6 cols)
v=$1; o=$2; n=${3:-12}
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $v)
ffmpeg -y -loglevel error -i $v -vf "fps=$n/$d,scale=216:384,tile=6x$(( (n+5)/6 ))" -frames:v 1 $o
