#!/bin/bash
# usage: fetch.sh idsfile dldir kind(reel|p)
IDS=$1; D=$2; K=$3
cd "$D" || exit 1
while read id; do
  [ -f "sheet_$id.jpg" ] && continue
  for try in 1 2; do
    rm -f "$id".* 
    out=$(timeout 180 yt-dlp -q --no-warnings -f "best[height<=1280]/best" -o "%(id)s.%(ext)s" --print-to-file "%(id)s|views=%(view_count)s|likes=%(like_count)s|dur=%(duration)s|date=%(upload_date)s" meta.txt --no-simulate "https://www.instagram.com/$K/$id/" </dev/null 2>&1)
    f=$(ls "$id".* 2>/dev/null | head -1)
    if [ -n "$f" ]; then
      dur=$(ffprobe </dev/null -v error -show_entries format=duration -of csv=p=0 "$f")
      ffmpeg -nostdin -v error -y -i "$f" -vf "fps=6/${dur},scale=180:320:force_original_aspect_ratio=decrease,pad=180:320:(ow-iw)/2:(oh-ih)/2,tile=6x1" -frames:v 1 -q:v 4 "sheet_$id.jpg"
      echo "$id OK dur=$dur" >> log.txt; rm -f "$f"; break
    fi
    echo "$id FAIL try$try: $(echo "$out" | tail -1 | cut -c1-160)" >> log.txt
    if echo "$out" | grep -qiE "429|rate-limit|login"; then sleep 300; else break; fi
  done
  sleep 18
done < "$IDS"
echo DONE >> log.txt
