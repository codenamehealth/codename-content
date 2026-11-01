#!/bin/bash
# fin.sh NNN noaudio.mp4 : mux with batch_review audio -> batch_v3, frame-count check, QA sheet
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
src=$(ls $S/pixellab/batch_review/$1_*.mp4); out=$S/pixellab/batch_v3/$(basename $src)
bash $S/fork_hfg5/mux2.sh "$2" "$src" "$out"
for f in "$src" "$out"; do echo "frames $(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $f) $f"; done
python3 $S/fork_hfg5/qa.py "$out" $S/fork_hfg10/qa$1 $3
