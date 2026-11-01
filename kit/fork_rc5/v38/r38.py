import sys, os, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
HOOK, HB = hook_layer2(['WHICH GUMMY FITS', 'THE OUTLINE?'], accent=1, sub='Comment A, B, C or D'); print('HB', HB)
BG = ImageEnhance.Brightness(up(Image.open(SP + 'fork3/tavern1/00.png').convert('RGBA'), 3)).enhance(0.62)
THINK = seq(SP + 'fork2/hollow_think', 4, 0, 9)   # 3x -> 4x
PED = [up(crop(Image.open(SP + f'fork2/pedestal/{i:02d}.png').convert('RGBA')), 2) for i in (0, 2, 4, 3)]
OPTS = [('A', 'ACV', 'acv'), ('B', 'CREATINE', 'cre'), ('C', 'MUSHROOM', 'mush'), ('D', 'MELATONIN', 'mel')]
TARGET = 'mel'
SIL = up(Image.open(PL + f'gummies/pick_{TARGET}.png').convert('RGBA'), 7)
a = SIL.getchannel('A').point(lambda p: 255 if p > 60 else 0)
SILF = Image.new('RGBA', SIL.size, (24, 18, 40, 255)); SILF.putalpha(a)
dil = a.filter(ImageFilter.MaxFilter(13)); edge = Image.fromarray((np.array(dil).astype(int) - np.array(a).astype(int)).clip(0, 255).astype('uint8'))
END = 8.3; T0 = 0.3; T_UP = 7.0
PX0, PY0, PX1, PY1 = 250, HB + 50, 1010, HB + 50 + 278; PCX, PCY = (PX0 + PX1) // 2, (PY0 + PY1) // 2
CW, CH = 395, 306
CY0 = PY1 + 16; CARD = [(75, CY0), (487, CY0), (75, CY0 + CH + 12), (487, CY0 + CH + 12)]; print('cards end', CY0 + 2 * CH + 12)
GUMS = {k: (up(acv_gummy_strong(), 4) if k == 'acv' else gummy(k, 4)) for _, _, k in OPTS}
W_ = Writer('d38_noaudio.mp4'); ev = []
for f in range(int(END * FPS)):
    t = f / FPS; img = BG.copy()
    # timer bar under hook
    rem = max(0.0, T_UP - max(T0, t)) / (T_UP - T0)
    def tbar(d):
        x0, x1, y = 90, 1005, HB + 24
        d.rounded_rectangle([x0, y - 13, x1, y + 13], 9, fill=(30, 22, 45, 230), outline=(255, 255, 255, 255), width=4)
        if rem > 0: d.rounded_rectangle([x0 + 6, y - 8, x0 + 6 + (x1 - x0 - 12) * rem, y + 8], 6, fill=(255, 214, 60, 255) if rem > 0.3 else (255, 110, 80, 255))
    layer(img, tbar)
    def panel(d):
        d.rounded_rectangle([PX0, PY0, PX1, PY1], 28, fill=(16, 12, 30, 215), outline=(255, 214, 60, 255), width=8)
        for k in range(14):
            ang = t * 1.4 + k * 2 * math.pi / 14; r = 1 + 0.04 * math.sin(t * 3 + k)
            x = PCX + 300 * r * math.cos(ang); y = PCY + 140 * r * math.sin(ang)
            d.rectangle([x - 4, y - 4, x + 4, y + 4], fill=(255, 230, 150, 180))
    layer(img, panel)
    sx, sy = PCX - SIL.width // 2, PCY - SIL.height // 2 + int(6 * math.sin(t * 2))
    img.alpha_composite(SILF, (sx, sy))
    glow = Image.new('RGBA', SIL.size, (255, 214, 60, 0)); pulse = 0.85 + 0.15 * math.sin(t * 5)
    glow.putalpha(edge.point(lambda p: int(p * pulse))); img.alpha_composite(glow, (sx, sy))
    text_layer(img, [(PX1 - 70, PY1 - 90, '?', 56, (255, 255, 255), 6, int(255 * (0.5 + 0.5 * math.sin(t * 4))))])
    for i, ((L, name, k), (cx, cy)) in enumerate(zip(OPTS, CARD)):
        appear = max(0, min(1, (t + 0.3 - 0.15 * i) / 0.3))   # card A is up on frame 0 (the Hollow stands on it)
        if appear <= 0: continue
        if 0 < i and appear < 1 and not any(e[1] == 'poof' and abs(e[0] - (0.15 * i - 0.3)) < 0.01 for e in ev): ev.append((round(max(0, 0.15 * i - 0.3), 3), 'poof'))
        layer(img, lambda d, cx=cx, cy=cy: d.rounded_rectangle([cx, cy, cx + CW, cy + CH], 22, fill=(16, 12, 30, int(215 * appear)), outline=(255, 214, 60, int(255 * appear)), width=6))
        ped = PED[i]; py = cy + CH - 66 - ped.height
        img.alpha_composite(ped, (cx + CW // 2 - ped.width // 2, py))
        g = GUMS[k]; bob = int(6 * math.sin(t * 3 + i))
        gy = py - g.height + 10 + bob
        layer(img, lambda d, cx=cx, gy=gy, g=g: d.ellipse([cx + CW / 2 - g.width / 2 - 18, gy - 12, cx + CW / 2 + g.width / 2 + 18, gy + g.height + 12], fill=(255, 220, 140, 40)))
        img.alpha_composite(g, (cx + CW // 2 - g.width // 2, gy))
        text_layer(img, [(cx + 52, cy + 16, L, 64, (255, 214, 60), 8, 255), (cx + CW / 2, cy + CH - 56, name, 40, (255, 255, 255), 6, 255)])
    th = THINK[min(8, int(t * 8)) if t < 1.1 else 4 + int(t * 4) % 5]
    img.alpha_composite(th, (76 - 25 * 4, CY0 + 3 - 78 * 4))   # stands on card A's top edge (was floating beside the panel)
    secs = int(math.ceil(max(0, T_UP - max(T0, t))))
    if t < T_UP:
        if T_UP - 3.05 <= t and abs((t - T0) - round(t - T0)) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))   # ticks only in the last 3s
    else:
        layer(img, lambda d: d.rounded_rectangle([PX0 + 20, PCY - 100, PX1 - 20, PCY + 100], 26, fill=(16, 12, 30, 240), outline=(255, 214, 60, 255), width=6))
        text_layer(img, [(PCX, PCY - 76, "TIME'S UP!", 66, (255, 255, 255), 8, 255), (PCX, PCY + 20, 'A, B, C OR D?', 48, (255, 214, 60), 7, 255)])
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_UP, 3), 'ding_8bit'))
    img.alpha_composite(HOOK)
    W_.write(img)
    if f in (0, 60, 150, 290): img.convert('RGB').save(f'prev/d38_{f:04d}.png')
W_.close(); json.dump({'events': ev}, open('d38_ev.json', 'w')); print('done', HB)
