p='r108.py'; s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, (s.count(a), a); s=s.replace(a,b)
R("os.chdir(os.path.dirname(os.path.abspath(__file__)))",
  "OUTD = os.path.dirname(os.path.abspath(__file__))\nos.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11/shop')\nsys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer\nHOOK, HB = hook_layer(['WINDOW SHOPPING,', 'RPG EDITION'], accent=1); print('hook bottom', HB)")
R("BG = up(Image.open(S + 'fork_b11/gen/bg_shop_1/00.png').convert('RGBA'), 3)\nCOUNTER_Y = 1336",
  """BG0 = up(Image.open(S + 'fork_b11/gen/bg_shop_1/00.png').convert('RGBA'), 3)
DY = 350                                        # whole shop raised 350px so the Hollow's feet land at y1500 (was 1850)
BG = Image.new('RGBA', (W, H)); BG.paste(BG0.crop((0, DY, W, H)), (0, 0)); BG.paste(BG0.crop((0, H - DY, W, H)).transpose(Image.FLIP_TOP_BOTTOM), (0, H - DY))
COUNTER_Y = 1336 - DY""")
R("JX = 300; JFEET = 1420\nHFEET = 1850","JX = 300; JFEET = 1420 - DY\nHFEET = 1850 - DY")
R("'-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'shop_noaudio.mp4'], stdin=subprocess.PIPE)",
  "'-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + '/noaudio.mp4'], stdin=subprocess.PIPE)\nKEEP = {int(v) for v in os.environ.get('KEEP', '').split(',') if v}\njars = Image.open(A + 'jars.png').convert('RGBA')\ndef jar(i):\n    c = jars.crop((i * 200, 0, i * 200 + 200, 200)); a = np.array(c); bg = a[0, 0, :3]\n    m = (np.abs(a[:, :, :3].astype(int) - bg.astype(int)).sum(2) < 12); a[m, 3] = 0\n    return crop(Image.fromarray(a).resize((50, 50), Image.NEAREST))\nJARS = [jar(i) for i in range(4)]\nTAGG = up(GUMS['mush'], 1)                     # price unit: gummies (no gold)")
# display: potions priced in gummies; legendary elixir 999
R("""    items = [('acv', '99G'), ('mush', '99G'), ('gold', '999G'), ('mel', '99G'), ('cre', '99G')]
    for i, (k, p) in enumerate(items):
        gx = 560 + i * 98; g = up(GUMS[k], 3 if k != 'gold' else 4); gy = COUNTER_Y - g.height + 6
        if k == 'gold':""",
"""    items = [(0, '99'), (2, '99'), (1, '999'), (3, '99'), (0, '99')]
    for i, (k, p) in enumerate(items):
        gx = 474 + i * 104; g = up(JARS[k], 2 if p != '999' else 3); gy = COUNTER_Y - g.height + 6
        if i == 4: g = up(JARS[3].transpose(Image.FLIP_LEFT_RIGHT), 2)
        if p == '999':""")
R("""        tw = d.textlength(p, font=F(18)); d.rectangle([gx - tw / 2 - 8, COUNTER_Y + 14, gx + tw / 2 + 8, COUNTER_Y + 46], fill=(240, 226, 190), outline=(60, 40, 20), width=3)
        d.text((gx - tw / 2, COUNTER_Y + 21), p, font=F(18), fill=(120, 40, 30))""",
"""        tw = d.textlength(p, font=F(20)) + 4 + TAGG.width; x0 = gx - tw / 2
        d.rectangle([x0 - 7, COUNTER_Y + 12, x0 + tw + 7, COUNTER_Y + 50], fill=(240, 226, 190), outline=(60, 40, 20), width=3)
        d.text((x0, COUNTER_Y + 21), p, font=F(20), fill=(120, 40, 30))
        img.alpha_composite(TAGG, (int(x0 + tw - TAGG.width), COUNTER_Y + 18)); d = ImageDraw.Draw(img)""")
# 3 gold -> 3 gummies
R("""        for q in range(3):
            cx, cy = hx - 50 + q * 50, HFEET - FOOT + 30 - min(1, u / 0.15) * 40
            d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(255, 210, 60), outline=(120, 70, 10), width=4)
            d.rectangle([cx - 4, cy - 10, cx + 4, cy + 10], fill=(255, 240, 150))
        ctext(d, hx, HFEET - FOOT - 60, '3 GOLD', F(44), (255, 214, 60), 6)""",
"""        for q, gk in enumerate(('mush', 'acv', 'mel')):
            gg = up(GUMS[gk], 2) if gk != 'mel' else up(GUMS[gk], 1).resize((48, 48), Image.NEAREST)
            cx, cy = hx - 60 + q * 60, HFEET - FOOT + 30 - min(1, u / 0.15) * 40
            img.alpha_composite(gg, (int(cx - gg.width / 2), int(cy - gg.height / 2)))
        d = ImageDraw.Draw(img)
        ctext(d, hx, HFEET - FOOT - 60, '3 GUMMIES', F(44), (255, 214, 60), 6)""")
R("""    layer(img, lambda dd: [dd.rectangle([0, y, W, y + 8], fill=(14, 10, 24, int(200 * (1 - y / 300)))) for y in range(0, 300, 8)])
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 70, 'Me in every shop', F(52), (255, 255, 255), 8); ctext(d, W / 2, 150, 'with 3 gold', F(52), (255, 214, 60), 8)
""","")
R("bx0, by0, bx1, by1 = 40, 300, W - 40, 540","bx0, by0, bx1, by1 = 76, HB + 14, 1004, HB + 254")
R("    ff.stdin.write(img.convert('RGB').tobytes())\nff.stdin.close()",
  "    img.alpha_composite(HOOK)\n    ff.stdin.write(img.convert('RGB').tobytes())\n    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')\nff.stdin.close()")
R("json.dump({'events': events}, open('shop_events.json', 'w'))","json.dump({'events': events}, open(OUTD + '/ev.json', 'w'))")
open(p,'w').write(s); print('ok')
