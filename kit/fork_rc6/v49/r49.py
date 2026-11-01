# rc6 recut of #49 (approved by Bennett): universal + legibility fixes, and VETTING r049 (odd gummy findable at phone size).
# Source: fork_sz44/v49/render.py. Answer stays G3, never shown.
import sys, math, json, random, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'fork_rc1'); from hook2 import hook_layer2
from PIL import ImageOps
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BG = bg_frames('vit_hd.gif', (W, H), box=(420, 0, 420 + 607, 1080), step=2, bright=0.55, blur=3)
G = up(Image.open(SP0 + 'pixellab/gummies/pick_mush.png').convert('RGBA'), 3)   # 72x78, unchanged
ODD = ImageOps.flip(G)            # was a mirrored highlight (unfindable on a phone); now upside down: one bold difference
HOOK, HB = hook_layer2(['FIND THE ODD', 'GUMMY'], accent=1, sub='Comment it (like B4)')
COLS, ROWS = 8, 10; SX, SY = 93, 79
PX0, PX1 = 74, 884
BX0 = 136
TP = (PX0, HB + 6, PX1, HB + 62)              # timer plate
BY0 = HB + 122
ODD_RC = (6, 2)                                # row G, column 3; never shown
THINK = seq(SP0 + 'fork2/hollow_think', 3, 0, None)
PANEL = (PX0, HB + 68, PX1, BY0 + ROWS * SY + 10)
print('hook', HB, 'panel', PANEL); assert PANEL[3] <= 1496 and BX0 + COLS * SX <= PX1 - 4
T_END_TIMER = 5.0; STAMP = 0.6; HOLD = 1.4; DUR = T_END_TIMER + HOLD      # timer runs from frame 0 (no 2.4s blank board + 3-2-1)
NF = int(round(DUR * FPS)); wr = Writer('v49_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    img = BG[int(t * 5) % len(BG)].copy()
    layer(img, lambda d: (d.rectangle([0, 0, W, H], fill=(10, 8, 18, 70)),
                          d.rounded_rectangle([PANEL[0] - 4, PANEL[1] - 4, PANEL[2] + 4, PANEL[3] + 4], 26, fill=(110, 70, 30, 255)),
                          d.rounded_rectangle(PANEL, 22, fill=(236, 222, 188, 255), outline=(255, 214, 60, 255), width=7)))
    d = ImageDraw.Draw(img)
    for c in range(COLS): ctext(d, BX0 + c * SX + SX / 2, BY0 - 50, str(c + 1), F(44), (110, 70, 30), 0)        # 28 -> 44px
    for r in range(ROWS): d.text((PX0 + 12, BY0 + r * SY + (SY - 44) // 2), 'ABCDEFGHIJ'[r], font=F(44), fill=(110, 70, 30))
    for r in range(ROWS):
        for c in range(COLS):
            g = ODD if (r, c) == ODD_RC else G
            bob = int(round(1 * math.sin(t * 3)))
            img.alpha_composite(g, (int(BX0 + c * SX + (SX - g.width) / 2), int(BY0 + r * SY + (SY - g.height) / 2 + bob)))
    # timer plate under the band: bar + 44px seconds digit; TIME'S UP! after
    left = max(0.0, T_END_TIMER - t)
    layer(img, lambda dd: dd.rounded_rectangle(TP, 16, fill=(14, 10, 24, 230)))
    d = ImageDraw.Draw(img)
    if t < T_END_TIMER:
        col = (120, 230, 90) if left > 3 else ((255, 200, 60) if left > 1.5 else (240, 70, 60))
        x1 = TP[2] - 96
        d.rounded_rectangle([TP[0] + 10, TP[1] + 14, TP[0] + 10 + int((x1 - TP[0] - 10) * left / 5), TP[3] - 14], 12, fill=col)
        ctext(d, TP[2] - 50, TP[1] + 6, str(int(math.ceil(left - 1e-9))), F(44), (255, 255, 255), 6)
    else:
        u = t - T_END_TIMER
        layer(img, lambda dd: dd.rounded_rectangle(TP, 16, outline=(240, 70, 60, 255), width=5))
        text_layer(img, [((TP[0] + TP[2]) / 2, TP[1] + 6, "TIME'S UP!", 44, (240, 80, 70), 7, 255)])
        if u < STAMP:   # big centred stamp over the grid (hard pop), no answer shown
            sc = 1.0 if u > 0.1 else 0.7 + 3 * u; s = int(72 * sc); cy = (BY0 + PANEL[3]) / 2 - 60
            def pl(dd):
                w = dd.textlength("TIME'S UP!", font=F(s)); dd.rounded_rectangle([(PX0 + PX1) / 2 - w / 2 - 30, cy - 30, (PX0 + PX1) / 2 + w / 2 + 30, cy + s + 30], 22, fill=(14, 10, 24, 240), outline=(240, 70, 60, 255), width=8)
            layer(img, pl); text_layer(img, [((PX0 + PX1) / 2, cy, "TIME'S UP!", s, (255, 90, 80), 12, 255)])
    # thinking Hollow removed: he floated mid-air beside the board (SPEC 13) and there is no ground inside the safe zone there
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (0, 60, 150, 160, NF - 1): img.convert('RGB').save(f'p49_{f:04d}.png')
wr.close()
ev = [(0.0, 'go_8bit'), (2.0, 'tick_8bit'), (3.0, 'tick_8bit'), (4.0, 'tick_8bit'), (T_END_TIMER, 'buzz_8bit')]
json.dump({'events': ev}, open('v49_ev.json', 'w')); print('done', DUR, NF)
