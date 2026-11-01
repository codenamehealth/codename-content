import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
from PIL import ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BG = bg_frames('vit_hd.gif', (W, H), box=(420, 0, 420 + 607, 1080), step=2, bright=0.55, blur=3)
G = up(Image.open('../../pixellab/gummies/pick_mush.png').convert('RGBA'), 3)
ODD = ImageOps.mirror(G)
COLS, ROWS = 8, 10; SX, SY = 108, 104
BX0 = (W - COLS * SX) // 2 + 30; BY0 = 520
ODD_RC = (6, 2)                                    # row 7, column 3 (G3 in the grid labels); never shown
THINK = seq('../../fork2/hollow_think', 3, 0, None)
PANEL = (BX0 - 70, BY0 - 80, BX0 + COLS * SX + 20, BY0 + ROWS * SY + 30)
T_SHOW, T_END_TIMER, DUR = 2.4, 7.4, 10.6
NF = int(DUR * FPS); wr = Writer('v49_noaudio.mp4'); ev = []
FONT_L = F(28)
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 5) % len(BG)].copy()
    layer(img, lambda d: (d.rectangle([0, 0, W, H], fill=(10, 8, 18, 70)),
                          d.rounded_rectangle([PANEL[0] - 12, PANEL[1] - 12, PANEL[2] + 12, PANEL[3] + 12], 30, fill=(110, 70, 30, 255)),
                          d.rounded_rectangle(PANEL, 22, fill=(236, 222, 188, 255), outline=(255, 214, 60, 255), width=8)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 70, 'FIND THE ODD', F(70)); ctext(d, W / 2, 165, 'GUMMY IN', F(70)); ctext(d, W / 2, 260, '5 SECONDS', F(70), (255, 214, 60))
    # grid labels
    for c in range(COLS): ctext(d, BX0 + c * SX + SX / 2 - 30, BY0 - 64, str(c + 1), FONT_L, (110, 70, 30), 0)
    for r in range(ROWS): d.text((PANEL[0] + 16, BY0 + r * SY + 36), 'ABCDEFGHIJ'[r], font=FONT_L, fill=(110, 70, 30))
    if t < T_SHOW:
        # covered board with countdown
        layer(img, lambda dd: dd.rounded_rectangle([PANEL[0] + 50, BY0 - 20, PANEL[2] - 10, PANEL[3] - 10], 18, fill=(214, 196, 156, 255)))
        if t > 0.2:
            n = 3 - int((t - 0.2) / 0.7); n = max(1, n); u = ((t - 0.2) % 0.7) / 0.7
            text_layer(img, [(W / 2 + 25, 1000, str(n), int(220 * (1.3 - 0.3 * u)), (255, 214, 60), 12, 255)])
            if abs(((t - 0.2) % 0.7)) < 0.5 / FPS and t < 2.3: ev.append((round(t, 3), 'tick_8bit'))
    else:
        for r in range(ROWS):
            for c in range(COLS):
                g = ODD if (r, c) == ODD_RC else G
                bob = int(3 * math.sin(t * 3))                      # identical motion for every gummy
                img.alpha_composite(g, (int(BX0 + c * SX + (SX - g.width) / 2 - 30), int(BY0 + r * SY + (SY - g.height) / 2 + bob)))
        if abs(t - T_SHOW) < 0.5 / FPS: ev.append((round(t, 3), 'go_8bit'))
    # timer bar
    left = max(0.0, min(5.0, T_END_TIMER - t)) if t >= T_SHOW else 5.0
    layer(img, lambda dd: dd.rounded_rectangle([60, 400, W - 60, 446], 18, fill=(14, 10, 24, 220)))
    d = ImageDraw.Draw(img)
    col = (120, 230, 90) if left > 3 else ((255, 200, 60) if left > 1.5 else (240, 70, 60))
    d.rounded_rectangle([68, 408, 68 + int((W - 136) * left / 5), 438], 14, fill=col)
    ctext(d, W / 2, 410, str(int(math.ceil(left))) if t >= T_SHOW else '5', F(26), (255, 255, 255), 4)
    if T_SHOW <= t < T_END_TIMER and abs((t - T_SHOW) % 1.0) < 0.5 / FPS and t > T_SHOW + 0.5: ev.append((round(t, 3), 'tick_8bit'))
    # Hollow thinking beside the board
    hf = THINK[int(t * 6) % len(THINK)]
    img.alpha_composite(hf, (W - hf.width + 20, H - hf.height + 30))
    if t >= T_END_TIMER:
        u = t - T_END_TIMER
        if abs(u) < 0.5 / FPS: ev.append((round(t, 3), 'buzz_8bit'))
        a = int(255 * min(1, u / 0.25))
        layer(img, lambda dd: dd.rounded_rectangle([140, 1640, W - 140, 1760], 20, fill=(14, 10, 24, int(225 * a / 255)), outline=(240, 70, 60, a), width=6))
        text_layer(img, [(W / 2, 1668, "TIME'S UP!", 60, (240, 80, 70), 7, a)])
        if u > 0.6:
            a2 = int(255 * min(1, (u - 0.6) / 0.4))
            text_layer(img, [(W / 2 - 60, 1800, 'Comment where it is', 36, (255, 255, 255), 6, a2), (W / 2 - 60, 1852, '(like B4)', 28, (255, 214, 60), 5, a2)])
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close(); json.dump(ev, open('v49_ev.json', 'w')); print('done', len(ev), ev)
