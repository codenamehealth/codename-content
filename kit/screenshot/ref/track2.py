import numpy as np, subprocess, json
from scipy import ndimage
W,H=720,1280
p=subprocess.run(['ffmpeg','-loglevel','error','-i','ref.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
fr=np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W,3).astype(np.int16)
# static background estimate: per-pixel median of frames -> diff mask
med=np.median(fr[::3],axis=0)
out=[];prev=None;pang=0.0
for i,f in enumerate(fr):
    d=np.abs(f-med).sum(-1)
    R,G,B=f[...,0],f[...,1],f[...,2]
    green=(G>R+10)&(R>B+30)&(G>120)&(G<225)&(R>95)
    m=green&(d>25)
    m=ndimage.binary_opening(m,iterations=2); m=ndimage.binary_closing(m,iterations=4)
    lab,n=ndimage.label(m)
    if n==0: out.append(None);continue
    sizes=ndimage.sum(m,lab,range(1,n+1)); k=int(np.argmax(sizes))+1
    ys,xs=np.nonzero(lab==k)
    cx,cy=xs.mean(),ys.mean()
    c=np.cov(np.vstack([xs-cx,ys-cy])); w,v=np.linalg.eigh(c); ax=v[:,1]
    a=np.degrees(np.arctan2(ax[0],-ax[1]))  # axis angle from vertical, mod 180
    # unwrap mod 180 relative to previous
    while a-pang>90: a-=180
    while a-pang<-90: a+=180
    elong=w[1]/max(w[0],1)
    out.append([float(cx),float(cy),float(a),int(len(xs)),float(elong)]); pang=a
json.dump(out,open('track2.json','w'))
for i in range(0,len(out),5): o=out[i]; print(round(i/30,2), o and [round(v,1) for v in o])
