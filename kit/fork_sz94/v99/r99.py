# #99 Pause it at exactly 10.00 -- Bennett: the timer stops at 9.99 and NEVER reaches 10.00 (that's the joke).
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['PAUSE IT AT', 'EXACTLY 10.00'], accent=1); print('hook bottom', HB)
OUT = SP + 'fork_sz94/v99/'; G = SP + 'fork_a10/gen/'
T_ST = 1.0
SEG = [(1.0, 3.2, 1.25, ''), (3.2, 5.0, 0.55, 'SLOW...'), (5.0, 6.6, 1.5, ''), (6.6, 7.6, 0.8, 'SLOW...'), (7.6, 8.5, 2.4, 'TIME WARP!'), (8.5, 99, 0.7, 'SLOW...')]
def vel(t):
    for a, b, v, lab in SEG:
        if a <= t < b: return v, lab
    return 0, ''
# displayed hundredths per frame: continuous until 9.90, then a crawl 9.91 ... 9.99 and a hard stop at 9.99
STEPS = [0.06, 0.06, 0.07, 0.08, 0.10, 0.13, 0.18, 0.28, 0.40]   # how long 9.90 ... 9.98 stay up
NF0 = int(20 * FPS); D = [0] * NF0; acc = 0.0; f = 1
while f < NF0:
    acc += vel(f / FPS)[0] / FPS
    D[f] = min(990, int(math.floor(acc * 100 + 1e-9)))
    if D[f] == 990: break
    f += 1
F990 = f; tt = F990 / FPS; v = 990
for dur in STEPS:
    tt += dur; v += 1
    while f < int(round(tt * FPS)): D[f] = v - 1; f += 1
F_STOP = f
for k in range(F_STOP, NF0): D[k] = 999
assert max(D) == 999 and 1000 not in D
END = F_STOP / FPS + 3.2
print('9.90 at', F990 / FPS, 'stop (9.99) at', F_STOP / FPS, 'end', END)
def disp(f): return '%02d.%02d' % divmod(D[min(f, NF0 - 1)], 100)
BG0 = bg_frames('hub.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.72)
SH = 280   # background raised so the round stone platform sits under the watch
def shifted(b):
    o = Image.new('RGBA', (W, H)); o.alpha_composite(b, (0, -SH)); o.alpha_composite(b.crop((0, H - SH, W, H)).transpose(Image.FLIP_TOP_BOTTOM), (0, H - SH)); return o
BGS = [shifted(b) for b in BG0]
WATCH = up(crop(Image.open(G + 'watch/00.png').convert('RGBA')), 5)
RID = idle('ray', 4); RCAST = seq(SP + 'fork3/ray_cast', 4, 1, None)
MEL = gummy('mel', 3)
WX, WBOT = 470, 1150     # watch stands on the well's front rim
RX, RFEET = 775, 1480
PL0, PL1, PY0, PY1 = 100, 690, 1190, 1350
wa = np.array(WATCH); face = (wa[..., 0] > 230) & (wa[..., 1] > 230) & (wa[..., 2] > 230) & (wa[..., 3] > 200)
ys, xs = np.nonzero(face); FCX, FCY = xs.mean(), ys.mean(); FR = (xs.max() - xs.min()) / 2
w = Writer(OUT + 'noaudio.mp4'); ev = []; NF = int(END * FPS); last_sec = 0; last_d = 0
for f in range(NF):
    t = f / FPS; fd = min(f, F_STOP)
    img = BGS[int(t * 6) % len(BGS)].copy()
    lab = '' if f >= F_STOP else ('SLOW...' if f >= F990 else vel(t)[1])
    if t < T_ST: lab = ''
    ox, oy = int(WX - WATCH.width / 2), WBOT - WATCH.height
    if lab:
        col = (190, 110, 255) if lab == 'TIME WARP!' else (120, 170, 255)
        cy0 = oy + FCY
        def rings(d2):
            for k in range(3):
                r = 250 + ((t * (240 if lab == 'TIME WARP!' else 90) + k * 90) % 230)
                a = int(150 * (1 - (r - 250) / 230))
                d2.ellipse([WX - r, cy0 - r, WX + r, cy0 + r], outline=col + (a,), width=10)
        layer(img, rings)
    layer(img, lambda d2: d2.ellipse([WX - 200, WBOT - 26, WX + 200, WBOT + 14], fill=(0, 0, 0, 110)))
    img.alpha_composite(WATCH, (ox, oy))
    cx, cy = ox + FCX, oy + FCY; sec = D[fd] / 100
    def hands(d2):
        a = math.radians(sec * 30 - 90)
        d2.line([cx, cy, cx + math.cos(a) * FR * 0.85, cy + math.sin(a) * FR * 0.85], fill=(40, 30, 60, 255), width=12)
        a2 = math.radians(sec * 3 - 90)
        d2.line([cx, cy, cx + math.cos(a2) * FR * 0.55, cy + math.sin(a2) * FR * 0.55], fill=(150, 40, 60, 255), width=14)
        d2.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 214, 60, 255), outline=(40, 30, 60, 255), width=4)
    layer(img, hands)
    # melatonin gummy resting on the platform next to the watch
    img.alpha_composite(MEL, (800 - MEL.width // 2, WBOT + 2 - MEL.height))
    # readout plaque on the platform front
    shake = int(5 * math.sin(f * 2.1)) if f >= F_STOP and (f - F_STOP) < 12 else 0
    layer(img, lambda d2: d2.rounded_rectangle([PL0 + shake, PY0, PL1 + shake, PY1], 26, fill=(18, 14, 34, 235), outline=(255, 214, 60, 255), width=8))
    txt = disp(f); colr = (255, 255, 255) if f < F_STOP else (255, 214, 60)
    text_layer(img, [((PL0 + PL1) / 2 + shake, PY0 + 32, txt, 100, colr, 0, 255)])
    # rayleigh
    casting = bool(lab) or (F_STOP <= f < F_STOP + 18)
    fr = RCAST[int(t * 14) % len(RCAST)] if casting else RID[int(t * 8) % len(RID)]
    img.alpha_composite(fr, (int(RX - fr.width / 2), int(RFEET - 78 * 4)))
    if lab: text_layer(img, [((PL0 + PL1) / 2, 1374, lab, 44, (210, 160, 255) if lab == 'TIME WARP!' else (150, 200, 255), 7, 255)])
    # sounds: tick every whole second, then a tick on every hundredth of the crawl
    s_now = D[fd] // 100
    if f < F_STOP and s_now > last_sec: ev.append((round(t, 3), 'tick_8bit')); last_sec = s_now
    if F990 < f <= F_STOP and D[f] != last_d: ev.append((round(t, 3), 'tick_8bit'))
    last_d = D[fd]
    for a, b, vv, lb in SEG:
        if lb and f == int(round(a * FPS)) and f < F990: ev.append((round(t, 3), 'whoosh_8bit'))
    if f == F990: ev.append((round(t, 3), 'whoosh_8bit'))
    if f == F_STOP: ev.append((round(t, 3), 'boing'))
    if f >= F_STOP:
        u = (f - F_STOP) / FPS; a = int(255 * min(1, u / 0.2))
        text_layer(img, [((PL0 + PL1) / 2, 1374, 'TIME STOP!', 44, (255, 214, 60), 7, a)])
        if u > 0.7:
            a = int(255 * min(1, (u - 0.7) / 0.3))
            layer(img, lambda d2: d2.rounded_rectangle([90, 590, 1000, 770], 22, fill=(14, 10, 24, int(215 * a / 255)), outline=(255, 214, 60, a), width=5))
            text_layer(img, [(545, 618, 'DID YOU GET 10.00?', 46, (255, 255, 255), 7, a), (545, 700, 'Comment your time', 34, (255, 230, 150), 6, a)])
            if abs(u - 0.7) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit'))
    if t < T_ST: text_layer(img, [((PL0 + PL1) / 2, 1374, 'GET READY...', 44, (255, 255, 255), 7, 255)])
    img.alpha_composite(HOOK)
    w.write(img)
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev))
print('displays seen near end:', sorted(set(disp(k) for k in range(F990 - 3, NF))))
