# m06 DMOEx9VvQTm recreation: render. usage: python3 dmoe_render.py SEED [stills t1,t2,..]
import sys, os, json, math, random
from dmoe_map import *
from rlib import *
FPS = 30
SEED = sys.argv[1]
R = run(SEED, dur=float(os.environ.get('DUR', '80')))
FR, EV, WIN = R['frames'], R['ev'], R['win']
T_WIN, WINNER = WIN
T_CARD = T_WIN + 0.5; T_END = T_CARD + float(os.environ.get('HOLD', '2.5')); NF = int(round(T_END * FPS))
print('win', WIN, 'end', round(T_END, 2), 'frames', NF)
def fidx(t): return min(max(0, int(round(t * FPS))), len(FR) - 1)
def frame_at(t): return FR[fidx(t)]
OUTS = {g: (R['X'][g]['out'] if R['X'][g]['out'] is not None and R['X'][g]['out'] <= T_WIN else None) for g in G}   # the card freezes the board at T_CARD
MX0, MY0, MX1, MY1 = OX, OY, OX + COLS * C, OY + ROWS * C
BG = castle_backdrop()                                               # the Realm castle scene, blurred and dimmed, fills the frame
WALLC = (150, 140, 132); RIM = (62, 54, 60); HI = (226, 216, 198)
def isw(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or Wd.wall[r, c]
floor_mask = Image.new('L', (W, H), 0); fd = ImageDraw.Draw(floor_mask)
for r in range(ROWS):
    for c in range(COLS):
        if not Wd.wall[r, c] or Wd.haz[r, c]: fd.rectangle([OX + c * C, OY + r * C, OX + c * C + C - 1, OY + r * C + C - 1], fill=255)
for p in PENCILS: fd.rectangle([OX + p['x0'] * C, OY + p['slot0'] * C, OX + p['x1'] * C - 1, OY + p['slot1'] * C - 1], fill=255)   # the slot behind the pencil is floor
# hook on the solid upper-left wall (soft fade masked off the floor); roster 2x2 on the same wall under it
HOOK, HB = hook_wall(os.environ.get('HOOK', 'WHO OUTRUNS|THE WATER?').split('|'), 420, 272, 60, floor_mask)
RSP = {'joy': (80, 446), 'cleo': (339, 446), 'cyrus': (80, 548), 'ray': (339, 548)}
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
bd.rounded_rectangle([MX0 - 8, MY0 - 8, MX1 + 7, MY1 + 7], 8, fill=(34, 30, 38, 255), outline=(14, 12, 18, 255), width=4)
bd.rectangle([MX0, MY0, MX1 - 1, MY1 - 1], fill=WALLC + (255,))
FL = flagstones(MX0, MY0, MX1, MY1, seed=5)                          # courtyard flagstones (Realm palette, darker so the faces pop)
_br = castle_bricks(MX0, MY0, MX1, MY1, seed=7)                      # castle bricks with darker/cracked bricks and moss
BOARD.paste(_br, (0, 0), ImageChops.invert(floor_mask).crop((0, 0, W, H)))
BOARD.paste(FL, (0, 0), floor_mask); bd = ImageDraw.Draw(BOARD)
def solid_vis(r, c):
    if r < 0 or c < 0 or r >= ROWS or c >= COLS: return True
    if Wd.haz[r, c]: return False
    for p in PENCILS:
        if p['slot0'] <= r < p['slot1'] and p['x0'] <= c < p['x1']: return False
    return bool(Wd.wall[r, c])
for r in range(ROWS):
    for c in range(COLS):
        if not solid_vis(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        if not solid_vis(r + 1, c): bd.rectangle([x0, y0 + C - 3, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
        if not solid_vis(r - 1, c):                                    # top face: light lip with a little moss
            bd.rectangle([x0, y0, x0 + C - 1, y0 + 2], fill=HI + (255,))
            if (r * 31 + c * 17) % 5 < 2: bd.rectangle([x0 + (c % 3), y0, x0 + (c % 3) + 5, y0 + 3], fill=(96, 136, 72, 255)); bd.rectangle([x0 + (c % 3) + 1, y0 + 4, x0 + (c % 3) + 3, y0 + 5], fill=(70, 108, 58, 255))
        if not solid_vis(r, c - 1): bd.rectangle([x0, y0, x0 + 2, y0 + C - 1], fill=RIM + (255,))
        if not solid_vis(r, c + 1): bd.rectangle([x0 + C - 3, y0, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
BOARD.alpha_composite(ledge_shadow(Wd, OX, OY, C, solid_vis)); bd = ImageDraw.Draw(BOARD)
EX0, EY0, EX1, EY1 = Wd.px(*EXIT)                                   # exit: glowing gate in the ceiling corner (frame static, light per frame)
for k, yy in enumerate(range(int(EY0), int(EY1), 12)): bd.rectangle([EX0 - 13, yy, EX0 - 1, yy + 10], fill=(200, 188, 170, 255) if k % 2 else (178, 166, 150, 255), outline=(90, 82, 86, 255))
TORCHES = [(330, 760), (200, 1110)]
for (tx_, ty_) in TORCHES: sconce(bd, tx_, ty_)
banner(bd, 96, 706, 62, 140)
_SW = {}
def pencil_img(p, cap):
    # the hazard is a spear stuck out of the step: steel spearhead whose tip covers exactly the 4 hazard cells (kill hitbox
    # unchanged), socket + leather binding, shaded wooden shaft over the solid body cells, wraps and an iron butt cap at the wall.
    if p['i'] in _SW: return _SW[p['i']]
    x0 = OX + p['x0'] * C; x1 = OX + p['x1'] * C; y0 = OY + p['slot0'] * C; Hs = (p['slot1'] - p['slot0']) * C; L_ = x1 - x0
    im = Image.new('RGBA', (L_, Hs), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cy = Hs // 2; OUT = (28, 24, 30, 255)
    hl = 4 * C                                                          # spearhead length = the hazard cells
    sock = hl + 12
    # shaft
    d.rectangle([sock, cy - 5, L_ - 1, cy + 4], fill=OUT); d.rectangle([sock, cy - 4, L_ - 2, cy + 3], fill=(138, 94, 54, 255))
    d.rectangle([sock, cy - 4, L_ - 2, cy - 3], fill=(182, 134, 82, 255)); d.rectangle([sock, cy + 2, L_ - 2, cy + 3], fill=(96, 62, 34, 255))
    for k in range(sock + 14, L_ - 8, 23): d.rectangle([k, cy - 1, k + 5, cy - 1], fill=(112, 76, 42, 255))   # grain
    for wx in (L_ - 46, L_ - 34):                                       # leather wraps near the wall end
        d.rectangle([wx, cy - 6, wx + 7, cy + 5], fill=OUT); d.rectangle([wx + 1, cy - 5, wx + 6, cy + 4], fill=(92, 52, 36, 255)); d.rectangle([wx + 1, cy - 5, wx + 6, cy - 4], fill=(132, 82, 56, 255))
    d.rectangle([L_ - 12, cy - 6, L_ - 1, cy + 5], fill=OUT); d.rectangle([L_ - 11, cy - 5, L_ - 2, cy + 4], fill=(96, 92, 104, 255)); d.rectangle([L_ - 11, cy - 5, L_ - 2, cy - 4], fill=(150, 146, 160, 255))
    # socket + binding
    d.rectangle([hl - 2, cy - 5, sock + 2, cy + 4], fill=OUT); d.rectangle([hl - 1, cy - 4, sock + 1, cy + 3], fill=(150, 156, 172, 255)); d.rectangle([hl - 1, cy - 4, sock + 1, cy - 3], fill=(206, 212, 226, 255))
    d.rectangle([sock - 4, cy - 6, sock + 3, cy + 5], fill=(92, 52, 36, 255))
    # leaf-shaped spearhead, apex at x=0 (the block face, same as the old tip)
    leaf = [(0, cy), (14, cy - 7), (26, cy - 10), (hl - 2, cy - 5), (hl - 2, cy + 4), (26, cy + 9), (14, cy + 6)]
    d.polygon(leaf, fill=OUT)
    d.polygon([(2, cy), (14, cy - 6), (26, cy - 8), (hl - 3, cy - 4), (hl - 3, cy + 3), (26, cy + 7), (14, cy + 5)], fill=(176, 186, 204, 255))
    d.polygon([(3, cy), (14, cy - 5), (26, cy - 7), (hl - 3, cy - 3), (hl - 3, cy - 1)], fill=(226, 234, 246, 255))
    d.line([(5, cy), (hl - 4, cy)], fill=(120, 128, 150, 255), width=1)
    d.point((4, cy - 1), fill=(255, 255, 255, 255))
    _SW[p['i']] = (im, (x0, y0)); return _SW[p['i']]
CAPS = [(255, 140, 170), (170, 110, 240), (90, 170, 255), (110, 210, 120), (250, 200, 70)]
WATER = (34, 92, 190)
_WG = Image.new('RGBA', (1, 2 * H), (0, 0, 0, 0))                       # shaded water: light just under the surface, deep below
for d_ in range(2 * H):
    u_ = min(1.0, d_ / 320.0); _WG.putpixel((0, d_), (int(70 - 46 * u_), int(132 - 74 * u_), int(214 - 82 * u_), 255))
WGRAD = _WG.resize((W, 2 * H))
_v = Image.new('L', (W // 8, H // 8), 0)
for yy in range(H // 8):
    for xx in range(W // 8):
        dx_, dy_ = (xx - W / 16) / (W / 16), (yy - H / 16) / (H / 16); _v.putpixel((xx, yy), int(min(1.0, max(0.0, (dx_ * dx_ + dy_ * dy_) ** 0.5 - 0.55) / 0.75) * 120))
VIG = Image.new('RGBA', (W, H), (6, 4, 12, 255)); VIG.putalpha(_v.resize((W, H), Image.BILINEAR))
_ex = Image.new('L', (W, H), 0); ImageDraw.Draw(_ex).ellipse([OX + 95 * C - 150, OY - 150, OX + 100 * C + 150, OY + 9 * C + 150], fill=255)
VIG.putalpha(ImageChops.multiply(VIG.getchannel('A'), ImageChops.invert(_ex.filter(ImageFilter.GaussianBlur(40)))))   # keep the exit bright
BOXI = {g: box_img(g, 2 * HS) for g in G}; XBOX = {g: box_img(g, 2 * HS, x_mark=True) for g in G}
VIC_W = vic_frames(WINNER, 5)
def draw(f):
    t = f / FPS; st, tau, hp, gm = frame_at(min(t, T_CARD))   # board frozen under the winner card
    img = BG.copy(); img.alpha_composite(BOARD)
    portal_glow(img, EX0, EY0, EX1, EY1, t, 'up')
    bd_ = ImageDraw.Draw(img); bd_.rectangle([EX0 - 2, EY0, EX1 - 1, EY0 + 7], fill=(56, 52, 60, 255))     # raised portcullis
    for xx in range(int(EX0) + 4, int(EX1) - 3, 10): bd_.rectangle([xx, EY0 + 7, xx + 3, EY0 + 15], fill=(66, 62, 72, 255)); bd_.polygon([(xx, EY0 + 15), (xx + 3, EY0 + 15), (xx + 1, EY0 + 20)], fill=(66, 62, 72, 255))
    for k_, (tx_, ty_) in enumerate(TORCHES): torch_flame(img, tx_, ty_, t, k_ * 1.7)
    cap = CAPS[int(t / 2.0) % len(CAPS)]
    for p in PENCILS:
        pim, pos = pencil_img(p, cap); img.alpha_composite(pim, pos)
    trails(img, FR, fidx(min(t, T_CARD)), G, HS, lambda g: st[g][4] is None and st[g][5] is None, spd=SPD)   # solid colour trails, ~4 box lengths
    for g in G:
        x, y, vx, vy, out, won = st[g]
        if out is not None and out <= t: continue
        if won is not None and t >= T_CARD: continue
        img.alpha_composite(BOXI[g], (int(round(x - HS)), int(round(y - HS))))
    # water (only over the open floor), surface line with a gentle ripple
    wy = None
    for (x0, y0, x1, y1, d) in Wd.flood_rects(tau): wy = y0
    if wy is not None:
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle([MX0, int(wy), MX1, MY1], fill=215); m = ImageChops.multiply(m, floor_mask)
        L = WGRAD.crop((0, H - int(wy), W, 2 * H - int(wy)))
        for k in range(14):                                            # drifting ripple glints inside the water
            rx_ = (k * 173 + int(t * 22 * (1 if k % 2 else -1))) % (MX1 - MX0) + MX0; ry_ = int(wy) + 26 + (k * 97) % 600
            ImageDraw.Draw(L).rectangle([rx_, ry_, rx_ + 14, ry_ + 2], fill=(120, 176, 236, 255))
        img.paste(Image.alpha_composite(img, L), (0, 0), m)
        sl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sl)
        for xx in range(MX0, MX1, 6):
            yy = wy + 2 * math.sin(xx * 0.05 + t * 3); sd.rectangle([xx, yy - 2, xx + 5, yy + 1], fill=(214, 240, 255, 245)); sd.rectangle([xx, yy + 2, xx + 5, yy + 3], fill=(120, 190, 250, 200))
            if (xx // 6 + int(t * 4)) % 9 == 0: sd.rectangle([xx + 1, yy - 4, xx + 3, yy - 3], fill=(240, 250, 255, 220))   # foam flecks
        sm = Image.new('L', (W, H), 0); ImageDraw.Draw(sm).rectangle([MX0, int(wy) - 5, MX1, int(wy) + 5], fill=255); sm = ImageChops.multiply(sm, floor_mask)
        img.paste(Image.alpha_composite(img, sl), (0, 0), sm)
    for g in G:                                                        # pencil victims: frozen X marker (drawn over the water, like the reference)
        x, y, vx, vy, out, won = st[g]
        if out is None or out > t: continue
        img.alpha_composite(XBOX[g], (int(round(x - HS)), int(round(y - HS))))
        if t - out < 0.45: burst(img, x, y, (t - out) / 0.45, COL[g], hash(g) % 1000, n=12, R=80)
    roster_at(img, RSP, OUTS, t, WINNER, T_WIN)
    if T_WIN <= t < T_CARD:
        u = (t - T_WIN) / 0.5; wx, wy_ = frame_at(T_WIN)[0][WINNER][:2]
        layer(img, lambda dd: dd.rectangle([wx - HS - 6 - 40 * u, wy_ - HS - 6 - 40 * u, wx + HS + 6 + 40 * u, wy_ + HS + 6 + 40 * u], outline=(255, 214, 60, int(255 * (1 - u))), width=6))
    if t >= T_CARD:
        u = t - T_CARD; a_ = min(1, u / 0.3); wx, wy_ = frame_at(T_WIN)[0][WINNER][:2]
        layer(img, lambda dd: dd.rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], fill=(8, 6, 16, int(170 * a_))))
        vf = VIC_W[int(u * 8) % len(VIC_W)]; q = min(1.0, u / 0.3); sc = 0.25 + 0.75 * (1 - (1 - q) ** 3)
        vf2 = vf if sc >= 0.999 else vf.resize((max(2, int(vf.width * sc)), max(2, int(vf.height * sc))), Image.NEAREST)
        FEET = 1330; cxp = 540; cyp = FEET                       # pose grows in place under the text (no fly-through)
        img.alpha_composite(vf2, (int(cxp - vf2.width / 2), int(cyp - vf2.height * (78 / 92))))
        rs = random.Random(int(t * 6))
        layer(img, lambda dd: [sparkle(dd, 540 + rs.uniform(-220, 220), FEET - rs.uniform(60, 400), rs.choice([4, 6, 8]), int(255 * (0.5 + 0.5 * math.sin(t * 9 + i)))) for i in range(7)])
        fs = min(80, int(880 / (len(NAME[WINNER]) + 6)))
        text_layer(img, [(540, 680, NAME[WINNER] + ' WINS!', fs, COL[WINNER], 10, int(255 * a_))])
    img.alpha_composite(VIG)
    img.alpha_composite(HOOK)
    return img
STILLS = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else []
if STILLS:
    for x in STILLS: draw(int(round(x * FPS))).convert('RGB').save(f'sm_{x:.2f}.png')
    sys.exit()
OUTV = os.environ.get('OUTV', 'm06_noaudio.mp4'); wr = Writer(OUTV)
for f in range(NF): wr.write(draw(f))
wr.close()
out_ev = []; last = -9
for i, cf in enumerate(R['contacts']):
    t = i / FPS
    if any(cf.values()) and t - last > 0.3 and t < T_WIN: out_ev.append((round(t, 3), tick_name(t))); last = t
for e in EV:
    if e[1] == 'out' and e[0] <= T_WIN: out_ev += [(round(e[0], 3), 'squish_ko'), (round(e[0] + 0.03, 3), 'buzz_ko')]   # KO SFX +8/+4 dB variants
out_ev += [(round(T_WIN, 3), 'win_sting'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(e for e in out_ev if e[0] < T_END - 0.1)
json.dump({'events': out_ev, 'end': T_END, 'beats': {'win': T_WIN, 'winner': WINNER, 'card': T_CARD, 'end': T_END, 'outs': OUTS}}, open('m06_events.json', 'w'), indent=1)
print('done', NF)
