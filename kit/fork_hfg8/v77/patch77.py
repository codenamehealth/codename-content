p = 'r77.py'; s = open(p).read()
def R(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
R("sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer",
  "sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2\nSTILL = os.environ.get('STILL')")
R("SS = 2; FOOT = 78 * SS", "SS = 3; FOOT = 78 * SS     # rc8: guides 2x -> 3x (~190px; were ~90-128px)")
R("HOOK, HB = hook_layer(['MUSICAL', 'CHAIRS'], accent=1, sub='SLAPPING IS ALLOWED')",
  "HOOK, HB = hook_layer2(['MUSICAL', 'CHAIRS'], accent=1, sub='SLAPPING IS ALLOWED'); print('HB', HB)   # rc8: sub 36px -> real >=44px band line")
R("TPLAY = [3.0, 2.5, 2.1];", "TPLAY = [3.2, 2.5, 2.1];   # rc8: march starts on frame 0 (was 1.6s), first STOP at 3.2s (was 4.6s)\n")
R("rounds = []; t = 1.6;", "rounds = []; t = 0.0;")
R("T_WIN = rounds[-1]['ts'] + 2.3; DUR = T_WIN + 3.6; N = int(DUR * FPS)",
  "T_WIN = rounds[-1]['ts'] + 1.75; DUR = T_WIN + 1.8; N = int(round(DUR * FPS))   # rc8: straight from the last OUT to the win (was +2.3s), win card held ~1.5s then loops (was 3.6s)")
R("BENCH = {'cleo': (130, HB + 312), 'joy': (240, HB + 312), 'ray': (826, HB + 312)}   # out guides wait in the top band",
  "BENCH = {'cleo': (150, 945), 'joy': (806, 945), 'ray': (318, 940)}   # out guides wait in the top band (3x)")
R("kx, ky = min(850, max(110, kx)), min(1495, ky)", "kx, ky = min(806, max(150, kx)), min(1495, ky)")
R("            img.alpha_composite(GOLD, (int(x - GOLD.width / 2), int(y - FOOT - GOLD.height + 10 + 5 * math.sin(t * 8))))",
  "            img.alpha_composite(GOLD, (int(x - GOLD.width / 2), int(y - FOOT + 30 - GOLD.height + 10 + 5 * math.sin(t * 8))))")
old = s[s.index("    if cur: status = "):s.index("    if t >= T_WIN:")]
new = '''    if cur: status = (f'ROUND {cur[0] + 1} - {NR - cur[0]} CHAIR' + ('S' if cur[0] < LAST else ''), 44, (235, 235, 235))
    stamp = None; slap = None; flash = 0
    if t < 2.6:   # rc8: PICK A PLAYER over the moving guides from frame 0, with name tags on each guide (VETTING)
        a = 255 if t < 2.3 else int(255 * (2.6 - t) / 0.3)
        tl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(tl)
        for n in NAMES:
            x, y, _, _ = sts[n]; tw_ = td.textlength(LABEL[n], font=F(44)); tx = min(1015 - tw_ / 2 - 12, max(80 + tw_ / 2 + 12, x)); ty = max(ST_Y1 + 8, y - FOOT + 30 - 64)
            td.rounded_rectangle([tx - tw_ / 2 - 12, ty, tx + tw_ / 2 + 12, ty + 60], 12, fill=(14, 10, 24, int(a * 0.9)), outline=RING[n] + (a,), width=4)
            ctext(td, tx, ty + 8, LABEL[n], F(44), RING[n], 6, a)
        img.alpha_composite(tl)
        layer(img, lambda d: d.rounded_rectangle([CX - 330, CY - 70, CX + 330, CY + 30], 16, fill=(14, 10, 24, int(a * 0.85))))
        items.append((CX, CY - 52, 'PICK A PLAYER!', 54, (255, 255, 255), 8, a))
    for ri, R in enumerate(rounds):
        u = t - R['ts']
        if 0 <= u < 0.6: status = ('STOP!', 48, (255, 80, 80)); stamp = ('STOP!', 110, (255, 70, 70), u)
        if 0.6 <= u < 1.1:
            lx, ly, _, _ = state(R['loser'], R['ts'] + 0.62); slap = (min(811 - 150, max(80 + 150, lx)), max(ST_Y1 + 10, ly - FOOT + 30 - 110), u - 0.6)
            if u < 0.6 + 2.5 / FPS: flash = 1
        if 1.1 <= u < 2.3: status = (LABEL[R['loser']] + ' IS OUT!', 44, (255, 255, 255))
        if 1.1 <= u < 1.75: stamp = (LABEL[R['loser']] + ' IS OUT!', 56 if len(LABEL[R['loser']]) > 5 else 64, (255, 255, 255), u - 1.1)
    if flash:      # rc8: white hit flash + shake on each SLAP
        img = img.transform(img.size, Image.AFFINE, (1, 0, 10, 0, 1, -8), resample=Image.NEAREST)
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 255, 255, 120)))
    if stamp:      # rc8: big centred stamp on the carpet (was status-bar text only)
        txt, sz, col, su = stamp; sc = 1.25 - 0.25 * min(1, su / 0.12); sz2 = int(sz * sc)
        tw_ = ImageDraw.Draw(Image.new('L', (1, 1))).textlength(txt, font=F(sz2))
        layer(img, lambda d: d.rounded_rectangle([547 - tw_ / 2 - 30, 990 - sz2 / 2 - 26, 547 + tw_ / 2 + 30, 990 + sz2 / 2 + 26], 18, fill=(14, 10, 24, 235), outline=col + (255,), width=6))
        items.append((547, 990 - sz2 / 2, txt, sz2, col, 10, 255))
    if slap:       # rc8: SLAP! 50 -> 84px on its own dark plate above the hit
        sx_, sy_, su = slap; sz2 = int(84 * (1.3 - 0.3 * min(1, su / 0.1)))
        tw_ = ImageDraw.Draw(Image.new('L', (1, 1))).textlength('SLAP!', font=F(sz2))
        layer(img, lambda d: d.rounded_rectangle([sx_ - tw_ / 2 - 20, sy_ - 16, sx_ + tw_ / 2 + 20, sy_ + sz2 + 16], 14, fill=(14, 10, 24, 225), outline=(255, 214, 60, 255), width=5))
        items.append((sx_, sy_, 'SLAP!', sz2, (255, 214, 60), 9, 255))
'''
s = s.replace(old, new)
R("        items.append((CX, 1416, 'Did you pick right?', 36, (255, 255, 255), 5, a))",
  "        items.append((CX, 1404, 'Did you pick right?', 46, (255, 255, 255), 7, a))   # rc8: 36 -> 46px")
R("    img.alpha_composite(HOOK)\n    w.write(img)",
  "    img.alpha_composite(HOOK)\n    if STILL and f in [int(x) for x in STILL.split(',')]: img.convert('RGB').save(f'k77_{f}.png')\n    w.write(img)")
open(p, 'w').write(s); print('ok')
