#!/bin/bash
D=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n19
until grep -q '077 exit' $D/queue3.log; do sleep 5; done
cd $D/v046 && rm -f p_*.png e_*.png && python3 r46.py 78 > run.log 2>&1; echo "046 exit $? $(date +%T)"
