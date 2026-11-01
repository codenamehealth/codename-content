#!/bin/bash
# lufs_fix.sh in.mp4 out.mp4 : nudge integrated loudness to about -14
I=$(ffmpeg -i "$1" -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}')
G=$(python3 -c "print(round(-14-($I),2))")
ffmpeg -y -loglevel error -i "$1" -c:v copy -af "volume=${G}dB,alimiter=limit=0.95" -c:a aac -b:a 192k "$2"
echo "in $I gain $G -> $(ffmpeg -i "$2" -af ebur128 -f null - 2>&1 | grep 'I:' | tail -1)"
