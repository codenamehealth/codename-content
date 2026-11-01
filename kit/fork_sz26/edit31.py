p='v31/r31.py'; s=open(p).read()
R=[("import numpy as np, math, random, subprocess, json, os, glob","import numpy as np, math, random, subprocess, json, os, glob, sys"),
("os.chdir(os.path.dirname(os.path.abspath(__file__)))\nR = '../../';","os.chdir(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['HOLD YOUR THUMB', 'ON THE CRYSTAL'], accent=1)\nprint('hook bottom', HB)\nR = '../../';"),
("Image.open('../shrine1/00.png')","Image.open('../../fork_a3/shrine1/00.png')"),
("up(Image.open('../crystal/03.png').convert('RGBA').crop(Image.open('../crystal/03.png').getbbox()), 5)","up(Image.open('../../fork_a3/crystal/03.png').convert('RGBA').crop(Image.open('../../fork_a3/crystal/03.png').getbbox()), 5)"),
("CX, CY = 510, 700","CX, CY = 470, 790"),
("CAST = [up(Image.open(p).convert('RGBA'), 3) for p in sorted(glob.glob('../joy_cast/*.png'))]\nJX, JY = 800, 1440           # Joy's feet",
 "CAST = [up(Image.open(p).convert('RGBA'), 4) for p in sorted(glob.glob('../../fork_a3/joy_cast/*.png'))]\nJX, JY = 845, 1096           # Joy's feet (4x)\nWX0, WX1, WY0, WY1 = 72, 880, 1118, 1496   # status window"),
("ay = CY - 260 + 18 * math.sin(t * 6)","ay = CY - 225 + 18 * math.sin(t * 6)"),
("(JX, JY - 150), u)","(JX - 20, JY - 190), u)"),
("img.alpha_composite(fr, (JX - fr.width // 2, JY - 78 * 3))","img.alpha_composite(fr, (JX - fr.width // 2, JY - 78 * 4))"),
("""        d.rounded_rectangle([40, 1500, W - 40, 1880], 22, fill=(16, 22, 40, 225), outline=(240, 230, 200, 255), width=6)
        d.rounded_rectangle([52, 1512, W - 52, 1868], 16, outline=(110, 120, 160, 255), width=3)""",
"""        d.rounded_rectangle([WX0, WY0, WX1, WY1], 22, fill=(16, 22, 40, 225), outline=(240, 230, 200, 255), width=6)
        d.rounded_rectangle([WX0 + 12, WY0 + 12, WX1 - 12, WY1 - 12], 16, outline=(110, 120, 160, 255), width=3)"""),
("""    d.text((80, 1540), 'JOY', font=F(34), fill=(140, 230, 110), stroke_width=4, stroke_fill=(10, 10, 20))
    d.text((220, 1548), 'HP', font=F(26), fill=(255, 214, 60), stroke_width=3, stroke_fill=(10, 10, 20))
    d.rectangle([300, 1546, 840, 1576], fill=(40, 30, 50), outline=(240, 230, 200), width=3)""",
"""    d.text((WX0 + 30, WY0 + 36), 'JOY', font=F(34), fill=(140, 230, 110), stroke_width=4, stroke_fill=(10, 10, 20))
    d.text((WX0 + 148, WY0 + 44), 'HP', font=F(26), fill=(255, 214, 60), stroke_width=3, stroke_fill=(10, 10, 20))
    d.rectangle([WX0 + 210, WY0 + 42, WX0 + 610, WY0 + 72], fill=(40, 30, 50), outline=(240, 230, 200), width=3)"""),
("d.rectangle([304, 1550, 304 + int(532 * hp / 100), 1572], fill=col)\n    d.text((860, 1548), f'{int(hp)}/100', font=F(24),",
 "d.rectangle([WX0 + 214, WY0 + 46, WX0 + 214 + int(392 * hp / 100), WY0 + 68], fill=col)\n    d.text((WX0 + 626, WY0 + 47), f'{int(hp)}/100', font=F(20),"),
("x = 80 + (i % 2) * 480; y = 1610 + (i // 2) * 84","x = WX0 + 28 + (i % 2) * 392; y = WY0 + 108 + (i // 2) * 86"),
("ctext(d, min(W - 250, max(250, JX - 120)), JY - 360 - u * 60, nm + ' CLEARED!', F(30), (140, 240, 110), 6, aa)\n                ctext(d, JX - 40, JY - 305 - u * 60, '+15 HP', F(34), (255, 214, 60), 6, aa)",
 "ctext(d, 700, JY - 400 - u * 60, nm + ' CLEARED!', F(30), (140, 240, 110), 6, aa)\n                ctext(d, JX - 20, JY - 345 - u * 60, '+15 HP', F(34), (255, 214, 60), 6, aa)"),
("""    layer(img, lambda d: d.rectangle([0, 200, W, 440], fill=(10, 20, 14, 175)))
    d = ImageDraw.Draw(img)
    if t < T_END:
        ctext(d, W / 2, 240, 'HOLD YOUR THUMB', F(60)); ctext(d, W / 2, 330, 'ON THE CRYSTAL', F(60), (150, 230, 255))
    else:
        u = t - T_END; s = min(1, u / 0.25)
        ctext(d, W / 2, 240, 'ALL DEBUFFS', F(int(40 + 22 * s))); ctext(d, W / 2, 330, 'CLEARED', F(int(40 + 22 * s)), (140, 240, 110))""",
"""    d = ImageDraw.Draw(img)
    if t >= T_END:
        u = t - T_END; s = min(1, u / 0.25)
        ctext(d, W / 2, HB + 24, 'ALL DEBUFFS CLEARED!', F(int(28 + 14 * s)), (140, 240, 110), 6)"""),
("(JX - 70, JY - 160), gu)","(JX - 80, JY - 190), gu)"),
("ctext(d, W / 2, 1040, '+100 HP', F(64), (255, 214, 60), 8)","ctext(d, 470, 960, '+100 HP', F(64), (255, 214, 60), 8)"),
("    ff.stdin.write(img.convert('RGB').tobytes())","    img.alpha_composite(HOOK)\n    ff.stdin.write(img.convert('RGB').tobytes())"),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)
open(p,'w').write(s)
