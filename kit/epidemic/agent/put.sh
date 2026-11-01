#!/bin/bash
# put.sh local.mp4 media_id upload_url
r=$(curl -s -o /dev/null -w "%{http_code}" -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *" --data-binary @$1 "$3"); sleep 1
cl=$(curl -sI https://d2ol7oe51mr4n9.cloudfront.net/user_3JL1Gr5rHOzCnvQ5HbpmsPan7mx/$2.mp4 | grep -i content-length | tr -dc 0-9); echo "$r $2 cf=$cl local=$(stat -c %s $1) $([ "$cl" == "$(stat -c %s $1)" ] && echo MATCH || echo MISMATCH)"
