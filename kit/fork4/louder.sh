#!/bin/bash
# usage: louder.sh in.mp4 out.mp4  -> measure and lift integrated loudness to ~-14 LUFS
I=$(ffmpeg -i "$1" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-14.2-($I),2))")
ffmpeg -y -loglevel error -i "$1" -c:v copy -af "volume=${G}dB,alimiter=limit=0.95:level=disabled" -c:a aac -b:a 192k "$2"
ffmpeg -i "$2" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1
