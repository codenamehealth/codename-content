import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7'); from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
STILL = os.environ.get('STILL')
sys.path.insert(0, SP + 'fork_sp/tools'); import atk   # Oct 29 shove rule: the seated guide plays the existing PixelLab attack (~1s)
XLO, XHI = 125, 900   # fork_sp: loser stand spot x range (body inside the focus zone; spots sit at y<1110 where the zone runs to x1025)
KLO, KHI = 90, 930    # knockback landing x range (a 0.4s flight; may brush the zone edge)
ARR = 0.1     # fork_sp: the loser reaches the mark this long before the strike frame
SEAT = 0.45   # the contest guide is seated by then and starts the strike
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['joy', 'cyrus', 'cleo', 'ray']   # HOLLOW RULE: the Hollow is no longer a contestant
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
SS = 3; FOOT = 78 * SS     # rc8: guides 2x -> 3x (~190px; were ~90-128px)
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
DYS = 90   # hfg8: whole arena moved up 90px into the space the smaller hook + cut status strip freed
AY0 = -28; TS = 64; CX, CY = 478, 1212 - DYS    # hfg8: hall floor tiles now start above the frame top (was AY0 420 under a castle header strip)
# hfg8: soft fade, no box; the twist folded into the hook (was a 3rd band line); end question replaces it in the same fade
HOOK, HBF = hook_fade(['MUSICAL CHAIRS', 'SLAPPING ALLOWED'], accent=1); print('HBF', HBF)
HOOKE, _ = hook_fade(['DID YOU', 'PICK RIGHT?'], accent=1, size=72)
HB = 584 - DYS   # old band bottom, shifted: keeps every derived position (prize, clamps) relative to the arena
CHIP_Y0, CHIP_Y1 = HB + 8, HB + 80; ST_Y0, ST_Y1 = HB + 86, HB + 146   # portrait chips, status strip
GROUND = Image.new('RGBA', (W, H), (60, 10, 14, 255))
def low(i, j):
    x, y = i * TS, AY0 + j * TS
    return ((x - CX) / 450) ** 2 + ((y - CY) / 560) ** 2 >= 1.0
GC, GR = 17, 31
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
TPLAY = [3.2, 2.5, 2.1];   # rc8: march starts on frame 0 (was 1.6s), first STOP at 3.2s (was 4.6s)
RP = 280; NR = len(TPLAY); LAST = NR - 1
def chair_pos(k):
    if k == 1: return [(CX, CY)]
    r = {3: 150, 2: 110}[k]
    return [(CX + r * math.cos(-math.pi / 2 + 2 * math.pi * i / k + math.pi / k), CY + r * math.sin(-math.pi / 2 + 2 * math.pi * i / k + math.pi / k)) for i in range(k)]
rounds = []; t = 0.0; alive = list(NAMES); theta = {n: -math.pi / 2 + 2 * math.pi * i / 4 for i, n in enumerate(NAMES)}
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
    HT = SEAT + atk.hit_t(contest)
    SD_ = atk.strike_d(contest, SS)     # fork_sp spacing: the loser stops at strike distance (fist lands on their front, no pass-through)
    _c = chairs[assign[contest]]
    def _room(sd):   # standing spot beside the striker's stool: inside the carpet and clear of the other stools
        sx_ = _c[0] + sd * SD_
        if not (XLO <= sx_ <= XHI): return -1
        oth = [chairs[assign[m]] for m in assign if m != contest]
        return min([math.hypot(sx_ - o[0], (_c[1] - o[1]) * 1.5) for o in oth] + [999])
    SIDE = -1 if pos[loser][0] < _c[0] else 1          # the side the loser runs in from
    if _room(SIDE) < 170 and _room(-SIDE) > _room(SIDE): SIDE = -SIDE   # unless that spot is crowded by another stool   # the strike lands here (loser arrives at the chair on this frame)
    rounds.append(dict(t0=t, ts=ts, chairs=chairs, loser=loser, alive=list(alive), assign=assign, contest=contest, pos=pos, theta={n: theta[n] for n in alive}, H=HT, side=SIDE))
    mute.append((ts, ts + 2.9 if r < LAST else 999))
    events += [(round(ts, 3), 'buzz_8bit'), (round(ts + 0.08, 3), 'swish'), (round(ts + HT - 0.06, 3), 'swish'), (round(ts + HT + 0.02, 3), 'punch'), (round(ts + HT + 0.45, 3), 'boing')]
    alive.remove(loser)
    # new circle angles for next round: evenly spaced, from current positions order
    if r < LAST:
        events.append((round(ts + 2.25, 3), 'poof'))
        order = sorted(alive, key=lambda n: math.atan2(pos[n][1] - CY, pos[n][0] - CX))
        for i, n in enumerate(order): theta[n] = math.atan2(pos[order[0]][1] - CY, pos[order[0]][0] - CX) + 2 * math.pi * i / len(order)
        t = ts + 2.9
T_WIN = rounds[-1]['ts'] + 1.75; DUR = T_WIN + 1.8; N = int(round(DUR * FPS))   # rc8: straight from the last OUT to the win (was +2.3s), win card held ~1.5s then loops (was 3.6s)
events += [(round(T_WIN, 3), 'victory'), (round(T_WIN + 0.9, 3), 'powerup_8bit')]   # gummy grab (was coin)
mute[-1] = (mute[-1][0], T_WIN + 0.4)
print('spots', [(r_['loser'], [round(v) for v in r_['pos'][r_['loser']]], [round(v) for v in r_['chairs'][r_['assign'][r_['contest']]]], r_['side'], [(m, [round(v) for v in r_['chairs'][r_['assign'][m]]]) for m in r_['assign']]) for r_ in rounds])
print('rounds', [(round(r_['t0'], 2), round(r_['ts'], 2), r_['loser'], r_['contest']) for r_ in rounds], 'win', round(T_WIN, 2), 'dur', round(DUR, 2))
BENCH = {'cleo': (150, 945 - DYS), 'joy': (806, 945 - DYS), 'ray': (318, 940 - DYS)}   # out guides wait in the top band (3x)
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
        HT = R['H']
        if n == R['loser']:
            c = R['chairs'][R['assign'][R['contest']]]
            side = R['side']                   # shove rule: the loser runs up beside the chair (within the strike's reach), side-on to the striker
            ex, ey = c[0] + side * atk.strike_d(R['contest'], SS), c[1] + 12
            if u < HT - ARR:
                e = ease(u / (HT - ARR)); x, y = lerp(px, ex, e), lerp(py, ey, e)
                return x, y, sprite_for(n, ex - px, ey - py, int(t * 16)), None
            if u < HT: return ex, ey, PANIC[n][int(t * 16) % 8], None    # fork_sp: on the mark a beat early, flinches as the fist comes
            kx = min(KHI, max(KLO, ex + side * 150)); ky = ey + 80 + (150 - abs(kx - ex))   # knocked back (and down when the carpet edge is close), away from the striker
            ky = min(1495 - DYS, ky)   # knockback stays in the zone
            if u < HT + 0.4:
                e = 1 - (1 - min(1, (u - HT) / 0.4)) ** 3   # fork_sp: hit = instant shove then slows (ease-out), so the fist never sits inside them
                return lerp(ex, kx, e), lerp(ey, ky, e) - 60 * math.sin(math.pi * e), PANIC[n][int(t * 16) % 8], 'slap'
            bx, by = BENCH[n]
            if u < HT + 1.3:
                e = ease((u - HT - 0.4) / 0.9); x, y = lerp(kx, bx, e), lerp(ky, by, e)
                return x, y, sprite_for(n, bx - kx, by - ky, int(t * 14)), None
            return bx, by, IDL[n][int(t * 8) % len(IDL[n])], 'bench'
        c = R['chairs'][R['assign'][n]]
        if n == R['contest'] and SEAT <= u < SEAT + atk.ATK_DUR:   # planted on the stool, strikes the one going for its chair
            return c[0], c[1] + 12, None, ('atk', u - SEAT, R['side'] < 0)
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
        if spr is None: atk.draw(img, n, SS, ex[1], x, y, left=ex[2])
        else: img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if n == WINNER and t >= T_WIN + 0.9:
            img.alpha_composite(GOLD, (int(x - GOLD.width / 2), int(y - GOLD.height - 40 + 5 * math.sin(t * 8))))   # rc8: held at chest height (above his head it went under the 3x-tall panel)
    # hfg8: castle header strip, its dark tint, the portrait chips and the ROUND/status strip are cut
    items = []; status = None
    cur = None
    for ri, R in enumerate(rounds):
        if t >= R['t0'] - 0.01: cur = (ri, R)
    if cur: status = (f'ROUND {cur[0] + 1} - {NR - cur[0]} CHAIR' + ('S' if cur[0] < LAST else ''), 44, (235, 235, 235))
    stamp = None; slap = None; flash = 0
    # hfg8: PICK A PLAYER! + name tags cut (caption asks; the guides are on screen)
    for ri, R in enumerate(rounds):
        u = t - R['ts']
        if 0 <= u < 0.6: status = ('STOP!', 48, (255, 80, 80)); stamp = ('STOP!', 110, (255, 70, 70), u)
        HT = R['H']
        if HT <= u < HT + 0.5:
            lx, ly, _, _ = state(R['loser'], R['ts'] + HT + 0.02); slap = (min(811 - 150, max(80 + 150, lx)), max(ST_Y1 + 10, ly - FOOT + 30 - 110), u - HT)
            if u < HT + 2.5 / FPS: flash = 1
        if HT + 0.5 <= u < 2.3: status = (LABEL[R['loser']] + ' IS OUT!', 44, (255, 255, 255))
        if HT + 0.5 <= u < HT + 1.15: stamp = (LABEL[R['loser']] + ' IS OUT!', 56 if len(LABEL[R['loser']]) > 5 else 64, (255, 255, 255), u - HT - 0.5)
    if flash:      # rc8: white hit flash + shake on each SLAP
        img = img.transform(img.size, Image.AFFINE, (1, 0, 10, 0, 1, -8), resample=Image.NEAREST)
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 255, 255, 120)))
    if stamp:      # rc8: big centred stamp on the carpet (was status-bar text only)
        txt, sz, col, su = stamp; sc = 1.25 - 0.25 * min(1, su / 0.12); sz2 = int(sz * sc)
        tw_ = ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=F(sz2))
        items.append((547, 990 - DYS - sz2 / 2, txt, sz2, col, 10, 255))   # hfg8: no plate
    if slap:       # rc8: SLAP! 50 -> 84px on its own dark plate above the hit
        sx_, sy_, su = slap; sz2 = int(84 * (1.3 - 0.3 * min(1, su / 0.1)))
        tw_ = ImageDraw.Draw(Image.new('L', (1, 1))).textlength('SLAP!', font=F(sz2))
        items.append((sx_, sy_, 'SLAP!', sz2, (255, 214, 60), 9, 255))
    if t >= T_WIN:
        u = t - T_WIN; a = int(255 * min(1, u / 0.3))
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 14, int(110 * min(1, u / 0.3)))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1450 - DYS - vf.height))   # rc8: pose lowered under the win plate
        # rc8: win text moved above the victory pose into the wide upper zone (centre x547) so the 46px line fits the safe zone
        items.append((547, 968 - DYS + 30, LABEL[WINNER] + ' WINS!', 72, (255, 214, 60), 9, a))   # hfg8: no plate; question moved into the hook fade
        layer(img, lambda d: [d.rectangle([x, (y + u * 420) % H, x + 10, (y + u * 420) % H + 10], fill=col) for x, y, col in CONF])
    text_layer(img, items)
    img.alpha_composite(HOOKE if t >= T_WIN else HOOK)
    if STILL and f in [int(x) for x in STILL.split(',')]: img.convert('RGB').save(f'k77_{f}.png')
    if os.environ.get('STOPAT') and f >= int(os.environ['STOPAT']): break
    w.write(img)
w.close()
json.dump({'events': events, 'mute': mute}, open('events.json', 'w')); print('done', round(DUR, 2))
