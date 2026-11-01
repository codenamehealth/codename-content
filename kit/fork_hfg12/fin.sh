#!/bin/bash
# fin.sh NAME noaudio.mp4 [t_busy] : NAME = 105..108 or steal_3_gummies / plat_pause_when_he_lands / race_v3
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
src=$(ls $S/pixellab/batch_review/$1*.mp4 | grep -v nochip | head -1); out=$S/pixellab/batch_v3/$(basename $src)
bash $S/fork_hfg5/mux2.sh "$2" "$src" "$out"
for f in "$src" "$out"; do echo "frames $(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $f) $f"; done
python3 $S/fork_hfg5/qa.py "$out" $S/fork_hfg12/qa_$1 $3
