import numpy as np, glob, math, random, subprocess, json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'
A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
S = 3                                   # pixel scale for sprites and tiles
def F(s): return ImageFont.truetype(FONT, s)
def load(d, scale=S):
    fr = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(d + '/*.png'))]
    return [f.resize((f.width * scale, f.height * scale), Image.NEAREST) for f in fr]
SLIME_IDLE_DIR = sys.argv[1] if len(sys.argv) > 1 else 'slime_idle2'
DUSTPICK = os.environ.get('DUSTPICK', '00')
G = ['cyrus', 'cleo', 'joy', 'ray']
NAMES = {'cyrus': 'CYRUS', 'cleo': 'CLEO', 'joy': 'JOY', 'ray': 'RAYLEIGH'}
COL = {'cyrus': (255, 176, 40), 'cleo': (120, 170, 255), 'joy': (120, 220, 90), 'ray': (200, 110, 255)}
RUN = {g: load(f'{g}_run')[1:] for g in G}          # drop duplicate first frame of loop
ATK = {g: load(f'{g}_atk') for g in G}
# contact frame and contact x (in attack-canvas native px) per guide
HIT = {'joy': (4, 100), 'ray': (5, 102), 'cleo': (4, 66), 'cyrus': (3, 84)}
SFX = {'joy': 'vg02', 'ray': 'vg02', 'cleo': 'swish', 'cyrus': 'punch'}
SL_IDLE = load(SLIME_IDLE_DIR); SL_SPLAT = load('slime_splat')
VIC = {'cyrus': 'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', 'cleo': 'vic_victoryPose.gif',
       'joy': 'vic_Victory_Pose.gif', 'ray': 'vic_victoryPose_1.gif'}
def gif(p, h):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
# ---------------- layout
TRACK_TOP, LANE_H, NL = 760, 220, 4
TRACK_BOT = TRACK_TOP + LANE_H * NL               # 1536
FEET = [TRACK_TOP + LANE_H * i + LANE_H - 30 for i in range(NL)]
START_X = 300; FINISH_X = 6200
# ---------------- ground (tiles 32 -> 64 px)
T = {i: Image.open(f'tiles/tile_{i}.png').convert('RGBA').resize((96, 96), Image.NEAREST) for i in range(16)}
GW = 8000
ground = Image.new('RGBA', (GW, H - 568), (0, 0, 0, 0))
rows = list(range(568, H, 96))
rng0 = random.Random(7)
for r, y in enumerate(rows):
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
# lane lines (chalk) and start / finish
for i in range(1, NL):
    y = TRACK_TOP + LANE_H * i - 568
    for x in range(0, GW, 48): gd.rectangle([x, y - 3, x + 28, y + 3], fill=(238, 230, 205, 230))
gd.rectangle([START_X - 6, TRACK_TOP - 568, START_X + 6, TRACK_BOT - 568], fill=(245, 245, 240, 255))
for j, y in enumerate(range(TRACK_TOP - 568, TRACK_BOT - 568, 20)):
    for k in range(3):
        c = (20, 20, 24, 255) if (j + k) % 2 == 0 else (245, 245, 245, 255)
        gd.rectangle([FINISH_X + k * 20 - 30, y, FINISH_X + k * 20 - 11, y + 19], fill=c)
ground = ground
# ---------------- village backdrop (Liza hub, mirrored tiling, parallax)
g = Image.open(A + 'hub.gif'); HUBF = []
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').resize((1067, 600), Image.NEAREST)
    strip = Image.new('RGB', (1067 * 2, 600)); strip.paste(f, (0, 0)); strip.paste(f.transpose(Image.FLIP_LEFT_RIGHT), (1067, 0))
    HUBF.append(strip)
FIN = Image.open('finish_cands/00.png').convert('RGBA'); FIN = FIN.crop(FIN.getbbox()); FIN = FIN.resize((FIN.width * 3, FIN.height * 3), Image.NEAREST)
# ---------------- simulation
def simulate(seed):
    rnd = random.Random(seed)
    st = {}
    for li, gname in enumerate(G):
        sl = sorted(rnd.uniform(1200, FINISH_X - 700) for _ in range(3))
        while min(b - a for a, b in zip(sl, sl[1:])) < 950: sl = sorted(rnd.uniform(1200, FINISH_X - 700) for _ in range(3))
        st[gname] = dict(lane=li, x=float(START_X - 150), slimes=[dict(x=s, hp=rnd.choice([1, 1, 1, 2]), dead_t=None) for s in sl],
                         v=rnd.uniform(440, 490), ph=rnd.uniform(0, 6.28), state='run', t0=0, target=None, fin=None, events=[])
    return st
T_GO = 2.8; DUR = 23.0
OUT_G = ['cleo', 'joy']; T_WARN = 4.7; T_LAND = 5.8
ATK_FPS = 18; ATK_LEN = 12 / ATK_FPS
def run_sim(seed):
    st = simulate(seed); timeline = []
    dt = 1 / FPS
    for f in range(int(DUR * FPS)):
        t = f / FPS
        for gname, s in st.items():
            if t < T_GO: continue
            if s['state'] == 'out': continue
            if t >= T_LAND and gname in OUT_G:
                s['state'] = 'out'; s['out_x'] = s['x']; s['t0'] = T_LAND; continue
            if s['state'] == 'run':
                v = s['v'] * (1 + 0.10 * math.sin(1.3 * t + s['ph']) + 0.05 * math.sin(3.1 * t + 2 * s['ph']))
                nx = s['x'] + v * dt
                live = [sl for sl in s['slimes'] if sl['dead_t'] is None]
                hf, hx = HIT[gname]; reach = (hx + 14) * S
                if live and nx + reach >= live[0]['x']:
                    s['x'] = live[0]['x'] - reach; s['state'] = 'atk'; s['t0'] = t; s['target'] = live[0]
                    s['events'].append(('atk', t))
                else:
                    s['x'] = nx
                if s['fin'] is None and s['x'] + 46 * S >= FINISH_X: s['fin'] = t
            elif s['state'] == 'atk':
                u = t - s['t0']; hf, hx = HIT[gname]
                if u >= hf / ATK_FPS and not s.get('hitdone'):
                    s['hitdone'] = True; s['target']['hp'] -= 1
                    if s['target']['hp'] <= 0: s['target']['dead_t'] = t; s['events'].append(('kill', t))
                    else: s['events'].append(('bonk', t))
                if u >= ATK_LEN:
                    s['hitdone'] = False
                    s['state'] = 'run' if s['target']['dead_t'] is not None else 'atk'
                    s['t0'] = t
        timeline.append({k: (v['x'], v['state'], v['t0']) for k, v in st.items()})
    return st, timeline
def score(seed):
    st, tl = run_sim(seed)
    li = int(T_LAND * FPS)
    if abs(tl[li]['cleo'][0] - tl[li]['joy'][0]) > 220: return None
    fins = sorted((s['fin'] if s['fin'] else 99, g) for g, s in st.items() if g not in OUT_G)
    if fins[0][0] > 19.5 or fins[0][0] < 17: return None
    margin = fins[1][0] - fins[0][0]
    leaders = []
    for i in range(int(T_GO * FPS), int(fins[0][0] * FPS), 15):
        L = max([k for k in tl[i] if k not in OUT_G or i < li], key=lambda k: tl[i][k][0])
        if not leaders or leaders[-1] != L: leaders.append(L)
    return margin, len(leaders), fins[0][1], leaders
if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'search':
    out = []
    for seed in range(400):
        r = score(seed)
        if r and r[0] < 0.4 and r[1] >= 4: out.append((seed, r))
    for o in out[:40]: print(o)
    sys.exit()
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0
st, TL = run_sim(SEED)
fins = sorted((s['fin'] if s['fin'] else 99, g) for g, s in st.items() if g not in OUT_G)
WIN = fins[0][1]; T_WIN = fins[0][0]
print('winner', WIN, 'at', round(T_WIN, 2), 'margin', round(fins[1][0] - T_WIN, 2))
END = min(DUR, T_WIN + 3.6)
VICF = gif(VIC[WIN], 240)
KO = {g: load(f'../king/{g}_ko') for g in OUT_G}
KIDLE = load('../king/king_idle'); KLAND = load('../king/king_land')
DUST = Image.open('../king/dust_cands/%s.png' % DUSTPICK).convert('RGBA'); DUST = DUST.crop(DUST.getbbox())
li0 = int(T_LAND * FPS)
KX = (TL[li0]['cleo'][0] + TL[li0]['joy'][0]) / 2 + 46 * S
K_BOT = FEET[2] + 18

# ---------------- render
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'king_noaudio.mp4'], stdin=subprocess.PIPE)
events = []
cam = 0.0
for f in range(int(END * FPS)):
    t = f / FPS; snap = TL[f]
    lead_x = max(v[0] for k, v in snap.items() if not (k in OUT_G and t >= T_LAND))
    target_cam = max(0, min(FINISH_X + 420 - W, lead_x - 520))
    cam += (target_cam - cam) * 0.12
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    hb = HUBF[int(t * 6) % len(HUBF)]; px = int(cam * 0.35) % 1067
    img.paste(hb.crop((px, 0, px + W, 600)), (0, 0))
    img.alpha_composite(ground.crop((int(cam), 0, int(cam) + W, H - 568)), (0, 568))
    # finish arch behind lane 1
    fx = FINISH_X - int(cam) - FIN.width // 2
    if -FIN.width < fx < W: img.alpha_composite(FIN, (fx, TRACK_TOP - FIN.height + 60))
    # king shadow
    kx = int(KX - cam)
    if T_WARN <= t < T_LAND + 0.05:
        u = (t - T_WARN) / (T_LAND - T_WARN); sw = int(60 + 300 * u)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([kx - sw // 2, K_BOT - sw // 7, kx + sw // 2, K_BOT + sw // 7], fill=(0, 0, 0, int(70 + 80 * u)))
        img.alpha_composite(sh)
    flyers = []
    # draw lanes back to front
    for gname in G:
        s = st[gname]; li = s['lane']; x, state, t0 = snap[gname]; feet = FEET[li]
        # slimes
        for sl in s['slimes']:
            sx = int(sl['x'] - cam) - 32 * S
            if sx < -200 or sx > W + 200: continue
            if sl['dead_t'] is None or t < sl['dead_t']:
                fr = SL_IDLE[int(t * 10 + sl['x']) % len(SL_IDLE)]
                img.alpha_composite(fr, (sx, feet - 62 * S))
            else:
                k = int((t - sl['dead_t']) * 16)
                if k < len(SL_SPLAT): img.alpha_composite(SL_SPLAT[k], (sx, feet - 62 * S))
        # guide
        rx = int(x - cam)
        if state == 'out':
            u = t - T_LAND; ox = s['out_x'] - cam - 18 * S - 320 * u; oy = feet - 78 * S - 18 * S - (1900 * u - 450 * u * u)
            fr = KO[gname][3 + int(u * 18) % 6]
            if oy > -400: flyers.append((fr, (int(ox), int(oy))))
            continue
        if t < T_GO:
            fr = RUN[gname][0]; img.alpha_composite(fr, (rx, feet - 78 * S))
        elif state == 'atk':
            k = min(11, int((t - t0) * ATK_FPS)); fr = ATK[gname][k]
            img.alpha_composite(fr, (rx - 14 * S, feet - 78 * S - 26 * S))
        else:
            if s['fin'] is not None and t > s['fin'] + 0.6 and gname == WIN:
                pass
            fr = RUN[gname][int(t * 14) % len(RUN[gname])]; img.alpha_composite(fr, (rx, feet - 78 * S))
    # king slime
    if t >= T_LAND - 0.32:
        if t < T_LAND:
            u = (t - (T_LAND - 0.32)) / 0.32; fr = KIDLE[0]; ky = int(-fr.height + (K_BOT - 4 * S) * u * u)
            img.alpha_composite(fr, (kx - fr.width // 2, ky - fr.height + fr.height))
        else:
            u = t - T_LAND; k = int(u * 15)
            fr = KLAND[k] if k < len(KLAND) else KIDLE[int(u * 10) % len(KIDLE)]
            img.alpha_composite(fr, (kx - fr.width // 2, K_BOT - fr.height))
            if u < 0.7:
                sc = 1.0 + 0.9 * u; dw, dh = int(DUST.width * 3 * sc), int(DUST.height * 3 * sc)
                du = DUST.resize((dw, dh), Image.NEAREST); al = du.getchannel('A').point(lambda p: int(p * max(0, 1 - u / 0.7)))
                du.putalpha(al); img.alpha_composite(du, (kx - dw // 2, K_BOT - dh + 20))
    for fr_, pos_ in flyers: img.alpha_composite(fr_, pos_)
    # screen shake
    if T_LAND <= t < T_LAND + 0.5:
        amp = int(26 * (1 - (t - T_LAND) / 0.5)); rs = random.Random(f)
        dx, dy = rs.randint(-amp, amp), rs.randint(-amp, amp)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 255)); sh.paste(img, (dx, dy)); img = sh
    d = ImageDraw.Draw(img)
    # header panel
    d.rectangle([0, 0, W, 330], fill=(18, 14, 32, 205))
    ctext(d, W / 2, 80, 'CHOOSE YOUR', F(70)); ctext(d, W / 2, 175, 'GUIDE!', F(86), (255, 214, 60))
    ctext(d, W / 2, 280, 'Slay the slimes. First to finish wins', F(26))
    # lane name tags on the left during intro
    if t < T_GO + 1.2:
        a = 1 if t < T_GO else max(0, 1 - (t - T_GO) / 1.2)
        for gname in G:
            li = st[gname]['lane']; y = TRACK_TOP + LANE_H * li + 22
            tag = NAMES[gname]; w = d.textlength(tag, font=F(26))
            d.rectangle([W - w - 60, y, W - 24, y + 50], fill=(20, 15, 35, int(220 * a)))
            d.text((W - w - 42, y + 12), tag, font=F(26), fill=COL[gname] + (int(255 * a),))
    # countdown
    if 0.9 <= t < T_GO + 0.5:
        u = t - 0.9; n = 3 - int(u / 0.63)
        txt = str(n) if n > 0 else 'GO!'
        sc = 1.25 - 0.25 * ((u % 0.63) / 0.63) if n > 0 else 1.0
        fs = int(170 * sc); ctext(d, W / 2, 470 - fs // 2, txt, F(fs), (255, 214, 60) if n > 0 else (120, 230, 90), 10)
    # king banner and OUT tags
    if T_WARN <= t < T_LAND + 1.4 and int(t * 6) % 2 == 0:
        ctext(d, W / 2, 400, 'KING SLIME!', F(86), (255, 70, 70), 10)
    if T_LAND + 0.4 <= t < T_LAND + 3.2:
        for gname in OUT_G:
            li = st[gname]['lane']; y = TRACK_TOP + LANE_H * li + 70
            tag = NAMES[gname] + ' OUT!'; w = d.textlength(tag, font=F(40))
            d.rectangle([W - w - 70, y, W - 20, y + 70], fill=(150, 20, 30, 230))
            d.text((W - w - 45, y + 15), tag, font=F(40), fill=(255, 255, 255))
    # winner banner
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.25)
        d.rectangle([0, 1650, W, 1920], fill=(18, 14, 32, int(225 * a)))
        vf = VICF[int(u * 8) % len(VICF)]
        img.alpha_composite(vf, (90, 1650 + (270 - vf.height) // 2))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2 + 120, 1755, NAMES[WIN] + ' WINS!', F(54), COL[WIN], 8)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prevk/p_{f:04d}.png')
ff.stdin.close(); ff.wait()
ev = []
for gname, s in st.items():
    for kind, t in s['events']:
        if t < END:
            if kind == 'atk': ev.append((round(t + HIT[gname][0] / ATK_FPS * 0.6, 3), SFX[gname]))
            if kind == 'kill': ev.append((round(t, 3), 'squish'))
            if kind == 'bonk': ev.append((round(t, 3), 'punch'))
ev.append((round(T_LAND, 3), 'punch')); ev.append((round(T_LAND + 0.02, 3), 'squish')); ev.append((round(T_LAND + 0.05, 3), 'punch'))
json.dump({'events': ev, 'end': END, 'winner': WIN, 't_win': T_WIN}, open('king_events.json', 'w'))
print('done', END)
