"""Compare the new #36 against the previous batch_v3 file frame by frame for frames 0..N-1 (everything before the new finale).
Prints max/mean abs diff for the full frame and for the counter crop, and the diff around the three 99 frames."""
import subprocess, sys, numpy as np
W, H = 1080, 1920
def frames(path, n):
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', path, '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    for _ in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.int16)
old, new, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
CROP = (slice(560, 960), slice(140, 940))     # counter digits area (UY=-64 HUD: 491..986)
worst = (0, -1); worstc = (0, -1); rows = []
for i, (a, b) in enumerate(zip(frames(old, n), frames(new, n))):
    d = np.abs(a - b).mean(); dc = np.abs(a[CROP] - b[CROP]).mean()
    if d > worst[0]: worst = (d, i)
    if dc > worstc[0]: worstc = (dc, i)
    if i in (81, 82, 83, 169, 170, 171, 278, 279, 280): rows.append((i, round(d, 3), round(dc, 3)))
print('frames compared', i + 1, 'worst full', round(worst[0], 3), 'at', worst[1], 'worst counter', round(worstc[0], 3), 'at', worstc[1])
print('around the 99 frames (frame, full, counter):', rows)
