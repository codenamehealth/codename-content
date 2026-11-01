# #100 First to the top wins: safe zone + hook, Hollow climber removed (Hollow rule), gummy powers per SPEC 12.
# rc12 review recut: climbing from frame 0 (countdown cut), shorter climb (finish ~13s), SLEEP stops everyone else (cancels SPEED),
# big one-at-a-time stamps, 48px altitude chips + leader glow, COMMENT YOUR PICK in the band, ACV gloss + tag, 1.3s win hold then loop.
import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
sys.path.insert(0, SP + 'fork_rc12'); from rc12 import *
HOOK, HB = hook_layer2(['FIRST TO', 'THE TOP WINS'], accent=1, sub='COMMENT YOUR PICK'); print('hook bottom', HB)
B = SP + 'fork_b10/'; OUT = SP + 'fork_rc12/v100/'
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240)}
GK = {'joy': 'acv', 'cyrus': 'mush', 'cleo': 'cre', 'ray': 'mel'}
POW = {'joy': 'SHIELD!', 'cyrus': 'SPEED!', 'cleo': 'STRONG!', 'ray': 'SLEEP!'}
LANE_X = {n: 196 + i * 208 for i, n in enumerate(NAMES)}     # stalk x; the climber's body is ~30px left of it
CLIMB_D = int(os.environ.get('CD', 2800)); GROUND = 6300; TOP_Y = GROUND - CLIMB_D; WH = GROUND + 520
T_GO = 0.0
def sim(seed):
    rnd = random.Random(seed); cl = {}
    for n in NAMES:
        cl[n] = dict(y=float(GROUND), base=rnd.uniform(214, 246), ph=rnd.uniform(0, 6.3), speed=-9.0, strong=-9.0, shield=False, stun=-9.0, sleep=-9.0, fin=None, dist=0.0)
    slimes = []
    for n in NAMES:
        for k in range(rnd.choice([2, 3])): slimes.append(dict(lane=n, t0=rnd.uniform(1.2, 11), y=None, hit=None, done=False, how=None))
    gums = []
    for n in NAMES:
        for h in sorted(rnd.sample(range(450, CLIMB_D - 350, 150), rnd.choice([2, 3]))): gums.append(dict(lane=n, y=GROUND - h, got=None))
    frames = []; events = []
    for f in range(int(45 * 30)):
        t = f / 30; dt = 1 / 30
        if t >= T_GO:
            lead = min(c['y'] for c in cl.values())
            for n, c in cl.items():
                if c['fin'] is not None: continue
                sp = c['base'] * (1 + 0.2 * math.sin(0.8 * t + c['ph']) + 0.1 * math.sin(2.1 * t + 2 * c['ph']))
                gap = c['y'] - lead
                if gap < 1: sp *= 0.95
                elif gap > 500: sp *= 1.08
                if t - c['speed'] < 1.4: sp *= 1.75
                if t - c['strong'] < 3.0: sp *= 1.12
                if t - c['stun'] < 0.45 or t - c['sleep'] < 1.0: sp = 0.0
                ny = c['y'] - sp * dt; c['dist'] += c['y'] - ny; c['y'] = ny
                for g in gums:
                    if g['lane'] == n and g['got'] is None and c['y'] <= g['y']:
                        g['got'] = t; events.append((t, 'gum', n))
                        if n == 'cyrus': c['speed'] = t
                        elif n == 'cleo': c['strong'] = t
                        elif n == 'joy': c['shield'] = True
                        else:
                            for m, o in cl.items():
                                if m == n or o['fin'] is not None: continue
                                if o['shield']: o['shield'] = False; events.append((t, 'blocked', m))
                                else: o['sleep'] = t; o['speed'] = -9.0; events.append((t, 'zzz', m))   # rc12: asleep = stopped, SPEED ends
                if c['y'] <= TOP_Y: c['y'] = TOP_Y; c['fin'] = t; events.append((t, 'fin', n))
            for s in slimes:
                if s['done'] or t < s['t0']: continue
                c = cl[s['lane']]
                if s['y'] is None: s['y'] = c['y'] - 1150
                s['y'] += 300 * dt
                if c['fin'] is None and s['hit'] is None and s['y'] >= c['y'] - 230:
                    s['hit'] = t; s['done'] = True
                    if t - c['strong'] < 3.0: s['how'] = 'smash'; events.append((t, 'smash', s['lane']))
                    elif c['shield']: c['shield'] = False; s['how'] = 'blocked'; events.append((t, 'blocked', s['lane']))
                    else: c['stun'] = t; s['how'] = 'pow'; events.append((t, 'pow', s['lane']))
                if s['y'] > GROUND: s['done'] = True
        frames.append({n: dict(y=c['y'], speed=c['speed'], strong=c['strong'], shield=c['shield'], stun=c['stun'], sleep=c['sleep'], fin=c['fin'], dist=c['dist']) for n, c in cl.items()})
        if all(c['fin'] is not None for c in cl.values()) or (any(c['fin'] for c in cl.values()) and t > min(c['fin'] for c in cl.values() if c['fin']) + 3.4): break
    return frames, events, slimes, gums
def leaders(frames):
    out = []
    for fr in frames[int(T_GO * 30):]:
        n = min(NAMES, key=lambda k: fr[k]['y'])
        if not out or out[-1] != n: out.append(n)
    return out
def score(seed):
    fr, ev, sl, gm = sim(seed)
    fins = sorted((e[0], e[2]) for e in ev if e[1] == 'fin')
    if not fins: return None
    tw, win = fins[0]
    if not (12.3 < tw < 14.0) or win != 'cyrus': return None
    st_y = sorted(fr[int(tw * 30)][n]['y'] for n in NAMES); margin = st_y[1] - st_y[0]
    ld = leaders(fr); kinds = set(e[1] for e in ev)
    if margin > 200 or len(ld) < 5 or not {'smash', 'blocked', 'zzz', 'pow'} <= kinds: return None
    return round(tw, 2), win, len(ld), round(margin), sum(1 for e in ev if e[1] == 'zzz')
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(s)
        if r: print(s, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1]); FR, EV, SL, GM = sim(SEED)
fins = sorted((e[0], e[2]) for e in EV if e[1] == 'fin'); T_WIN, WIN = fins[0]
print('winner', WIN, round(T_WIN, 2), 'leaders', leaders(FR), [(round(e[0], 1), e[1], e[2]) for e in EV if e[1] != 'fin'])
# ---------------- art
CLIMB = {g: seq(B + f'{g}_climb', 3, 1, 9) for g in NAMES}; CLIMB['ray'] = seq(B + 'ray_climb2', 3, 1, 9)
STAND = {g: seq(SP + f'pixellab/maze/anim/{g}_frun', 3, 0, 1)[0] for g in NAMES}
def nored(im):
    a = np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
SL_IDLE = [nored(up(Image.open(p).convert('RGBA'), 2)) for p in sorted(glob.glob(SP + 'pixellab/race/slime_idle_c/*.png'))[1:]]
DUST = crop(Image.open(SP + 'pixellab/king/dust_cands/00.png').convert('RGBA'))
STALK = up(crop(Image.open(sorted(glob.glob(B + 'stalk/*.png'))[2]).convert('RGBA').crop((0, 0, 64, 142))), 2)
CLOUDS = [crop(Image.open(p).convert('RGBA')) for p in sorted(glob.glob(B + 'cloud/*.png'))[:8]]
CTOP = crop(Image.open(sorted(glob.glob(B + 'cloudtop/*.png'))[0]).convert('RGBA'))
GUM = {n: gummy(GK[n], 3) for n in NAMES}; GUM['joy'] = up(gummy_src('acv'), 3)   # rc12: ACV gummy gloss
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png'}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 32) for n in NAMES}
rng = random.Random(3)
SKY = np.zeros((WH, W, 3), np.uint8)
cols = [(0, (255, 214, 150)), (0.12, (255, 190, 170)), (0.35, (150, 190, 255)), (0.75, (120, 200, 255)), (1.0, (170, 225, 255))]
for y in range(WH):
    u = 1 - y / WH
    for k in range(len(cols) - 1):
        if cols[k][0] <= u <= cols[k + 1][0]:
            a = (u - cols[k][0]) / (cols[k + 1][0] - cols[k][0]); c = [int(cols[k][1][i] * (1 - a) + cols[k + 1][1][i] * a) for i in range(3)]; break
    SKY[y] = c
WORLD = Image.fromarray(SKY).convert('RGBA')
for k in range(42):
    c = rng.choice(CLOUDS); s = rng.choice([3, 4, 5]); c2 = up(c, s)
    c2.putalpha(c2.getchannel('A').point(lambda p: int(p * 0.85)))
    WORLD.alpha_composite(c2, (rng.randint(-150, W - 100), rng.randint(200, GROUND - 1700)))
def stalks(img, y_lo, off):
    for n in NAMES:
        x = LANE_X[n]; y = GROUND + 60; k = 0
        while y > y_lo:
            seg = STALK if k % 2 == 0 else STALK.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(seg, (int(x - seg.width / 2), int(y - seg.height - off))); y -= seg.height - 4; k += 1
stalks(WORLD, TOP_Y + 60, 0)
for k in range(8):
    c = up(CTOP, 4); WORLD.alpha_composite(c, (k * 170 - 160 + (k % 2) * 40, TOP_Y - c.height // 2 - 40 + (k % 3) * 18))
FOREST = [f.crop((420, 0, 420 + 1080, 1080)) for f in bg_frames('found_hd.gif', (1920, 1080), step=2)]
FADE = Image.fromarray(np.tile(np.clip(np.arange(1080) * 255 // 320, 0, 255).astype(np.uint8)[:, None], (1, W)), 'L')
FOREST_Y = GROUND - 735          # forest path (src y ~735) lines up with the climbers' feet
# ---------------- render
END = T_WIN + 1.5; NF = int(END * 30)   # rc12: win held 1.5s, then the reel loops to frame 0
# rc12: one stamp at a time (60px on a dark plate); gummy powers first, BLOCKED!/SMASH! queued, POW! dropped when busy
SEV = []
for (te, kind, n) in EV:
    if kind == 'gum': SEV.append((te, POW[n], RING[n], n, 0, 3, 0.8))
    elif kind == 'blocked': SEV.append((te, 'BLOCKED!', (150, 255, 150), n, 0, 2, 0.6))
    elif kind == 'smash': SEV.append((te, 'SMASH!', (255, 170, 90), n, 0, 2, 0.6))
    elif kind == 'pow': SEV.append((te, 'POW!', (255, 255, 255), n, 0, 1, 0.5))
STAMPS = Stamps().build([e for e in SEV if e[0] < T_WIN])
print('stamps', [(round(a, 2), round(b, 2), tx) for a, b, tx, *_ in STAMPS])
TAG = [None]
CAM0 = GROUND - 1480; CAM_MIN = TOP_Y - 1000
wr = Writer(OUT + 'noaudio.mp4'); out_ev = []; cam = CAM0
def scr(y): return int(y - cam)
VICF = vic(WIN, 340)
def pop_x(n): return min(max(LANE_X[n] - 30, 170), 790)
for f in range(NF):
    t = f / 30; st = FR[min(f, len(FR) - 1)]
    ys_ = sorted(st[n]['y'] for n in NAMES); lead_y, last_y = ys_[0], ys_[-1]
    target = max(lead_y - 1150, min(lead_y - 1000, last_y - 1490)) if t >= T_GO else CAM0
    target = max(CAM_MIN, min(CAM0, target))
    cam += (target - cam) * 0.08
    img = WORLD.crop((0, int(cam), W, int(cam) + H)).copy()
    fy = scr(FOREST_Y)
    if fy < H:
        fo = FOREST[int(t * 6) % len(FOREST)].copy(); fo.putalpha(FADE); img.alpha_composite(fo, (0, fy))
        if fy + 1080 < H: img.alpha_composite(fo.crop((0, 1080 - (H - fy - 1080), W, 1080)).transpose(Image.FLIP_TOP_BOTTOM), (0, fy + 1080))   # rc12: no bare strip under the forest
        for n in NAMES:
            x = LANE_X[n]; y = GROUND + 60; k = 0
            while y > GROUND - 1100:
                seg = STALK if k % 2 == 0 else STALK.transpose(Image.FLIP_LEFT_RIGHT)
                img.alpha_composite(seg, (int(x - seg.width / 2), scr(y - seg.height))); y -= seg.height - 4; k += 1
    # gummies on the stalks
    TAGD = []
    for g in GM:
        if g['got'] is not None and t >= g['got']:
            u = t - g['got']
            if u < 0.5:
                def burst(d, g=g, u=u):
                    for q in range(8):
                        a = q * 0.785; rr = 20 + 120 * u; sx, sy = LANE_X[g['lane']] + rr * math.cos(a), scr(g['y'] - 80) + rr * math.sin(a)
                        d.rectangle([sx - 6, sy - 6, sx + 6, sy + 6], fill=RING[g['lane']] + (int(255 * (1 - u / 0.5)),))
                layer(img, burst)
            continue
        gs = GUM[g['lane']]; bob = int(5 * math.sin(t * 4 + g['y']))
        gx, gy = LANE_X[g['lane']], scr(g['y'] - 90) + bob
        if g['lane'] == 'joy' and TAG[0] is None and HB + 320 < gy < 1250: TAG[0] = (t, id(g))
        if TAG[0] and TAG[0][1] == id(g) and 0 <= t - TAG[0][0] < 1.1: TAGD.append((gx, gy - gs.height // 2 - 6, int(255 * min(1, (1.1 - (t - TAG[0][0])) / 0.2))))
        if -100 < gy < H + 100:
            layer(img, lambda d: d.ellipse([gx - 44, gy - 44, gx + 44, gy + 44], fill=(255, 240, 180, 90)))
            img.alpha_composite(gs, (int(gx - gs.width / 2), int(gy - gs.height / 2)))
    # slimes sliding down
    for s in SL:
        if t < s['t0']: continue
        c0 = FR[min(int(s['t0'] * 30), len(FR) - 1)][s['lane']]['y'] - 1150
        sy = c0 + 300 * (t - s['t0'])
        if s['hit'] is not None and t >= s['hit']:
            u = t - s['hit']
            if s['how'] == 'smash' and u < 0.8:      # punched clean off the stalk
                sp = SL_IDLE[0].rotate(-u * 900, expand=True); dx = 420 * u * (1 if LANE_X[s['lane']] < 540 else -1)
                img.alpha_composite(sp, (int(LANE_X[s['lane']] + dx - sp.width / 2), int(scr(sy) - 120 - 300 * u + 500 * u * u)))
            elif u < 0.4:
                du = up(DUST, 1); du.putalpha(du.getchannel('A').point(lambda p, u=u: int(p * (1 - u / 0.4))))
                img.alpha_composite(du, (LANE_X[s['lane']] - du.width // 2, scr(sy) - du.height // 2))
            continue
        if sy > GROUND: continue
        sp = SL_IDLE[int(t * 10) % len(SL_IDLE)]
        img.alpha_composite(sp, (LANE_X[s['lane']] - sp.width // 2, scr(sy) - sp.height + 20))
    # climbers
    for n in NAMES:
        c = st[n]; x = LANE_X[n]; y = c['y']
        stopped = (t - c['stun'] < 0.45) or (t - c['sleep'] < 1.0)
        if t < T_GO: spr = STAND[n]; yy = GROUND
        else: spr = CLIMB[n][int(c['dist'] / 26) % 8]; yy = y
        fin = c['fin'] is not None and t >= c['fin']
        if fin: spr = STAND[n]; yy = TOP_Y - 40
        if t < T_GO or fin: sx, sy = int(x - 30 - spr.width / 2), scr(yy) - 234
        else: sx, sy = int(x - 165), scr(yy) - 249
        cx_, cy_ = x - 30, sy + 140
        if not fin and t >= T_GO:
            if 0 <= t - c['speed'] < 1.4:       # SPEED: streaks + dust trail
                def streak(d, x=x, sy=sy):
                    for q in range(5):
                        o = (int(t * 30) * 23 + q * 37) % 90
                        d.rectangle([x - 100 + q * 34, sy + 200 + o, x - 94 + q * 34, sy + 260 + o], fill=(255, 200, 110, 190))
                    for q in range(4):
                        d.ellipse([x - 60 + q * 20, sy + 250 + q * 14, x - 30 + q * 20, sy + 280 + q * 14], fill=(240, 220, 180, 150))
                layer(img, streak)
            if 0 <= t - c['strong'] < 3.0:      # STRONG: rc12 orange/red power flames (the blue bubble read like a shield)
                def flames(d, cx_=cx_, cy_=cy_):
                    for q in range(12):
                        a_ = q * 0.5236; fl = 26 + 14 * math.sin(t * 18 + q * 1.7)
                        bx, by = cx_ + 95 * math.cos(a_), cy_ + 115 * math.sin(a_)
                        d.polygon([(bx - 12, by + 8), (bx + 12, by + 8), (bx, by - fl)], fill=(255, 120 + 60 * (q % 2), 40, 210))
                layer(img, flames)
        img.alpha_composite(spr, (sx, sy))
        if not fin and c['shield']:            # SHIELD: green bubble
            layer(img, lambda d: d.ellipse([cx_ - 118, cy_ - 132, cx_ + 118, cy_ + 132], fill=(120, 230, 120, 55), outline=(150, 255, 150, 230), width=6))
        if 0 <= t - c['sleep'] < 1.0 and not fin:      # rc12: big Zzz, asleep climbers stop dead
            u = t - c['sleep']
            text_layer(img, [(min(cx_ + 30 + 10 * math.sin(u * 6), 820), sy + 30 - 40 * u, 'Zzz', 58, (215, 175, 255), 8, 255)])
        if 0 <= t - c['stun'] < 0.45:
            u = t - c['stun']
            layer(img, lambda d: d.arc([x - 20, sy - 30, x + 100, sy + 90], 200, 340, fill=(255, 255, 255, int(255 * (1 - u / 0.45))), width=8))
    for (jx_, jy_, a_t) in TAGD: acv_tag(img, jx_, jy_, a=a_t, xmax=880)
    # SLEEP wave from Rayleigh
    for (te, kind, n) in EV:
        if kind == 'gum' and n == 'ray' and 0 <= t - te < 0.6:
            u = t - te; ry = scr(FR[min(int(te * 30), len(FR) - 1)]['ray']['y']) - 110; r = 80 + 900 * u
            layer(img, lambda d: d.ellipse([LANE_X['ray'] - 30 - r, ry - r, LANE_X['ray'] - 30 + r, ry + r], outline=(200, 140, 255, int(220 * (1 - u / 0.6))), width=14))
    # popups
    items = []
    for (te, kind, n) in EV:
        u = t - te
        if 0 <= u < 0.9:
            y = scr(FR[min(int(te * 30), len(FR) - 1)][n]['y']) - 270 - u * 60; a = int(255 * min(1, (0.9 - u) / 0.3)); y = max(y, HB + 150)
        if abs(t - te) < 0.5 / 30:
            snd = {'gum': 'powerup_8bit', 'pow': 'sword_hit', 'fin': 'ding_8bit', 'smash': 'punch', 'blocked': 'boing', 'zzz': None}[kind]
            if kind == 'gum' and n == 'ray': snd = 'twinkle'
            if snd and not any(abs(e[0] - te) < 0.01 and e[1] == snd for e in out_ev): out_ev.append((round(te, 3), snd))
    for (a0, b0, tx, c0, n0, _, pr) in STAMPS:
        if a0 <= t < b0 and t < T_WIN:
            u = t - a0; sc = 1.25 - 0.25 * min(1, u / 0.12); al = int(255 * min(1, (b0 - t) / 0.12))
            sy0 = max(HB + 170, scr(st[n0]['y']) - 390)
            plate(img, LANE_X[n0] - 30, sy0, tx, 60, c0, al, scale=sc)
    # header (under the hook): icons + altitude
    layer(img, lambda d: d.rounded_rectangle([74, HB + 6, 1006, HB + 150], 16, fill=(14, 10, 24, 215)))
    order = sorted(NAMES, key=lambda n: (st[n]['fin'] if st[n]['fin'] else 99, st[n]['y']))
    ld = order[0]; lx = LANE_X[ld] - 30; pa = int(150 + 80 * math.sin(t * 8))      # rc12: the leader's chip glows gold (replaces the tiny 1ST tag)
    if t > 0.5: layer(img, lambda d: d.rounded_rectangle([lx - 100, HB + 12, lx + 100, HB + 144], 14, fill=(255, 214, 60, 55), outline=(255, 214, 60, pa), width=6))
    d = ImageDraw.Draw(img)
    for n in NAMES:
        ix = LANE_X[n] - 30; ic = ICON[n]
        img.alpha_composite(ic, (ix - ic.width // 2, HB + 16))
        pct = int(100 * min(1, (GROUND - st[n]['y']) / CLIMB_D))
        d = ImageDraw.Draw(img); ctext(d, ix, HB + 90, f'{pct}%', F(44), RING[n], 6)   # rc12: 26 -> 44px
    if t < 1.5:          # rc12: no countdown; PICK ONE! over the climb from frame 0
        a_ = int(255 * min(1, (1.5 - t) / 0.3))
        plate(img, 478, 880, 'PICK ONE!', 80, (255, 255, 255), a_, border=(255, 214, 60))
        if f == 0: out_ev.append((0.0, 'go_8bit'))
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        layer(img, lambda dd: dd.rectangle([0, HB + 134, W, H], fill=(8, 6, 14, int(130 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (478 - vf.width // 2, 1180 - vf.height))
        plate(img, 478, 1210, LABEL[WIN] + ' WINS!', 64, (255, 214, 60), int(255 * a))
        plate(img, 478, 1330, 'DID YOURS WIN?', 46, (255, 255, 255), int(255 * a), border=(255, 214, 60))
        def conf(d):
            rr = random.Random(f)
            for _ in range(40):
                cx2, cy2 = rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H
                if cy2 > HB + 134: d.rectangle([cx2, cy2, cx2 + 10, cy2 + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120)]) + (255,))
        layer(img, conf)
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN, 3), 'victory'))
    img.alpha_composite(HOOK)
    wr.write(img)
    pass
wr.close()
json.dump(out_ev, open(OUT + 'ev.json', 'w'))
print('done', round(END, 2), len(out_ev))
