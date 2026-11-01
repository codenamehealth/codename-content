import sys; sys.path.insert(0, '..')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rnd = random.Random(7)
K = 4; GY = 1700; CXH = 540; M = 44
IDL = idle('hollow', K)                                   # feet at 78*K
FALL = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob('fall2/*.png'))]   # feet at 108*K in 128 canvas
CRATER = up(crop(Image.open('crater/03.png').convert('RGBA')), 5)
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
VICF = vic('hollow', 330)
GUM = gummy('mush', 4)
hub = Image.open(A + 'hub.gif'); BG = []
for i in range(0, hub.n_frames, 2):
    hub.seek(i); f = hub.convert('RGB').resize((3569, 2008), Image.NEAREST).crop((1500 - M, 0, 1500 + W + M, H + 2 * M))
    BG.append(f.convert('RGBA'))
def star(d, x, y, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=(60, 40, 10))
T_NOW = 3.2; T_FALL = 3.35; FALL_D = 0.55; T_HIT = T_FALL + FALL_D; T_GUM = 5.0; T_BONK = 5.55; T_UP = 6.5; DUR = 9.6
out = Writer('d10_noaudio.mp4'); ev = []
def once(name, t0, t):
    if t0 <= t < t0 + 1 / FPS and (round(t0, 3), name) not in ev: ev.append((round(t0, 3), name))
for f in range(int(DUR * FPS)):
    t = f / FPS
    bgf = BG[int(t * 8) % len(BG)]
    world = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # crater after impact
    if t >= T_HIT:
        k = min(1, (t - T_HIT) / 0.12)
        cr = CRATER if k >= 1 else up(CRATER, 0.6 + 0.4 * k)
        world.alpha_composite(cr, (CXH - cr.width // 2, GY - cr.height // 2 - 6))
    # hollow
    jit = 0
    if t < T_NOW:
        jit = int(rnd.uniform(-1, 1) * (1 + 3 * t / T_NOW))
        spr = IDL[int(t * 8) % 6]; world.alpha_composite(spr, (CXH - spr.width // 2 + jit, GY - 78 * K))
    elif t < T_UP:
        if t < T_FALL: i = 0
        else: i = min(len(FALL) - 1, int((t - T_FALL) / FALL_D * (len(FALL) - 1)))
        spr = FALL[i]; bob = 0
        if T_BONK <= t < T_BONK + 0.25: bob = int(10 * math.sin((t - T_BONK) / 0.25 * math.pi))
        world.alpha_composite(spr, (CXH - spr.width // 2, GY - 108 * K + bob))
    else:
        u = t - T_UP
        if u < 0.35:
            i = max(0, len(FALL) - 1 - int(u / 0.35 * (len(FALL) - 1)))
            spr = FALL[i]; world.alpha_composite(spr, (CXH - spr.width // 2, GY - 108 * K - int(40 * math.sin(u / 0.35 * math.pi))))
        else:
            vf = VICF[int((u - 0.35) * 8) % len(VICF)]
            world.alpha_composite(vf, (CXH - vf.width // 2, GY - vf.height + 4))
            g = GUM; gy = GY - vf.height - g.height - 10 + int(6 * math.sin(t * 5))
            world.alpha_composite(g, (CXH + 50 - g.width // 2, gy))
    # dust at impact
    if T_HIT <= t < T_HIT + 0.6:
        v = (t - T_HIT) / 0.6
        for side in (-1, 1):
            sc = 2.5 + 2.0 * v; du = up(DUST, sc); al = du.getchannel('A').point(lambda p: int(p * max(0, 1 - v))); du.putalpha(al)
            world.alpha_composite(du, (int(CXH + side * (120 + 160 * v) - du.width / 2), int(GY - du.height + 20)))
    # gummy falling
    if T_GUM <= t < T_BONK:
        v = (t - T_GUM) / (T_BONK - T_GUM); gy = -100 + (GY - 200 + 100) * v * v
        g = GUM.rotate(-v * 300, expand=True, resample=Image.NEAREST)
        world.alpha_composite(g, (CXH - 20 - g.width // 2, int(gy - g.height / 2)))
    elif T_BONK <= t < T_UP:
        v = min(1, (t - T_BONK) / 0.4); gy = GY - 150 - 60 * math.sin(v * math.pi) * (1 - v) - 0
        world.alpha_composite(GUM, (CXH - 20 - GUM.width // 2, int(GY - 150 - GUM.height + (0 if v >= 1 else -80 * math.sin(v * math.pi)))))
    # shake whole world
    sx = sy = 0
    if T_NOW <= t < T_HIT + 0.9:
        amp = 34 if t < T_HIT + 0.15 else 34 * max(0, 1 - (t - T_HIT - 0.15) / 0.75)
        sx, sy = int(rnd.uniform(-amp, amp)), int(rnd.uniform(-amp, amp))
    img = bgf.crop((M - sx, M - sy, M - sx + W, M - sy + H))
    img.alpha_composite(world.transform(world.size, Image.AFFINE, (1, 0, -sx, 0, 1, -sy)) if (sx or sy) else world)
    d = ImageDraw.Draw(img)
    # stars circling after the hit (until he gets up)
    if T_HIT + 0.2 <= t < T_UP:
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        for k in range(3):
            a = t * 5 + k * 2.09; star(dd, CXH - 80 + 110 * math.cos(a), GY - 200 + 30 * math.sin(a), 22, (255, 220, 70, 255))
        img.alpha_composite(L)
    # text
    items = []
    if t < T_NOW:
        items += [(W / 2, 250, 'SHAKE YOUR PHONE', 52, (255, 255, 255), 7, 255), (W / 2, 330, 'FOR A SURPRISE', 52, (255, 255, 255), 7, 255), (W / 2, 410, 'IN...', 44, (255, 255, 255), 6, 255)]
        n = 4 - int(t / 0.8); u = (t % 0.8) / 0.8; s = int(150 * (1.3 - 0.3 * min(1, u * 4)))
        items.append((W / 2, 520, str(n), s, (255, 80, 80), 10, 255)); once('tick_8bit', round(int(t / 0.8 + 1e-6) * 0.8, 3), t)
    elif t < T_NOW + 1.0:
        u = t - T_NOW; s = int(160 * (1.2 - 0.2 * min(1, u * 5)))
        items.append((W / 2, 400, 'NOW!', s, (255, 80, 80), 10, int(255 * min(1, (1.0 - u) / 0.3))))
    if T_BONK <= t < T_BONK + 1.0:
        u = t - T_BONK; items.append((CXH + 180, GY - 420 - u * 60, 'BONK!', 56, (255, 214, 60), 8, int(255 * min(1, (1 - u) / 0.3))))
    if t >= T_UP + 0.35:
        u = t - T_UP - 0.35; a = int(255 * min(1, u / 0.25)); s = int(84 * (1.25 - 0.25 * min(1, u * 4)))
        items += [(W / 2, 300, 'SURPRISE!', s, (255, 214, 60), 10, a), (W / 2, 440, '+1 GUMMY', 48, (255, 255, 255), 7, a)]
    if items: text_layer(img, items)
    once('boom', T_NOW, t); once('swish', T_FALL, t); once('punch', T_HIT, t); once('whoosh_8bit', T_GUM, t); once('boing', T_BONK, t)
    once('jump', T_UP, t); once('powerup_8bit', T_UP + 0.35, t)
    out.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
out.close(); json.dump(ev, open('ev.json', 'w')); print('done', DUR, ev)
