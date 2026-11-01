# n02 race (Oct 30 post). New race in the race_v3 format (fork_hfg12/race/render_race3_chip.py): four guides, slimes on the track,
# King Slime takes out Cleo + Joy, Cyrus 'wins', the slime referee calls the foul, Rayleigh is crowned.
# Fresh: new lane order + seed, the foul is a FALSE START (Cyrus leaves on '1'), hook 'CAN YOU SPOT THE FOUL?', end 'DID YOU SEE IT?'
# loops straight back into the countdown where it happens. Break: the King Slime drops in next to the champion... and just wants to say congrats.
# Physics fixes vs race_v3: real time (no fast-forward), attack frames aligned to the run frames (+14 native; race_v3's -14 made every
# swing jump the guide 112px back), planted stop before each swing, finishers decelerate (no instant stop), KO flight under real gravity,
# winner poses replace the track sprite (no banner portraits), referee hops on ballistic arcs.
import numpy as np, glob, math, random, subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
OUTD = os.path.dirname(os.path.abspath(__file__)); S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
os.chdir(S_ + 'pixellab/race')
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'
A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
S = 4
_fc = {}
def F(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
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
G = ['cyrus', 'ray', 'joy', 'cleo']          # fresh lane order: the two contenders side by side up top
NAMES = {'cyrus': 'CYRUS', 'cleo': 'CLEO', 'joy': 'JOY', 'ray': 'RAYLEIGH'}
COL = {'cyrus': (255, 176, 40), 'cleo': (120, 170, 255), 'joy': (120, 220, 90), 'ray': (200, 110, 255)}
RUN = {g: load(f'{g}_run')[1:] for g in G}
ATK = {g: load(f'{g}_atk') for g in G}
def tip(g):
    fs = sorted(glob.glob(f'{g}_atk/*.png'))[:9]; r = [Image.open(p).convert('RGBA').getbbox()[2] for p in fs]
    k = max(range(len(r)), key=lambda i: r[i]); return k, r[k]
HIT = {g: tip(g) for g in G}                 # (impact frame, weapon tip x in attack-native px)
SFX = {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'swish', 'cyrus': 'punch'}
SL_IDLE = load('slime_idle_c', clean=True); SL_SPLAT = load('slime_splat_c', clean=True)
IDLE = {g: gifload({'joy': 'idle_0.gif', 'cyrus': 'idle_8.gif', 'ray': 'idle_6.gif', 'cleo': 'idle_3.gif'}[g]) for g in G}
VIC = {'cyrus': gifload('vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif'), 'ray': gifload('vic_victoryPose_1.gif')}
RS = S_ + 'fork_rc1/race/refslime/'
REF_I = load(RS + 'edit7'); REF_W = load(RS + 'blow22')
CROWN = Image.open('../ref/crown_cands/01.png').convert('RGBA'); CROWN = CROWN.crop(CROWN.getbbox()); CROWN = CROWN.resize((CROWN.width * S, CROWN.height * S), Image.NEAREST)
KIDLE = load('../king/king2_idle', 3); KLAND = load('../king/king2_land', 3)          # 3x for the ending cameo (fits beside the champion)
KIDLE4 = load('../king/king2_idle'); KLAND4 = load('../king/king2_land')
KO = {g: load(f'../king/{g}_ko') for g in G}
DUST = Image.open('../king/dust_cands/00.png').convert('RGBA'); DUST = DUST.crop(DUST.getbbox())
# ---------------- layout
TRACK_TOP, LANE_H, NL = 540, 240, 4
GY0 = TRACK_TOP - 96
TRACK_BOT = TRACK_TOP + LANE_H * NL
FEET = [TRACK_TOP + LANE_H * i + LANE_H - 30 for i in range(NL)]
START_X = 300; FINISH_X = int(os.environ.get('FIN', '3600'))
def blend(img, fn):
    L_ = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L_)); img.alpha_composite(L_)
# ---------------- simulation (output time = sim time; the countdown runs 0..T_GO)
T_GO = 0.9; T_FALSE = 0.6                    # 3 (0-0.3) 2 (0.3-0.6) 1 (0.6-0.9) GO! (0.9): Cyrus leaves on '1'
OUT_G = ['joy', 'cleo']
T_WARN = float(os.environ.get('TW', '4.4')); T_LAND = T_WARN + 1.1
ATK_FPS = 18; ATK_LEN = 12 / ATK_FPS; PLANT = 0.35
DECEL = 0.5
DEC = {'cyrus': 1.6, 'ray': 0.5, 'joy': 0.5, 'cleo': 0.5}   # Cyrus celebrates on the run-out, so the two finishers end up apart
def run_sim(seed, dur=16.0):
    rnd = random.Random(seed); st = {}
    for li, g in enumerate(G):
        while True:
            sl = sorted(rnd.uniform(1000, FINISH_X - 500) for _ in range(3))
            if min(b - a for a, b in zip(sl, sl[1:])) >= 650: break
        st[g] = dict(lane=li, x=float(START_X - 150), slimes=[dict(x=s, hp=rnd.choice([1, 1, 1, 2]), dead_t=None) for s in sl],
                     v=rnd.uniform(440, 490), ph=rnd.uniform(0, 6.28), state='ready', t0=0, target=None, fin=None, vfin=0, events=[], hitdone=False)
    tl = []; dt = 1 / FPS
    for f in range(int(dur * FPS)):
        t = f / FPS
        for g, s in st.items():
            if s['state'] == 'out': continue
            go = T_FALSE if g == 'cyrus' else T_GO
            if t < go: continue
            if s['state'] == 'ready': s['state'] = 'run'
            if t >= T_LAND and g in OUT_G:
                s['state'] = 'out'; s['out_x'] = s['x']; s['t0'] = T_LAND; continue
            if s['fin'] is not None:
                u = t - s['fin']
                if u < DEC[g]: s['x'] += s['vfin'] * (1 - u / DEC[g]) * dt; s['state'] = 'coast'
                else: s['state'] = 'stop'
                continue
            if s['state'] == 'run':
                v = s['v'] * (1 + 0.10 * math.sin(1.3 * t + s['ph']) + 0.05 * math.sin(3.1 * t + 2 * s['ph']))
                nx = s['x'] + v * dt
                live = [sl for sl in s['slimes'] if sl['dead_t'] is None]
                hf, hx = HIT[g]; reach = (hx + 14) * S - 16      # weapon tip sinks 16px into the slime
                if live and nx + reach >= live[0]['x']:
                    s['x'] = live[0]['x'] - reach; s['state'] = 'atk'; s['t0'] = t; s['target'] = live[0]; s['events'].append(('atk', t)); s['hitdone'] = False; s['first'] = True
                else:
                    s['x'] = nx; s['vnow'] = v
            elif s['state'] == 'atk':
                pl = PLANT if s['first'] else 0.0
                u = t - s['t0'] - pl; hf, hx = HIT[g]
                if u >= (hf + 0.5) / ATK_FPS and not s['hitdone']:
                    s['hitdone'] = True; s['target']['hp'] -= 1
                    if s['target']['hp'] <= 0: s['target']['dead_t'] = t; s['events'].append(('kill', t))
                    else: s['events'].append(('bonk', t))
                if u >= ATK_LEN:
                    s['hitdone'] = False
                    if s['target']['dead_t'] is not None: s['state'] = 'run'
                    else: s['t0'] = t; s['first'] = False; s['events'].append(('atk', t))
            if s['fin'] is None and s['x'] + 46 * S >= FINISH_X: s['fin'] = t; s['vfin'] = s.get('vnow', s['v'])
        tl.append({k: (v['x'], v['state'], v['t0'], v.get('first', True)) for k, v in st.items()})
    return st, tl
def score(seed):
    st, tl = run_sim(seed); li = int(T_LAND * FPS)
    if abs(tl[li]['cleo'][0] - tl[li]['joy'][0]) > 220: return None
    front_out = max(tl[li]['cleo'][0], tl[li]['joy'][0])
    if min(tl[li]['cyrus'][0], tl[li]['ray'][0]) < front_out + float(os.environ.get('AHEAD', '60')): return None     # the KO flight never crosses the contenders
    c, r = st['cyrus']['fin'], st['ray']['fin']
    if c is None or r is None or not (c < r < c + 0.22): return None              # the 0.3s false start decided it
    if not (10.0 < c < 12.0): return None
    leaders = []
    for i in range(int(1.5 * FPS), int(c * FPS), 10):
        L_ = max([k for k in tl[i] if k not in OUT_G or i < li], key=lambda k: tl[i][k][0])
        if not leaders or leaders[-1] != L_: leaders.append(L_)
    if 'ray' not in leaders or len(leaders) < 3: return None
    return round(r - c, 2), round(c, 2), leaders
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r_ = score(seed)
        if r_: print(seed, r_, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
st, TL = run_sim(SEED)
T_FIN = st['cyrus']['fin']; T_RAY = st['ray']['fin']
print('cyrus', round(T_FIN, 2), 'ray', round(T_RAY, 2))
li0 = int(T_LAND * FPS)
KX = (TL[li0]['cleo'][0] + TL[li0]['joy'][0]) / 2 + 46 * S
K_BOT = FEET[3] + 18
# ---------------- ending beats
T_POSE = T_FIN + DEC['cyrus'] + 0.05                # Cyrus celebrates (victory pose replaces his track sprite)
T_REF = T_FIN + 1.0                          # slime referee hops in along Cyrus's lane
REF_HOPS = 3; HOPD = 0.32
T_WHIS = T_REF + REF_HOPS * HOPD + 0.05       # lands, blows the whistle
T_FOUL = T_WHIS + 0.5                        # FOUL stamp on Cyrus, strip: FALSE START!
T_CROWN = T_FOUL + 0.85                        # crown pops off the finish banner, arcs onto Rayleigh
CROWN_D = 0.7
T_RWIN = T_CROWN + CROWN_D                    # RAYLEIGH WINS!
T_KSH = T_RWIN + 0.85                          # a shadow grows beside the champion...
T_KL = T_KSH + 0.8                            # ...King Slime lands right next to her
T_HEART = T_KL + 0.95                         # and just wants to say congrats
T_END = T_HEART + 0.2; T_LOOP = T_END + 2.3   # DID YOU / SEE IT? held 2.3s
LOOP_TAIL = 0.0
END_O = T_LOOP
NOUT = int(round(END_O * FPS))
# ---------------- camera
RX_EXT = max(max(f.getbbox()[2] for f in RUN[g]) for g in G)
CAMS = []; cam = 0.0; hold_cam = 0.0
CAM_END = FINISH_X - 230                       # finish line at screen x~300 at the end (room for the King on the right)
for f in range(len(TL)):
    t = f / FPS; snap = TL[f]
    lead_x = max(v[0] for k, v in snap.items() if not (k in OUT_G and t >= T_LAND))
    target_cam = max(0, min(CAM_END, lead_x - 520))
    if t > T_FIN: target_cam = CAM_END
    if T_LAND - 0.3 <= t < T_LAND + 0.9: target_cam = hold_cam
    else: hold_cam = target_cam
    cam += (target_cam - cam) * 0.12
    need = max((v[0] + RX_EXT - (887 if st[k]['lane'] >= 2 else 1020)) for k, v in snap.items() if not (k in OUT_G and t >= T_LAND))
    cam = max(cam, min(need, CAM_END)); CAMS.append(cam)
def snapf(t):
    f = max(0, min(len(TL) - 1, int(round(t * FPS)))); return TL[f], CAMS[f]
# ---------------- track
T_ = {i: Image.open(f'tiles/tile_{i}.png').convert('RGBA').resize((96, 96), Image.NEAREST) for i in range(16)}
GW = FINISH_X + 1400
ground = Image.new('RGBA', (GW, H - GY0), (0, 0, 0, 0))
for y in range(GY0, H, 96):
    for x in range(0, GW, 96):
        if y < TRACK_TOP - 96: idx = 0
        elif y < TRACK_TOP: idx = 3
        elif y < TRACK_BOT: idx = 15
        elif y < TRACK_BOT + 96: idx = 12
        else: idx = 0
        tile = T_[idx]
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
g_ = Image.open(A + 'hub.gif'); HUBF = []
for i in range(0, g_.n_frames, 2):
    g_.seek(i); f_ = g_.convert('RGB').resize((1067, 600), Image.NEAREST)
    strip = Image.new('RGB', (1067 * 2, 600)); strip.paste(f_, (0, 0)); strip.paste(f_.transpose(Image.FLIP_LEFT_RIGHT), (1067, 0))
    HUBF.append(strip)
FIN = Image.open('finish_cands/00.png').convert('RGBA'); FIN = FIN.crop(FIN.getbbox()); FIN = FIN.resize((FIN.width * 3, FIN.height * 3), Image.NEAREST)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
# ---------------- positions used by the ending
fin_snap, CAMF = snapf(T_POSE + 0.2)
CYR_X = fin_snap['cyrus'][0]; RAY_X = fin_snap['ray'][0]
RAY_ORG = lambda cam_: (int(RAY_X - cam_), FEET[1] - 78 * S)
REF_STOP = CYR_X + 64 * S                      # just right of Cyrus in his lane, ~one body-width clear (canvas-left x, world)
REF_START = REF_STOP + REF_HOPS * 150         # hops in from the right edge
REF_Y = FEET[0] - 80 * S + 6
KXE = RAY_X + 46 * S + 255                    # King lands just right of the champion, in the empty lane below her (centre, world)
KBOT_E = FEET[2] + 14
def heart(img, x, y, a=255, cell=8):
    pat = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']
    def dr(d):
        for r_, row in enumerate(pat):
            for c_, ch in enumerate(row):
                if ch == 'X': x_ = x + (c_ - 3.5) * cell; y_ = y + r_ * cell; d.rectangle([x_ - 3, y_ - 3, x_ + cell + 2, y_ + cell + 2], fill=(60, 10, 30, a))
        for r_, row in enumerate(pat):
            for c_, ch in enumerate(row):
                if ch == 'X': x_ = x + (c_ - 3.5) * cell; y_ = y + r_ * cell; d.rectangle([x_, y_, x_ + cell - 1, y_ + cell - 1], fill=(255, 110, 150, a) if (r_, c_) != (1, 1) else (255, 225, 235, a))
    blend(img, dr)
def world(fo):
    t = fo / FPS; snap, cam = snapf(t)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    hb = HUBF[int((t + 5) * 6) % len(HUBF)]; px = int(cam * 0.35) % 1067
    img.paste(hb.crop((px, 0, px + W, 600)), (0, 0))
    img.alpha_composite(ground.crop((int(cam), 0, int(cam) + W, H - GY0)), (0, GY0))
    fx = FINISH_X - int(cam) - FIN.width // 2
    if -FIN.width < fx < W: img.alpha_composite(FIN, (fx, TRACK_TOP - FIN.height + 60))
    kx = int(KX - cam)
    if T_WARN <= t < T_LAND + 0.05:
        u = (t - T_WARN) / (T_LAND - T_WARN); sw = int(60 + 300 * u)
        blend(img, lambda dd: dd.ellipse([kx - sw // 2, K_BOT - sw // 7, kx + sw // 2, K_BOT + sw // 7], fill=(0, 0, 0, int(70 + 80 * u))))
    if T_KL - 0.32 <= t < T_KL:
        q = (t - (T_KL - 0.32)) / 0.32; frk = KIDLE[0]; kxe_ = int(KXE - cam)
        ky = int((KBOT_E - frk.height) - (1 - q * q) * (KBOT_E + 40))
        img.alpha_composite(frk, (kxe_ - frk.width // 2, ky))
    flyers = []; front = []
    for g in OUT_G + [g2 for g2 in G if g2 not in OUT_G]:      # KO'd guides first: their flight passes behind the contenders
        s = st[g]; li = s['lane']; x, state, t0, first = snap[g]; feet = FEET[li]
        for sl in s['slimes']:
            sx = int(sl['x'] - cam) - 32 * S
            if sx < -300 or sx > W + 200: continue
            if g in OUT_G and t >= T_LAND + 1.2 and (sl['dead_t'] is None): continue     # empty lanes after the KO
            if sl['dead_t'] is None or t < sl['dead_t']:
                img.alpha_composite(SL_IDLE[int((t + 5) * 10 + sl['x']) % len(SL_IDLE)], (sx, feet - 62 * S))
            else:
                k = int((t - sl['dead_t']) * 16)
                if k < len(SL_SPLAT): img.alpha_composite(SL_SPLAT[k], (sx, feet - 62 * S))
        rx = int(x - cam)
        if state == 'out':
            u = t - T_LAND; ox = s['out_x'] - cam - 18 * S - 900 * u; oy = feet - 78 * S - 18 * S - (2500 * u - 0.5 * 2600 * u * u)
            fr = KO[g][3 + int(u * 18) % 6]
            if oy > -500 and ox > -600: img.alpha_composite(fr, (int(ox), int(oy)))
            continue
        if g == 'cyrus' and t >= T_POSE:
            if t < T_FOUL: fr = VIC['cyrus'][int((t - T_POSE) * 8) % len(VIC['cyrus'])]
            else: fr = IDLE['cyrus'][int(t * 8) % len(IDLE['cyrus'])]
            front.append((fr, (rx, feet - 78 * S))); continue
        if g == 'ray' and t >= T_RWIN: continue          # drawn as the crowned champion below
        if state == 'ready':
            go_ = T_FALSE if g == 'cyrus' else T_GO; amp = 22 * max(0.0, min(1.0, (go_ - t) / 0.15))
            img.alpha_composite(RUN[g][0], (rx, feet - 78 * S - int(abs(math.sin((t + 5) * 9 + li * 0.8)) * amp)))   # bouncing in place, settles before the start
        elif state == 'atk':
            pl = PLANT if first else 0.0; u = t - t0
            k = 0 if u < pl else min(11, int((u - pl) * ATK_FPS)); img.alpha_composite(ATK[g][k], (rx + 14 * S, feet - 78 * S - 26 * S))
        elif state == 'stop':
            img.alpha_composite(IDLE[g][int(t * 8) % len(IDLE[g])], (rx, feet - 78 * S))
        else:
            img.alpha_composite(RUN[g][PH[g][fo] % len(RUN[g])], (rx, feet - 78 * S))
    for fr_, pos_ in front: img.alpha_composite(fr_, pos_)
    if t >= T_LAND - 0.32 and t < T_KSH:
        if t < T_LAND:
            u = (t - (T_LAND - 0.32)) / 0.32; fr = KIDLE4[0]; ky = int(-fr.height + (K_BOT - 4 * S + fr.height) * u * u)
            img.alpha_composite(fr, (kx - fr.width // 2, ky - 0))
        else:
            u = t - T_LAND; k = int(u * 15)
            fr = KLAND4[k] if k < len(KLAND4) else KIDLE4[int(t * 10) % len(KIDLE4)]
            img.alpha_composite(fr, (kx - fr.width // 2, K_BOT - fr.height))
            if u < 0.7:
                sc = 1.0 + 0.9 * u; dw, dh = int(DUST.width * 3 * sc), int(DUST.height * 3 * sc)
                du = DUST.resize((dw, dh), Image.NEAREST); du.putalpha(du.getchannel('A').point(lambda p: int(p * max(0, 1 - u / 0.7))))
                img.alpha_composite(du, (kx - dw // 2, K_BOT - dh + 20))
    for fr_, pos_ in flyers: img.alpha_composite(fr_, pos_)
    return img, cam
def shake(img, fo, t0, amp0=26, dur=0.5):
    t = fo / FPS
    if t0 <= t < t0 + dur:
        amp = int(amp0 * (1 - (t - t0) / dur)); rs = random.Random(fo)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 255)); sh.paste(img, (rs.randint(-amp, amp), rs.randint(-amp, amp))); return sh
    return img
# run-cycle phase per guide: legs advance with distance travelled (no skating)
PH = {g: {} for g in G}
for g in G:
    acc = 0.0; prev = TL[0][g][0]
    for fo in range(NOUT + 2):
        x = TL[min(fo, len(TL) - 1)][g][0]; acc += abs(x - prev) / 30.0; prev = x
        PH[g][fo] = int(acc)
# ---------------- top strip (Bennett's approved full-width translucent strip)
HY0 = 262
def strip(img, lines, cols, px, a=1.0):
    gap = int(px * 0.35); y1 = HY0 + 2 * 24 + len(lines) * px + (len(lines) - 1) * gap
    blend(img, lambda dd: dd.rectangle([0, HY0, W, y1], fill=(10, 8, 20, int(175 * a))))
    d = ImageDraw.Draw(img); y = HY0 + 24
    for l, c in zip(lines, cols):
        ctext(d, W / 2, y, l, F(px), c, 8); y += px + gap
def out_stamp(name):
    f = F(72); tw = ImageDraw.Draw(Image.new('L', (1, 1))).textlength(name, font=f)
    im = Image.new('RGBA', (int(tw) + 90, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, im.width - 5, 145], 22, fill=(170, 20, 34, 245), outline=(255, 255, 255, 255), width=8)
    d.text((45, 39), name, font=f, fill=(255, 255, 255), stroke_width=8, stroke_fill=(60, 4, 12))
    return im.rotate(-4, expand=True, resample=Image.NEAREST)
OUTST = {g: out_stamp(NAMES[g] + ' OUT!') for g in OUT_G}
def foul_plate():
    f = F(60); txt = 'CYRUS: FOUL!'; tw = ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=f)
    im = Image.new('RGBA', (int(tw) + 70, 124), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, im.width - 5, 119], 20, fill=(200, 24, 36, 255), outline=(255, 255, 255, 255), width=7)
    d.text((35, 32), txt, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=(60, 4, 12))
    return im.rotate(-5, expand=True, resample=Image.NEAREST)
FOULP = foul_plate()
STILLS = [float(x) for x in os.environ.get('STILLS', '').split(',') if x]
out = None if STILLS else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + '/n02_noaudio.mp4'], stdin=subprocess.PIPE)
for fo in range(NOUT):
    t = fo / FPS
    if STILLS and not any(abs(t - x) < 0.5 / FPS for x in STILLS): continue
    img, cam = world(fo)
    d = ImageDraw.Draw(img)
    # countdown + name tags
    if t < T_GO + 1.0:
        a = 1 if t < T_GO else max(0, 1 - (t - T_GO) / 1.0)
        for g in G:
            li = st[g]['lane']; y = TRACK_TOP + LANE_H * li + 22; tag = NAMES[g]; w = d.textlength(tag, font=F(44)); tx0 = 360
            blend(img, lambda dd: dd.rectangle([tx0, y, tx0 + w + 36, y + 70], fill=(20, 15, 35, int(220 * a))))
            blend(img, lambda dd: dd.text((tx0 + 18, y + 13), tag, font=F(44), fill=COL[g] + (int(255 * a),), stroke_width=4, stroke_fill=(10, 6, 18, int(255 * a))))
        d = ImageDraw.Draw(img)
    if t < T_GO + 0.45:
        n = 3 - int(t / 0.3); txt = str(n) if n > 0 else 'GO!'
        sc = 1.25 - 0.25 * ((t % 0.3) / 0.3) if n > 0 else 1.0
        fs = int((170 if n > 0 else 130) * sc); ctext(d, 830, 1060 - fs // 2, txt, F(fs), (255, 214, 60) if n > 0 else (120, 230, 90), 10)
    for k_, g in enumerate(OUT_G):
        u = t - (T_LAND + 0.5 + 0.9 * k_)                # one stamp at a time
        if 0 <= u < 0.8:
            stp = OUTST[g]; sc = 1.0 + 0.3 * max(0, 1 - u / 0.12)
            if sc > 1.01: stp = stp.resize((int(stp.width * sc), int(stp.height * sc)), Image.NEAREST)
            cy_ = TRACK_TOP + LANE_H * 3 + LANE_H // 2 - 20          # on the King's base, his face stays visible
            img.alpha_composite(stp, (int(470 - stp.width / 2), int(cy_ - stp.height / 2)))
    # slime referee: three ballistic hops along Cyrus's lane, whistle, then a happy bounce for the champion
    if t >= T_REF:
        u = t - T_REF
        if u < REF_HOPS * HOPD:
            k = int(u / HOPD); q = (u - k * HOPD) / HOPD
            x = REF_START + (k + q) * (REF_STOP - REF_START) / REF_HOPS; y = REF_Y - 4 * 90 * q * (1 - q)
            img.alpha_composite(REF_I[0], (int(x - cam), int(y)))
        elif t < T_WHIS + len(REF_W) / 12:
            k = max(0, min(len(REF_W) - 1, int((t - T_WHIS) * 12))); img.alpha_composite(REF_W[k], (int(REF_STOP - cam), REF_Y))
        else:
            img.alpha_composite(REF_I[int(t * 6) % len(REF_I)], (int(REF_STOP - cam), REF_Y))
    # FOUL plate on Cyrus's legs
    if T_FOUL <= t < T_CROWN + 0.1:
        u = t - T_FOUL; sc = max(1.0, 1.15 - u / 0.1 * 0.15); fp = FOULP.resize((int(FOULP.width * sc), int(FOULP.height * sc)), Image.NEAREST)
        cx = CYR_X - cam + 46 * S; cx = min(max(cx, 70 + fp.width / 2), 1015 - fp.width / 2)
        img.alpha_composite(fp, (int(cx - fp.width / 2), int(FEET[0] - 40 - fp.height / 2)))
    # crown: off the finish banner, a high arc over the track, onto Rayleigh's head
    ro = RAY_ORG(cam); head = (ro[0] + 46 * S - CROWN.width // 2, ro[1] + 8 * S - CROWN.height + 14)
    if t >= T_CROWN:
        src = (FINISH_X - cam - CROWN.width // 2, TRACK_TOP - FIN.height // 2 + 40)
        p = min(1, (t - T_CROWN) / CROWN_D)
        cx = src[0] + (head[0] - src[0]) * p; cyy = src[1] + (head[1] - src[1]) * p - 4 * 60 * p * (1 - p)
        if p >= 1:
            vf = VIC['ray'][int((t - T_RWIN) * 8) % len(VIC['ray'])]; img.alpha_composite(vf, ro)
            a_ = np.array(vf.getchannel('A')) > 0; band = a_[:, 30 * S:60 * S]          # hat columns only (the raised staff is not the head)
            top = int(np.where(band.any(1))[0][0]); cols = np.where(band[top:top + 10].any(0))[0] + 30 * S
            hx = ro[0] + (cols.min() + cols.max()) / 2; cyy = ro[1] + top - CROWN.height + 22; cx = hx - CROWN.width / 2
            if t < T_KSH:
                for k2 in range(6):
                    ang = t * 3 + k2; r = 150
                    sx_, sy_ = ro[0] + 46 * S + math.cos(ang) * r, ro[1] + 40 * S + math.sin(ang) * r * 0.6
                    d = ImageDraw.Draw(img); d.rectangle([sx_ - 6, sy_ - 6, sx_ + 6, sy_ + 6], fill=(255, 230, 120)); d.rectangle([sx_ - 14, sy_ - 2, sx_ + 14, sy_ + 2], fill=(255, 245, 190)); d.rectangle([sx_ - 2, sy_ - 14, sx_ + 2, sy_ + 14], fill=(255, 245, 190))
        img.alpha_composite(CROWN, (int(cx), int(cyy)))
    # the break: a growing shadow beside the champion, King Slime drops in... and just wants to congratulate her
    kxe = int(KXE - cam)
    if T_KSH <= t < T_KL:
        u = (t - T_KSH) / (T_KL - T_KSH); sw = int(60 + 280 * u)
        blend(img, lambda dd: dd.ellipse([kxe - sw // 2, KBOT_E - sw // 7, kxe + sw // 2, KBOT_E + sw // 7], fill=(0, 0, 0, int(60 + 90 * u))))
        pass   # the falling King is drawn inside world(), behind the guides and the referee
    if t >= T_KL:
        u = t - T_KL; k = int(u * 15)
        fr = KLAND[k] if k < len(KLAND) else KIDLE[int(t * 10) % len(KIDLE)]       # squash, rebound, settle, then his happy idle
        img.alpha_composite(fr, (kxe - fr.width // 2, KBOT_E - fr.height))
        if u < 0.6:
            sc = 1.0 + 0.9 * u; dw, dh = int(DUST.width * 2 * sc), int(DUST.height * 2 * sc)
            du = DUST.resize((dw, dh), Image.NEAREST); du.putalpha(du.getchannel('A').point(lambda p_: int(p_ * max(0, 1 - u / 0.6))))
            img.alpha_composite(du, (kxe - dw // 2, KBOT_E - dh + 16))
        if t >= T_HEART:
            bbk = KIDLE[0].getbbox(); uh = t - T_HEART
            heart(img, kxe, KBOT_E - KIDLE[0].height + bbk[1] - 70 - min(uh, 0.4) * 30, int(255 * min(1, uh / 0.15)))
    img = shake(img, fo, T_LAND); img = shake(img, fo, T_KL, 18, 0.35)
    # top strip
    if t < T_FIN: strip(img, ['CAN YOU SPOT', 'THE FOUL?'], [(255, 255, 255), (255, 214, 60)], 64)
    elif t < T_WHIS: strip(img, ['CYRUS WINS!'], [COL['cyrus']], 68)
    elif t < T_FOUL: pass
    elif t < T_RWIN: strip(img, ['FALSE START!'], [(255, 90, 90)], 68)
    elif t < T_HEART: strip(img, ['RAYLEIGH WINS!'], [COL['ray']], 64)
    else: strip(img, ['DID YOU', 'SEE IT?'], [(255, 255, 255), (255, 214, 60)], 64)
    if STILLS: img.convert('RGB').save(OUTD + f'/st_{t:.2f}.png')
    else: out.stdin.write(img.convert('RGB').tobytes())
if STILLS: sys.exit()
out.stdin.close(); out.wait()
events = []
for g, s in st.items():
    for kind, t in s['events']:
        if kind == 'atk' and not (g in OUT_G and t >= T_LAND): events.append((t + PLANT + (HIT[g][0]) / ATK_FPS - 0.05, SFX[g]))
        if kind == 'kill': events.append((t, 'squish'))
        if kind == 'bonk': events.append((t, 'punch'))
events = [e for e in events if e[0] < T_FIN + 0.5]
events += [(0.0, 'tick_8bit'), (0.3, 'tick_8bit'), (0.6, 'tick_8bit'), (T_GO, 'go_8bit'),
           (T_LAND, 'punch'), (T_LAND + 0.02, 'squish'), (T_LAND + 0.05, 'stomp_8bit'),
           (T_FIN, 'ding_8bit'), (T_RAY, 'ding_8bit'), (T_POSE, 'cheer')]
events += [(T_REF + k * HOPD + HOPD, 'jump') for k in range(REF_HOPS)]
events += [(T_WHIS + 0.1, 'whistle'), (T_FOUL, 'punch'), (T_FOUL + 0.03, 'buzz_8bit'),
           (T_CROWN, 'whoosh_8bit'), (T_RWIN, 'victory'), (T_KL, 'stomp_8bit'), (T_KL + 0.02, 'squish'), (T_HEART, 'twinkle')]
events = [(round(a, 3), b) for a, b in events if 0 <= a < END_O - 0.1]
json.dump({'events': sorted(events), 'end': END_O,
           'beats': {'go': T_GO, 'false_start': T_FALSE, 'king_warn': T_WARN, 'king_land': T_LAND, 'cyrus_finish': T_FIN, 'ray_finish': T_RAY,
                     'referee': T_REF, 'whistle': T_WHIS, 'foul': T_FOUL, 'crown': T_CROWN, 'ray_wins': T_RWIN, 'king_shadow': T_KSH, 'king_land2': T_KL,
                     'heart': T_HEART, 'loop': T_LOOP}}, open(OUTD + '/n02_events.json', 'w'), indent=1)
print('done', round(END_O, 2), NOUT)
