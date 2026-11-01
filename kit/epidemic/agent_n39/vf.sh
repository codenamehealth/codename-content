#!/bin/bash
# vf.sh local.mp4 fileid... : download each static.metricool.com media and cmp with local
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad; f=$1; shift
for u in "$@"; do o=$S/epidemic/agent_n39/vf/$u.mp4; curl -s -o $o https://static.metricool.com/planner/202610/7178389-file-$u.mp4; echo "$u $(stat -c %s $o) $(cmp -s $o $f && echo IDENTICAL || echo DIFF)"; rm -f $o; done
