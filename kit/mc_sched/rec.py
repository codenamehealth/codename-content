import json,sys,os
f='results.json'; R=json.load(open(f)) if os.path.exists(f) else {}
# usage: rec.py num main_id main_uuid tt_id tt_uuid yt_id yt_uuid
n=sys.argv[1]; a=sys.argv[2:]
R[n]={'main':[a[0],a[1]],'tt':[a[2],a[3]],'yt':[a[4],a[5]]}
json.dump(R,open(f,'w'),indent=1); print(len(R),'done')
