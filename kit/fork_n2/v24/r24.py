"""#24 Which vibe (approved): review recut, fixes only.
realm keys ! @ # $ -> E F G H (no @/# in comments), item X -> gummy pile, gummy row: gummy is the hero (4x, gloss on ACV),
44px labels + key badges, comment prompt in the band from frame 0, rows slide in from frame 0, slot-style highlight hops
during the hold and locks one row at a time, hold 1.3s, cut back to the empty opening (loop)."""
import sys, math, json, random
SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP + 'fork1'); from common import *
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import acv_gloss, FF
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
# Oct 29 hookfade pass: boxed band, COMMENT YOUR COMBO, row tabs, ACV tag and the LIKE 2 B G X plate cut; rows are edge-to-edge strips
HOOK, HB = hook_fade(['WHICH VIBE', 'DO I GIVE OFF?'], accent=1, size=64)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
TEST = len(sys.argv) > 1
HILITE = False   # Oct 29 notes: no slot-machine outline hopping through the rows / locking a combo
BG = bg_frames('hub.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.85, blur=0)
GUIDES = [('joy', '1'), ('cyrus', '2'), ('cleo', '3'), ('ray', '4')]
IDL = {g: idle(g, 3) for g, _ in GUIDES}
JARS = Image.open(A + 'jars.png').convert('RGBA')
def jar(i, hgt):
    j = JARS.crop((i * 200, 0, i * 200 + 200, 200)); px = np.array(j); bg = (px[:, :, 0] == px[0, 0, 0]) & (px[:, :, 1] == px[0, 0, 1]) & (px[:, :, 2] == px[0, 0, 2]); px[bg, 3] = 0
    im = crop(Image.fromarray(px)); return im.resize((int(im.width * hgt / im.height), hgt), Image.NEAREST)
def gsrc(k):
    g0 = Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA')
    return acv_gloss(g0) if k == 'acv' else g0
JAR = [(jar(0, 96), 'acv', 'A'), (jar(2, 96), 'mush', 'B'), (jar(1, 96), 'cre', 'C'), (jar(3, 96), 'mel', 'D')]
GM = {k: up(gsrc(k), 4) for k in ('acv', 'mush', 'cre', 'mel')}
REALMS = []
for nm, sym in (('found_hd.gif', 'E'), ('sun_hd.gif', 'F'), ('vit_hd.gif', 'G'), ('recov_hd.gif', 'H')):
    fr = bg_frames(nm, (160, 120), box=(960 - 400, 200, 960 + 400, 800), step=3)
    REALMS.append((fr, sym))
FRM = crop(Image.open(SP + 'fork_a2/gen/frame/00.png').convert('RGBA')).resize((190, 150), Image.NEAREST)
def it(k, i):
    im = crop(Image.open(SP + f'fork_a2/gen/{k}/{i:02d}.png').convert('RGBA')); return up(im, max(1, int(130 / max(im.width, im.height))))
# item X: a little pile of the four product gummies (was a gold gummy that read as a gold nugget)
PILE = Image.new('RGBA', (120, 124), (0, 0, 0, 0))
for k, (x, y) in zip(('mush', 'cre', 'mel'), ((0, 60), (56, 60), (28, 2))):
    g = up(gsrc(k), 2); PILE.alpha_composite(g, (x + (60 - g.width) // 2, y + (64 - g.height)))
PILE = crop(PILE)
ITEMS = [(it('book', 0), 'W'), (PILE, 'X'), (it('hourglass', 5), 'Y'), (it('backpack', 1), 'Z')]
PX0, PX1 = 76, 881
Y1 = HB + 44
ROWS = []; y = Y1
for lab, hh in (('GUIDE', 230), ('GUMMY', 178), ('REALM', 186), ('ITEM', 170)):
    ROWS.append((lab, y, hh)); y += hh + 28
EXY = y - 4                      # example plate top
assert EXY + 74 <= 1498, EXY
COLX = [PX0 + (PX1 - PX0) * (i + 0.5) / 4 for i in range(4)]
CW = (PX1 - PX0) / 4
rng = random.Random(2); SPK = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, 6.28)) for _ in range(40)]
# slot-style highlight: each row hops through its 4 cells (hops slow down), rows lock one at a time
FINAL = [2, 0, 3, 1]              # 3 A H X (not the example)
LOCK = [4.6, 5.1, 5.6, 6.1]; HOP0 = 1.55
def hop_times(r):
    ts = []; t = HOP0 + r * 0.07; dt = 0.11
    while t < LOCK[r] - 0.02:
        ts.append(t); left = LOCK[r] - t
        dt = 0.11 if left > 1.4 else 0.11 + (1.4 - left) * 0.22
        t += dt
    return ts
HOPS = []
for r in range(4):
    ts = hop_times(r); start = (FINAL[r] - len(ts)) % 4    # land exactly on FINAL[r] at the lock
    HOPS.append((ts, start))
def cell_at(r, t):
    ts, start = HOPS[r]
    if t < HOP0 + r * 0.07: return None
    if t >= LOCK[r]: return FINAL[r]
    n = sum(1 for x in ts if x <= t)
    return (start + n - 1) % 4
DUR = 7.5
SLIDE0, SLIDE_DT, SLIDE_LEN = 0.0, 0.3, 0.35
events = []
for r in range(4): events.append((round(SLIDE0 + r * SLIDE_DT + 0.02, 3), 'swish'))
if HILITE:
    for r in range(4): events.append((LOCK[r], 'tick_8bit'))
    events.append((LOCK[3] + 0.05, 'chime'))
def badge(d, x1, y1, key, al):
    f = FF(44); w = d.textlength(key, font=f)
    d.rounded_rectangle([x1 - 66, y1 - 66, x1, y1], 12, fill=(16, 10, 30, al), outline=(255, 214, 60, al), width=4)
    d.text((x1 - 33 - w / 2, y1 - 56), key, font=f, fill=(255, 255, 255, al), stroke_width=4, stroke_fill=(10, 6, 18, al))
def frame(t):
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x - 2, y - 2 + 14 * math.sin(t + p), x + 2, y + 2 + 14 * math.sin(t + p)], fill=(255, 240, 190, int(110 + 100 * math.sin(t * 3 + p)))) for x, y, p in SPK])
    for r, (lab, y0, hh) in enumerate(ROWS):
        u = min(1, max(0, (t - SLIDE0 - r * SLIDE_DT) / SLIDE_LEN)); ease = 1 - (1 - u) ** 3
        if t == 0 and r == 0: u = 0.12; ease = 1 - (1 - u) ** 3      # first row already moving on frame 0
        if u <= 0: continue
        dy = int((1 - ease) * 90); al = int(255 * min(1, u * 1.3))
        layer(img, lambda d, y0=y0, hh=hh, dy=dy, al=al: d.rectangle([0, y0 + dy, W, y0 + hh + dy], fill=(12, 9, 22, int(190 * al / 255))))
        c = cell_at(r, t) if HILITE else None    # Oct 29 notes: highlight removed ("We don't pick for them")
        if c is not None:
            locked = t >= LOCK[r]; cx = COLX[c]
            pl = 1.0 if not locked else 1 + 0.5 * max(0, 1 - (t - LOCK[r]) / 0.25)
            def hl(d, cx=cx, y0=y0, hh=hh, dy=dy, locked=locked, pl=pl):
                x0, x1 = cx - CW / 2 + 6, cx + CW / 2 - 6
                d.rounded_rectangle([x0, y0 + dy + 6, x1, y0 + hh + dy - 6], 16, fill=(255, 214, 60, 70 if locked else 45))
                d.rounded_rectangle([x0, y0 + dy + 6, x1, y0 + hh + dy - 6], 16, outline=(255, 255, 255, 255) if locked else (255, 214, 60, 255), width=int(8 * pl) if locked else 6)
            layer(img, hl)
        for i, cx in enumerate(COLX):
            bob = int(5 * math.sin(t * 3 + i + r))
            if r == 0:
                g, key = GUIDES[i]; s = IDL[g][int(t * 8 + i) % len(IDL[g])]
                img.alpha_composite(s, (int(cx - s.width / 2) - 8, y0 + dy + 222 - 78 * 3))
            elif r == 1:
                j, gk, key = JAR[i]; img.alpha_composite(j, (int(cx - j.width) + 10, y0 + dy + 34 + bob // 2))
                gg = GM[gk]; img.alpha_composite(gg, (int(cx - gg.width / 2) + 14, y0 + dy + hh - 18 - gg.height + bob))
            elif r == 2:
                fr, key = REALMS[i]; fi = fr[int(t * 6) % len(fr)]
                img.alpha_composite(fi, (int(cx - 80), y0 + dy + 30)); img.alpha_composite(FRM, (int(cx - 95), y0 + dy + 15))
            else:
                ii, key = ITEMS[i]; img.alpha_composite(ii, (int(cx - ii.width / 2) - (30 if i == 1 else 10), y0 + dy + 26 + (140 - ii.height) // 2 + bob))
            key = [GUIDES, JAR, REALMS, ITEMS][r][i][-1]
            layer(img, lambda d, cx=cx, y0=y0, hh=hh, dy=dy, al=al, key=key: badge(d, int(cx + CW / 2 - 8), y0 + dy + hh - 8, key, al))
    img.alpha_composite(HOOK)
    return img
if TEST:
    for ts in sys.argv[1:]:
        frame(float(ts)).convert('RGB').save(f't_{ts}.png')
    sys.exit()
wr = Writer('v24_noaudio.mp4')
for f in range(int(round(DUR * FPS))): wr.write(frame(f / FPS))
wr.close()
json.dump({'events': events}, open('v24_events.json', 'w')); print('done', HB, y)
