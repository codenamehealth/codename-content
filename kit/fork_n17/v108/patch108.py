p='r108b.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("""T_SKIP, T_SKIP1 = 2.1, 2.95                     # n17: '3 HOURS LATER...' card
LINES = [(0.0, ['Welcome! Anything', 'catch your eye?']), (T_SKIP1 + 0.1, ['...You\\'re not', 'buying anything,', 'are you?'])]
PRE = [8, 0]
CPS = 26; T_POUCH = 4.85; T_CY = 6.25; T_GIVE = 7.15; GFPS = 14; G0, G1 = 11, 54; END = 11.0""",
"""T_SKIP, T_SKIP1 = 1.9, 2.7                      # n17: '3 HOURS LATER...' card
LINES = [(0.0, ['Welcome!']), (T_SKIP1 + 0.05, ['Not buying?'])]   # n18: one short line per bubble, 64px (was 3 lines at 40px)
PRE = [0, 0]
CPS = 13; T_POUCH = 2.95; T_FLIP = T_POUCH + 0.55; T_CY = 4.75; T_GIVE = 5.6; GFPS = 16; G0, G1 = 11, 59
T_ZIP = T_GIVE + (G1 - G0 + 1) / GFPS; ZIPD = 0.34; END = T_ZIP + ZIPD + 0.3   # n18: he zips off left with SPEED after eating""")
R("""HPOUCH = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(S + 'fork_b11/gen/hollow_pouch/*.png'))[1:9]]""",
"""_PS = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(S + 'fork_b11/gen/hollow_pouch/*.png'))]
HPOUCH = [up(p, K) for p in _PS[1:9]]
def _flip_pouch(im, dx=0):
    im = im.copy(); box = (57, 48, 67, 62); pc = im.crop(box); a = np.array(im); a[48:62, 57:67] = 0; im = Image.fromarray(a)
    im.alpha_composite(pc.transpose(Image.FLIP_TOP_BOTTOM), (57 + dx, 48)); return im
HPOUCHUP = [up(_flip_pouch(_PS[8], dx), K) for dx in (0, 1, 0, -1)]   # shaken upside down (only the pouch pixels flip)""")
R("""def hollow(t):
    if t < 0.95: u = t / 0.95; return HWALK[int(t * 10) % len(HWALK)], -120 + 760 * u
    if t < T_POUCH: return HSTAND, 640
    if t < T_POUCH + 0.75: u = (t - T_POUCH) / 0.75; return HPOUCH[min(7, int(u * 8))], 640
    return HSTAND, 640""",
"""def hollow(t):
    if t < 0.95: u = t / 0.95; return HWALK[int(t * 10) % len(HWALK)], -120 + 760 * u
    if t < T_POUCH: return HSTAND, 640
    if t < T_FLIP: u = (t - T_POUCH) / (T_FLIP - T_POUCH); return HPOUCH[min(7, int(u * 8))], 640
    if t < T_FLIP + 0.75: return HPOUCHUP[int((t - T_FLIP) * 16) % 4], 640
    return HPOUCH[7], 640""")
i=s.index("    # 3 gummies reveal: all he has, vs the 999 tag"); j=s.index("    # sweat drop on the last line")
s=s[:i]+"""    # n18: pouch upside down, shaken: nothing falls out but a few specks of dust
    if T_FLIP + 0.1 <= t < T_FLIP + 1.0:
        u = t - T_FLIP - 0.1; d = ImageDraw.Draw(img); ox, oy = 640 + (62 - 46) * K, HFEET - FOOT + 62 * K
        for q in range(5):
            uq = u - q * 0.12
            if 0 <= uq < 0.55:
                dy = 260 * uq * uq + 40 * uq; dxq = (q - 2) * 9 + 10 * math.sin(uq * 9 + q); r_ = 5 if q % 2 else 4
                d.rectangle([ox + dxq - r_, oy + dy - r_, ox + dxq + r_, oy + dy + r_], fill=(180, 170, 160))
        if 0 <= u < 1 / FPS: ev(t, 'swish')
"""+s[j:]
R("    if T_POUCH + 0.85 <= t < T_GIVE:\n        d = ImageDraw.Draw(img); u = (t - T_POUCH - 0.85)","    if T_FLIP + 0.55 <= t < T_GIVE:\n        d = ImageDraw.Draw(img); u = (t - T_FLIP - 0.55)")
R("""def gidx(t):
    k = int((t - T_GIVE) * GFPS) + G0
    if k > G1: k = 45 + (k - 45) % (G1 - 45 + 1)   # keep the arms-up celebration looping
    return k""","""def gidx(t):
    k = min(G1, int((t - T_GIVE) * GFPS) + G0)
    return 39 if k == 40 else k                    # n18: frame 40 (gummy at the lips) read as a tongue""")
R("""    else:
        k = gidx(t); gf = GIVE[k]; img.alpha_composite(gf, (int(640 - GHX * 1), int(HFEET - GFY)))
        if k == 30: ev(t, 'swish')
        if k == 38: ev(t, 'crunch_8bit')
        if k == 45 and int((t - T_GIVE) * GFPS) + G0 == 45: ev(t, 'powerup_8bit')
        if int((t - T_GIVE) * GFPS) + G0 == 47: ev(t, 'cheer')""",
"""    elif t < T_ZIP:
        k = gidx(t); gf = GIVE[k]; img.alpha_composite(gf, (int(640 - GHX * 1), int(HFEET - GFY)))
        kr = int((t - T_GIVE) * GFPS) + G0
        if kr == 30: ev(t, 'swish')
        if kr == 39: ev(t, 'crunch_8bit')
        if kr == 48: ev(t, 'powerup_8bit')
        if kr == 50: ev(t, 'cheer')
        if 39 <= kr <= 42:                            # chomp puff over his mouth (no teeth), hands come down empty
            u = (t - (T_GIVE + (39 - G0) / GFPS)) / (4 / GFPS); al = int(255 * max(0, min(1, (1 - u) / 0.35)))
            pcx, pcy = 623, HFEET - 194; rr = 26 + 30 * u
            layer(img, lambda dd: [dd.ellipse([pcx + ox_ * (1 + u) - rr * sz, pcy + oy_ * (1 + u) - rr * sz, pcx + ox_ * (1 + u) + rr * sz, pcy + oy_ * (1 + u) + rr * sz], fill=(255, 255, 255, al), outline=(20, 15, 35, al), width=5)
                                   for (ox_, oy_, sz) in ((-26, 6, 0.7), (24, 4, 0.75), (0, -12, 0.85), (0, 14, 0.6))])
    else:                                             # n18: SPEED zip off to the left (Syeda's side walk, fast), Cyrus stays
        cyr = GIVE[G1].crop((0, 0, GHX - 90, GIVE[G1].height)); img.alpha_composite(cyr, (int(640 - GHX), int(HFEET - GFY)))
        u = (t - T_ZIP) / ZIPD; zx = 640 - 820 * min(1, u) ** 1.6
        if u < 1:
            hw = HWALKL[int(t * 30) % len(HWALKL)]
            for q, ga in ((2, 60), (1, 110)):
                gh = hw.copy(); gh.putalpha(Image.fromarray((np.array(gh.getchannel('A')) * ga / 255).astype(np.uint8)))
                img.alpha_composite(gh, (int(zx + q * 70 - hw.width / 2), int(HFEET - FOOT)))
            img.alpha_composite(hw, (int(zx - hw.width / 2), int(HFEET - FOOT)))
        L_ = max(0.0, 1 - max(0, u - 1) / 0.35)
        layer(img, lambda dd: [dd.rectangle([zx + 60 + q * 30, HFEET - 330 + q * 52, min(W - 60, zx + 60 + q * 30 + 340 * L_), HFEET - 322 + q * 52], fill=(255, 190, 90, int(230 * L_))) for q in range(6)]
              + [dd.ellipse([zx + 60 + q * 50 - 16 - q * 4, HFEET - 30 - q * 6 - (u * 60 % 20), zx + 60 + q * 50 + 16 + q * 4, HFEET - q * 6 - (u * 60 % 20)], fill=(210, 190, 160, int(170 * L_ * (1 - q / 6)))) for q in range(5)])
        if 0 <= t - T_ZIP < 1 / FPS: ev(t, 'whoosh_8bit')""")
R("""        bx0, by0, bx1, by1 = 76, HB + 14, 1004, HB + 254""","""        bx0, by0, bx1, by1 = 76, HB + 14, 1004, HB + 230""")
R("""            d.text((bx0 + 170, by0 + 36 + j * 60), ln[:max(0, n - k0)], font=F(40), fill=(255, 255, 255)); k0 += len(ln)""",
"""            d.text((bx0 + 168, by0 + 76 + j * 80), ln[:max(0, n - k0)], font=F(64), fill=(255, 255, 255), stroke_width=4, stroke_fill=(10, 6, 18)); k0 += len(ln)""")
open(p,'w').write(s); print('ok')
