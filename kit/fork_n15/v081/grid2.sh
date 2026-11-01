cd /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n15/v081
for P in "9.0 0.6 170" "10.5 0.6 175" "9.0 0.9 165" "11.5 0.8 180"; do set -- $P
 ( SA=$1 SB=$2 VB=$3 python3 r81.py search 0 250 | grep -v "hook bottom" > g2_$1_$2_$3.txt ) &
done; wait; echo GRIDDONE
