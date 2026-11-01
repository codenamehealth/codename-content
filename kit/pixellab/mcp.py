import json,sys,urllib.request,os
T=open(os.path.join(os.path.dirname(__file__),'.token')).read().strip()
URL='https://api.pixellab.ai/mcp'
def rpc(method,params=None,sid=None,_id=1):
    body={"jsonrpc":"2.0","id":_id,"method":method}
    if params is not None: body["params"]=params
    h={"Authorization":"Bearer "+T,"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"]=sid
    r=urllib.request.urlopen(urllib.request.Request(URL,data=json.dumps(body).encode(),headers=h),timeout=300)
    sid2=r.headers.get('mcp-session-id') or sid
    txt=r.read().decode()
    out=None
    for line in txt.splitlines():
        if line.startswith('data:'):
            try: out=json.loads(line[5:])
            except: pass
    if out is None and txt.strip():
        try: out=json.loads(txt)
        except: out={'raw':txt[:2000]}
    return out,sid2
def session():
    out,sid=rpc("initialize",{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"claude","version":"1"}})
    h={"Authorization":"Bearer "+T,"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"]=sid
    try: urllib.request.urlopen(urllib.request.Request(URL,data=json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}).encode(),headers=h),timeout=60).read()
    except Exception as e: pass
    return sid
def call(name,args,sid):
    out,_=rpc("tools/call",{"name":name,"arguments":args},sid,_id=2)
    return out
if __name__=='__main__':
    sid=session()
    out,_=rpc("tools/list",{},sid,_id=3)
    for t in out['result']['tools']:
        print('##',t['name'],'::',t.get('description','')[:300].replace('\n',' '))
        print('   params:',json.dumps(t.get('inputSchema',{}).get('properties',{}))[:600])
