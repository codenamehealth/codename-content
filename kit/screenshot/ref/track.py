import numpy as np, subprocess, json
from scipy import ndimage
W,H=720,1280
p=subprocess.run(['ffmpeg','-loglevel','error','-i','ref.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
fr=np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W,3).astype(np.int16)
print(len(fr))
out=[];prev=(361,305)
for i,f in enumerate(fr):
    R,G,B=f[...,0],f[...,1],f[...,2]
    green=(G>R+10)&(R>B+30)&(G>120)&(G<225)&(R>95)
    pink=(R>200)&(G>130)&(G<200)&(B>120)&(B<200)&(R-G>40)
    red=(R>40)&(R<140)&(G<40)&(B<50)
    m=green|pink|red
    m=ndimage.binary_opening(m,iterations=2)
    m=ndimage.binary_closing(m,iterations=6)
    lab,n=ndimage.label(m)
    best=None;bd=1e9
    if n:
        sizes=ndimage.sum(m,lab,range(1,n+1))
        cms=ndimage.center_of_mass(m,lab,range(1,n+1))
        for k in range(n):
            if sizes[k]<15000: continue
            cy,cx=cms[k]; d=(cx-prev[0])**2+(cy-prev[1])**2 - sizes[k]*0.5
            if d<bd: bd=d;best=k+1
    if best is None:
        out.append(None);continue
    ys,xs=np.nonzero(lab==best)
    cx,cy=xs.mean(),ys.mean()
    c=np.cov(np.vstack([xs-cx,ys-cy]))
    w,v=np.linalg.eigh(c); ax=v[:,1]   # major axis
    ang=np.degrees(np.arctan2(ax[0],ax[1]))  # angle from vertical
    if ang>90: ang-=180
    if ang<-90: ang+=180
    # which end is pink (top)?
    pk=pink&(lab==best); 
    if pk.sum()>200:
        py,px=np.nonzero(pk); 
        # vector from center to pink
        vx,vy=px.mean()-cx,py.mean()-cy
        # true up-axis angle: angle of vector (center->top) measured from up (0,-1), clockwise positive
        ang=np.degrees(np.arctan2(vx,-vy))
    out.append([float(cx),float(cy),float(ang),int(len(xs))])
    prev=(cx,cy)
json.dump(out,open('track.json','w'))
for i in range(0,len(out),6): print(round(i/30,2),out[i] and [round(v,1) for v in out[i][:3]]+[out[i][3]])
