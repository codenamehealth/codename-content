#!/bin/bash
# commit.sh <batch_v3 basename without .mp4> <noaudio.mp4> <expected frames> <log line>
set -e
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad; B=$S/pixellab/batch_v3; N=$1
nf() { ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 "$1"; }
echo "batch file: $(ls -l --time-style=+%H:%M $B/$N.mp4)"
[ -e $B/prev/${N}_prehook.mp4 ] && { echo "prev/${N}_prehook.mp4 exists, abort"; exit 1; }
out=$(dirname $2)/out.mp4
bash $S/fork_hfg5/mux2.sh "$2" $B/$N.mp4 $out
a=$(nf "$2"); b=$(nf $out); o=$(nf $B/$N.mp4); echo "frames noaudio $a out $b old $o expected $3"
[ "$b" = "$3" ] && [ "$o" = "$3" ] || { echo FRAME MISMATCH; exit 1; }
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 $out | tr '\n' ' '; echo
cp $B/$N.mp4 $B/prev/${N}_prehook.mp4
cp $out $B/$N.mp4
echo "$4" >> $B/log.txt
echo committed; ls -l $B/$N.mp4 $B/prev/${N}_prehook.mp4
