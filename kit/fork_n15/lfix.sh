#!/bin/bash
# usage: lfix.sh in.mp4 out.mp4 : nudge integrated loudness to -15.0 LUFS, true peak <= -1.5 dBTP (video copied)
IN=$1; OUT=$2
I=$(ffmpeg -nostats -i "$IN" -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-15.0 - ($I), 2))")
ffmpeg -y -loglevel error -i "$IN" -c:v copy -af "volume=${G}dB,alimiter=limit=0.70:level=false:attack=2:release=40" -c:a aac -b:a 192k "$OUT"
ffmpeg -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2 | tr '\n' ' '; echo " gain $G"
