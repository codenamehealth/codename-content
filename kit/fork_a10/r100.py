import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a10')
from common7 import *
import plan100
OUT = SP + 'fork_a10/v100/'; G = SP + 'fork_a10/gen/'
STEPS, FPOS, WALLS = plan100.plan(5)
CC, RR, S = 8, 10, 108
BX, BY = (W - CC * S) // 2, 560
GOAL = plan100.GOAL
# ground: grass everywhere, flagstone board
court = wang(G + 'court_meta.json', G + 'court_sheet.png')
GRASS = up(court[(False, False, False, False)], 3); FLAG = up(court[(True, True, True, True)], 3)
BASE = Image.new('RGBA', (W, H), (30, 60, 30, 255))
for y in range(0, H, GRASS.height):
    for x in range(0, W, GRASS.width):
        g = GRASS if (x // 96 + y // 96) % 2 else GRASS.transpose(Image.FLIP_LEFT_RIGHT); BASE.alpha_composite(g, (x, y))
board = Image.new('RGBA', (CC * S, RR * S))
for y in range(0, RR * S, FLAG.height):
    for x in range(0, CC * S, FLAG.width):
        fl = FLAG if (x // 96 + y // 96) % 2 else FLAG.transpose(Image.FLIP_LEFT_RIGHT); board.alpha_composite(fl, (x, y))
BASE.alpha_composite(board, (BX, BY))
def frame_board(d):
    d.rectangle([BX - 14, BY - 14, BX + CC * S + 14, BY + RR * S + 14], outline=(70, 66, 80, 255), width=14)
    d.rectangle([BX - 16, BY - 16, BX + CC * S + 16, BY + RR * S + 16], outline=(30, 26, 36, 255), width=3)
    for c in range(1, CC): d.line([BX + c * S, BY, BX + c * S, BY + RR * S], fill=(255, 255, 255, 40), width=2)
    for r in range(1, RR): d.line([BX, BY + r * S, BX + CC * S, BY + r * S], fill=(255, 255, 255, 40), width=2)
layer(BASE, frame_board)
BAN = up(crop(Image.open(G + 'banner/00.png').convert('RGBA')), 3)
for x in (40, W - 40 - BAN.width): BASE.alpha_composite(BAN, (x, BY + 300))
HDR = bg_frames('bg_castle.gif', (W, 470), box=(0, 60, 1600, 756), step=2, bright=0.6)
# wall bar sprite (pixel art at 1/4 res then x4)
def bar(length_px, vertical):
    L = length_px // 4; T = 8
    im = Image.new('RGBA', (L, T), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, L - 1, T - 1], fill=(22, 30, 70, 255)); d.rectangle([1, 1, L - 2, T - 2], fill=(70, 130, 232, 255))
    d.line([1, 1, L - 2, 1], fill=(170, 210, 255, 255)); d.line([1, T - 2, L - 2, T - 2], fill=(40, 80, 170, 255)); d.line([1, 2, L - 2, 2], fill=(120, 175, 250, 255))
    for x in range(3, L - 2, 7): d.rectangle([x, 3, x + 1, 4], fill=(255, 214, 60, 255))
    im = up(im, 4)
    return im.rotate(90, expand=True) if vertical else im
BAR_H = bar(S + 24, False); BAR_V = bar(S + 24, True)
def wall_pos(e):
    k, r, c = e
    if k == 'h': return (BX + c * S - 12, BY + (r + 1) * S - 16, BAR_H)
    return (BX + (c + 1) * S - 16, BY + r * S - 12, BAR_V)
def cell_xy(p): return (BX + p[1] * S + S / 2, BY + p[0] * S + S / 2)
HF = gif_frames(A + 'hollow-walk-front.gif', h=150); HS = gif_frames(A + 'hollow-walk-side.gif', h=150)
HSL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in HS]
HPAN = seq(PL + 'maze/anim/hollow_panic', 2, 1, 9); HSIT = seq(SP + 'fork_a4/hollow_sit', 2, 1, None)
CIDL = idle('cleo', 2); CBLK = seq(SP + 'fork_a4/cleo_block', 2, 1, None); CVIC = vic('cleo', 300)
GOLD = gummy('gold', 3)
CX, CY = W / 2, 1880
T0, TURN = 2.4, 0.62
NT = len(STEPS); T_SEAL = T0 + (NT - 1) * TURN; END = T_SEAL + 4.2
def hollow_state(t):
    if t < T0: return cell_xy(STEPS[0][1]), None
    k = min(NT - 1, int((t - T0) / TURN)); u = (t - T0 - k * TURN) / TURN
    placed, pos, move = STEPS[k]
    a = cell_xy(pos)
    if move and u > 0.35:
        b = cell_xy(move); v = min(1, (u - 0.35) / 0.6); v = v * v * (3 - 2 * v)
        return (a[0] + (b[0] - a[0]) * v, a[1] + (b[1] - a[1]) * v), (move[0] - pos[0], move[1] - pos[1])
    return a, None
w = Writer(OUT + 'noaudio.mp4'); ev = []; NF = int(END * FPS)
for f in range(NF):
    t = f / FPS
    img = BASE.copy()
    img.alpha_composite(HDR[int(t * 6) % len(HDR)], (0, 0))
    layer(img, lambda d: (d.rectangle([0, 0, W, 470], fill=(14, 10, 24, 90)), d.rectangle([0, 462, W, 470], fill=(70, 66, 80, 255))))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 120, 'THE CLEANEST', F(62)); ctext(d, W / 2, 210, 'TRAP EVER', F(76), (255, 214, 60), 8)
    # goal gummy
    gx, gy = cell_xy(GOAL); bob = 6 * math.sin(t * 4)
    layer(img, lambda d2: d2.ellipse([gx - 50, gy - 50 + bob, gx + 50, gy + 50 + bob], fill=(255, 220, 90, 70)))
    img.alpha_composite(GOLD, (int(gx - GOLD.width / 2), int(gy - GOLD.height / 2 + bob)))
    # walls placed so far
    k = int((t - T0) / TURN) if t >= T0 else -1
    shake = 0
    for i in range(max(0, min(NT, k + 1))):
        placed = STEPS[i][0]
        if not placed: continue
        x, y, im = wall_pos(placed); tp = T0 + i * TURN; u = t - tp
        if u < 0.2:
            v = u / 0.2; y2 = y - 160 * (1 - v) ** 2; a = int(255 * v)
            im2 = im.copy(); im2.putalpha(im2.getchannel('A').point(lambda p, a=a: p * a // 255)); img.alpha_composite(im2, (int(x), int(y2)))
        else:
            img.alpha_composite(im, (int(x), int(y)))
            if u < 0.5:
                def dust(d2, x=x, y=y, im=im, u=u):
                    for q in range(8):
                        px = x + (q / 7) * im.width; py = y + im.height / 2
                        d2.ellipse([px - 10 - 30 * u, py - 10 - 30 * u, px + 10 + 30 * u, py + 10 + 30 * u], fill=(220, 210, 190, int(160 * (1 - u / 0.5))))
                layer(img, dust)
            if u < 0.12: shake = 4
        if f == int(round(tp * FPS)) + 6: ev.append((round(t, 3), 'brick_8bit' if i < NT - 2 else 'boom'))
    # hollow
    (hx, hy), mv = hollow_state(t)
    if t >= T_SEAL + 0.2:
        fr = HPAN[int(t * 12) % 8] if t < T_SEAL + 1.4 else HSIT[min(len(HSIT) - 1, int((t - T_SEAL - 1.4) * 10))]
        img.alpha_composite(fr, (int(hx - fr.width / 2), int(hy + 40 - 78 * 2)))
    else:
        if mv is None: fr = HF[0]
        elif mv[0] > 0: fr = HF[int(t * 10) % 6]
        elif mv[1] > 0: fr = HS[int(t * 10) % 6]
        else: fr = HSL[int(t * 10) % 6]
        layer(img, lambda d2: d2.ellipse([hx - 34, hy + 30, hx + 34, hy + 46], fill=(0, 0, 0, 80)))
        img.alpha_composite(fr, (int(hx - fr.width / 2), int(hy + 40 - fr.height)))
    # cleo below the board
    if t >= T_SEAL + 0.8:
        fr = CVIC[int((t - T_SEAL) * 8) % len(CVIC)]; img.alpha_composite(fr, (int(CX - fr.width / 2), int(CY - fr.height)))
    else:
        u = (t - T0) % TURN if t >= T0 else 9
        if u < 0.3 and k < NT and k >= 0 and STEPS[k][0]: fr = CBLK[min(len(CBLK) - 1, int(u / 0.3 * len(CBLK)))]
        else: fr = CIDL[int(t * 8) % len(CIDL)]
        img.alpha_composite(fr, (int(CX - fr.width / 2), int(CY - 78 * 2)))
    # intro
    if t < T0:
        a = int(255 * min(1, t / 0.3) * min(1, (T0 - t) / 0.3))
        def cards(d2):
            for i, (nm, col) in enumerate((('CLEO', (90, 150, 255)), ('HOLLOW', (170, 160, 200)))):
                x0 = 120 + i * 450
                d2.rounded_rectangle([x0, 760, x0 + 390, 1160], 22, fill=(18, 14, 30, int(a * 0.85)), outline=col + (a,), width=6)
        layer(img, cards)
        for i, g in enumerate(('cleo', 'hollow')):
            fr = idle(g, 3)[int(t * 8) % 4] if False else (CIDL[int(t * 8) % len(CIDL)] if g == 'cleo' else HF[0])
            fr = up(fr, 1.5) if g == 'cleo' else fr
            x0 = 120 + i * 450 + 195
            f2 = fr.copy(); f2.putalpha(f2.getchannel('A').point(lambda p: p * a // 255)); img.alpha_composite(f2, (int(x0 - f2.width / 2), int(1060 - f2.height)))
        text_layer(img, [(315, 1090, 'CLEO', 40, (90, 150, 255), 6, a), (765, 1090, 'HOLLOW', 40, (190, 180, 220), 6, a),
                         (W / 2, 900, 'VS', 56, (255, 255, 255), 8, a), (W / 2, 660, 'PICK A SIDE!', 60, (255, 255, 255), 8, a)])
    # trap
    if t >= T_SEAL:
        u = t - T_SEAL
        def tint(d2):
            for p in [(5, 0), (6, 0), (7, 0)]:
                x0, y0 = BX + p[1] * S, BY + p[0] * S
                d2.rectangle([x0 + 4, y0 + 4, x0 + S - 4, y0 + S - 4], fill=(90, 150, 255, int(70 + 30 * math.sin(t * 8))))
        layer(img, tint)
        s = 1 + max(0, 0.5 - u) * 1.6
        text_layer(img, [(W / 2, 740, 'TRAPPED!', int(86 * s), (255, 80, 80), 10, int(255 * min(1, u / 0.15)))])
        if u > 0.8:
            a = int(255 * min(1, (u - 0.8) / 0.3))
            text_layer(img, [(W / 2, 860, 'CLEO WINS!', 58, (110, 170, 255), 8, a), (W / 2, 945, 'Which side did you pick?', 32, (255, 255, 255), 6, a)])
        if f == int(round(T_SEAL * FPS)) + 1: ev.append((round(t, 3), 'slot'))
        if f == int(round((T_SEAL + 0.8) * FPS)): ev.append((round(t, 3), 'victory'))
    if f == int(round(T0 * FPS)): ev.append((round(t, 3), 'go_8bit'))
    if shake:
        img = img.transform(img.size, Image.AFFINE, (1, 0, random.Random(f).choice([-shake, shake]), 0, 1, 0))
    w.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p_{f:04d}.png')
w.close(); json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev), NT)
