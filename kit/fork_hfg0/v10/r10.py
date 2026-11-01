import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c2')
from common import *
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import hook_layer2
# review r010: 36px 'FOR A SURPRISE' sub cut (the post caption says it); comment prompt as a 52px band line from frame 0
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['SHAKE YOUR', 'PHONE'], accent=0, color=(255, 214, 60), size=72)   # Oct 29: soft fade, no box; 'Did you shake it?' sub cut
print('hook bottom', HB)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rnd = random.Random(7)
K = 8; GY = 1460; CXH = 540; M = 44
IDL = idle('hollow', K)                                   # feet at 78*K
FALL = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c2/v10/fall2/*.png'))]   # feet at 108*K in 128 canvas
CRATER = up(crop(Image.open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_c2/v10/crater/03.png').convert('RGBA')), 8)
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
_vf = gif_frames(A + VIC['hollow']); _bb = None
for _f in _vf:
    _b = _f.getbbox(); _bb = _b if _bb is None else (min(_bb[0], _b[0]), min(_bb[1], _b[1]), max(_bb[2], _b[2]), max(_bb[3], _b[3]))
VICF = [up(_f.crop(_bb).resize(((_bb[2] - _bb[0]) // 10, (_bb[3] - _bb[1]) // 10), Image.NEAREST), K) for _f in _vf]   # 10x source -> native -> 8x
GUM = gummy('mush', 6)
hub = Image.open(A + 'found_hd.gif'); BG = []   # forest clearing (Bennett: new background, Hollow on solid ground)
for i in range(hub.n_frames):
    hub.seek(i); f = hub.convert('RGB').resize((hub.width * 2, hub.height * 2), Image.NEAREST)
    oy = f.height - (H + 2 * M); f = f.crop((900, oy, 900 + W + 2 * M, oy + H + 2 * M))
    BG.append(f.convert('RGBA'))
def shadow(world, w, a=95):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse([CXH - w, GY - 22, CXH + w, GY + 16], fill=(10, 20, 10, a)); world.alpha_composite(L)
def star(d, x, y, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=(60, 40, 10))
# review r010: countdown 3-2-1 at 0.5s each (was 4-3-2-1 at 0.8s), gag tightened, end hold ~1.1s, last 0.5s returns to the opening state
CNT = 0.5; T_NOW = 3 * CNT; T_FALL = T_NOW + 0.15; FALL_D = 0.55; T_HIT = T_FALL + FALL_D; T_GUM = T_HIT + 0.8; T_BONK = T_GUM + 0.55; T_UP = T_BONK + 0.9
T_SUR = T_UP + 0.35; T_OUT = T_SUR + 1.1; DUR = T_OUT + 0.5
def outv(t): return 0.0 if t < T_OUT else min(1.0, (t - T_OUT) / 0.3)   # 0 -> 1 fade of the end state
STILL = os.environ.get('STILL')
out = Writer('v10_noaudio.mp4' if not STILL else 'still_tmp.mp4'); ev = []
def once(name, t0, t):
    if t0 <= t < t0 + 1 / FPS and (round(t0, 3), name) not in ev: ev.append((round(t0, 3), name))
for f in ([int(x) for x in STILL.split(',')] if STILL else range(int(round(DUR * FPS)))):
    t = f / FPS
    bgf = BG[int(t * 12) % len(BG)]
    world = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    # crater after impact
    if t >= T_HIT:
        k = min(1, (t - T_HIT) / 0.12)
        cr = CRATER if k >= 1 else up(CRATER, 0.6 + 0.4 * k)
        if outv(t) > 0: cr = cr.copy(); cr.putalpha(cr.getchannel('A').point(lambda p: int(p * (1 - outv(t)))))
        world.alpha_composite(cr, (CXH - cr.width // 2, GY - cr.height // 2 - 6))
    # hollow
    jit = 0
    if t < T_NOW:
        jit = int(rnd.uniform(-1, 1) * (2 + 6 * t / T_NOW))   # he trembles harder as the count runs down
        shadow(world, 150); spr = IDL[int(t * 8) % 6]; world.alpha_composite(spr, (CXH - spr.width // 2 + jit, GY - 78 * K))
    elif t < T_UP:
        if t < T_FALL: i = 0
        else: i = min(len(FALL) - 1, int((t - T_FALL) / FALL_D * (len(FALL) - 1)))
        spr = FALL[i]; bob = 0
        if T_BONK <= t < T_BONK + 0.25: bob = int(16 * math.sin((t - T_BONK) / 0.25 * math.pi))
        world.alpha_composite(spr, (CXH - spr.width // 2, GY - 108 * K + bob))
    else:
        u = t - T_UP
        if u < 0.35:
            i = max(0, len(FALL) - 1 - int(u / 0.35 * (len(FALL) - 1)))
            spr = FALL[i]; world.alpha_composite(spr, (CXH - spr.width // 2, GY - 108 * K - int(60 * math.sin(u / 0.35 * math.pi))))
        elif t < T_OUT + 0.15:
            shadow(world, 170); vf = VICF[int((u - 0.35) * 8) % len(VICF)]
            world.alpha_composite(vf, (CXH - vf.width // 2, GY - vf.height + 4))
            g = GUM; gy = GY - vf.height - g.height - 10 + int(6 * math.sin(t * 5))
            if outv(t) > 0: g = g.copy(); g.putalpha(g.getchannel('A').point(lambda p: int(p * (1 - outv(t)))))
            world.alpha_composite(g, (CXH + 50 - g.width // 2, gy))
        else:   # arms down: back to the opening idle stance so the loop joins frame 0
            shadow(world, 150); spr = IDL[int(t * 8) % 6]; world.alpha_composite(spr, (CXH - spr.width // 2, GY - 78 * K))
    # dust at impact
    if T_HIT <= t < T_HIT + 0.6:
        v = (t - T_HIT) / 0.6
        for side in (-1, 1):
            sc = 4.0 + 3.0 * v; du = up(DUST, sc); al = du.getchannel('A').point(lambda p: int(p * max(0, 1 - v))); du.putalpha(al)
            world.alpha_composite(du, (int(CXH + side * (190 + 250 * v) - du.width / 2), int(GY - du.height + 20)))
    # gummy falling
    if T_GUM <= t < T_BONK:
        v = (t - T_GUM) / (T_BONK - T_GUM); gy = -100 + (GY - 295 + 100) * v * v
        g = GUM.rotate(-v * 300, expand=True, resample=Image.NEAREST)
        world.alpha_composite(g, (CXH - 150 - g.width // 2, int(gy - g.height / 2)))
    elif T_BONK <= t < T_UP:
        v = min(1, (t - T_BONK) / 0.4); gy = GY - 150 - 60 * math.sin(v * math.pi) * (1 - v) - 0
        world.alpha_composite(GUM, (CXH - 150 - GUM.width // 2, int(GY - 215 - GUM.height + (0 if v >= 1 else -80 * math.sin(v * math.pi)))))
    # shake whole world
    sx = sy = 0
    if t < T_NOW:   # small building wobble under the countdown
        amp = 1 + 4 * t / T_NOW; sx, sy = int(rnd.uniform(-amp, amp)), int(rnd.uniform(-amp, amp))
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
            a = t * 5 + k * 2.09; star(dd, CXH - 160 + 170 * math.cos(a), GY - 300 + 40 * math.sin(a), 32, (255, 220, 70, 255))
        img.alpha_composite(L)
    # text
    items = []
    if t < T_NOW:
        n = 3 - int(t / CNT + 1e-6); u = (t % CNT) / CNT; s = int(150 * (1.3 - 0.3 * min(1, u * 4)))
        items.append((W / 2, HB + 50, str(n), s, (255, 80, 80), 10, 255)); once('tick_8bit', round(int(t / CNT + 1e-6) * CNT, 3), t)
    elif t < T_NOW + 1.0:
        u = t - T_NOW; s = int(160 * (1.2 - 0.2 * min(1, u * 5)))
        items.append((W / 2, HB + 60, 'NOW!', s, (255, 80, 80), 10, int(255 * min(1, (1.0 - u) / 0.3))))
    if T_BONK <= t < T_BONK + 1.0:
        u = t - T_BONK; items.append((CXH + 190, GY - 560 - u * 60, 'BONK!', int(84 * (1.25 - 0.25 * min(1, u * 6))), (255, 214, 60), 11, int(255 * min(1, (1 - u) / 0.3))))   # 56 -> 84px, heavier outline
    if t >= T_SUR:
        u = t - T_SUR; a = int(255 * min(1, u / 0.25) * (1 - outv(t))); s = int(84 * (1.25 - 0.25 * min(1, u * 4)))
        if a > 0: items += [(W / 2, HB + 50, 'SURPRISE!', s, (255, 80, 80), 10, a)]   # '+1 GUMMY' cut (the gummy is right there)
    if t >= DUR - 0.2:   # the first count number comes back in, matching frame 0
        u = (t - (DUR - 0.2)) / 0.2; items.append((W / 2, HB + 50, '3', 195, (255, 80, 80), 10, int(255 * min(1, u * 1.4))))
    if items: text_layer(img, items)
    once('boom', T_NOW, t); once('swish', T_FALL, t); once('punch', T_HIT, t); once('whoosh_8bit', T_GUM, t); once('boing', T_BONK, t)
    once('jump', T_UP, t); once('powerup_8bit', T_SUR, t)
    img.alpha_composite(HOOK)
    out.write(img)
    if STILL: img.convert('RGB').save(f'still_{f}.png')
out.close(); json.dump(ev, open('ev10.json', 'w')); print('done', DUR, ev)
