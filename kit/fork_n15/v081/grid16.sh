cd /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n15/v081
( SHSEP=120 SA=8.0 SB=0.6 VB=170 RB=1.0 python3 r81.py search 0 900 | grep -v "hook bottom" > g16a.txt ) &
( SHSEP=120 SA=8.5 SB=0.6 VB=170 RB=1.05 python3 r81.py search 0 900 | grep -v "hook bottom" > g16b.txt ) &
wait; echo GRIDDONE
