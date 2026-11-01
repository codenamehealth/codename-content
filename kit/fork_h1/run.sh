#!/bin/bash
# run.sh <name> <needMB> <cmd...> : wait (max ~9 min) for cgroup headroom >= needMB, then render with a 9.5 min cap
cd /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h1
d=/sys/fs/cgroup/memory$(grep ":memory:" /proc/self/cgroup | cut -d: -f3)
n=$1; need=$2; shift 2
for i in $(seq 1 108); do hr=$(( ($(cat $d/memory.limit_in_bytes) - $(cat $d/memory.usage_in_bytes) + $(awk "/^total_inactive_file /{print \$2}" $d/memory.stat)) / 1048576 )); [ "$hr" -gt "$need" ] && break; sleep 5; done
echo "start $(date +%T) headroom ${hr}MB" > log_$n.txt
timeout 570 "$@" >> log_$n.txt 2>&1; echo "EXIT $? $(date +%T)" >> log_$n.txt
