import numpy as np, math, random, subprocess, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SPD = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SPD + 'pixellab/safezone'); from hook import hook_fade
sys.path.insert(0, SPD + 'fork_rc3'); from rc3 import acv_gummy_strong
# hook: the old 30px sub line is gone; the hook words run over two big lines, comment prompt is a real 44px+ band line from frame 0
# Oct 29 soft-fade pass: no box; 'gummy' back in the hook (so the apple-shaped ACV gummy needs no tag); comment line cut (caption asks)
HOOK, HBF = hook_fade(['Screenshot when', 'the gummy fits'], accent=1)
HOOK_END, _ = hook_fade(['How close', 'did you get?'], accent=1)   # last 1.4s: the hook itself turns into the question (no extra card)
print('fade hook bottom', HBF)
HB = 552   # old boxed-hook bottom: kept ONLY for the motion search so seed 4 finds the identical path (fit frame 198 unchanged)
R = '../../'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
W, H, FPS, DUR = 1080, 1920, 30, 10.0; N = int(round(DUR * FPS))
TAU = 2 * math.pi / DUR          # whole harmonics only -> the motion is periodic over the reel, last frame flows into frame 0
def F(s): return ImageFont.truetype(FONT, s)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
g = Image.open(A + 'found_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2 - 120, 0, 960 - cw // 2 - 120 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.8).convert('RGBA'))
K = 8
G0 = acv_gummy_strong(); G = G0.resize((G0.width * K, G0.height * K), Image.NEAREST)   # Syeda's ACV gummy + gummy shine (same silhouette)
PAD = 60; GP = Image.new('RGBA', (G.width + 2 * PAD, G.height + 2 * PAD)); GP.alpha_composite(G, (PAD, PAD))
al = np.array(GP.getchannel('A')) > 0
er = np.zeros_like(al); er[1:-1, 1:-1] = al[1:-1, 1:-1] & al[:-2, 1:-1] & al[2:, 1:-1] & al[1:-1, :-2] & al[1:-1, 2:]
edge = al & ~er
dil = edge.copy()
for dy in range(-3, 4):
    for dx in range(-3, 4): dil |= np.roll(np.roll(edge, dy, 0), dx, 1)
yy, xx = np.mgrid[0:al.shape[0], 0:al.shape[1]]
ang = np.arctan2(yy - al.shape[0] / 2, xx - al.shape[1] / 2)
dash = (np.floor((ang + math.pi) / (2 * math.pi) * 40) % 2) == 0
OUT = Image.fromarray((dil & dash).astype(np.uint8) * 255, 'L')
OUTGLOW = OUT.filter(ImageFilter.GaussianBlur(9))
TX, TY = W // 2, 1040
HW, HH = G.width // 2 + 12, G.height // 2 + 12
FM = 198   # 6.60s, the one fitting frame (same as before)
def path(p, t):
    x = p['A1'] * math.sin(p['w1'] * t + p['p1']) + p['A2'] * math.sin(p['w2'] * t + p['p2'])
    y = p['B1'] * math.sin(p['v1'] * t + p['q1']) + p['B2'] * math.sin(p['v2'] * t + p['q2'])
    a = p['R'] * math.sin(p['w3'] * t + p['p3']); s = 0.10 * math.sin(p['w4'] * t + p['p4'])
    return x, y, a, s
def miss(p, f, ref):
    x, y, a, s = path(p, f / FPS); x0, y0, a0, s0 = ref
    return abs(x - x0) + abs(y - y0) + 7 * abs(a - a0) + 400 * abs(s - s0)
def evalp(p):
    ref = path(p, FM / FPS); mins = 1e9; near = 0; nf = []
    for f in range(N):
        if f == FM: continue
        m = miss(p, f, ref); mins = min(mins, m)
        if m < 70: near += 1
        nf.append(m)
    return mins, near
def inside(p):
    x0, y0, a0, s0 = path(p, FM / FPS)
    for f in range(0, N, 2):
        x, y, a, s = path(p, f / FPS); x = TX + x - x0; y = TY + y - y0
        if y - HH < HB + 16 or y + HH > 1496 or x - HW < 72 or x + HW > 1022: return False
        if y + HH > 1110 and x + HW > 884: return False
    return True
def startok(p):
    # frame 0 must be a clear miss (thumbnail must not look like a fit)
    return miss(p, 0, path(p, FM / FPS)) > 150
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 4); best = None
for _ in range(int(os.environ.get('NT', '6000'))):
    p = dict(A1=rng.uniform(110, 190), A2=rng.uniform(25, 70), w1=TAU * rng.choice([2, 3, 4]), w2=TAU * rng.choice([5, 6, 7, 8]), p1=rng.uniform(0, 6.3), p2=rng.uniform(0, 6.3),
             B1=rng.uniform(110, 190), B2=rng.uniform(25, 70), v1=TAU * rng.choice([2, 3]), v2=TAU * rng.choice([5, 6, 7]), q1=rng.uniform(0, 6.3), q2=rng.uniform(0, 6.3),
             R=rng.uniform(14, 30), w3=TAU * rng.choice([2, 3, 4, 5]), p3=rng.uniform(0, 6.3), w4=TAU * rng.choice([2, 3, 4]), p4=rng.uniform(0, 6.3))
    if not inside(p) or not startok(p): continue
    mins, near = evalp(p)
    if mins < 22 or near < 3: continue
    sc_ = near + mins * 0.05
    if best is None or sc_ > best[0]: best = (sc_, p, mins, near)
_, P, MINS, NEAR = best; print('min miss', round(MINS, 1), 'near misses', NEAR, 'frame0 miss', round(miss(P, 0, path(P, FM / FPS)), 1))
X0, Y0, A0, S0 = path(P, FM / FPS)
def pose(t):
    x, y, a, s = path(P, t); return TX + x - X0, TY + y - Y0, a - A0, 1 + s - S0
jg = Image.open(A + 'idle_0.gif'); JOY = []
for i in range(jg.n_frames):
    jg.seek(i); f = jg.convert('RGBA').crop((260, 140, 730, 780)); JOY.append(f.resize((282, 384), Image.NEAREST))
rng2 = random.Random(2); MOTES = [(rng2.uniform(0, W), rng2.uniform(500, 1800), rng2.uniform(0, 6.3), TAU * rng2.choice([1, 2, 3])) for _ in range(40)]
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v30_noaudio.mp4'], stdin=subprocess.PIPE)
T_END = DUR - 1.4
events = [(0.0, 'twinkle'), (round(T_END, 3), 'ding_8bit')]
for f in range(N):
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    def rune(d):
        for k in range(3):
            r = 230 + k * 26
            d.ellipse([TX - r, TY - r * 0.42 + 190, TX + r, TY + r * 0.42 + 190], outline=(150, 230, 120, 70 - k * 18), width=4)
        for k in range(12):
            a = t * TAU + k * math.pi / 6; rx, ry = TX + 245 * math.cos(a), TY + 190 + 103 * math.sin(a)
            d.rectangle([rx - 5, ry - 5, rx + 5, ry + 5], fill=(190, 255, 150, 150))
    layer(img, rune)
    pulse = 0.6 + 0.4 * math.sin(t * TAU * 8)
    gl = Image.new('RGBA', OUT.size, (180, 255, 140, 0)); gl.putalpha(OUTGLOW.point(lambda v: int(v * 0.9 * pulse)))
    img.alpha_composite(gl, (TX - OUT.width // 2, TY - OUT.height // 2))
    ol = Image.new('RGBA', OUT.size, (255, 255, 255, 0)); ol.putalpha(OUT)
    img.alpha_composite(ol, (TX - OUT.width // 2, TY - OUT.height // 2))
    layer(img, lambda d: [d.rectangle([mx, my - 30 * math.sin(t * sp + ph), mx + 5, my + 5 - 30 * math.sin(t * sp + ph)], fill=(230, 255, 160, int(140 + 100 * math.sin(t * TAU * 5 + ph)))) for mx, my, ph, sp in MOTES])
    # gummy: moving from frame 0; trail from the periodic path (so it is identical across the loop point)
    x, y, a, s = pose(t)
    trail = [pose(t - (9 - i) / FPS)[:2] for i in range(10)]
    gi = GP.resize((int(GP.width * s), int(GP.height * s)), Image.NEAREST).rotate(a, resample=Image.NEAREST, expand=True)
    layer(img, lambda d: [d.rectangle([tx_ - 3 - i, ty_ - 3 - i, tx_ + 3 + i, ty_ + 3 + i], fill=(255, 200, 150, 20 + i * 14)) for i, (tx_, ty_) in enumerate(trail)])
    sh = Image.new('RGBA', (220, 50), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, 219, 49], fill=(0, 0, 0, 70))
    img.alpha_composite(sh, (int(x - 110), int(TY + 170)))
    img.alpha_composite(gi, (int(round(x - gi.width / 2)), int(round(y - gi.height / 2))))
    vf = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(vf, (72, 1492 - vf.height))
    img.alpha_composite(HOOK_END if t >= T_END else HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (FM - 1, FM, FM + 1): img.convert('RGB').crop((240, 700, 840, 1340)).save(f'm_{f - FM:+d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v30_events.json', 'w')); print('done match frame', FM)
