# #99 Pause it at exactly 10.00 -- FIX (fork_fix9899, Bennett): the REEL ITSELF is 9.99s long.
# Clock shows 00.00 on frame 0 and counts up every frame (no SLOW / TIME WARP, no freeze, no TIME STOP)
# to 09.99 on the last frame, then the video loops straight back to 00.00. Never shows 10.00.
# 300 frames at 10000/333 fps (30.03) = exactly 9.990s. Display = round(k * 999 / 299) hundredths,
# so each frame advances 3-4 hundredths (1.0033x real time: the last frame must start one frame before the end).
# Scene, characters and hook unchanged from fork_sz94/v99 (watch on the well rim, Rayleigh 4x, melatonin gummy).
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['PAUSE IT AT', 'EXACTLY 10.00'], accent=1); print('hook bottom', HB)
OUT = SP + 'fork_fix9899/v99/'; G = SP + 'fork_a10/gen/'
NF = 300; RATE = '10000/333'; RF = 10000 / 333
D = [int(round(k * 999 / 299)) for k in range(NF)]
assert D[0] == 0 and D[-1] == 999 and max(D) == 999 and all(b > a for a, b in zip(D, D[1:]))
def disp(k): return '%02d.%02d' % divmod(D[k], 100)
BG0 = bg_frames('hub.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.72)
SH = 280
def shifted(b):
    o = Image.new('RGBA', (W, H)); o.alpha_composite(b, (0, -SH)); o.alpha_composite(b.crop((0, H - SH, W, H)).transpose(Image.FLIP_TOP_BOTTOM), (0, H - SH)); return o
BGS = [shifted(b) for b in BG0]
WATCH = up(crop(Image.open(G + 'watch/00.png').convert('RGBA')), 5)
RID = idle('ray', 4)
MEL = gummy('mel', 3)
WX, WBOT = 470, 1150
RX, RFEET = 775, 1480
PL0, PL1, PY0, PY1 = 100, 690, 1190, 1350
wa = np.array(WATCH); face = (wa[..., 0] > 230) & (wa[..., 1] > 230) & (wa[..., 2] > 230) & (wa[..., 3] > 200)
ys, xs = np.nonzero(face); FCX, FCY = xs.mean(), ys.mean(); FR = (xs.max() - xs.min()) / 2
# loop-seamless animation indices: whole cycles over the 300 frames (bg ~6 fps, idle ~8 fps)
def cyc(L, rate):
    n = max(1, round(NF / RF * rate / L)); return lambda k: int(k * n * L / NF) % L
BGI, RII = cyc(len(BGS), 6), cyc(len(RID), 8)
print('bg frames', len(BGS), 'idle frames', len(RID))
class W2(Writer):
    def __init__(self, path):
        self.p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', RATE, '-i', '-',
                                   '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', RATE, path], stdin=subprocess.PIPE)
w = W2(OUT + 'noaudio.mp4'); ev = []; last_sec = -1
ox, oy = int(WX - WATCH.width / 2), WBOT - WATCH.height
for f in range(NF):
    t = f / RF
    img = BGS[BGI(f)].copy()
    layer(img, lambda d2: d2.ellipse([WX - 200, WBOT - 26, WX + 200, WBOT + 14], fill=(0, 0, 0, 110)))
    img.alpha_composite(WATCH, (ox, oy))
    cx, cy = ox + FCX, oy + FCY; sec = D[f] / 100
    def hands(d2):
        a = math.radians(sec * 30 - 90)
        d2.line([cx, cy, cx + math.cos(a) * FR * 0.85, cy + math.sin(a) * FR * 0.85], fill=(40, 30, 60, 255), width=12)
        a2 = math.radians(sec * 3 - 90)
        d2.line([cx, cy, cx + math.cos(a2) * FR * 0.55, cy + math.sin(a2) * FR * 0.55], fill=(150, 40, 60, 255), width=14)
        d2.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 214, 60, 255), outline=(40, 30, 60, 255), width=4)
    layer(img, hands)
    img.alpha_composite(MEL, (800 - MEL.width // 2, WBOT + 2 - MEL.height))
    layer(img, lambda d2: d2.rounded_rectangle([PL0, PY0, PL1, PY1], 26, fill=(18, 14, 34, 235), outline=(255, 214, 60, 255), width=8))
    text_layer(img, [((PL0 + PL1) / 2, PY0 + 32, disp(f), 100, (255, 255, 255), 0, 255)])
    text_layer(img, [((PL0 + PL1) / 2, 1374, 'Comment your time', 34, (255, 230, 150), 6, 255)])
    fr = RID[RII(f)]
    img.alpha_composite(fr, (int(RX - fr.width / 2), int(RFEET - 78 * 4)))
    s_now = D[f] // 100
    if s_now > last_sec: ev.append((round(t, 3), 'tick_8bit')); last_sec = s_now
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (0, NF - 1): img.convert('RGB').save(OUT + f'render_{f:03d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', NF, 'frames', NF / RF, 's', len(ev), 'ticks')
print('first', disp(0), 'last', disp(NF - 1), 'distinct', len(set(D)))
