import json,urllib.request,os,sys
T=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'.key')).read().strip()
URL='https://www.epidemicsound.com/a/mcp-service/mcp'
def rpc(method,params=None,sid=None,_id=1):
    body={"jsonrpc":"2.0","id":_id,"method":method}
    if params is not None: body["params"]=params
    h={"Authorization":"Bearer "+T,"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"]=sid
    r=urllib.request.urlopen(urllib.request.Request(URL,data=json.dumps(body).encode(),headers=h),timeout=120)
    sid2=r.headers.get('mcp-session-id') or sid; txt=r.read().decode(); out=None
    for line in txt.splitlines():
        if line.startswith('data:') and line[5:].strip():
            try: out=json.loads(line[5:])
            except: pass
    return out,sid2
def session():
    out,sid=rpc("initialize",{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"claude","version":"1"}})
    h={"Authorization":"Bearer "+T,"Content-Type":"application/json","Accept":"application/json, text/event-stream","Mcp-Session-Id":sid}
    try: urllib.request.urlopen(urllib.request.Request(URL,data=json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}).encode(),headers=h),timeout=30).read()
    except Exception: pass
    return sid
def call(name,args,sid): return rpc("tools/call",{"name":name,"arguments":args},sid,_id=2)[0]
if __name__=='__main__':
    sid=session(); out,_=rpc("tools/list",{},sid,_id=3)
    for t in out['result']['tools']:
        print('##',t['name'],'::',t.get('description','')[:220].replace('\n',' '))
        print('   ',json.dumps(t.get('inputSchema',{}).get('properties',{}))[:400])
