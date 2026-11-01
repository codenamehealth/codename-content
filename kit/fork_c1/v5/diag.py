import sys, math
sys.argv=['x']
import sim_orig as so
fr, ev, cnt, ld, T = so.run(343)
print('T', round(T,1), cnt, ld)
esc = {}; maxd=0
for k,(balls,counts,ang) in enumerate(fr):
    tot=sum(counts.values())
    for n,x,y in balls:
        d=math.hypot(x-so.GX,y-so.GY); maxd=max(maxd,d)
        if d > so.GR - so.BR + 8:
            esc.setdefault(k,[]).append((n,round(x),round(y),round(d)))
ks=sorted(esc)
print('frames with a ball outside the glass:', len(ks), 'first', ks[:5], 'maxdist', round(maxd), 'GR', so.GR)
for k in ks[:8]: print(k, round(k/30,2), 'balls', len(fr[k][0]), esc[k][:4])
# packing
for k in (0, len(fr)//2, len(fr)-1):
    n=len(fr[k][0]); print('frame',k,'balls',n,'packing %.0f%%' % (100*n*so.BR**2/so.GR**2))
