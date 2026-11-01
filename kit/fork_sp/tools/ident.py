# identify which music_adobe track (and offset) a reel's audio uses: python3 ident.py reel.mp4
import sys, subprocess, numpy as np, glob, os
SR = 4000
def load(p, t0=0, dur=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(t0)] + (['-t', str(dur)] if dur else []) + ['-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)
q = load(sys.argv[1], 0.0, 8.0); q = q - q.mean()
res = []
for m in sorted(glob.glob('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/music_adobe/*.wav')):
    a = load(m); a = a - a.mean()
    if len(a) <= len(q): a = np.tile(a, 3)
    a = np.concatenate([a, a[:len(q)]])
    n = len(a) + len(q); N = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(a, N) * np.conj(np.fft.rfft(q, N)), N)[:len(a)]
    # normalise by local energy
    cs = np.concatenate([[0], np.cumsum(a.astype(np.float64) ** 2)]); e = np.sqrt(np.maximum(cs[len(q):] - cs[:-len(q)], 0)) + 1e-6
    cc = c[:len(e)] / e / (np.linalg.norm(q) + 1e-9)
    i = int(np.argmax(cc)); res.append((cc[i], os.path.basename(m), i / SR))
for r in sorted(res, reverse=True)[:3]: print('%.3f %s offset %.2f' % r)
