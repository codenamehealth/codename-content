import numpy as np, subprocess, glob, sys
S='/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
q = np.frombuffer(open(sys.argv[1],'rb').read(), dtype=np.int16).astype(float)[int(8000*float(sys.argv[2])):int(8000*float(sys.argv[3]))]
q = (q - q.mean()) / (q.std() + 1e-9)
for m in sorted(glob.glob(S + 'music_adobe/*.wav')):
    a = np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',m,'-t','90','-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout, dtype=np.int16).astype(float)
    n = len(a) + len(q); N = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(a, N) * np.conj(np.fft.rfft(q, N)), N)[:len(a) - len(q)]
    # normalise by local energy
    e = np.sqrt(np.convolve(a * a, np.ones(len(q)), 'valid'))[:len(c)] + 1e-9
    r = c / e / np.sqrt(len(q)); k = int(np.argmax(r))
    print(f'{r[k]:.3f} {k/8000:.3f} {m.split("/")[-1]}')
