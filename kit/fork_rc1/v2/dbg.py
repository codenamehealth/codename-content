import sys; sys.argv=['r2.py','search','0','0']
src=open('r2.py').read().split("F0 = 196")[0]
exec(src)
import random, math
F0=196; rnd=random.Random(0); c={'x':0,'ymax':0,'ymin':0,'nb':0,'ok':0}
for _ in range(4000):
    p = dict(ax=rnd.uniform(120, 185), wx=TAU * rnd.choice([4, 5]), px=rnd.uniform(0, 6.3), bx=rnd.uniform(20, 45), wx2=TAU * rnd.choice([7, 8, 9]), px2=rnd.uniform(0, 6.3),
             ay=rnd.uniform(50, 72), wy=TAU * rnd.choice([3, 4]), py=rnd.uniform(0, 6.3), aa=rnd.uniform(18, 32), wa=TAU * rnd.choice([3, 4, 5]), pa=rnd.uniform(0, 6.3))
    x0,y0,a0=motion(p,F0/FPS); p['ox'],p['oy'],p['oa']=-x0,-y0,-a0
    xs=[motion(p,f/FPS)[0]+p['ox'] for f in range(0,NF,3)]; ys=[motion(p,f/FPS)[1]+p['oy'] for f in range(0,NF,3)]
    if max(map(abs,xs))>230: c['x']+=1; continue
    if max(ys)>20: c['ymax']+=1; continue
    if min(ys)<-140: c['ymin']+=1; continue
    nb=[math.hypot(motion(p,(F0+d)/FPS)[0]+p['ox'],motion(p,(F0+d)/FPS)[1]+p['oy']) for d in (-2,-1,1,2)]
    if min(nb)<26: c['nb']+=1; continue
    c['ok']+=1
print(c)
