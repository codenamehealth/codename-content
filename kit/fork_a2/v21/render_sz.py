import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['PAUSE AND', 'MATCH ALL 4'], accent=1, sub='TO REVEAL YOUR GUILD')
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
GIM = [gummy(g[3], 2) for g in GUILDS]
IH = 300; COLW = 210; GAP = 14; X0 = (W - (4 * COLW + 3 * GAP)) // 2; WY0 = HB + 26; WH = 560
def item_tile(gi):
    t = Image.new('RGBA', (COLW, IH), (0, 0, 0, 0)); j = JIM[gi]
    t.alpha_composite(j, ((COLW - j.width) // 2, 30))
    g = GIM[gi]; t.alpha_composite(g, (COLW - g.width - 18, 150))
    d = ImageDraw.Draw(t); name, _, col, _, _ = GUILDS[gi]
    f = F(22 if len(name) < 10 else 20); w = d.textlength(name, font=f)
    d.text(((COLW - w) / 2, 228), name, font=f, fill=col, stroke_width=4, stroke_fill=(15, 10, 25))
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
FR = up(crop(Image.open('../gen/frame/00.png').convert('RGBA')), 1)
DIRS = [1, -1, 1, -1]
wr = Writer('sz21_noaudio.mp4'); events = []; last = [None] * 4
FACE = {}
for g in ('joy', 'cyrus', 'ray', 'cleo'):
    src = {'joy': 'char1/char11.png', 'cyrus': 'char4/char9.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png'}[g]
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    FACE[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
NF = 10 * FPS
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    # windows
    layer(img, lambda d: [d.rounded_rectangle([X0 + i * (COLW + GAP) - 6, WY0 - 6, X0 + i * (COLW + GAP) + COLW + 6, WY0 + WH + 6], 22, fill=(16, 10, 32, 225), outline=(255, 214, 60, 255), width=6) for i in range(4)])
    for r in range(4):
        p = pos(r, t) * DIRS[r]
        reel = Image.new('RGBA', (COLW, WH), (0, 0, 0, 0))
        base = math.floor(p); frac = p - base
        for k in range(-3, 4):
            gi = ORD[r][(base + k) % 4] if DIRS[r] > 0 else ORD[r][(-(base + k)) % 4]
            y = WH / 2 - IH / 2 + (k - frac) * IH * (-1)
            y = WH / 2 - IH / 2 - (k - frac) * IH
            reel.alpha_composite(TILES[gi], (0, int(y)))
        # motion blur feel: fade top/bottom
        m = Image.new('L', (COLW, WH), 255); md = ImageDraw.Draw(m)
        for yy in range(160):
            a = int(255 * yy / 160); md.line([(0, yy), (COLW, yy)], fill=a); md.line([(0, WH - 1 - yy), (COLW, WH - 1 - yy)], fill=a)
        reel.putalpha(Image.fromarray(np.minimum(np.array(reel.getchannel('A')), np.array(m))))
        img.alpha_composite(reel, (X0 + r * (COLW + GAP), WY0))
        cur = round(pos(r, t))
        if r == 0 and cur != last[0]: events.append((round(t, 3), 'reeltick_8bit'))
        last[r] = cur
    # match band
    by = WY0 + WH // 2
    layer(img, lambda d: (d.rectangle([X0 - 22, by - IH // 2, W - X0 + 22, by + IH // 2], outline=(255, 240, 150, 230), width=5),
                          d.polygon([(X0 - 28, by - 26), (X0 - 4, by), (X0 - 28, by + 26)], fill=(255, 214, 60, 255)),
                          d.polygon([(W - X0 + 28, by - 26), (W - X0 + 4, by), (W - X0 + 28, by + 26)], fill=(255, 214, 60, 255))))
    # guild legend with guides (safe zone: x 76-881)
    ly = WY0 + WH + 34; LX0, LX1 = 76, 881
    layer(img, lambda d: d.rounded_rectangle([LX0, ly - 14, LX1, ly + 226], 20, fill=(10, 6, 22, 200), outline=(120, 90, 180, 255), width=3))
    for i, (name, ji, col, gk, g) in enumerate(GUILDS):
        cx = LX0 + (LX1 - LX0) * (i + 0.5) / 4; fc = FACE[g]
        bob = int(4 * math.sin(t * 4 + i))
        img.alpha_composite(fc, (int(cx - fc.width / 2 - 14), ly + 6 + bob))
        gg = GIM[i]; img.alpha_composite(gg, (int(cx + 30), ly + 62 + bob))
        text_layer(img, [(cx, ly + 128, name, 18, col, 4, 255), (cx, ly + 168, {'joy': 'JOY', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH', 'cleo': 'CLEO'}[g], 18, (230, 230, 230), 3, 255)])
    if t > 9.4: text_layer(img, [((LX0 + LX1) / 2, ly + 262, 'WHICH GUILD DID YOU GET?', 30, (255, 255, 255), 6, 255)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (int(2.2 * FPS) - 2, int(2.2 * FPS), int(4.5 * FPS)): img.convert('RGB').save(f'szchk_{f}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': events}, open('sz21_events.json', 'w')); print('done', len(events))
