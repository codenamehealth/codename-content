#!/bin/bash
# swap.sh NNN expected_last_log_lineno "log text"
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad; B=$S/pixellab/batch_v3
N=$1; EXP=$2; MSG=$3
LAST=$(grep -n "^$N " $B/log.txt | tail -1 | cut -d: -f1)
if [ "$LAST" != "$EXP" ]; then echo "CONFLICT: $N latest log line is $LAST, expected $EXP"; grep -n "^$N " $B/log.txt | tail -1 | cut -c1-300; exit 1; fi
CUR=$(ls $B/${N}_*.mp4); BN=$(basename $CUR .mp4); DST=$B/prev/$BN.mp4; i=2
while [ -e "$DST" ]; do DST=$B/prev/${BN}_$i.mp4; i=$((i+1)); done
cp -p "$CUR" "$DST" && cp $S/fork_n8/v$N/${N}_out.mp4 "$CUR" && echo "$N | $MSG" >> $B/log.txt && echo "swapped $CUR (old -> $DST)"
