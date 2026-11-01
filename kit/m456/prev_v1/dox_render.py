# m04 DOXTeq2DVZd recreation: render (sim from dox_map.run). usage: python3 dox_render.py SEED [stills t1,t2,..]
import sys, os, json, math, random
from dox_map import *
from rlib import *
SEED = int(sys.argv[1]); WANT = os.environ.get('WANT', 'joy')
R = run(SEED, dur=float(os.environ.get('DUR', '66')))
FR, EV, BB, GUM, WIN = R['frames'], R['ev'], R['B'], R['gum'], R['win']
T_WIN = WIN[0]; WINNER = WIN[1]
T_CARD = T_WIN + 0.5; T_END = T_CARD + float(os.environ.get('HOLD', '2.5')); NF = int(round(T_END * FPS))
print('win', WIN, 'end', round(T_END, 2), 'frames', NF, 'simframes', len(FR))
def fidx(t): return min(max(0, int(round(t * FPS))), len(FR) - 1)
def frame_at(t): return FR[fidx(t)]
OUTS = {g: R['X'][g]['out'] for g in G}; HOW = {g: R['X'][g]['how'] for g in G}
HOOK, HB = hook_fade(os.environ.get('HOOK', 'WHO BREAKS|THROUGH FIRST?').split('|'), accent=1)
MX0, MY0, MX1, MY1 = OX, OY, OX + COLS * C, OY + ROWS * C
RY0 = MY1 + 12
# ---------------- static board
BG = checker_bg((22, 54, 58), (17, 43, 47), 60)
BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (0, 0, 0, 60)))
WALLC = (40, 98, 106); RIM = (22, 60, 66); HI = (84, 150, 156)
floor_mask = Image.new('L', (W, H), 0); fd = ImageDraw.Draw(floor_mask)
for r in range(ROWS):
    for c in range(COLS):
        if not Wd.wall[r, c]: fd.rectangle([OX + c * C, OY + r * C, OX + c * C + C - 1, OY + r * C + C - 1], fill=255)
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
bd.rounded_rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], 10, fill=(12, 26, 30, 255), outline=(8, 16, 18, 255), width=4)
bd.rectangle([MX0, MY0, MX1 - 1, MY1 - 1], fill=WALLC + (255,))
FL = floor_layer(None, MX0, MY0, MX1, MY1)
BOARD.paste(FL, (0, 0), floor_mask)
bd = ImageDraw.Draw(BOARD)
def isw(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or Wd.wall[r, c]
for r in range(ROWS):                                                    # clean wall edges: dark rim on the floor side, light lip on top faces
    for c in range(COLS):
        if not isw(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        if not isw(r + 1, c): bd.rectangle([x0, y0 + C - 3, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
        if not isw(r - 1, c): bd.rectangle([x0, y0, x0 + C - 1, y0 + 2], fill=HI + (255,))
        if not isw(r, c - 1): bd.rectangle([x0, y0, x0 + 2, y0 + C - 1], fill=RIM + (255,))
        if not isw(r, c + 1): bd.rectangle([x0 + C - 3, y0, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
ao = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ao)
for r in range(1, ROWS):
    for c in range(COLS):
        if not isw(r, c) and isw(r - 1, c):
            for k in range(3): ad.rectangle([OX + c * C, OY + r * C + 2 * k, OX + c * C + C - 1, OY + r * C + 2 * k + 1], fill=(40, 20, 10, 60 - k * 18))
BOARD.alpha_composite(ao)
EX0, EY0, EX1, EY1 = Wd.px(8, 10, 18, 18)                               # exit: bright green block with a checkered finish strip
bd = ImageDraw.Draw(BOARD)
bd.rectangle([EX0, EY0, EX1 - 23, EY1 - 1], fill=(96, 226, 100, 255)); bd.rectangle([EX0, EY0, EX1 - 23, EY1 - 1], outline=(30, 110, 40, 255), width=3)
for i in range(EY1 - EY0 >> 3):
    for j in range(3):
        bd.rectangle([EX1 - 22 + j * 7, EY0 + i * 8, EX1 - 22 + j * 7 + 6, EY0 + i * 8 + 7], fill=(240, 240, 240, 255) if (i + j) % 2 == 0 else (24, 24, 30, 255))
# ---------------- breakables
wsheet = Image.open(S_ + 'pixellab/maze/walls_sheet.png').convert('RGBA'); BRICK = up(wsheet.crop((77, 13, 128, 56)), 2)
def tint(im, col, k=0.8):
    a = np.array(im).astype(float); g_ = a[..., :3].mean(2, keepdims=True) / 255.0
    a[..., :3] = a[..., :3] * (1 - k) + (np.array(col)[None, None, :] * (0.35 + 0.95 * g_)) * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def gate_img(i, stage):
    x0, y0, x1, y1 = Wd.px(*Wd.B[i]['rect']); w, h = int(x1 - x0), int(y1 - y0); col = COL[Wd.B[i]['owner']]
    base = Image.new('RGBA', (w, h)); bt = tint(BRICK, col)
    for xx in range(0, w, bt.width):
        for yy in range(0, h, bt.height): base.alpha_composite(bt, (xx, yy))
    dd = ImageDraw.Draw(base); dd.rectangle([0, 0, w - 1, 3], fill=tuple(min(255, int(v * 1.3)) for v in col) + (255,)); dd.rectangle([0, 0, w - 1, h - 1], outline=(18, 12, 24, 255), width=2)
    rr = random.Random(i * 13)
    for s_ in range(stage):                                                # one crack per hit, the second knocks a chip out
        px_ = rr.randint(16, w - 16); pts = [(px_, 0)]; y_ = 0
        while y_ < h - 4: y_ += 6; px_ += rr.choice([-6, -3, 0, 3, 6]); pts.append((px_, y_))
        dd.line(pts, fill=(14, 8, 20, 255), width=3)
        if s_ == 1: cx_ = rr.randint(14, w - 24); dd.rectangle([cx_, h - 12, cx_ + 14, h - 1], fill=(22, 16, 30, 255))
    return base
GIMG = {i: [gate_img(i, s_) for s_ in range(3)] for i, b in enumerate(Wd.B) if b['kind'] == 'gate'}
BX0, BY0, BX1, BY1 = [int(v) for v in Wd.px(*Wd.B[BLOCK]['rect'])]
def block_img(n, pop):
    w, h = BX1 - BX0, BY1 - BY0; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); bv = 26
    d.rectangle([0, 0, w - 1, h - 1], fill=(206, 204, 212, 255))
    d.polygon([(0, 0), (w, 0), (w - bv, bv), (bv, bv)], fill=(232, 230, 236, 255)); d.polygon([(0, 0), (bv, bv), (bv, h - bv), (0, h)], fill=(160, 158, 168, 255))
    d.polygon([(w, 0), (w, h), (w - bv, h - bv), (w - bv, bv)], fill=(120, 118, 128, 255)); d.polygon([(0, h), (w, h), (w - bv, h - bv), (bv, h - bv)], fill=(70, 68, 78, 255))
    d.rectangle([0, 0, w - 1, h - 1], outline=(30, 28, 36, 255), width=3)
    fs = int(110 * (1 + 0.12 * pop)); txt = str(n); tw = d.textlength(txt, font=F(fs))
    d.text(((w - tw) / 2, (h - fs) / 2 + 4), txt, font=F(fs), fill=tuple(int(a + (255 - a) * pop) for a in (52, 50, 58)) + (255,), stroke_width=int(6 * pop), stroke_fill=(40, 38, 46, 255))
    return im
BLOCK_HITS = [(e[0]) for e in EV if e[1] == 'hit' and e[3] == BLOCK]
T_BLK = BB[BLOCK]['broke']
SHTEX = shadow_tex(COLS * C, ROWS * C)
EYES = [(OX + x * C, OY + y * C) for (x, y) in [(10, 41), (24, 65), (6, 77), (40, 56), (52, 50), (60, 79), (20, 53)]]
def shadow_layer(t, tau):
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m); rims = []
    for (x0, y0, x1, y1, d), sg in zip(Wd.flood_rects(tau), [s_ for s_ in Wd.segs if tau > s_['t0']]):
        if x1 - 1 < x0 or y1 - 1 < y0: continue
        md.rectangle([x0, y0, x1 - 1, y1 - 1], fill=255)
        if (tau - sg['t0']) * sg['v'] >= sg['L']: continue
        if d == '+x': rims.append([x1 - 4, y0, x1 - 1, y1 - 1])
        elif d == '-x': rims.append([x0, y0, x0 + 3, y1 - 1])
        elif d == '+y': rims.append([x0, y1 - 4, x1 - 1, y1 - 1])
        else: rims.append([x0, y0, x1 - 1, y0 + 3])
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.paste(SHTEX, (OX + int(5 * math.sin(t)), OY), m.crop((0, 0, W, H)).crop((OX + int(5 * math.sin(t)), OY, OX + int(5 * math.sin(t)) + SHTEX.width, OY + SHTEX.height)) if False else None)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tex = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tex.paste(SHTEX, (OX, OY)); L.paste(tex, (0, 0), m)
    dd = ImageDraw.Draw(L)
    full = set()
    for (x0, y0, x1, y1, d) in Wd.flood_rects(tau): full.add((x0, y0, x1, y1))
    for b_ in rims:                                                          # glowing front edge (skip edges that sit on a wall)
        cx_, cy_ = (b_[0] + b_[2]) / 2, (b_[1] + b_[3]) / 2
        dd.rectangle(b_, fill=(175, 115, 255, 220))
    for i, (ex, ey) in enumerate(EYES):
        if m.getpixel((ex, ey)) == 255 and m.getpixel((ex + 22, ey + 10)) == 255:
            if (int(t * 1.7 + i * 3) % 9) == 0: dd.rectangle([ex, ey + 4, ex + 20, ey + 6], fill=(230, 220, 255, 230))
            else: dd.rectangle([ex, ey, ex + 5, ey + 8], fill=(240, 235, 255, 245)); dd.rectangle([ex + 15, ey, ex + 20, ey + 8], fill=(240, 235, 255, 245))
    return L, m
BOXI = {g: box_img(g, 2 * HS) for g in G}
VIC_W = vic_frames(WINNER, 5)
EXT = Image.open(A + 'bg_moon.gif') if False else None
# rubble from the block shatter: chunks fly out and fade (clipped to the floor)
rr0 = random.Random(9); CHUNKS = [dict(x=rr0.uniform(BX0 + 10, BX1 - 10), y=rr0.uniform(BY0 + 10, BY1 - 10), vx=rr0.uniform(-160, 160), vy=rr0.uniform(-160, 160),
                                       s=rr0.choice([10, 14, 18, 22]), c=rr0.choice([(206, 204, 212), (160, 158, 168), (232, 230, 236), (120, 118, 128)])) for _ in range(46)]
PICKS = [e for e in EV if e[1] == 'pick']; KILLS = [e for e in EV if e[1] == 'out']
def held_at(t):
    hold = None
    for (tp, g) in [(e[0], e[2]) for e in PICKS]:
        if tp <= t: hold = (tp, g)
    if hold is None: return None
    for k in GUM['kills']:
        if hold[0] <= k[0] <= t and k[1] == hold[1]: return None
    return hold
def gum_floor(t):
    """lying gummy position at t (None if held)"""
    if held_at(t): return None
    pos = (GUM0['x'], GUM0['y'])
    for k in GUM['kills']:
        if k[0] <= t: pos = frame_at(k[0])[0][k[2]][:2]
    return pos
WINXY = None
def draw(f):
    global WINXY
    t = f / FPS; st, tau, hp, gm = frame_at(t)
    img = BG.copy(); img.alpha_composite(BOARD)
    for i, b in enumerate(Wd.B):                                           # gates
        if b['kind'] != 'gate' or hp[i] <= 0: continue
        x0, y0, x1, y1 = [int(v) for v in Wd.px(*b['rect'])]; stage = min(2, b['hp0'] - hp[i])
        lastk = [h_[0] for h_ in BB[i]['hits'] if h_[0] <= t]
        sh_ = int(3 * math.sin((t - lastk[-1]) * 90)) if lastk and t - lastk[-1] < 0.12 else 0
        img.alpha_composite(GIMG[i][stage], (x0 + sh_, y0))
    if hp[BLOCK] > 0:                                                      # the 66 block, pops on every hit
        lh = [h_ for h_ in BLOCK_HITS if h_ <= t]; pop = max(0.0, 1 - (t - lh[-1]) / 0.25) if lh else 0.0
        bi = block_img(hp[BLOCK], pop)
        if pop > 0.01:
            k = 1 + 0.035 * pop; bi2 = bi.resize((int(bi.width * k), int(bi.height * k)), Image.BILINEAR)
            cl = bi2.crop(((bi2.width - bi.width) // 2, (bi2.height - bi.height) // 2, (bi2.width - bi.width) // 2 + bi.width, (bi2.height - bi.height) // 2 + bi.height)); img.alpha_composite(cl, (BX0, BY0))
        else: img.alpha_composite(bi, (BX0, BY0))
    elif T_BLK is not None and t - T_BLK < 0.7:                            # shatter
        u = (t - T_BLK) / 0.7; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        for ch in CHUNKS:
            x = ch['x'] + ch['vx'] * u * 0.7; y = ch['y'] + ch['vy'] * u * 0.7; s_ = ch['s']
            dd.rectangle([x - s_ / 2, y - s_ / 2, x + s_ / 2, y + s_ / 2], fill=ch['c'] + (int(255 * (1 - u ** 2)),))
        if u < 0.3: dd.rectangle([BX0, BY0, BX1, BY1], fill=(255, 255, 255, int(200 * (1 - u / 0.3))))
        Lm = Image.new('RGBA', (W, H), (0, 0, 0, 0)); Lm.paste(L, (0, 0), floor_mask); img.alpha_composite(Lm)
    gp = gum_floor(t)
    if gp:                                                                 # STRENGTH gummy lying on the floor
        gx, gy = gp; bob = 3 * math.sin(t * 4)
        layer(img, lambda dd: [dd.ellipse([gx - 34 + q * 9, gy - 34 + q * 9, gx + 34 - q * 9, gy + 34 - q * 9], fill=STR_COL + (26 + q * 20,)) for q in range(3)])
        img.alpha_composite(GUMI, (int(gx - GUMI.width / 2), int(gy - GUMI.height / 2 + bob)))
    # trails
    for g in G:
        x, y, vx, vy, out, won = st[g]
        if out is not None and out <= t: continue
        if won is not None and t >= T_CARD: continue
        for q in range(1, 6):
            s0 = frame_at(max(0, t - q * 0.033))[0][g]
            if s0[4] is not None: continue
            a_ = 90 - q * 15; s_ = int(HS * (1 - q * 0.11))
            layer(img, lambda dd, px_=s0[0], py_=s0[1], a_=a_, s_=s_, g=g: dd.rectangle([px_ - s_, py_ - s_, px_ + s_, py_ + s_], fill=COL[g] + (a_,)))
    for g in G:                                                            # knocked out / crushed: shrink + burst in the guide's colour
        x, y, vx, vy, out, won = st[g]
        if out is None or out > t: continue
        u = (t - out) / 0.3
        if u < 1:
            bi = box_img(g, 2 * HS, dark=0.4 * u); k = 1 - 0.7 * u
            if HOW[g] == 'crush': bi = bi.resize((max(2, int(2 * HS * (1 + 0.3 * u))), max(2, int(2 * HS * k))), Image.NEAREST)
            else: bi = bi.resize((max(2, int(2 * HS * k)), max(2, int(2 * HS * k))), Image.NEAREST)
            img.alpha_composite(bi, (int(x - bi.width / 2), int(y - bi.height / 2)))
    SL, SM = shadow_layer(t, tau); img.alpha_composite(SL)
    hold = held_at(t)
    for g in G:
        x, y, vx, vy, out, won = st[g]
        if out is not None and out <= t: continue
        if won is not None and t >= T_CARD: continue
        if hold and hold[1] == g:
            pul = 0.5 + 0.5 * math.sin(t * 14)
            layer(img, lambda dd, x=x, y=y, pul=pul: dd.rectangle([x - HS - 6, y - HS - 6, x + HS + 5, y + HS + 5], outline=STR_COL + (int(140 + 100 * pul),), width=4))
        img.alpha_composite(BOXI[g], (int(round(x - HS)), int(round(y - HS))))
        if hold and hold[1] == g:                                          # the gummy rides on the holder's shoulder
            img.alpha_composite(GUMI, (int(x + HS - 14), int(y - HS - GUMI.height + 14)))
    for e in EV:
        if e[1] == 'out' and 0 <= t - e[0] < 0.45:
            x, y = frame_at(e[0])[0][e[2]][:2]; u = (t - e[0]) / 0.45
            burst(img, x, y, u, COL[e[2]], hash(e[2]) % 1000)
            if e[3] == 'gummy' and u < 0.5:
                layer(img, lambda dd, u=u: dd.ellipse([x - 20 - 90 * u, y - 20 - 90 * u, x + 20 + 90 * u, y + 20 + 90 * u], outline=(255, 245, 220, int(255 * (1 - 2 * u))), width=8))
        if e[1] == 'pick' and 0 <= t - e[0] < 0.5:
            px_, py_ = frame_at(e[0])[0][e[2]][:2]; u = (t - e[0]) / 0.5
            layer(img, lambda dd, px_=px_, py_=py_, u=u: [dd.rectangle([px_ + (24 + 100 * u) * math.cos(q * 0.785) - 6, py_ + (24 + 100 * u) * math.sin(q * 0.785) - 6, px_ + (24 + 100 * u) * math.cos(q * 0.785) + 6, py_ + (24 + 100 * u) * math.sin(q * 0.785) + 6], fill=STR_COL + (int(255 * (1 - u)),)) for q in range(8)])
        if e[1] == 'break' and e[3] != BLOCK and 0 <= t - e[0] < 0.4:
            x0, y0, x1, y1 = Wd.px(*Wd.B[e[3]]['rect']); u = (t - e[0]) / 0.4; rr = random.Random(int(e[0] * 1000))
            pts = [(rr.uniform(x0, x1), rr.uniform(y0, y1)) for _ in range(8)]
            layer(img, lambda dd, u=u, pts=pts, cc=COL[Wd.B[e[3]]['owner']]: [dd.rectangle([px - 7 - 12 * u, py - 7 - 12 * u, px + 7 + 12 * u, py + 7 + 12 * u], fill=cc + (int(190 * (1 - u)),)) for px, py in pts])
    for e in PICKS:                                                        # the power stamp
        if e[0] <= t < e[0] + 1.1 and t < T_WIN:
            stamp(img, NAME[e[2]] + ': STRENGTH!', STR_COL, t - e[0], e[0] + 1.1 - t, OY + 46 * C)
    if t >= T_WIN:
        u = t - T_WIN; wx, wy = frame_at(T_WIN)[0][WINNER][:2]
        if u < 0.5: layer(img, lambda dd: dd.rectangle([wx - HS - 6 - 40 * u / 0.5, wy - HS - 6 - 40 * u / 0.5, wx + HS + 6 + 40 * u / 0.5, wy + HS + 6 + 40 * u / 0.5], outline=(255, 214, 60, int(255 * (1 - u / 0.5))), width=6))
        if t < T_CARD: text_layer(img, [(EX0 + 110, EY0 - 50, NAME[WINNER] + ' WON', 30, COL[WINNER], 7, 255)])
    roster(img, RY0, OUTS, min(t, T_END), WINNER, T_WIN)
    if t >= T_CARD:                                                        # winner card: Syeda's victory pose replaces the box
        u = t - T_CARD; a_ = min(1, u / 0.3); wx, wy = frame_at(T_WIN)[0][WINNER][:2]
        layer(img, lambda dd: dd.rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], fill=(8, 6, 16, int(170 * a_))))
        vf = VIC_W[int(u * 8) % len(VIC_W)]; q = min(1.0, u / 0.3); sc = 0.25 + 0.75 * (1 - (1 - q) ** 3)
        vf2 = vf if sc >= 0.999 else vf.resize((max(2, int(vf.width * sc)), max(2, int(vf.height * sc))), Image.NEAREST)
        FEET = 1250; cxp = wx + (540 - wx) * q; cyp = wy + (FEET - wy) * q
        img.alpha_composite(vf2, (int(cxp - vf2.width / 2), int(cyp - vf2.height * (78 / 92))))
        rs = random.Random(int(t * 6))
        layer(img, lambda dd: [sparkle(dd, 540 + rs.uniform(-220, 220), FEET - rs.uniform(60, 400), rs.choice([4, 6, 8]), int(255 * (0.5 + 0.5 * math.sin(t * 9 + i)))) for i in range(7)])
        fs = min(80, int(880 / (len(NAME[WINNER]) + 4)))
        text_layer(img, [(540, MY0 + 70, NAME[WINNER] + ' WON', fs, COL[WINNER], 10, int(255 * a_))])
    img.alpha_composite(HOOK)
    return img
STILLS = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else []
if STILLS:
    for x in STILLS: draw(int(round(x * FPS))).convert('RGB').save(f'st_{x:.2f}.png')
    sys.exit()
OUTV = os.environ.get('OUTV', 'm04_noaudio.mp4'); wr = Writer(OUTV)
for f in range(NF): wr.write(draw(f))
wr.close()
# events for the mix
out_ev = []; last = -9
for (t_, g, k) in []: pass
cont_t = [i / FPS for i, cf in enumerate(R['contacts']) if any(cf.values())]
for e in EV:
    if e[0] >= T_END - 0.1: continue
    if e[1] == 'hit' and Wd.B[e[3]]['kind'] == 'gate': out_ev.append((round(e[0], 3), 'brick_8bit'))
    elif e[1] == 'hit' and e[3] == BLOCK:
        if e[0] - last > 0.06: out_ev.append((round(e[0], 3), 'reeltick_8bit')); last = e[0]
    elif e[1] == 'break':
        out_ev.append((round(e[0], 3), 'crunch_8bit'))
        if e[3] == BLOCK: out_ev += [(round(e[0], 3), 'boom_short'), (round(e[0] + 0.02, 3), 'exitcrack')]
        else: out_ev.append((round(e[0] + 0.02, 3), 'brick_8bit'))
    elif e[1] == 'pick': out_ev.append((round(e[0], 3), 'powerup_8bit'))
    elif e[1] == 'out':
        if e[3] == 'gummy': out_ev += [(round(e[0], 3), 'punch'), (round(e[0] + 0.02, 3), 'poof')]
        else: out_ev += [(round(e[0], 3), 'squish'), (round(e[0] + 0.03, 3), 'buzz_loud')]
out_ev += [(round(T_WIN, 3), 'win_sting'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(out_ev)
json.dump({'events': out_ev, 'end': T_END, 'beats': {'win': T_WIN, 'winner': WINNER, 'card': T_CARD, 'end': T_END, 'block': T_BLK,
           'gates': {g: BB[GATE[g]]['broke'] for g in G}, 'outs': OUTS, 'how': HOW, 'picks': [(e[0], e[2]) for e in PICKS]}}, open('m04_events.json', 'w'), indent=1)
print('done', NF)
