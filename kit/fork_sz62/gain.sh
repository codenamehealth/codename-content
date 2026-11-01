#!/bin/bash
# gain.sh in.mp4 dB out.mp4 : audio gain (limited), video copied; prints integrated loudness
set -e
ffmpeg -y -loglevel error -i "$1" -c:v copy -af "volume=$2dB,alimiter=limit=0.97" -c:a aac -b:a 192k "$3"
ffmpeg -hide_banner -i "$3" -af ebur128 -f null - 2>&1 | grep -A1 "Integrated" | tail -1
