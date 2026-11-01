#!/bin/bash
cd "$(dirname "$0")"; export SIMDUR=18.8
part=$1; i=0
for P in "4.5 2 1.0" "4.5 3 1.2" "5 2 1.4" "5.5 2 1.0" "5 1.5 0.9" "6 2 1.2" "4.5 1.5 0.7" "5.5 3 0.6"; do
  i=$((i+1)); [ $((i % 2)) -ne $part ] && continue
  set -- $P
  SH0=$1 SHV=$2 SHA=$3 python3 srch6.py 0 5000 >> g6_$part.txt
done
echo done >> g6_$part.txt
