#!/bin/bash
# fin.sh NNN slug noaudio.mp4 busy_t : mux source audio, qa sheet, frame counts
S=/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
src=$S/pixellab/batch_review/$1_$2.mp4; out=$S/pixellab/batch_v3/$1_$2.mp4
bash $S/fork_hfg5/mux2.sh "$3" "$src" "$out"
for f in "$src" "$out"; do echo "frames $(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 $f) $f"; done
python3 $S/fork_hfg5/qa.py "$out" $S/fork_hfg9/qa$1 $4
python3 $S/fork_hfg9/sheet.py $S/fork_hfg9/qa$1/clean.jpg 0.02 "$out" ; for fr in 0.3 0.6 0.9 0.99; do python3 $S/fork_hfg9/sheet.py $S/fork_hfg9/qa$1/c_$fr.jpg $fr "$out"; done
python3 - <<PY
from PIL import Image
ims=[Image.open('$S/fork_hfg9/qa$1/'+n) for n in ['clean.jpg','c_0.3.jpg','c_0.6.jpg','c_0.9.jpg','c_0.99.jpg']]
sh=Image.new('RGB',(360*5,640))
for i,im in enumerate(ims): sh.paste(im,(i*360,0))
sh.save('$S/fork_hfg9/qa$1/strip.jpg',quality=85)
PY
