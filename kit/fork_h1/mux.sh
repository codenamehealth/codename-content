#!/bin/bash
# mux.sh NNN noaudio.mp4 : reuse the current batch_v3 audio (mux2), print frame counts old/new
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad; cd $S/fork_h1
src=$(ls $S/pixellab/batch_v3/$1_*.mp4)
bash $S/fork_hfg5/mux2.sh "$2" "$src" m_$1.mp4
cnt() { ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$1"; }
echo "frames old $(cnt $src) new $(cnt m_$1.mp4) src=$src"
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,duration -of csv=p=0 m_$1.mp4
