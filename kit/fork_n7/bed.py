# race_v4 music bed: eight_bit for the race, ducked out under the rewind, a sneaky pizzicato line (Karplus-Strong plucks, synthesized here)
# under the flashback with a little plink on the replay hop, then eight_bit resumes for the present.
# usage: bed.py events.json out.wav
import json, subprocess, sys, numpy as np
SR = 44100
ev = json.load(open(sys.argv[1])); B = ev['beats']; END = ev['end']
M = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/music_adobe/eight_bit.wav',
                                  '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout, np.float32).reshape(-1, 2)
N = int(END * SR) + SR
bed = np.zeros((N, 2), np.float32)
t = np.arange(N) / SR
t_rw, t_fb, t_now = B['rewind'], B['fb_bribe'], B['present']
# music envelope: full until rewind, 0.12s fade out, silent through the flashback, 0.08s fade in at present (music resumes where it paused)
env = np.ones(N, np.float32)
env[(t >= t_rw)] = 0
fo = (t >= t_rw) & (t < t_rw + 0.12); env[fo] = 1 - (t[fo] - t_rw) / 0.12
mus_idx = np.arange(N).copy()
paused = int((t_now - t_rw) * SR)
mus_idx[t >= t_now] -= paused
env[t >= t_now] = 1.0 * np.clip((t[t >= t_now] - t_now) / 0.08, 0, 1)
MO = 12.0   # music offset: skips eight_bit's sparse intro (it has near-silent gaps that landed on the slime hop)
bed += M[(mus_idx + int(MO * SR)) % len(M)] * env[:, None]
def pluck(freq, dur, amp, seed=0):
    n = int(dur * SR); L = max(2, int(SR / freq)); rs = np.random.default_rng(seed)
    buf = list(rs.uniform(-1, 1, L)); out = np.zeros(n, np.float32)
    for i in range(n):
        v = buf[i % L]; out[i] = v; buf[i % L] = 0.5 * (v + buf[(i + 1) % L]) * 0.994
    out *= np.exp(-np.arange(n) / SR / 0.16)    # pizzicato: short
    return out * amp
def m2f(m): return 440 * 2 ** ((m - 69) / 12)
E8 = 0.19
pat = [40, None, 43, None, 45, None, 46, 47, 40, None, 43, None, 45, None, 46, 45, 40, None, 43, None]
start = t_fb - 0.12
for k, m in enumerate(pat):
    ts = start + k * E8
    if m is None or ts >= t_now - 0.05: continue
    i0 = int(ts * SR)
    for mm, a in ((m, 0.9), (m + 12, 0.36)):
        p = pluck(m2f(mm), 0.35, a, seed=k * 3 + mm)
        bed[i0:i0 + len(p)] += p[:, None] * np.array([0.9, 1.0], np.float32) if mm == m else p[:, None] * np.array([1.0, 0.85], np.float32)
# the 'aha' plink on the replay hop: a quick high minor-third pair
for dt, mm in ((0.0, 76), (0.09, 79)):
    i0 = int((B['replay_hop'] + dt) * SR); p = pluck(m2f(mm), 0.4, 0.55, seed=mm)
    bed[i0:i0 + len(p)] += p[:, None]
bed = bed[:int(END * SR)]
import wave
pk = np.abs(bed).max(); bed = bed / max(1.0, pk / 0.95)
w = wave.open(sys.argv[2], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((bed * 32767).astype('<i2').tobytes()); w.close()
print('bed', sys.argv[2], round(len(bed) / SR, 2), 'peak', round(float(pk), 2))
