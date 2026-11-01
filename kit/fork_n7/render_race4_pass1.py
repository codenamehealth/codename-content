import numpy as np, glob, math, random, subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
OUTD = os.path.dirname(os.path.abspath(__file__)); os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/race')
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'
A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
S = 4      # race_v3: guides 3x -> 4x (rule: guides at least 4x)
def F(s): return ImageFont.truetype(FONT, s)
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
def load(d, scale=S, clean=False):
    fr = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(d + '/*.png'))]
    if clean: fr = [nored(f) for f in fr]
    return [f.resize((f.width * scale, f.height * scale), Image.NEAREST) for f in fr]
def gifload(p, scale=S):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames):
        im.seek(i); f = im.convert('RGBA').resize((92, 92), Image.NEAREST); fr.append(f.resize((92 * scale, 92 * scale), Image.NEAREST))
    return fr
G = ['cyrus', 'cleo', 'joy', 'ray']
NAMES = {'cyrus': 'CYRUS', 'cleo': 'CLEO', 'joy': 'JOY', 'ray': 'RAYLEIGH'}
COL = {'cyrus': (255, 176, 40), 'cleo': (120, 170, 255), 'joy': (120, 220, 90), 'ray': (200, 110, 255)}
RUN = {g: load(f'{g}_run')[1:] for g in G}
ATK = {g: load(f'{g}_atk') for g in G}
HIT = {'joy': (4, 100), 'ray': (5, 102), 'cleo': (4, 66), 'cyrus': (3, 84)}
SFX = {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'swish', 'cyrus': 'punch'}
SL_IDLE = load('slime_idle_c', clean=True); SL_SPLAT = load('slime_splat_c', clean=True)
IDLE = {'cyrus': gifload('idle_8.gif'), 'ray': gifload('idle_6.gif')}
VIC = {'cyrus': gifload('vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif'), 'ray': gifload('vic_victoryPose_1.gif')}
# race_v3 (Bennett): the referee is a SLIME referee (PixelLab edit of the race slime: striped referee shirt + whistle), not the Hollow
RS = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1/race/refslime/'
REF_I = load(RS + 'edit7'); REF_W = load(RS + 'blow22')
CROWN = Image.open('../ref/crown_cands/01.png').convert('RGBA'); CROWN = CROWN.crop(CROWN.getbbox()); CROWN = CROWN.resize((CROWN.width * S, CROWN.height * S), Image.NEAREST)
# ---------------- layout
TRACK_TOP, LANE_H, NL = 540, 240, 4   # race_v4: +20 for the 2-line hook strip
GY0 = TRACK_TOP - 96
def blend(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
TRACK_BOT = TRACK_TOP + LANE_H * NL
FEET = [TRACK_TOP + LANE_H * i + LANE_H - 30 for i in range(NL)]
START_X = 300; FINISH_X = 6200
T = {i: Image.open(f'tiles/tile_{i}.png').convert('RGBA').resize((96, 96), Image.NEAREST) for i in range(16)}
GW = 8000
ground = Image.new('RGBA', (GW, H - GY0), (0, 0, 0, 0))
for y in range(GY0, H, 96):
    for x in range(0, GW, 96):
        if y < TRACK_TOP - 96: idx = 0
        elif y < TRACK_TOP: idx = 3
        elif y < TRACK_BOT: idx = 15
        elif y < TRACK_BOT + 96: idx = 12
        else: idx = 0
        tile = T[idx]
        if idx in (0, 15):
            if (x // 96) % 2: tile = tile.transpose(Image.FLIP_LEFT_RIGHT)
            if (y // 96) % 2: tile = tile.transpose(Image.FLIP_TOP_BOTTOM)
        elif (x // 96) % 2: tile = tile.transpose(Image.FLIP_LEFT_RIGHT)
        ground.alpha_composite(tile, (x, y - GY0))
gd = ImageDraw.Draw(ground)
for i in range(1, NL):
    y = TRACK_TOP + LANE_H * i - GY0
    for x in range(0, GW, 48): gd.rectangle([x, y - 3, x + 28, y + 3], fill=(238, 230, 205, 230))
gd.rectangle([START_X - 6, TRACK_TOP - GY0, START_X + 6, TRACK_BOT - GY0], fill=(245, 245, 240, 255))
for j, y in enumerate(range(TRACK_TOP - GY0, TRACK_BOT - GY0, 20)):
    for k in range(3):
        c = (20, 20, 24, 255) if (j + k) % 2 == 0 else (245, 245, 245, 255)
        gd.rectangle([FINISH_X + k * 20 - 30, y, FINISH_X + k * 20 - 11, y + 19], fill=c)
g = Image.open(A + 'hub.gif'); HUBF = []
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').resize((1067, 600), Image.NEAREST)
    strip = Image.new('RGB', (1067 * 2, 600)); strip.paste(f, (0, 0)); strip.paste(f.transpose(Image.FLIP_LEFT_RIGHT), (1067, 0))
    HUBF.append(strip)
FIN = Image.open('finish_cands/00.png').convert('RGBA'); FIN = FIN.crop(FIN.getbbox()); FIN = FIN.resize((FIN.width * 3, FIN.height * 3), Image.NEAREST)
# ---------------- simulation
T_GO = 2.8; DUR = 24.0
OUT_G = ['cleo', 'joy']; T_WARN = 9.2; T_LAND = 10.3
ATK_FPS = 18; ATK_LEN = 12 / ATK_FPS
SNEAK = 0.8
def simulate(seed):
    rnd = random.Random(seed); st = {}
    for li, gname in enumerate(G):
        sl = sorted(rnd.uniform(1200, FINISH_X - 700) for _ in range(3))
        while min(b - a for a, b in zip(sl, sl[1:])) < 950: sl = sorted(rnd.uniform(1200, FINISH_X - 700) for _ in range(3))
        st[gname] = dict(lane=li, x=float(START_X - 150), slimes=[dict(x=s, hp=rnd.choice([1, 1, 1, 2]), dead_t=None) for s in sl],
                         v=rnd.uniform(440, 490), ph=rnd.uniform(0, 6.28), state='run', t0=0, target=None, fin=None, events=[], sneak=None)
    return st
def run_sim(seed):
    st = simulate(seed); timeline = []; dt = 1 / FPS
    for f in range(int(DUR * FPS)):
        t = f / FPS
        for gname, s in st.items():
            if t < T_GO or s['state'] == 'out': continue
            if t >= T_LAND and gname in OUT_G:
                s['state'] = 'out'; s['out_x'] = s['x']; s['t0'] = T_LAND; continue
            if s['fin'] is not None and t > s['fin'] + 0.45:
                s['state'] = 'stop'; continue
            if s['state'] == 'run':
                v = s['v'] * (1 + 0.10 * math.sin(1.3 * t + s['ph']) + 0.05 * math.sin(3.1 * t + 2 * s['ph']))
                nx = s['x'] + v * dt
                live = [sl for sl in s['slimes'] if sl['dead_t'] is None and not sl.get('skipped')]
                hf, hx = HIT[gname]; reach = (hx + 14) * S
                if live and nx + reach >= live[0]['x']:
                    if gname == 'cyrus' and live[0] is s['slimes'][-1]:
                        # race_v4: the bribed slime has already hopped out of his lane; Cyrus just keeps running (no dodge, no hop)
                        live[0]['skipped'] = True; s['sneak'] = t; s['x'] = nx
                    else:
                        s['x'] = live[0]['x'] - reach; s['state'] = 'atk'; s['t0'] = t; s['target'] = live[0]; s['events'].append(('atk', t))
                else:
                    s['x'] = nx
            elif s['state'] == 'sneak':
                u = min(1, (t - s['t0']) / SNEAK); s['x'] = s['sx0'] + (s['sx1'] - s['sx0']) * u
                if u >= 1: s['state'] = 'run'
            elif s['state'] == 'atk':
                u = t - s['t0']; hf, hx = HIT[gname]
                if u >= hf / ATK_FPS and not s.get('hitdone'):
                    s['hitdone'] = True; s['target']['hp'] -= 1
                    if s['target']['hp'] <= 0: s['target']['dead_t'] = t; s['events'].append(('kill', t))
                    else: s['events'].append(('bonk', t))
                if u >= ATK_LEN:
                    s['hitdone'] = False; s['state'] = 'run' if s['target']['dead_t'] is not None else 'atk'; s['t0'] = t
            if s['fin'] is None and s['x'] + 46 * S >= FINISH_X: s['fin'] = t
        timeline.append({k: (v['x'], v['state'], v['t0']) for k, v in st.items()})
    return st, timeline
def score(seed):
    st, tl = run_sim(seed); li = int(T_LAND * FPS)
    if abs(tl[li]['cleo'][0] - tl[li]['joy'][0]) > 220: return None
    if st['cyrus']['sneak'] is None or st['cyrus']['fin'] is None or st['ray']['fin'] is None: return None
    if not (st['cyrus']['fin'] < st['ray']['fin'] < st['cyrus']['fin'] + 0.6): return None
    if not (16.5 < st['cyrus']['fin'] < 19): return None
    # cheat must matter: without the ~0.7s skip Ray would have won
    if st['ray']['fin'] - st['cyrus']['fin'] > 0.45: return None
    leaders = []
    for i in range(int(T_GO * FPS), int(st['cyrus']['fin'] * FPS), 15):
        L = max([k for k in tl[i] if k not in OUT_G or i < li], key=lambda k: tl[i][k][0])
        if not leaders or leaders[-1] != L: leaders.append(L)
    return round(st['ray']['fin'] - st['cyrus']['fin'], 2), len(leaders), leaders, round(st['cyrus']['sneak'], 2)
#### ---- v2 render follows
SEED = 1896   # race_v4: re-searched with the no-dodge rule (Cyrus runs straight past the bribed slime); 11 lead changes, Cyrus edges Rayleigh by 0.1s only because his slime moved.  was 157 # race_v3: re-searched for the 4x sprites (all four guides lead at some point, Cyrus edges Rayleigh by 0.1s only because he skipped)
st, TL = run_sim(SEED)
T_WIN = st['cyrus']['fin']; T_RAY = st['ray']['fin']; T_CH = st['cyrus']['sneak']
print('src: cyrus', round(T_WIN, 2), 'ray', round(T_RAY, 2), 'cheat at', round(T_CH, 2))
KIDLE = load('../king/king2_idle'); KLAND = load('../king/king2_land')
KO = {g: load(f'../king/{g}_ko') for g in OUT_G}
DUST = Image.open('../king/dust_cands/00.png').convert('RGBA'); DUST = DUST.crop(DUST.getbbox())
li0 = int(T_LAND * FPS)
KX = (TL[li0]['cleo'][0] + TL[li0]['joy'][0]) / 2 + 46 * S
K_BOT = FEET[2] + 18
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
# ---------------- time remap: output time -> source (simulation) time
# (out0, out1, src0, src1); piecewise linear, continuous
_A = 6.6 + (T_CH - 0.8 - 11.2) / 2.6; _B = _A + 1.6; _C = _B + (T_RAY + 0.25 - (T_CH + 0.8)) / 1.4
SEG = [(0.0, 1.0, 1.8, 2.8),            # 3-2-1-GO in 1s over the bouncing racers (was 2s)
       (1.0, 4.6, 2.8, T_WARN),         # first jog, ~1.8x
       (4.6, 5.7, T_WARN, T_LAND),      # KING SLIME warning + drop (real time)
       (5.7, 6.6, T_LAND, 11.2),        # Cleo/Joy knocked out (real time)
       (6.6, _A, 11.2, T_CH - 0.8),     # second jog, 2.6x (the dead stretch the review flagged)
       (_A, _B, T_CH - 0.8, T_CH + 0.8),  # race_v4: the bribed slime hops out of Cyrus's lane (real time)
       (_B, _C, T_CH + 0.8, T_RAY + 0.25),  # photo finish (1.4x)
       (_C, _C + 0.7, T_RAY + 0.25, T_RAY + 1.65)]   # post-finish settle
_END_SRC = T_RAY + 1.65; _END_O = _C + 0.7
def src_t(t):
    if t < 0: return 1.8 + t          # loop tail: start line just before frame 0
    for o0, o1, s0, s1 in SEG:
        if t < o1: return s0 + (t - o0) * (s1 - s0) / (o1 - o0)
    return min(23.8, _END_SRC + (t - _END_O))
def out_t(ts):
    for o0, o1, s0, s1 in SEG:
        if ts < s1: return o0 + (ts - s0) * (o1 - o0) / (s1 - s0)
    return _END_O + (ts - _END_SRC)
def speed(t):
    for o0, o1, s0, s1 in SEG:
        if 0 <= t < o1: return (s1 - s0) / (o1 - o0)
    return 1.0
T_FIN_O = out_t(T_WIN); T_RAY_O = out_t(T_RAY)
T_CH_O = out_t(T_CH); T_CH_END_O = out_t(T_CH + SNEAK)
T_KWARN_O = out_t(T_WARN); T_KLAND_O = out_t(T_LAND)
T_REF_O = T_FIN_O + 1.0   # slime referee hops in (CYRUS WINS banner held until here)
T_DQ_O = T_REF_O + 0.6     # FOUL! on Cyrus
T_TOSS_O = T_DQ_O + 0.6    # crown toss
T_RWIN_O = T_TOSS_O + 0.8  # RAYLEIGH WINS
T_RWD_O = T_RWIN_O + 0.7   # race_v4 twist: rewind starts
D_RWD, D_FB1, D_FB2, D_NOW = 0.5, 1.9, 1.3, 1.3
T_FB1_O = T_RWD_O + D_RWD  # flashback 1: before the race, Rayleigh hands that slime a gummy
T_FB2_O = T_FB1_O + D_FB1  # flashback 2: replay of the slime hopping out of Cyrus's way
T_NOW_O = T_FB2_O + D_FB2  # back to the present: Rayleigh with the crown
T_LOOP_O = T_NOW_O + D_NOW
FBF = int(round((T_NOW_O - T_RWD_O) * FPS))   # frames spent in the rewind + flashback (present resumes the post-race scene)
LOOP_TAIL = 0.3
END_O = T_LOOP_O + LOOP_TAIL
print('out: go', out_t(T_GO), 'kwarn', round(T_KWARN_O, 2), 'kland', round(T_KLAND_O, 2), 'chip', round(T_CH_O, 2), 'fin', round(T_FIN_O, 2), 'ray', round(T_RAY_O, 2))
# ---------------- interpolated source state + camera
NSRC = len(TL)
RX_EXT = max([max(f.getbbox()[2] for f in RUN[g]) for g in G] + [max(f.getbbox()[2] for f in ATK[g]) - 14 * S for g in G])
st0 = st; print('RX_EXT', RX_EXT)
CAMS = []; cam = 0.0; hold_cam = 0.0
for f in range(NSRC):
    t = f / FPS; snap = TL[f]
    lead_x = max(v[0] for k, v in snap.items() if not (k in OUT_G and t >= T_LAND))
    target_cam = max(0, min(FINISH_X + 620 - W, lead_x - 520))
    if T_LAND - 0.3 <= t < T_LAND + 0.9: target_cam = hold_cam      # keep King Slime + KO in frame (safe zone)
    else: hold_cam = target_cam
    cam += (target_cam - cam) * 0.12
    # race_v3: never let a racer's sprite run into the unsafe right edge (x>1025; x>887 for the two bottom lanes)
    need = max((v[0] + RX_EXT - (887 if st0[k]['lane'] >= 2 else 1020)) for k, v in snap.items() if not (k in OUT_G and t >= T_LAND))
    cam = max(cam, min(need, FINISH_X + 620 - W)); CAMS.append(cam)
def snap_at(ts):
    fs = ts * FPS; f0 = int(math.floor(fs)); f0 = max(0, min(NSRC - 2, f0)); a = min(1, max(0, fs - f0))
    s0, s1 = TL[f0], TL[f0 + 1]
    out = {}
    for k in s0:
        x0, stt, t0 = s0[k]; x1 = s1[k][0]
        out[k] = (x0 + (x1 - x0) * a if s1[k][1] == stt else x0, stt, t0)
    return out, CAMS[f0] + (CAMS[f0 + 1] - CAMS[f0]) * a
# run-cycle phase: legs speed up with the time ramp but capped (no skating, no frame skipping)
NOUT = int(round(END_O * FPS))
PH = {}; ph = 0.0
for i in range(-int(LOOP_TAIL * FPS) - 2, NOUT + 2):
    t = i / FPS; PH[i] = ph; ph += 14 * min(2.0, speed(t)) / FPS
POS = {}
BRIBE_POS = [None]; HIDE_BRIBE = [False]
HOP_D = 0.32
def bribe_off(ts):
    """(y offset, squash) of the bribed slime: hop down a lane at T_CH-0.6 (Cyrus still ~2 body lengths back), hop back at T_CH+0.45"""
    a0 = T_CH - 0.6; b0 = T_CH + 0.45
    def hop(u, y0, y1):
        return y0 + (y1 - y0) * u - 120 * math.sin(math.pi * u)
    if ts < a0 - 0.12: return 0, 1.0
    if ts < a0: return 0, 1.0 + 0.18 * (ts - (a0 - 0.12)) / 0.12          # crouch
    if ts < a0 + HOP_D: return hop((ts - a0) / HOP_D, 0, LANE_H), 0.9
    if ts < b0: q = ts - a0 - HOP_D; return LANE_H, 1.0 + (0.16 * math.sin(q * 18) * max(0, 1 - q / 0.3))   # landing squash
    if ts < b0 + HOP_D: return hop((ts - b0) / HOP_D, LANE_H, 0), 0.9
    q = ts - b0 - HOP_D; return 0, 1.0 + (0.16 * math.sin(q * 18) * max(0, 1 - q / 0.3))
def world(fo, skip=(), ts_over=None, cam_over=None):
    ta = fo / FPS; ts = src_t(ta) if ts_over is None else ts_over; snap, cam = snap_at(ts)
    if cam_over is not None: cam = cam_over
    BRIBE_POS[0] = None
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    hb = HUBF[int((ta + 5) * 6) % len(HUBF)]; px = int(cam * 0.35) % 1067
    img.paste(hb.crop((px, 0, px + W, 600)), (0, 0))
    img.alpha_composite(ground.crop((int(cam), 0, int(cam) + W, H - GY0)), (0, GY0))
    fx = FINISH_X - int(cam) - FIN.width // 2
    if -FIN.width < fx < W: img.alpha_composite(FIN, (fx, TRACK_TOP - FIN.height + 60))
    kx = int(KX - cam)
    if T_WARN <= ts < T_LAND + 0.05:
        u = (ts - T_WARN) / (T_LAND - T_WARN); sw = int(60 + 300 * u)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([kx - sw // 2, K_BOT - sw // 7, kx + sw // 2, K_BOT + sw // 7], fill=(0, 0, 0, int(70 + 80 * u)))
        img.alpha_composite(sh)
    flyers = []
    for gname in G:
        s = st[gname]; li = s['lane']; x, state, t0 = snap[gname]; feet = FEET[li]
        for sl in s['slimes']:
            sx = int(sl['x'] - cam) - 32 * S
            if sx < -200 or sx > W + 200: continue
            if sl['dead_t'] is None or ts < sl['dead_t']:
                fr = SL_IDLE[int((ta + 5) * 10 + sl['x']) % len(SL_IDLE)]
                if sl.get('skipped') and HIDE_BRIBE[0]: continue
                if sl.get('skipped'):   # race_v4: the bribed slime hops down into Cleo's empty lane before Cyrus reaches it, then hops back
                    dy, sq = bribe_off(ts)
                    fr2 = fr.resize((int(fr.width * sq), int(fr.height / sq)), Image.NEAREST) if abs(sq - 1) > 0.01 else fr
                    bx, by = sx - (fr2.width - fr.width) // 2, feet - 62 * S + (fr.height - fr2.height) + int(dy)
                    img.alpha_composite(fr2, (bx, by)); BRIBE_POS[0] = (sx + 32 * S, feet - 62 * S + int(dy) + 36 * S)
                else:
                    img.alpha_composite(fr, (sx, feet - 62 * S))
            else:
                k = int((ts - sl['dead_t']) * 16)
                if k < len(SL_SPLAT): img.alpha_composite(SL_SPLAT[k], (sx, feet - 62 * S))
        rx = int(x - cam)
        POS[(fo, gname)] = (rx + 46 * S, feet - 40 * S, rx)
        if gname in skip: continue
        if state == 'out':
            u = ts - T_LAND; ox = s['out_x'] - cam - 18 * S - 320 * u; oy = feet - 78 * S - 18 * S - (1900 * u - 450 * u * u)
            fr = KO[gname][3 + int(u * 18) % 6]
            if oy > -400: flyers.append((fr, (int(ox), int(oy))))
            continue
        if ts < T_GO: img.alpha_composite(RUN[gname][0], (rx, feet - 78 * S - int(abs(math.sin((ta + 5) * 9 + li * 0.8)) * 22)))   # bouncing in place, ready
        elif state == 'atk':
            k = min(11, int((ts - t0) * ATK_FPS)); img.alpha_composite(ATK[gname][k], (rx - 14 * S, feet - 78 * S - 26 * S))
        elif state == 'sneak':
            u = min(1, (ts - t0) / SNEAK); dy = int(-150 * math.sin(math.pi * u))
            fr = RUN[gname][int(PH[fo]) % len(RUN[gname])]; img.alpha_composite(fr, (rx, feet - 78 * S + dy))
            POS[(fo, gname)] = (rx + 46 * S, feet - 40 * S + dy, rx)
        elif state == 'stop' and gname in IDLE:
            img.alpha_composite(IDLE[gname][int(ta * 8) % len(IDLE[gname])], (rx, feet - 78 * S))
        else:
            img.alpha_composite(RUN[gname][int(PH[fo]) % len(RUN[gname])], (rx, feet - 78 * S))
    if ts >= T_LAND - 0.32:
        if ts < T_LAND:
            u = (ts - (T_LAND - 0.32)) / 0.32; fr = KIDLE[0]; ky = int(-fr.height + (K_BOT - 4 * S) * u * u)
            img.alpha_composite(fr, (kx - fr.width // 2, ky))
        else:
            u = ts - T_LAND; k = int(u * 15)
            fr = KLAND[k] if k < len(KLAND) else KIDLE[int(ta * 10) % len(KIDLE)]
            img.alpha_composite(fr, (kx - fr.width // 2, K_BOT - fr.height))
            if u < 0.7:
                sc = 1.0 + 0.9 * u; dw, dh = int(DUST.width * 3 * sc), int(DUST.height * 3 * sc)
                du = DUST.resize((dw, dh), Image.NEAREST); al = du.getchannel('A').point(lambda p: int(p * max(0, 1 - u / 0.7)))
                du.putalpha(al); img.alpha_composite(du, (kx - dw // 2, K_BOT - dh + 20))
    for fr_, pos_ in flyers: img.alpha_composite(fr_, pos_)
    if T_LAND <= ts < T_LAND + 0.5:
        amp = int(26 * (1 - (ts - T_LAND) / 0.5)); rs = random.Random(fo)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 255)); sh.paste(img, (rs.randint(-amp, amp), rs.randint(-amp, amp))); img = sh
    return img
# ---------------- top band (hook style: big, high contrast, safe zone x70-1025, y>=262)
HX0, HX1, HY0 = 70, 1025, 262
HOOK_LINES = [('CAN YOU FIND', (255, 255, 255), 68), ('THE CHEATER?', (255, 214, 60), 76)]   # race_v4 (Bennett): the audience's job
END_LINES = [('DID YOU', (255, 255, 255), 68), ('CATCH HIM?', (255, 214, 60), 76)]          # replaces the hook text in the same strip at the end
def band(img, y1, border=(255, 214, 60), a=1.0):
    # hfg12: Bennett's approved strip (the original race reel): full-width dark translucent strip edge to edge, no corners, no border
    blend(img, lambda dd: dd.rectangle([0, HY0, W, y1], fill=(10, 8, 20, int(175 * a))))
def strip_lines(img, lines, pad=22, gap=18):
    y1 = HY0 + 2 * pad + sum(px for _, _, px in lines) + gap * (len(lines) - 1); band(img, y1)
    d = ImageDraw.Draw(img); y = HY0 + pad
    for t, c, px in lines:
        ctext(d, (HX0 + HX1) / 2, y, t, F(px), c, 9); y += px + gap
    return y1
def hook(img): return strip_lines(img, HOOK_LINES)
VIC2 = {k: [f.resize((f.width // 2, f.height // 2), Image.NEAREST) for f in v] for k, v in VIC.items()}   # same 184px as v2 (VIC is now 4x)
def win_banner(img, who, text, u, col):
    a = min(1, u / 0.2); band(img, 452, col, a)
    vf = VIC2[who][int(u * 8) % len(VIC2[who])]
    img.alpha_composite(vf, (84, 448 - vf.height))
    d = ImageDraw.Draw(img); lx = 84 + vf.width + 8; px = 60
    while d.textlength(text, font=F(px)) + 18 > HX1 - 24 - lx: px -= 2
    f = F(px); w = d.textlength(text, font=f); cx = (lx + HX1 - 24) / 2
    d.text((cx - w / 2, 357 - px // 2), text, font=f, fill=col, stroke_width=9, stroke_fill=(10, 6, 18))
def text_band(img, lines, cols, px):
    gap = int(px * 0.4); y1 = HY0 + 2 * 28 + len(lines) * px + (len(lines) - 1) * gap; band(img, y1, (255, 255, 255))
    d = ImageDraw.Draw(img); y = HY0 + 28
    for l, c in zip(lines, cols):
        ctext(d, (HX0 + HX1) / 2, y, l, F(px), c, 9); y += px + gap
def live_overlays(img, fo):
    ta = fo / FPS; ts = src_t(ta); d = ImageDraw.Draw(img)
    if ts < T_GO + 1.2:
        a = 1 if ts < T_GO else max(0, 1 - (ts - T_GO) / 1.2)
        for gname in G:
            li = st[gname]['lane']; y = TRACK_TOP + LANE_H * li + 22
            tag = NAMES[gname]; w = d.textlength(tag, font=F(44)); tx0 = 360
            blend(img, lambda dd: dd.rectangle([tx0, y, tx0 + w + 36, y + 70], fill=(20, 15, 35, int(220 * a))))
            blend(img, lambda dd: dd.text((tx0 + 18, y + 13), tag, font=F(44), fill=COL[gname] + (int(255 * a),), stroke_width=4, stroke_fill=(10, 6, 18, int(255 * a))))
            d = ImageDraw.Draw(img)
    if 0 <= ta < 1.35:
        u = ta; n = 3 - int(u / 0.25); txt = str(n) if n > 0 else 'GO!'
        sc = 1.25 - 0.25 * ((u % 0.25) / 0.25) if n > 0 else 1.0
        fs = int(170 * sc); ctext(d, 800, 1000 - fs // 2, txt, F(fs), (255, 214, 60) if n > 0 else (120, 230, 90), 10)
    # hfg12: flashing 'KING SLIME!' cut (the growing shadow and the crowned giant slime say it)
    for k_, gname in enumerate(OUT_G):   # big OUT stamps, one per lane, staggered after the KING SLIME banner (never overlapping it)
        u = ts - (T_LAND + 0.6 + 0.3 * k_)
        if 0 <= u < 2.2:
            stp = OUTST[gname]; sc = 1.0 + 0.3 * max(0, 1 - u / 0.12)    # hard pop
            if sc > 1.01: stp = stp.resize((int(stp.width * sc), int(stp.height * sc)), Image.NEAREST)
            cy_ = TRACK_TOP + LANE_H * st[gname]['lane'] + LANE_H // 2 - 10
            img.alpha_composite(stp, (int(470 - stp.width / 2), int(cy_ - stp.height / 2)))

CHIP_INFO = {}
# RULES chip (Bennett: "a small RULES chip flashing on the skip"): small, fixed spot under the hook band, no arrow, no other text
def rules_chip(img, fo):
    ta = fo / FPS
    if not (T_CH_O <= ta < T_CH_END_O + 0.35): return
    u = ta - T_CH_O
    if not (u > 0.75 or int(u * 8) % 2 == 0): return
    f = F(44); d0 = ImageDraw.Draw(img); w = d0.textlength('RULES', font=f); cw, ch = int(w + 52), 44 + 36
    chip = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(chip)
    cd.rounded_rectangle([0, 0, cw - 1, ch - 1], 16, fill=(196, 26, 40, 245), outline=(255, 255, 255, 255), width=5)
    cd.text((26, 18), 'RULES', font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(70, 6, 14))
    sc = 1.0 + 0.3 * max(0, 1 - u / 0.15)
    if sc > 1.01: chip = chip.resize((int(cw * sc), int(ch * sc)), Image.NEAREST)
    x = 1012 - chip.width; y = 436 + ch // 2 - chip.height // 2
    img.alpha_composite(chip, (int(x), int(y)))
    CHIP_INFO.setdefault('frames', []).append(fo)
def out_stamp(name):
    f = F(72); tw = ImageDraw.Draw(Image.new('L', (1, 1))).textlength(name, font=f)
    im = Image.new('RGBA', (int(tw) + 90, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, im.width - 5, 145], 22, fill=(170, 20, 34, 245), outline=(255, 255, 255, 255), width=8)
    d.text((45, 39), name, font=f, fill=(255, 255, 255), stroke_width=8, stroke_fill=(60, 4, 12))
    return im.rotate(-4, expand=True, resample=Image.NEAREST)
OUTST = {g: out_stamp(NAMES[g] + ' OUT!') for g in OUT_G}
# ---------------- render
STILLS = [float(x) for x in sys.argv[1:]]
OUTV = OUTD + '/race4_noaudio.mp4'
if not STILLS:
    out = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTV], stdin=subprocess.PIPE)
def emit(img, fo):
    if STILLS: img.convert('RGB').save(OUTD + f'/st_{fo / FPS:.2f}.png')
    else: out.stdin.write(img.convert('RGB').tobytes())
REF_X = 100; REF_Y = FEET[1] - 80 * S + 6     # slime referee stands in Cleo's empty lane
# FOUL stamp (race_v4: 0.8x and placed on Cyrus, so the verdict points at him)
STAMP = Image.new('RGBA', (640, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(STAMP)
sd.rounded_rectangle([10, 10, 630, 190], 28, outline=(230, 40, 40), width=14, fill=(255, 245, 235, 60))
tw = sd.textlength('FOUL!', font=F(100)); sd.text(((640 - tw) / 2, 50), 'FOUL!', font=F(100), fill=(230, 40, 40), stroke_width=4, stroke_fill=(90, 10, 16))
STAMP = STAMP.rotate(-8, expand=True, resample=Image.NEAREST)
STAMP = STAMP.resize((STAMP.width * 4 // 5, STAMP.height * 4 // 5), Image.NEAREST)
NTAIL = int(round(LOOP_TAIL * FPS))
RAY_ORG_FIX = [None]

def race_frame(fo, ta=None):
    """the race and its verdict, exactly as before (fo = race output frame); ta = clock for idle animations"""
    if ta is None: ta = fo / FPS
    tr = fo / FPS
    img = world(fo) if tr < T_TOSS_O + 0.8 else world(fo, skip=('ray',))
    if tr >= T_REF_O:   # slime referee
        u = tr - T_REF_O
        if u < 0.25:
            yy = REF_Y + int((1 - u / 0.25) * 500); img.alpha_composite(REF_I[0], (REF_X, yy))
        elif u < 0.25 + len(REF_W) / 12:
            k = min(len(REF_W) - 1, int((u - 0.25) * 12)); img.alpha_composite(REF_W[k], (REF_X, REF_Y))
        else:
            hop = int(abs(math.sin((ta - T_RWIN_O) * 9)) * 40) if tr >= T_RWIN_O else 0   # happy bounce when Rayleigh wins
            img.alpha_composite(REF_I[int(ta * 6) % len(REF_I)], (REF_X, REF_Y - hop))
    live_overlays(img, fo)
    if T_DQ_O <= tr < T_RWIN_O:   # FOUL! on Cyrus
        u = tr - T_DQ_O; cx, cy, rx = POS[(fo, 'cyrus')]
        sc = max(1.0, 1.7 - u / 0.12 * 0.7); st2 = STAMP.resize((int(STAMP.width * sc), int(STAMP.height * sc)), Image.NEAREST)
        x0 = max(72, min(1022 - st2.width, cx - st2.width / 2)); y0 = FEET[0] + 20 - (st2.height - STAMP.height) / 2   # just under Cyrus's feet: he stays visible
        img.alpha_composite(st2, (int(x0), int(y0)))
    rx_, ry_, rr = POS[(fo, 'ray')]; RAY_ORG = (rr, FEET[3] - 78 * S)
    if tr >= T_TOSS_O:
        head = (RAY_ORG[0] + 46 * S - CROWN.width // 2, RAY_ORG[1] + 4 * S - CROWN.height + 10)
        src = (REF_X + 44 * S - CROWN.width // 2, REF_Y + 24 * S)
        p = min(1, (tr - T_TOSS_O) / 0.8); e = p * p * (3 - 2 * p)
        cx = src[0] + (head[0] - src[0]) * e; cyy = src[1] + (head[1] - src[1]) * e - 260 * math.sin(math.pi * e)
        if p >= 1:
            vf = VIC['ray'][int(ta * 8) % len(VIC['ray'])]; img.alpha_composite(vf, RAY_ORG)
            cyy = head[1] + int(3 * math.sin(ta * 8))
            d = ImageDraw.Draw(img)
            for k2 in range(6):
                ang = ta * 3 + k2; r = 150
                sx_, sy_ = RAY_ORG[0] + 46 * S + math.cos(ang) * r, RAY_ORG[1] + 30 * S + math.sin(ang) * r * 0.6
                d.rectangle([sx_ - 6, sy_ - 6, sx_ + 6, sy_ + 6], fill=(255, 230, 120)); d.rectangle([sx_ - 14, sy_ - 2, sx_ + 14, sy_ + 2], fill=(255, 245, 190)); d.rectangle([sx_ - 2, sy_ - 14, sx_ + 2, sy_ + 14], fill=(255, 245, 190))
        img.alpha_composite(CROWN, (int(cx), int(cyy)))
    # top strip
    if tr < T_FIN_O: hook(img)
    elif tr < T_REF_O: win_banner(img, 'cyrus', 'CYRUS WINS!', tr - T_FIN_O, COL['cyrus'])
    elif tr < T_RWIN_O: pass   # referee + FOUL!: the picture says it (HE SKIPPED A SLIME! cut)
    elif tr < T_RWD_O: win_banner(img, 'ray', 'RAYLEIGH WINS!', tr - T_RWIN_O, COL['ray'])
    return img

# ---------------- flashback look
_yy, _xx = np.mgrid[0:H, 0:W]
_r = np.sqrt(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H * 0.47) / (H * 0.6)) ** 2)
VIG = np.clip(1.15 - 0.75 * _r ** 2, 0.25, 1.0)[..., None].astype(np.float32)
def sepia(img, amt=1.0, seed=0, grain=True):
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    g = a @ np.array([0.30, 0.59, 0.11], np.float32)
    sp = np.stack([g * 1.02 + 38, g * 0.86 + 22, g * 0.62 + 4], -1)
    o = a * (1 - amt) + sp * amt
    o = o * (1 - amt + amt * VIG)
    if grain:
        rs = np.random.default_rng(seed); n = rs.normal(0, 7, (H // 4, W // 4)).astype(np.float32)
        o += amt * np.repeat(np.repeat(n, 4, 0), 4, 1)[..., None]
        o *= 1 + amt * 0.03 * math.sin(seed * 2.3)   # projector flicker
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).convert('RGBA')
def rewind_fx(img, k, n):
    """VHS rewind: tracking bands shifted sideways, noise lines, a white rewind icon (no text)"""
    a = np.asarray(img.convert('RGB')).copy(); rs = np.random.default_rng(1000 + k)
    for _ in range(3):
        y0 = int(rs.integers(0, H - 80)); h = int(rs.integers(20, 70)); a[y0:y0 + h] = np.roll(a[y0:y0 + h], int(rs.integers(-60, 60)), 1)
    for _ in range(4):
        y0 = int(rs.integers(0, H - 6)); a[y0:y0 + 4] = np.clip(a[y0:y0 + 4].astype(int) + rs.integers(60, 140, (4, W, 1)), 0, 255)
    im = Image.fromarray(a).convert('RGBA'); d = ImageDraw.Draw(im)
    if (k // 4) % 2 == 0:
        x0, y0 = 120, 560
        for j in range(2):
            xo = x0 + j * 62; d.polygon([(xo + 62, y0), (xo + 62, y0 + 96), (xo, y0 + 48)], fill=(255, 255, 255), outline=(10, 6, 18), width=6)
    return im
GUM = Image.open('../gummies/pick_mel.png').convert('RGBA'); GUM = GUM.resize((GUM.width * 3, GUM.height * 3), Image.NEAREST)   # Rayleigh's melatonin gummy (existing art)
def heart(d, cx, cy, s, col=(255, 90, 140)):
    for (x, y) in [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (0, 2), (-2, -1)]:
        d.rectangle([cx + x * s - s // 2, cy + y * s - s // 2, cx + x * s + s // 2 - 1, cy + y * s + s // 2 - 1], fill=col)
BRIBED = [sl for sl in st['cyrus']['slimes'] if sl.get('skipped')][0]
FB_CAM = BRIBED['x'] - 720
FB_TS = 1.2   # source time before GO: all racers still at the start line, far off screen
def fb_handoff(u, fo):
    """flashback 1 (u = seconds in): Rayleigh runs in behind the slime in Cyrus's lane, stops, tosses it a gummy, the slime gobbles it.
    returns (sepia base, colour overlay fn): the gummy and its sparkles stay in full colour on the sepia flashback"""
    HIDE_BRIBE[0] = True; img = world(fo, skip=tuple(G), ts_over=FB_TS, cam_over=FB_CAM); HIDE_BRIBE[0] = False
    feet = FEET[0]; stop_x = 720 - 330 - 46 * S; t_run = 0.75; x_start = -260
    t_toss = 0.95; t_land = t_toss + 0.45
    # the bribed slime (existing idle frames), squash-hop when it swallows the gummy
    fr = SL_IDLE[int((u + 5) * 10) % len(SL_IDLE)]; q = u - t_land; hop = 0; sq = 1.0
    if 0 <= q < 0.45: hop = int(70 * math.sin(math.pi * q / 0.45)); sq = 0.88
    elif 0.45 <= q < 0.75: sq = 1.0 + 0.16 * math.sin((q - 0.45) * 18) * (1 - (q - 0.45) / 0.3)
    fr2 = fr.resize((int(fr.width * sq), int(fr.height / sq)), Image.NEAREST) if abs(sq - 1) > 0.01 else fr
    img.alpha_composite(fr2, (720 - 32 * S - (fr2.width - fr.width) // 2, feet - 62 * S + (fr.height - fr2.height) - hop))
    if u < t_run:
        rx = x_start + (stop_x - x_start) * (u / t_run); rf = RUN['ray'][int(u * 14) % len(RUN['ray'])]
    else:
        rx = stop_x; rf = IDLE['ray'][int(u * 8) % len(IDLE['ray'])]
    img.alpha_composite(rf, (int(rx), feet - 78 * S))
    hand = (stop_x + 66 * S, feet - 46 * S); mouth = (720, feet - 30 * S)
    def overlay(im):
        if t_toss <= u < t_land:
            p = (u - t_toss) / (t_land - t_toss)
            gx = hand[0] + (mouth[0] - hand[0]) * p; gy = hand[1] + (mouth[1] - hand[1]) * p - 170 * math.sin(math.pi * p)
            im.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
        if q >= 0: draw_bribe_react(im, q, 720, feet - 26 * S - hop)
    return img, overlay
def draw_bribe_react(img, q, cx, top):
    d = ImageDraw.Draw(img)
    if q < 0.5:
        for k2 in range(5):
            ang = k2 * 1.256 + q * 4; r = 60 + 160 * q
            sx_, sy_ = cx + math.cos(ang) * r, top + 40 + math.sin(ang) * r * 0.7
            d.rectangle([sx_ - 7, sy_ - 7, sx_ + 7, sy_ + 7], fill=(200, 120, 255)); d.rectangle([sx_ - 15, sy_ - 2, sx_ + 15, sy_ + 2], fill=(235, 200, 255)); d.rectangle([sx_ - 2, sy_ - 15, sx_ + 2, sy_ + 15], fill=(235, 200, 255))
    if q > 0.12:
        heart(d, int(cx + 20), int(top - 40 - 50 * min(1, (q - 0.12) / 0.3)), 11)
# ---------------- main loop
events = []
NOUT = int(round(END_O * FPS))
NRWD = int(round(D_RWD * FPS)); NFB1 = int(round(D_FB1 * FPS)); NFB2 = int(round(D_FB2 * FPS))
F_RWD = int(round(T_RWD_O * FPS)); F_FB1 = F_RWD + NRWD; F_FB2 = F_FB1 + NFB1; F_NOW = F_FB2 + NFB2
F_LOOP = NOUT - NTAIL
RW_FROM = F_RWD - 1; RW_TO = int(0.4 * FPS)
F_REPLAY0 = int(round((T_CH_O - 0.95) * FPS))
print('frames: rewind', F_RWD, 'fb1', F_FB1, 'fb2', F_FB2, 'now', F_NOW, 'loop', F_LOOP, 'end', NOUT)
for fo in range(NOUT):
    ta = fo / FPS
    if STILLS and not any(abs(ta - x) < 0.5 / FPS for x in STILLS): continue
    if fo >= F_LOOP:                       # loop tail: start line just before frame 0
        fw = fo - NOUT
        img = world(fw); live_overlays(img, fw); hook(img); emit(img, fo); continue
    if fo < F_RWD:
        img = race_frame(fo)
    elif fo < F_FB1:                       # rewind: the whole race runs backwards to the start line, fading to sepia
        k = fo - F_RWD; p = (k + 1) / NRWD
        fr_src = int(round(RW_FROM + (RW_TO - RW_FROM) * (p ** 1.4)))
        img = world(fr_src)
        img = rewind_fx(sepia(img, min(1, 0.25 + p), seed=fo), k, NRWD)
    elif fo < F_FB2:                       # flashback 1: the bribe
        u = (fo - F_FB1) / FPS
        img, ov = fb_handoff(u, fo)
        img = sepia(img, 1.0, seed=fo); ov(img)
    elif fo < F_NOW:                       # flashback 2: replay of the slime hopping out of Cyrus's way
        fr_src = F_REPLAY0 + (fo - F_FB2)
        img = world(fr_src)
        img = sepia(img, 1.0, seed=fo)
        if BRIBE_POS[0] is not None:
            ts_ = src_t(fr_src / FPS); q = ts_ - (T_CH - 0.6)
            if 0 <= q < 0.6: draw_bribe_react(img, q * 0.8, BRIBE_POS[0][0], BRIBE_POS[0][1])
    else:                                  # back to the present: the post-race scene resumes, Rayleigh crowned
        img = race_frame(fo - FBF)
        k = fo - F_NOW
        if k < 4: blend(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(255, 255, 255, int(200 * (1 - k / 4)))))
        strip_lines(img, END_LINES)
    emit(img, fo)
if not STILLS: out.stdin.close(); out.wait()
# ---------------- sound events (source-time hits remapped to output time)
for gname, s in st.items():
    for kind, t in s['events']:
        to = out_t(t)
        if kind == 'atk': events.append((out_t(t + HIT[gname][0] / ATK_FPS * 0.6), SFX[gname]))
        if kind == 'kill': events.append((to, 'squish'))
        if kind == 'bonk': events.append((to, 'punch'))
T_HOP1_O = out_t(T_CH - 0.6); T_HOP2_O = out_t(T_CH + 0.45)
RP = lambda t_src_out: F_FB2 / FPS + (t_src_out - F_REPLAY0 / FPS)   # race output time -> replay output time
events += [(0.0, 'tick_8bit'), (0.25, 'tick_8bit'), (0.5, 'tick_8bit'), (0.75, 'go_8bit'),
           (T_KLAND_O, 'punch'), (T_KLAND_O + 0.02, 'squish'), (T_KLAND_O + 0.05, 'punch'),
           (T_HOP1_O, 'jump'), (T_HOP2_O, 'jump'), (T_FIN_O, 'ding_8bit'),
           (T_REF_O + 0.3, 'whistle'),
           (T_DQ_O, 'punch'), (T_DQ_O + 0.03, 'buzz_8bit'),
           (T_TOSS_O, 'vg02'), (T_RWIN_O, 'vg02'),
           (T_RWD_O, 'rewind'),
           (T_FB1_O + 0.95, 'swish'), (T_FB1_O + 1.40, 'squish'), (T_FB1_O + 1.52, 'twinkle'),
           (RP(T_HOP1_O), 'jump'), (RP(T_HOP1_O) + 0.05, 'twinkle'),
           (T_NOW_O, 'vg02'), (T_NOW_O + 0.05, 'twinkle')]
events = [(round(a, 3), b) for a, b in events if 0 <= a < END_O - 0.1]
json.dump({'events': sorted(events), 'end': END_O,
           'beats': {'go': out_t(T_GO), 'king_land': T_KLAND_O, 'slime_hop_out': T_HOP1_O, 'cyrus_passes': T_CH_O, 'slime_hop_back': T_HOP2_O,
                     'cyrus_finish': T_FIN_O, 'ray_finish': T_RAY_O, 'referee': T_REF_O, 'foul': T_DQ_O, 'crown': T_TOSS_O, 'ray_wins': T_RWIN_O,
                     'rewind': T_RWD_O, 'fb_bribe': T_FB1_O, 'fb_replay': T_FB2_O, 'replay_hop': RP(T_HOP1_O), 'present': T_NOW_O, 'loop_cut': T_LOOP_O}},
          open(OUTD + '/race4_events.json', 'w'), indent=1)
print('done', round(END_O, 2), NOUT)
