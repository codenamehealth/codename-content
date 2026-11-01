import numpy as np, subprocess, glob, os, sys, json
SR = 8000
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad'

def dec(path, dur=None):
    cmd = ['ffmpeg', '-v', 'error', '-i', path]
    if dur: cmd += ['-t', str(dur)]
    cmd += ['-ac', '1', '-ar', str(SR), '-f', 'f32le', '-']
    b = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(b, dtype=np.float32).astype(np.float64)

lib = {}
for p in sorted(glob.glob(S + '/music/*.wav') + glob.glob(S + '/music_adobe/*.wav') + glob.glob('/home/claude/tl/music/*.mp3')):
    x = dec(p, 400)
    # loop once so offsets that wrap (stream_loop) still match
    lib[p] = np.concatenate([x, x[:SR * 30]])

def ncc(track, clip):
    n = len(track) + len(clip)
    N = 1 << int(np.ceil(np.log2(n)))
    F = np.fft.rfft(track, N) * np.conj(np.fft.rfft(clip, N))
    xc = np.fft.irfft(F, N)[:len(track) - len(clip) + 1]
    c2 = np.concatenate([[0], np.cumsum(track ** 2)])
    e = c2[len(clip):] - c2[:-len(clip)]
    e = np.sqrt(np.maximum(e, 1e-9)) * np.linalg.norm(clip)
    r = xc / e
    i = int(np.argmax(np.abs(r)))
    return float(r[i]), i / SR

files = sys.argv[1:]
out = {}
for f in files:
    v = dec(f)
    # use windows of 4s from the clip; best track = highest median score across windows
    res = {}
    wins = [v[s:s + 4 * SR] for s in range(0, max(1, len(v) - 4 * SR), 3 * SR)]
    wins = [w for w in wins if len(w) == 4 * SR and np.linalg.norm(w) > 1e-3]
    for p, t in lib.items():
        sc = [ncc(t, w) for w in wins]
        vals = sorted([abs(s[0]) for s in sc])
        res[os.path.basename(p)] = (float(np.median(vals)) if vals else 0, max(vals) if vals else 0, sc[0][1] if sc else None)
    best = sorted(res.items(), key=lambda kv: -kv[1][0])[:3]
    out[os.path.basename(f)] = best
    print(os.path.basename(f), ' | '.join(f"{k} med={a:.2f} max={b:.2f} off={o}" for k, (a, b, o) in best), flush=True)
json.dump(out, open(S + '/maudit/fp_out.json', 'a'))
