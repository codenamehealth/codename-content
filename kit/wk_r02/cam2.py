import subprocess,numpy as np
W,H=540,960
p=subprocess.Popen(['ffmpeg','-v','error','-i','../igref/Dd4TeRFSsqG.mp4','-vf','scale=540:960','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
prev=None;out=[];i=0
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3:break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(float)
    # yellowish/structure mask over band rows: use grayscale gradient profile averaged over band
    g=f[200:760].mean(2)
    prof=np.abs(np.diff(g,axis=1)).mean(0)
    if prev is not None:
        best=None
        for s in range(-3,40):
            a=prev[max(0,s):len(prev)+min(0,s)];c=prof[max(0,-s):len(prof)-max(0,s)] if s>=0 else prof[-s:]
            # shift: content moves left by s => prof[x]=prev[x+s]
            if s>=0: a=prev[s:];c=prof[:len(prof)-s]
            else: a=prev[:s];c=prof[-s:]
            e=np.mean((a-c)**2)
            if best is None or e<best[0]:best=(e,s)
        out.append(best[1])
    else: out.append(0)
    prev=prof;i+=1
out=np.array(out)*2  # full-res px/frame
np.save('cam2.npy',out)
for k in range(0,len(out),15):
    print('%.1fs'%(k/30),out[k:k+15].tolist())
print('total',out.sum())
