#!/bin/bash
# psn.sh old new : frame ranges with PSNR < 40 (real content changes)
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad; P=$(mktemp -p $S/fork_n8)
ffmpeg -loglevel error -i "$1" -i "$2" -lavfi "[0:v][1:v]psnr=stats_file=$P" -f null -
awk '{for(i=1;i<=NF;i++) if($i~/^psnr_avg/){split($i,b,":"); print NR-1, b[2]}}' $P | awk '$2!="inf" && $2<40 {print $1}' | awk 'NR==1{s=$1;p=$1;next} $1==p+1{p=$1;next} {printf "%d-%d ",s,p; s=$1;p=$1} END{if(NR) printf "%d-%d",s,p; print ""}'
rm -f $P
