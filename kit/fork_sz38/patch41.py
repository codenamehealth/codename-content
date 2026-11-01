s=open('../fork_a4/r41.py').read()
R=[("from common import *","from common import *\nimport os; os.chdir(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['FIND 3', 'DIFFERENCES'], accent=1)"),
("PW, PH = 1000, 700; PX = 40; PY1, PY2 = 280, 1010","PW, PH = 640, 448; PX = 220; PY1, PY2 = 572, 1036; KQ = 0.64"),
("CY = idle('cyrus', 3); JO = idle('joy', 3)","CY = idle('cyrus', 2); JO = idle('joy', 2)"),
("SL = seq(PL + 'race/slime_idle_c', 3, 1)","SL = seq(PL + 'race/slime_idle_c', 2, 1)"),
("p.alpha_composite(g, (488 - g.width // 2, 438 - g.height + bob))","p.alpha_composite(g, (int(488 * KQ) - g.width // 2, int(438 * KQ) - g.height + bob))"),
("p.alpha_composite(G_G, (500 - G_G.width // 2, 560 - G_G.height // 2 + int(2 * math.sin(t * 3))))","p.alpha_composite(G_G, (int(500 * KQ) - G_G.width // 2, int(560 * KQ) - G_G.height // 2 + int(2 * math.sin(t * 3))))"),
("p.alpha_composite(cy, (190 - cy.width // 2, 640 - 78 * 3))","p.alpha_composite(cy, (int(190 * KQ) - cy.width // 2, int(640 * KQ) - 78 * 2))"),
("p.alpha_composite(jo, (330 - jo.width // 2, 655 - 78 * 3))","p.alpha_composite(jo, (int(330 * KQ) - jo.width // 2, int(655 * KQ) - 78 * 2))"),
("p.alpha_composite(s, (790 - s.width // 2, 660 - s.height + 20))","p.alpha_composite(s, (int(790 * KQ) - s.width // 2, int(660 * KQ) - s.height + 13))"),
("    d.rectangle([0, 0, W, 250], fill=(20, 10, 4, 170))\n",""),
("d.rounded_rectangle([90, 1760, 990, 1800], 14,","d.rounded_rectangle([90, HB + 14, 900, HB + 50], 14,"),
("d.rounded_rectangle([96, 1766, 96 + int(888 * rem), 1794], 10,","d.rounded_rectangle([96, HB + 20, 96 + int(798 * rem), HB + 44], 10,"),
("items = [(W / 2, 60, 'FIND 3 DIFFERENCES', 56, (255, 214, 60), 7, 255), (W / 2, 150, 'in the Sun Temple', 34, (255, 255, 255), 6, 255)]","items = []"),
("items.append((W / 2, 1830, f'{int(math.ceil(TL - t))}', 50, (255, 255, 255), 6, 255))","items.append((960, HB + 8, f'{int(math.ceil(TL - t))}', 48, (255, 255, 255), 6, 255))"),
("rounded_rectangle([110, 800, 970, 1170], 30,","rounded_rectangle([110, 860, 970, 1100], 30,"),
("items += [(W / 2, 850, \"TIME'S UP!\", 64, (255, 214, 60), 8, a), (W / 2, 970, 'How many did you spot?', 34, (255, 255, 255), 5, a), (W / 2, 1050, 'Comment 0, 1, 2 or 3'","items += [(W / 2, 890, \"TIME'S UP!\", 64, (255, 214, 60), 8, a), (W / 2, 985, 'How many did you spot?', 34, (255, 255, 255), 5, a), (W / 2, 1040, 'Comment 0, 1, 2 or 3'"),
("    wr.write(img)\n    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p41_{f:04d}.png')","    img.alpha_composite(HOOK)\n    wr.write(img)\n    if f in (30, 150, 300): img.convert('RGB').save(f'prev/d41_{f:04d}.png')")]
for a,b in R:
    assert s.count(a)==1, a
    s=s.replace(a,b)
open('r41_sz.py','w').write(s); print('ok')
