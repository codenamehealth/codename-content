import sys; sys.path.insert(0, '../../fork_a7')
from common7 import *
import numpy as np
COLS, ROWS = 6, 8; CS = 128
BX0 = (W - COLS * CS) // 2; BY0 = 470
CYC = ['acv', 'mush', 'mel', 'cre']
START, END = (ROWS - 1, 0), (0, COLS - 1)
def nbrs(r, c):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS: yield r + dr, c + dc
def count_paths(G, cap=3):
    n = 0; stack = [(START, 0, {START})]
    if G[START] != 0: return 0
    while stack:
        (r, c), k, seen = stack.pop()
        if (r, c) == END: n += 1
        if n >= cap: return n
        if (r, c) == END: continue
        for rr, cc in nbrs(r, c):
            if (rr, cc) not in seen and G[rr, cc] == (k + 1) % 4: stack.append(((rr, cc), k + 1, seen | {(rr, cc)}))
    return n
def make(seed):
    rnd = random.Random(seed)
    for _ in range(4000):
        path = [START]; seen = {START}
        while path[-1] != END and len(path) < 40:
            opts = [p for p in nbrs(*path[-1]) if p not in seen]
            if not opts: break
            p = rnd.choice(opts); path.append(p); seen.add(p)
        if path[-1] != END or len(path) < 16 or len(path) > 24: continue
        G = np.zeros((ROWS, COLS), int) - 1
        for i, p in enumerate(path): G[p] = i % 4
        for _ in range(60):
            H2 = G.copy()
            for r in range(ROWS):
                for c in range(COLS):
                    if H2[r, c] < 0: H2[r, c] = rnd.randrange(4)
            if count_paths(H2) == 1: return H2, path
    return None
G, PATH = make(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
print('path len', len(PATH), PATH)
SLAB = up(Image.open('../gen/slab/18.png').convert('RGBA').resize((32, 32), Image.NEAREST), CS // 32)
GUM = {k: gummy(k, 2) for k in CYC}; GUMS = {k: gummy(k, 2) for k in CYC}
BGF = bg_frames('bg_thorn.gif', (W, H), box=(400, 0, 906, 900), bright=0.45, blur=3)
HOL = idle('hollow', 2); CHEST = up(crop(Image.open('../../fork_b5/chest_closed/00.png').convert('RGBA')), 3)
LANT = [up(crop(Image.open(p).convert('RGBA')), 3) for p in sorted(glob.glob('../../fork_a7/gen/lantern/*.png'))[:1]]
rnd = random.Random(3); FLIES = [(rnd.uniform(0, W), rnd.uniform(300, H), rnd.uniform(0, 6)) for _ in range(40)]
DUR = 9.6; TT0, TT1 = 1.0, 8.0
out = Writer('v93_noaudio.mp4'); events = [(0.0, 'whoosh_8bit')]
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BGF[int(t * 6) % len(BGF)].copy()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x, y, p in FLIES:
        a = int(120 + 120 * math.sin(t * 2 + p)); fx, fy = x + 20 * math.sin(t * 0.7 + p), y + 15 * math.cos(t * 0.9 + p)
        d.rectangle([fx - 3, fy - 3, fx + 3, fy + 3], fill=(230, 255, 140, max(0, a)))
    img.alpha_composite(L)
    # board frame
    layer(img, lambda dd: dd.rounded_rectangle([BX0 - 26, BY0 - 26, BX0 + COLS * CS + 26, BY0 + ROWS * CS + 26], 20, fill=(24, 30, 22, 235)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([BX0 - 26, BY0 - 26, BX0 + COLS * CS + 26, BY0 + ROWS * CS + 26], 20, outline=(120, 150, 80), width=6)
    d.rounded_rectangle([BX0 - 14, BY0 - 14, BX0 + COLS * CS + 14, BY0 + ROWS * CS + 14], 14, outline=(60, 80, 40), width=4)
    for r in range(ROWS):
        for c in range(COLS):
            delay = (r + c) * 0.035; u = min(1, max(0, (t - delay) / 0.25))
            if u <= 0: continue
            x, y = BX0 + c * CS, BY0 + r * CS - int((1 - u) * 40)
            img.alpha_composite(SLAB, (x, y))
            g = GUM[CYC[G[r, c]]]; bob = int(3 * math.sin(t * 3 + r * 0.7 + c))
            img.alpha_composite(g, (x + CS // 2 - g.width // 2, y + CS // 2 - g.height // 2 + bob))
    # START / END markers
    hf = HOL[int(t * 6) % len(HOL)]; img.alpha_composite(hf, (BX0 - 26 - hf.width + 40, BY0 + ROWS * CS - 78 * 2 + 30))
    ch = CHEST; glow = int(40 + 30 * math.sin(t * 4))
    layer(img, lambda dd: dd.ellipse([BX0 + COLS * CS + 4 - 30, BY0 - 10 - 30, BX0 + COLS * CS + 4 + ch.width + 30, BY0 - 10 + ch.height + 30], fill=(255, 220, 120, glow)))
    img.alpha_composite(ch, (BX0 + COLS * CS + 4, BY0 - 10))
    d = ImageDraw.Draw(img)
    ctext(d, BX0 + 40, BY0 + ROWS * CS + 40, 'START', F(26), (255, 255, 255), 5)
    ctext(d, BX0 + COLS * CS - 20, BY0 - 74, 'END', F(26), (255, 214, 60), 5)
    # header
    layer(img, lambda dd: dd.rectangle([0, 0, W, 410], fill=(8, 10, 8, 150)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 60, 'FIND THE PATH', F(68), (255, 255, 255), 8)
    ctext(d, W / 2, 158, 'ONLY 1% CAN FIND IT', F(34), (255, 214, 60), 6)
    ctext(d, W / 2, 232, 'YOU MUST GO:', F(30), (220, 240, 200), 5)
    seq = CYC + CYC[:1]; sx0 = W / 2 - (len(seq) * 120) / 2 + 30
    for i, k in enumerate(seq):
        g = GUMS[k]; x = sx0 + i * 120; img.alpha_composite(g, (int(x - g.width / 2), 300 - g.height // 2))
        if i < len(seq) - 1: ctext(d, x + 60, 288, '>', F(28), (255, 255, 255), 4)
    ctext(d, sx0 + len(seq) * 120 - 40, 288, '...', F(28), (255, 255, 255), 4)
    # timer + end
    if TT0 <= t < TT1:
        u = (t - TT0) / (TT1 - TT0)
        layer(img, lambda dd: dd.rounded_rectangle([140, 1640, 940, 1680], 14, fill=(10, 10, 10, 190)))
        d = ImageDraw.Draw(img); col = (120, 220, 90) if u < 0.6 else ((255, 200, 60) if u < 0.85 else (240, 80, 70))
        d.rounded_rectangle([146, 1646, 146 + int(788 * (1 - u)), 1674], 10, fill=col)
        ctext(d, W / 2, 1720, 'Diagonals not allowed', F(26), (230, 230, 230), 5)
    elif t >= TT1:
        if not any(e[1] == 'buzz_8bit' for e in events): events.append((TT1, 'buzz_8bit'))
        a = min(255, int((t - TT1) / 0.25 * 255))
        layer(img, lambda dd: dd.rounded_rectangle([110, 1600, 970, 1800], 22, fill=(14, 10, 24, int(a * 0.85))))
        text_layer(img, [(W / 2, 1630, "TIME'S UP!", 54, (255, 214, 60), 7, a), (W / 2, 1720, 'Did you find it?', 34, (255, 255, 255), 5, a)])
    if int((t - 0.0) * 1) != int((t - 1 / FPS) * 1) and TT0 <= t < TT1: events.append((round(t, 3), 'tick_8bit'))
    out.write(img)
    if f % 40 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
out.close(); json.dump(events, open('ev.json', 'w')); print('ok')
