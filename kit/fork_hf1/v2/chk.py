import sys; sys.argv=['r2.py','7']
src=open('r2.py').read().split("# outline from the unrotated")[0]
exec(src)
r=[]
for f in range(NF):
    x,y,a=motion(P,f/FPS); x+=P['ox']; y+=P['oy']; a+=P['oa']; r.append((round(max(abs(x),abs(y),abs(a)*9),1),f))
print(sorted(r)[:8])
