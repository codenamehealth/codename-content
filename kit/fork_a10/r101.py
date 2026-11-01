import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
OUT = SP + 'fork_a10/v101/'; G = SP + 'fork_a10/gen/'
# ---- displayed time profile (real t -> D), exactly one frame shows 10.00
T_ST = 1.0
SEG = [(1.0, 3.2, 1.25, ''), (3.2, 5.0, 0.55, 'SLOW...'), (5.0, 6.6, 1.5, ''), (6.6, 7.6, 0.8, 'SLOW...'), (7.6, 9.4, 2.4, 'TIME WARP!'), (9.4, 99, 1.3, '')]
def vel(t):
    for a, b, v, lab in SEG:
        if a <= t < b: return v, lab
    return 0, ''
NF0 = int(13 * FPS); D = [0.0] * NF0
for f in range(1, NF0):
    t = f / FPS; v, _ = vel(t); D[f] = D[f - 1] + v / FPS
# shift so the crossing frame lands inside [10.00, 10.01)
fx = next(f for f in range(NF0) if D[f] >= 10.0)
target = 10.004; scale = target / D[fx]; D = [d * scale for d in D]
shows = [f for f in range(NF0) if '%05.2f' % (math.floor(D[f] * 100) / 100) == '10.00']
assert len(shows) == 1, shows
F_STOP = next(f for f in range(NF0) if D[f] >= 12.38); END = F_STOP / FPS + 3.2
print('10.00 frame', shows, 'stop', F_STOP / FPS, 'neighbours', ['%.3f' % D[shows[0] + k] for k in (-2, -1, 0, 1, 2)])
def disp(f):
    f = min(f, F_STOP); return '%05.2f' % (math.floor(D[f] * 100) / 100)
BGS = bg_frames('hub.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.72)
WATCH = up(crop(Image.open(G + 'watch/00.png').convert('RGBA')), 5)
RID = idle('ray', 4); RCAST = seq(SP + 'fork3/ray_cast', 4, 1, None)
MEL = gummy('mel', 3)
WX, WY = W / 2, 900
# watch face centre: find white face centroid
wa = np.array(WATCH); face = (wa[..., 0] > 230) & (wa[..., 1] > 230) & (wa[..., 2] > 230) & (wa[..., 3] > 200)
ys, xs = np.nonzero(face); FCX, FCY = xs.mean(), ys.mean(); FR = (xs.max() - xs.min()) / 2
w = Writer(OUT + 'noaudio.mp4'); ev = []; NF = int(END * FPS); last_sec = 0
for f in range(NF):
    t = f / FPS; fd = min(f, F_STOP)
    img = BGS[int(t * 6) % len(BGS)].copy()
    v, lab = vel(t) if f < F_STOP else (0, '')
    layer(img, lambda d: d.rectangle([0, 0, W, 330], fill=(14, 10, 24, 170)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 80, 'PAUSE IT AT', F(60)); ctext(d, W / 2, 175, 'EXACTLY 10.00', F(66), (255, 214, 60), 8)
    # warp rings
    if lab and t >= T_ST:
        col = (190, 110, 255) if lab == 'TIME WARP!' else (120, 170, 255)
        def rings(d2):
            for k in range(3):
                r = 250 + ((t * (240 if lab == 'TIME WARP!' else 90) + k * 90) % 270)
                a = int(150 * (1 - (r - 250) / 270))
                d2.ellipse([WX - r, WY - r, WX + r, WY + r], outline=col + (a,), width=10)
        layer(img, rings)
    # watch + hands
    ox, oy = int(WX - WATCH.width / 2), int(WY - WATCH.height / 2 + 6 * math.sin(t * 2))
    img.alpha_composite(WATCH, (ox, oy))
    cx, cy = ox + FCX, oy + FCY; sec = D[fd]
    def hands(d2):
        a = math.radians(sec * 30 - 90)       # one turn every 12s so the hand visibly sweeps
        d2.line([cx, cy, cx + math.cos(a) * FR * 0.85, cy + math.sin(a) * FR * 0.85], fill=(40, 30, 60, 255), width=12)
        a2 = math.radians(sec * 3 - 90)
        d2.line([cx, cy, cx + math.cos(a2) * FR * 0.55, cy + math.sin(a2) * FR * 0.55], fill=(150, 40, 60, 255), width=14)
        d2.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 214, 60, 255), outline=(40, 30, 60, 255), width=4)
    layer(img, hands)
    # melatonin gummy orbiting on sparkles
    an = t * 1.6; gx, gy = WX + 330 * math.cos(an), WY + 90 * math.sin(an) + 230
    def trail(d2):
        for k in range(10):
            a3 = an - k * 0.08; d2.rectangle([WX + 330 * math.cos(a3) - 4, WY + 90 * math.sin(a3) + 226, WX + 330 * math.cos(a3) + 4, WY + 90 * math.sin(a3) + 234], fill=(210, 170, 255, 200 - k * 18))
    layer(img, trail)
    img.alpha_composite(MEL, (int(gx - MEL.width / 2), int(gy - MEL.height / 2)))
    # readout plaque
    layer(img, lambda d2: d2.rounded_rectangle([180, 1270, 900, 1450], 26, fill=(18, 14, 34, 235), outline=(255, 214, 60, 255), width=8))
    txt = disp(f); col = (255, 255, 255) if f < F_STOP else (255, 214, 60)
    text_layer(img, [(W / 2, 1305, txt, 112, col, 0, 255)])
    # rayleigh
    if lab and t >= T_ST and f < F_STOP:
        fr = RCAST[int(t * 14) % len(RCAST)]
    else: fr = RID[int(t * 8) % len(RID)]
    img.alpha_composite(fr, (int(250 - fr.width / 2), int(1830 - 78 * 4)))
    if lab and t >= T_ST and f < F_STOP:
        text_layer(img, [(700, 1560, lab, 44, (210, 160, 255) if lab == 'TIME WARP!' else (150, 200, 255), 7, 255)])
    # sounds
    s_now = int(D[fd])
    if f < F_STOP and s_now > last_sec: ev.append((round(t, 3), 'tick_8bit')); last_sec = s_now
    for a, b, vv, lb in SEG:
        if lb and f == int(round(a * FPS)): ev.append((round(t, 3), 'whoosh_8bit'))
    if f == F_STOP: ev.append((round(t, 3), 'ding_8bit'))
    if f >= F_STOP:
        u = (f - F_STOP) / FPS; a = int(255 * min(1, u / 0.25))
        text_layer(img, [(W / 2, 1520, 'TIME!', 70, (255, 214, 60), 9, a)])
        if u > 0.5:
            a = int(255 * min(1, (u - 0.5) / 0.3))
            text_layer(img, [(W / 2, 1625, 'DID YOU GET 10.00?', 44, (255, 255, 255), 7, a), (W / 2, 1700, 'Comment your time', 32, (255, 230, 150), 5, a)])
    if t < T_ST:
        text_layer(img, [(W / 2, 1520, 'GET READY...', 48, (255, 255, 255), 7, 255)])
    w.write(img)
    if f % 20 == 0 or f in shows: img.convert('RGB').resize((270, 480)).save(OUT + f'p_{f:04d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev))
