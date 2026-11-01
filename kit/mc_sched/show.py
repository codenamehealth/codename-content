import json,sys
o=json.load(open('payloads.json'))[int(sys.argv[1])]
print(o['slot'],o['num'],o['slotposts'],o['date'])
for k in ('main','tt','yt'): print(k, json.dumps(o[k],ensure_ascii=False))
