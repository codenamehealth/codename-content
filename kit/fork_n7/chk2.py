src=open('render_race4.py').read().split('#### ---- v2 render follows')[0]
exec(src)
def q(seed):
    st,tl=run_sim(seed); tc=st['cyrus']['sneak']
    if tc is None: return None
    f=int(tc*FPS); dx=tl[f]['ray'][0]-tl[f]['cyrus'][0]
    ratk=[round(t,2) for k,t in st['ray']['events'] if k=='atk']
    busy=[t for t in ratk if tc-1.4<=t<=tc+1.0]
    return round(tc,2), round(dx), ratk, busy
print(1896, q(1896))
for seed in range(4000):
    r=score(seed)
    if not r: continue
    gap,n,L,tch=r
    if gap<=0.17 and set(L)==set(G) and L[-2:]==['ray','cyrus'] and 13.0<tch<15.5:
        qq=q(seed)
        if not qq[3] and abs(qq[1])<450: print(seed,r,qq[:2])
