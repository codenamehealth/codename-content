# m05 DOXTeq2DVZd recreation: render (sim from dox_map.run). usage: python3 dox_render.py SEED [stills t1,t2,..]
import sys, os, json, math, random
from dox_map import *
from rlib import *
SEED = sys.argv[1]; WANT = os.environ.get('WANT', 'joy')
os.environ.setdefault('POST', '3.4')                                   # the game keeps running under the end card (as in the reference)
R = run(SEED, dur=float(os.environ.get('DUR', '66')))
FR, EV, BB, GUM, WIN = R['frames'], R['ev'], R['B'], R['gum'], R['win']
T_WIN = WIN[0]; WINNER = WIN[1]
T_CARD = T_WIN + 0.5; T_END = T_CARD + float(os.environ.get('HOLD', '2.5')); NF = int(round(T_END * FPS))
print('win', WIN, 'end', round(T_END, 2), 'frames', NF, 'simframes', len(FR))
def fidx(t): return min(max(0, int(round(t * FPS))), len(FR) - 1)
def frame_at(t): return FR[fidx(t)]
OUTS = {g: R['X'][g]['out'] for g in G}; HOW = {g: R['X'][g]['how'] for g in G}
MX0, MY0, MX1, MY1 = OX, OY, OX + COLS * C, OY + ROWS * C
# ---------------- static board
BG = castle_backdrop()                                                    # the Realm castle scene, blurred and dimmed, fills the frame
WALLC = (150, 140, 132); RIM = (62, 54, 60); HI = (226, 216, 198)
floor_mask = Image.new('L', (W, H), 0); fd = ImageDraw.Draw(floor_mask)
for r in range(ROWS):
    for c in range(COLS):
        if not Wd.wall[r, c]: fd.rectangle([OX + c * C, OY + r * C, OX + c * C + C - 1, OY + r * C + C - 1], fill=255)
# hook on the wall band between the top room and the start lanes (soft dark band masked off the floor); roster stacked on the right wall
HOOK, HB = hook_wall(os.environ.get('HOOK', 'WHO BREAKS|THROUGH FIRST?').split('|'), 470, 712, 46, floor_mask, band=True)
RSP = {g: (756, 905 + i * 124) for i, g in enumerate(G)}
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
bd.rounded_rectangle([MX0 - 8, MY0 - 8, MX1 + 7, MY1 + 7], 8, fill=(34, 30, 38, 255), outline=(14, 12, 18, 255), width=4)
bd.rectangle([MX0, MY0, MX1 - 1, MY1 - 1], fill=WALLC + (255,))
FL = flagstones(MX0, MY0, MX1, MY1, seed=11)                              # courtyard flagstones (same world as m06)
BOARD.paste(castle_bricks(MX0, MY0, MX1, MY1, seed=13), (0, 0), ImageChops.invert(floor_mask))
BOARD.paste(FL, (0, 0), floor_mask)
bd = ImageDraw.Draw(BOARD)
def isw(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or Wd.wall[r, c]
for r in range(ROWS):                                                    # clean wall edges: dark rim on the floor side, light lip on top faces
    for c in range(COLS):
        if not isw(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        if not isw(r + 1, c): bd.rectangle([x0, y0 + C - 3, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
        if not isw(r - 1, c):
            bd.rectangle([x0, y0, x0 + C - 1, y0 + 2], fill=HI + (255,))
            if (r * 31 + c * 17) % 5 < 2: bd.rectangle([x0 + (c % 3), y0, x0 + (c % 3) + 5, y0 + 3], fill=(96, 136, 72, 255)); bd.rectangle([x0 + (c % 3) + 1, y0 + 4, x0 + (c % 3) + 3, y0 + 5], fill=(70, 108, 58, 255))
        if not isw(r, c - 1): bd.rectangle([x0, y0, x0 + 2, y0 + C - 1], fill=RIM + (255,))
        if not isw(r, c + 1): bd.rectangle([x0 + C - 3, y0, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
ao = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ad = ImageDraw.Draw(ao)
for r in range(1, ROWS):
    for c in range(COLS):
        if not isw(r, c) and isw(r - 1, c):
            for k in range(3): ad.rectangle([OX + c * C, OY + r * C + 2 * k, OX + c * C + C - 1, OY + r * C + 2 * k + 1], fill=(40, 20, 10, 60 - k * 18))
BOARD.alpha_composite(ledge_shadow(Wd, OX, OY, C, isw))                  # darker band under every ledge
EX0, EY0, EX1, EY1 = [int(v) for v in Wd.px(*EXIT)]                    # exit: glowing gate in the left wall (frame static, light per frame)
bd = ImageDraw.Draw(BOARD); portal_frame(bd, EX0, EY0, EX1, EY1, 'right')
TORCHES = [(150, 420), (150, 620)]
for (tx_, ty_) in TORCHES: sconce(bd, tx_, ty_)
banner(bd, 808, 470, 62, 150)
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
    # the 66 block: carved stone slab with iron corner brackets; the number is cut into the stone and flares warm on each hit
    w, h = BX1 - BX0, BY1 - BY0; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); bv = 22; rr = random.Random(4)
    d.rectangle([0, 0, w - 1, h - 1], fill=(160, 150, 138, 255))
    for _ in range(900):
        x_, y_ = rr.randint(bv, w - bv - 2), rr.randint(bv, h - bv - 2); v_ = rr.randint(-14, 12); d.rectangle([x_, y_, x_ + 1, y_ + 1], fill=(160 + v_, 150 + v_, 138 + v_, 255))
    for _ in range(4):
        x_ = rr.randint(bv + 10, w - bv - 30); y_ = rr.randint(bv + 10, h - bv - 30); d.line([(x_, y_), (x_ + 8, y_ + 9), (x_ + 5, y_ + 18), (x_ + 12, y_ + 26)], fill=(108, 100, 94, 255))
    d.polygon([(0, 0), (w, 0), (w - bv, bv), (bv, bv)], fill=(206, 196, 180, 255)); d.polygon([(0, 0), (bv, bv), (bv, h - bv), (0, h)], fill=(184, 174, 160, 255))
    d.polygon([(w, 0), (w, h), (w - bv, h - bv), (w - bv, bv)], fill=(118, 110, 106, 255)); d.polygon([(0, h), (w, h), (w - bv, h - bv), (bv, h - bv)], fill=(90, 84, 84, 255))
    d.rectangle([0, 0, w - 1, h - 1], outline=(30, 26, 32, 255), width=3)
    for (cx_, cy_, sx, sy) in [(0, 0, 1, 1), (w - 1, 0, -1, 1), (0, h - 1, 1, -1), (w - 1, h - 1, -1, -1)]:   # iron corner brackets + rivets
        d.polygon([(cx_, cy_), (cx_ + sx * 58, cy_), (cx_ + sx * 58, cy_ + sy * 16), (cx_ + sx * 16, cy_ + sy * 16), (cx_ + sx * 16, cy_ + sy * 58), (cx_, cy_ + sy * 58)], fill=(58, 54, 64, 255))
        d.line([(cx_ + sx * 2, cy_ + sy * 2), (cx_ + sx * 56, cy_ + sy * 2)], fill=(104, 100, 112, 255), width=2)
        for (ox_, oy_) in [(8, 8), (44, 8), (8, 44)]: d.rectangle([cx_ + sx * ox_ - 2, cy_ + sy * oy_ - 2, cx_ + sx * ox_ + 2, cy_ + sy * oy_ + 2], fill=(160, 156, 170, 255))
    fs = int(min(w, h) * 0.5 * (1 + 0.12 * pop)); txt = str(n); tw = d.textlength(txt, font=F(fs)); tx_, ty_ = (w - tw) / 2, (h - fs) / 2 + 4
    d.text((tx_ + 4, ty_ + 4), txt, font=F(fs), fill=(214, 204, 188, 255))                                          # cut edge catching light
    d.text((tx_, ty_), txt, font=F(fs), fill=tuple(int(a + (b - a) * pop) for a, b in zip((44, 38, 42), (255, 214, 120))) + (255,))
    return im
BLOCK_HITS = [(e[0]) for e in EV if e[1] == 'hit' and e[3] == BLOCK]
T_BLK = BB[BLOCK]['broke']
SHTEX = shadow_tex(COLS * C + 40, ROWS * C + 40)
import scipy.ndimage as nd
OPENC = ~Wd.wall
_nz = Image.effect_noise((W // 4 + 40, H // 4 + 40), 70).resize((W + 160, H + 160), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
NZ = _nz.point(lambda v: int(150 + 105 * max(0.0, min(1.0, (v - 70) / 120))))
POCKETS = []
def flood_mask(t, tau, st, hp):
    """flood mask = segment rects + any small open pocket the rectangle model leaves cut off between segments
    (no live box inside), so the shadow always reads as one continuous mass"""
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m); fl = np.zeros(Wd.wall.shape, bool)
    for (x0, y0, x1, y1, d) in Wd.flood_rects(tau):
        if x1 - 1 < x0 or y1 - 1 < y0: continue
        md.rectangle([x0, y0, x1 - 1, y1 - 1], fill=255)
        c0, c1 = int(math.floor((x0 - OX) / C + 0.5)), int(math.floor((x1 - OX) / C + 0.5)); r0, r1 = int(math.floor((y0 - OY) / C + 0.5)), int(math.floor((y1 - OY) / C + 0.5))
        fl[max(0, r0):r1, max(0, c0):c1] = True
    solid = Wd.wall.copy()
    for k, b in enumerate(Wd.B):
        if hp[k] > 0: x0, y0, x1, y1 = b['rect']; solid[y0:y1, x0:x1] = True
    free = ~solid & ~fl; lab, n = nd.label(free)
    if n > 1:
        sizes = nd.sum(free, lab, range(1, n + 1))
        boxcells = set()
        for g, v in st.items():
            if v[4] is None and v[5] is None:
                for yy in (v[1] - HS + 1, v[1], v[1] + HS - 1):
                    for xx in (v[0] - HS + 1, v[0], v[0] + HS - 1):
                        rr_, cc_ = int((yy - OY) // C), int((xx - OX) // C)
                        if 0 <= rr_ < Wd.rows and 0 <= cc_ < Wd.cols: boxcells.add(lab[rr_, cc_])
        for k in range(1, n + 1):
            if sizes[k - 1] >= 120 or k in boxcells: continue
            ys, xs = np.where(lab == k)
            # only pockets that touch the flood (seams between segments), never a dry room
            ring = np.zeros_like(free); ring[ys, xs] = True; ring = nd.binary_dilation(ring) & fl
            if not ring.any(): continue
            fillc = nd.binary_dilation(lab == k) & OPENC & ~solid               # the pocket plus the partly covered cells around it
            for yy, xx in zip(*np.where(fillc)): md.rectangle([OX + xx * C, OY + yy * C, OX + xx * C + C - 1, OY + yy * C + C - 1], fill=255)
            POCKETS.append((round(t, 2), int(sizes[k - 1])))
    return m
def shadow_layer(t, tau, st, hp):
    m = flood_mask(t, tau, st, hp)
    dx, dy = int(6 * math.sin(t * 0.7)), int(5 * math.cos(t * 0.5))
    tex = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tex.paste(SHTEX, (OX - 20 + dx, OY - 20 + dy))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); L.paste(tex, (0, 0), m)
    free = ImageChops.subtract(floor_mask, m)                                 # open floor the shadow borders
    ox_, oy_ = int(t * 23) % 160, int(t * 17) % 160; nzc = NZ.crop((ox_, oy_, ox_ + W, oy_ + H))
    glow = free.filter(ImageFilter.GaussianBlur(8)).point(lambda v: min(255, int(v * 2.4)))
    ga = ImageChops.multiply(ImageChops.multiply(glow, m), nzc)
    gl = Image.new('RGBA', (W, H), (150, 92, 236, 255)); gl.putalpha(ga.point(lambda v: int(v * 0.8))); L.alpha_composite(gl)
    edge = ImageChops.multiply(free.filter(ImageFilter.MaxFilter(5)), m)
    el = Image.new('RGBA', (W, H), (206, 164, 255, 255)); el.putalpha(ImageChops.multiply(edge, nzc).point(lambda v: int(v * 0.75))); L.alpha_composite(el)
    return L, m
BOXI = {g: box_img(g, 2 * HS) for g in G}
VIG = vignette()
_ex = Image.new('L', (W, H), 0); ImageDraw.Draw(_ex).ellipse([EX0 - 120, EY0 - 120, EX1 + 120, EY1 + 120], fill=255)
VIG.putalpha(ImageChops.multiply(VIG.getchannel('A'), ImageChops.invert(_ex.filter(ImageFilter.GaussianBlur(40)))))
_gb = GUMI.crop(GUMI.getbbox()); GUM_HELD = _gb.resize((28, max(1, int(28 * _gb.height / _gb.width))), Image.NEAREST)
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
    portal_glow(img, EX0, EY0, EX1, EY1, t, 'left')
    bd_ = ImageDraw.Draw(img); bd_.rectangle([EX0, EY0, EX1 - 1, EY0 + 7], fill=(56, 52, 60, 255))                # raised portcullis
    for xx in range(EX0 + 5, EX1 - 3, 12): bd_.rectangle([xx, EY0 + 7, xx + 3, EY0 + 14], fill=(66, 62, 72, 255)); bd_.polygon([(xx, EY0 + 14), (xx + 3, EY0 + 14), (xx + 1, EY0 + 19)], fill=(66, 62, 72, 255))
    for k_, (tx_, ty_) in enumerate(TORCHES): torch_flame(img, tx_, ty_, t, k_ * 1.7)
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
    trails(img, FR, fidx(t), G, HS, lambda g: st[g][4] is None and st[g][5] is None, spd=SPD)   # solid colour trails, ~4 box lengths
    for g in G:                                                            # knocked out / crushed: shrink + burst in the guide's colour
        x, y, vx, vy, out, won = st[g]
        if out is None or out > t: continue
        u = (t - out) / 0.3
        if u < 1:
            bi = box_img(g, 2 * HS, dark=0.4 * u); k = 1 - 0.7 * u
            if HOW[g] == 'crush': bi = bi.resize((max(2, int(2 * HS * (1 + 0.3 * u))), max(2, int(2 * HS * k))), Image.NEAREST)
            else: bi = bi.resize((max(2, int(2 * HS * k)), max(2, int(2 * HS * k))), Image.NEAREST)
            img.alpha_composite(bi, (int(x - bi.width / 2), int(y - bi.height / 2)))
    SL, SM = shadow_layer(t, tau, st, hp); img.alpha_composite(SL)
    hold = held_at(t)
    for g in G:
        x, y, vx, vy, out, won = st[g]
        if out is not None and out <= t: continue
        if won is not None and t >= T_CARD: continue
        if hold and hold[1] == g:
            pul = 0.5 + 0.5 * math.sin(t * 14)
            layer(img, lambda dd, x=x, y=y, pul=pul: dd.rectangle([x - HS - 6, y - HS - 6, x + HS + 5, y + HS + 5], outline=STR_COL + (int(140 + 100 * pul),), width=4))
        img.alpha_composite(BOXI[g], (int(round(x - HS)), int(round(y - HS))))
        if hold and hold[1] == g:                                          # the held gummy sits small, centred inside the holder's box
            img.alpha_composite(GUM_HELD, (int(round(x - GUM_HELD.width / 2)), int(round(y - GUM_HELD.height / 2))))
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
            stamp(img, NAME[e[2]] + ': STRENGTH!', STR_COL, t - e[0], e[0] + 1.1 - t, 838)
    if t >= T_WIN:
        u = t - T_WIN; wx, wy = frame_at(T_WIN)[0][WINNER][:2]
        if u < 0.5: layer(img, lambda dd: dd.rectangle([wx - HS - 6 - 40 * u / 0.5, wy - HS - 6 - 40 * u / 0.5, wx + HS + 6 + 40 * u / 0.5, wy + HS + 6 + 40 * u / 0.5], outline=(255, 214, 60, int(255 * (1 - u / 0.5))), width=6))
        if t < T_CARD: text_layer(img, [(EX0 + 110, EY0 - 50, NAME[WINNER] + ' WON', 30, COL[WINNER], 7, 255)])
    roster_at(img, RSP, OUTS, min(t, T_END), WINNER, T_WIN, cw=128, ch=110, compact=True)
    if t >= T_CARD:                                                        # winner card: Syeda's victory pose replaces the box
        u = t - T_CARD; a_ = min(1, u / 0.3); wx, wy = frame_at(T_WIN)[0][WINNER][:2]
        vf = VIC_W[int(u * 8) % len(VIC_W)]; q = min(1.0, u / 0.3); sc = 0.25 + 0.75 * (1 - (1 - q) ** 3)
        vf2 = vf if sc >= 0.999 else vf.resize((max(2, int(vf.width * sc)), max(2, int(vf.height * sc))), Image.NEAREST)
        FEET = 1250; cxp = wx + (540 - wx) * q; cyp = wy + (FEET - wy) * q
        img.alpha_composite(vf2, (int(cxp - vf2.width / 2), int(cyp - vf2.height * (78 / 92))))
        rs = random.Random(int(t * 6))
        layer(img, lambda dd: [sparkle(dd, 540 + rs.uniform(-220, 220), FEET - rs.uniform(60, 400), rs.choice([4, 6, 8]), int(255 * (0.5 + 0.5 * math.sin(t * 9 + i)))) for i in range(7)])
        fs = min(80, int(880 / (len(NAME[WINNER]) + 4)))
        text_layer(img, [(540, MY0 + 70, NAME[WINNER] + ' WON', fs, COL[WINNER], 10, int(255 * a_))])
    img.alpha_composite(VIG)
    if t < T_WIN: img.alpha_composite(HOOK)                                # hook off once someone is through
    return img
STILLS = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else []
if STILLS:
    for x in STILLS: draw(int(round(x * FPS))).convert('RGB').save(f'st_{x:.2f}.png')
    print('pockets filled', POCKETS); sys.exit()
OUTV = os.environ.get('OUTV', 'm05_noaudio.mp4'); wr = Writer(OUTV)
for f in range(NF): wr.write(draw(f))
wr.close()
print('pocket fills (t, cells):', len(POCKETS), POCKETS[:3], POCKETS[-3:])
# events for the mix
out_ev = []; last = -9
for (t_, g, k) in []: pass
cont_t = [i / FPS for i, cf in enumerate(R['contacts']) if any(cf.values())]
for e in EV:
    if e[0] >= T_END - 0.1: continue
    if e[1] == 'hit' and Wd.B[e[3]]['kind'] == 'gate': out_ev.append((round(e[0], 3), 'brick_8bit'))
    elif e[1] == 'hit' and e[3] == BLOCK:
        if e[0] - last > 0.06: out_ev.append((round(e[0], 3), btick_name(e[0]))); last = e[0]
    elif e[1] == 'break':
        out_ev.append((round(e[0], 3), 'crunch_gate' if e[3] != BLOCK else 'crunch_8bit'))   # gate breaks: +16 dB crunch so they clear the bed
        if e[3] == BLOCK: out_ev += [(round(e[0], 3), 'boom_short'), (round(e[0] + 0.02, 3), 'exitcrack')]
        else: out_ev.append((round(e[0] + 0.02, 3), 'brick_8bit'))
    elif e[1] == 'pick': out_ev.append((round(e[0], 3), 'powerup_8bit'))
    elif e[1] == 'out':
        if e[3] == 'gummy': out_ev += [(round(e[0], 3), 'punch_ko'), (round(e[0] + 0.02, 3), 'poof_ko')]     # KO hits +8 dB over the stock files
        else: out_ev += [(round(e[0], 3), 'squish_ko'), (round(e[0] + 0.03, 3), 'buzz_ko')]
out_ev += [(round(T_WIN, 3), 'win_sting'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(out_ev)
json.dump({'events': out_ev, 'end': T_END, 'beats': {'win': T_WIN, 'winner': WINNER, 'card': T_CARD, 'end': T_END, 'block': T_BLK,
           'gates': {g: BB[GATE[g]]['broke'] for g in G}, 'outs': OUTS, 'how': HOW, 'picks': [(e[0], e[2]) for e in PICKS]}}, open('m05_events.json', 'w'), indent=1)
print('done', NF)
