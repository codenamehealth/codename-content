#!/bin/bash
# loudfix_es.sh file.mp4 -> linear gain to -15.0 LUFS (+-0.2), true peak <= -1.5 dBTP; limiter starts at 0.71 and tightens if the AAC encode overshoots
f=$1; T=-15.0; src="${f%.mp4}_src.mp4"; cp "$f" "$src"
meas(){ ffmpeg -nostats -i "$1" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2 | awk '{print $2}' | tr '\n' ' '; }
read I0 _ <<< "$(meas "$src")"; g=$(python3 -c "print(round($T-($I0),2))"); L=0.71
for pass in 1 2 3 4 5 6; do
  ffmpeg -y -loglevel error -i "$src" -c:v copy -af "volume=${g}dB,alimiter=limit=${L}:level=0" -c:a aac -b:a 192k "$f"
  read I TP <<< "$(meas "$f")"
  okI=$(python3 -c "print(1 if abs($I-($T))<=0.2 else 0)"); okP=$(python3 -c "print(1 if $TP<=-1.5 else 0)")
  [ "$okI" == "1" ] && [ "$okP" == "1" ] && break
  [ "$okP" == "0" ] && L=$(python3 -c "print(round($L*0.89,3))")
  [ "$okI" == "0" ] && g=$(python3 -c "print(round($g+($T)-($I),2))")
done
rm -f "$src"; echo "$I0 -> I: $I LUFS TP $TP (gain ${g} dB, limiter $L, pass $pass)"
