#!/bin/bash
# fdiff.sh old new : list frame indices whose decoded video differs
paste <(ffmpeg -loglevel error -i "$1" -map 0:v -f framemd5 - | grep -v '^#' | awk -F, '{print $NF}') <(ffmpeg -loglevel error -i "$2" -map 0:v -f framemd5 - | grep -v '^#' | awk -F, '{print $NF}') | awk '$1!=$2{c++; if(!f)f=NR-1; l=NR-1} END{print "differing frames:", c+0, "first", f, "last", l, "total", NR}'
