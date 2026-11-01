#!/bin/bash
# usage: fin15.sh in.mp4 out.mp4 -> about -15.0 LUFS integrated, true peak <= -1.5 dBTP; video stream copied
in=$1; out=$2
meas() { ffmpeg -i "$1" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2 | awk '{print $2}' | tr '\n' ' '; }
read I0 P0 <<< "$(meas "$in")"
g=$(python3 -c "print(round(-15.0-($I0),2))")
for k in 1 2 3; do
  ffmpeg -y -loglevel error -i "$in" -map 0:v -map 0:a -c:v copy -af "volume=${g}dB,aresample=192000,alimiter=limit=0.75:level=false,aresample=48000" -c:a aac -b:a 192k "$out"
  read I1 P1 <<< "$(meas "$out")"
  ok=$(python3 -c "print(int(abs($I1+15.0)<=0.2 and $P1<=-1.5))")
  [ "$ok" = 1 ] && break
  g=$(python3 -c "print(round($g+(-15.0-($I1)) - (0.5 if $P1>-1.5 else 0),2))")
done
echo "I $I1 LUFS, true peak $P1 dBTP (gain ${g}dB)"
