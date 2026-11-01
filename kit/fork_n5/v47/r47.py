# n5 rework of #47 (Bennett Oct 29: "cleos floating", "same as the others", "top isnt interesting enough", "a little too zoomed in").
# Base: fork_hfg5/v47/r47.py. Changes: guides 5x -> 4x; Cleo walks on the castle yard dirt (ground moved down into the yard);
# top lane escalates (sprint, faceplant slide, faster sprint, tumbling wipeout, BURNED OUT, slimes gather and poke her);
# expected ending happens (Cleo FINISHED), then the break: the slimes lift Joy and crowd-surf her over the line, CARRIED.
# usage: python3 r47.py [preview t1 t2 ...]
import sys, math, json, random, os, glob
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'fork_hfg5'); from hk import hook_fade_segs
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = 4
def fr(d, k=K, lo=0, hi=None): return [up(Image.open(p).convert('RGBA'), k) for p in sorted(glob.glob(SP0 + d + '/*.png'))[lo:hi]]
RUN = fr('pixellab/race/joy_run', lo=1, hi=9); SLIDE = fr('pixellab/maze/anim/joy_slide'); KO = fr('pixellab/king/joy_ko')
CLAP = fr('fork2/joy_clap'); JIDLE = idle('joy', K)
WALK = fr('fork_a5/gen/cleo_walk', lo=1, hi=9); WIN = fr('fork_a5/gen/cleo_win')
SLM = fr('pixellab/race/slime_idle_c', 3)
FLAG = up(crop(Image.open(SP0 + 'fork_a5/gen/flag/00.png').convert('RGBA')), 3).transpose(Image.FLIP_LEFT_RIGHT)
GUM = gummy('cre', 3)
MCOL = (120, 225, 90); DCOL = (100, 165, 255)
HOOK, HB = hook_fade_segs([[('MOTIVATION', MCOL)], [('VS ', (255, 255, 255)), ('DISCIPLINE', DCOL)]])
SEAM = 985; P1, PH1 = 0, SEAM - 5; P2 = SEAM + 5; PH2 = H - P2
GY1 = 900; GY2 = 1420
def panel(name, x0, src_ground, gy_panel, ph):
    out = []; y0 = src_ground - gy_panel
    for f in bg_frames(name, (1920, 1080), step=2, bright=0.85):
        c = f.crop((x0, max(0, y0), x0 + W, min(1080, y0 + ph))); p = Image.new('RGBA', (W, ph), (14, 10, 24, 255)); p.alpha_composite(c, (0, max(0, -y0)))
        yb = 1080 - y0
        if yb < ph:
            strip = f.crop((x0, 1080 - (ph - yb), x0 + W, 1080)).transpose(Image.FLIP_TOP_BOTTOM); p.alpha_composite(strip, (0, yb))
            g = Image.new('L', (1, ph), 0)
            for yy in range(max(0, yb - 60), ph): g.putpixel((0, yy), int(140 * min(1, max(0, (yy - yb + 60) / 200))))
            sh = Image.new('RGBA', (W, ph), (14, 10, 24, 255)); sh.putalpha(g.resize((W, ph))); p.alpha_composite(sh)
        out.append(p)
    return out
TOP = panel('sun_hd.gif', 420, 975, GY1 - P1, PH1)
BOT = panel('vit_hd.gif', 420, 905, GY2 - P2, PH2)    # ground in the middle of the castle yard dirt (was the wall base: Cleo read as floating)
FLAGX = 885
def put(img, spr, x, gy, base=78, cx=46):
    img.alpha_composite(spr, (int(x - cx * K), int(gy - base * K)))
def put_bb(img, spr, x, gy, lift=0):              # lying / tumbling frames: bbox bottom on the ground
    bb = spr.getbbox(); img.alpha_composite(spr, (int(x - (bb[0] + bb[2]) / 2), int(gy - bb[3] - lift)))
def shadow(img, x, gy, r=56):
    layer(img, lambda dd: dd.ellipse([x - r, gy - 11, x + r, gy + 11], fill=(0, 0, 0, 80)))
def stamp(img, cx, cy, txt, col, u, size=72):
    sc = 1.0 if u > 0.12 else 0.7 + 2.5 * u
    text_layer(img, [(cx, cy, txt, int(size * sc), col, 12, 255)])
# ---- top timeline (Joy = MOTIVATION)   review2: stumbles read as intentional, carry faster, CARRIED by ~6.3s, crossfade loop
XS = 150
ROCK = up(crop(Image.open(SP0 + 'fork_a11/gen/rock/00.png').convert('RGBA')), 3); X_ROCK = 392
T_TRIP = 0.8; X_TRIP = 330                        # sprint 1 into the rock
T_DOWN = T_TRIP + 0.22; T_UP = T_DOWN + 0.34      # trip + faceplant (slide 0-3), impact dust, quick get-up (slide 7-8)
X_UP = 490
T_S2 = T_UP; T_SLOW = 1.85; T_COL = 2.2; X_COL = 545   # sprint 2 fast, runs out of steam, slows
T_FLAT = T_COL + 0.35; X_FLAT = 555               # collapses backwards flat (joy_ko 0,2,3 then 8: no upside-down frames)
T_BURN = T_FLAT
SLIMES = [  # (enter time, from x, rest x)  they gather around her one by one
    (2.85, 1150, X_FLAT + 150), (3.35, -150, X_FLAT - 150), (3.85, 1150, X_FLAT + 10)]
T_POKE = 3.2                                      # slime 1 hops onto her and back off
T_FIN = 4.9                                       # Cleo finishes (the expected ending)
T_LIFT = 5.15; T_SURF0 = 5.35; T_SURF1 = 6.05; X_END = 760     # the break: slimes lift Joy and crowd-surf her to the flag
T_LAND = T_SURF1 + 0.2
T_XF = 0.4; T_END = T_LAND + 1.1 + T_XF; DUR = T_END; T_RW = 99; NF = int(round(DUR * FPS)); NXF = int(round(T_XF * FPS))
# ---- bottom (Cleo = DISCIPLINE)
XC0, XC1 = 150, 770; GX = [300, 430, 560, 690]
def sm(a, b, t):
    u = min(1.0, max(0.0, (t - a) / (b - a))); return u * u * (3 - 2 * u)
ev = []; popped = {i: (gxp - 10 - XC0) / (XC1 - XC0) * T_FIN for i, gxp in enumerate(GX)}
def render(f, log=False):
    t = f / FPS; rw = t >= T_RW; ur = min(1.0, (t - T_RW) / (RW - 1 / FPS)) if rw else 0
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    for py, bgs, gyy in ((P1, TOP, GY1), (P2, BOT, GY2)):
        img.alpha_composite(bgs[int(f / NF * 2 * len(bgs)) % len(bgs)], (0, py))
        img.alpha_composite(FLAG, (FLAGX - FLAG.width, gyy - FLAG.height + 6))
    # ================= top: Joy
    gy = GY1
    def dust(x, n=3, a0=150):
        layer(img, lambda dd: [dd.ellipse([x - 70 - q * 30 - (t * 300 % 30), gy - 12 - q * 4, x - 40 - q * 30 - (t * 300 % 30), gy + 4], fill=(230, 210, 170, max(0, a0 - q * 40))) for q in range(n)])
    def speed(x):
        layer(img, lambda dd: [dd.rectangle([x - 120 - 90 - (q * 29) % 50, gy - 70 - q * 36, x - 120 - (q * 29) % 50, gy - 65 - q * 36], fill=(255, 250, 235, 200)) for q in range(5)])
    # slimes (behind Joy until they lift her)
    sl_pos = []
    for i, (te, xf, xr) in enumerate(SLIMES):
        if rw or t < te: continue
        if t < T_LIFT:
            u = min(1.0, (t - te) / 0.6); x = xf + (xr - xf) * u; hop = abs(math.sin(u * math.pi * 2)) * 70 if u < 1 else 0
            y = gy - 62 * 3 - hop
            if i == 0 and T_POKE <= t < T_POKE + 0.5:      # boing on her belly, then back
                v = (t - T_POKE) / 0.5; x = xr + (X_FLAT + 20 - xr) * math.sin(v * math.pi); y = gy - 62 * 3 - 90 * math.sin(v * math.pi)
            if T_LIFT - 0.3 <= t:                          # squeeze in under her
                v = sm(T_LIFT - 0.3, T_LIFT, t); x = x + (X_FLAT + (i - 1) * 105 - x) * v
            sl_pos.append((x, y, i))
        else:
            sx = X_FLAT + (X_END - X_FLAT) * sm(T_SURF0, T_SURF1, t) if t < T_LAND + 0.3 else X_END
            if t >= T_LAND: sx = X_END + 260 * sm(T_LAND, T_LAND + 0.7, t) + (i - 1) * 60   # they hop off to the side after the drop
            ph = (t * 7 + i * 2.1); bounce = abs(math.sin(ph)) * (40 if T_SURF0 <= t < T_SURF1 else 10)
            sl_pos.append((sx + (i - 1) * 105, gy - 62 * 3 - bounce, i))
    surfing = T_LIFT <= t < T_LAND and not rw
    for (x, y, i) in sl_pos:
        if surfing: continue
        s = SLM[int(t * 10 + i * 3) % len(SLM)]; img.alpha_composite(s, (int(x - s.width / 2), int(y)))
    # '?' emotes over the gathered slimes, '!' when they decide to carry her
    if not rw and 3.6 <= t < T_LIFT:
        items = []
        for (x, y, i) in sl_pos:
            if t >= SLIMES[i][0] + 0.6: items.append((x, y - 10, '!' if t >= T_LIFT - 0.5 else '?', 52, (255, 255, 255), 8, 255))
        text_layer(img, items)
    if rw:
        x = X_END + (XS - X_END) * ur; spr = JIDLE[0]; shadow(img, x, gy); put(img, spr, x, gy)
    elif t < T_TRIP:
        u = t / T_TRIP; x = XS + (X_TRIP - XS) * u; dust(x); shadow(img, x, gy); put(img, RUN[int(t * 22) % 8], x, gy)
    elif t < T_DOWN:                                  # foot catches the rock, pitches forward
        u = (t - T_TRIP) / (T_DOWN - T_TRIP); k = 1 + min(2, int(u * 3)); x = X_TRIP + 70 * u
        shadow(img, x, gy, 70); put(img, SLIDE[k], x, gy)
    elif t < T_UP:                                    # impact + skid, then pops straight back up
        u = (t - T_DOWN) / (T_UP - T_DOWN); x = X_TRIP + 70 + (X_UP - X_TRIP - 70) * min(1, u * 2)
        k = 3 if u < 0.25 else (4 if u < 0.5 else (7 if u < 0.75 else 8))
        if u < 0.5:
            v = u / 0.5
            layer(img, lambda dd: [dd.ellipse([x - 90 + q * 60 - 40 * v - 26, gy - 30 - 40 * v - (q % 2) * 20 - 26, x - 90 + q * 60 - 40 * v + 26, gy - 30 - 40 * v - (q % 2) * 20 + 26], fill=(235, 215, 175, int(210 * (1 - v)))) for q in range(4)])
        shadow(img, x, gy, 80); put(img, SLIDE[k], x, gy)
    elif t < T_COL:                                   # sprint 2: fast with speed lines, then runs out of steam
        u = sm(T_S2, T_COL, t) if False else (t - T_S2) / (T_COL - T_S2)
        x = X_UP + (X_COL - X_UP) * (1 - (1 - u) ** 2)
        fast = t < T_SLOW
        if fast: speed(x)
        dust(x, 3 if fast else 1); shadow(img, x, gy); put(img, RUN[int(t * (28 if fast else 12)) % 8], x, gy)
        if not fast:                                  # sweat drops
            v = (t - T_SLOW) / (T_COL - T_SLOW)
            layer(img, lambda dd: [dd.ellipse([x + 40 + q * 26, gy - 250 + 60 * v + q * 14, x + 52 + q * 26, gy - 232 + 60 * v + q * 14], fill=(170, 220, 255, int(230 * (1 - v)))) for q in range(2)])
    elif t < T_FLAT:                                  # collapses backwards onto the floor
        u = (t - T_COL) / (T_FLAT - T_COL); k = [0, 2, 3, 8][min(3, int(u * 4))]; x = X_COL + (X_FLAT - X_COL) * u
        shadow(img, x, gy, 70)
        if k in (0, 2): put(img, KO[k], x, gy, base=96, cx=66)
        else: put_bb(img, KO[k], x, gy)
        if k == 8:
            layer(img, lambda dd: [dd.ellipse([x - 120 + q * 80 - 24, gy - 24 - (q % 2) * 16, x - 120 + q * 80 + 24, gy + 4 - (q % 2) * 16], fill=(235, 215, 175, 190)) for q in range(4)])
    elif not surfing and t < T_LAND:
        x = X_FLAT; shadow(img, x, gy, 90)
        twitch = 1 if (T_POKE + 0.2 <= t < T_POKE + 0.3) else 0
        put_bb(img, KO[8], x, gy, 6 * twitch)
    elif surfing:
        sx = X_FLAT + (X_END - X_FLAT) * sm(T_SURF0, T_SURF1, t)
        rise = 120 * sm(T_LIFT, T_SURF0, t)
        for (x_, y_, i) in sl_pos:
            s = SLM[int(t * 10 + i * 3) % len(SLM)]; img.alpha_composite(s, (int(x_ - s.width / 2), int(y_)))
        top = sum(y_ for (x_, y_, i) in sl_pos) / max(1, len(sl_pos)) + 36 * 3 + 14   # rests on the slimes' backs
        put_bb(img, KO[8], sx, gy, (gy - top) * sm(T_LIFT - 0.05, T_LIFT + 0.15, t))
        x = sx
    else:
        x = X_END; u = t - T_LAND
        if u < 0.15: put_bb(img, KO[2], x, gy, 60 * (1 - u / 0.15))
        else: shadow(img, x, gy); put(img, CLAP[int(t * 10) % len(CLAP)], x, gy)
    img.alpha_composite(ROCK, (int(X_ROCK - ROCK.width / 2), int(gy - ROCK.height + 4)))   # in front: her foot catches it
    if T_BURN <= t < T_LIFT and not rw:             # burnout smoke
        u = t - T_BURN; xx = X_FLAT
        layer(img, lambda dd: [dd.ellipse([xx - 30 + 30 * math.sin(u * 3 + q) - (8 + ((u * 0.9 + q / 4) % 1) * 30), gy - 90 - ((u * 0.9 + q / 4) % 1) * 170 - (8 + ((u * 0.9 + q / 4) % 1) * 30),
                                           xx - 30 + 30 * math.sin(u * 3 + q) + (8 + ((u * 0.9 + q / 4) % 1) * 30), gy - 90 - ((u * 0.9 + q / 4) % 1) * 170 + (8 + ((u * 0.9 + q / 4) % 1) * 30)],
                                          fill=(150, 150, 160, int(170 * (1 - (u * 0.9 + q / 4) % 1)))) for q in range(4)])
    if surfing and t >= T_SURF0:                     # little cheer sparkles over the crowd-surf
        layer(img, lambda dd: [dd.rectangle([x - 120 + (q * 61) % 240, gy - 330 - ((t * 1.5 + q * 0.17) % 1) * 120, x - 112 + (q * 61) % 240, gy - 322 - ((t * 1.5 + q * 0.17) % 1) * 120], fill=(255, 235, 140, 220)) for q in range(6)])
    # ================= bottom: Cleo
    gy = GY2
    for i, gxp in enumerate(GX):
        if not rw and i in popped and t >= popped[i]:
            u = t - popped[i]
            if u < 0.9: text_layer(img, [(gxp, gy - 300 - u * 40, '+1', 56, (140, 200, 255), 8, int(255 * min(1, (0.9 - u) / 0.3)))])
            if u < 0.4:
                layer(img, lambda dd: [dd.rectangle([gxp + (20 + 110 * u) * math.cos(q * 0.785) - 6, gy - 80 + (20 + 110 * u) * math.sin(q * 0.785) - 6,
                                                     gxp + (20 + 110 * u) * math.cos(q * 0.785) + 6, gy - 80 + (20 + 110 * u) * math.sin(q * 0.785) + 6], fill=(190, 225, 255, int(255 * (1 - u / 0.4)))) for q in range(8)])
            continue
        bob = int(8 * math.sin(t * 4 + i))
        layer(img, lambda dd: dd.ellipse([gxp - 42, gy - 120 + bob, gxp + 42, gy - 36 + bob], fill=(120, 180, 255, 60)))
        img.alpha_composite(GUM, (int(gxp - GUM.width / 2), int(gy - 78 - GUM.height / 2 + bob)))
        layer(img, lambda dd: dd.ellipse([gxp - 26, gy - 8, gxp + 26, gy + 8], fill=(0, 0, 0, 60)))
    if rw: x = XC1 + (XC0 - XC1) * ur; spr = WALK[0]
    elif t < T_FIN:
        x = XC0 + (XC1 - XC0) * t / T_FIN; spr = WALK[int(t * 9) % 8]
    else:
        x = XC1; spr = WIN[min(8, int((t - T_FIN) * 10))]
        layer(img, lambda dd: [dd.rectangle([x + 50 + 80 * math.cos(t * 3 + q * 1.26), gy - 300 + 60 * math.sin(t * 3 + q * 1.26), x + 59 + 80 * math.cos(t * 3 + q * 1.26), gy - 291 + 60 * math.sin(t * 3 + q * 1.26)], fill=(255, 230, 120, 230)) for q in range(5)])
    shadow(img, x, gy, 50); put(img, spr, x, gy)
    # stamps (one per lane)
    if T_BURN + 0.1 <= t < T_LIFT and not rw: stamp(img, 520, 540, 'BURNED OUT', (255, 110, 80), t - T_BURN - 0.1, 68)
    if T_LAND <= t < T_RW: stamp(img, 470, 540, 'CARRIED', MCOL, t - T_LAND, 72)
    if T_FIN <= t < T_RW: stamp(img, 420, 1080, 'FINISHED', (255, 214, 60), t - T_FIN, 60)
    if rw:
        layer(img, lambda dd: [dd.rectangle([0, py + 40 + q * 70, W - 1, py + 46 + q * 70], fill=(255, 255, 255, int(70 * (1 - ur)))) for py in (P1 + 520, P2 + 60) for q in range(6)])
    layer(img, lambda dd: dd.rectangle([0, SEAM - 5, W, SEAM + 4], fill=(14, 10, 24, 255)))
    img.alpha_composite(HOOK)
    return img
_F0 = None
def frame(f):                                     # last T_XF crossfades into frame 0 (clean loop)
    global _F0
    img = render(f); k = f - (NF - NXF)
    if k >= 0:
        if _F0 is None: _F0 = render(0)
        img = Image.blend(img, _F0, (k + 1) / (NXF + 1))
    return img
if len(sys.argv) > 1 and sys.argv[1] == 'preview':
    for ts in sys.argv[2:]:
        f = int(round(float(ts) * FPS)); frame(f).convert('RGB').save(f'pv_{f:04d}.png')
    sys.exit()
wr = Writer('v47_noaudio.mp4')
for f in range(NF): wr.write(frame(f))
wr.close()
ev = [(round(popped[i], 3), 'coin_8bit') for i in popped]
ev += [(0.0, 'swish'), (T_DOWN, 'punch'), (T_COL + 0.3, 'poof'), (SLIMES[0][0], 'boing'), (T_POKE + 0.2, 'boing'),
       (SLIMES[2][0] + 0.1, 'jump'), (T_FIN, 'victory'), (T_LIFT, 'powerup1'), (T_LAND, 'cheer')]
ev.sort()
json.dump({'events': ev}, open('v47_ev.json', 'w')); print('done', DUR, NF, ev)
