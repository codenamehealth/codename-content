import numpy as np, math, random, subprocess, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['SCREENSHOT', 'THE SECOND'], accent=0, sub='THE GUMMY FITS PERFECTLY')
print('hook bottom', HB)
R = '../../'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
W, H, FPS, DUR = 1080, 1920, 30, 11.0; N = int(DUR * FPS)
def F(s): return ImageFont.truetype(FONT, s)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
# background: Liza's Foundation forest (Joy's realm)
g = Image.open(A + 'found_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2 - 120, 0, 960 - cw // 2 - 120 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.8).convert('RGBA'))
# gummy
K = 8
G0 = Image.open(R + 'pixellab/gummies/pick_acv.png').convert('RGBA'); G = G0.resize((G0.width * K, G0.height * K), Image.NEAREST)
PAD = 60; GP = Image.new('RGBA', (G.width + 2 * PAD, G.height + 2 * PAD)); GP.alpha_composite(G, (PAD, PAD))
# outline from the gummy silhouette (dashed, glowing)
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
TX, TY = W // 2, 1020        # target centre
HW, HH = G.width // 2 + 12, G.height // 2 + 12
FM = int(6.6 * FPS)
def path(p, t):
    x = p['A1'] * math.sin(p['w1'] * t + p['p1']) + p['A2'] * math.sin(p['w2'] * t + p['p2'])
    y = p['B1'] * math.sin(p['v1'] * t + p['q1']) + p['B2'] * math.sin(p['v2'] * t + p['q2'])
    a = p['R'] * math.sin(p['w3'] * t + p['p3']); s = 0.10 * math.sin(p['w4'] * t + p['p4'])
    return x, y, a, s
def evalp(p):
    tm = FM / FPS; x0, y0, a0, s0 = path(p, tm); mins = 1e9; near = 0
    for f in range(int(1.0 * FPS), N):
        if f == FM: continue
        x, y, a, s = path(p, f / FPS); m = abs(x - x0) + abs(y - y0) + 7 * abs(a - a0) + 400 * abs(s - s0)
        mins = min(mins, m)
        if m < 70: near += 1
    return mins, near
def inside(p):
    tm = FM / FPS; x0, y0, a0, s0 = path(p, tm)
    for f in range(int(0.6 * FPS), N, 2):
        x, y, a, s = path(p, f / FPS); x = TX + x - x0; y = TY + y - y0
        if y - HH < HB + 16 or y + HH > 1496 or x - HW < 72 or x + HW > 1022: return False
        if y + HH > 1110 and x + HW > 884: return False
    return True
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 4); best = None
for _ in range(2500):
    p = dict(A1=rng.uniform(110, 190), A2=rng.uniform(25, 70), w1=rng.uniform(1.4, 2.4), w2=rng.uniform(3, 5), p1=rng.uniform(0, 6.3), p2=rng.uniform(0, 6.3),
             B1=rng.uniform(110, 190), B2=rng.uniform(25, 70), v1=rng.uniform(1.1, 2.1), v2=rng.uniform(2.8, 4.6), q1=rng.uniform(0, 6.3), q2=rng.uniform(0, 6.3),
             R=rng.uniform(14, 30), w3=rng.uniform(1.5, 3.5), p3=rng.uniform(0, 6.3), w4=rng.uniform(1.0, 3.0), p4=rng.uniform(0, 6.3))
    if not inside(p): continue
    mins, near = evalp(p)
    if mins < 22 or near < 3: continue
    sc_ = near + mins * 0.05
    if best is None or sc_ > best[0]: best = (sc_, p, mins, near)
_, P, MINS, NEAR = best; print('min miss', round(MINS, 1), 'near misses', NEAR)
X0, Y0, A0, S0 = path(P, FM / FPS)
def pose(t):
    x, y, a, s = path(P, t); return TX + x - X0, TY + y - Y0, a - A0, 1 + s - S0
# Joy watching (Syeda idle) bottom-left
jg = Image.open(A + 'idle_0.gif'); JOY = []
for i in range(jg.n_frames):
    jg.seek(i); f = jg.convert('RGBA').crop((260, 140, 730, 780)); JOY.append(f.resize((282, 384), Image.NEAREST))
rng2 = random.Random(2); MOTES = [(rng2.uniform(0, W), rng2.uniform(500, 1800), rng2.uniform(0, 6.3), rng2.uniform(0.3, 1)) for _ in range(40)]
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v30_noaudio.mp4'], stdin=subprocess.PIPE)
trail = []; events = [(0.0, 'twinkle')]
for f in range(N):
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    # magic rune circle under the target
    def rune(d):
        for k in range(3):
            r = 230 + k * 26
            d.ellipse([TX - r, TY - r * 0.42 + 190, TX + r, TY + r * 0.42 + 190], outline=(150, 230, 120, 70 - k * 18), width=4)
        for k in range(12):
            a = t * 0.6 + k * math.pi / 6; rx, ry = TX + 245 * math.cos(a), TY + 190 + 103 * math.sin(a)
            d.rectangle([rx - 5, ry - 5, rx + 5, ry + 5], fill=(190, 255, 150, 150))
    layer(img, rune)
    # outline (pulsing glow)
    pulse = 0.6 + 0.4 * math.sin(t * 5)
    gl = Image.new('RGBA', OUT.size, (180, 255, 140, 0)); gl.putalpha(OUTGLOW.point(lambda v: int(v * 0.9 * pulse)))
    img.alpha_composite(gl, (TX - OUT.width // 2, TY - OUT.height // 2))
    ol = Image.new('RGBA', OUT.size, (255, 255, 255, 0)); ol.putalpha(OUT)
    img.alpha_composite(ol, (TX - OUT.width // 2, TY - OUT.height // 2))
    # floating motes
    layer(img, lambda d: [d.rectangle([mx, my - 30 * math.sin(t * sp + ph), mx + 5, my + 5 - 30 * math.sin(t * sp + ph)], fill=(230, 255, 160, int(140 + 100 * math.sin(t * 3 + ph)))) for mx, my, ph, sp in MOTES])
    # gummy
    if t >= 0.6:
        x, y, a, s = pose(t)
        gi = GP.resize((int(GP.width * s), int(GP.height * s)), Image.NEAREST).rotate(a, resample=Image.NEAREST, expand=True)
        trail = (trail + [(x, y)])[-10:]
        layer(img, lambda d: [d.rectangle([tx_ - 3 - i, ty_ - 3 - i, tx_ + 3 + i, ty_ + 3 + i], fill=(255, 200, 150, 20 + i * 14)) for i, (tx_, ty_) in enumerate(trail)])
        sh = Image.new('RGBA', (220, 50), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([0, 0, 219, 49], fill=(0, 0, 0, 70))
        img.alpha_composite(sh, (int(x - 110), int(TY + 170)))
        img.alpha_composite(gi, (int(round(x - gi.width / 2)), int(round(y - gi.height / 2))))
    vf = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(vf, (72, 1492 - vf.height))
    # header
    d = ImageDraw.Draw(img)
    if t < 0.9: ctext(d, W / 2, HB + 40, 'GET READY...', F(44), (255, 255, 255), 6)
    if t > DUR - 1.3:
        a_ = int(255 * min(1, (t - (DUR - 1.3)) / 0.25)); L_ = Image.new('RGBA', img.size, (0, 0, 0, 0)); ctext(ImageDraw.Draw(L_), W / 2, HB + 22, 'How close did you get?', F(36), (255, 214, 60), 6, a_); img.alpha_composite(L_)
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (FM - 1, FM, FM + 1): img.convert('RGB').crop((240, 700, 840, 1340)).save(f'm_{f - FM:+d}.png')
    if f % 30 == 0: img.convert('RGB').resize((216, 384)).save(f'p_{f:03d}.png')
ff.stdin.close(); ff.wait()
for k in range(1, 6): events.append((round(k * 1.85 + 0.6, 3), 'whoosh_8bit'))
json.dump({'events': events}, open('v30_events.json', 'w')); print('done match frame', FM)
