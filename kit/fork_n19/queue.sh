#!/bin/bash
# sequential renders (one video at a time)
D=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n19
while pgrep -f 'r93.py 4962' >/dev/null; do sleep 5; done
echo "077 start $(date +%T)"
cd $D/v077 && rm -f k77_*.png && STILL=118,125,281,290,410,418 python3 r77.py > run.log 2>&1; echo "077 exit $? $(date +%T)"
cd $D/v046 && rm -f k_*.png p_*.png && python3 r46.py 78 > run.log 2>&1; echo "046 exit $? $(date +%T)"
cd $D/v015 && TS=0.0 TSL=1.2 GC=8,8 SA=6.5 SB=0.5 SPD=0.72 PREV=40,45,50,70,75,80,105,110,115,170,175,180 python3 r15.py 1480 > run.log 2>&1; echo "015 exit $? $(date +%T)"
