p='r92.py'; s=open(p).read()
def R(a,b):
    global s
    assert s.count(a)==1,a; s=s.replace(a,b)
R("import numpy as np\n", "import numpy as np\nimport hook as HK\n# rc10 review recut (source fork_sz86/v92/r92.py). Bennett loves it: bug/legibility/universal fixes only; same shuffles, same answer.\n")
R("FX, FY, FS = 490, 1000, 0.85", "FX, FY, FS = 496, 1030, 0.85   # rc10: play area 30px lower (taller hook band), x +6 so the bigger numbers clear the left edge")
R("HOOKS = {k: hook_layer(['NIGHTMARE MODE', k], accent=0, color=(255, 70, 80)) for k in ('LOCK ON TO CLEO', \"DON'T LOSE HER.\", 'WHICH NUMBER?')}",
"""def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
# rc10: COMMENT HER NUMBER (46px) in the band from frame 0; replaces the 26px end card 'Which number is Cleo? / COMMENT IF YOU KEPT HER'
HOOKS = {k: band(['NIGHTMARE MODE', k], 0, 'COMMENT HER NUMBER', color=(255, 70, 80)) for k in ('LOCK ON TO CLEO', "DON'T LOSE HER.", 'WHICH NUMBER?')}""")
R("T_INTRO = 2.6; MOVE, HOLD = 1.05, 0.45", "T_INTRO = 1.9; MOVE, HOLD = 1.05, 0.45   # rc10: intro 2.6 -> 1.9s (shrink starts 0.5s)")
R("T_END = t; DUR = T_END + 3.2", "T_END = t; DUR = T_END + 2.0   # rc10: question hold 3.2 -> 2.0s, then loop")
R("    x, y = _pos0(i, t); y = max(HBMAX + 66 + 50, min(1500 - 52, y))", "    x, y = _pos0(i, t); y = max(HBMAX + 76 + 50, min(1500 - 52, y))")
R("out = Writer('v94_noaudio.mp4'); events = [(0.2, 'whoosh_8bit')]", "out = Writer('v92_noaudio.mp4'); events = []   # rc10: no fixed-interval whoosh_8bit on every formation change")
R("""        layer(img, lambda dd: dd.ellipse([x - 70, y - 70, x + 70, y + 70], outline=(255, 214, 60, 255), width=8))
        if t < 1.6:
            k = 1.0 if t < 1.0 else max(0.05, 1 - (t - 1.0) / 0.6)
            cf = CLEO_ID[int(t * 6) % len(CLEO_ID)]; cf = cf.resize((max(1, int(cf.width * k)), max(1, int(cf.height * k))), Image.NEAREST)
            img.alpha_composite(cf, (int(x - cf.width / 2), int(y - 40 * k - 78 * 3 * k + cf.height * 0.18)))
            text_layer(img, [(x, y - 330, 'CLEO', 40, (120, 170, 255), 6, 255)])
        if 1.0 <= t < 1.6 and not any(e[1] == 'poof' for e in events): events.append((1.0, 'poof'))
        if t >= 1.6: text_layer(img, [(x, y - 120, 'THAT ONE!', 34, (255, 214, 60), 6, int(255 * min(1, (T_INTRO - t) / 0.4)))])""",
"""        def ring(dd, x=x, y=y):   # rc10: the gold lock-on ring spins from frame 0
            for j in range(8):
                a0 = j * 45 + t * 160; dd.arc([x - 70, y - 70, x + 70, y + 70], a0, a0 + 30, fill=(255, 214, 60, 255), width=8)
        layer(img, ring)
        if t < 1.0:
            k = 1.0 if t < 0.5 else max(0.05, 1 - (t - 0.5) / 0.5)
            cf = CLEO_ID[int(t * 6) % len(CLEO_ID)]; cf = cf.resize((max(1, int(cf.width * k)), max(1, int(cf.height * k))), Image.NEAREST)
            img.alpha_composite(cf, (int(x - cf.width / 2), int(y - 40 * k - 78 * 3 * k + cf.height * 0.18)))
            text_layer(img, [(x, y - 340, 'CLEO', 56, (120, 170, 255), 8, 255)])   # rc10: 40 -> 56px
        if 0.5 <= t < 1.0 and not any(e[1] == 'poof' for e in events): events.append((0.5, 'poof'))
        if t >= 1.0:
            if not any(e[1] == 'twinkle' for e in events): events.append((1.0, 'twinkle'))
            text_layer(img, [(x + 40, y - 136, 'THAT ONE!', 48, (255, 214, 60), 8, int(255 * min(1, (T_INTRO - t) / 0.4)))])   # rc10: 34 -> 48px""")
R("""        layer(img, lambda dd: dd.rounded_rectangle([547 - 150, HBMAX + 10, 547 + 150, HBMAX + 58], 14, fill=(10, 6, 20, 220), outline=(190, 180, 230, 255), width=3))
        text_layer(img, [(547, HBMAX + 20, f'LEVEL {k_done + 1}/{len(sched)}', 28, (190, 180, 230), 5, 255)])""",
"""        lvl = min(k_done + 1, len(sched))   # rc10 BUG FIX: capped (it read LEVEL 9/8 during the last settle)
        layer(img, lambda dd: dd.rounded_rectangle([547 - 220, HBMAX + 10, 547 + 220, HBMAX + 74], 14, fill=(10, 6, 20, 225), outline=(190, 180, 230, 255), width=4))
        text_layer(img, [(547, HBMAX + 20, f'LEVEL {lvl}/{len(sched)}', 44, (210, 200, 245), 7, 255)])   # 28 -> 44px""")
R("""    for (t0, t1, k) in sched:
        if abs(t - t0) < 0.5 / FPS: events.append((round(t0, 3), 'whoosh_8bit'))
""", "")
R("""            ang = -math.pi / 2 + 2 * math.pi * s / N; nx, ny = FX + 378 * math.cos(ang), FY + 378 * math.sin(ang)
            items.append((nx, ny - 16, str(s + 1), 34, (255, 214, 60), 5, a))
        text_layer(img, items)
        layer(img, lambda dd: dd.rounded_rectangle([90, 1416, 866, 1496], 20, fill=(10, 6, 20, int(a * 0.9))))
        text_layer(img, [(478, 1426, 'Which number is Cleo?', 26, (255, 255, 255), 5, a), (478, 1462, 'COMMENT IF YOU KEPT HER', 26, (255, 214, 60), 5, a)])""",
"""            ang = -math.pi / 2 + 2 * math.pi * s / N; nx, ny = FX + 374 * math.cos(ang), FY + 374 * math.sin(ang)
            items.append((nx, ny - 24, str(s + 1), 48, (255, 214, 60), 7, a))   # rc10: numbers 34 -> 48px
        text_layer(img, items)""")
R("    if f in (40, 130, int(DUR * FPS) - 10): img.convert('RGB').save(f'f92_{f}.png')",
  "    if f in (0, 12, 40, int(sched[-1][1] * FPS) + 5, int(DUR * FPS) - 1): img.convert('RGB').save(f'f92_{f}.png')")
R("out.close(); json.dump(events, open('v92_ev.json', 'w')); print('dur', DUR)", "out.close(); json.dump({'events': events}, open('v92_ev.json', 'w')); print('dur', DUR, 'hb', HBMAX)")
open(p,'w').write(s); print('ok')
