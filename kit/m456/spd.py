import sys,subprocess,numpy as np
from scipy import ndimage as ndi
# spd.py video t0 t1 dt colour tol y0 y1 x0 x1 : centroid of largest blob of colour per time
V=sys.argv[1]; t0,t1,dt=map(float,sys.argv[2:5]); c=np.array(eval(sys.argv[5])); tol=int(sys.argv[6]); y0,y1,x0,x1=map(int,sys.argv[7:11])
t=t0
while t<=t1+1e-9:
    b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.4f}','-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    a=np.frombuffer(b,np.uint8).reshape(1920,1080,3).astype(int)[y0:y1,x0:x1]
    m=np.abs(a-c).max(2)<tol; lab,n=ndi.label(m)
    if n:
        sz=ndi.sum(m,lab,range(1,n+1)); j=int(np.argmax(sz)); s=ndi.find_objects(lab)[j]
        print(f'{t:.3f}', s[1].start+x0, s[0].start+y0, s[1].stop+x0, s[0].stop+y0, int(sz[j]))
    t+=dt
