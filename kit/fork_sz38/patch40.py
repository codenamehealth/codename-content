s=open('../fork_a4/r40.py').read()
R=[("from common import *","from common import *\nimport os; os.chdir(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['NPCS BLOCKING', 'THE ONLY PATH'], accent=1)"),
("box=(1205, 300, 1611, 1020)","box=(1241, 476, 1575, 1071)"),
("seq('hollow_bonk', K)","seq('../fork_a4/hollow_bonk', K)"),
("seq('cleo_block', K)","seq('../fork_a4/cleo_block', K)"),
("GROUND = 1330","GROUND = 1040"),
("x0, y0, x1, y1 = 60, 1520, W - 60, 1790","x0, y0, x1, y1 = 76, 1170, 880, 1440"),
("items = [(W / 2, 250, 'NPCs blocking', 50, (255, 255, 255), 7, 255), (W / 2, 320, 'the only path', 50, (255, 255, 255), 7, 255)]","items = []"),
("GROUND - 360 - (t - T_HIT) * 80, 'BONK!'","GROUND - 330 - (t - T_HIT) * 80, 'BONK!'"),
("    wr.write(img)\n    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p40_{f:04d}.png')","    img.alpha_composite(HOOK)\n    wr.write(img)\n    if f in (20, 45, 70, 150): img.convert('RGB').save(f'prev/d40_{f:04d}.png')")]
for a,b in R:
    assert s.count(a)==1, a
    s=s.replace(a,b)
open('r40_sz.py','w').write(s); print('ok')
