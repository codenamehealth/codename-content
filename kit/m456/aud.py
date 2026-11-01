import sys,subprocess,numpy as np
V=sys.argv[1]
b=subprocess.run(['ffmpeg','-v','error','-i',V,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
x=np.frombuffer(b,np.int16).astype(float)/32768
hop=800; n=len(x)//hop; r=np.array([np.sqrt((x[i*hop:(i+1)*hop]**2).mean()) for i in range(n)])
db=20*np.log10(r+1e-9)
print('dur',len(x)/16000,'mean dB',db.mean().round(1),'pct10/50/90',np.percentile(db,[10,50,90]).round(1))
# coarse loudness per 5s
for k in range(0,n,100): print(f'{k*0.05:5.1f}s', round(float(db[k:k+100].mean()),1), round(float(db[k:k+100].max()),1))
# high-frequency onset count (spectral flux) per second
F=np.abs(np.fft.rfft(x[:n*hop].reshape(n,hop)*np.hanning(hop),axis=1)); fl=np.maximum(0,np.diff(F,axis=0)).sum(1)
th=np.percentile(fl,97); on=np.nonzero(fl>th)[0]
print('strong onsets/s', round(len(on)/(n*0.05),2))
