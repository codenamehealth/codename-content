# Recut of pixellab/steal/render_steal_safe.py (review-recut pass, Oct 28)
# - Hollow removed (4 guides, 4 baskets, 4 HUD chips), guides 2x -> 3x, arena re-laid inside the safe zone
# - motion from frame 0, winner ~13s, win hold 1.3s then cut back to the opening state (loop)
# - hook via hook2 (comment prompt "PICK A PLAYER!" as a 52px second line), HUD counts 0/3..3/3, big non-overlapping stamps
import numpy as np, math, random, subprocess, json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S + 'pixellab/steal/'
sys.path.insert(0, S + 'fork_rc_paused'); from hook2 import hook_layer2
FONT = S + 'npmfont/ps/package/files/PressStart2P.ttf'; A = S + 'pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def crop(im): return im.crop(im.getbbox())
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
SS = 4; FOOT = 78 * SS; HEAD = 65 * SS   # n18: guides 3x -> 4x (1.33x)
def seq(d, lo=1, hi=9):
    return [up(Image.open(p).convert('RGBA'), SS) for p in sorted(glob.glob(d + '/*.png'))[lo:hi]]
SRUN = {g: seq(P + f'../race/{g}_run') for g in NAMES}
FRUN = {g: seq(P + f'../maze/anim/{g}_frun') for g in NAMES}
STAND = {g: seq(P + f'../maze/anim/{g}_frun', 0, 1)[0] for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
GUMK = ['mush', 'acv', 'mel', 'cre']
def gum_src(k):
    g0 = Image.open(P + f'../gummies/pick_{k}.png').convert('RGBA')
    if k == 'acv':   # gummy gloss on Syeda's apple-shaped ACV gummy so it reads as a gummy
        gl = Image.new('RGBA', g0.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).arc([5, 7, 26, 29], 290, 350, fill=(255, 240, 230, 170), width=2)
        gl.putalpha(Image.fromarray(np.minimum(np.array(gl.getchannel('A')), np.array(g0.getchannel('A')))))
        g0.alpha_composite(gl)
    return g0
GUMS = {k: gum_src(k) for k in GUMK}
GUM = {k: up(GUMS[k], 3) for k in GUMK}
GUMH = {k: up(GUMS[k], 2) for k in GUMK}
def pick(d, i): return crop(Image.open(P + f'{d}/{i:02d}.png').convert('RGBA'))
BASKET = up(pick('basket', 1), 4); BLANKET = up(pick('blanket', 0), 4)
BARREL = up(pick('barrel', 0), 3); CRATE = up(pick('crate', 1), 3); POT = up(pick('flowers', 1), 3)
def face(name, rad):
    im = Image.open(S + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 34) for n in NAMES}; ICONS = {n: face(n, 28) for n in NAMES}
# ---------------- layout
sys.path.insert(0, S + 'pixellab/safezone'); from hook import hook_fade
# hfg12: soft fade, no box; PICK A PLAYER! leaves the hook (unboxed line under the standings for the first 1.6s, as on #093)
HOOK, HB = hook_fade(['CAN YOU SPOT', 'THE THIEF?'], accent=1, size=72)   # n17: job hook
HUD0 = HB + 10; HUD1 = HUD0 + 180   # n18: stacked chips, count digits 44 -> 88px
CX, CY = 482, 1190; RX, RY = 300, 250   # CX 482 = centre of the lower-half safe width (70..887)
BASE = {'joy': (CX, CY - RY), 'cyrus': (CX + RX, CY), 'cleo': (CX, CY + RY), 'ray': (CX - RX, CY)}
YMIN, YMAX = 654 + 8 + HEAD, 1488   # hfg12: sim clamp pinned to the old HUD bottom (654) so the race is bit-identical (Cyrus still wins)
def xr(y): return (1025 if y - HEAD < 1110 else 887) - 62
def clampxy(x, y):
    y = min(max(y, YMIN), YMAX); return min(max(x, 70 + 62), xr(y)), y
# ---------------- arena ground (PixelLab Wang cobble plaza inside grass)
meta = json.load(open(P + 'plaza_meta.json')); sheet = Image.open(P + 'plaza_sheet.png').convert('RGBA')
TILE = {}
for t in meta['tileset_data']['tiles']:
    c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
AY0 = 400; TS = 64; GC, GR = 18, 25
def lowc(i, j):
    x, y = i * TS - 4, AY0 + j * TS
    e = ((x - CX) / 450) ** 2 + ((y - CY) / 470) ** 2
    return e < 1.0 + 0.12 * math.sin(i * 1.7 + j * 0.9)
CORN = [[lowc(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
GROUND = Image.new('RGBA', (W, H), (30, 60, 30, 255))
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1])
        tl = TILE[key]
        if all(key) or not any(key):
            if (i + j) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        GROUND.alpha_composite(tl, (i * TS - 4, AY0 + j * TS))
PROPS = [(BARREL, 985, 760), (CRATE, 990, 1000), (POT, 975, 1620), (BARREL, 90, 1640), (CRATE, 970, 1780), (POT, 120, 1800)]
for im, x, y in PROPS: GROUND.alpha_composite(im, (x - im.width // 2, y - im.height // 2))
GROUND.alpha_composite(BLANKET, (CX - BLANKET.width // 2, CY - BLANKET.height // 2))
layer(GROUND, lambda dd: [dd.ellipse([bx - 104, by - 62, bx + 104, by + 62], fill=RING[n] + (110,), outline=RING[n] + (255,), width=6) for n, (bx, by) in BASE.items()])
for n, (bx, by) in BASE.items():
    GROUND.alpha_composite(BASKET, (int(bx - BASKET.width / 2), int(by - BASKET.height / 2 - 8)))
# ---------------- header backdrop: Liza's village
hub = Image.open(A + 'hub.gif'); HUB = []
for i in range(0, hub.n_frames, 2):
    hub.seek(i); fr_ = hub.convert('RGB').crop((0, 60, 1920, 60 + 782)).resize((W, HUD0 + 2), Image.NEAREST)   # hfg12: village runs down to the standings strip (no grass gap)
    HUB.append(ImageEnhance.Brightness(fr_).enhance(0.62).convert('RGBA'))
VIC = {'joy': 'vic_Victory_Pose.gif', 'cyrus': 'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', 'cleo': 'vic_victoryPose.gif', 'ray': 'vic_victoryPose_1.gif'}
def gif(p, h):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
# ======================= n17: scripted 'spot the thief' choreography =======================
# Rayleigh secretly steals from Joy, then from Cleo, reaches 3/3... then carries all 3 to a hungry slime.
PILE_POS = [(-44, -26), (40, -34), (-8, 16), (54, 26), (-60, 30), (8, -58), (70, -8), (-76, -4)]
BSLOT = [(-34, -20), (34, -24), (0, 4)]
SIDE = {'joy': 120, 'cyrus': -120, 'cleo': 120, 'ray': 120}   # stand beside the basket so its gummies stay visible
HOME = {n: (BASE[n][0] + SIDE[n], BASE[n][1] + (70 if n == 'joy' else 24)) for n in NAMES}
PSPOT = {n: (CX + 0.36 * (BASE[n][0] - CX), CY + 20 + 0.36 * (BASE[n][1] - CY)) for n in NAMES}
SLX, SLY = 176, 1446                    # slime feet (bottom-left of the plaza, solid ground)
RAYFEED = (330, 1365)
KINDS = ['mush', 'acv', 'mel', 'cre', 'cre', 'mush', 'acv', 'mel']
gk = {i: KINDS[i] for i in range(8)}
# timeline builder: each guide's script -> list of segments (t0, t1, x0, y0, x1, y1) + timed actions
class Actor:
    def __init__(s, n, t, x, y): s.n = n; s.t = t; s.x = x; s.y = y; s.seg = []; s.act = []
    def go(s, x, y, v):
        d = math.hypot(x - s.x, y - s.y); dt = d / v
        s.seg.append((s.t, s.t + dt, s.x, s.y, x, y)); s.t += dt; s.x, s.y = x, y; return s
    def wait(s, dt): s.seg.append((s.t, s.t + dt, s.x, s.y, s.x, s.y)); s.t += dt; return s
    def until(s, t): return s.wait(max(0, t - s.t))
    def do(s, kind, arg=None, dt=0.1): s.act.append((s.t, kind, arg)); return s.wait(dt)
    def pos(s, t):
        for (a, b, x0, y0, x1, y1) in s.seg:
            if a <= t < b:
                u = (t - a) / (b - a) if b > a else 1; return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, (x1 - x0) / max(1e-6, b - a), (y1 - y0) / max(1e-6, b - a)
        return s.x, s.y, 0.0, 0.0
V = {'joy': 400, 'cyrus': 440, 'cleo': 390, 'ray': 420}
AC = {n: Actor(n, 0.0, PSPOT[n][0] + 0.5 * (HOME[n][0] - PSPOT[n][0]), PSPOT[n][1] + 0.5 * (HOME[n][1] - PSPOT[n][1])) for n in NAMES}   # frame 0: already running home with a gummy
# frame 0: each already holds one gummy from the pile (ids 0-3); pile keeps 4-6 (3) and 7 drops from the sky later
# trip 1: everyone home
for n in NAMES: AC[n].go(*HOME[n], V[n]).do('drop', n)
# trip 2: Joy / Cyrus / Cleo take the last 3 from the pile; Rayleigh sneaks to Joy's basket instead
for n in ['cyrus', 'joy', 'cleo']:
    a = AC[n]; a.go(*PSPOT[n], V[n]).do('grab', 'pile', 0.5 if n == 'joy' else 0.15).go(*HOME[n], V[n]).do('drop', n)
r = AC['ray']; r.wait(0.3).go(BASE['joy'][0] - 120, BASE['joy'][1] + 90, V['ray'])   # n18: low enough that the lifted gummy clears the HUD
T_STEAL1 = r.t; r.do('grab', 'joy', 0.12).go(*HOME['ray'], V['ray']).do('drop', 'ray')
T_JOYQ = T_STEAL1 + 0.15                 # n18: Joy's '?' right when her gummy goes (she's at the pile)
# n18: the slime gets hungry once (rumble + gummy thought bubble), its own beat before the sky gummy
T_HUNGRY = max(T_JOYQ + 0.85, max(AC[n].t for n in NAMES) - 0.1)
# the last gummy falls from the sky onto the blanket
T_FALL = max(max(AC[n].t for n in NAMES) + 0.25, T_HUNGRY + 0.95); G_LAND = T_FALL + 0.53
TOP_Y, LAND_Y = HUD1 + 40, CY + 10
def drop_y(u, top, land, tf=0.53):
    """gravity drop from `top` (at rest) landing on `land` after tf seconds, then two damped bounces (restitution 0.3)."""
    if u < 0: return None
    g = 2 * (land - top) / tf ** 2
    if u < tf: return land - (land - top) * (1 - (u / tf) ** 2)
    u -= tf; v = 0.3 * (2 * (land - top) / tf)
    if u < 2 * v / g: return land - (v * u - 0.5 * g * u * u)
    u -= 2 * v / g; v2 = 0.3 * v
    if u < 2 * v2 / g: return land - (v2 * u - 0.5 * g * u * u)
    return land
def fall_y(t): return drop_y(t - T_FALL, TOP_Y, LAND_Y)
# Joy wins the scramble; Cyrus and Cleo stop short and trudge back; Rayleigh sneaks to Cleo's basket
j = AC['joy']; j.until(G_LAND - 0.1).go(CX, CY - 40, 470); T_JOYGRAB = j.t; j.do('grab', 'sky', 0.15).go(*HOME['joy'], 400).do('drop', 'joy')
for n in ['cyrus', 'cleo']:
    a = AC[n]; a.until(G_LAND - 0.1); tx, ty = PSPOT[n]; a.go(tx + (40 if n == 'cyrus' else 0), ty + (30 if n == 'cleo' else 0), V[n]).until(T_JOYGRAB + 0.45).go(*HOME[n], 240).do('arrive', n)
r.until(G_LAND - 0.1).go(BASE['cleo'][0] - 120, BASE['cleo'][1] + 24, V['ray'])
T_STEAL2 = r.t; r.do('grab', 'cleo', 0.12).go(*HOME['ray'], V['ray']).do('drop', 'ray')
T_RAY3 = r.t
r.wait(0.55).do('grab', 'ray', 0.18).do('grab', 'ray', 0.18).do('grab', 'ray', 0.25)
T_GOFEED = r.t; r.go(*RAYFEED, 330)
T_FEED0 = r.t + 0.15; FEEDS = [T_FEED0 + 0.45 * i for i in range(3)]
r.until(FEEDS[-1] + 0.4)
for k_ in range(3): r.act.append((FEEDS[k_], 'feed', None))
# n18 loop: fresh gummies rain onto the blanket (ids 0-6, the frame-0 set), then cut to frame 0
T_RAIN = FEEDS[-1] + 0.55; RAIN = [(T_RAIN + 0.07 * i, i) for i in [5, 0, 3, 1, 6, 2, 4]]
END = RAIN[-1][0] + 0.53 + 0.32
for a in AC.values(): a.until(END + 1)
print({n: round(a.t, 2) for n, a in AC.items()}, 'steal1', round(T_STEAL1, 2), 'joy home', round(T_JOYQ, 2), 'fall', round(T_FALL, 2), 'steal2', round(T_STEAL2, 2), 'ray3', round(T_RAY3, 2), 'hungry', round(T_HUNGRY, 2), 'feeds', [round(x, 2) for x in FEEDS], 'end', round(END, 2))
# inventory events in time order
ALL = sorted([(t, n, k, arg) for n, a in AC.items() for (t, k, arg) in a.act], key=lambda e: e[0])
def state(t):
    pile = [4, 5, 6]; bases = {n: [] for n in NAMES}; carry = {n: [i] for i, n in enumerate(NAMES)}; sky = 7 if t < T_JOYGRAB else None; fed = 0; last = {}
    if t < T_FALL: sky = None
    for (te, n, k, arg) in ALL:
        if te > t: break
        if k == 'drop' and carry[n]: bases[arg] += carry[n]; carry[n] = []
        elif k == 'grab':
            if arg == 'pile' and pile: carry[n].append(pile.pop())
            elif arg == 'sky': carry[n].append(7)
            elif arg in bases and bases[arg]: carry[n].append(bases[arg].pop())
        elif k == 'feed' and carry[n]: carry[n].pop(); fed += 1
    if T_FALL <= t < T_JOYGRAB: sky = 7
    return pile, bases, carry, sky, fed
SLK = 5   # n18: slime 4x -> 5x
SLIME = [up(Image.open(q).convert('RGBA'), SLK) for q in sorted(glob.glob(P + '../race/slime_idle_c/*.png'))]
SLIMEB = [up(Image.open(q).convert('RGBA'), SLK) for q in sorted(glob.glob(P + '../race/slime_idle3/*.png'))]
GSM = {k: up(GUMS[k], 3) for k in GUMK}
GBUB = up(GUMS['mush'], 4)
def heart(d, x, y, s, col, a):
    bm = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']
    for j_, row in enumerate(bm):
        for i_, c in enumerate(row):
            if c == 'X': d.rectangle([x + (i_ - 3.5) * s, y + j_ * s, x + (i_ - 2.5) * s - 1, y + (j_ + 1) * s - 1], fill=col + (a,))
STAMP3 = T_RAY3
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', os.path.join(HERE, 'noaudio.mp4')], stdin=subprocess.PIPE)
KEEP = {int(v) for v in os.environ.get('KEEP', '').split(',') if v}
QMARK = [('joy', T_JOYQ), ('cleo', T_STEAL2 + 0.15)]   # n18: each '?' lands the moment that guide's gummy goes
def render(f):
    t = f / FPS; pile, bases, carry, sky, fed = state(t)
    img = GROUND.copy()
    for gid in pile:
        g = GSM[gk[gid]]; px, py = PILE_POS[gid]; img.alpha_composite(g, (int(CX + px - g.width / 2), int(CY + py - g.height / 2)))
    for n, b in bases.items():
        bx, by = BASE[n]
        for i, gid in enumerate(b[:3]):
            g = GSM[gk[gid]]; px, py = BSLOT[i]; img.alpha_composite(g, (int(bx + px - g.width / 2), int(by + py - g.height / 2 - 20)))
    # falling gummy + its shadow
    if sky is not None:
        fy = fall_y(t); g = GSM[gk[7]]; sh = max(0.2, min(1, 1 - (LAND_Y - fy) / 600))
        layer(img, lambda dd: dd.ellipse([CX - 40 * sh, LAND_Y - 8 * sh, CX + 40 * sh, LAND_Y + 8 * sh], fill=(0, 0, 0, int(110 * sh))))
    # slime (sits on the plaza from frame 0)
    feeds_done = [ft for ft in FEEDS if ft <= t]
    if feeds_done and t - feeds_done[-1] < 0.47: sl = SLIMEB[min(len(SLIMEB) - 1, int((t - feeds_done[-1]) * 15))]
    else: sl = SLIME[int(t * 8) % len(SLIME)]
    layer(img, lambda dd: dd.ellipse([SLX - 76, SLY - 14, SLX + 76, SLY + 12], fill=(0, 0, 0, 80)))
    uh = t - T_HUNGRY; jx = int(round(5 * math.sin(uh * 75))) if 0 <= uh < 0.5 else 0   # n18: tummy rumble
    img.alpha_composite(sl, (SLX - sl.width // 2 + jx, SLY - 62 * SLK))
    # guides
    pos = {n: AC[n].pos(t) for n in NAMES}
    layer(img, lambda dd: [dd.ellipse([pos[n][0] - 40, pos[n][1] - 11, pos[n][0] + 40, pos[n][1] + 11], fill=(0, 0, 0, 80)) for n in NAMES])
    for n in sorted(NAMES, key=lambda n: pos[n][1]):
        x, y, vx, vy = pos[n]; v = math.hypot(vx, vy)
        if v < 1: spr = STAND[n]
        else:
            ph = int(t * 14) % 8
            spr = FRUN[n][ph] if abs(vy) > 0.75 * v else (SRUNL if vx < 0 else SRUN)[n][ph]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        tossing = n == 'ray' and any(0 <= t - (ft - 0.32) < 0.32 for ft in FEEDS)
        for i, gid in enumerate(carry[n][:-1] if tossing else carry[n]):
            g = GSM[gk[gid]]; bob = int(5 * math.sin(t * 10 + i))
            img.alpha_composite(g, (int(x - g.width / 2), int(y - HEAD - g.height + 6 + bob - i * 48)))
    # tossed gummies (Rayleigh -> slime) on a real arc
    for ft in FEEDS:
        u = t - (ft - 0.32)
        if 0 <= u < 0.32:
            g = GSM[gk[carry['ray'][-1]]] if carry['ray'] else GSM['mel']; s_ = u / 0.32
            x0_, y0_ = RAYFEED[0] - 20, RAYFEED[1] - HEAD - 30; x1_, y1_ = SLX, SLY - 112
            gx_ = x0_ + (x1_ - x0_) * s_; gy_ = y0_ + (y1_ - y0_) * s_ - 160 * 4 * s_ * (1 - s_)
            img.alpha_composite(g, (int(gx_ - g.width / 2), int(gy_ - g.height / 2)))
    if sky is not None:
        fy = fall_y(t); g = GSM[gk[7]]; img.alpha_composite(g, (int(CX - g.width / 2), int(fy - g.height + 10)))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    # '?' over the robbed guide, one at a time
    for n, tq in QMARK:
        u = t - tq
        if 0 <= u < 0.62:
            x, y = pos[n][0], pos[n][1]; a = int(255 * min(1, (0.62 - u) / 0.12)); sc = 1.3 - 0.3 * min(1, u / 0.1)
            ctext(d, x + 20, y - HEAD - 100 - 10 * min(1, u / 0.1), '?', F(int(84 * sc)), RING[n], 10, a)
    # 3/3! when the thief 'wins'
    u = t - STAMP3
    if 0 <= u < 0.9:
        a = int(255 * min(1, (0.9 - u) / 0.15)); bx, by = BASE['ray']; sc = 1.35 - 0.35 * min(1, u / 0.12)   # n18: anchored on Rayleigh's basket
        fs = int(76 * sc); ctext(d, max(70 + 2 * fs + 16, bx + 40), by - 70 - fs / 2, '3/3!', F(fs), (255, 214, 60), 11, a)
    # n18: hungry slime (once): rumble lines then a gummy thought bubble
    uh = t - T_HUNGRY
    if 0 <= uh < 0.5:
        for q in range(3):
            yy = SLY - 40 - q * 26; xx = SLX + 92 + 6 * math.sin(uh * 40 + q)
            d.line([(xx, yy), (xx + 12, yy - 8), (xx + 24, yy), (xx + 36, yy - 8)], fill=(255, 255, 255, 230), width=5)
    if 0.2 <= uh < 0.9:
        a = int(255 * min(1, (uh - 0.2) / 0.1, (0.9 - uh) / 0.12)); bxc, byc = SLX + 130, SLY - 270
        for (ox, oy, r_) in [(-78, 116, 10), (-56, 84, 16)]:
            d.ellipse([bxc + ox - r_, byc + oy - r_, bxc + ox + r_, byc + oy + r_], fill=(255, 255, 255, a), outline=(20, 15, 35, a), width=4)
        d.ellipse([bxc - 92, byc - 74, bxc + 92, byc + 70], fill=(255, 255, 255, a), outline=(20, 15, 35, a), width=5)
        bub_a = a
    # hearts from the fed slime
    for i, ft in enumerate(FEEDS):
        u = t - ft
        if 0 <= u < 1.2:
            for q in range(2 + i):
                hx = SLX - 50 + (q % 3) * 50 + 10 * math.sin(u * 5 + q); hy = SLY - 180 - u * 60 - (q % 2) * 22
                heart(d, hx, hy, 8 + 2 * (i == 2), (255, 90, 130), int(255 * max(0, min(1, (1.2 - u) / 0.4))))
    img.alpha_composite(L)
    if 0.2 <= uh < 0.9:
        gb = GBUB.copy(); gb.putalpha(Image.fromarray((np.array(gb.getchannel('A')) * (bub_a / 255)).astype(np.uint8)))
        img.alpha_composite(gb, (int(SLX + 130 - gb.width / 2), int(SLY - 272 - gb.height / 2)))
    # n18: fresh gummies rain onto the blanket for the loop
    for (tr, gid) in RAIN:
        ry_ = drop_y(t - tr, HUD1 + 20, CY + PILE_POS[gid][1] + 30, 0.5)
        if ry_ is not None:
            g = GSM[gk[gid]]; img.alpha_composite(g, (int(CX + PILE_POS[gid][0] - g.width / 2), int(ry_ - g.height)))
    # header backdrop + standings
    img.alpha_composite(HUB[int(t * 6) % len(HUB)], (0, 0))
    layer(img, lambda dd: dd.rectangle([0, HUD0, W, HUD1], fill=(14, 10, 24, 190)))
    d = ImageDraw.Draw(img); cw = (1025 - 70) / 4
    for i, n in enumerate(NAMES):   # n18: icon on top, count below at 2x (88px digit, 44px '/3')
        xm = 70 + cw * (i + 0.5); ic = ICON[n]; cnt = len(bases[n])
        img.alpha_composite(ic, (int(xm - ic.width / 2), HUD0 + 8))
        col = (255, 214, 60) if cnt >= 3 else RING[n]; ty = HUD0 + 8 + ic.height + 6
        d.text((xm - 88, ty), f'{cnt}', font=F88, fill=col, stroke_width=7, stroke_fill=(10, 6, 18))
        d.text((xm + 4, ty + 40), '/3', font=F44, fill=col, stroke_width=5, stroke_fill=(10, 6, 18))
    img.alpha_composite(HOOK)
    return img
F44 = F(44); F88 = F(88)
NF = int(round(END * FPS))
for f in range(NF):
    im = render(f); ff.stdin.write(im.convert('RGB').tobytes())
    if f in KEEP: im.convert('RGB').save(os.path.join(HERE, f'k_{f:04d}.png'))
ff.stdin.close(); ff.wait()
ev = [(0.0, 'go_8bit')]
for (te, n, k, arg) in ALL:
    if k == 'grab' and arg in ('joy', 'cleo'): ev.append((te, 'swish'))
    if k == 'grab' and arg == 'sky': ev.append((te, 'coin_8bit'))
for n, tq in QMARK: ev.append((tq, 'boing'))
ev += [(T_FALL, 'whoosh_8bit'), (G_LAND, 'jump'), (STAMP3, 'ding_8bit')] + [(ft, 'squish') for ft in FEEDS] + [(FEEDS[-1] + 0.1, 'victory'), (T_HUNGRY, 'squish'), (T_HUNGRY + 0.2, 'poof'), (T_RAIN, 'twinkle')]
for n in NAMES: ev.append((AC[n].act[0][0], 'twinkle')) if n == 'joy' else None
json.dump({'events': sorted((round(a, 3), b) for a, b in ev)}, open(os.path.join(HERE, 'ev.json'), 'w'))
print('done', NF, round(END, 2))
