import sys,subprocess,numpy as np
from scipy import ndimage as ndi
V,t=sys.argv[1],sys.argv[2]; cols=eval(sys.argv[3])
b=subprocess.run(['ffmpeg','-v','error','-ss',t,'-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
a=np.frombuffer(b,np.uint8).reshape(1920,1080,3).astype(int)
for k,c in cols.items():
    m=np.abs(a-np.array(c)).max(2)<(int(sys.argv[4]) if len(sys.argv)>4 else 28)
    lab,n=ndi.label(m); sl=ndi.find_objects(lab); sz=ndi.sum(m,lab,range(1,n+1))
    out=[(s[1].start,s[0].start,s[1].stop-s[1].start,s[0].stop-s[0].start,int(z)) for s,z in zip(sl,sz) if z>40]
    print(k,sorted(out,key=lambda o:-o[4])[:6])
