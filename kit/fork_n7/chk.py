src=open('render_race4.py').read().split('#### ---- v2 render follows')[0]
exec(src)
for sd in [157,1406,1896,2448,3708,3962]:
  st,tl=run_sim(sd); print(sd, round(st['cyrus']['fin'],2), round(st['ray']['fin'],2), round(st['cyrus']['sneak'],2), score(sd), [ (round(s['x']),s['hp']) for s in st['cyrus']['slimes']])
