import sys, collections
sys.argv=['n02.py','x']
src=open('n02.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C=collections.Counter()
for seed in range(1,300):
    st_, tl = run_sim(seed); li=int(T_LAND*FPS)
    c, r = st_['cyrus']['fin'], st_['ray']['fin']
    C['cj'] += abs(tl[li]['cleo'][0]-tl[li]['joy'][0])<=220
    fo=max(tl[li]['cleo'][0], tl[li]['joy'][0]); C['ahead'] += min(tl[li]['cyrus'][0], tl[li]['ray'][0]) >= fo+60
    if c and r: C['close'] += (c<r<c+0.22); C['ctime'] += 9.0<c<9.9; C['c%d'%int(c)]+=1
    at=[a for a in attacks(st_) if not (a[2] in OUT_G and a[0]>=T_LAND)]
    C['disj'] += all(b[0]>=a[1]+0.25 for a,b in zip(at,at[1:]))
    C['win'] += all(not (a[1]>T_WARN-0.2 and a[0]<T_OUTEND+0.2) for a in at)
print(C)
