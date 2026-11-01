import numpy as np, glob, math, random, subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'
A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
S = 3
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
REF_W = load('../ref/ref_whistle'); REF_C = load('../ref/ref_cheer'); REF_I = load('../ref/ref_idle')
CROWN = Image.open('../ref/crown_cands/01.png').convert('RGBA'); CROWN = CROWN.crop(CROWN.getbbox()); CROWN = CROWN.resize((CROWN.width * S, CROWN.height * S), Image.NEAREST)
# ---------------- layout
TRACK_TOP, LANE_H, NL = 760, 220, 4
TRACK_BOT = TRACK_TOP + LANE_H * NL
FEET = [TRACK_TOP + LANE_H * i + LANE_H - 30 for i in range(NL)]
START_X = 300; FINISH_X = 6200
T = {i: Image.open(f'tiles/tile_{i}.png').convert('RGBA').resize((96, 96), Image.NEAREST) for i in range(16)}
GW = 8000
ground = Image.new('RGBA', (GW, H - 568), (0, 0, 0, 0))
for y in range(568, H, 96):
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
        ground.alpha_composite(tile, (x, y - 568))
gd = ImageDraw.Draw(ground)
for i in range(1, NL):
    y = TRACK_TOP + LANE_H * i - 568
    for x in range(0, GW, 48): gd.rectangle([x, y - 3, x + 28, y + 3], fill=(238, 230, 205, 230))
gd.rectangle([START_X - 6, TRACK_TOP - 568, START_X + 6, TRACK_BOT - 568], fill=(245, 245, 240, 255))
for j, y in enumerate(range(TRACK_TOP - 568, TRACK_BOT - 568, 20)):
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
                        s['state'] = 'sneak'; s['t0'] = t; s['sx0'] = live[0]['x'] - reach; s['sx1'] = live[0]['x'] + 70 * S
                        live[0]['skipped'] = True; s['sneak'] = t; s['x'] = s['sx0']
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
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(600):
        r = score(seed)
        if r and r[1] >= 4: print(seed, r)
    sys.exit()
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
st, TL = run_sim(SEED)
T_WIN = st['cyrus']['fin']; T_RAY = st['ray']['fin']; T_CH = st['cyrus']['sneak']
print('cyrus', round(T_WIN, 2), 'ray', round(T_RAY, 2), 'cheat at', round(T_CH, 2))
KIDLE = load('../king/king2_idle'); KLAND = load('../king/king2_land')
KO = {g: load(f'../king/{g}_ko') for g in OUT_G}
DUST = Image.open('../king/dust_cands/00.png').convert('RGBA'); DUST = DUST.crop(DUST.getbbox())
li0 = int(T_LAND * FPS)
KX = (TL[li0]['cleo'][0] + TL[li0]['joy'][0]) / 2 + 46 * S
K_BOT = FEET[2] + 18
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
# ---------------- world render (live)
CAM = []
cam = 0.0
for f in range(int(DUR * FPS)):
    t = f / FPS; snap = TL[f]
    lead_x = max(v[0] for k, v in snap.items() if not (k in OUT_G and t >= T_LAND))
    target_cam = max(0, min(FINISH_X + 420 - W, lead_x - 520))
    cam += (target_cam - cam) * 0.12; CAM.append(cam)
POS = {}
def world(f, skip=()):
    t = f / FPS; snap = TL[f]; cam = CAM[f]
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    hb = HUBF[int(t * 6) % len(HUBF)]; px = int(cam * 0.35) % 1067
    img.paste(hb.crop((px, 0, px + W, 600)), (0, 0))
    img.alpha_composite(ground.crop((int(cam), 0, int(cam) + W, H - 568)), (0, 568))
    fx = FINISH_X - int(cam) - FIN.width // 2
    if -FIN.width < fx < W: img.alpha_composite(FIN, (fx, TRACK_TOP - FIN.height + 60))
    kx = int(KX - cam)
    if T_WARN <= t < T_LAND + 0.05:
        u = (t - T_WARN) / (T_LAND - T_WARN); sw = int(60 + 300 * u)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([kx - sw // 2, K_BOT - sw // 7, kx + sw // 2, K_BOT + sw // 7], fill=(0, 0, 0, int(70 + 80 * u)))
        img.alpha_composite(sh)
    flyers = []
    for gname in G:
        s = st[gname]; li = s['lane']; x, state, t0 = snap[gname]; feet = FEET[li]
        for sl in s['slimes']:
            sx = int(sl['x'] - cam) - 32 * S
            if sx < -200 or sx > W + 200: continue
            if sl['dead_t'] is None or t < sl['dead_t']:
                fr = SL_IDLE[int(t * 10 + sl['x']) % len(SL_IDLE)]; img.alpha_composite(fr, (sx, feet - 62 * S))
            else:
                k = int((t - sl['dead_t']) * 16)
                if k < len(SL_SPLAT): img.alpha_composite(SL_SPLAT[k], (sx, feet - 62 * S))
        rx = int(x - cam)
        POS[(f, gname)] = (rx + 46 * S, feet - 40 * S)
        if gname in skip: continue
        if state == 'out':
            u = t - T_LAND; ox = s['out_x'] - cam - 18 * S - 320 * u; oy = feet - 78 * S - 18 * S - (1900 * u - 450 * u * u)
            fr = KO[gname][3 + int(u * 18) % 6]
            if oy > -400: flyers.append((fr, (int(ox), int(oy))))
            continue
        if t < T_GO: img.alpha_composite(RUN[gname][0], (rx, feet - 78 * S))
        elif state == 'atk':
            k = min(11, int((t - t0) * ATK_FPS)); img.alpha_composite(ATK[gname][k], (rx - 14 * S, feet - 78 * S - 26 * S))
        elif state == 'sneak':
            u = min(1, (t - t0) / SNEAK); dy = int(-150 * math.sin(math.pi * u))
            fr = RUN[gname][int(t * 18) % len(RUN[gname])]; img.alpha_composite(fr, (rx, feet - 78 * S + dy))
            POS[(f, gname)] = (rx + 46 * S, feet - 40 * S + dy)
        elif state == 'stop' and gname in IDLE:
            img.alpha_composite(IDLE[gname][int(t * 8) % len(IDLE[gname])], (rx, feet - 78 * S))
        else:
            img.alpha_composite(RUN[gname][int(t * 14) % len(RUN[gname])], (rx, feet - 78 * S))
    if t >= T_LAND - 0.32:
        if t < T_LAND:
            u = (t - (T_LAND - 0.32)) / 0.32; fr = KIDLE[0]; ky = int(-fr.height + (K_BOT - 4 * S) * u * u)
            img.alpha_composite(fr, (kx - fr.width // 2, ky))
        else:
            u = t - T_LAND; k = int(u * 15)
            fr = KLAND[k] if k < len(KLAND) else KIDLE[int(u * 10) % len(KIDLE)]
            img.alpha_composite(fr, (kx - fr.width // 2, K_BOT - fr.height))
            if u < 0.7:
                sc = 1.0 + 0.9 * u; dw, dh = int(DUST.width * 3 * sc), int(DUST.height * 3 * sc)
                du = DUST.resize((dw, dh), Image.NEAREST); al = du.getchannel('A').point(lambda p: int(p * max(0, 1 - u / 0.7)))
                du.putalpha(al); img.alpha_composite(du, (kx - dw // 2, K_BOT - dh + 20))
    for fr_, pos_ in flyers: img.alpha_composite(fr_, pos_)
    if T_LAND <= t < T_LAND + 0.5:
        amp = int(26 * (1 - (t - T_LAND) / 0.5)); rs = random.Random(f)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 255)); sh.paste(img, (rs.randint(-amp, amp), rs.randint(-amp, amp))); img = sh
    return img
def header(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 330], fill=(18, 14, 32, 205))
    ctext(d, W / 2, 80, 'CHOOSE YOUR', F(70)); ctext(d, W / 2, 175, 'GUIDE!', F(86), (255, 214, 60))
    ctext(d, W / 2, 280, 'Slay the slimes. First to finish wins', F(26))
    return d
def live_overlays(img, f):
    t = f / FPS; d = header(img)
    if t < T_GO + 1.2:
        a = 1 if t < T_GO else max(0, 1 - (t - T_GO) / 1.2)
        for gname in G:
            li = st[gname]['lane']; y = TRACK_TOP + LANE_H * li + 22
            tag = NAMES[gname]; w = d.textlength(tag, font=F(26))
            d.rectangle([W - w - 60, y, W - 24, y + 50], fill=(20, 15, 35, int(220 * a)))
            d.text((W - w - 42, y + 12), tag, font=F(26), fill=COL[gname] + (int(255 * a),))
    if 0.9 <= t < T_GO + 0.5:
        u = t - 0.9; n = 3 - int(u / 0.63); txt = str(n) if n > 0 else 'GO!'
        sc = 1.25 - 0.25 * ((u % 0.63) / 0.63) if n > 0 else 1.0
        fs = int(170 * sc); ctext(d, W / 2, 470 - fs // 2, txt, F(fs), (255, 214, 60) if n > 0 else (120, 230, 90), 10)
    if T_WARN <= t < T_LAND + 1.4 and int(t * 6) % 2 == 0:
        ctext(d, W / 2, 400, 'KING SLIME!', F(86), (255, 196, 40), 10)
    if T_LAND + 0.4 <= t < T_LAND + 3.2:
        for gname in OUT_G:
            li = st[gname]['lane']; y = TRACK_TOP + LANE_H * li + 70
            tag = NAMES[gname] + ' OUT!'; w = d.textlength(tag, font=F(40))
            d.rectangle([20, y, w + 70, y + 70], fill=(150, 20, 30, 230)); d.text((45, y + 15), tag, font=F(40), fill=(255, 255, 255))
    return d
def banner(img, who, text, u, col):
    d = ImageDraw.Draw(img); a = min(1, u / 0.25)
    d.rectangle([0, 1650, W, 1920], fill=(18, 14, 32, int(225 * a)))
    vf = VIC[who][int(u * 8) % len(VIC[who])]
    img.alpha_composite(vf, (40, 1650 + 270 - vf.height + 10))
    d = ImageDraw.Draw(img); ctext(d, W / 2 + 120, 1755, text, F(54), col, 8)
# ---------------- timeline
T_REF = T_WIN + 1.5            # referee steps in
T_LIVE_END = T_REF + 1.6       # whistle + point done
RP0, RP1 = T_CH - 0.5, T_CH + SNEAK + 0.5   # replay window (live time)
RP_SPEED = 0.5
out = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v3_noaudio.mp4'], stdin=subprocess.PIPE)
def emit(img): out.stdin.write(img.convert('RGB').tobytes())
events = []
REF_X = W // 2 - 64 * S; REF_Y = FEET[1] + 10 - 112 * S
cache = {}
NLIVE = int(T_LIVE_END * FPS)
for f in range(NLIVE):
    t = f / FPS
    w_ = world(f)
    if int(RP0 * FPS) - 2 <= f <= int(RP1 * FPS) + 2: cache[f] = w_.copy()
    img = w_
    if t >= T_REF:
        u = t - T_REF
        if u < 0.25:   # ref pops in from below with a hop
            yy = REF_Y + int((1 - u / 0.25) * 500)
            img.alpha_composite(REF_I[0], (REF_X, yy))
        else:
            k = min(len(REF_W) - 1, int((u - 0.25) * 10)); img.alpha_composite(REF_W[k], (REF_X, REF_Y))
            if 0.3 < u < 1.1:
                d = ImageDraw.Draw(img); ctext(d, REF_X + 64 * S, REF_Y - 10, 'TWEEEET!', F(48), (255, 255, 255), 8)
    d = live_overlays(img, f)
    if T_WIN <= t < T_REF + 0.25:
        banner(img, 'cyrus', 'CYRUS WINS!', t - T_WIN, COL['cyrus'])
    if t >= T_REF + 1.0:
        d = ImageDraw.Draw(img); d.rectangle([0, 1650, W, 1920], fill=(18, 14, 32, 225))
        ctext(d, W / 2, 1735, 'HOLD ON...', F(64), (255, 255, 255), 8)
    emit(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev3/p_{f:04d}.png')
last_clean = world(NLIVE - 1)
last_noray = world(NLIVE - 1, skip=('ray',))
# ---------------- rewind flicker (0.5s) then replay
def vhs(img, tt, label=True):
    im = img.convert('RGB'); im = ImageEnhance.Color(im).enhance(0.75); im = ImageEnhance.Brightness(im).enhance(0.9)
    a = np.array(im); a[::4] = (a[::4] * 0.7).astype(np.uint8); im = Image.fromarray(a).convert('RGBA')
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 170], fill=(10, 8, 18, 230))
    if int(tt * 2.5) % 2 == 0: d.ellipse([50, 62, 100, 112], fill=(230, 40, 40))
    d.text((125, 62), 'INSTANT REPLAY', font=F(50), fill=(255, 255, 255), stroke_width=4, stroke_fill=(20, 15, 35))
    return im
def zoomed(f, z):
    img = cache[f]; cx, cy = POS[(f, 'cyrus')]
    cw, ch = W / z, H / z
    x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2 + 60, 0), H - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.NEAREST)
fr_list = sorted(cache.keys())
# rewind: play cache backwards fast from the live end
n_rw = 15
for i in range(n_rw):
    base = last_clean if i < 3 else cache[fr_list[int((1 - i / (n_rw - 1)) * (len(fr_list) - 1))]]
    im = vhs(base, i / FPS); d = ImageDraw.Draw(im); ctext(d, W / 2, 880, '<< REWIND', F(70), (255, 255, 255), 8)
    a = np.array(im.convert('RGB')); sh = np.random.RandomState(i).randint(-30, 30); a = np.roll(a, sh, axis=1); emit(Image.fromarray(a))
events.append((T_LIVE_END, 'rewind'))
# replay at half speed with zoom ramp 1 -> 2.2
n_rp = int((RP1 - RP0) / RP_SPEED * FPS)
f0 = int(RP0 * FPS)
for i in range(n_rp):
    lt = RP0 + i / FPS * RP_SPEED; f = min(max(f0, int(lt * FPS)), max(fr_list))
    z = 1 + 1.2 * min(1, i / (0.8 * FPS))
    im = vhs(zoomed(f, z), i / FPS)
    d = ImageDraw.Draw(im)
    ctext(d, W / 2, 1720, 'WATCH CYRUS...', F(52), (255, 214, 60), 8)
    emit(im)
# freeze on the skip + FOUL stamp
fz = min(int((T_CH + SNEAK * 0.5) * FPS), max(fr_list))
for i in range(int(1.6 * FPS)):
    im = vhs(zoomed(fz, 2.2), 99)
    st_ = Image.new('RGBA', (900, 260), (0, 0, 0, 0)); sd = ImageDraw.Draw(st_)
    sd.rounded_rectangle([10, 10, 890, 250], 30, outline=(230, 40, 40), width=16)
    tw = sd.textlength('FOUL!', font=F(120)); sd.text(((900 - tw) / 2, 70), 'FOUL!', font=F(120), fill=(230, 40, 40))
    sc = max(1.0, 1.8 - i / 4); st2 = st_.rotate(-8, expand=True, resample=Image.NEAREST); st2 = st2.resize((int(st2.width * sc), int(st2.height * sc)), Image.NEAREST)
    im.alpha_composite(st2, (W // 2 - st2.width // 2, 760 - st2.height // 2))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 1640, W, 1840], fill=(18, 14, 32, 230))
    ctext(d, W / 2, 1680, 'He skipped a slime!', F(46), (255, 255, 255), 6)
    emit(im)
    if i == 0: events.append((T_LIVE_END + n_rw / FPS + n_rp / FPS, 'punch'))
t_after = T_LIVE_END + (n_rw + n_rp) / FPS + 1.6
# ---------------- verdict: Cyrus DQ, ref crowns Rayleigh
ray_x, ray_y = POS[(NLIVE - 1, 'ray')]; cy_x, cy_y = POS[(NLIVE - 1, 'cyrus')]
RAY_ORG = (ray_x - 46 * S, FEET[3] - 78 * S); CY_ORG = (cy_x - 46 * S, FEET[0] - 78 * S)
NV = int(3.8 * FPS)
for i in range(NV):
    u = i / FPS
    img = (last_clean if u < 0.9 + 0.9 else last_noray).copy()
    # cover Rayleigh's live sprite with victory pose
    d = ImageDraw.Draw(img)
    if u < 0.9:
        k = 7 + min(4, int(u * 10)); img.alpha_composite(REF_W[k], (REF_X, REF_Y))
        d = ImageDraw.Draw(img); tag = 'DISQUALIFIED'; w = d.textlength(tag, font=F(34))
        d.rectangle([CY_ORG[0] + 46 * S - w / 2 - 20, CY_ORG[1] - 70, CY_ORG[0] + 46 * S + w / 2 + 20, CY_ORG[1] - 14], fill=(150, 20, 30, 235))
        d.text((CY_ORG[0] + 46 * S - w / 2, CY_ORG[1] - 58), tag, font=F(34), fill=(255, 255, 255))
    else:
        k = min(len(REF_C) - 1, int((u - 0.9) * 10)); img.alpha_composite(REF_C[k] if u > 2.0 else REF_I[int(u * 8) % len(REF_I)], (REF_X, REF_Y))
        d = ImageDraw.Draw(img); tag = 'DISQUALIFIED'; w = d.textlength(tag, font=F(34))
        d.rectangle([CY_ORG[0] + 46 * S - w / 2 - 20, CY_ORG[1] - 70, CY_ORG[0] + 46 * S + w / 2 + 20, CY_ORG[1] - 14], fill=(150, 20, 30, 235))
        d.text((CY_ORG[0] + 46 * S - w / 2, CY_ORG[1] - 58), tag, font=F(34), fill=(255, 255, 255))
    # crown flight from ref hands to Rayleigh's head
    head = (RAY_ORG[0] + 46 * S - CROWN.width // 2, RAY_ORG[1] + 4 * S - CROWN.height + 10)
    src = (REF_X + 64 * S - CROWN.width // 2, REF_Y + 20 * S)
    if 0.9 <= u:
        p = min(1, (u - 0.9) / 0.9); e = p * p * (3 - 2 * p)
        cx = src[0] + (head[0] - src[0]) * e; cyy = src[1] + (head[1] - src[1]) * e - 260 * math.sin(math.pi * e)
        if p >= 1:
            # Rayleigh victory pose with crown
            bg = Image.new('RGBA', (92 * S, 92 * S), (0, 0, 0, 0))
            vf = VIC['ray'][int(u * 8) % len(VIC['ray'])]
            img.alpha_composite(vf, RAY_ORG)
            cyy = head[1] + int(3 * math.sin(u * 8))
            for k2 in range(6):
                ang = u * 3 + k2; r = 150
                sx_, sy_ = RAY_ORG[0] + 46 * S + math.cos(ang) * r, RAY_ORG[1] + 30 * S + math.sin(ang) * r * 0.6
                d = ImageDraw.Draw(img); d.rectangle([sx_ - 6, sy_ - 6, sx_ + 6, sy_ + 6], fill=(255, 230, 120)); d.rectangle([sx_ - 14, sy_ - 2, sx_ + 14, sy_ + 2], fill=(255, 245, 190)); d.rectangle([sx_ - 2, sy_ - 14, sx_ + 2, sy_ + 14], fill=(255, 245, 190))
        img.alpha_composite(CROWN, (int(cx), int(cyy)))
    header(img)
    if u >= 1.8:
        banner(img, 'ray', 'RAYLEIGH WINS!', u - 1.8, COL['ray'])
    emit(img)
    if i == int(0.1 * FPS): events.append((t_after + 0.1, 'vg02'))
    if i == int(1.8 * FPS): events.append((t_after + 1.8, 'vg02'))
out.stdin.close(); out.wait()
END = t_after + NV / FPS
for gname, s in st.items():
    for kind, t in s['events']:
        if t < T_LIVE_END:
            if kind == 'atk': events.append((round(t + HIT[gname][0] / ATK_FPS * 0.6, 3), SFX[gname]))
            if kind == 'kill': events.append((round(t, 3), 'squish'))
            if kind == 'bonk': events.append((round(t, 3), 'punch'))
events += [(T_LAND, 'punch'), (T_LAND + 0.02, 'squish'), (T_LAND + 0.05, 'punch'), (T_REF + 0.3, 'whistle'), (T_REF + 0.55, 'whistle')]
# replayed hit sounds are omitted on purpose; the replay is silent except music
json.dump({'events': [(round(a, 3), b) for a, b in events], 'end': END}, open('v3_events.json', 'w'))
print('done', round(END, 2))
