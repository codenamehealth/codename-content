import sys, os, math, random, json
sys.path.insert(0, '../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BG = ImageEnhance.Brightness(up(Image.open('../fork3/tavern1/00.png').convert('RGBA'), 3)).enhance(0.62)
THINK = seq('../fork2/hollow_think', 3, 0, 9)
PED = [up(crop(Image.open(f'../fork2/pedestal/{i:02d}.png').convert('RGBA')), 3) for i in (0, 2, 4, 3)]
OPTS = [('A', 'ACV', 'acv'), ('B', 'CREATINE', 'cre'), ('C', 'MUSHROOM', 'mush'), ('D', 'MELATONIN', 'mel')]
TARGET = 'mel'
SIL = up(Image.open(PL + f'gummies/pick_{TARGET}.png').convert('RGBA'), 9)
a = SIL.getchannel('A').point(lambda p: 255 if p > 60 else 0)
SILF = Image.new('RGBA', SIL.size, (24, 18, 40, 255)); SILF.putalpha(a)
# outline ring: dilated alpha minus alpha
from PIL import ImageFilter
dil = a.filter(ImageFilter.MaxFilter(13)); edge = Image.fromarray((__import__('numpy').array(dil).astype(int) - __import__('numpy').array(a).astype(int)).clip(0, 255).astype('uint8'))
END = 10.4; T0 = 0.6; T_UP = 9.2
W_ = Writer('d38_noaudio.mp4'); ev = []
CARD = [(60, 1000), (560, 1000), (60, 1420), (560, 1420)]; CW, CH = 460, 390
for f in range(int(END * FPS)):
    t = f / FPS; img = BG.copy()
    # header
    layer(img, lambda d: d.rectangle([0, 0, W, 300], fill=(14, 10, 24, 200)))
    text_layer(img, [(W / 2, 60, 'WHICH GUMMY', 76, (255, 255, 255), 8, 255), (W / 2, 160, 'FITS THE OUTLINE?', 60, (255, 214, 60), 7, 255)])
    # outline panel
    pop = min(1, t / 0.4)
    def panel(d):
        d.rounded_rectangle([170, 330, W - 170, 930], 30, fill=(16, 12, 30, 215), outline=(255, 214, 60, 255), width=8)
        for k in range(14):
            ang = t * 1.4 + k * 2 * math.pi / 14; r = 250 + 10 * math.sin(t * 3 + k)
            x = W / 2 + r * math.cos(ang); y = 630 + r * 0.9 * math.sin(ang)
            d.rectangle([x - 4, y - 4, x + 4, y + 4], fill=(255, 230, 150, 180))
    layer(img, panel)
    sx, sy = W // 2 - SIL.width // 2, 630 - SIL.height // 2 + int(6 * math.sin(t * 2))
    img.alpha_composite(SILF, (sx, sy))
    glow = Image.new('RGBA', SIL.size, (255, 214, 60, 0)); pulse = 0.6 + 0.4 * math.sin(t * 5)
    glow.putalpha(edge.point(lambda p: int(p * pulse))); img.alpha_composite(glow, (sx, sy))
    text_layer(img, [(W / 2, 860, '?', 60, (255, 255, 255), 6, int(255 * (0.5 + 0.5 * math.sin(t * 4))))])
    # option cards
    for i, ((L, name, k), (cx, cy)) in enumerate(zip(OPTS, CARD)):
        appear = max(0, min(1, (t - 0.15 * i) / 0.3))
        if appear <= 0: continue
        if appear < 1 and not any(e[1] == 'poof' and abs(e[0] - 0.15 * i) < 0.01 for e in ev): ev.append((round(0.15 * i, 3), 'poof'))
        def card(d, cx=cx, cy=cy):
            d.rounded_rectangle([cx, cy, cx + CW, cy + CH], 24, fill=(16, 12, 30, int(215 * appear)), outline=(255, 214, 60, int(255 * appear)), width=6)
        layer(img, card)
        ped = PED[i]; img.alpha_composite(ped, (cx + CW // 2 - ped.width // 2, cy + CH - 70 - ped.height))
        g = gummy(k, 5); bob = int(10 * math.sin(t * 3 + i))
        gy = cy + CH - 80 - ped.height - g.height - 10 + bob
        layer(img, lambda d, cx=cx, gy=gy, g=g: d.ellipse([cx + CW / 2 - g.width / 2 - 20, gy - 16, cx + CW / 2 + g.width / 2 + 20, gy + g.height + 16], fill=(255, 220, 140, 40)))
        img.alpha_composite(g, (cx + CW // 2 - g.width // 2, gy))
        text_layer(img, [(cx + 44, cy + 22, L, 44, (255, 214, 60), 6, 255), (cx + CW / 2, cy + CH - 54, name, 30, (255, 255, 255), 5, 255)])
    # Hollow thinking + timer
    th = THINK[min(8, int(t * 8)) if t < 1.1 else 4 + int(t * 4) % 5]
    img.alpha_composite(th, (40, 940 - 78 * 3))
    rem = max(0.0, T_UP - max(T0, t)) / (T_UP - T0)
    def tbar(d):
        x0, x1, y = 120, W - 120, 1865
        d.rounded_rectangle([x0, y - 18, x1, y + 18], 10, fill=(30, 22, 45, 230), outline=(255, 255, 255, 255), width=4)
        if rem > 0: d.rounded_rectangle([x0 + 6, y - 12, x0 + 6 + (x1 - x0 - 12) * rem, y + 12], 7, fill=(255, 214, 60, 255) if rem > 0.3 else (255, 110, 80, 255))
    layer(img, tbar)
    secs = int(math.ceil(max(0, T_UP - max(T0, t))))
    if t < T_UP:
        if t >= T0 and abs((t - T0) - round(t - T0)) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    else:
        u = t - T_UP
        layer(img, lambda d: d.rounded_rectangle([140, 560, W - 140, 760], 26, fill=(16, 12, 30, 235), outline=(255, 214, 60, 255), width=6))
        text_layer(img, [(W / 2, 590, "TIME'S UP!", 64, (255, 255, 255), 7, 255), (W / 2, 690, 'Comment A, B, C or D', 32, (255, 214, 60), 5, 255)])
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_UP, 3), 'ding_8bit'))
    W_.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/d_{f:04d}.png')
W_.close(); json.dump(ev, open('d38_ev.json', 'w')); print('done')
