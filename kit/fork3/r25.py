import sys; sys.path.insert(0, '../fork1')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 40.0; NF = int(DUR * FPS)
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
K = 2
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
IDL = {g: idle(g, K) for g in NAMES}
CHEER = {g: seq(PL + f'maze/anim/{g}_panic', K, 1, 9) for g in NAMES}
EAT = seq('hollow_eat', K, 0, 13)
TGT = [EAT[2], EAT[3], EAT[4], EAT[3]]           # holding the red gummy
HEAT = [EAT[5], EAT[6], EAT[5], EAT[8]]          # decoys: hands at mouth, no gummy visible
FOOT = 78 * K
# background: Liza's castle (vit_hd) scaled to full height
BG = bg_frames('vit_hd.gif', (3413, 1920), step=2)
BG = [b.crop((1415, 0, 1415 + W, H)) for b in BG]
# crowd layout
sprites = []
rows = list(range(700, 2060, 44))
TR = 18; TX = 772
for ri, y in enumerate(rows):
    off = (ri % 2) * 32
    for x in range(-40 + off, 1130, 64):
        x2 = x + rnd.randint(-10, 10); y2 = y + rnd.randint(-6, 6)
        if ri == TR and abs(x2 - TX) < 50: continue
        if ri == TR + 1 and abs(x2 - TX) < 44: continue
        if ri == TR + 2 and abs(x2 - TX) < 20: continue
        g = rnd.choices(NAMES, weights=[1, 1, 1, 1, 1.3])[0]
        r = rnd.random()
        if g == 'hollow' and r < 0.25: kind = 'heat'
        elif r < 0.62: kind = 'idle'
        else: kind = 'cheer'
        sprites.append(dict(g=g, x=x2, y=y2, kind=kind, ph=rnd.randint(0, 7), flip=rnd.random() < 0.5))
sprites.append(dict(g='hollow', x=TX, y=rows[TR] + 7, kind='target', ph=0, flip=False))
sprites.sort(key=lambda s: s['y'])
def spr(s, k):
    if s['kind'] == 'target': fr = TGT[(k // 2) % 4]
    elif s['kind'] == 'heat': fr = HEAT[(k // 2 + s['ph']) % 4]
    elif s['kind'] == 'idle': L = IDL[s['g']]; fr = L[(k + s['ph']) % len(L)]
    else: L = CHEER[s['g']]; fr = L[(k + s['ph']) % len(L)]
    return fr.transpose(Image.FLIP_LEFT_RIGHT) if s['flip'] and s['kind'] != 'target' else fr
NC = 24
CROWD = []
for k in range(NC):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for s in sprites:
        f = spr(s, k); L.alpha_composite(f, (int(s['x'] - f.width / 2), int(s['y'] - FOOT)))
    CROWD.append(L)
# soft shadow band where the crowd meets the castle
SH = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(SH)
for y in range(560, 760): sd.line([(0, y), (W, y)], fill=(20, 14, 10, int(120 * (y - 560) / 200)))
# header card
CARD_IMG = up(crop(Image.open('hollow_eat/03.png').convert('RGBA')), 3)
w = Writer('v25_noaudio.mp4'); ev = []
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy(); img.alpha_composite(SH)
    img.alpha_composite(CROWD[int(t * 8) % NC])
    def hdr(d):
        d.rounded_rectangle([60, 110, W - 60, 420], 26, fill=(250, 246, 236, 238), outline=(40, 30, 50, 255), width=6)
    layer(img, hdr)
    d = ImageDraw.Draw(img)
    ctext(d, 400, 170, 'Only 1% can', F(40), (40, 30, 50), 0); ctext(d, 400, 230, 'find this', F(40), (40, 30, 50), 0)
    ctext(d, 400, 290, 'Hollow', F(52), (150, 60, 200), 0)
    ax = 700; ay = 265
    d.polygon([(ax - 40, ay - 14), (ax + 10, ay - 14), (ax + 10, ay - 32), (ax + 46, ay), (ax + 10, ay + 32), (ax + 10, ay + 14), (ax - 40, ay + 14)], fill=(240, 130, 40), outline=(40, 30, 50), width=4)
    bob = int(4 * math.sin(t * 3))
    img.alpha_composite(CARD_IMG, (860 - CARD_IMG.width // 2, 265 - CARD_IMG.height // 2 + bob))
    # timer bar
    rem = max(0, DUR - 3 - t); frac = rem / (DUR - 3)
    def bar(d):
        d.rounded_rectangle([90, 450, W - 90, 486], 14, fill=(20, 14, 30, 210))
        col = (110, 220, 90) if frac > 0.35 else ((250, 200, 60) if frac > 0.15 else (240, 80, 70))
        if frac > 0: d.rounded_rectangle([96, 456, 96 + (W - 192) * frac, 480], 10, fill=col + (255,))
    layer(img, bar)
    if t < DUR - 3:
        text_layer(img, [(W / 2, 455, f'{int(math.ceil(rem))}s', 24, (255, 255, 255), 4, 255)])
        if rem < 5.5 and abs(rem - round(rem)) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    else:
        u = t - (DUR - 3); a = int(255 * min(1, u / 0.25))
        layer(img, lambda d: d.rounded_rectangle([140, 820, W - 140, 1100], 28, fill=(20, 14, 30, int(225 * a / 255)), outline=(255, 214, 60, a), width=6))
        text_layer(img, [(W / 2, 870, "TIME'S UP!", 64, (255, 214, 60), 8, a), (W / 2, 980, 'Did you find him?', 36, (255, 255, 255), 5, a), (W / 2, 1040, 'Comment where he is', 26, (200, 200, 220), 4, a)])
        if f == int((DUR - 3) * FPS): ev.append((round(t, 3), 'buzz_8bit'))
    w.write(img)
    if f % 150 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/a_{f:04d}.png')
w.close()
json.dump(ev, open('v25_ev.json', 'w')); print('done', len(sprites), 'sprites')
