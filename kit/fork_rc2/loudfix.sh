#!/bin/bash
# usage: loudfix.sh file.mp4  -> gain to ~-14 LUFS (video copied)
f=$1; I=$(ffmpeg -i "$f" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
g=$(python3 -c "print(round(-14.0-($I),2))"); tmp="${f%.mp4}_lf.mp4"
ffmpeg -y -loglevel error -i "$f" -c:v copy -af "volume=${g}dB,alimiter=limit=0.95" -c:a aac -b:a 192k "$tmp" && mv "$tmp" "$f"
echo "$I -> $(ffmpeg -i "$f" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1)"
