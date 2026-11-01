import sys,subprocess,numpy as np
# flood.py video fps colour tol out : flood pixel area (full-res px) + per-row/col extent per sample, half-res decode
V,fps,c,tol,out=sys.argv[1],sys.argv[2],np.array(eval(sys.argv[3])),int(sys.argv[4]),sys.argv[5]
p=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-vf',f'fps={fps},scale=540:960','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
N=540*960*3;i=0;f=open(out,'w')
while True:
    b=p.stdout.read(N)
    if len(b)<N: break
    a=np.frombuffer(b,np.uint8).reshape(960,540,3).astype(np.int16)
    m=np.abs(a-c).max(2)<tol
    ys,xs=np.nonzero(m)
    f.write(f'{i/float(fps):.2f} {int(m.sum())*4} {2*xs.min() if len(xs) else -1} {2*xs.max() if len(xs) else -1} {2*ys.min() if len(ys) else -1} {2*ys.max() if len(ys) else -1}\n'); i+=1
f.close()
