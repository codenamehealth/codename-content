import sys, os, math, random, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c7'); from powers import *
POWER['cre'] = ('STRENGTH!', POWER['cre'][1])   # n8 Oct 29: creatine power word is STRENGTH, never STRONG
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import gummy_src, FF
HOOK, HB = hook_fade(['Can you spot', 'the cheater?'], accent=1, color=(255, 214, 60))   # n14 Oct 29: job hook (Bennett-approved idea), same soft fade + size
NAMES = ['joy', 'cleo', 'cyrus', 'ray']  # Hollow rule: the Hollow is the player, never a pickable champion
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel', 'hollow': 'gold'}
SWIM_SRC = {'joy': ('joy_swim', [4, 5, 6, 7, 8]), 'ray': ('ray_swim', [3, 4, 5, 6, 7, 8]), 'cyrus': ('cyrus_swim', [3, 4, 5, 6, 7, 8]),
            'cleo': ('cleo_swim3', [4, 5, 6, 7, 8])}
SS = 4   # rc18: swimmers 3x -> 4x (review: bigger swimmers; VETTING: within the safe zone)
SWIM = {}
for g, (d, idx) in SWIM_SRC.items():
    fr = [Image.open(f'/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/{d}/{i:02d}.png').convert('RGBA') for i in idx]
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    SWIM[g] = [up(f.crop(bb), SS) for f in fr]
_CA = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(SP + 'pixellab/race/cleo_atk/*.png'))]
_cb = None
for f in _CA:
    b = f.getbbox(); _cb = b if _cb is None else (min(_cb[0], b[0]), min(_cb[1], b[1]), max(_cb[2], b[2]), max(_cb[3], b[3]))
CATK = [up(f.crop(_cb), SS) for f in _CA]; CATK_WAIST = (75 - _cb[1]) * SS      # waterline at her waist (sprite y ~75 of 40-104)
CATK_CX = (28 - _cb[0]) * SS                                                     # body centre column (sprite x ~28)
# n14: the cheater = a green slime (existing race slime idle frames, pixellab/race/slime_idle_c) under the water pushing Cleo's feet the whole race
import glob as _g, numpy as _np
def _nored(im):
    a = _np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
_SL = [_nored(Image.open(f).convert('RGBA')) for f in sorted(_g.glob(SP + 'pixellab/race/slime_idle_c/*.png'))]
_bb = None
for f in _SL:
    b = f.getbbox(); _bb = b if _bb is None else (min(_bb[0], b[0]), min(_bb[1], b[1]), max(_bb[2], b[2]), max(_bb[3], b[3]))
SLK = 3; SLIME = [up(f.crop(_bb), SLK) for f in _SL]     # faces right (eyes on the right)
SL_ALPHA = float(os.environ.get('SLA', '0.42'))       # under-water visibility during the race (subtle, findable on a rewatch)
REV = dict(rise=0.0, ta=None)                          # set during the reveal: rise 0..1 (eyes break the surface), ta = slime anim time
SLBOX = [None]
# scene
BGF = bg_frames('found_hd.gif', (W, H), box=(1100, 0, 1707, 1080), step=2, bright=0.95)
STONE = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/stair/00.png').convert('RGBA')), 2)
BUOY = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork4/buoy/04.png').convert('RGBA')), 2)
PX0, PX1, PY0, PY1 = -40, 1120, -40, 1960   # Oct 29: full-bleed pool (Bennett: 'should go the full length'), stone border off-frame
NL = 4; LY0, LY1 = HB + 16, 1520; LH = (LY1 - LY0) / NL   # lanes 470-1520: every swimmer, face icon and stamp stays inside the safe zone
LANEY = [LY0 + LH * (i + 0.5) for i in range(NL)]
SX0, SX1 = 80, 877   # safe x range for stamps (lower-right button zone starts at x887)
XL, XR = 280, 700; LEN = XR - XL; TOT = 2 * LEN   # sim units (unchanged so the race is identical)
XLD, XRD = 284, 700; KD = (XRD - XLD) / LEN       # rc18: display mapping for the 4x swimmers
T_GO = float(os.environ.get('TG', '0.6'))
SPEED_T, SPEED_K = 2.0, 1.8; STRONG_T = 2.5; SLEEP_T = 1.0; STUN_T = 0.6
# n14 (Bennett Oct 29: 'a clear shove animation... they have to stop for a second to perform the shove'):
# Cleo's STRENGTH shove = she stops, stands up waist-deep and swings (existing race cleo_atk animation, 13 frames), the swing lands at
# HIT_T and sends the wave that BONKs the lanes next to her; she dives back in at SHOVE_T, then the STRENGTH x1.2 strokes run for STRONG_T
SHOVE_T = float(os.environ.get('SHT', '1.0')); HIT_T = 0.4
def water_layer(t):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([PX0, PY0, PX1, PY1], fill=(38, 128, 206, 255))
    for i in range(NL):
        y0 = LY0 + LH * i
        d.rectangle([PX0, y0 + LH * 0.15, PX1, y0 + LH * 0.85], fill=(46, 142, 218, 255))
    rr = random.Random(11)
    for k in range(160):
        x = (rr.uniform(PX0, PX1) + t * rr.uniform(10, 30)) % (PX1 - PX0 - 30) + PX0; y = rr.uniform(PY0 + 6, PY1 - 10)
        x = int(x / 6) * 6; y = int(y / 6) * 6; w = rr.choice([12, 18, 24])
        d.rectangle([x, y, x + w, y + 5], fill=(120, 200, 245, 200))
    # lane line markers on the pool floor
    for i in range(NL):
        y = int(LANEY[i] / 6) * 6
        d.rectangle([XLD - 20, y - 3, XRD + 20, y + 3], fill=(28, 96, 170, 255))
    return L
FRAME = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for x in range(PX0 - STONE.width, PX1 + STONE.width, STONE.width - 4):
    FRAME.alpha_composite(STONE, (x, PY0 - STONE.height + 6)); FRAME.alpha_composite(STONE, (x, PY1 - 6))
for y in range(PY0 - STONE.height + 6, PY1 + STONE.height, STONE.height - 4):
    FRAME.alpha_composite(STONE, (PX0 - STONE.width + 6, y)); FRAME.alpha_composite(STONE.transpose(Image.FLIP_LEFT_RIGHT), (PX1 - 6, y))
for i in range(0, NL + 1):
    y = LY0 + LH * i
    for k, x in enumerate(range(PX0 + 4, PX1 - 20, BUOY.width + 4)):
        b = BUOY if k % 2 == 0 else BUOY.rotate(90)
        FRAME.alpha_composite(b, (x, int(y - BUOY.height / 2)))
CK = float(os.environ.get('CK', '1.08'))   # n14 seed 1184 (re-searched for the 1s shove stop)
def sim(seed):
    """gummy powers (SPEC 12): each lane's gummy does what its type does.
    Cyrus mushroom SPEED (x1.8 for 2s), Cleo creatine STRONG (blue aura, power strokes x1.2 for 2.5s, and her
    first power stroke sends a wave that BONKs the swimmers in the lanes next to her: shoved back + slowed),
    Rayleigh melatonin SLEEP (every other swimmer stops 1s with Zzz), Joy ACV SHIELD (bubble blocks the next bonk/sleep)."""
    rnd = random.Random(seed)
    S = {n: dict(s=0.0, base=rnd.uniform(118, 134) * float(os.environ.get('SPF', '0.62')), ph=rnd.uniform(0, 6.3), fin=None, boost=None,
                 gs=rnd.uniform(200 * LEN / 680, TOT - 260 * LEN / 680), sleep=-9.0, stun=-9.0, shield=False, shield_t=None, pop=None) for n in NAMES}
    S['cleo']['base'] *= CK      # n14: Cleo's base pace (the slime is pushing her), tuned per seed so the 1s shove stop still ends in a photo finish
    frames = []; first = None; half_lead = None; FX = []; PEND = []
    def hit(m, t, kind):
        o = S[m]
        if o['fin'] is not None: return
        if o['shield']: o['shield'] = False; o['pop'] = t; FX.append((t, 'block', m, kind)); return
        if kind == 'sleep': o['sleep'] = t + SLEEP_T
        else: o['stun'] = t + STUN_T; o['s'] = max(0.0, o['s'] - 18)
        FX.append((t, kind, m))
    for f in range(int(40 * FPS)):
        t = f / FPS; dt = 1 / FPS
        for pe in [p for p in PEND if p[0] <= t + 1e-6]: PEND.remove(pe); hit(pe[1], t, 'bonk')
        if t >= T_GO:
            for n, r in S.items():
                if r['fin'] is not None: continue
                if t < r['sleep']: continue
                sp = r['base'] * (1 + 0.16 * math.sin(0.9 * (t - T_GO) + r['ph']) + 0.07 * math.sin(2.7 * t + 2 * r['ph']))
                if r['boost'] is not None and t - r['boost'] < SPEED_T and GK[n] == 'mush': sp *= SPEED_K
                if r['boost'] is not None and GK[n] == 'cre':
                    if t - r['boost'] < SHOVE_T: continue                      # stopped: performing the shove
                    if t - r['boost'] < SHOVE_T + STRONG_T: sp *= 1.2
                if t < r['stun']: sp *= 0.3
                if r['boost'] is None and r['s'] < r['gs'] <= r['s'] + sp * dt:
                    r['boost'] = t; k = GK[n]; FX.append((t, 'pick', n, k))
                    if k == 'acv': r['shield'] = True; r['shield_t'] = t
                    elif k == 'mel':
                        for m in NAMES:
                            if m != n: hit(m, t, 'sleep')
                        FX.append((t, 'sleepwave', n))
                    elif k == 'cre':
                        i = NAMES.index(n); FX.append((t + HIT_T, 'wave', n))
                        for j in (i - 1, i + 1):
                            if 0 <= j < len(NAMES): PEND.append((t + HIT_T + 0.15, NAMES[j]))
                        continue                                                  # stops on the spot to shove
                r['s'] += sp * dt
                if r['s'] >= TOT: r['s'] = TOT; r['fin'] = t; first = first or (n, t)
            if half_lead is None and max(r['s'] for r in S.values()) >= LEN: half_lead = max(S, key=lambda n: S[n]['s'])
        frames.append({n: dict(s=r['s'], fin=r['fin'], boost=r['boost'], gs=r['gs'], sleep=r['sleep'], stun=r['stun'], shield=r['shield'], pop=r['pop']) for n, r in S.items()})
        if all(r['fin'] is not None for r in S.values()): break
    fins = sorted((r['fin'], n) for n, r in S.items())
    return frames, fins, half_lead, FX
def score(seed):
    fr, fins, hl, fx = sim(seed)
    if not any(e[1] in ('sleep', 'block') for e in fx) or not any(e[1] in ('bonk',) for e in fx): return None
    if not any(e[1] == 'block' for e in fx) or len([e for e in fx if e[1] == 'pick']) < 4: return None
    if fins[0][1] != 'cleo': return None
    pk = sorted(e[0] for e in fx if e[1] == 'pick')
    if min(b - a for a, b in zip(pk, pk[1:])) < 1.3: return None          # one gag at a time
    tc = [e[0] for e in fx if e[1] == 'pick' and e[3] == 'cre'][0]
    if tc == pk[0]: return None
    if any(e[1] == 'sleep' and e[2] == 'cleo' and tc - 0.2 <= e[0] <= tc + SHOVE_T + 0.3 for e in fx): return None
    gap = fins[1][0] - fins[0][0]
    if not (0.03 < gap < 0.2): return None
    if hl == fins[0][1]: return None
    if not (10.0 < fins[0][0] < 15.0): return None
    # lead changes
    lead = None; ch = 0
    for st in fr[int(T_GO * FPS):]:
        l = max(st, key=lambda n: st[n]['s'])
        if l != lead: ch += 1; lead = l
    if ch < 4: return None
    if os.environ.get('WN') and fins[0][1] != os.environ['WN']: return None
    return round(fins[0][0], 2), fins[0][1], fins[1][1], round(gap, 3), ch
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for sd in range(int(sys.argv[2]), int(sys.argv[3])):
        for ck in [1.0 + 0.01 * q for q in range(0, 9)]:
            CK = ck; r = score(sd)
            if r: print(sd, round(ck, 2), r, flush=True); break
    sys.exit()
SEED = int(sys.argv[1]); FR, FINS, HL, FX = sim(SEED); print(FX)
win, T_F = FINS[0][1], FINS[0][0]; second = FINS[1][1]
print('fins', [(n, round(t, 2)) for t, n in FINS], 'half leader', HL)
ICON = {}
for n in NAMES:
    src = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}[n]
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((60, 60), Image.NEAREST)
    b = Image.new('RGBA', (72, 72), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([0, 0, 71, 71], fill=(20, 16, 30, 255)); d.ellipse([3, 3, 68, 68], fill=RING[n] + (255,)); d.ellipse([6, 6, 65, 65], fill=(235, 232, 220, 255))
    m = Image.new('L', (60, 60), 0); ImageDraw.Draw(m).ellipse([0, 0, 59, 59], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', (60, 60), (0, 0, 0, 0)), m).getchannel('A')); ICON[n] = b
def xpos(s):
    if s <= LEN: return XLD + s * KD, 1
    return XRD - (s - LEN) * KD, -1
GHOST = {}
def swimmer(img, n, s, t, moving, fx={}):
    x, d = xpos(s); i = NAMES.index(n); y = LANEY[i]
    fr = SWIM[n][int(t * 10) % len(SWIM[n])] if moving else SWIM[n][0]
    if d < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    bob = 4 * math.sin(t * 6 + i)
    top = int(y - fr.height * 0.62 + bob); left = int(x - fr.width / 2)
    if fx.get('shove') is not None:          # stands up waist-deep and swings (existing cleo_atk frames), facing her swim direction
        u = fx['shove']; k = int(u / HIT_T * 4) if u < HIT_T else min(12, 4 + int((u - HIT_T) / (SHOVE_T - HIT_T) * 9))
        fr = CATK[k]; cxo = CATK_CX
        if d < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT); cxo = fr.width - CATK_CX
        bob = 2 * math.sin(t * 4 + i); top = int(y + 6 + bob - CATK_WAIST); left = int(x - cxo)
    wl = int(y + 6 + bob) - top                     # waterline inside sprite
    a = fr.getchannel('A'); below = a.crop((0, max(0, wl), fr.width, fr.height)).point(lambda p: int(p * 0.35))
    fr2 = fr.copy(); a2 = a.copy(); a2.paste(below, (0, max(0, wl))); fr2.putalpha(a2)
    tint = Image.new('RGBA', fr.size, (40, 130, 210, 0)); ta = a.copy(); ta.paste(0, (0, 0, fr.width, max(0, wl))); ta = ta.point(lambda p: int(p * 0.55)); tint.putalpha(ta)
    fr2.alpha_composite(tint)
    if fx.get('speed'):
        afterimages(img, GHOST.get(n, [])[-4:]); speed_lines(img, x - d * fr.width * 0.3, y + bob + 10, d, t, 160)
        GHOST[n] = (GHOST.get(n, []) + [(fr2, left, top)])[-6:]
    else: GHOST[n] = []
    if fx.get('strong'):
        pu = 0.5 + 0.5 * math.sin(t * 14)
        hw = fr.width * 0.58; layer(img, lambda dd: [dd.ellipse([x - hw - q, top - 6 - q / 2, x + hw + q, y + 34 + q / 2], fill=(90, 160, 255, int(40 + 30 * pu))) for q in (0, 16)])
        tt = tinted(fr, (200, 235, 255), int(200 + 55 * pu))
        for k_ in range(12):
            a_ = k_ * math.pi / 6; img.alpha_composite(tt, (int(left + 9 * math.cos(a_)), int(top + 9 * math.sin(a_))))
        tt = tinted(fr, (60, 130, 255), 255)
        for k_ in range(8):
            a_ = k_ * math.pi / 4; img.alpha_composite(tt, (int(left + 5 * math.cos(a_)), int(top + 5 * math.sin(a_))))
    if fx.get('asleep') is not None: sleepy(img, fr2, left, top); zzz(img, x, top + 10, fx['asleep'])
    else: img.alpha_composite(fr2, (left, top))
    if fx.get('stun'): dizzy(img, x, top + 8, t)
    if fx.get('shield'):
        hw = fr.width * 0.56
        layer(img, lambda dd: (dd.ellipse([x - hw, top - 18, x + hw, y + 40], fill=(110, 230, 90, 55), outline=(150, 255, 120, 230), width=7),
                               dd.arc([x - hw * 0.75, top - 4, x - hw * 0.1, top + 70], 200, 260, fill=(230, 255, 220, 230), width=6)))
    if moving:
        def splash(dd):
            rr = random.Random(int(t * 30) + i * 7)
            for k in range(10):
                sx = x - d * (fr.width * 0.45 + rr.uniform(0, 50)); sy = y + bob + rr.uniform(-14, 10)
                dd.rectangle([sx, sy, sx + 6, sy + 6], fill=(235, 250, 255, 220))
            dd.arc([x - fr.width / 2 - 10, y - 6, x + fr.width / 2 + 10, y + 26], 200, 340, fill=(220, 245, 255, 160), width=4)
        layer(img, splash)
STILLS = [int(x) for x in os.environ.get('STILLS', '').split(',') if x]
W_ = Writer('v37_noaudio.mp4') if not STILLS else None; ev = []
# n14 photo-finish beats (s after the finish frame): zoom in on the wall, CLEO WINS!, slide back along her lane, the slime surfaces + heart
P_ZOOM, P_WIN, P_SLIDE0, P_SLIDE1, P_RISE0, P_RISE1, P_HEART, P_END = 0.35, 0.75, 1.2, 1.8, 1.85, 2.2, 2.15, float(os.environ.get('PEND', '3.5'))
# rc18: after the last power (+0.4s) the race ramps to 1.6x for the final sprint (sim unchanged), so the photo finish lands sooner
A_SPR = max(e[0] for e in FX) + 0.4; R_SPR = float(os.environ.get('RSPR', '1.6'))
# n14: tighten dead time: the quiet stretches between powers (no stamp on screen, no power firing) run at R_Q x (sim unchanged, smooth 0.2s ramps)
R_Q = float(os.environ.get('RQ', '1.7'))
_busy = sorted([(T_GO, T_GO + 0.6)] + [(e[0], e[0] + (1.15 if e[1] in ('pick', 'bonk', 'block') else (SLEEP_T if e[1] == 'sleep' else 0.5))) for e in FX]
               + [(e[0], e[0] + SHOVE_T + 0.2) for e in FX if e[1] == 'pick' and e[3] == 'cre'] + [(e[0], e[0] + SPEED_T) for e in FX if e[1] == 'pick' and e[3] == 'mush'])
QUIET = []; _c = 0.0
for a_, b_ in _busy:
    if a_ - 0.15 - (_c + 0.1) >= 0.6: QUIET.append((_c + 0.1, a_ - 0.15))
    _c = max(_c, b_)
print('quiet windows', [(round(a_, 2), round(b_, 2)) for a_, b_ in QUIET])
def qrate(ts):
    w = 0.0
    for a, b in QUIET:
        if a <= ts <= b: w = max(w, min(1, (ts - a) / 0.2, (b - ts) / 0.2))
    return 1 + (R_Q - 1) * w
TMAP = []; ts = 0.0; tv = 0.0
while ts < T_F - 1e-9:
    TMAP.append(ts); rate = qrate(ts) if ts < A_SPR else 1 + (R_SPR - 1) * min(1, (ts - A_SPR) / 0.5); ts = min(T_F, ts + rate / FPS); tv += 1 / FPS
def s2v(t0):   # sim time -> video time (for the sfx events)
    import bisect
    return bisect.bisect_left(TMAP, t0) / FPS
NRACE = len(TMAP); T_FV = NRACE / FPS
END = T_FV + P_END
print('sprint from', round(A_SPR, 2), 'finish video', round(T_FV, 2), 'sim', round(T_F, 2), 'end', round(END, 2))
seen_boost = set(); seen_turn = set(); seen_fin = set()
# rc18: power stamps 34-40px -> 56px on a dark plate with an outline, each inside its own lane (top of the lane, biased to the
# swimmer's trailing side so the head stays visible); one stamp per lane at a time, so stamps never overlap
STAMPS = []
def add_stamp(t0, n, text, col):
    i = NAMES.index(n); st0 = FR[min(int(round(t0 * FPS)), len(FR) - 1)][n]; x, d = xpos(st0['s']); sw = SWIM[n][0].width
    tw = len(text) * 56 + 40; cx = x - d * 0.3 * sw; cx = max(SX0 + tw / 2 + 8, min(SX1 - tw / 2 - 8, cx))
    cy = LY0 + LH * i + 40 if text != POWER['cre'][0] else LY0 + LH * (i + 1) - 44
    STAMPS.append([t0, i, text, col, cx, cy, t0 + 1.15])
for e in FX:
    if e[1] == 'pick':
        add_stamp(e[0], e[2], POWER[e[3]][0], POWER[e[3]][1]); ev.append((round(s2v(e[0]), 3), SFX[e[3]]))
        if e[3] == 'cre': ev.append((round(s2v(e[0] + HIT_T - 0.12), 3), 'sword_swish'))   # n14: her shove swing
    elif e[1] == 'bonk':
        add_stamp(e[0], e[2], 'BONK!', (255, 255, 255)); ev.append((round(s2v(e[0]), 3), 'punch'))
    elif e[1] == 'block':
        add_stamp(e[0], e[2], 'BLOCKED!', (150, 255, 120)); ev.append((round(s2v(e[0]), 3), 'boing'))
STAMPS.sort()
for a in STAMPS:
    for b in STAMPS:
        if b[1] == a[1] and b[0] > a[0]: a[6] = min(a[6], b[0]); break
print('stamps', [(round(a[0], 2), NAMES[a[1]], a[2]) for a in STAMPS])
def draw_stamps(img, t_sim):
    for t0, i, text, col, cx, cy, t1 in STAMPS:
        if not t0 <= t_sim < t1: continue
        u = t_sim - t0; a = int(255 * min(1, (t1 - t_sim) / 0.18)); sc = 1 + 0.3 * max(0, 1 - u / 0.12); fs = int(56 * sc)
        def fn(dd, text=text, col=col, cx=cx, cy=cy, a=a, fs=fs):
            f_ = FF(fs); tw = dd.textlength(text, font=f_)
            dd.rounded_rectangle([cx - tw / 2 - 18, cy - fs / 2 - 12, cx + tw / 2 + 18, cy + fs / 2 + 12], 12, fill=(14, 10, 24, int(215 * a / 255)), outline=col + (a,), width=5)
            dd.text((cx - tw / 2, cy - fs / 2), text, font=f_, fill=col + (a,), stroke_width=6, stroke_fill=(10, 6, 18, a))
        layer(img, fn)
CI = NAMES.index('cleo')
T_TURN = next((k / FPS for k, st_ in enumerate(FR) if st_['cleo']['s'] >= LEN), 99)
def draw_slime(img, st, t_sim, t_anim):
    """the slime rides right behind Cleo's feet, under the water (same waterline split + tint as the swimmers' submerged half).
    At her turn it slides under her to the new trailing side over 0.4s (no teleport)."""
    s_ = st['cleo']['s']; x, d = xpos(s_); y = LANEY[CI]; bob = 4 * math.sin(t_anim * 6 + CI)
    sw = SWIM['cleo'][0].width
    u = (t_sim - T_TURN) / 0.4; side = 1.0 if u <= 0 else (-1.0 if u >= 1 else 1 - 2 * (0.5 - 0.5 * math.cos(math.pi * u)))
    ta = REV['ta'] if REV['ta'] is not None else t_anim
    fr = SLIME[int(ta * 9) % len(SLIME)]
    if side < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    cx = x - side * (sw * 0.5 - 35 + 24 * REV['rise'])          # its front tucked right under her kicking feet; pops up just behind them on the reveal
    wl = int(y + 6 + bob)
    top = int(wl + 1 - REV['rise'] * fr.height * 0.8); left = int(cx - fr.width / 2)
    cut = wl - top
    a = fr.getchannel('A'); fr2 = fr.copy(); a2 = a.point(lambda p: int(p * SL_ALPHA))
    if cut > 0: a2.paste(a.crop((0, 0, fr.width, min(cut, fr.height))), (0, 0))
    fr2.putalpha(a2)
    tint = Image.new('RGBA', fr.size, (40, 130, 210, 0)); ta_ = a.copy()
    if cut > 0: ta_.paste(0, (0, 0, fr.width, min(cut, fr.height)))
    tint.putalpha(ta_.point(lambda p: int(p * 0.5 * SL_ALPHA))); fr2.alpha_composite(tint)
    img.alpha_composite(fr2, (left, top))
    if REV['rise'] > 0:
        layer(img, lambda dd: dd.arc([left - 14, wl - 10, left + fr.width + 14, wl + 22], 200, 340, fill=(220, 245, 255, int(200 * REV['rise'])), width=4))
    SLBOX[0] = (left, top, left + fr.width, top + fr.height)
OPEN = []
def scene(t_sim, t_anim):
    img = BGF[int(t_anim * 6) % len(BGF)].copy()
    img.alpha_composite(water_layer(t_anim)); img.alpha_composite(FRAME)
    st = FR[min(int(t_sim * FPS), len(FR) - 1)]
    # gummies
    for n in NAMES:
        r = st[n]
        if r['boost'] is None:
            gx, _ = xpos(r['gs']); gy = LANEY[NAMES.index(n)]; bob = int(5 * math.sin(t_anim * 4 + gx))
            g = up(gummy_src(GK[n]), 4)
            layer(img, lambda d, gx=gx, gy=gy: d.ellipse([gx - 44, gy - 24, gx + 44, gy + 24], fill=(255, 255, 255, 60)))
            img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2 - 14 + bob)))
    # wave / sleep rings under the swimmers
    for e in FX:
        u = t_sim - e[0]
        if e[1] == 'wave' and 0 <= u < 0.45:
            x, _ = xpos(FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]['s']); y = LANEY[NAMES.index(e[2])]; q = u / 0.45
            layer(img, lambda dd, x=x, y=y, q=q: [dd.ellipse([x - 60 - 90 * q, y - 30 - LH * 1.1 * q, x + 60 + 90 * q, y + 30 + LH * 1.1 * q], outline=(150, 200, 255, int(240 * (1 - q))), width=12 - 4 * k_) for k_ in range(2)])
        if e[1] == 'sleepwave' and 0 <= u < 0.7:
            x, _ = xpos(FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]['s']); y = LANEY[NAMES.index(e[2])]
            sleep_wave(img, x, y, u / 0.7, 1100)
    draw_slime(img, st, t_sim, t_anim)
    for n in NAMES:
        r = st[n]; moving = r['fin'] is None and t_sim >= r['sleep']
        b = r['boost']; k = GK[n]
        shv = (t_sim - b) if (b is not None and k == 'cre' and 0 <= t_sim - b < SHOVE_T and r['fin'] is None) else None
        if shv is not None: moving = False
        fx = dict(shove=shv, speed=b is not None and k == 'mush' and 0 <= t_sim - b < SPEED_T, strong=b is not None and k == 'cre' and 0 <= t_sim - b < SHOVE_T + STRONG_T,
                  asleep=(t_sim - (r['sleep'] - SLEEP_T)) if t_sim < r['sleep'] else None, stun=t_sim < r['stun'] and r['fin'] is None, shield=r['shield'])
        swimmer(img, n, r['s'], t_anim, moving, fx)
        if b is not None and k == 'cre':
            for t0_ in (b, b + SHOVE_T):
                if 0 <= t_sim - t0_ < 0.3:
                    x_, _ = xpos(r['s']); burst(img, x_, LANEY[NAMES.index(n)] + 6, (t_sim - t0_) / 0.3, (225, 245, 255), n=12, r0=30, r1=110)
        if r['pop'] is not None and 0 <= t_sim - r['pop'] < 0.5:
            x, _ = xpos(r['s']); shield_pop(img, x, LANEY[NAMES.index(n)] + 36, 170, (t_sim - r['pop']) / 0.5, SWIM[n][0].width * 0.56)
    for e in FX:
        if e[1] == 'bonk' and 0 <= t_sim - e[0] < 0.3:
            x, _ = xpos(st[e[2]]['s']); bonk_burst(img, x, LANEY[NAMES.index(e[2])] - 20, (t_sim - e[0]) / 0.3)
    if any(e[1] == 'sleepwave' and 0 <= t_sim - e[0] < 0.25 for e in FX): img.alpha_composite(Image.new('RGBA', (W, H), (120, 60, 220, 50)))
    draw_stamps(img, t_sim)
    if False:   # Oct 29: 'ACV GUMMY' explainer tag cut (the SHIELD! stamp names the power when it fires)
        aa = int(255 * min(1, (1.8 - t_anim) / 0.25)); gx, _ = xpos(st['joy']['gs']); gy = LANEY[0]
        def acvtag(dd, jx=gx, gtop=gy - 70, aa=aa):
            tg = 'ACV GUMMY'; f_ = FF(44); tw = dd.textlength(tg, font=f_); y0 = gtop - 100
            x0 = max(PX0 + 6, min(PX1 - 6 - tw - 36, jx - tw / 2 - 18)); ring = (90, 200, 80)
            dd.polygon([(jx - 16, y0 + 70), (jx + 16, y0 + 70), (jx, gtop - 4)], fill=ring + (aa,))
            dd.rounded_rectangle([x0, y0, x0 + tw + 36, y0 + 72], 14, fill=(14, 10, 24, int(235 * aa / 255)), outline=ring + (aa,), width=5)
            dd.text((x0 + 18, y0 + 14), tg, font=f_, fill=(255, 255, 255, aa), stroke_width=5, stroke_fill=(10, 6, 18, aa))
        layer(img, acvtag)
    for i, n in enumerate(NAMES):
        if t_sim < T_F: img.alpha_composite(ICON[n], (74, int(LANEY[i] - LH / 2 + 2)))
    return img, st
def heart(d, cx, cy, s, col=(255, 90, 140)):   # pixel heart emote (same as fork_n7/render_race4.py)
    for (x, y) in [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (0, 2), (-2, -1)]:
        d.rectangle([cx + x * s - s // 2, cy + y * s - s // 2, cx + x * s + s // 2 - 1, cy + y * s + s // 2 - 1], fill=col)
def ease(q): q = max(0.0, min(1.0, q)); return 0.5 - 0.5 * math.cos(math.pi * q)
for f in range(int(round(END * FPS))):
    t = f / FPS
    frozen = f >= NRACE
    t_sim = TMAP[f] if not frozen else T_F
    u = t - T_FV
    if frozen:
        REV['rise'] = ease((u - P_RISE0) / (P_RISE1 - P_RISE0)); REV['ta'] = T_F + max(0.0, u - P_SLIDE1)   # the slime comes alive once the camera lands on it
    img, st = scene(t_sim, t_sim)
    for n in NAMES:
        r = st[n]
        if r['s'] >= LEN and n not in seen_turn: seen_turn.add(n); ev.append((round(t, 3), 'swish'))
    if frozen:
        # photo finish: zoom on the finish wall around the two leaders, then the camera slides back along Cleo's lane to her feet
        ys = [LANEY[NAMES.index(win)], LANEY[NAMES.index(second)]]; cyA = (ys[0] + ys[1]) / 2
        BX0, BY0, BX1, BY1 = 0, int(LY0 - 40), W, 1500; bw, bh = BX1 - BX0, BY1 - BY0
        sl = SLBOX[0]; scx, scy = (sl[0] + sl[2]) / 2, (sl[1] + sl[3]) / 2
        ZB = float(os.environ.get('ZB', '3.0'))
        k = ease((u - P_SLIDE0) / (P_SLIDE1 - P_SLIDE0))
        z = (1 + 0.9 * min(1, u / P_ZOOM)) * (1 - k) + ZB * k
        cw, ch = bw / z, bh / z
        xA = 0.0; xB = scx - 610 / ZB                     # slime lands right of centre, Cleo's legs on the left
        cy = cyA * (1 - k) + (LANEY[CI] - 55) * k     # slime sits low in the shot so the heart clears CLEO WINS!
        x0 = max(0, min(W - cw, xA * (1 - k) + xB * k)); y0 = max(BY0, min(BY1 - ch, cy - ch / 2))
        zoom = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((bw, bh), Image.NEAREST)
        img.paste(zoom, (BX0, BY0))
        if u < 0.12: layer(img, lambda d: d.rectangle([BX0, BY0, BX1, BY1], fill=(255, 255, 255, int(200 * (1 - u / 0.12)))))
        layer(img, lambda d: d.rectangle([BX0, BY0, BX1, BY1], outline=(255, 255, 255, 255), width=8))
        if u < P_WIN:
            text_layer(img, [(490, HB + 105, 'PHOTO FINISH!', 60, (255, 255, 255), 9, 255)])
        else:
            q = u - P_WIN; sc = 1 + 0.3 * max(0, 1 - q / 0.12)
            text_layer(img, [(490, HB + 105, LABEL[win] + ' WINS!', int(64 * sc), (255, 214, 60), 9, 255)])
        if u >= P_HEART:   # heart emote over the slime
            q = u - P_HEART; hx = BX0 + (scx - x0) * z; htop = BY0 + (sl[1] - y0) * z
            hy = htop - 60 - 40 * ease(q / 0.3); pop = 1 + 0.4 * max(0, 1 - q / 0.15)
            def hfn(d, hx=hx, hy=hy, s_=int(18 * pop)):
                heart(d, int(hx), int(hy), s_ + 5, (12, 8, 20)); heart(d, int(hx), int(hy), s_)
            layer(img, hfn)
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_FV, 3), 'ding_8bit'))
        if u >= P_WIN and not any(e[1] == 'victory' for e in ev): ev.append((round(t, 3), 'victory'))
        if u >= P_SLIDE0 and not any(e[1] == 'whoosh_8bit' for e in ev): ev.append((round(t, 3), 'whoosh_8bit'))
        if u >= P_RISE0 and not any(e[1] == 'jump' for e in ev): ev.append((round(t, 3), 'jump'))
        if u >= P_HEART and not any(e[1] == 'chime' for e in ev): ev.append((round(t, 3), 'chime'))
    if T_GO <= t < T_GO + 0.6:
        text_layer(img, [(490, 960, 'GO!', 130, (255, 214, 60), 10, 255)])
        if not any(e[1] == 'go_8bit' for e in ev): ev.append((round(T_GO, 3), 'go_8bit'))
    img.alpha_composite(HOOK)
    if STILLS:
        if f in STILLS: img.convert('RGB').save(f'st_{f:04d}.png')
        if f >= max(STILLS): sys.exit()
        continue
    W_.write(img)
    if f < 9: OPEN.append(img.copy())
    if os.environ.get('PV') and f in [int(x) for x in os.environ['PV'].split(',')]: img.convert('RGB').save(f'pv_{f:04d}.png')
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/c_{f:04d}.png')
for im_ in OPEN: W_.write(im_)          # loop: cut back to the opening
W_.close()
json.dump(ev, open('v37_ev.json', 'w')); print('done', END)
