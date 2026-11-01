import mcp,json,re,time,urllib.request,os,subprocess,sys,threading
from concurrent.futures import ThreadPoolExecutor
def upload(paths):
    sid=mcp.session(); r=mcp.call('get_upload_url',{},sid)
    url=re.search(r'(https://api\.pixellab\.ai/v2/uploads/\S+)',r['result']['content'][0]['text']).group(1)
    out={}
    for p in paths:
        o=subprocess.run(['curl','-sS','-F',f'file=@{p}',url],capture_output=True,text=True).stdout
        out[p]=json.loads(o)['ref']
    return out
def txt(r):
    return ''.join(c.get('text','') for c in r.get('result',{}).get('content',[]) if c.get('type')=='text') if 'result' in r else json.dumps(r)
def run_one(name,tool,args,outdir,log=print):
    for attempt in range(60):
        sid=mcp.session()
        try: r=mcp.call(tool,args,sid)
        except Exception as e: log(name,'submit err',e); time.sleep(10); continue
        t=txt(r)
        if 'rate limit' in t or 'concurren' in t.lower(): time.sleep(8); continue
        m=re.search(r'job_id: (\S+)',t)
        if not m: log(name,'ERR',t[:400]); return None
        jid=m.group(1); break
    else: return None
    while True:
        try: r=mcp.call('get_image',{'job_id':jid},sid)
        except Exception as e: time.sleep(10); sid=mcp.session(); continue
        t=txt(r)
        if 'status: completed' in t:
            n=int(re.search(r'frames: (\d+)',t).group(1)) if 'frames:' in t else 1
            os.makedirs(outdir,exist_ok=True)
            for i in range(n): urllib.request.urlretrieve(f'https://api.pixellab.ai/mcp/images/{jid}/download?index={i}',f'{outdir}/{i:02d}.png')
            ch=re.search(r'charged: .*',t); log(name,'done',n,ch.group(0) if ch else ''); return outdir
        if 'status: failed' in t or 'error' in t[:80].lower(): log(name,'FAILED',t[:300]); return None
        time.sleep(10)
def run_many(jobs,workers=6):
    lock=threading.Lock()
    def lg(*a):
        with lock: print(*a,flush=True)
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda j: run_one(*j,log=lg),jobs))
