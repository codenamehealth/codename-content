p='r_pick.py'; s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, (s.count(a), a); s=s.replace(a,b)
R("os.chdir(os.path.dirname(os.path.abspath(__file__)))",
  "OUTD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'v105' if sys.argv[1] == 'cyrus' else 'v106')\nos.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11/pick')\nsys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer")
R("hook=('Cyrus is picking mushrooms', 'for his gummy'), col=(217, 122, 31), floor=1730,",
  "hook=('Cyrus is picking mushrooms', 'for his gummy'), col=(217, 122, 31), floor=1730, hk=(['CYRUS PICKS', 'MUSHROOMS'], (255, 160, 40), 'FOR HIS GUMMY'),")
R("hook=('Joy is picking everything', 'for the ACV gummy'), col=(118, 200, 80), floor=1760,",
  "hook=('Joy is picking everything', 'for the ACV gummy'), col=(118, 200, 80), floor=1760, hk=(['JOY PICKS', 'EVERYTHING'], (130, 225, 90), 'FOR THE ACV GUMMY'),")
R("BG = up(Image.open(C['bg']).convert('RGBA'), 3)",
  """BG0 = up(Image.open(C['bg']).convert('RGBA'), 3)
FLOOR = 1495; DY = C['floor'] - FLOOR          # raise the scene so the guide's feet stay on the same ground, now inside the safe zone
BG = Image.new('RGBA', (W, H)); BG.paste(BG0.crop((0, DY, W, H)), (0, 0))
BG.paste(BG0.crop((0, H - DY, W, H)).transpose(Image.FLIP_TOP_BOTTOM), (0, H - DY))
HOOK, HB = hook_layer(C['hk'][0], accent=1, color=C['hk'][1], sub=C['hk'][2]); print('hook bottom', HB)""")
R("bot = crop(Image.open(C['bottle']).convert('RGBA')); BOT = bot.resize((int(bot.width * 560 / bot.height), 560), Image.LANCZOS)\nFLOOR = C['floor']",
  "bot = crop(Image.open(C['bottle']).convert('RGBA')); BOT = bot.resize((int(bot.width * 460 / bot.height), 460), Image.LANCZOS)\nCX = 478")
R("SPOTS = [700, 300, 840, 230, 600, 880, 380, 660]",
  "SPOTS = [700, 300, 840, 230, 600, 880, 380, 660]           # original spots: used only for timing (same beats, same audio)\nNEWX = lambda x: int(180 + (x - 230) * (580 / 650))          # drawn spots x180-760 so the guide and the item stay inside the zone\nSIDE = lambda x: 1 if NEWX(x) < 478 else -1                 # item on the open side, never under the guide\nIOFF = 118")
R("    x = SPOTS[k]; dist = abs(x - px); trun = min(0.55, dist / 1300)",
  "    x = SPOTS[k]; dist = abs(x - px); trun = min(0.55, dist / 1300)")
R("BAR_Y = 330; SLOT_X = [W / 2 + (k - 3.5) * 114 for k in range(8)]","BAR_Y = HB + 26; SLOT_X = [W / 2 + (k - 3.5) * 104 for k in range(8)]")
# char_state: map positions, pick faces the item
R("    if t < timeline[0][1]: return IDLE[int(t * 8) % len(IDLE)], x0","    if t < timeline[0][1]: return IDLE[int(t * 8) % len(IDLE)], NEWX(x0)")
R("        face_left = x < pxx\n        if tr <= t < tarr:\n            u = (t - tr) / max(1e-3, tarr - tr); cx = pxx + (x - pxx) * u",
  "        face_left = x < pxx; side_left = SIDE(x) < 0\n        if tr <= t < tarr:\n            u = (t - tr) / max(1e-3, tarr - tr); cx = NEWX(pxx) + (NEWX(x) - NEWX(pxx)) * u")
R("            u = (t - tarr) / 0.6; fr = (PICKL if face_left else PICK)[min(7, int(u * 8))]; return fr, x",
  "            u = (t - tarr) / 0.6; fr = (PICKL if side_left else PICK)[min(7, int(u * 8))]; return fr, NEWX(x)")
R("            return (IDLEL if face_left else IDLE)[int(t * 8) % len(IDLE)], x\n    return IDLE[int(t * 8) % len(IDLE)], timeline[-1][5]",
  "            return (IDLEL if side_left else IDLE)[int(t * 8) % len(IDLE)], NEWX(x)\n    return IDLE[int(t * 8) % len(IDLE)], NEWX(timeline[-1][5])")
R("f'{G}_noaudio.mp4'], stdin=subprocess.PIPE)","OUTD + '/noaudio.mp4'], stdin=subprocess.PIPE)\nKEEP = {int(v) for v in os.environ.get('KEEP', '').split(',') if v}")
R("motes = [(rnd.uniform(0, W), rnd.uniform(500, 1700), rnd.uniform(0, 6.3), rnd.uniform(0.3, 1.0)) for _ in range(28)]",
  "motes = [(rnd.uniform(0, W), rnd.uniform(500, 1700), rnd.uniform(0, 6.3), rnd.uniform(0.3, 1.0)) for _ in range(28)]\nmotes = [(m[0], m[1] - DY, m[2], m[3]) for m in motes]")
# items: drawn at the new x on the open side
R("        how = C['how'][k]; ic = ICON3[k]","        how = C['how'][k]; ic = ICON3[k]; xo = x; x = NEWX(xo); ix = x + SIDE(xo) * IOFF")
R("                gx, gy = x + 70, FLOOR - im.height","                gx, gy = ix, FLOOR - im.height")
R("                yy = (FLOOR - 1000) + 1000 * min(1, u * u) ; bounce = 0 if u >= 1 else 0\n                im = ic; gx, gy = x + 70, int(yy - ic.height)",
  "                yy = (FLOOR - 760) + 760 * min(1, u * u)\n                im = ic; gx, gy = ix, int(yy - ic.height)")
R("yy = FLOOR - 520 + 520 * (1 - (1 - u) ** 2); im = ic; gx, gy = x + 70, int(yy - ic.height)","yy = FLOOR - 520 + 520 * (1 - (1 - u) ** 2); im = ic; gx, gy = ix, int(yy - ic.height)")
R("layer(img, lambda dd, a=a, rr=rr: dd.rectangle([x + 70 + rr * math.cos(a) - 4, FLOOR - 40 + rr * math.sin(a) * 0.5 - 4, x + 70 + rr * math.cos(a) + 4, FLOOR - 40 + rr * math.sin(a) * 0.5 + 4], fill=(255, 245, 190, int(220 * (1 - u)))))",
  "layer(img, lambda dd, a=a, rr=rr: dd.rectangle([ix + rr * math.cos(a) - 4, FLOOR - 40 + rr * math.sin(a) * 0.5 - 4, ix + rr * math.cos(a) + 4, FLOOR - 40 + rr * math.sin(a) * 0.5 + 4], fill=(255, 245, 190, int(220 * (1 - u)))))")
R("img.alpha_composite(ic, (int(cx - ic.width / 2 + (20 if C['items'] else 0)), int(FLOOR - FOOT + 30 - ic.height)))",
  "img.alpha_composite(ic, (int(cx - ic.width / 2 + 20 * SIDE(xo)), int(FLOOR - FOOT + 30 - ic.height)))")
R("        layer(img, lambda dd: dd.ellipse([cx - 60, FLOOR - 14, cx + 60, FLOOR + 10], fill=(0, 0, 0, 70)))\n        img.alpha_composite(sp, (int(cx - sp.width / 2), int(FLOOR - FOOT)))",
  "        layer(img, lambda dd: dd.ellipse([cx - 60, FLOOR - 14, cx + 60, FLOOR + 10], fill=(0, 0, 0, 70)))\n        img.alpha_composite(sp, (int(cx - sp.width / 2), int(FLOOR - FOOT)))     # guide drawn after every prop: never covered")
R("ctext(d, x, FLOOR - FOOT - 110 - u * 60, '+1', F(44), C['col'], 6, a)","ctext(d, NEWX(x), FLOOR - FOOT - 110 - u * 60, '+1', F(44), C['col'], 6, a)")
R("    layer(img, lambda dd: [dd.rectangle([0, y, W, y + 8], fill=(14, 10, 24, int(170 * (1 - y / 470) ** 1.2))) for y in range(0, 470, 8)])\n    d = ImageDraw.Draw(img)\n    ctext(d, W / 2, 80, C['hook'][0], F(38), (255, 255, 255), 7); ctext(d, W / 2, 150, C['hook'][1], F(40), (255, 214, 60), 7)\n    d.rounded_rectangle([W / 2 - 480, BAR_Y - 14, W / 2 + 480, BAR_Y + 114], 40, fill=(26, 20, 34), outline=(26, 20, 34))\n    d.rounded_rectangle([W / 2 - 470, BAR_Y - 4, W / 2 + 470, BAR_Y + 104], 34, fill=(247, 240, 222))",
  "    d = ImageDraw.Draw(img)\n    d.rounded_rectangle([W / 2 - 430, BAR_Y - 14, W / 2 + 430, BAR_Y + 114], 40, fill=(26, 20, 34), outline=(26, 20, 34))\n    d.rounded_rectangle([W / 2 - 420, BAR_Y - 4, W / 2 + 420, BAR_Y + 104], 34, fill=(247, 240, 222))")
R("    cxg, cyg = W / 2, 980","    cxg, cyg = CX, 1000")
R("d = ImageDraw.Draw(img); ctext(d, W / 2, cyg + 200, C['banner'], F(46), C['col'], 7)","d = ImageDraw.Draw(img); ctext(d, CX, cyg + 200, C['banner'], F(46), C['col'], 7)")
R("        layer(img, lambda dd: [dd.ellipse([W / 2 - r, 900 - r, W / 2 + r, 900 + r], fill=(255, 240, 190, a)) for r, a in ((380, 35), (300, 45), (220, 55))])",
  "        layer(img, lambda dd: [dd.ellipse([CX - r, 870 - r, CX + r, 870 + r], fill=(255, 240, 190, a)) for r, a in ((380, 35), (300, 45), (220, 55))])")
R("layer(img, lambda dd, a=a, rr=rr: dd.rectangle([W / 2 + rr * math.cos(a) - 6, 900 + rr * math.sin(a) - 6, W / 2 + rr * math.cos(a) + 6, 900 + rr * math.sin(a) + 6], fill=(255, 220, 90, 230)))",
  "layer(img, lambda dd, a=a, rr=rr: dd.rectangle([CX + rr * math.cos(a) - 6, 870 + rr * math.sin(a) - 6, CX + rr * math.cos(a) + 6, 870 + rr * math.sin(a) + 6], fill=(255, 220, 90, 230)))")
R("a = q * 0.628 + t * 1.2; rr = 330 + 20 * math.sin(t * 3 + q)","a = q * 0.628 + t * 1.2; rr = 290 + 20 * math.sin(t * 3 + q)")
R("b = BOT; yy = int(900 - b.height / 2 + (1 - e) * 500 + math.sin(t * 2.5) * 8)","b = BOT; yy = int(870 - b.height / 2 + (1 - e) * 500 + math.sin(t * 2.5) * 8)")
R("img.alpha_composite(bb, (int(W / 2 - b.width / 2), yy))","img.alpha_composite(bb, (int(CX - b.width / 2), yy))")
R("layer(img, lambda dd: dd.ellipse([W / 2 - 80, FLOOR - 14, W / 2 + 80, FLOOR + 10], fill=(0, 0, 0, 70)))\n        img.alpha_composite(vf, (int(W / 2 - vf.width / 2), int(FLOOR - vf.height)))",
  "layer(img, lambda dd: dd.ellipse([CX - 80, FLOOR - 14, CX + 80, FLOOR + 10], fill=(0, 0, 0, 70)))\n        img.alpha_composite(vf, (int(CX - vf.width / 2), int(FLOOR - vf.height)))")
R("d = ImageDraw.Draw(img); ctext(d, W / 2, 1222, 'CRAFTED!', F(60), (255, 214, 60), 8)","d = ImageDraw.Draw(img); ctext(d, CX, 1098, 'CRAFTED!', F(60), (255, 214, 60), 8)")
R("    ff.stdin.write(img.convert('RGB').tobytes())\n    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev_{G}_{f:04d}.png')",
  "    img.alpha_composite(HOOK)\n    ff.stdin.write(img.convert('RGB').tobytes())\n    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')")
R("json.dump({'events': events}, open(f'{G}_events.json', 'w'))","json.dump({'events': events}, open(OUTD + '/ev.json', 'w'))")
open(p,'w').write(s); print('ok')
