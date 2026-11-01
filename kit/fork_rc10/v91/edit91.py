p='r91.py'; s=open(p).read()
def R(a,b):
    global s
    assert s.count(a)==1,a; s=s.replace(a,b)
R("import numpy as np\n", "import numpy as np\nimport hook as HK\nsys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong\n# rc10 review recut (source fork_sz86/v91/r91.py). Bennett loves it: legibility + universal fixes only; same grid, same single path.\n")
R("""HOOK, HB = hook_layer(['FIND THE PATH'], sub='ONLY 1% CAN FIND IT', sub_color=(255, 214, 60))
RULE0 = HB + 12; RULE1 = RULE0 + 84
BX0 = 240; BY0 = RULE1 + 58""",
"""def band(lines, subs, size=72, color=(255, 214, 60)):
    f = ImageFont.truetype(HK.FONT, size); gap = int(size * 0.38); pad = 22
    h = pad + size + sum(gap if i == 0 else 10 for i in range(len(subs))) + sum(ss for _, ss, _ in subs) + 18
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad; w_ = d.textlength(lines[0], font=f)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), lines[0], font=f, fill=(255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += size + gap
    for txt, ss, col in subs:
        fs = ImageFont.truetype(HK.FONT, ss); w_ = d.textlength(txt, font=fs)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), txt, font=fs, fill=col, stroke_width=7, stroke_fill=(10, 6, 18)); y += ss + 10
    return L, HK.Y0 + h
# rc10: ONLY 1% 36 -> 44px; COMMENT YOUR PATH (46px) from frame 0
HOOK, HB = band(['FIND THE PATH'], [('ONLY 1% CAN FIND IT', 44, (255, 214, 60)), ('COMMENT YOUR PATH', 46, (255, 255, 255))])
RULE0 = HB + 8; RULE1 = RULE0 + 102          # rc10: rule row taller, 3x icons, 'YOU MUST GO:' label dropped
BX0 = 240; BY0 = RULE1 + 38""")
R("GUM = {k: gummy(k, 2) for k in CYC}; GUMS = {k: gummy(k, 2) for k in CYC}",
  "GUM = {k: gummy(k, 2) for k in CYC}; GUMS = {k: gummy(k, 3) for k in CYC}\nGUM['acv'] = up(acv_gummy_strong(), 2); GUMS['acv'] = up(acv_gummy_strong(), 3)   # rc10: ACV gummy with the gummy shine")
R("DUR = 9.6; TT0, TT1 = 1.0, 8.0", "DUR = 9.0; TT0, TT1 = 1.0, 8.0   # rc10: TIME'S UP hold 1.6 -> 1.0s, then loop")
R("""    layer(img, lambda dd: dd.ellipse([BX0 + COLS * CS + 4 - 30, BY0 - 10 - 30, BX0 + COLS * CS + 4 + ch.width + 30, BY0 - 10 + ch.height + 30], fill=(255, 220, 120, glow)))
    img.alpha_composite(ch, (BX0 + COLS * CS + 4, BY0 - 10))
    d = ImageDraw.Draw(img)
    ctext(d, 140, BY0 + ROWS * CS - 200, 'START', F(24), (255, 255, 255), 5)
    ctext(d, BX0 + COLS * CS + 4 + ch.width // 2, BY0 - 58, 'END', F(28), (255, 214, 60), 5)""",
"""    CHX = BX0 + COLS * CS + 34; CHY = BY0 + 2                    # rc10: chest beside the top-right cell (was above it), END label under it
    layer(img, lambda dd: dd.ellipse([CHX - 24, CHY - 24, CHX + ch.width + 24, CHY + ch.height + 24], fill=(255, 220, 120, glow)))
    img.alpha_composite(ch, (CHX, CHY))
    d = ImageDraw.Draw(img)
    ctext(d, 140, BY0 + ROWS * CS - 200, 'START', F(28), (255, 255, 255), 6)
    ctext(d, CHX + ch.width // 2 + 2, CHY + ch.height + 8, 'END', F(44), (255, 214, 60), 7)""")
R("""    ctext(d, 232, ym - 12, 'YOU MUST GO:', F(24), (220, 240, 200), 5)
    seq = CYC + CYC[:1]; sx0 = 436
    for i, k in enumerate(seq):
        g = GUMS[k]; x = sx0 + i * 100; img.alpha_composite(g, (int(x - g.width / 2), ym - g.height // 2))
        if i < len(seq) - 1: ctext(d, x + 50, ym - 12, '>', F(24), (255, 255, 255), 4)
    ctext(d, sx0 + len(seq) * 100 - 30, ym - 12, '...', F(26), (255, 255, 255), 4)""",
"""    seq = CYC + CYC[:1]; sx0 = 160; stp = 160
    for i, k in enumerate(seq):
        g = GUMS[k]; x = sx0 + i * stp; img.alpha_composite(g, (int(x - g.width / 2), ym - g.height // 2))
        if i < len(seq) - 1: ctext(d, x + stp // 2, ym - 22, '>', F(44), (255, 255, 255), 6)
    ctext(d, sx0 + (len(seq) - 1) * stp + 104, ym - 22, '..', F(44), (255, 255, 255), 6)
    if t < 1.0:   # rc10: ACV label on first appearance (before the timer starts)
        layer(img, lambda dd: dd.rounded_rectangle([80, RULE1 + 6, 500, RULE1 + 78], 14, fill=(14, 10, 24, 235), outline=(150, 235, 110, 255), width=4))
        text_layer(img, [(290, RULE1 + 20, 'ACV GUMMY', 44, (150, 235, 110), 6, 255)])""")
R("""        layer(img, lambda dd: dd.rounded_rectangle([98, 1408, 858, 1442], 14, fill=(10, 10, 10, 200)))
        d = ImageDraw.Draw(img); col = (120, 220, 90) if u < 0.6 else ((255, 200, 60) if u < 0.85 else (240, 80, 70))
        d.rounded_rectangle([104, 1414, 104 + int(748 * (1 - u)), 1436], 10, fill=col)
        ctext(d, 478, 1458, 'Diagonals not allowed', F(26), (230, 230, 230), 5)""",
"""        TB0 = BY0 + ROWS * CS + 34; TB1 = min(1498, TB0 + 58)      # rc10: one bar, the rule written on it at 44px
        layer(img, lambda dd: dd.rounded_rectangle([90, TB0, 866, TB1], 16, fill=(10, 10, 10, 215)))
        d = ImageDraw.Draw(img); col = (90, 180, 70) if u < 0.6 else ((215, 160, 40) if u < 0.85 else (200, 60, 55))
        d.rounded_rectangle([96, TB0 + 6, 96 + int(764 * (1 - u)), TB1 - 6], 12, fill=col)
        text_layer(img, [(478, (TB0 + TB1) // 2 - 22, 'NO DIAGONALS', 44, (255, 255, 255), 8, 255)])""")
R("""        layer(img, lambda dd: dd.rounded_rectangle([98, 1388, 858, 1496], 22, fill=(14, 10, 24, int(a * 0.9))))
        text_layer(img, [(478, 1400, "TIME'S UP!", 50, (255, 214, 60), 7, a), (478, 1458, 'Did you find it?', 30, (255, 255, 255), 5, a)])""",
"""        TB0 = BY0 + ROWS * CS + 34; TB1 = min(1498, TB0 + 58)
        layer(img, lambda dd: dd.rounded_rectangle([90, TB0, 866, TB1], 16, fill=(14, 10, 24, int(a * 0.95)), outline=(255, 214, 60, a), width=4))
        text_layer(img, [(478, (TB0 + TB1) // 2 - 26, "TIME'S UP!", 52, (255, 214, 60), 8, a)])   # the band already says COMMENT YOUR PATH""")
R("""    if int((t - 0.0) * 1) != int((t - 1 / FPS) * 1) and TT0 <= t < TT1: events.append((round(t, 3), 'tick_8bit'))""",
"""    if f > 0 and int(t) != int(t - 1 / FPS) and 5.0 <= t < TT1 and not any(abs(e[0] - int(t)) < 0.1 and e[1] == 'tick_8bit' for e in events): events.append((float(int(t)), 'tick_8bit'))   # rc10: ticks only on the last 3s""")
R("    if f in (150, 270): img.convert('RGB').save(f'f91_{f}.png')", "    if f in (0, 15, 150, 245, int(DUR * FPS) - 1): img.convert('RGB').save(f'f91_{f}.png')")
R("out.close(); json.dump(events, open('v91_ev.json', 'w')); print('ok')", "out.close(); json.dump({'events': events}, open('v91_ev.json', 'w')); print('ok', BY0, BY0 + ROWS * CS)")
open(p,'w').write(s); print('ok')
