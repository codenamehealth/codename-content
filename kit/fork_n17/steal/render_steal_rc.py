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
SS = 3; FOOT = 78 * SS; HEAD = 65 * SS
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
ICON = {n: face(n, 36) for n in NAMES}; ICONS = {n: face(n, 28) for n in NAMES}
# ---------------- layout
sys.path.insert(0, S + 'pixellab/safezone'); from hook import hook_fade
# hfg12: soft fade, no box; PICK A PLAYER! leaves the hook (unboxed line under the standings for the first 1.6s, as on #093)
HOOK, HB = hook_fade(['WHOEVER GETS 3', 'GUMMIES WINS'], accent=1, size=72)
HUD0 = HB + 10; HUD1 = HUD0 + 92
CX, CY = 482, 1150; RX, RY = 300, 280
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
# ---------------- simulation (items carry ids so the ACV tag can follow one gummy)
N0 = int(os.environ.get('N0', '6')); WINN = 3
def sim(seed, dur=30):
    rnd = random.Random(seed)
    kinds = [GUMK[i % 4] for i in range(N0)]; rnd.shuffle(kinds)
    pile = [(i, k) for i, k in enumerate(kinds)]; bases = {n: [] for n in NAMES}
    ag = {}
    for n in NAMES:
        bx, by = BASE[n]; x, y = clampxy(bx, by + 24)
        ag[n] = dict(x=x, y=y, vx=0.0, vy=0.0, carry=None, tgt=None, spd=rnd.uniform(290, 340), ph=rnd.uniform(0, 6.3),
                     greedy=rnd.random() < 0.5, dist=0.0, mode='down', retarget=0.0)
    frames = []; events = []; steals = 0; winner = None; leaders = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if winner is None:
            for n, s in ag.items():
                if s['carry'] is not None: s['tgt'] = ('home', n)
                elif pile: s['tgt'] = ('pile', None)
                else:
                    if s['tgt'] is None or s['tgt'][0] != 'base' or not bases[s['tgt'][1]] or t > s['retarget']:
                        opts = [m for m in NAMES if m != n and bases[m]]
                        if opts:
                            if s['greedy']: mx = max(len(bases[m]) for m in opts); opts = [m for m in opts if len(bases[m]) == mx]
                            m = min(opts, key=lambda m: math.hypot(BASE[m][0] - s['x'], BASE[m][1] - s['y']) + rnd.uniform(0, 160))
                            s['tgt'] = ('base', m); s['retarget'] = t + rnd.uniform(0.8, 1.6)
                        else: s['tgt'] = ('home', n)
                kind, who = s['tgt']
                tx, ty = (CX, CY + 20) if kind == 'pile' else (BASE[who][0], BASE[who][1] + 24)
                dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                sp = s['spd'] * (1 + 0.18 * math.sin(1.3 * t + s['ph'])) * (0.9 if s['carry'] else 1.0)
                if L < 70: sp *= L / 70 + 0.3
                wob = 0.25 * math.sin(2.7 * t + s['ph'] * 2)
                ux, uy = dx / L, dy / L; ux, uy = ux - uy * wob, uy + ux * wob
                s['vx'] += (ux * sp - s['vx']) * 0.2; s['vy'] += (uy * sp - s['vy']) * 0.2
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                for m, o in ag.items():
                    if m == n: continue
                    ddx, ddy = nx - o['x'], (ny - o['y']) * 1.5; dd = math.hypot(ddx, ddy)
                    if 0 < dd < 76: nx += ddx / dd * (76 - dd) * 0.4; ny += ddy / dd * (76 - dd) * 0.25
                nx, ny = clampxy(nx, ny)
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
                v = math.hypot(s['vx'], s['vy']) or 1; s['mode'] = 'down' if abs(s['vy']) > 0.75 * v else 'side'
                if kind == 'pile' and math.hypot(CX - s['x'], CY + 20 - s['y']) < 90 and pile and s['carry'] is None:
                    s['carry'] = pile.pop(); events.append((t, 'grab', n, None, 0))
                elif kind == 'base' and who != n and math.hypot(BASE[who][0] - s['x'], BASE[who][1] + 24 - s['y']) < 80 and s['carry'] is None:
                    if bases[who]:
                        s['carry'] = bases[who].pop(); steals += 1; events.append((t, 'yoink', n, who, len(bases[who])))
                    s['tgt'] = None
                elif kind == 'home' and math.hypot(BASE[n][0] - s['x'], BASE[n][1] + 24 - s['y']) < 72 and s['carry'] is not None:
                    bases[n].append(s['carry']); s['carry'] = None; c_ = len(bases[n])
                    if c_ == 2 and any(len(bases[m]) >= 2 for m in NAMES if m != n): c_ = -2   # not the only one at 2: plain +1
                    events.append((t, 'drop', n, None, c_)); s['tgt'] = None
                    if len(bases[n]) >= WINN: winner = (n, t)
            cnt = {n: len(bases[n]) for n in NAMES}; mx = max(cnt.values())
            if mx > 0:
                lead = [n for n in NAMES if cnt[n] == mx]
                if len(lead) == 1 and (not leaders or leaders[-1] != lead[0]): leaders.append(lead[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], carry=s['carry'], dist=s['dist'], mode=s['mode']) for n, s in ag.items()},
                       list(pile), {n: list(b) for n, b in bases.items()}, steals))
        if winner and t > winner[1] + 2: break
    return frames, events, winner, steals, leaders
def score(seed):
    fr, ev, win, st, ld = sim(seed)
    if not win: return None
    tw = win[1]; final = fr[-1][2]
    second = sorted((len(b) for n, b in final.items() if n != win[0]), reverse=True)[0]
    twos = sum(1 for e in ev if e[1] == 'drop' and e[4] == 2)
    if not (12.4 < tw < 13.8) or st < 8 or len(set(ld)) < 3 or second < 2 or twos < 3 or twos > 6: return None
    return round(tw, 2), win[0], st, len(set(ld)), ld, twos
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, WIN, STEALS, LEAD = sim(SEED)
print('winner', WIN, 'steals', STEALS, 'leaders', LEAD)
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
win = WIN[0]; T_WIN = WIN[1]; VICF = gif(VIC[win], 400)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
HOLD = 1.3; NMAIN = int(round((T_WIN + HOLD) * FPS)); NTAIL = 6; NF = NMAIN + NTAIL
# ---------------- stamps: laid out once, never overlapping
F64 = F(64); F56 = F(56); F44 = F(44)
STAMPS = []   # (t0, t1, x, y, text, color, font, plate)
_d = ImageDraw.Draw(Image.new('L', (1, 1)))
for (te, kind, n, who, c) in EV:
    if kind == 'grab' or te >= T_WIN - 0.01: continue
    s = FR[min(int(round(te * FPS)), len(FR) - 1)][0][n]
    if kind == 'yoink': txt, col, fnt, plate = 'YOINK!', (255, 220, 60), F64, False
    elif c == 2: txt, col, fnt, plate = '2/3!', (255, 214, 60), F64, True
    elif c in (1, -2): txt, col, fnt, plate = '+1', RING[n], F64, False
    else: continue
    w = _d.textlength(txt, font=fnt) + (40 if plate else 16); h = fnt.size + (36 if plate else 16)
    placed = None
    for dy in (0, -100, 100, -200, 200):
        y = s['y'] - HEAD - 30 - h + dy
        y = min(max(y, HUD1 + 10), 1490 - h - 40)
        xx = min(max(s['x'], 70 + w / 2), (1025 if y + h < 1110 else 887) - w / 2)
        box = (xx - w / 2, y, xx + w / 2, y + h + 40)
        ok = all(not (te < o[1] and o[0] < te + 0.9 and box[0] < o[8][2] and o[8][0] < box[2] and box[1] < o[8][3] and o[8][1] < box[3]) for o in STAMPS)
        if ok: placed = (xx, y, box); break
    if placed is None:
        if kind == 'drop' and c in (1, -2): continue
        xx, y, box = placed or (s['x'], s['y'] - HEAD - 100, None)
    else: xx, y, box = placed
    STAMPS.append((te, te + 0.9, xx, y, txt, col, fnt, plate, box or (0, 0, 0, 0), n))
print('stamps', len(STAMPS), [(round(s[0], 2), s[4], s[9]) for s in STAMPS])
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', os.path.join(HERE, 'steal_rc_noaudio.mp4')], stdin=subprocess.PIPE)
out_ev = []
PILE_POS = [(-54, -28), (48, -38), (-12, 22), (64, 30), (-74, 36), (10, -64), (84, -10), (-96, -6)]
BSLOT = [(-40, -22), (40, -26), (0, 6)]
ACV_ID = next(i for i, k in FR[0][1] if k == 'acv') if any(k == 'acv' for i, k in FR[0][1]) else None
def render(f):
    t = f / FPS; st, pile, bases, steals = FR[min(f, len(FR) - 1)]
    img = GROUND.copy()
    acv_at = None
    for i, (gid, k) in enumerate(pile):
        g = GUM[k]; px, py = PILE_POS[gid]; pos = (int(CX + px - g.width / 2), int(CY + py - g.height / 2)); img.alpha_composite(g, pos)
        if gid == ACV_ID: acv_at = (CX + px, CY + py - g.height / 2)
    for n, b in bases.items():
        bx, by = BASE[n]
        for i, (gid, k) in enumerate(b[:3]):
            g = GUM[k]; px, py = BSLOT[i]; img.alpha_composite(g, (int(bx + px - g.width / 2), int(by + py - g.height / 2 - 20)))
            if gid == ACV_ID: acv_at = (bx + px, by + py - g.height / 2 - 20)
    layer(img, lambda dd: [dd.ellipse([st[n]['x'] - 40, st[n]['y'] - 11, st[n]['x'] + 40, st[n]['y'] + 11], fill=(0, 0, 0, 80)) for n in NAMES])
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if t >= T_WIN: spr = STAND[n] if n == win else FRUN[n][0]
        elif f == 0: spr = STAND[n]
        else:
            ph = int(s['dist'] / 30) % 8
            spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['carry'] is not None:
            gid, k = s['carry']; g = GUM[k]; bob = int(6 * math.sin(t * 10 + x * 0.01))
            gy = int(y - HEAD - g.height + 6 + bob); img.alpha_composite(g, (int(x - g.width / 2), gy))
            if gid == ACV_ID: acv_at = (x, gy)
    # 'ACV GUMMY' tag on first appearance (follows that gummy)
    if False:   # hfg12: 'ACV GUMMY' tag cut (consistency rule: Syeda's ACV gummy art stands on its own)
        jx, jy = acv_at; tag = 'ACV GUMMY'
        L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(L2); tw = d2.textlength(tag, font=F44)
        y0 = max(HUD1 + 10, jy - 112); x0 = max(80, min((1015 if y0 < 1110 else 877) - tw - 36, jx - tw / 2 - 18))
        d2.rounded_rectangle([x0, y0, x0 + tw + 36, y0 + 72], 14, fill=(14, 10, 24, 235), outline=RING['joy'] + (255,), width=5)
        d2.polygon([(jx - 14, y0 + 70), (jx + 14, y0 + 70), (jx, y0 + 98)], fill=RING['joy'] + (255,))
        d2.text((x0 + 18, y0 + 14), tag, font=F44, fill=(255, 255, 255), stroke_width=5, stroke_fill=(10, 6, 18))
        img.alpha_composite(L2)
    # stamps
    if f < NMAIN:
        PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(PL)
        for (t0, t1, xx, y, txt, col, fnt, plate, box, n) in STAMPS:
            u = t - t0
            if 0 <= u < t1 - t0:
                if plate and len(bases[n]) < 2 and u > 0.2: continue   # '2/3!' leaves as soon as that gummy gets stolen
                a = int(255 * min(1, (t1 - t0 - u) / 0.25)); sc_y = max(HUD1 + 26, y - u * 36)
                if False:   # hfg12: plate behind 2/3! dropped (text kept)
                    w = d.textlength(txt, font=fnt)
                    d.rounded_rectangle([xx - w / 2 - 20, sc_y - 16, xx + w / 2 + 20, sc_y + fnt.size + 18], 14, fill=(14, 10, 24, int(a * 0.9)), outline=RING[n] + (a,), width=6)
                ctext(d, xx, sc_y, txt, fnt, col, 8, a)
        img.alpha_composite(PL)
    # header backdrop + HUD
    img.alpha_composite(HUB[int(t * 6) % len(HUB)], (0, 0))
    if T_WIN <= t and f < NMAIN:
        u = t - T_WIN; a = min(1, u / 0.25)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(150 * a))), (0, 0))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1180 - vf.height))
        d = ImageDraw.Draw(img, 'RGBA'); ctext(d, 478, 1220, LABEL[win] + ' WINS!', F(72) if len(LABEL[win]) < 8 else F(60), (255, 214, 60), 10)
        rr = random.Random(f)
        for _ in range(40):
            cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H
            d.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120)]))
    layer(img, lambda dd: dd.rectangle([0, HUD0, W, HUD1], fill=(14, 10, 24, 190)))   # hfg12: standings on an edge-to-edge strip (no box/border)
    if t < 1.6 and f < NMAIN or f == 0:
        layer(img, lambda dd: ctext(dd, W / 2, HUD1 + 22, 'PICK A PLAYER!', F(56), (255, 255, 255), 8, int(255 * min(1, (1.6 - t) / 0.25)) if 0 < t else 255))
    d = ImageDraw.Draw(img)
    cw = (1025 - 70) / 4
    for i, n in enumerate(NAMES):
        x0 = 70 + cw * i; ic = ICON[n]; cnt = len(bases[n])
        img.alpha_composite(ic, (int(x0 + 14), int(HUD0 + (HUD1 - HUD0 - ic.height) / 2)))
        col = (255, 214, 60) if cnt == 2 else (RING[n] if cnt < 2 else (255, 255, 255))
        if t >= T_WIN and n == win and f < NMAIN: col = (255, 214, 60)
        d.text((x0 + 14 + ic.width + 12, HUD0 + (HUD1 - HUD0 - 44) / 2), f'{cnt}/3', font=F44, fill=col, stroke_width=5, stroke_fill=(10, 6, 18))
        if t >= T_WIN and n == win and f < NMAIN:
            d.rounded_rectangle([x0 + 6, HUD0 + 6, x0 + cw - 6, HUD1 - 6], 14, outline=(255, 214, 60), width=6)
    img.alpha_composite(HOOK)
    return img
for (te, kind, n, who, c) in EV:
    if te <= T_WIN + 0.001: out_ev.append((round(te, 3), {'yoink': 'boing', 'grab': 'coin_8bit', 'drop': 'twinkle'}[kind]))
out_ev.append((round(T_WIN, 3), 'victory'))
F0 = render(0).convert('RGB').tobytes()
for f in range(NF):
    fr = F0 if (f == 0 or f >= NMAIN) else render(f).convert('RGB').tobytes()
    ff.stdin.write(fr)
    if f % 15 == 0: Image.frombytes('RGB', (W, H), fr).resize((270, 480)).save(os.path.join(HERE, f'prevs/p_{f:04d}.png'))
ff.stdin.close(); ff.wait()
json.dump({'events': out_ev}, open(os.path.join(HERE, 'steal_rc_events.json'), 'w'))
print('done', round(NF / FPS, 2), 'T_WIN', round(T_WIN, 2))
