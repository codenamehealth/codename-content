#!/bin/bash
# commit.sh NNN "log text" : back up current to prev/<name>_prehook.mp4 (no clobber), install m_NNN.mp4, append log line
set -e
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad; B=$S/pixellab/batch_v3
src=$(ls $B/$1_*.mp4); base=$(basename $src .mp4); bk=$B/prev/${base}_prehook.mp4; k=2
while [ -e $bk ]; do bk=$B/prev/${base}_prehook$k.mp4; k=$((k+1)); done
cnt() { ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$1"; }
a=$(cnt $src); b=$(cnt $S/fork_h1/m_$1.mp4); [ "$a" = "$b" ] || { echo "FRAME MISMATCH $a $b"; exit 1; }
cp $src $bk; cp $S/fork_h1/m_$1.mp4 $src
echo "$1 | Oct 29 hook: $2 | frames $a -> $b (same), audio reused via fork_hfg5/mux2.sh | backup $bk" >> $B/log.txt
echo "committed $1 -> $src ; backup $bk"; rm $S/fork_h1/m_$1.mp4
