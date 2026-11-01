import sys, math, json, random, os
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP_ + 'fork1'); from common import *
sys.path.insert(0, SP_ + 'pixellab/safezone'); from hook import hook_band
sys.path.insert(0, SP_ + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Oct 29 pass: soft fade hook, 'COMMENT YOUR GUILD' cut (caption asks); reels run the full height of the frame
HOOK, HB = hook_band(['PAUSE AND', 'MATCH ALL 4'], accent=1)   # strip, not fade: the reels behind the hook are busy
PREVIEW = [float(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else None
print('HB', HB)
import numpy as np
JARS = Image.open(A + 'jars.png').convert('RGBA')
# jars.png order: green, cyan, orange, purple (each 200 wide)
def jar(i):
    j = JARS.crop((i * 200, 0, i * 200 + 200, 200)); j = crop(j.convert('RGBA'))
    px = np.array(j); bg = (px[:, :, 0] == px[0, 0, 0]) & (px[:, :, 1] == px[0, 0, 1]) & (px[:, :, 2] == px[0, 0, 2]); px[bg, 3] = 0
    return crop(Image.fromarray(px))
GUILDS = [('FOUNDATION', 0, (120, 230, 80), 'acv', 'joy'), ('ENERGY', 2, (255, 160, 40), 'mush', 'cyrus'),
          ('RECOVERY', 3, (190, 110, 255), 'mel', 'ray'), ('VITALITY', 1, (90, 220, 230), 'cre', 'cleo')]
JIM = [up(jar(g[1]), 1.0) for g in GUILDS]
JIM = [j.resize((int(j.width * 170 / j.height), 170), Image.NEAREST) for j in JIM]
GIM = [up(acv_gummy_strong(), 2) if g[3] == 'acv' else gummy(g[3], 2) for g in GUILDS]
GIM4 = [up(acv_gummy_strong(), 4) if g[3] == 'acv' else gummy(g[3], 4) for g in GUILDS]
GIM3 = [up(acv_gummy_strong(), 3) if g[3] == 'acv' else gummy(g[3], 3) for g in GUILDS]
JIM = [j.resize((int(j.width * 150 / j.height), 150), Image.NEAREST) for j in JIM]
IH = 300; COLW = 210; GAP = 14; X0 = (W - (4 * COLW + 3 * GAP)) // 2; BY = 770; WY0 = 0; WH = H   # payline centre BY; reel columns span the whole frame height
def item_tile(gi):
    # review: 22px labels unreadable -> no text on the reels; each tile is tinted in its guild colour, gummy big (4x) in front of a smaller potion
    t = Image.new('RGBA', (COLW, IH), (0, 0, 0, 0)); d = ImageDraw.Draw(t); name, _, col, _, _ = GUILDS[gi]
    d.rounded_rectangle([10, 14, COLW - 10, IH - 14], 22, fill=col + (95,), outline=col + (255,), width=6)
    j = JIM[gi]; t.alpha_composite(j, (14, 34))
    g = GIM4[gi]; t.alpha_composite(g, (COLW - g.width - 16, IH - g.height - 26))
    return t
TILES = [item_tile(i) for i in range(4)]
rng = random.Random(7)
ORD = [[0, 1, 2, 3], [2, 0, 3, 1], [1, 3, 0, 2], [3, 2, 1, 0]]
TA = [2.2, 4.5, 6.8, 9.0]; GSEQ = [1, 3, 0, 2]          # guild aligned at each TA
SPD = [7.5, 9.0, 6.4, 8.2]
# keyframes per reel: position (float, item units) where integer k means item ORD[k%4] centered
KEYS = []
for r in range(4):
    ks = [(0.0, rng.uniform(0, 4))]; p = ks[0][1]
    for ta, g in zip(TA, GSEQ):
        target = p + SPD[r] * (ta - ks[-1][0])
        # nearest k >= target-1 with ORD[r][k%4]==g
        k = math.floor(target - 1.5)
        while ORD[r][k % 4] != g: k += 1
        ks.append((ta, float(k))); p = k
    ks.append((10.5, p + SPD[r] * 1.45))
    KEYS.append(ks)
def pos(r, t):
    ks = KEYS[r]
    for (t0, p0), (t1, p1) in zip(ks, ks[1:]):
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0); return p0 + (p1 - p0) * u    # linear between keys: speed changes per segment
    return ks[-1][1]
# check alignment frames
al = []
for f in range(300):
    t = f / FPS; ps = [pos(r, t) for r in range(4)]
    cen = [ORD[r][round(p) % 4] if abs(p - round(p)) < 0.12 else None for r, p in enumerate(ps)]
    if None not in cen and len(set(cen)) == 1: al.append((f, cen[0], [round(p - round(p), 2) for p in ps]))
print('aligned frames', al)
BG = bg_frames('bg_moon.gif', (W, H), box=(800 - 253, 0, 800 + 253, 900), step=1, bright=0.6, blur=2)
FR = up(crop(Image.open(SP_ + 'fork_a2/gen/frame/00.png').convert('RGBA')), 1)
DIRS = [1, -1, 1, -1]
wr = None if PREVIEW else Writer('v21_noaudio.mp4'); events = []; last = [None] * 4
FACE = {}
for g in ('joy', 'cyrus', 'ray', 'cleo'):
    src = {'joy': 'char1/char11.png', 'cyrus': 'char4/char9.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png'}[g]
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    FACE[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
NF = 10 * FPS
for f in ([int(round(x * FPS)) for x in PREVIEW] if PREVIEW else range(NF)):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    # windows
    layer(img, lambda d: [d.rectangle([X0 + i * (COLW + GAP) - 6, -10, X0 + i * (COLW + GAP) + COLW + 6, H + 10], fill=(16, 10, 32, 225), outline=(255, 214, 60, 255), width=6) for i in range(4)])
    for r in range(4):
        p = pos(r, t) * DIRS[r]
        reel = Image.new('RGBA', (COLW, WH), (0, 0, 0, 0))
        base = math.floor(p); frac = p - base
        for k in range(-4, 6):
            gi = ORD[r][(base + k) % 4] if DIRS[r] > 0 else ORD[r][(-(base + k)) % 4]
            y = WH / 2 - IH / 2 + (k - frac) * IH * (-1)
            y = BY - IH / 2 - (k - frac) * IH
            reel.alpha_composite(TILES[gi], (0, int(y)))
        # motion blur feel: fade top/bottom
        m = Image.new('L', (COLW, WH), 255); md = ImageDraw.Draw(m)
        for yy in range(160):
            a = int(255 * yy / 160); md.line([(0, yy), (COLW, yy)], fill=a); md.line([(0, WH - 1 - yy), (COLW, WH - 1 - yy)], fill=a)
        img.alpha_composite(reel, (X0 + r * (COLW + GAP), WY0))
        cur = round(pos(r, t))
        if r == 0 and cur != last[0]: events.append((round(t, 3), 'reeltick_8bit'))
        last[r] = cur
    # match band: rows above/below dimmed so only the centre row reads as the line; thick gold payline
    by = BY
    layer(img, lambda d: [d.rectangle([X0 + i * (COLW + GAP), y0_, X0 + i * (COLW + GAP) + COLW, y1_], fill=(6, 4, 14, 165)) for i in range(4) for (y0_, y1_) in ((WY0, by - IH // 2), (by + IH // 2, WY0 + WH))])
    layer(img, lambda d: (d.rectangle([X0 - 22, by - IH // 2, W - X0 + 22, by + IH // 2], outline=(20, 12, 30, 255), width=16),
                          d.rectangle([X0 - 18, by - IH // 2 + 4, W - X0 + 18, by + IH // 2 - 4], outline=(255, 214, 60, 255), width=9),
                          d.polygon([(X0 - 28, by - 26), (X0 - 4, by), (X0 - 28, by + 26)], fill=(255, 214, 60, 255)),
                          d.polygon([(W - X0 + 28, by - 26), (W - X0 + 4, by), (W - X0 + 28, by + 26)], fill=(255, 214, 60, 255))))
    # guild legend with guides (safe zone: x 76-881)
    # legend, one row per guild: guide face (3x) + gummy (3x, tile colour) + guild name 44px
    ly = 1066; LX0, LX1 = 76, 881; RH = (1494 - ly - 12) // 4
    layer(img, lambda d: d.rounded_rectangle([LX0, ly - 8, LX1, 1496], 20, fill=(10, 6, 22, 215), outline=(120, 90, 180, 255), width=4))
    for i, (name, ji, col, gk, g) in enumerate(GUILDS):
        ry = ly + 4 + i * RH; fc = FACE[g]; bob = int(3 * math.sin(t * 4 + i))
        layer(img, lambda d, ry=ry, col=col: d.rounded_rectangle([LX0 + 14, ry + 2, LX1 - 14, ry + RH - 4], 14, fill=col + (55,), outline=col + (200,), width=3))
        img.alpha_composite(fc, (LX0 + 28, ry + (RH - fc.height) // 2 + bob - 4))
        gg = GIM3[i]; img.alpha_composite(gg, (LX0 + 150 + (84 - gg.width) // 2, ry + (RH - gg.height) // 2))
        d = ImageDraw.Draw(img); d.text((LX0 + 262, ry + (RH - 44) // 2), name, font=F(44), fill=col, stroke_width=6, stroke_fill=(15, 10, 25))
    img.alpha_composite(HOOK)
    if PREVIEW: img.convert('RGB').save(f'p_{f:03d}.png')
    else: wr.write(img)
if not PREVIEW: wr.close(); print('done')
