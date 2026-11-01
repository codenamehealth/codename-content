#!/bin/bash
D=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n19
until grep -q '015 exit' $D/queue2.log; do sleep 5; done
cd $D/v077 && rm -f k77_*.png e_*.png && STILL=100,118,125,270,279,284,290,420,429,434,440 python3 r77.py > run.log 2>&1; echo "077 exit $? $(date +%T)"
