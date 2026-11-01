import sys, os; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
sys.path.insert(0, SP + 'fork_hfg5'); from hk import hook_fade_segs
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import math, random
G = SP + 'fork_a7/gen/'; K = 3; FOOT = 78 * K
SRUN = {g: seq(PL + f'race/{g}_run', K) for g in ['joy', 'cyrus', 'cleo', 'ray']}   # HOLLOW RULE: the Hollow is no longer a racer
SL = slime_frames(4)
def dr(d): return [up(crop(Image.open(p).convert('RGBA')), 1.55) for p in sorted(glob.glob(G + d + '/*.png'))]
sys.path.insert(0, SP + 'fork_c7'); from degold import dragon_gummy
_RAW = dragon_gummy([Image.open(p).convert('RGBA') for d_ in ('ddoze', 'dglare') for p in sorted(glob.glob(G + d_ + '/*.png'))], 150, 1)   # recut: gold hoard -> gummy pile
_RAW = [up(crop(im), 1.55) for im in _RAW]; DOZE, GLARE = _RAW[:9], _RAW[9:]
GUMK2 = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel'}
GUMI = {k: gummy(k, 2) for k in GUMK}
BG = bg_frames('sun_hd.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.72)
ICON = {}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
for n, p in SRC.items():
    im = Image.open(SP + 'syeda_src/' + p).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    ICON[n] = up(im.crop((cx - 16, 10, cx + 16, 44)), 2)
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
POW = {'joy': 'SHIELD', 'cyrus': 'SPEED', 'cleo': 'STRONG', 'ray': 'SLEEP'}   # GUMMY POWERS rule (SPEC 12)
T_JOY, T_CLEO, T_RAY, T_CY = 4.0, 4.8, 7.0, float(os.environ.get('TCY', str(290 / 30)))   # recut: same green-phase offsets, red phases shortened
CRATE = up(crop(Image.open(SP + 'fork_b6/gen/crate/00.png').convert('RGBA')), 4)
LANES = ['slimeA', 'joy', 'cyrus', 'cleo', 'ray']      # slime on top so the power pops stay under the header
X0, XF = 120, 700                                       # sim coordinates (unchanged)
SX0, KX = 130, 0.8                                      # screen: start x130, finish x594 (runners unchanged 3x)
def TX(x): return SX0 + (x - X0) * KX
# hfg8: soft-fade hook, no box. The hook IS the light: the active line lights up in its colour (flashes white on each switch),
# the other line dims. Replaces the boxed light bar (RED LIGHT!/GREEN LIGHT!/PICK A PLAYER!) and the gummy cards row.
RED_, GRN_, DIM_ = (240, 70, 60), (90, 220, 90), (128, 122, 140)
HOOKV = {'wait': hook_fade_segs([[('RED LIGHT,', RED_)], [('GREEN LIGHT', GRN_)]], size=72),
         'R': hook_fade_segs([[('RED LIGHT,', RED_)], [('GREEN LIGHT', DIM_)]], size=72),
         'G': hook_fade_segs([[('RED LIGHT,', DIM_)], [('GREEN LIGHT', GRN_)]], size=72),
         'Rf': hook_fade_segs([[('RED LIGHT,', (255, 255, 255))], [('GREEN LIGHT', DIM_)]], size=72),
         'Gf': hook_fade_segs([[('RED LIGHT,', DIM_)], [('GREEN LIGHT', (255, 255, 255))]], size=72)}
HB = HOOKV['wait'][1]
HOOKE, _ = hook_fade(['DID YOUR', 'PICK WIN?'], accent=1, size=72)   # end question replaces the hook text in the same fade
CY0, CY1 = 576, 616                                    # hfg8: field raised 70px into the space the header freed
LY = {'slimeA': CY1 + 104, 'joy': 905, 'cyrus': 1092, 'cleo': 1280, 'ray': 1468}   # guides get ~188px lanes (were 168)

# #73 note: "characters floating" -> new ground. A flat grass race field (pixel art at 1/4 res, 4x) fills everything below
# FIELD_TOP; every lane is a dirt running lane with chalk edges, so each runner's feet are on the ground; the temple stays as
# the backdrop behind the field's hedge line; the dragon sits on the grass past the finish line.
FIELD_TOP = CY1 + 44
def build_field():
    q = 4; fw, fh = W // q, H // q; f0 = FIELD_TOP // q
    im = Image.new('RGBA', (fw, fh), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rr = random.Random(73)
    d.rectangle([0, f0, fw, fh], fill=(86, 150, 64, 255))
    for _ in range(2600):
        x, y = rr.randint(0, fw - 1), rr.randint(f0 + 3, fh - 1); d.point((x, y), fill=rr.choice([(74, 134, 54), (100, 166, 74), (66, 122, 48)]) + (255,))
    for _ in range(260):
        x, y = rr.randint(0, fw - 2), rr.randint(f0 + 4, fh - 2); c = rr.choice([(120, 186, 84), (58, 112, 42)]); d.line([x, y, x, y - 1], fill=c + (255,))
    # dirt lanes
    for n in LANES:
        y = (LY[n] + 20) // q; y0, y1 = y - 11, y + 7
        d.rectangle([18, y0, 172, y1], fill=(196, 152, 98, 255))
        for _ in range(150):
            x, yy = rr.randint(18, 172), rr.randint(y0, y1); d.point((x, yy), fill=rr.choice([(180, 136, 84), (208, 166, 112), (170, 128, 80)]) + (255,))
        d.line([18, y0, 172, y0], fill=(244, 240, 226, 255)); d.line([18, y1, 172, y1], fill=(244, 240, 226, 255))
        d.line([18, y0 - 1, 172, y0 - 1], fill=(60, 110, 44, 255)); d.line([18, y1 + 1, 172, y1 + 1], fill=(60, 110, 44, 255))
        # start line + chequered finish on the dirt
        sx = int((TX(X0) - 53) // q); d.line([sx, y0, sx, y1], fill=(244, 240, 226, 255))
        fx = int(TX(XF) // q)
        for yy in range(y0 + 1, y1):
            for xx in (fx - 1, fx, fx + 1): d.point((xx, yy), fill=(20, 20, 24, 255) if (xx + yy) % 2 else (250, 250, 250, 255))
    # hedge + stone curb along the top edge of the field (the field's horizon)
    for x in range(-2, fw + 2, 6):
        h = rr.randint(5, 8); d.ellipse([x - 4, f0 - h, x + 5, f0 + 3], fill=(44, 98, 40, 255), outline=(28, 64, 26, 255))
        d.point((x, f0 - h + 2), fill=(96, 160, 70, 255))
    d.rectangle([0, f0 + 2, fw, f0 + 4], fill=(150, 140, 128, 255)); d.line([0, f0 + 2, fw, f0 + 2], fill=(196, 188, 176, 255)); d.line([0, f0 + 5, fw, f0 + 5], fill=(70, 66, 60, 255))
    return up(im, q)
FIELD = build_field()
# light schedule
LIGHTS = [(0, 'wait'), (0.5, 'G'), (2.7, 'R'), (3.6, 'G'), (5.4, 'R'), (6.4, 'G'), (8.5, 'R'), (9.4, 'G')]   # recut: green phases unchanged (2.2/1.8/2.1s), reds 1.6/1.4/1.3 -> 0.9/1.0/0.9, pick 1.8 -> 0.5s
def light(t):
    cur = 'wait'; ts = 0
    for (a, s) in LIGHTS:
        if t >= a: cur, ts = s, a
    return cur, ts
SPD = {'joy': 77, 'cyrus': 73.5, 'cleo': 75, 'ray': 76, 'slimeA': 68}
CAUGHT = {'slimeA': 2.95}
NEAR = ('ray', 8.5, 0.3)   # recut: near miss, Ray is still moving 0.3s into the 3rd red light and freezes just in time (SAFE!)
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
        if n in ('cyrus', 'cleo') and T_RAY <= t < T_RAY + 1.0: v = 0                                   # Ray's melatonin: asleep 1s (Joy's shield blocks it)
        if n == 'cyrus' and t >= T_CY + 0.05: v = 280                                                   # mushroom: SPEED
        if n == NEAR[0] and NEAR[1] <= t < NEAR[1] + NEAR[2]: v = SPD[n]
        pos[n] += v * DT; moving[n] = v > 1
        if n not in ('slimeA', 'slimeB') and pos[n] >= XF and T_WIN is None: T_WIN = t; WINNER = n
    TRACK.append(({n: pos[n] for n in LANES}, dict(moving)))
    if abs(t - T_CLEO) < DT / 2: CRATE_X = pos['cleo'] + 40
print('winner', WINNER, round(T_WIN, 2), {n: round(p) for n, p in pos.items()}, 'LY', LY, 'HB', HB)
POWER_EV = [(T_JOY, 'joy', 'SHIELD!'),   # hfg8: no ACV tags
            (T_CLEO, 'cleo', 'STRONG!'), (T_RAY, 'ray', 'SLEEP!'), (T_CY, 'cyrus', 'SPEED!')]
print('crate x', round(CRATE_X))
CRB = [CRATE.crop((0, 0, CRATE.width // 2, CRATE.height // 2)), CRATE.crop((CRATE.width // 2, 0, CRATE.width, CRATE.height // 2)), CRATE.crop((0, CRATE.height // 2, CRATE.width // 2, CRATE.height)), CRATE.crop((CRATE.width // 2, CRATE.height // 2, CRATE.width, CRATE.height))]
DUR = T_WIN + 1.5 + 0.2; T_LOOP = DUR - 0.2   # recut: win held 1.5s, last 0.2s = opening state (loop)
if len(sys.argv) > 1: Image.alpha_composite(BG[0], FIELD).convert('RGB').resize((540, 960)).save('field.png'); print('FIELD_TOP', FIELD_TOP); sys.exit()
wr = Writer('v73_noaudio.mp4'); ev = []
ICONS_G = {n: gummy(GUMK2[n], 2) for n in POW}
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
    t = f / FPS
    if t >= T_LOOP:   # cut back to the opening state (same jog phase as frame 0)
        if not getattr(sys, '_lp', False): sys._lp = True; dist = {n: 0.0 for n in LANES}
        t = 0.0; f = 0
    P, M = TRACK[min(f, len(TRACK) - 1)]; L, ts = light(t)
    img = BG[int(t * 4) % len(BG)].copy()
    img.alpha_composite(FIELD)   # ground: grass field with one dirt lane per runner
    # dragon
    df = dragon_frame(t); dx, dy = 1022 - df.width, 1104 - df.height   # top-right, fully above y1110
    img.alpha_composite(df, (dx, dy))
    if L == 'R' and t - ts > 0.4:
        layer(img, lambda dd: dd.ellipse([dx + df.width * 0.42, dy + 30, dx + df.width * 0.62, dy + 90], fill=(255, 40, 40, 70)))
    # Cleo's crate: smashed by her creatine STRONG! at T_CLEO
    cx_, cy_ = TX(CRATE_X), LY['cleo'] + 20
    if t < T_CLEO: img.alpha_composite(CRATE, (int(cx_ - CRATE.width / 2), int(cy_ - CRATE.height)))
    elif t < T_CLEO + 0.8:
        u = t - T_CLEO
        for q, pc in enumerate(CRB):
            sx, sy = (-1 if q % 2 == 0 else 1), (-1 if q < 2 else -0.4)
            pc2 = pc.copy(); pc2.putalpha(pc2.getchannel('A').point(lambda a, u=u: int(a * max(0, 1 - u / 0.8))))
            img.alpha_composite(pc2, (int(cx_ - CRATE.width / 2 + (q % 2) * CRATE.width / 2 + sx * 260 * u), int(cy_ - CRATE.height + (q // 2) * CRATE.height / 2 + sy * 300 * u + 500 * u * u)))
    # runners
    for n in LANES:
        x, y = TX(P[n]), LY[n]
        if M[n]: dist[n] += 1
        elif L == 'wait': dist[n] += 0.55   # reel lesson: jog in place at the start line (no frozen line-up)
        caught = n in CAUGHT and t >= CAUGHT[n]
        if n.startswith('slime'):
            spr = SL[int(t * 10 + len(n)) % len(SL)] if not caught else SL[0]; foot = 62 * 4
        else:
            fr = SRUN[n]; spr = fr[int(dist[n] / 3.2) % 8]; foot = FOOT
        if caught:
            g = ImageEnhance.Color(spr).enhance(0); g = ImageEnhance.Brightness(g).enhance(0.75); spr = g
        layer(img, lambda dd, x=x, y=y: dd.ellipse([x - 52, y + 10, x + 52, y + 30], fill=(0, 0, 0, 80)))
        if n == 'cyrus' and T_CY + 0.05 <= t < T_WIN:     # dust trail behind the sprint
            layer(img, lambda dd, x=x, y=y: [dd.ellipse([x - 70 - q * 34 - 14 + q * 3, y + 4 - q * 3, x - 70 - q * 34 + 14 - q * 3, y + 28 - q * 3], fill=(200, 170, 120, 150 - q * 30)) for q in range(5)])
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y + 20 - foot)))
        if n == 'joy' and T_JOY <= t < T_RAY:              # ACV shield bubble until it blocks the sleep
            layer(img, lambda dd, x=x, y=y: dd.ellipse([x - 92, y - 190, x + 92, y + 34], fill=(90, 220, 90, 46), outline=(120, 240, 120, 210), width=5))
        if n == 'joy' and T_RAY <= t < T_RAY + 0.45:       # bubble pops
            u = (t - T_RAY) / 0.45; rr = 92 + 70 * u
            layer(img, lambda dd, x=x, y=y, rr=rr, u=u: dd.ellipse([x - rr, y - 78 - rr * 1.2, x + rr, y - 78 + rr * 1.2], outline=(120, 240, 120, int(220 * (1 - u))), width=6))
        if n in ('cyrus', 'cleo') and T_RAY + 0.3 <= t < T_RAY + 1.0:   # asleep (Zzz staggered 0.3s after SLEEP!)
            zz = int(t * 3) % 3; text_layer(img, [(x + 30 + zz * 14, y - 200 - zz * 18, 'Z' * (zz + 1), 30, (225, 205, 255), 5, 255)])
        if n in CAUGHT and 0 <= t - CAUGHT[n] < 1.1:
            u = t - CAUGHT[n]
            if u < 0.35: layer(img, lambda dd, x=x, y=y: dd.line([(dx + df.width * 0.52, dy + 70), (x, y - 80)], fill=(255, 60, 60, 200), width=8))
            sc = 1 + 0.3 * max(0, 1 - u / 0.18)   # big OUT stamp, same weight as the win stamp
            text_layer(img, [(478, y - 40 - int(16 * (sc - 1)), 'CAUGHT!', int(64 * sc), (255, 70, 60), 9, int(255 * min(1, (1.1 - u) / 0.3)))])
            if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'poof'))
    for (te, n, txt) in POWER_EV:
        u = t - te
        if 0 <= u < 1.3:
            x, y = TX(P[n]), LY[n]; a = int(255 * min(1, (1.3 - u) / 0.35))
            if u < 0.4:
                g = GUMI[GUMK2[n]]; img.alpha_composite(g, (int(x - g.width / 2), int(y - 240 - u * 40)))
            if n == 'ray' and u < 0.9:     # sleep wave rolls out over the other lanes
                rr = 90 + 900 * u / 0.9
                layer(img, lambda dd, x=x, y=y, rr=rr, u=u: dd.ellipse([x - rr, y - 90 - rr, x + rr, y - 90 + rr], outline=(190, 90, 240, int(220 * (1 - u / 0.9))), width=10))
            if n == 'cleo' and u < 0.5:
                layer(img, lambda dd, x=x, y=y, u=u: [dd.line([(x + 60, y - 90), (x + 60 + 90 * math.cos(a_) * (0.4 + u), y - 90 + 90 * math.sin(a_) * (0.4 + u))], fill=(255, 240, 160, int(230 * (1 - u / 0.5))), width=7) for a_ in [k_ * math.pi / 4 for k_ in range(8)]])
            if n == 'cyrus' and t < T_WIN:
                layer(img, lambda dd, x=x, y=y: [dd.line([(x - 60 - q * 40, y - 60 - q * 20), (x - 140 - q * 40, y - 60 - q * 20)], fill=(255, 200, 80, 200), width=6) for q in range(3)])
            hw = len(txt) * 24 + 6; text_layer(img, [(min(880 - hw, max(72 + hw, x)), max(CY1 + 14, y - 300 - u * 20), txt, 48, RING[n], 7, a)])
            if abs(u) < 0.5 / FPS:
                ev.append((round(t, 3), 'powerup_8bit'))
                if n == 'cleo': ev.append((round(t + 0.05, 3), 'crunch_8bit'))
                if n == 'ray': ev.append((round(t + 0.1, 3), 'poofpops'))
                if n == 'cyrus': ev.append((round(t + 0.05, 3), 'whoosh_8bit'))
    if T_RAY + 0.6 <= t < T_RAY + 1.6:      # Joy's shield blocks the sleep (staggered after SLEEP! and the Zzz, on Joy)
        a = int(255 * min(1, (T_RAY + 1.6 - t) / 0.3)); jx = TX(P['joy'])
        text_layer(img, [(min(880 - 198, max(72 + 198, jx)), max(CY1 + 14, LY['joy'] - 260), 'BLOCKED!', 48, (120, 240, 120), 7, a)])
    if NEAR[1] + NEAR[2] <= t < NEAR[1] + NEAR[2] + 1.0:   # near miss
        u = t - NEAR[1] - NEAR[2]; a = int(255 * min(1, (1.0 - u) / 0.3)); sc = 1 + 0.3 * max(0, 1 - u / 0.18); nx = TX(P[NEAR[0]])
        text_layer(img, [(478, LY[NEAR[0]] - 300 - int(16 * (sc - 1)), 'RAYLEIGH: SAFE!', int(52 * sc), (255, 255, 255), 9, a)])   # kept with the name: it sits between two lanes
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'boing'))
    # hfg8: gummy cards row + boxed light bar cut; the hook lines are the light (active line lit, flashes white for 0.25s on a switch)
    u = t - ts; fl = L != 'wait' and u < 0.25 and int(u * 16) % 2 == 0
    HOOK = HOOKV['wait'] if L == 'wait' else HOOKV[L + ('f' if fl else '')][0]
    if L == 'wait': HOOK = HOOK[0]
    if L != 'wait' and abs(t - ts) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit' if L == 'G' else 'buzz_8bit'))
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, CY1 + 6, W, H], fill=(8, 6, 14, int(130 * a))))
        if not hasattr(sys, '_vf'): sys._vf = vic(WINNER, 380)
        vf = sys._vf[int(u * 8) % len(sys._vf)]; img.alpha_composite(vf, (478 - vf.width // 2, 1290 - vf.height))
        text_layer(img, [(478, 1316, f'{WINNER.upper()} WINS!', 64, (255, 214, 60), 8, int(255 * a))])   # hfg8: question moved into the hook fade
        HOOK = HOOKE
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'victory')); ev.append((round(t + 0.2, 3), 'cheer'))
    img.alpha_composite(HOOK)
    wr.write(img)
wr.close(); json.dump({'events': ev}, open('v73_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
