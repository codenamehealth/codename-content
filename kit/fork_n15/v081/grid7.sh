cd /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n15/v081
for P in "8.5 0.6 170 1.05" "7.5 0.8 170 1.08"; do set -- $P
 ( SA=$1 SB=$2 VB=$3 RB=$4 python3 r81.py search 0 400 | grep -v "hook bottom" > g7_$1_$2_$3_$4.txt ) &
done; wait; echo GRIDDONE
