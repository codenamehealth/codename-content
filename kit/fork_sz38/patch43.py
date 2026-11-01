s=open('../fork_a4/r43.py').read()
R=[("from common import *","from common import *\nimport os; os.chdir(os.path.dirname(os.path.abspath(__file__)))\nsys.path.insert(0, '../pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['FINALLY MADE IT', 'TO A SAVE POINT'], accent=1)\nSHIFT = 340"),
("SIT = seq('hollow_sit', K)","SIT = seq('../fork_a4/hollow_sit', K)"),
("RCAST = seq(PL + '../fork3/ray_cast', K, 1)","RCAST = seq('../fork3/ray_cast', K, 1)"),
("GROUND = 1520; XH = 300; XR = 790; XC = 545","GROUND = 1180; XH = 300; XR = 790; XC = 545\ndef shifted(fr):\n    o = Image.new('RGBA', (W, H)); o.alpha_composite(fr, (0, -SHIFT)); o.alpha_composite(fr.crop((0, H - SHIFT, W, H)), (0, H - SHIFT)); return o\nBG = [shifted(b) for b in BG]"),
("x0, y0, x1, y1 = 60, 1600, W - 60, 1860","x0, y0, x1, y1 = 76, 1258, 880, 1488"),
("    for ln in text[:n].split('\\n'): d.text((x0 + 40, y), ln, font=F(44), fill=(255, 255, 255)); y += 70","    for ln in text[:n].split('\\n'): d.text((x0 + 36, y), ln, font=F(38), fill=(255, 255, 255)); y += 64"),
("bob = 10 * math.sin(t * 2.6); cy = 1330 + bob","bob = 10 * math.sin(t * 2.6); cy = GROUND - 190 + bob"),
("items = [(W / 2, 110, 'Finally made it', 50, (255, 255, 255), 7, 255), (W / 2, 180, 'to a save point', 50, (255, 255, 255), 7, 255)]","items = []"),
("items.append((W / 2, 1040, 'GAME SAVED'","items.append((W / 2, HB + 40, 'GAME SAVED'"),
("    wr.write(img)\n    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p43_{f:04d}.png')","    img.alpha_composite(HOOK)\n    wr.write(img)\n    if f in (30, 55, 100, 150, 175, 215): img.convert('RGB').save(f'prev/d43_{f:04d}.png')")]
for a,b in R:
    assert s.count(a)==1, a
    s=s.replace(a,b)
open('r43_sz.py','w').write(s); print('ok')
