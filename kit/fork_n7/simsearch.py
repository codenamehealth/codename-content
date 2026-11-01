import sys
src=open('render_race4.py').read().split('#### ---- v2 render follows')[0]
exec(src)
res=[]
for seed in list(range(0,4000)):
    r=score(seed)
    if r: res.append((seed,r))
print(len(res))
st,tl=run_sim(157); print('157', st['cyrus']['fin'], st['ray']['fin'], st['cyrus']['sneak'], score(157))
for seed,r in res:
    if r[1]>=4: print(seed,r)
