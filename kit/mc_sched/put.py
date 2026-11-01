import json,sys,subprocess,re,os
F=sys.argv[1]; B='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/batch_v2/'
reg='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/mc_sched/hosted.json'
H=json.load(open(reg)) if os.path.exists(reg) else {}
for u in json.load(open(F))['uploads']:
    fn=re.search(r'@(\S+\.mp4)',u['instructions']).group(1)
    n=int(fn[:3])
    r=subprocess.run(['curl','-sS','-o','/dev/null','-w','%{http_code}','-X','PUT','-H','If-None-Match: *','-H','Content-Type: video/mp4','--upload-file',B+fn,u['upload_url']],capture_output=True,text=True)
    print(n,fn,r.stdout,r.stderr[:200])
    if r.stdout=='200': H[str(n)]={'media_id':u['media_id'],'url':u['url'],'file':fn,'confirmed':False}
json.dump(H,open(reg,'w'),indent=1)
print(','.join(json.dumps(H[k]['media_id']) for k in H if not H[k]['confirmed']))
