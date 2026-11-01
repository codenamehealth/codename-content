import sys, os, math, json
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
sys.path.insert(0, SP + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
# Oct 29 soft-fade + full-bleed pass: no box, 'Comment A, B, C or D' cut (letters + caption carry it). The quiz is now IN the tavern:
# no dimmed backdrop with boxed cards; the four pedestals stand in a row on the big tavern table, the Hollow stands on the floor
# beside it, the outline floats above as a glowing apparition. Option names cut (the picture shows each gummy; letters are the answer).
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['WHICH GUMMY FITS', 'THE OUTLINE?'], accent=1); HOOK_END, _ = hook_fade(["TIME'S UP!"], accent=0, size=72); print('HB', HB)
SHIFT = 120   # tavern shifted up so the table top sits inside the safe zone; the dark under the stage continues to the frame bottom
_t = up(Image.open(SP + 'fork3/tavern1/00.png').convert('RGBA'), 3)
BG = Image.new('RGBA', (W, H), (26, 9, 27, 255)); BG.alpha_composite(_t.crop((0, SHIFT, W, H)), (0, 0))
BG = ImageEnhance.Brightness(BG).enhance(0.78)
THINK = seq(SP + 'fork2/hollow_think', 4, 0, 9)
PED = [up(crop(Image.open(SP + f'fork2/pedestal/{i:02d}.png').convert('RGBA')), 2) for i in (0, 2, 4, 3)]
OPTS = [('A', 'ACV', 'acv'), ('B', 'CREATINE', 'cre'), ('C', 'MUSHROOM', 'mush'), ('D', 'MELATONIN', 'mel')]
TARGET = 'mel'
SIL = up(Image.open(PL + f'gummies/pick_{TARGET}.png').convert('RGBA'), 8)   # back to 8x (room freed by the smaller hook)
a = SIL.getchannel('A').point(lambda p: 255 if p > 60 else 0)
SILF = Image.new('RGBA', SIL.size, (24, 18, 40, 255)); SILF.putalpha(a)
dil = a.filter(ImageFilter.MaxFilter(13)); edge = Image.fromarray((np.array(dil).astype(int) - np.array(a).astype(int)).clip(0, 255).astype('uint8'))
HALO = Image.new('RGBA', (560, 560), (0, 0, 0, 0)); ImageDraw.Draw(HALO).ellipse([60, 60, 500, 500], fill=(255, 214, 120, 70)); HALO = HALO.filter(ImageFilter.GaussianBlur(50))
END = 8.3; T0 = 0.3; T_UP = 7.0
PCX, PCY = 560, 830
OX = [300, 455, 610, 765]; FEETY = 1440          # pedestal bases on the table top
HX, HFEET = 150, 1400                            # the Hollow's body centre / feet (floor beside the table)
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
    img.alpha_composite(HALO, (PCX - 280, PCY - 280))
    def orbit(d):
        for k in range(14):
            ang = t * 1.4 + k * 2 * math.pi / 14; r = 1 + 0.04 * math.sin(t * 3 + k)
            x = PCX + 210 * r * math.cos(ang); y = PCY + 190 * r * math.sin(ang)
            d.rectangle([x - 5, y - 5, x + 5, y + 5], fill=(255, 230, 150, 200))
    layer(img, orbit)
    sx, sy = PCX - SIL.width // 2, PCY - SIL.height // 2 + int(6 * math.sin(t * 2))
    img.alpha_composite(SILF, (sx, sy))
    glow = Image.new('RGBA', SIL.size, (255, 214, 60, 0)); pulse = 0.85 + 0.15 * math.sin(t * 5)
    glow.putalpha(edge.point(lambda p: int(p * pulse))); img.alpha_composite(glow, (sx, sy))
    for i, ((L, name, k), cx) in enumerate(zip(OPTS, OX)):
        appear = max(0, min(1, (t + 0.3 - 0.15 * i) / 0.3))   # A is up on frame 0, the rest pop in by 0.45s (same timing)
        if appear <= 0: continue
        if 0 < i and appear < 1 and not any(e[1] == 'poof' and abs(e[0] - (0.15 * i - 0.3)) < 0.01 for e in ev): ev.append((round(max(0, 0.15 * i - 0.3), 3), 'poof'))
        ped = PED[i]
        if appear < 1: ped = ped.resize((max(1, int(ped.width * appear)), max(1, int(ped.height * appear))), Image.NEAREST)
        layer(img, lambda d, cx=cx: d.ellipse([cx - 52, FEETY - 12, cx + 52, FEETY + 10], fill=(0, 0, 0, 90)))
        py = FEETY - ped.height
        img.alpha_composite(ped, (cx - ped.width // 2, py))
        if appear < 1: continue
        g = GUMS[k]; bob = int(6 * math.sin(t * 3 + i))
        gy = py - g.height + 10 + bob
        layer(img, lambda d, cx=cx, gy=gy, g=g: d.ellipse([cx - g.width / 2 - 6, gy - 4, cx + g.width / 2 + 6, gy + g.height + 4], fill=(255, 220, 140, 45)))
        img.alpha_composite(g, (cx - g.width // 2, gy))
        text_layer(img, [(cx, FEETY - 118 - 136 - 74, L, 64, (255, 214, 60), 8, 255)])
    th = THINK[min(8, int(t * 8)) if t < 1.1 else 4 + int(t * 4) % 5]
    layer(img, lambda d: d.ellipse([HX - 70, HFEET - 12, HX + 70, HFEET + 12], fill=(0, 0, 0, 90)))
    img.alpha_composite(th, (HX - 190, HFEET - 312))
    secs = int(math.ceil(max(0, T_UP - max(T0, t))))
    if t < T_UP:
        if T_UP - 3.05 <= t and abs((t - T0) - round(t - T0)) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))   # ticks only in the last 3s
    else:
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_UP, 3), 'ding_8bit'))
    img.alpha_composite(HOOK_END if t >= T_UP else HOOK)
    W_.write(img)
    if f in (0, 8, 60, 150, 240): img.convert('RGB').save(f'prev/d38_{f:04d}.png')
W_.close(); json.dump({'events': ev}, open('d38_ev.json', 'w')); print('done', HB)
