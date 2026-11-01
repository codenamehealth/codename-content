#!/bin/bash
# loud15.sh in.mp4 out.mp4 : integrated -15.0 LUFS, true peak <= -1.5 dBTP (Oct 29 5:25pm level change). Video stream copied.
set -e
I=$(ffmpeg -nostats -i "$1" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(${TGT:--15.0}-($I),2))")
ffmpeg -y -loglevel error -i "$1" -c:v copy -af "volume=${G}dB,alimiter=limit=0.78:level=disabled" -c:a aac -b:a 192k "$2"
ffmpeg -nostats -i "$2" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
