import subprocess, numpy as np, sys
v = sys.argv[1]
GX0, GX1, GY0, GY1, C = 131, 665, 566, 1262, 398
w, h = GX1-GX0, GY1-GY0
raw = subprocess.run(['ffmpeg','-v','error','-i',v,'-vf',f'crop={w}:{h}:{GX0}:{GY0}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
n = len(raw)//(w*h); fr = np.frombuffer(raw, np.uint8).reshape(n, h, w)
c = C-GX0; hw = min(c, w-c) - 6
errs = np.array([np.abs(fr[k,:,c-hw:c-3].astype(int) - fr[k,:,c+3:c+hw][:, ::-1].astype(int)).mean() for k in range(n)])
SEG = 81
for i in range(5):
    seg = errs[i*SEG:(i+1)*SEG]; o = np.argsort(seg)
    print('shape', i+1, 'best frame', i*SEG+o[0], round(seg[o[0]],2), 'next', i*SEG+o[1], round(seg[o[1]],2), 'ratio', round(seg[o[1]]/max(seg[o[0]],1e-3),1))
