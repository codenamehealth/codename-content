#!/bin/bash
D=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n19
cd $D/v046 && rm -f p_*.png && python3 r46.py 78 > run.log 2>&1; echo "046 exit $? $(date +%T)"
cd $D/v015 && TS=0.0 TSL=1.2 GC=8,8 SA=6.5 SB=0.5 SPD=0.72 PREV=40,45,50,70,75,80,105,110,115,170,175,180 python3 r15.py 1480 > run.log 2>&1; echo "015 exit $? $(date +%T)"
