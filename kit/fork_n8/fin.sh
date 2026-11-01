#!/bin/bash
# fin.sh NNN noaudio.mp4 t_sec : mux with current batch_v3 audio into fork_n8/vNNN/NNN_out.mp4, compare frames, grab frame
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
N=$1; NA=$2; T=$3; D=$S/fork_n8/v$N
CUR=$(ls $S/pixellab/batch_v3/${N}_*.mp4)
nf(){ ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$1"; }
bash $S/fork_hfg5/mux2.sh "$NA" "$CUR" $D/${N}_out.mp4
echo "frames old $(nf $CUR) noaudio $(nf $NA) new $(nf $D/${N}_out.mp4)"
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 $D/${N}_out.mp4
ffmpeg -y -loglevel error -ss $T -i $D/${N}_out.mp4 -frames:v 1 $D/chk_new.png
ffmpeg -y -loglevel error -ss $T -i $CUR -frames:v 1 $D/chk_old.png
