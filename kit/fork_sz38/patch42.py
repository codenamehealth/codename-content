s=open('../fork_a4/r42.py').read()
R=[("from common import *","from common import *\nimport os; os.chdir(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['PAUSE WHEN BOTH', 'FIT PERFECTLY'], accent=1)"),
("P0 = (320, 960); G0 = (770, 960)","P0 = (312, 770); G0 = (762, 770)"),
("JOY = idle('joy', 3)","JOY = idle('joy', 4)"),
("img.alpha_composite(jo, (W - 150 - jo.width // 2, 1880 - 78 * 3))","img.alpha_composite(jo, (160 - jo.width // 2, 1492 - 78 * 4))"),
("    d.rectangle([0, 0, W, 290], fill=(16, 10, 30, 175)); img.alpha_composite(L)\n",""),
("items = [(W / 2, 80, 'PAUSE WHEN BOTH', 56, (255, 255, 255), 7, 255), (W / 2, 165, 'FIT PERFECTLY', 56, (255, 214, 60), 7, 255)]","items = []"),
("items.append((W / 2, 1290, name,","items.append((W / 2 + 40, 1120, name,"),
("items.append((W / 2, 1410, f'LEVEL {i + 1} OF 4'","items.append((W / 2 + 40, 1240, f'LEVEL {i + 1} OF 4'"),
("rounded_rectangle([100, 1480, 980, 1650], 26,","rounded_rectangle([262, 1300, 880, 1470], 26,"),
("items += [(W / 2, 1510, 'Which level did', 38, (255, 255, 255), 5, a), (W / 2, 1575, 'you beat?'","items += [(571, 1330, 'Which level did', 36, (255, 255, 255), 5, a), (571, 1395, 'you beat?'"),
("    wr.write(img)\n    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p42_{f:04d}.png')","    img.alpha_composite(HOOK)\n    wr.write(img)\n    if f in (53, 188, 300, 431, 500): img.convert('RGB').save(f'prev/d42_{f:04d}.png')")]
for a,b in R:
    assert s.count(a)==1, a
    s=s.replace(a,b)
open('r42_sz.py','w').write(s); print('ok')
