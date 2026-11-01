import sys,json,os,time,urllib.request
sys.path.insert(0,'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/epidemic')
import es
_sid=None
def sid():
    global _sid
    if _sid is None: _sid=es.session()
    return _sid
def call(name,args):
    global _sid
    for i in range(4):
        try:
            out=es.call(name,args,sid())
        except Exception as e:
            _sid=None; time.sleep(3); continue
        if out is None: _sid=None; time.sleep(2); continue
        r=out.get('result',out)
        if r.get('isError'):
            txt=json.dumps(r)[:600]
            if 'RETRY_LATER' in txt: time.sleep(10); continue
            raise RuntimeError(txt)
        c=r.get('structuredContent')
        if c is None:
            c=json.loads(r['content'][0]['text'])
        return c
    raise RuntimeError('call failed '+name)
def search(term=None,first=20,sort='POPULARITY',filt=None,ext=None):
    q={'externalID':ext} if ext else {'term':term}
    a={'query':q,'first':first}
    if sort: a['sort']={'by':sort,'order':'DESCENDING'}
    if filt: a['filter']=filt
    d=call('SearchRecordings',a)
    d=d.get('data',d)
    rs=[n['recording'] for n in d['recordings']['nodes']]
    cp=os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache.json')
    try: c=json.load(open(cp))
    except Exception: c={}
    for r in rs: c[r['id']]=r
    json.dump(c,open(cp,'w'))
    return rs
def fmt(i,r):
    art=', '.join(c['artist']['name'] for c in r['credits'] if c['role']=='MAIN_ARTIST') or (r['credits'][0]['artist']['name'] if r['credits'] else '?')
    tags=','.join(t['displayName'] for t in r['tags'] if t['dimension']['name'] in ('genre','mood'))[:110]
    vt=[t['displayName'] for t in r['tags'] if t['dimension']['name']=='vocal type']
    voc='-' if vt==['no vocals'] or not vt else 'V:'+'/'.join(vt)
    return f"{i+1:2d} {r['id']} {r['bpm']:3d}bpm {r['audioFile']['durationInMilliseconds']//1000:3d}s {voc} {r['title']} / {art} | {tags}"
if __name__=='__main__':
    term=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 20
    filt=json.loads(sys.argv[3]) if len(sys.argv)>3 else None
    rs=search(term,n,filt=filt)
    for i,r in enumerate(rs): print(fmt(i,r))
