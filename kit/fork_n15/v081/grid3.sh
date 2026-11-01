cd /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n15/v081
for P in "9.0 0.6 170" "8.3 0.55 170"; do set -- $P
 ( SA=$1 SB=$2 VB=$3 python3 r81.py search 0 600 | grep -v "hook bottom" > g6_$1_$2_$3.txt ) &
done; wait; echo GRIDDONE
