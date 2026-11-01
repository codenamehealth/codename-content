import sys; sys.path.insert(0, '../../fork_a7')
from common7 import *
import numpy as np
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (160, 150, 190)}
POWER = {'joy': 'VINE SNARE', 'cyrus': 'SUN DASH', 'cleo': 'SHIELD BASH', 'ray': 'MOON MAP', 'hollow': 'SHADOW STEP'}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
SS = 2; FOOT = 78 * SS
SRUN = {g: seq(PL + f'race/{g}_run') for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq(PL + 'maze/anim/hollow_srun')
FRUN = {g: seq(PL + f'maze/anim/{g}_frun') for g in NAMES}
STAND = {g: seq(PL + f'maze/anim/{g}_frun', 2, 0, 1)[0] for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
GUMK = ['mush', 'acv', 'mel', 'cre']
GUM = {k: gummy(k, 2) for k in GUMK}; GUMS = {k: gummy(k, 1) for k in GUMK}
def pick(d, i): return crop(Image.open(PL + f'steal/{d}/{i:02d}.png').convert('RGBA'))
BASKET = up(pick('basket', 1), 3); BLANKET = up(pick('blanket', 0), 3)
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
ICON = {n: face(n, 34) for n in NAMES}; ICONS = {n: face(n, 22) for n in NAMES}
# ---------------- desert arena (PixelLab)
AREN = up(Image.open('../gen/arena/00.png').convert('RGBA'), 3)
AY0 = 500; CX, CY = 540, AY0 + 576
GROUND = Image.new('RGBA', (W, H), (176, 104, 52, 255))
GROUND.alpha_composite(AREN, (-36, AY0))
GROUND.alpha_composite(AREN.crop((0, AREN.height - 260, AREN.width, AREN.height)).transpose(Image.FLIP_TOP_BOTTOM), (-36, AY0 + AREN.height))
GROUND.alpha_composite(BLANKET, (CX - BLANKET.width // 2, CY - BLANKET.height // 2))
BASE = {}
for k, n in enumerate(NAMES):
    a = -math.pi / 2 + k * 2 * math.pi / 5
    BASE[n] = (CX + 330 * math.cos(a), CY + 350 * math.sin(a))
layer(GROUND, lambda dd: [dd.ellipse([bx - 84, by - 50, bx + 84, by + 50], fill=RING[n] + (120,), outline=RING[n] + (255,), width=5) for n, (bx, by) in BASE.items()])
for n, (bx, by) in BASE.items():
    GROUND.alpha_composite(BASKET, (int(bx - BASKET.width / 2), int(by - BASKET.height / 2 - 6)))
    ic = ICONS[n]; GROUND.alpha_composite(ic, (int(bx - ic.width / 2), int(by + 34)))
# ---------------- simulation with guild powers
T_START = 2.2; N0 = 8; WINN = 3; CD = 4.5
def sim(seed, dur=40):
    rnd = random.Random(seed)
    kinds = [GUMK[i % 4] for i in range(N0)]; rnd.shuffle(kinds)
    pile = list(kinds); bases = {n: [] for n in NAMES}
    ag = {}
    for n in NAMES:
        bx, by = BASE[n]
        ag[n] = dict(x=bx, y=by + 20, vx=0.0, vy=0.0, carry=None, tgt=None, spd=rnd.uniform(295, 335), ph=rnd.uniform(0, 6.3),
                     greedy=rnd.random() < 0.5, dist=0.0, mode='down', retarget=0.0, cd=T_START + rnd.uniform(1, 3), slow=-9, dash=-9, blink=None, hid=-9)
    frames = []; events = []; steals = 0; winner = None; leaders = []; used = {n: 0 for n in NAMES}; denied = 0
    def fire(n, t, extra=None):
        used[n] += 1; ag[n]['cd'] = t + CD; events.append((t, 'power', n, extra))
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if t >= T_START and winner is None:
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
                tx, ty = (CX, CY) if kind == 'pile' else BASE[who]
                dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                # SHADOW STEP: the Hollow blinks toward a far target
                if n == 'hollow' and t >= s['cd'] and kind == 'base' and L > 380:
                    ox, oy = s['x'], s['y']; s['x'] += dx / L * 240; s['y'] += dy / L * 240; s['hid'] = t; fire(n, t, (ox, oy)); dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                # MOON MAP: Rayleigh warps home when carrying far from home
                if n == 'ray' and t >= s['cd'] and s['carry'] is not None and L > 330 and s['blink'] is None:
                    s['blink'] = t; fire(n, t, (s['x'], s['y']))
                if s['blink'] is not None and t - s['blink'] >= 0.35:
                    s['x'], s['y'] = BASE[n][0] + 30, BASE[n][1] + 10; s['blink'] = None; dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1
                sp = s['spd'] * (1 + 0.18 * math.sin(1.3 * t + s['ph'])) * (0.9 if s['carry'] else 1.0)
                if t - s['slow'] < 1.4: sp *= 0.25
                if t - s['dash'] < 1.3: sp *= 1.9
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
                # VINE SNARE: Joy snares a thief closing on her basket
                if kind == 'base' and who == 'joy' and n != 'joy' and t >= ag['joy']['cd'] and math.hypot(BASE['joy'][0] - s['x'], BASE['joy'][1] - s['y']) < 200 and bases['joy']:
                    s['slow'] = t; fire('joy', t, n)
                if kind == 'pile' and math.hypot(CX - s['x'], CY - s['y']) < 70 and pile and s['carry'] is None:
                    s['carry'] = pile.pop(); events.append((t, 'grab', n, None))
                    if n == 'cyrus' and t >= s['cd']: s['dash'] = t; fire(n, t)
                elif kind == 'base' and who != n and math.hypot(BASE[who][0] - s['x'], BASE[who][1] - s['y']) < 62 and s['carry'] is None:
                    if bases[who]:
                        c = ag['cleo']
                        if who == 'cleo' and t >= c['cd'] and math.hypot(c['x'] - BASE['cleo'][0], c['y'] - BASE['cleo'][1]) < 320:
                            fire('cleo', t, n); denied += 1; events.append((t, 'denied', n, None))
                            ang = math.atan2(s['y'] - BASE['cleo'][1], s['x'] - BASE['cleo'][0]); s['x'] += 150 * math.cos(ang); s['y'] += 150 * math.sin(ang)
                        else:
                            s['carry'] = bases[who].pop(); steals += 1; events.append((t, 'yoink', n, who))
                            if n == 'cyrus' and t >= s['cd']: s['dash'] = t; fire(n, t)
                    s['tgt'] = None
                elif kind == 'home' and math.hypot(BASE[n][0] - s['x'], BASE[n][1] - s['y']) < 55 and s['carry'] is not None:
                    bases[n].append(s['carry']); s['carry'] = None; events.append((t, 'drop', n, None)); s['tgt'] = None
                    if len(bases[n]) >= WINN: winner = (n, t)
            cnt = {n: len(bases[n]) for n in NAMES}; mx = max(cnt.values())
            if mx > 0:
                lead = [n for n in NAMES if cnt[n] == mx]
                if len(lead) == 1 and (not leaders or leaders[-1] != lead[0]): leaders.append(lead[0])
        frames.append(({n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], carry=s['carry'], dist=s['dist'], mode=s['mode'], slow=s['slow'], dash=s['dash'], blink=s['blink'], hid=s['hid']) for n, s in ag.items()},
                       list(pile), {n: list(b) for n, b in bases.items()}, steals))
        if winner and t > winner[1] + 3.2: break
    return frames, events, winner, steals, leaders, used, denied
def score(seed):
    fr, ev, win, st, ld, used, den = sim(seed)
    if not win: return None
    tw = win[1]; final = fr[-1][2]
    second = sorted((len(b) for n, b in final.items() if n != win[0]), reverse=True)[0]
    if not (19 < tw < 27) or st < 12 or len(set(ld)) < 3 or second < 2 or min(used.values()) < 1 or den < 1: return None
    return round(tw, 1), win[0], st, len(set(ld)), used, den
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for seed in range(int(sys.argv[2]), int(sys.argv[3])):
        r = score(seed)
        if r: print(seed, r, flush=True)
    sys.exit()
SEED = int(sys.argv[1])
FR, EV, WIN, STEALS, LEAD, USED, DEN = sim(SEED)
print('winner', WIN, 'steals', STEALS, 'leaders', LEAD, USED, DEN)
HUB = bg_frames('sun_hd.gif', (W, 500), box=(0, 120, 1920, 120 + 889), step=2, bright=0.6)
win = WIN[0]; T_WIN = WIN[1]; VICF = vic(win, 360)
END = T_WIN + 3.2; NF = int(END * FPS)
out = Writer('v95_noaudio.mp4'); out_ev = []
PILE_POS = [(-34, -18), (30, -24), (-8, 14), (40, 18), (-46, 22), (6, -40), (52, -6), (-60, -4)]
BSLOT = [(-30, -14), (26, -18), (-2, 4)]
SFX = {'yoink': 'boing', 'grab': 'coin_8bit', 'drop': 'twinkle', 'denied': 'sword_hit'}
PSFX = {'joy': 'whoosh_8bit', 'cyrus': 'powerup_8bit', 'cleo': 'sword_hit', 'ray': 'chime', 'hollow': 'poof'}
for f in range(NF):
    t = f / FPS; st, pile, bases, steals = FR[min(f, len(FR) - 1)]
    img = GROUND.copy()
    for i, k in enumerate(pile):
        g = GUM[k]; px, py = PILE_POS[i]; img.alpha_composite(g, (int(CX + px - g.width / 2), int(CY + py - g.height / 2)))
    for n, b in bases.items():
        bx, by = BASE[n]
        for i, k in enumerate(b[:3]):
            g = GUM[k]; px, py = BSLOT[i]; img.alpha_composite(g, (int(bx + px - g.width / 2), int(by + py - g.height / 2 - 14)))
    FX = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(FX)
    for n in NAMES:
        s = st[n]; x, y = s['x'], s['y']
        fd.ellipse([x - 28, y - 8, x + 28, y + 8], fill=(0, 0, 0, 80))
        if t - s['dash'] < 1.3:
            for q in range(6):
                px_ = x - s['vx'] * 0.02 * q * 3; py_ = y - 30 - s['vy'] * 0.02 * q * 3
                fd.rectangle([px_ - 10 + q, py_ - 10 + q, px_ + 10 - q, py_ + 10 - q], fill=(255, 140 + q * 15, 40, 200 - q * 30))
    img.alpha_composite(FX)
    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if s['blink'] is not None: continue
        if t < T_START or t >= T_WIN: spr = STAND[n]
        else:
            ph = int(s['dist'] / 24) % 8
            spr = FRUN[n][ph] if s['mode'] == 'down' else (SRUNL if s['vx'] < 0 else SRUN)[n][ph]
        if t - s['hid'] < 0.5:
            spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda p: int(p * 0.55)))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if t - s['slow'] < 1.4:
            layer(img, lambda dd: [dd.arc([x - 34 - k * 6, y - 26 - k * 10, x + 34 + k * 6, y + 14 + k * 4], 200 + k * 40, 340 + k * 40, fill=(70, 170, 60, 255), width=6) for k in range(3)])
        if s['carry'] is not None:
            g = GUM[s['carry']]; bob = int(5 * math.sin(t * 10 + x * 0.01))
            img.alpha_composite(g, (int(x - g.width / 2), int(y - FOOT + 14 - g.height + bob)))
    PLy = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(PLy)
    for e in EV:
        te, kind, n, extra = e; u = t - te
        s = FR[min(int(te * FPS), len(FR) - 1)][0][n]
        if 0 <= u < 1.0:
            x, y = s['x'], s['y'] - FOOT - 10 - u * 50; a = int(255 * min(1, (1 - u) / 0.35))
            if kind == 'yoink': ctext(d, x, y - 30, 'YOINK!', F(38), (255, 220, 60), 6, a)
            elif kind == 'drop': ctext(d, x, y - 20, '+1', F(40), RING[n], 6, a)
            elif kind == 'denied': ctext(d, x, y - 70, 'DENIED!', F(40), (255, 80, 80), 6, a)
            elif kind == 'power':
                ctext(d, x, y - 110, POWER[n] + '!', F(30), RING[n], 6, a)
                if n == 'ray' and extra:
                    for k in range(10):
                        aa = k * 0.63; r = 20 + 120 * u
                        for (cx_, cy_) in (extra, BASE['ray']):
                            d.rectangle([cx_ + r * math.cos(aa) - 5, cy_ - 60 + r * math.sin(aa) - 5, cx_ + r * math.cos(aa) + 5, cy_ - 60 + r * math.sin(aa) + 5], fill=(200, 140, 255, a))
                if n == 'hollow' and extra and u < 0.5:
                    ox, oy = extra; d.ellipse([ox - 50, oy - 120, ox + 50, oy], fill=(60, 40, 90, int(160 * (1 - u / 0.5))))
                if n == 'cleo':
                    bx, by = BASE['cleo']; r = 60 + 160 * u
                    d.ellipse([bx - r, by - r * 0.6, bx + r, by + r * 0.6], outline=(140, 190, 255, a), width=8)
        if abs(t - te) < 0.5 / FPS:
            out_ev.append((round(te, 3), PSFX[n] if kind == 'power' else SFX[kind]))
    img.alpha_composite(PLy)
    # header: Liza's sun temple
    img.alpha_composite(HUB[int(t * 6) % len(HUB)], (0, 0))
    layer(img, lambda dd: (dd.rectangle([0, 0, W, 500], fill=(30, 14, 4, 70)), dd.rounded_rectangle([18, 268, W - 18, 488], 18, fill=(20, 12, 8, 205))))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 34, 'WHOEVER GETS 3', F(58)); ctext(d, W / 2, 114, 'GUMMIES WINS', F(58), (255, 214, 60))
    ctext(d, W / 2, 196, 'POWERS ARE ON!', F(34), (255, 140, 60), 6)
    d.rounded_rectangle([18, 268, W - 18, 488], 18, outline=(255, 214, 60), width=4)
    active = {e[2]: e[0] for e in EV if e[1] == 'power' and 0 <= t - e[0] < 0.9}
    for i, n in enumerate(NAMES):
        sx = 18 + (W - 36) * (i + 0.5) / 5; ic = ICON[n]
        img.alpha_composite(ic, (int(sx - ic.width / 2), 276))
        for k in range(3):
            gx = sx - 54 + k * 54; gy = 376
            if k < len(bases[n]):
                g = GUMS[bases[n][k]]; g = g.resize((int(g.width * 1.3), int(g.height * 1.3)), Image.NEAREST)
                img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
            else: d.ellipse([gx - 9, gy - 9, gx + 9, gy + 9], outline=(140, 120, 100), width=3)
        on = n in active
        cw = 186; d.rounded_rectangle([sx - cw / 2 + 6, 420, sx + cw / 2 - 6, 470], 10, fill=RING[n] if on else (40, 28, 22), outline=RING[n], width=3)
        tw_ = d.textlength(POWER[n], font=F(14)); d.text((sx - tw_ / 2, 438), POWER[n], font=F(14), fill=(20, 15, 35) if on else (235, 225, 210))
        if t >= T_WIN and n == win: d.ellipse([sx - 40, 274, sx + 40, 354], outline=(255, 214, 60), width=6)
    layer(img, lambda dd: dd.rectangle([0, H - 90, W, H], fill=(20, 12, 8, 210))); d = ImageDraw.Draw(img)
    ctext(d, 150, H - 62, f'0:{int(min(t, T_WIN)):02d}', F(28), (230, 230, 230), 4)
    ctext(d, W - 190, H - 62, f'{steals} STEALS', F(28), (255, 214, 60), 4)
    if t < T_START + 0.4: text_layer(img, [(W / 2, CY - 280, 'PICK A PLAYER!', 52, (255, 255, 255), 8, 255)])
    if t >= T_WIN:
        u = t - T_WIN; a = min(1, u / 0.3)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(150 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        text_layer(img, [(W / 2, 1230, LABEL[win] + ' WINS!', 60, (255, 214, 60), 8, 255)])
        rr = random.Random(f); L3 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d3 = ImageDraw.Draw(L3)
        for _ in range(40):
            cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 500) % H
            d3.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120)]))
        img.alpha_composite(L3)
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN, 3), 'victory'))
    out.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
out.close(); json.dump(out_ev, open('ev.json', 'w')); print('done', round(END, 2))
