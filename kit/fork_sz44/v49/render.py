import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
from PIL import ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BG = bg_frames('vit_hd.gif', (W, H), box=(420, 0, 420 + 607, 1080), step=2, bright=0.55, blur=3)
G = up(Image.open('../../pixellab/gummies/pick_mush.png').convert('RGBA'), 3)   # 72x78, unchanged
ODD = ImageOps.mirror(G)
HOOK, HB = hook_layer(['FIND THE ODD', 'GUMMY'], accent=1, sub='IN 5 SECONDS', sub_color=(255, 214, 60))
COLS, ROWS = 8, 10; SX, SY = 93, 80
PX0, PX1 = 74, 884
BX0 = 124; BY0 = HB + 100
ODD_RC = (6, 2)                                    # row G, column 3; never shown
THINK = seq('../../fork2/hollow_think', 3, 0, None)
PANEL = (PX0, HB + 54, PX1, BY0 + ROWS * SY + 16)
print('hook', HB, 'panel', PANEL)
T_SHOW, T_END_TIMER, DUR = 2.4, 7.4, 10.6
NF = int(DUR * FPS); wr = Writer('v49_noaudio.mp4')
FONT_L = F(28)
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 5) % len(BG)].copy()
    layer(img, lambda d: (d.rectangle([0, 0, W, H], fill=(10, 8, 18, 70)),
                          d.rounded_rectangle([PANEL[0] - 4, PANEL[1] - 4, PANEL[2] + 4, PANEL[3] + 4], 26, fill=(110, 70, 30, 255)),
                          d.rounded_rectangle(PANEL, 22, fill=(236, 222, 188, 255), outline=(255, 214, 60, 255), width=7)))
    d = ImageDraw.Draw(img)
    for c in range(COLS): ctext(d, BX0 + c * SX + SX / 2, BY0 - 40, str(c + 1), FONT_L, (110, 70, 30), 0)
    for r in range(ROWS): d.text((PX0 + 14, BY0 + r * SY + 26), 'ABCDEFGHIJ'[r], font=FONT_L, fill=(110, 70, 30))
    if t < T_SHOW:
        layer(img, lambda dd: dd.rounded_rectangle([BX0 - 6, BY0 - 6, PX1 - 12, PANEL[3] - 10], 18, fill=(214, 196, 156, 255)))
        if t > 0.2:
            n = 3 - int((t - 0.2) / 0.7); n = max(1, n); u = ((t - 0.2) % 0.7) / 0.7
            text_layer(img, [(BX0 + COLS * SX / 2, BY0 + ROWS * SY / 2 - 110, str(n), int(220 * (1.3 - 0.3 * u)), (255, 214, 60), 12, 255)])
    else:
        for r in range(ROWS):
            for c in range(COLS):
                g = ODD if (r, c) == ODD_RC else G
                bob = int(1 * math.sin(t * 3))                      # identical motion for every gummy
                img.alpha_composite(g, (int(BX0 + c * SX + (SX - g.width) / 2), int(BY0 + r * SY + (SY - g.height) / 2 + bob)))
    # timer bar / end message, directly under the hook
    left = max(0.0, min(5.0, T_END_TIMER - t)) if t >= T_SHOW else 5.0
    layer(img, lambda dd: dd.rounded_rectangle([PX0, HB + 6, PX1, HB + 46], 16, fill=(14, 10, 24, 225)))
    d = ImageDraw.Draw(img)
    if t < T_END_TIMER:
        col = (120, 230, 90) if left > 3 else ((255, 200, 60) if left > 1.5 else (240, 70, 60))
        d.rounded_rectangle([PX0 + 6, HB + 12, PX0 + 6 + int((PX1 - PX0 - 12) * left / 5), HB + 40], 12, fill=col)
        ctext(d, (PX0 + PX1) / 2, HB + 14, str(int(math.ceil(left))) if t >= T_SHOW else '5', F(24), (255, 255, 255), 4)
    else:
        u = t - T_END_TIMER
        if u < 1.0:
            layer(img, lambda dd: dd.rounded_rectangle([PX0, HB + 6, PX1, HB + 46], 16, outline=(240, 70, 60, 255), width=4))
            text_layer(img, [((PX0 + PX1) / 2, HB + 10, "TIME'S UP!", 32, (240, 80, 70), 5, int(255 * min(1, u / 0.2)))])
        else:
            text_layer(img, [((PX0 + PX1) / 2, HB + 14, 'COMMENT WHERE IT IS (LIKE B4)', 24, (255, 214, 60), 4, int(255 * min(1, (u - 1.0) / 0.3)))])
    hf = THINK[int(t * 6) % len(THINK)]
    img.alpha_composite(hf, (905 - 87, 1100 - 234))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); print('done')
