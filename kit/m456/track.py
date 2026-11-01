import sys,subprocess,json,numpy as np
from scipy import ndimage as ndi
# usage: track.py video fps out.json [y0 y1]  -> per frame: square boxes per colour, orange mask stats
V,fps,out=sys.argv[1],float(sys.argv[2]),sys.argv[3]
COL={'green':(22,252,6),'yellow':(254,246,4),'red':(254,0,1),'blue':(6,114,255)}
EXTRA=json.loads(sys.argv[4]) if len(sys.argv)>4 else {}
COL.update({k:tuple(v) for k,v in EXTRA.items()})
p=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-vf',f'fps={fps}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
W,H=1080,1920;N=W*H*3;res=[];i=0
while True:
    b=p.stdout.read(N)
    if len(b)<N: break
    a=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.int16)
    fr={'t':round(i/fps,3)}
    for k,c in COL.items():
        m=(np.abs(a-np.array(c)).max(2)<28)
        lab,n=ndi.label(m)
        if n==0: fr[k]=[];continue
        sl=ndi.find_objects(lab); sz=ndi.sum(m,lab,range(1,n+1))
        objs=[]
        for j in np.argsort(-sz)[:6]:
            if sz[j]<150: break
            s=sl[j]; objs.append([s[1].start,s[0].start,s[1].stop,s[0].stop,int(sz[j])])
        fr[k]=objs
    o=(np.abs(a-np.array((248,104,0))).max(2)<30)
    fr['orange']=int(o.sum())
    res.append(fr); i+=1
json.dump(res,open(out,'w'))
print(len(res))
