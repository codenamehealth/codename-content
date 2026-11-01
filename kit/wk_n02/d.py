import sys, collections
sys.argv=['n02.py','x']
src=open('n02.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C=collections.Counter()
for seed in range(1,150):
    st_, tl = run_sim(seed); li=int(T_LAND*FPS)
    c, r = st_['cyrus']['fin'], st_['ray']['fin']
    C['cleojoy_close'] += abs(tl[li]['cleo'][0]-tl[li]['joy'][0])<=220
    fo=max(tl[li]['cleo'][0], tl[li]['joy'][0]); C['ahead'] += min(tl[li]['cyrus'][0], tl[li]['ray'][0]) >= fo+260
    if c and r: C['c<r'] += c<r; C['close'] += (c<r<c+0.22); C['c%d'%int(c)]+=1
print(C)
