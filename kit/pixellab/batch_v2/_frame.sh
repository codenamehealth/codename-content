#!/bin/bash
# _frame.sh video t out.jpg [crop W:H:X:Y]  -> full-res frame (optionally cropped) at half scale
C=${4:-1080:1920:0:0}
ffmpeg -y -loglevel error -ss $2 -i $1 -frames:v 1 -vf "crop=$C" -q:v 3 $3
