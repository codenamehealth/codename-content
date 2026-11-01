import sys, os; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import math, random
G = SP + 'fork_a7/gen/'; K = 3; FOOT = 78 * K
SRUN = {g: seq(PL + f'race/{g}_run', K) for g in ['joy', 'cyrus', 'cleo', 'ray']}   # HOLLOW RULE: the Hollow is no longer a racer
SL = slime_frames(4)
def dr(d): return [up(crop(Image.open(p).convert('RGBA')), 1.55) for p in sorted(glob.glob(G + d + '/*.png'))]
DOZE = dr('ddoze'); GLARE = dr('dglare')
GUMK2 = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel'}
GUMI = {k: gummy(k, 2) for k in GUMK}
BG = bg_frames('sun_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.72)
ICON = {}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
for n, p in SRC.items():
    im = Image.open(SP + 'syeda_src/' + p).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    ICON[n] = up(im.crop((cx - 16, 10, cx + 16, 44)), 2)
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
POW = {'joy': 'VINE DASH', 'cyrus': 'SUN SPRINT', 'cleo': 'SHIELD', 'ray': 'MOON FREEZE', 'hollow': 'SHADOW STEP'}
LANES = ['slimeA', 'joy', 'cyrus', 'cleo', 'ray']      # slime on top so the power pops stay under the header
X0, XF = 120, 700                                       # sim coordinates (unchanged)
SX0, KX = 130, 0.8                                      # screen: start x130, finish x594 (runners unchanged 3x)
def TX(x): return SX0 + (x - X0) * KX
HA, HB = hook_layer(['RED LIGHT,', 'GREEN LIGHT'], accent=0, color=(240, 70, 60), sub='EVERY GUIDE HAS ONE POWER', border=(255, 214, 60))
HG, _ = hook_layer(['RED LIGHT,', 'GREEN LIGHT'], accent=1, color=(90, 220, 90), sub='EVERY GUIDE HAS ONE POWER', border=(255, 214, 60))
HOOK = HA.copy(); HOOK.paste(HG.crop((0, 383, W, H)), (0, 383))
CY0, CY1 = HB + 8, HB + 118                             # power cards + light pill row
LY = {'slimeA': CY1 + 104, 'joy': 964, 'cyrus': 1132, 'cleo': 1300, 'ray': 1468}   # slime is short, guides get 168px lanes
# light schedule
LIGHTS = [(0, 'wait'), (1.8, 'G'), (4.0, 'R'), (5.6, 'G'), (7.4, 'R'), (8.8, 'G'), (10.9, 'R'), (12.2, 'G')]
def light(t):
    cur = 'wait'; ts = 0
    for (a, s) in LIGHTS:
        if t >= a: cur, ts = s, a
    return cur, ts
SPD = {'joy': 77, 'cyrus': 73.5, 'cleo': 75, 'ray': 76, 'slimeA': 68}
CAUGHT = {'slimeA': 4.25}
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
        if n == 'cleo' and 7.4 <= t < 7.75: v = 45                                                        # mid-stride, shield blocks
        if n == 'cyrus' and t >= 12.55: v = 280
        if n == 'joy' and 6.0 <= t < 6.35: v = 77 + 156                                                   # vine dash
        pos[n] += v * DT; moving[n] = v > 1
        if n not in ('slimeA', 'slimeB') and pos[n] >= XF and T_WIN is None: T_WIN = t; WINNER = n
    TRACK.append(({n: pos[n] for n in LANES}, dict(moving)))
print('winner', WINNER, round(T_WIN, 2), {n: round(p) for n, p in pos.items()}, 'LY', LY, 'HB', HB)
POWER_EV = [(4.0, 'ray', 'MOON FREEZE!'), (6.0, 'joy', 'VINE DASH!'), (7.45, 'cleo', 'BLOCKED!'), (12.5, 'cyrus', 'SUN SPRINT!')]
DUR = T_WIN + 3.6
wr = Writer('v73_noaudio.mp4'); ev = []
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
            y = LY[n]; dd.rounded_rectangle([72, y - 30, 880, y + 40], 24, fill=(255, 240, 200, 34))
        for y in range(CY1 + 24, LY['ray'] + 30, 28): dd.rectangle([TX(XF) - 4, y, TX(XF) + 4, y + 14], fill=(255, 214, 60, 230))
        dd.rectangle([TX(X0) - 56, CY1 + 24, TX(X0) - 50, LY['ray'] + 30], fill=(255, 255, 255, 120))
    layer(img, lanes)
    # dragon
    df = dragon_frame(t); dx, dy = 1022 - df.width, 1104 - df.height   # top-right, fully above y1110
    img.alpha_composite(df, (dx, dy))
    if L == 'R' and t - ts > 0.4:
        layer(img, lambda dd: dd.ellipse([dx + df.width * 0.42, dy + 30, dx + df.width * 0.62, dy + 90], fill=(255, 40, 40, 70)))
    if L in ('G', 'wait'):
        zz = int(t * 2) % 3; text_layer(img, [(dx + df.width * 0.62 + zz * 18, max(CY1 + 10, dy - 10 - zz * 22), 'z' * (zz + 1), 30, (230, 230, 255), 4, 220)])
    # runners
    for n in LANES:
        x, y = TX(P[n]), LY[n]
        if M[n]: dist[n] += 1
        caught = n in CAUGHT and t >= CAUGHT[n]
        if n.startswith('slime'):
            spr = SL[int(t * 10 + len(n)) % len(SL)] if not caught else SL[0]; foot = 62 * 4
        else:
            fr = SRUN[n]; spr = fr[int(dist[n] / 3.2) % 8]; foot = FOOT
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
            x, y = TX(P[n]), LY[n]; a = int(255 * min(1, (1.3 - u) / 0.35))
            if u < 0.4:
                g = GUMI[GUMK2[n]]; img.alpha_composite(g, (int(x - g.width / 2), int(y - 240 - u * 40)))
            if n == 'ray' or n == 'cleo':
                layer(img, lambda dd, x=x, y=y, n=n: dd.ellipse([x - 90, y - 220, x + 90, y + 40], outline=RING[n] + (int(200 * (1 - u / 1.3)),), width=6))
            if n == 'cyrus' and t < T_WIN:
                layer(img, lambda dd, x=x, y=y: [dd.line([(x - 60 - q * 40, y - 60 - q * 20), (x - 140 - q * 40, y - 60 - q * 20)], fill=(255, 200, 80, 200), width=6) for q in range(3)])
            hw = len(txt) * 16 + 6; text_layer(img, [(min(880 - hw, max(72 + hw, x)), max(CY1 + 14, y - 290 - u * 20), txt, 32, RING[n], 5, a)])
            if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'sword_hit' if n == 'cleo' else 'powerup_8bit'))
    # header
    for i, n in enumerate(['joy', 'cyrus', 'cleo', 'ray']):
        cx = 74 + i * 170 + 80
        used = any(t >= te and nn == n for (te, nn, _) in POWER_EV)
        out = n in CAUGHT and t >= CAUGHT[n]
        layer(img, lambda dd, cx=cx, n=n, used=used: dd.rounded_rectangle([cx - 80, CY0, cx + 80, CY1], 14, fill=(30, 24, 44, 235), outline=(RING[n] if used else (90, 80, 110)) + (255,), width=5))
        ic = ICON[n] if not out else ImageEnhance.Color(ICON[n]).enhance(0)
        img.alpha_composite(ic, (cx - ic.width // 2, CY0 + 8))
        text_layer(img, [(cx, CY0 + 82, POW[n], 14, RING[n] if not out else (130, 130, 130), 3, 255)])
    col = (60, 210, 80) if L == 'G' else ((230, 60, 50) if L == 'R' else (120, 120, 140))
    lab = ('GREEN', 'LIGHT') if L == 'G' else (('RED', 'LIGHT') if L == 'R' else ('PICK A', 'PLAYER!'))
    layer(img, lambda dd: dd.rounded_rectangle([756, CY0, 1022, CY1], 26, fill=col + (255,), outline=(255, 255, 255, 255), width=4))
    lc = (255, 214, 60) if L == 'wait' else (255, 255, 255)
    text_layer(img, [(889, CY0 + 14, lab[0], 32, lc, 5, 255), (889, CY0 + 60, lab[1], 32, lc, 5, 255)])
    if L != 'wait' and abs(t - ts) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit' if L == 'G' else 'buzz_8bit'))
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, CY1 + 6, W, H], fill=(8, 6, 14, int(130 * a))))
        if not hasattr(sys, '_vf'): sys._vf = vic(WINNER, 380)
        vf = sys._vf[int(u * 8) % len(sys._vf)]; img.alpha_composite(vf, (478 - vf.width // 2, 1290 - vf.height))
        text_layer(img, [(478, 1316, f'{WINNER.upper()} WINS!', 64, (255, 214, 60), 8, int(255 * a)), (478, 1420, 'Did your pick make it?', 34, (255, 255, 255), 5, int(255 * a))])
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'victory')); ev.append((round(t + 0.2, 3), 'cheer'))
    img.alpha_composite(HOOK)
    wr.write(img)
wr.close(); json.dump(ev, open('v73_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
