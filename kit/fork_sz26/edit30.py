p='v30/r30.py'; s=open(p).read()
R=[("os.chdir(os.path.dirname(os.path.abspath(__file__)))\nR = '../../';","os.chdir(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['SCREENSHOT', 'THE SECOND'], accent=0, sub='THE GUMMY FITS PERFECTLY')\nprint('hook bottom', HB)\nR = '../../';"),
("TX, TY = W // 2, 1080        # target centre","TX, TY = W // 2, 1020        # target centre\nHW, HH = G.width // 2 + 12, G.height // 2 + 12"),
("    return mins, near","    return mins, near\ndef inside(p):\n    tm = FM / FPS; x0, y0, a0, s0 = path(p, tm)\n    for f in range(int(0.6 * FPS), N, 2):\n        x, y, a, s = path(p, f / FPS); x = TX + x - x0; y = TY + y - y0\n        if y - HH < HB + 16 or y + HH > 1496 or x - HW < 72 or x + HW > 1022: return False\n        if y + HH > 1110 and x + HW > 884: return False\n    return True"),
("p = dict(A1=rng.uniform(150, 260), A2=rng.uniform(40, 110),","p = dict(A1=rng.uniform(110, 190), A2=rng.uniform(25, 70),"),
("B1=rng.uniform(140, 260), B2=rng.uniform(30, 90),","B1=rng.uniform(110, 190), B2=rng.uniform(25, 70),"),
("    mins, near = evalp(p)","    if not inside(p): continue\n    mins, near = evalp(p)"),
("    jg.seek(i); f = jg.convert('RGBA'); f = f.crop(f.getbbox()); k = 330 / f.height; JOY.append(f.resize((int(f.width * k), 330), Image.NEAREST))",
 "    jg.seek(i); f = jg.convert('RGBA').crop((260, 140, 730, 780)); JOY.append(f.resize((282, 384), Image.NEAREST))"),
("vf = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(vf, (40, 1560 - vf.height))","vf = JOY[int(t * 8) % len(JOY)]; img.alpha_composite(vf, (72, 1492 - vf.height))"),
("""    layer(img, lambda d: d.rectangle([0, 210, W, 540], fill=(14, 20, 12, 175)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 250, 'SCREENSHOT THE', F(62)); ctext(d, W / 2, 340, 'SECOND IT FITS', F(62), (170, 230, 110))
    ctext(d, W / 2, 445, 'Only 1 frame works', F(34), (255, 255, 255), 5)
    if t < 0.9: ctext(d, W / 2, 640, 'GET READY...', F(44), (255, 255, 255), 6)
    layer(img, lambda d: d.rectangle([0, 1610, W, 1730], fill=(14, 20, 12, 160)))
    d = ImageDraw.Draw(img); ctext(d, W / 2, 1650, 'How close did you get?', F(36), (255, 214, 60), 6)
""","""    d = ImageDraw.Draw(img)
    if t < 0.9: ctext(d, W / 2, HB + 40, 'GET READY...', F(44), (255, 255, 255), 6)
    if t > DUR - 1.3:
        a_ = int(255 * min(1, (t - (DUR - 1.3)) / 0.25)); L_ = Image.new('RGBA', img.size, (0, 0, 0, 0)); ctext(ImageDraw.Draw(L_), W / 2, HB + 22, 'How close did you get?', F(36), (255, 214, 60), 6, a_); img.alpha_composite(L_)
    img.alpha_composite(HOOK)
"""),
("crop((240, 760, 840, 1400))","crop((240, 700, 840, 1340))"),
]
for a,b in R:
    assert a in s, a[:70]; s=s.replace(a,b)
open(p,'w').write(s)
