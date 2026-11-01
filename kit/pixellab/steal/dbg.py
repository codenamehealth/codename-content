import numpy as np, math, random, subprocess, json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'; A = '../../pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def crop(im): return im.crop(im.getbbox())
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
SS = 2; FOOT = 78 * SS
def seq(d, lo=1, hi=9):
    return [up(Image.open(p).convert('RGBA'), SS) for p in sorted(glob.glob(d + '/*.png'))[lo:hi]]
SRUN = {g: seq(f'../race/{g}_run') for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq('../maze/anim/hollow_srun')
FRUN = {g: seq(f'../maze/anim/{g}_frun') for g in NAMES}
STAND = {g: seq(f'../maze/anim/{g}_frun', 0, 1)[0] for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
GUMK = ['mush', 'acv', 'mel', 'cre']
GUM = {k: up(Image.open(f'../gummies/pick_{k}.png').convert('RGBA'), 2) for k in GUMK}
GUMS = {k: Image.open(f'../gummies/pick_{k}.png').convert('RGBA') for k in GUMK}
def pick(d, i): return crop(Image.open(f'{d}/{i:02d}.png').convert('RGBA'))
BASKET = up(pick('basket', 1), 3); BLANKET = up(pick('blanket', 0), 3)
BARREL = up(pick('barrel', 0), 3); CRATE = up(pick('crate', 1), 3); POT = up(pick('flowers', 1), 3)
def face(name, rad):
    im = Image.open('../../syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 34) for n in NAMES}; ICONS = {n: face(n, 22) for n in NAMES}
# ---------------- arena ground from the PixelLab Wang tileset (cobble plaza inside grass)
meta = json.load(open('plaza_meta.json')); sheet = Image.open('plaza_sheet.png').convert('RGBA')
TILE = {}
for t in meta['tileset_data']['tiles']:
    c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
AY0 = 470; TS = 64; GC, GR = 17, 23
CX, CY = 540, AY0 + 700
rng0 = random.Random(5)
def lowc(i, j):
    x, y = i * TS - 4, AY0 + j * TS
    e = ((x - CX) / 470) ** 2 + ((y - CY) / 600) ** 2
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
# props in the grass ring
PROPS = [(BARREL, 70, AY0 + 150), (CRATE, 1000, AY0 + 170), (POT, 60, AY0 + 700), (BARREL, 1020, AY0 + 760), (CRATE, 80, AY0 + 1270), (POT, 1010, AY0 + 1300), (POT, 520, AY0 + 70)]
for im, x, y in PROPS: GROUND.alpha_composite(im, (x - im.width // 2, y - im.height // 2))
GROUND.alpha_composite(BLANKET, (CX - BLANKET.width // 2, CY - BLANKET.height // 2))
# bases in a ring
BASE = {}
for k, n in enumerate(NAMES):
    a = -math.pi / 2 + k * 2 * math.pi / 5
    BASE[n] = (CX + 360 * math.cos(a), CY + 470 * math.sin(a))
gd = ImageDraw.Draw(GROUND, 'RGBA')
for n, (bx, by) in BASE.items():
    gd.ellipse([bx - 84, by - 50, bx + 84, by + 50], fill=RING[n] + (110,), outline=RING[n] + (255,), width=5)
    GROUND.alpha_composite(BASKET, (int(bx - BASKET.width / 2), int(by - BASKET.height / 2 - 6)))
    ic = ICONS[n]; GROUND.alpha_composite(ic, (int(bx - ic.width / 2), int(by + 34)))
# ---------------- simulation
T_START = 2.2; N0 = int(os.environ.get("N0", "8")); WINN = 3
def sim(seed, dur=40):
    rnd = random.Random(seed)
    kinds = [GUMK[i % 4] for i in range(N0)]; rnd.shuffle(kinds)
    pile = list(kinds); bases = {n: [] for n in NAMES}
    ag = {}
    for n in NAMES:
        bx, by = BASE[n]
        ag[n] = dict(x=bx, y=by + 20, vx=0.0, vy=0.0, carry=None, tgt=None, spd=rnd.uniform(300, 345), ph=rnd.uniform(0, 6.3),
                     greedy=rnd.random() < 0.5, dist=0.0, mode='down', retarget=0.0)
    frames = []; events = []; steals = 0; winner = None; leaders = []
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= T_START and winner is None:
            for n, s in ag.items():
                # choose target
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
                tx, ty = (CX, CY) if kind == 'pile' else BASE[who]
                dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                sp = s['spd'] * (1 + 0.18 * math.sin(1.3 * t + s['ph'])) * (0.9 if s['carry'] else 1.0)
                if L < 60: sp *= L / 60 + 0.3
                wob = 0.25 * math.sin(2.7 * t + s['ph'] * 2)
                ux, uy = dx / L, dy / L; ux, uy = ux - uy * wob, uy + ux * wob
                s['vx'] += (ux * sp - s['vx']) * 0.18; s['vy'] += (uy * sp - s['vy']) * 0.18
                nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                for m, o in ag.items():
                    if m == n: continue
                    ddx, ddy = nx - o['x'], (ny - o['y']) * 1.5; dd = math.hypot(ddx, ddy)
                    if 0 < dd < 52: nx += ddx / dd * (52 - dd) * 0.4; ny += ddy / dd * (52 - dd) * 0.25
                s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
                v = math.hypot(s['vx'], s['vy']) or 1; s['mode'] = 'down' if s['vy'] > 0.75 * v else 'side'
                # arrivals
                if kind == 'pile' and math.hypot(CX - s['x'], CY - s['y']) < 70 and pile and s['carry'] is None:
                    s['carry'] = pile.pop(); events.append((t, 'grab', n, None))
                elif kind == 'base' and who != n and math.hypot(BASE[who][0] - s['x'], BASE[who][1] - s['y']) < 62 and s['carry'] is None:
                    if bases[who]:
                        s['carry'] = bases[who].pop(); steals += 1; events.append((t, 'yoink', n, who))
                    s['tgt'] = None
                elif kind == 'home' and math.hypot(BASE[n][0] - s['x'], BASE[n][1] - s['y']) < 55 and s['carry'] is not None:
                    bases[n].append(s['carry']); s['carry'] = None; events.append((t, 'drop', n, None)); s['tgt'] = None
                    if len(bases[n]) >= WINN: winner = (n, t)
            cnt = {n: len(bases[n]) for n in NAMES}; mx = max(cnt.values())
            if mx > 0:
                lead = [n for n in NAMES if cnt[n] == mx]
                if len(lead) == 1 and (not leaders or leaders[-1] != lead[0]): leaders.append(lead[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], carry=s['carry'], dist=s['dist'], mode=s['mode']) for n, s in ag.items()},
                       list(pile), {n: list(b) for n, b in bases.items()}, steals))
        if winner and t > winner[1] + 3.2: break
    return frames, events, winner, steals, leaders
def score(seed):
    fr, ev, win, st, ld = sim(seed)
    if not win: return None
    tw = win[1]; final = fr[-1][2]
    second = sorted((len(b) for n, b in final.items() if n != win[0]), reverse=True)[0]
    if not (18 < tw < 27) or st < 12 or len(set(ld)) < 3 or second < 2: return None
    return round(tw, 1), win[0], st, len(set(ld)), ld
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, WIN, STEALS, LEAD = sim(SEED)
print('winner', WIN, 'steals', STEALS, 'leaders', LEAD)
# ---------------- header: Liza's village
hub = Image.open(A + 'hub.gif'); HUB = []
for i in range(0, hub.n_frames, 2):
    hub.seek(i); fr_ = hub.convert('RGB').crop((0, 60, 1920, 60 + 835)).resize((W, 470), Image.NEAREST)
    HUB.append(ImageEnhance.Brightness(fr_).enhance(0.62).convert('RGBA'))
VIC = {'joy': 'vic_Victory_Pose.gif', 'cyrus': 'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', 'cleo': 'vic_victoryPose.gif', 'ray': 'vic_victoryPose_1.gif', 'hollow': 'hollow-victory.gif'}
def gif(p, h):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
win = WIN[0]; T_WIN = WIN[1]; VICF = gif(VIC[win], 360)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
END = T_WIN + 3.2; NF = int(END * FPS)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'steal_noaudio.mp4'], stdin=subprocess.PIPE)
out_ev = []; F28 = F(28); F40 = F(40)
PILE_POS = [(-34, -18), (30, -24), (-8, 14), (40, 18), (-46, 22), (6, -40), (52, -6), (-60, -4)]
BSLOT = [(-30, -14), (26, -18), (-2, 4)]
for f in range(NF):
    t = f / FPS; st, pile, bases, steals = FR[min(f, len(FR) - 1)]
    img = GROUND.copy(); d = ImageDraw.Draw(img, 'RGBA')
    for i, k in enumerate(pile):
        g = GUM[k]; px, py = PILE_POS[i]; img.alpha_composite(g, (int(CX + px - g.width / 2), int(CY + py - g.height / 2)))
    for n, b in bases.items():
        bx, by = BASE[n]
        for i, k in enumerate(b[:3]):
            g = GUM[k]; px, py = BSLOT[i]; img.alpha_composite(g, (int(bx + px - g.width / 2), int(by + py - g.height / 2 - 14)))
    # guides
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if t < T_START or (WIN and t >= T_WIN): spr = STAND[n] if t < T_START else (FRUN[n][0] if n != win else STAND[n])
        else:
            ph = int(s['dist'] / 24) % 8
            spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        d.ellipse([x - 28, y - 8, x + 28, y + 8], fill=(0, 0, 0, 80))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['carry'] is not None:
            g = GUM[s['carry']]; bob = int(5 * math.sin(t * 10 + x * 0.01))
            img.alpha_composite(g, (int(x - g.width / 2), int(y - FOOT + 14 - g.height + bob)))
    # popups
    for (te, kind, n, who) in EV:
        u = t - te
        if 0 <= u < 1.0:
            s = FR[min(int(te * FPS), len(FR) - 1)][0][n]; x, y = s['x'], s['y'] - FOOT - 10 - u * 50; a = int(255 * min(1, (1 - u) / 0.35))
            if kind == 'yoink': ctext(d, x, y - 30, 'YOINK!', F40, (255, 220, 60), 6, a)
            elif kind == 'drop': ctext(d, x, y - 20, '+1', F40, RING[n], 6, a)
        if abs(t - te) < 0.5 / FPS:
            out_ev.append((round(te, 3), {'yoink': 'boing', 'grab': 'coin_8bit', 'drop': 'twinkle'}[kind]))
    # header
    img.alpha_composite(HUB[int(t * 6) % len(HUB)], (0, 0))
    if os.environ.get('DBG'): print('after hub', img.getpixel((540, 250)), HUB[0].getpixel((540,250)), img.mode)
    d = ImageDraw.Draw(img, 'RGBA')
    d.rectangle([0, 0, W, 470], fill=(14, 10, 24, 70))
    if os.environ.get('DBG'): print('after rect', img.getpixel((540, 250))); sys.exit()
    ctext(d, W / 2, 46, 'WHOEVER GETS 3', F(60)); ctext(d, W / 2, 130, 'GUMMIES WINS', F(60), (255, 214, 60))
    ctext(d, W / 2, 218, 'Stealing is allowed', F(32), (255, 255, 255), 5)
    d.rounded_rectangle([18, 290, W - 18, 440], 18, fill=(14, 10, 24, 200), outline=(255, 214, 60, 255), width=4)
    for i, n in enumerate(NAMES):
        sx = 18 + (W - 36) * (i + 0.5) / 5; ic = ICON[n]
        img.alpha_composite(ic, (int(sx - ic.width / 2), 300))
        for k in range(3):
            gx = sx - 54 + k * 54; gy = 400
            if k < len(bases[n]):
                g = up(GUMS[bases[n][k]], 1); g = g.resize((int(g.width * 1.3), int(g.height * 1.3)), Image.NEAREST)
                img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
            else:
                d.ellipse([gx - 9, gy - 9, gx + 9, gy + 9], outline=(120, 110, 140, 255), width=3)
        if WIN and t >= T_WIN and n == win:
            d.ellipse([sx - 40, 298 - 2, sx + 40, 298 + 76], outline=(255, 214, 60, 255), width=6)
    # footer
    d.rectangle([0, H - 90, W, H], fill=(14, 10, 24, 200))
    ctext(d, 150, H - 62, f'0:{int(min(t, T_WIN)):02d}', F28, (230, 230, 230), 4)
    ctext(d, W - 190, H - 62, f'{steals} STEALS', F28, (255, 214, 60), 4)
    if t < T_START + 0.4: ctext(d, W / 2, CY - 300, 'PICK A PLAYER!', F(52), (255, 255, 255), 8)
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(150 * a))), (0, 0))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1150 - vf.height))
        d = ImageDraw.Draw(img, 'RGBA'); ctext(d, W / 2, 1200, LABEL[win] + ' WINS!', F(60), (255, 214, 60), 8)
        rr = random.Random(f)
        for _ in range(40):
            cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H
            d.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120)]))
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN, 3), 'victory'))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': out_ev}, open('steal_events.json', 'w'))
print('done', round(END, 2))
