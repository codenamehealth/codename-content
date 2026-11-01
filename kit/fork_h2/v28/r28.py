"""#28 Swipe to the beat, Oct 29 notes (Bennett): the Hollow grows a little with every hit until he is bigger than the reel;
at the end the camera zooms out to show his head poking out of the tavern roof. Beat game, hits, hook strip and loop kept.
Base: fork_hfg2/v28/r28.py (batch_v3 version)."""
import sys; SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP + 'fork1'); sys.path.insert(0, SP + 'fork_rc2')
from common import *
from rc2 import acv_gloss, FF
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade, hook_band
os.chdir(os.path.dirname(os.path.abspath(__file__)))
TEST = len(sys.argv) > 1
HOOK, HB = hook_band(['SWIPE TO', 'THE BEAT!'], accent=1, size=64)
# fork_h2 Oct 29 hook swap (bottom edge kept)
import sys as _s; _s.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h2'); import hookx
HOOK, HB = hookx.band_keep(['SWIPE TO', 'THE BEAT!'], ['HOW BIG DOES', [('HE ', None), ('GET?', hookx.GOLD)]], size=64)
print('hook bottom', HB)
BG = up(Image.open(SP + 'fork3/tavern2/00.png').convert('RGBA'), 3)
B0, BP = 0.03, 0.4643
HITS = [B0 + BP * k for k in range(1, 17, 2)]           # 8 swipes on every other beat, first on beat 1 (unchanged)
KINDS = ['mush', 'acv', 'mel', 'cre', 'mush', 'acv', 'mel', 'cre']
EATS = [h + 0.25 for h in HITS]
GROW = 0.27                                             # Mario-style flicker between old and new size
SCALES = [4, 5, 6, 7, 9, 11, 14, 18, 24]               # Hollow scale after n gummies (24 = head already past the top)
T_SURGE = EATS[-1] + GROW + 0.05                        # 7.57: last surge, the ceiling shakes
T_CUT = T_SURGE + 0.45                                  # 8.02: cut outside
ZOOM = 1.1                                              # zoom-out length
HOLD = 0.2                                              # review: static end hold trimmed (~9.3s total)
DUR = T_CUT + ZOOM + HOLD; NF = int(round(DUR * FPS))
EAT1 = [Image.open(SP + f'fork3/hollow_eat/{i:02d}.png').convert('RGBA') for i in range(13)]
VIC92 = [f.resize((92, 92), Image.NEAREST) for f in gif_frames(A + 'hollow-victory.gif')]
def gs(k): g = Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA'); return acv_gloss(g) if k == 'acv' else g
G2 = {k: up(gs(k), 2) for k in ['mush', 'acv', 'mel', 'cre']}
G4 = {k: up(gs(k), 4) for k in G2}
HX0, HY = 360, 1480           # Hollow feet
RX, RY = 742, 884             # hit ring; lane x612-872
RR = 104; LW = 130
LB = 1496                     # lane bottom
_sc = {}
def spr(k, sc):
    if (k, sc) not in _sc: _sc[(k, sc)] = up(EAT1[k], sc)
    return _sc[(k, sc)]
def hscale(t):
    n = sum(1 for e in EATS if t >= e)
    if n == 0: return SCALES[0]
    e = EATS[n - 1]
    if t - e < GROW:   # flicker old/new every 3 frames, ending on new
        ph = int((t - e) * FPS) // 3
        return SCALES[n] if ph % 2 else SCALES[n - 1]
    if t >= T_SURGE:   # final surge: keeps growing, he is bigger than the reel
        return min(34, SCALES[-1] + int((t - T_SURGE) * 30))
    return SCALES[n]
def hx(sc): return int(HX0 + (min(sc, 24) - 4) * 6)

# ---------- exterior (Liza's village, tavern) ----------
HUB = Image.open(A + 'hub.gif'); HUBF = []
for i in range(HUB.n_frames):
    HUB.seek(i); HUBF.append(HUB.convert('RGB'))
SKY = (76, 197, 252)
ES = 1.2                    # hub native pixels are 5px -> 6px
EY0 = 950                   # hub top edge in the reel
EX0 = int(1122 * ES) - 540  # tavern gable centred
CB = (596, 64, 742, 176)   # the one clean whole cloud in the art, reused (some flipped)
CLOUDS = [((CB, 0), (20, 120)), ((CB, 1), (800, 150)), ((CB, 1), (40, 600)), ((CB, 0), (790, 680)), ((CB, 0), (-60, 900))]
def cloud(box):
    c = HUBF[0].crop(box).convert('RGBA'); px = c.load()
    for y in range(c.height):
        for x in range(c.width):
            r, g, b, a = px[x, y]
            if not (b >= 240 and r >= 120): px[x, y] = (0, 0, 0, 0)
    return c.resize((int(c.width * ES), int(c.height * ES)), Image.NEAREST)
CLOUDI = [(cloud(b).transpose(Image.FLIP_LEFT_RIGHT) if fl else cloud(b), xy) for (b, fl), xy in CLOUDS]
def hub_frame(i):
    f = HUBF[i % len(HUBF)].copy()
    # chimney smoke is cut by the top edge of the art: paint it out (sky)
    px = f.load()
    for y in range(0, 60):
        for x in range(1340, 1480):
            r, g, b = px[x, y]
            if (r, g, b) == (167, 222, 225): px[x, y] = SKY
    return f.resize((int(f.width * ES), int(f.height * ES)), Image.NEAREST)
_hubc = {}
def ext_base(i):
    i %= len(HUBF)
    if i in _hubc: return _hubc[i].copy()
    im = Image.new('RGBA', (W, H), SKY + (255,))
    for c, (x, y) in CLOUDI: im.alpha_composite(c, (x, y))
    hf = hub_frame(i).crop((EX0, 0, EX0 + W, H - EY0)); im.paste(hf, (0, EY0))
    _hubc[i] = im; return im.copy()
GX = 540 + 0                # gable centre in the reel
CUT_Y = EY0 + int(60 * ES)  # where his chest breaks through the gable / roof ridge
HS = 14                     # Hollow scale outside (native 92 canvas): his head is as wide as the tavern
def ext_frame(t):
    u = t - T_CUT
    im = ext_base(int(t * 10))
    # head + raised arms through the roof: victory frames cropped at the chest
    rise = min(1.0, u / 0.28); rise = 1 - (1 - rise) ** 3
    v = VIC92[int(u * 8) % len(VIC92)]
    cut_native = 47                                   # rows 0..47 of the 92 canvas = head, arms, upper chest
    top = v.crop((0, 0, 92, cut_native)); top = up(top, HS)
    vis = int(top.height * rise)
    if vis > 0:
        part = top.crop((0, top.height - vis if False else 0, 92 * HS, vis))
        # emerges upward: bottom of the visible part stays at CUT_Y
        im.alpha_composite(top.crop((0, 0, top.width, vis)), (GX - top.width // 2, CUT_Y - vis))
    # broken roof rim around his chest
    rr = random.Random(7)
    def rim(d):
        for k in range(40):
            x = GX - 200 + k * 10 + rr.randint(-3, 3); y = CUT_Y - 6 + rr.randint(-8, 6)
            col = rr.choice([(157, 87, 45), (100, 50, 40), (120, 62, 36), (60, 30, 24)])
            d.rectangle([x, y, x + 12 + rr.randint(0, 8), y + 12 + rr.randint(0, 6)], fill=col + (255,))
    layer(im, rim)
    # roof debris flying out and falling
    if u < 1.6:
        dr = random.Random(11)
        def deb(d):
            for k in range(22):
                vx = dr.uniform(-520, 520); vy = dr.uniform(-900, -420); s = dr.choice([12, 18, 24])
                x = GX + vx * u; y = CUT_Y - 40 + vy * u + 1400 * u * u
                if y < H:
                    col = dr.choice([(157, 87, 45), (100, 50, 40), (205, 120, 60), (90, 60, 40)])
                    d.rectangle([x, y, x + s, y + s * 0.7], fill=col + (255,))
        layer(im, deb)
    return im
def ext_zoom(t):
    u = t - T_CUT
    im = ext_frame(t)
    p = min(1.0, u / ZOOM); p = 1 - (1 - p) ** 3          # ease out
    z = 2.3 + (1.0 - 2.3) * p
    if z > 1.001:
        cx, cy = GX, CUT_Y - 150 + 150 * p                # start on the head, end on the whole village
        cw, ch = W / z, H / z
        x0 = max(0, min(W - cw, cx - cw / 2)); y0 = max(0, min(H - ch, cy - ch / 2))
        im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.NEAREST)
    return im

ev = []
for h in HITS: ev.append((round(h, 3), 'swish'))
for e in EATS: ev.append((round(e, 3), 'powerup_8bit'))
ev.append((round(T_SURGE, 3), 'boom'))
ev.append((round(T_CUT, 3), 'victory'))
def frame(f):
    t = f / FPS
    if t >= T_CUT:
        return ext_zoom(t)                                  # review: no hook strip once he is through the roof
    img = BG.copy()
    eaten = sum(1 for e in EATS if t >= e)
    sc = hscale(t); HX = hx(sc)
    # Hollow (behind the game UI: lane, counter and stamps stay on top)
    last = max([h for h in HITS if h <= t], default=None)
    k = 0
    if last is not None:
        u = t - last
        if u < 0.5: k = [4, 5, 6, 7, 8][min(4, int(u / 0.1))]
        elif u < 0.8: k = [9, 10, 11][min(2, int((u - 0.5) / 0.1))]
    if t >= T_SURGE: k = 0
    s_ = spr(k, sc)
    bob = int(6 * abs(math.sin(math.pi * (t - B0) / BP))) if sc < 18 else 0
    layer(img, lambda d: d.ellipse([HX - 26 * sc, HY - 5 * sc, HX + 26 * sc, HY + 5 * sc], fill=(0, 0, 0, 90)))
    img.alpha_composite(s_, (HX - s_.width // 2, HY - 78 * sc - bob))
    mouth = (HX, max(300, HY - 78 * sc + 30 * sc)); head = max(420, HY - 65 * sc)
    # gummy counter row
    for i in range(8):
        x = W / 2 + (i - 3.5) * 104; y = HB + 52
        if i < eaten:
            g = G2[KINDS[i]]; pop = max(0, 1 - (t - EATS[i]) / 0.2); g2 = up(g, 1 + 0.4 * pop) if pop > 0 else g
            img.alpha_composite(g2, (int(x - g2.width / 2), int(y - g2.height / 2)))
        else:
            layer(img, lambda d, x=x, y=y: d.ellipse([x - 28, y - 28, x + 28, y + 28], fill=(20, 12, 6, 120), outline=(255, 230, 180, 200), width=5))
    # swipe lane (until the last gummy is swiped)
    if t < EATS[-1] + 0.3:
        def lane(d):
            d.rounded_rectangle([RX - LW, RY - RR - 22, RX + LW, LB], 60, fill=(20, 12, 6, 185), outline=(255, 214, 60, 230), width=6)
            for j in range(5):
                yy = LB - 30 - ((t * 300 + j * 110) % 520)
                if yy > RY + RR + 30: d.line([(RX - 46, yy + 24), (RX, yy - 20), (RX + 46, yy + 24)], fill=(255, 230, 160, 150), width=10)
            beat = (t - B0) / BP; pulse = max(0, 1 - (beat - round(beat)) ** 2 * 12)
            d.ellipse([RX - RR, RY - RR, RX + RR, RY + RR], outline=(20, 12, 6, 230), width=16 + int(6 * pulse))
            d.ellipse([RX - RR, RY - RR, RX + RR, RY + RR], outline=(255, 240, 200, 240), width=8 + int(6 * pulse))
        layer(img, lane)
    texts = []
    for i, h in enumerate(HITS):
        g = G4[KINDS[i]]
        if h - 1.0 <= t < h:
            p = (t - (h - 1.0)) / 1.0; y = LB + 70 - (LB + 70 - RY) * p
            gc = g.crop((0, 0, g.width, max(1, min(g.height, int(LB - 8 - (y - g.height / 2))))))
            img.alpha_composite(gc, (int(RX - g.width / 2), int(y - g.height / 2)))
        elif h <= t < h + 0.25:
            p = (t - h) / 0.25; x = RX + (mouth[0] - RX) * p; y = RY + (mouth[1] - RY) * p - 180 * math.sin(math.pi * p)
            gg = up(G2[KINDS[i]], 2 - p * 0.9)
            img.alpha_composite(gg, (int(x - gg.width / 2), int(y - gg.height / 2)))
        if 0 <= t - h < 0.35:
            a = int(255 * (1 - (t - h) / 0.35)); r = RR + (t - h) * 300
            layer(img, lambda d, r=r, a=a: d.ellipse([RX - r, RY - r, RX + r, RY + r], outline=(255, 214, 60, a), width=10))
        if 0.0 <= t - h < 0.75 and i < 7:
            u = t - h; a = int(255 * min(1, (0.75 - u) / 0.3)); sc_ = 1 + 0.25 * max(0, 1 - u / 0.12)
            # review: drop PERFECT! when the grown Hollow reaches its spot (hit 7 on), never draw it over him
            sch = SCALES[sum(1 for e in EATS if h >= e)]; htop = HY - 64 * sch; hright = hx(sch) + 26 * sch
            if not (htop < RY - RR - 96 + 60 and hright > RX - 14 - 170): texts.append((RX - 14, RY - RR - 96, 'PERFECT!', int(56 * sc_), (255, 255, 255), 9, a))
    if t >= HITS[-1]:
        u = t - HITS[-1]; a = 255 if u >= 0.05 else int(255 * u / 0.05); sc_ = 1 + 0.3 * max(0, 1 - u / 0.15)
        texts.append((W / 2, 1250, 'FULL COMBO!', int(76 * sc_), (255, 214, 60), 10, a))   # review: on his body, below the face
    if texts: text_layer(img, texts)
    # surge: the whole tavern shakes, dust and planks fall from the ceiling
    if t >= T_SURGE:
        u = t - T_SURGE; rr = random.Random(f)
        dr = random.Random(5)
        def dust(d):
            for k_ in range(40):
                x = dr.uniform(0, W); v = dr.uniform(500, 1100); s = dr.choice([10, 14, 20, 28])
                y = -40 + v * u + 900 * u * u - dr.uniform(0, 200)
                col = dr.choice([(110, 70, 40), (80, 50, 30), (160, 120, 80), (60, 40, 24)])
                d.rectangle([x, y, x + s * 1.6, y + s], fill=col + (255,))
        layer(img, dust)
        dx, dy = rr.randint(-18, 18), rr.randint(-18, 18)
        big = img.resize((W + 48, H + 85), Image.NEAREST); img = big.crop((24 + dx, 42 + dy, 24 + dx + W, 42 + dy + H))
    img.alpha_composite(HOOK)
    return img
if TEST:
    for ts in sys.argv[1:]: frame(int(float(ts) * FPS)).convert('RGB').save(f't_{ts}.png')
    sys.exit()
w = Writer('v28_noaudio.mp4')
for f in range(NF): w.write(frame(f))
w.close(); json.dump({'events': ev}, open('v28_events.json', 'w')); print('done', NF, DUR, [round(e, 2) for e in EATS], T_SURGE, T_CUT)
