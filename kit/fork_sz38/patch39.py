s=open('../fork4/r39.py').read()
R=[("os.chdir(os.path.dirname(os.path.abspath(__file__)))","os.chdir(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['THE SHORTCUT OR', 'THE LONG ROAD?'], accent=1)\nTC0, TC1, BC0, BC1 = 280, 770, 300, 824"),
("Image.open('stair/00.png')","Image.open('../fork4/stair/00.png')"),
("Image.open('lilypad/02.png')","Image.open('../fork4/lilypad/02.png')"),
("TOP0, BOT0, PH = 170, 1035, 830","TOP0, BOT0, PH = 470, 972, 830"),
("NST = 9; ST0 = (90, 790); ST1 = (730, 470)","NST = 9; ST0 = (150, 800); ST1 = (720, 560)"),
("d.ellipse([gx - 40, gy - 290, gx + 40, gy - 210]","d.ellipse([gx - 40, gy - 240, gx + 40, gy - 160]"),
("int(gy - 250 - g.height / 2 + bob)","int(gy - 200 - g.height / 2 + bob)"),
("text_layer(P, [(x, 260, 'STUCK!'","text_layer(P, [(x, TC0 + 120, 'STUCK!'"),
("text_layer(P, [(250, 34, 'THE SHORTCUT', 38, (255, 255, 255), 6, 255), (948, 640, 'THE SWAMP'","text_layer(P, [(270, TC0 + 16, 'THE SHORTCUT', 38, (255, 255, 255), 6, 255), (870, TC0 + 380, 'THE SWAMP'"),
("img.alpha_composite(P, (0, TOP0))","img.alpha_composite(P.crop((0, TC0, W, TC1)), (0, TOP0))"),
("text_layer(Q, [(W / 2 - 60, 130, 'MADE IT!'","text_layer(Q, [(400, BC0 + 70, 'MADE IT!'"),
("text_layer(Q, [(x, y - 300 - (t - tg) * 60, '+1 XP'","text_layer(Q, [(x, max(BC0 + 8, y - 270 - (t - tg) * 40), '+1 XP'"),
("text_layer(Q, [(270, 34, 'THE LONG ROAD', 38, (255, 214, 60), 6, 255), (ST1[0] + 150, ST1[1] - 330, 'THE CASTLE'","text_layer(Q, [(290, BC0 + 16, 'THE LONG ROAD', 38, (255, 214, 60), 6, 255), (880, BC0 + 70, 'THE CASTLE'"),
("text_layer(Q, [(W - 140, 34, f'XP {n}/4'","text_layer(Q, [(900, BC0 + 16, f'XP {n}/4'"),
("img.alpha_composite(Q, (0, BOT0))","img.alpha_composite(Q.crop((0, BC0, W, BC1)), (0, BOT0))"),
("d.rectangle([0, TOP0 - 6, W, TOP0 + PH + 6]","d.rectangle([0, TOP0 - 6, W, TOP0 + (TC1 - TC0) + 6]"),
("d.rectangle([0, BOT0 - 6, W, BOT0 + PH + 6]","d.rectangle([0, BOT0 - 6, W, BOT0 + (BC1 - BC0) + 6]"),
("text_layer(img, [(W / 2, 30, 'THE SHORTCUT', 52, (255, 255, 255), 7, 255), (W / 2, 100, 'OR THE LONG ROAD?', 52, (255, 214, 60), 7, 255)])",""),
("d.rounded_rectangle([110, 1868 - 30, W - 110, 1868 + 40], 16, fill=(16, 12, 30, int(220 * a / 255)))","d.rounded_rectangle([110, TOP0 + 10, W - 110, TOP0 + 86], 16, fill=(16, 12, 30, int(230 * a / 255)), outline=(255, 214, 60, a), width=4)"),
("text_layer(img, [(W / 2, 1846, 'Which road are you on?'","text_layer(img, [(W / 2, TOP0 + 30, 'Which road are you on?'"),
("    W_.write(img)\n    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/e_{f:04d}.png')","    img.alpha_composite(HOOK)\n    W_.write(img)\n    if f in (20, 100, 200, 370): img.convert('RGB').save(f'prev/d39_{f:04d}.png')")]
for a,b in R:
    assert s.count(a)==1, a
    s=s.replace(a,b)
open('r39_sz.py','w').write(s); print('ok')
s=open('r39_sz.py').read()
R=[("img = Image.new('RGBA', (W, H), (14, 10, 24, 255))","img = BACK.copy()"),
("STAIRS_IMG = build_stairs()","STAIRS_IMG = build_stairs()\nBACK = bg_frames('vit_hd.gif', (W, H), box=(700, 0, 1700, 1778), step=1000, bright=0.45, blur=10)[0]"),
("(270, TC0 + 16, 'THE SHORTCUT', 38, (255, 255, 255), 6, 255), (870, TC0 + 380, 'THE SWAMP'","(270, TC0 + 16, 'THE SHORTCUT', 38, (255, 255, 255), 6, 255 if t < T_TOP + 1.0 else 0), (905, TC0 + 412, 'THE SWAMP'"),
("fill=(16, 12, 30, int(230 * a / 255))","fill=(16, 12, 30, a)")]
for a,b in R:
    assert s.count(a)==1, a
    s=s.replace(a,b)
open('r39_sz.py','w').write(s); print('ok2')
