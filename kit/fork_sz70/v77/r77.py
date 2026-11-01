import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7'); from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray']   # HOLLOW RULE: the Hollow is no longer a contestant
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
SS = 2; FOOT = 78 * SS
SRUN = {g: seq(PL + f'race/{g}_run', SS, 1, 9) for g in NAMES}
SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
FRUN = {g: seq(PL + f'maze/anim/{g}_frun', SS, 1, 9) for g in NAMES}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SS, 1, 9) for g in NAMES}
IDL = {g: idle(g, SS) for g in NAMES}
def face(name, rad):
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 30) for n in NAMES}
# ---------- hall floor (marble inside, royal carpet around)
T = wang(SP + 'fork_a8/gen/hall_meta.json', SP + 'fork_a8/gen/hall_sheet.png'); T = {k: up(v, 2) for k, v in T.items()}
AY0 = 420; TS = 64; CX, CY = 478, 1212    # was 540, 1170
HOOK, HB = hook_layer(['MUSICAL', 'CHAIRS'], accent=1, sub='SLAPPING IS ALLOWED')
CHIP_Y0, CHIP_Y1 = HB + 8, HB + 80; ST_Y0, ST_Y1 = HB + 86, HB + 146   # portrait chips, status strip
GROUND = Image.new('RGBA', (W, H), (60, 10, 14, 255))
def low(i, j):
    x, y = i * TS, AY0 + j * TS
    return ((x - CX) / 450) ** 2 + ((y - CY) / 560) ** 2 >= 1.0
GC, GR = 17, 24
CORN = [[low(i, j) for i in range(GC + 1)] for j in range(GR + 1)]
for j in range(GR):
    for i in range(GC):
        key = (CORN[j][i], CORN[j][i + 1], CORN[j + 1][i], CORN[j + 1][i + 1]); GROUND.alpha_composite(T[key], (i * TS, AY0 + j * TS))
import numpy as _np
_g = _np.array(GROUND).astype(float); _rgb = _g[..., :3]; _m = _rgb.std(-1) < 14
_v = _rgb.mean(-1) / 255.0
_new = _np.stack([40 + 70 * _v, 30 + 55 * _v, 34 + 45 * _v], -1)
_rgb[_m] = _new[_m]; _g[..., :3] = _rgb; GROUND = Image.fromarray(_g.astype('uint8'), 'RGBA')
CANDLE = up(crop(Image.open(SP + 'fork_a8/gen/candle/01.png').convert('RGBA')), 4)
CANDLES = [(70, 170), (1010, 170), (70, 1760), (1010, 1760), (60, 1160), (1020, 1160)]
for cx, cy in CANDLES: GROUND.alpha_composite(CANDLE, (cx - CANDLE.width // 2, cy - CANDLE.height // 2))
STOOL = up(crop(Image.open(SP + 'fork_a8/gen/stool/09.png').convert('RGBA')), 3)
# GOLD FIX: the prize is a cluster of the 4 product gummies (was one gold gummy)
GOLD = Image.new('RGBA', (170, 150), (0, 0, 0, 0))
for k, (gx, gy) in zip(['mel', 'acv', 'cre', 'mush'], [(0, 0), (84, 0), (0, 70), (84, 70)]):
    GOLD.alpha_composite(gummy(k, 3), (gx, gy))
GOLD = crop(GOLD); PRIZE_XY = (CX, HB + 222)
# header: Liza's castle
HBG = bg_frames('bg_castle.gif', (1080, 608), step=2, bright=0.55)
HBG = [b.crop((0, 60, 1080, 480)) for b in HBG]
# ---------- choreography
OUTS = ['cleo', 'joy', 'ray']; WINNER = 'cyrus'
TPLAY = [3.0, 2.5, 2.1]; RP = 280; NR = len(TPLAY); LAST = NR - 1
def chair_pos(k):
    if k == 1: return [(CX, CY)]
    r = {3: 150, 2: 110}[k]
    return [(CX + r * math.cos(-math.pi / 2 + 2 * math.pi * i / k + math.pi / k), CY + r * math.sin(-math.pi / 2 + 2 * math.pi * i / k + math.pi / k)) for i in range(k)]
rounds = []; t = 1.6; alive = list(NAMES); theta = {n: -math.pi / 2 + 2 * math.pi * i / 4 for i, n in enumerate(NAMES)}
OMEGA = 1.9
events = []; mute = []
for r, tp in enumerate(TPLAY):
    k = NR - r; chairs = chair_pos(k); loser = OUTS[r]
    ts = t + tp
    # positions at stop
    pos = {n: (CX + RP * math.cos(theta[n] + OMEGA * (ts - t)), CY + RP * 0.92 * math.sin(theta[n] + OMEGA * (ts - t))) for n in alive}
    # assign winners to chairs (greedy nearest)
    winners = [n for n in alive if n != loser]; free = list(range(k)); assign = {}
    pairs = sorted(((math.hypot(pos[n][0] - chairs[c][0], pos[n][1] - chairs[c][1]), n, c) for n in winners for c in free))
    for dd, n, c in pairs:
        if n in assign or c not in free: continue
        assign[n] = c; free.remove(c)
    contest = min(winners, key=lambda n: math.hypot(pos[n][0] - pos[loser][0], pos[n][1] - pos[loser][1]))
    rounds.append(dict(t0=t, ts=ts, chairs=chairs, loser=loser, alive=list(alive), assign=assign, contest=contest, pos=pos, theta={n: theta[n] for n in alive}))
    mute.append((ts, ts + 2.9 if r < LAST else 999))
    events += [(round(ts, 3), 'buzz_8bit'), (round(ts + 0.08, 3), 'swish'), (round(ts + 0.62, 3), 'punch'), (round(ts + 1.05, 3), 'boing')]
    alive.remove(loser)
    # new circle angles for next round: evenly spaced, from current positions order
    if r < LAST:
        events.append((round(ts + 2.25, 3), 'poof'))
        order = sorted(alive, key=lambda n: math.atan2(pos[n][1] - CY, pos[n][0] - CX))
        for i, n in enumerate(order): theta[n] = math.atan2(pos[order[0]][1] - CY, pos[order[0]][0] - CX) + 2 * math.pi * i / len(order)
        t = ts + 2.9
T_WIN = rounds[-1]['ts'] + 2.3; DUR = T_WIN + 3.6; N = int(DUR * FPS)
events += [(round(T_WIN, 3), 'victory'), (round(T_WIN + 0.9, 3), 'powerup_8bit')]   # gummy grab (was coin)
mute[-1] = (mute[-1][0], T_WIN + 0.4)
print('rounds', [(round(r_['t0'], 2), round(r_['ts'], 2), r_['loser'], r_['contest']) for r_ in rounds], 'win', round(T_WIN, 2), 'dur', round(DUR, 2))
BENCH = {'cleo': (130, HB + 312), 'joy': (240, HB + 312), 'ray': (826, HB + 312)}   # out guides wait in the top band
def sprite_for(n, vx, vy, ph):
    v = math.hypot(vx, vy) or 1
    if vy > 0.72 * v: return FRUN[n][ph % 8]
    return (SRUNL if vx < 0 else SRUN)[n][ph % 8]
def lerp(a, b, u): return a + (b - a) * u
def ease(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
def state(n, t):
    """returns x, y, sprite, extra"""
    if t < rounds[0]['t0']:
        th = rounds[0]['theta'][n]; x, y = CX + RP * math.cos(th), CY + RP * 0.92 * math.sin(th)
        return x, y, IDL[n][int(t * 8) % len(IDL[n])], None
    for ri, R in enumerate(rounds):
        nxt = rounds[ri + 1]['t0'] if ri < LAST else 1e9
        if n not in R['alive']: continue
        if t < R['t0']: break
        if ri < LAST and t >= nxt: continue
        if R['t0'] <= t < R['ts']:
            th = R['theta'][n] + OMEGA * (t - R['t0'])
            x, y = CX + RP * math.cos(th), CY + RP * 0.92 * math.sin(th)
            vx, vy = -math.sin(th), 0.92 * math.cos(th)
            return x, y, sprite_for(n, vx, vy, int(t * 14 + hash(n) % 8)), None
        u = t - R['ts']; px, py = R['pos'][n]
        if n == R['loser']:
            c = R['chairs'][R['assign'][R['contest']]]
            if u < 0.6:
                e = ease(u / 0.6); x, y = lerp(px, c[0], e * 0.85), lerp(py, c[1] + 12, e * 0.85)
                return x, y, sprite_for(n, c[0] - px, c[1] - py, int(t * 16)), None
            ex, ey = lerp(px, c[0], 0.85), lerp(py, c[1] + 12, 0.85)
            ang = math.atan2(ey - CY, ex - CX) if (ex, ey) != (CX, CY) else math.pi / 2
            kx, ky = ex + math.cos(ang) * 150, ey + math.sin(ang) * 150
            kx, ky = min(850, max(110, kx)), min(1495, ky)   # knockback stays in the zone
            if u < 1.0:
                e = ease((u - 0.6) / 0.4); return lerp(ex, kx, e), lerp(ey, ky, e) - 60 * math.sin(math.pi * e), PANIC[n][int(t * 16) % 8], 'slap'
            bx, by = BENCH[n]
            if u < 1.9:
                e = ease((u - 1.0) / 0.9); x, y = lerp(kx, bx, e), lerp(ky, by, e)
                return x, y, sprite_for(n, bx - kx, by - ky, int(t * 14)), None
            return bx, by, IDL[n][int(t * 8) % len(IDL[n])], 'bench'
        c = R['chairs'][R['assign'][n]]
        if u < 0.45:
            e = ease(u / 0.45); return lerp(px, c[0], e), lerp(py, c[1] + 12, e), sprite_for(n, c[0] - px, c[1] - py, int(t * 16)), None
        if ri == LAST or t < nxt - 0.5:
            return c[0], c[1] + 12, IDL[n][int(t * 8) % len(IDL[n])], 'seat'
        # walk back out to the next circle start
        N2 = rounds[ri + 1]; th = N2['theta'][n]; tx, ty = CX + RP * math.cos(th), CY + RP * 0.92 * math.sin(th)
        e = ease((t - (nxt - 0.5)) / 0.5); return lerp(c[0], tx, e), lerp(c[1] + 12, ty, e), sprite_for(n, tx - c[0], ty - c[1], int(t * 14)), None
    # out from an earlier round -> bench
    if n in OUTS:
        bx, by = BENCH[n]; return bx, by, IDL[n][int(t * 8) % len(IDL[n])], 'bench'
    return CX, CY, IDL[n][0], None
def chairs_at(t):
    for ri, R in enumerate(rounds):
        nxt = rounds[ri + 1]['t0'] if ri < LAST else 1e9
        if t < R['ts'] + 2.25 or ri == LAST: return R['chairs'], 255
        if t < nxt:
            # previous chairs fade one (the contested one disappears) and slide to new layout
            u = ease((t - R['ts'] - 2.25) / 0.45); new = rounds[ri + 1]['chairs']; old = R['chairs']
            gone = R['assign'][R['contest']] if False else len(old) - 1
            keep = [c for i, c in enumerate(old) if i != gone]
            return [(lerp(a[0], b[0], u), lerp(a[1], b[1], u)) for a, b in zip(keep, new)], 255
    return rounds[-1]['chairs'], 255
VICF = vic(WINNER, 300)
w = Writer('noaudio.mp4')
rr = random.Random(4); CONF = [(rr.uniform(0, W), rr.uniform(0, H), rr.choice([(255, 214, 60), (90, 200, 80), (90, 150, 255), (255, 120, 120)])) for _ in range(60)]
for f in range(N):
    t = f / FPS; img = GROUND.copy()
    layer(img, lambda d: [d.ellipse([cx - r, cy - 30 - r, cx + r, cy - 30 + r], fill=(255, 190, 90, int(12 + 6 * math.sin(t * 9 + cx)))) for cx, cy in CANDLES for r in (150, 100, 60)])
    # prize
    if t < T_WIN + 0.9:
        bob = 8 * math.sin(t * 3)
        layer(img, lambda d: [d.ellipse([PRIZE_XY[0] - r, PRIZE_XY[1] - r + bob, PRIZE_XY[0] + r, PRIZE_XY[1] + r + bob], fill=(255, 220, 110, 30)) for r in (90, 66, 44)])
        img.alpha_composite(GOLD, (int(PRIZE_XY[0] - GOLD.width / 2), int(PRIZE_XY[1] - GOLD.height / 2 + bob)))
    chs, _ = chairs_at(t)
    for (x, y) in chs: img.alpha_composite(STOOL, (int(x - STOOL.width / 2), int(y - STOOL.height / 2)))
    sts = {n: state(n, t) for n in NAMES}
    layer(img, lambda d: [d.ellipse([s[0] - 26, s[1] - 8, s[0] + 26, s[1] + 8], fill=(0, 0, 0, 80)) for s in sts.values()])
    for n in sorted(NAMES, key=lambda n: sts[n][1]):
        x, y, spr, ex = sts[n]
        if n == WINNER and t >= T_WIN:
            u = ease((t - T_WIN) / 0.8); c = rounds[-1]['chairs'][0]
            x, y = lerp(c[0], PRIZE_XY[0], u), lerp(c[1] + 12, PRIZE_XY[1] + 120, u)
            spr = sprite_for(n, 0.1, -1, int(t * 14)) if u < 1 else IDL[n][int(t * 8) % len(IDL[n])]
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if n == WINNER and t >= T_WIN + 0.9:
            img.alpha_composite(GOLD, (int(x - GOLD.width / 2), int(y - FOOT - GOLD.height + 10 + 5 * math.sin(t * 8))))
    # header
    hb = HBG[int(t * 6) % len(HBG)]; img.alpha_composite(hb, (0, 0))
    layer(img, lambda d: (d.rectangle([0, 0, W, 420], fill=(14, 10, 24, 90)), d.rounded_rectangle([70, CHIP_Y0, 1025, ST_Y1], 16, fill=(14, 10, 24, 250))))
    d = ImageDraw.Draw(img); d.rounded_rectangle([70, CHIP_Y0, 1025, ST_Y1], 16, outline=(255, 214, 60, 255), width=4)
    out_now = set()
    for R in rounds:
        if t >= R['ts'] + 1.0: out_now.add(R['loser'])
    for i, n in enumerate(NAMES):
        sx = 70 + 955 * (i + 0.5) / 4; ic = ICON[n]; iy = CHIP_Y0 + 6; my = iy + ic.height // 2
        if n in out_now: ic = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.15)).enhance(0.5)
        img.alpha_composite(ic, (int(sx - ic.width / 2), iy))
        if n in out_now:
            d = ImageDraw.Draw(img); d.line([sx - 22, my - 22, sx + 22, my + 22], fill=(230, 50, 50), width=7); d.line([sx - 22, my + 22, sx + 22, my - 22], fill=(230, 50, 50), width=7)
        if n == WINNER and t >= T_WIN:
            d = ImageDraw.Draw(img); d.ellipse([sx - 38, my - 38, sx + 38, my + 38], outline=(255, 214, 60), width=6)
    items = []; status = None
    cur = None
    for ri, R in enumerate(rounds):
        if t >= R['t0'] - 0.01: cur = (ri, R)
    if cur: status = (f'ROUND {cur[0] + 1}  -  {NR - cur[0]} CHAIR' + ('S' if cur[0] < LAST else ''), 32, (235, 235, 235))
    if t < rounds[0]['t0'] + 0.3: items.append((CX, CY - 40, 'PICK A PLAYER!', 54, (255, 255, 255), 8, 255))
    for ri, R in enumerate(rounds):
        u = t - R['ts']
        if 0 <= u < 0.6: status = ('STOP!', 48, (255, 80, 80))
        if 0.6 <= u < 1.1:
            lx, ly, _, _ = state(R['loser'], R['ts'] + 0.62); items.append((min(880 - 130, max(72 + 130, lx)), max(ST_Y1 + 10, ly - FOOT - 70), 'SLAP!', 50, (255, 214, 60), 7, 255))
        if 1.0 <= u < 2.3: status = (LABEL[R['loser']] + ' IS OUT!', 40, (255, 255, 255))
    if t >= T_WIN:
        u = t - T_WIN; a = int(255 * min(1, u / 0.3))
        layer(img, lambda d: d.rectangle([0, ST_Y1 + 4, W, H], fill=(8, 6, 14, int(110 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1300 - vf.height))
        items.append((CX, 1318, LABEL[WINNER] + ' WINS!', 64, (255, 214, 60), 8, a))
        items.append((CX, 1416, 'Did you pick right?', 36, (255, 255, 255), 5, a))
        layer(img, lambda d: [d.rectangle([x, (y + u * 420) % H, x + 10, (y + u * 420) % H + 10], fill=col) for x, y, col in CONF])
    if status: items.append((548, (ST_Y0 + ST_Y1) / 2 - status[1] / 2, status[0], status[1], status[2], 6, 255))
    text_layer(img, items)
    img.alpha_composite(HOOK)
    w.write(img)
w.close()
json.dump({'events': events, 'mute': mute}, open('events.json', 'w')); print('done', round(DUR, 2))
