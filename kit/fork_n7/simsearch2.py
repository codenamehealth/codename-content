src=open('render_race4.py').read().split('#### ---- v2 render follows')[0]
exec(src)
st,tl=run_sim(157); print('157', round(st['cyrus']['fin'],2), round(st['ray']['fin'],2), st['cyrus']['sneak'], score(157))
for seed in range(0,4000):
    r=score(seed)
    if not r: continue
    gap,n,L,tch=r
    if gap<=0.17 and set(L)==set(G) and L[-2:]==['ray','cyrus'] and 12.5<tch<15.5:
        st,_=run_sim(seed); print(seed,r,'fin',round(st['cyrus']['fin'],2))
