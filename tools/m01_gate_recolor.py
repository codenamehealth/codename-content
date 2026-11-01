# Recolor the four coloured gates (cols 6, 9, 12, 15; rows 4-6) of the published m01 to neutral slate,
# plus their break dust. Timing, frames outside the gates and audio stay untouched.
import subprocess, sys, numpy as np
from scipy.ndimage import label, find_objects
SRC, OUT = sys.argv[1], sys.argv[2]
W, H, FPS = 1080, 1920, 30
U, X0, Y0 = 51, 55, 396
GATES = {6: (190, 127, 64), 9: (91, 122, 184), 12: (129, 86, 149), 15: (107, 157, 84)}
SLATE = np.array([128, 128, 138], float)
GUIDE = {6: (255, 145, 30), 9: (70, 135, 255), 12: (180, 95, 235), 15: (100, 200, 70)}   # box/trail colour sharing each gate's hue
KEEP_R = 70
T_LIMIT = 17.5                                    # all gate cells are gone by ~16.7s

def hsv(a):
    a = a / 255.0; mx = a.max(-1); mn = a.min(-1); d = mx - mn + 1e-6
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    s = np.where(mx > 0, (mx - mn) / (mx + 1e-6), 0)
    return h, s, mx

GH = {c: hsv(np.array(col, float)[None, None])[0][0, 0] for c, col in GATES.items()}
def hue_near(h, h0, tol=0.06): return np.minimum(np.abs(h - h0), 1 - np.abs(h - h0)) < tol

def lum(a): return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114

intact = {(c, r): True for c in GATES for r in (4, 5, 6)}
PAL = {}                                          # exact gate palettes, read from frame 0

broke_at = {}
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-i', SRC, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p',
                        '-c:a', 'copy', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
fi = 0; changed = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = fi / FPS
    if t < T_LIMIT:
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(float)
        if fi == 0:
            for c in GATES:
                px = fr[Y0 + 4 * U:Y0 + 7 * U, X0 + c * U + 3:X0 + c * U + U - 3].reshape(-1, 3)
                hh, ss, vv = hsv(px[None])
                keep = px[(ss[0] > 0.18) & (vv[0] > 0.12)]
                u, n = np.unique(keep.astype(int), axis=0, return_counts=True)
                PAL[c] = u[n >= 3].astype(float)
        for c, col in GATES.items():
            base = np.array(col, float); bl = lum(base)
            # gate cells while intact
            for r in (4, 5, 6):
                if not intact[(c, r)]: continue
                x0, y0 = X0 + c * U, Y0 + r * U
                cell = fr[y0:y0 + U, x0:x0 + U]
                h, s, v = hsv(cell)
                m = (s > 0.18) & (v > 0.12)
                cf = cell.reshape(-1, 3); dmn = np.full(len(cf), 1e9)
                for i in range(0, len(PAL[c]), 64):
                    dmn = np.minimum(dmn, np.abs(cf[:, None, :] - PAL[c][None, i:i + 64, :]).sum(-1).min(1))
                frac = (dmn <= 10).mean()
                if frac < 0.25:                      # brick gone (floor or flood now)
                    intact[(c, r)] = False; broke_at[(c, r)] = t; continue
                k = (lum(cell) / bl)[..., None]
                cell[m] = np.clip(SLATE * k, 0, 255)[m]
                changed += int(m.sum())
            # break dust: solid gate-coloured squares near the gate for 1.2s after a cell breaks
            recent = [rr for (cc, rr), tb in broke_at.items() if cc == c and 0 <= t - tb < 1.2]
            if recent:
                ya, yb = Y0 + 2 * U, Y0 + 8 * U; xa, xb = X0 + (c - 2) * U, X0 + (c + 3) * U
                reg = fr[ya:yb, xa:xb]
                flat = reg.reshape(-1, 3)
                dmin = np.full(len(flat), 1e9)
                for i in range(0, len(PAL[c]), 64):
                    dmin = np.minimum(dmin, np.abs(flat[:, None, :] - PAL[c][None, i:i + 64, :]).sum(-1).min(1))
                m = (dmin <= 10).reshape(reg.shape[:2])     # exact gate/dust palette only, never a guide's border or trail
                if c != 6:                                   # faded dust edges (floor hue differs except for the orange gate)
                    hh, ss, vv = hsv(reg)
                    m |= hue_near(hh, GH[c], 0.05) & (ss > 0.22) & (vv > 0.25)
                gb = np.abs(reg - np.array(GUIDE[c], float)).sum(-1) < 70      # that guide's box border and trail core
                if gb.any():
                    lab, n = label(gb)
                    for sl in find_objects(lab):
                        m[max(0, sl[0].start - KEEP_R):sl[0].stop + KEEP_R, max(0, sl[1].start - KEEP_R):sl[1].stop + KEEP_R] = False
                k = (lum(reg) / bl)[..., None]
                reg[m] = np.clip(SLATE * k, 0, 255)[m]
                changed += int(m.sum())
        buf = fr.astype(np.uint8).tobytes()
    enc.stdin.write(buf); fi += 1
enc.stdin.close(); enc.wait(); dec.wait()
print('frames', fi, 'pixels changed', changed)
print('cell breaks', {f'{c},{r}': round(tb, 2) for (c, r), tb in sorted(broke_at.items(), key=lambda x: x[1])})
print('still intact at 20s', [k for k, v in intact.items() if v])
