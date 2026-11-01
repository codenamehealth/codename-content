import sys; sys.path.insert(0, '..')
from common7 import *
import math, random
G = '../gen/'; K = 3; FOOT = 78 * K
SRUN = {g: seq(PL + f'race/{g}_run', K) for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq(PL + 'maze/anim/hollow_srun', K)
SL = slime_frames(4)
def dr(d): return [up(crop(Image.open(p).convert('RGBA')), 1.55) for p in sorted(glob.glob(G + d + '/*.png'))]
DOZE = dr('ddoze'); GLARE = dr('dglare')
GUMK2 = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel', 'hollow': 'gold'}
GUMI = {k: gummy(k, 2) for k in GUMK}
BG = bg_frames('sun_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.72)
ICON = {}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
for n, p in SRC.items():
    im = Image.open(SP + 'syeda_src/' + p).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    ICON[n] = up(im.crop((cx - 16, 10, cx + 16, 44)), 2)
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
POW = {'joy': 'VINE DASH', 'cyrus': 'SUN SPRINT', 'cleo': 'SHIELD', 'ray': 'MOON FREEZE', 'hollow': 'SHADOW STEP'}
LANES = ['joy', 'cyrus', 'slimeA', 'cleo', 'ray', 'hollow']
LY = {n: 800 + i * 175 for i, n in enumerate(LANES)}
X0, XF = 120, 700
# light schedule
LIGHTS = [(0, 'wait'), (1.8, 'G'), (4.0, 'R'), (5.6, 'G'), (7.4, 'R'), (8.8, 'G'), (10.9, 'R'), (12.2, 'G')]
def light(t):
    cur = 'wait'; ts = 0
    for (a, s) in LIGHTS:
        if t >= a: cur, ts = s, a
    return cur, ts
SPD = {'joy': 77, 'cyrus': 73.5, 'cleo': 75, 'ray': 76, 'hollow': 73.5, 'slimeA': 68}
CAUGHT = {'slimeA': 4.25, 'hollow': 11.65}
DT = 1 / FPS
# simulate positions
pos = {n: float(X0) for n in LANES}; moving = {n: False for n in LANES}
TRACK = []; T_WIN = None; powers = []
for f in range(int(19 * FPS)):
    t = f * DT; L, ts = light(t)
    for n in LANES:
        if n in CAUGHT and t >= CAUGHT[n]: moving[n] = False; continue
        if T_WIN: moving[n] = False; continue
        v = 0
        if L == 'G' and t - ts > 0.12: v = SPD[n] * (1 + 0.12 * math.sin(t * 2.3 + len(n)))
        if n.startswith('slime') and n in CAUGHT and L == 'R' and t < CAUGHT[n]: v = SPD[n] * 0.8      # can't stop bouncing
        if n == 'hollow' and 10.95 < t < CAUGHT['hollow']: v = 70                                       # shadow step during red
        if n == 'cleo' and 7.4 <= t < 7.75: v = 45                                                        # mid-stride, shield blocks
        if n == 'cyrus' and t >= 12.55: v = 280
        if n == 'joy' and 6.0 <= t < 6.35: v = 77 + 156                                                   # vine dash
        pos[n] += v * DT; moving[n] = v > 1
        if n not in ('slimeA', 'slimeB') and pos[n] >= XF and T_WIN is None: T_WIN = t; WINNER = n
    TRACK.append(({n: pos[n] for n in LANES}, dict(moving)))
print('winner', WINNER, round(T_WIN, 2), {n: round(p) for n, p in pos.items()})
POWER_EV = [(4.0, 'ray', 'MOON FREEZE!'), (6.0, 'joy', 'VINE DASH!'), (7.45, 'cleo', 'BLOCKED!'), (10.95, 'hollow', 'SHADOW STEP!'), (12.5, 'cyrus', 'SUN SPRINT!')]
DUR = T_WIN + 3.6
wr = Writer('v75_noaudio.mp4'); ev = []
dist = {n: 0.0 for n in LANES}
def dragon_frame(t):
    L, ts = light(t); u = t - ts
    if L in ('wait', 'G'):
        if L == 'G' and ts > 0 and u < 0.45:      # turn away then doze
            k = int(u / 0.45 * 16)
            return GLARE[max(0, 8 - k)] if k < 8 else DOZE[min(8, k - 8)]
        return DOZE[8] if (L == 'G' or t > 0.4) else DOZE[min(8, int(t / 0.05))]
    k = int(u / 0.4 * 16)
    return DOZE[max(0, 8 - k)] if k < 8 else GLARE[min(8, k - 8)]
for f in range(int(DUR * FPS)):
    t = f / FPS; P, M = TRACK[min(f, len(TRACK) - 1)]; L, ts = light(t)
    img = BG[int(t * 4) % len(BG)].copy()
    # lanes, start + finish lines
    def lanes(dd):
        for n in LANES:
            y = LY[n]; dd.rounded_rectangle([60, y - 30, 1040, y + 40], 24, fill=(255, 240, 200, 34))
        for y in range(640, 1760, 28): dd.rectangle([XF - 4, y, XF + 4, y + 14], fill=(255, 214, 60, 230))
        dd.rectangle([X0 - 60, 640, X0 - 54, 1740], fill=(255, 255, 255, 120))
    layer(img, lanes)
    # dragon
    df = dragon_frame(t); dx, dy = 745, 1270 - df.height // 2
    img.alpha_composite(df, (dx, dy))
    if L == 'R' and t - ts > 0.4:
        layer(img, lambda dd: dd.ellipse([dx + df.width * 0.42, dy + 30, dx + df.width * 0.62, dy + 90], fill=(255, 40, 40, 70)))
    if L in ('G', 'wait'):
        zz = int(t * 2) % 3; text_layer(img, [(dx + df.width * 0.62 + zz * 18, dy - 10 - zz * 22, 'z' * (zz + 1), 30, (230, 230, 255), 4, 220)])
    # runners
    for n in LANES:
        x, y = P[n], LY[n]
        if M[n]: dist[n] += 1
        caught = n in CAUGHT and t >= CAUGHT[n]
        if n.startswith('slime'):
            spr = SL[int(t * 10 + len(n)) % len(SL)] if not caught else SL[0]; foot = 62 * 4
        else:
            fr = SRUN[n]; spr = fr[int(dist[n] / 3.2) % 8]; foot = FOOT
            if n == 'hollow' and 10.95 <= t < CAUGHT['hollow']:
                spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda a: a // 3))
        if caught:
            g = ImageEnhance.Color(spr).enhance(0); g = ImageEnhance.Brightness(g).enhance(0.75); spr = g
        layer(img, lambda dd, x=x, y=y: dd.ellipse([x - 52, y + 10, x + 52, y + 30], fill=(0, 0, 0, 80)))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y + 20 - foot)))
        if n in CAUGHT and 0 <= t - CAUGHT[n] < 1.1:
            u = t - CAUGHT[n]
            if u < 0.35: layer(img, lambda dd, x=x, y=y: dd.line([(dx + df.width * 0.52, dy + 70), (x, y - 80)], fill=(255, 60, 60, 200), width=8))
            text_layer(img, [(x, y - (60 if n.startswith('slime') else 120) - u * 30, 'CAUGHT!', 34, (255, 80, 80), 5, int(255 * min(1, (1.1 - u) / 0.3)))])
            if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'poof'))
    for (te, n, txt) in POWER_EV:
        u = t - te
        if 0 <= u < 1.3:
            x, y = P[n], LY[n]; a = int(255 * min(1, (1.3 - u) / 0.35))
            if u < 0.4:
                g = GUMI[GUMK2[n]]; img.alpha_composite(g, (int(x - g.width / 2), int(y - 270 - u * 40)))
            if n == 'ray' or n == 'cleo':
                layer(img, lambda dd, x=x, y=y, n=n: dd.ellipse([x - 90, y - 220, x + 90, y + 40], outline=RING[n] + (int(200 * (1 - u / 1.3)),), width=6))
            if n == 'cyrus' and t < T_WIN:
                layer(img, lambda dd, x=x, y=y: [dd.line([(x - 60 - q * 40, y - 60 - q * 20), (x - 140 - q * 40, y - 60 - q * 20)], fill=(255, 200, 80, 200), width=6) for q in range(3)])
            text_layer(img, [(min(880, max(200, x)), y - 300 - u * 20, txt, 32, RING[n], 5, a)])
            if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'sword_hit' if n == 'cleo' else 'powerup_8bit'))
    # header
    layer(img, lambda dd: dd.rectangle([0, 0, W, 520], fill=(16, 12, 24, 200)))
    text_layer(img, [(W / 2, 40, 'RED LIGHT', 64, (240, 70, 60), 8, 255), (W / 2, 120, 'GREEN LIGHT', 64, (90, 220, 90), 8, 255),
                     (W / 2, 205, 'Every guide has one power', 28, (255, 255, 255), 4, 255)])
    for i, n in enumerate(['joy', 'cyrus', 'cleo', 'ray', 'hollow']):
        cx = 20 + i * 208 + 104
        used = any(t >= te and nn == n for (te, nn, _) in POWER_EV)
        out = n in CAUGHT and t >= CAUGHT[n]
        layer(img, lambda dd, cx=cx, n=n, used=used: dd.rounded_rectangle([cx - 98, 262, cx + 98, 398], 14, fill=(30, 24, 44, 230), outline=(RING[n] if used else (90, 80, 110)) + (255,), width=5))
        ic = ICON[n] if not out else ImageEnhance.Color(ICON[n]).enhance(0)
        img.alpha_composite(ic, (cx - ic.width // 2, 270))
        text_layer(img, [(cx, 352, POW[n], 15, RING[n] if not out else (130, 130, 130), 3, 255)])
    col = (60, 210, 80) if L == 'G' else ((230, 60, 50) if L == 'R' else (120, 120, 140))
    lab = 'GREEN LIGHT' if L == 'G' else ('RED LIGHT' if L == 'R' else 'GET READY')
    layer(img, lambda dd: dd.rounded_rectangle([W / 2 - 200, 420, W / 2 + 200, 490], 30, fill=col + (255,), outline=(255, 255, 255, 255), width=4))
    text_layer(img, [(W / 2, 437, lab, 32, (255, 255, 255), 4, 255)])
    if L != 'wait' and abs(t - ts) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit' if L == 'G' else 'buzz_8bit'))
    if t < 1.8: text_layer(img, [(W / 2, 1800, 'PICK A PLAYER!', 54, (255, 255, 255), 8, 255)])
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, 520, W, H], fill=(8, 6, 14, int(130 * a))))
        if not hasattr(sys, '_vf'): sys._vf = vic(WINNER, 380)
        vf = sys._vf[int(u * 8) % len(sys._vf)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1300 - vf.height))
        text_layer(img, [(W / 2, 1340, f'{WINNER.upper()} WINS!', 64, (255, 214, 60), 8, int(255 * a)), (W / 2, 1450, 'Did your pick make it?', 34, (255, 255, 255), 5, int(255 * a))])
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'victory')); ev.append((round(t + 0.2, 3), 'cheer'))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('v75_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
