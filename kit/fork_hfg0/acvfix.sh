set -e
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
cd $S/fork_hfg0/v5 && timeout 900 python3 r5.py 2081 > /dev/null
cd $S/fork_hfg0/v9 && timeout 900 python3 r9.py > /dev/null
cd $S/fork_hfg1/v14 && timeout 900 python3 r14.py 11 > /dev/null
cd $S/pixellab
for p in "005:$S/fork_hfg0/v5/v5_noaudio.mp4" "009:$S/fork_hfg0/v9/v9_noaudio.mp4" "014:$S/fork_hfg1/v14/v14_noaudio.mp4"; do n=${p%%:*}; na=${p#*:}; out=$(ls batch_v3/${n}_*.mp4); src=$(ls batch_review/${n}_*.mp4)
 ffmpeg -y -loglevel error -i $na -i $src -map 0:v -map 1:a -c copy -t $(ffprobe -v error -show_entries format=duration -of csv=p=0 $na) /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/acv_$n.mp4
 a=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/acv_$n.mp4); c=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $src)
 echo "$n new=$a review=$c"; [ "$a" = "$c" ] && mv /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/acv_$n.mp4 $out && echo "$n | Oct 29 cleanup: ACV GUMMY tag removed (consistency rule); full frame count kept ($a)" >> batch_v3/log.txt
done
