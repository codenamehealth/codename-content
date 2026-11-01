p='r89.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n,(a,s.count(a)); s=s.replace(a,b)
R("HOOK, HB = hook_layer(['LAST ONE IN', 'THE RING WINS'], accent=1, sub='SHOVING ALLOWED')",
"""def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
HOOK, HB = band(['LAST ONE IN', 'THE RING WINS'], 1, 'COMMENT YOUR PICK', subcol=(255, 255, 255))   # rc10: 46px comment line; SHOVING ALLOWED moves to the opening plate""")
R("CH0 = HB + 12; CH1 = CH0 + 104", "CH0 = HB + 10; CH1 = CH0 + 96")
R("SS = 2; FOOT = 78 * SS", "SS = 3; FOOT = 78 * SS   # rc10: guides 2x -> 3x")
R("SRUN = {g: seq(PL + f'race/{g}_run', 2, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq(PL + 'maze/anim/hollow_srun', 2, 1, 9)",
  "SRUN = {g: seq(PL + f'race/{g}_run', SS, 1, 9) for g in ['joy', 'cyrus', 'cleo', 'ray']}")
R("FRUN = {g: seq(PL + f'maze/anim/{g}_frun', 2, 1, 9) for g in NAMES}\nSTAND = {g: seq(PL + f'maze/anim/{g}_frun', 2, 0, 1)[0] for g in NAMES}\nPANIC = {g: seq(PL + f'maze/anim/{g}_panic', 2, 1, 9) for g in NAMES}",
  "FRUN = {g: seq(PL + f'maze/anim/{g}_frun', SS, 1, 9) for g in NAMES}\nSTAND = {g: seq(PL + f'maze/anim/{g}_frun', SS, 0, 1)[0] for g in NAMES}\nPANIC = {g: seq(PL + f'maze/anim/{g}_panic', SS, 1, 9) for g in NAMES}")
R("ICON = {n: face(n, 30) for n in NAMES}; HEAD = {n: face(n, 34) for n in NAMES}", "ICON = {n: face(n, 32) for n in NAMES}; HEAD = {n: face(n, 42) for n in NAMES}")
R("GUM = {k: gummy(k, 2) for k in ['mush', 'cre', 'acv', 'mel', 'gold']}", "GUM = {k: gummy(k, 3) for k in ['mush', 'cre']}   # rc10: gummies 2x -> 3x")
R("T_WIN = OUTS[-1][1]; END = T_WIN + 3.4",
"""T_LAST = OUTS[-1][1]; T_WIN = T_LAST + 0.7; END = T_WIN + 1.5   # rc10: final OUT shown at full brightness 0.7s, win held 1.5s, then loop
# rc10: one stamp slot under the IN/OUT panel; OUT stamps and power stamps queued so they never overlap
STAMPS = []
for e in sorted([e for e in EV if e[1] in ('gum', 'splash')], key=lambda e: e[0]):
    if e[1] == 'gum': txt, col, dur = ('SPEED!' if e[3] == 'mush' else 'STRONG!'), ((255, 200, 60) if e[3] == 'mush' else (255, 110, 50)), 0.9
    else: txt, col, dur = LABEL[e[2]] + ' IS OUT!', (255, 90, 80), 1.2
    t1 = max(e[0], STAMPS[-1][1] + 0.05) if STAMPS else e[0]
    if e[1] == 'splash' and e[2] == OUTS[-1][0]: dur = T_WIN - t1
    STAMPS.append((t1, t1 + dur, txt, col))
print('stamps', [(round(a, 2), round(b, 2), c) for a, b, c, _ in STAMPS])
SY = CH1 + 8""")
R("BUSY = [int(e[0] * FPS) + 3 for e in EV if e[1] == 'gum'][:2] + [int(T_WIN * FPS) + 40]",
  "BUSY = [0, 20] + [int(e[0] * FPS) + 3 for e in EV if e[1] == 'gum'][:2] + [int(T_LAST * FPS) + 8, int(END * FPS) - 1]")
R("layer(img, lambda d: [d.ellipse([st[n]['x'] - 28, st[n]['y'] - 8, st[n]['x'] + 28, st[n]['y'] + 8], fill=(0, 0, 0, 80)) for n in NAMES if st[n]['out'] is None])",
  "layer(img, lambda d: [d.ellipse([st[n]['x'] - 40, st[n]['y'] - 11, st[n]['x'] + 40, st[n]['y'] + 11], fill=(0, 0, 0, 80)) for n in NAMES if st[n]['out'] is None])")
R("""                spr = PANIC[n][int(t * 14) % 8]; sink = int(u / 0.35 * 120)""", """                spr = PANIC[n][int(t * 14) % 8]; sink = int(u / 0.35 * 180)""")
R("                y = min(y, 1500 - 46); x = max(70 + 40, min((887 if y + 40 > 1110 else 1025) - 40, x))",
  "                y = min(y, 1500 - 50); x = max(70 + 50, min((887 if y + 50 > 1110 else 1025) - 50, x))")
R("""                sx_, sy_ = s['x'], min(s['y'], 1500 - 46); sx_ = max(110, min((887 if sy_ + 40 > 1110 else 1025) - 40, sx_))""",
  """                sx_, sy_ = s['x'], min(s['y'], 1500 - 50); sx_ = max(120, min((887 if sy_ + 50 > 1110 else 1025) - 50, sx_))""")
R("        if t < 2.2 or (WIN and t >= T_WIN): spr = STAND[n]", "        if WIN and t >= T_WIN: spr = STAND[n]")
R("""        if s['buff']:
            col = (255, 160, 40) if s['buff'] == 'mush' else (90, 150, 255)
            layer(img, lambda d, x=x, y=y, col=col: d.ellipse([x - 46, y - 18, x + 46, y + 18], outline=col + (220,), width=5))""",
"""        if s['buff']:
            col = (255, 210, 60) if s['buff'] == 'mush' else (255, 80, 40)
            layer(img, lambda d, x=x, y=y, col=col: d.ellipse([x - 62, y - 22, x + 62, y + 22], outline=col + (230,), width=6))""")
R("""                    for k, oy in enumerate((-110, -75, -40)):""", """                    for k, oy in enumerate((-160, -110, -60)):""")
R("""            if s['buff'] == 'cre':                       # STRONG!: pulsing blue power aura
                p_ = 0.5 + 0.5 * math.sin(t * 10)
                layer(img, lambda d, x=x, y=y, p_=p_: d.ellipse([x - 58, y - FOOT - 6, x + 58, y + 14], outline=(110, 170, 255, int(120 + 100 * p_)), width=6))""",
"""            if s['buff'] == 'cre':                       # STRONG!: rc10: red/orange power flames rising off the body (no oval: an oval read as the ACV shield)
                def flames(d, x=x, y=y):
                    r3 = random.Random(int(t * 15) + int(x))
                    for k in range(9):
                        fx = x + r3.uniform(-62, 62); fy = y - r3.uniform(20, FOOT - 20); L = r3.uniform(26, 54)
                        c = r3.choice([(255, 80, 40), (255, 140, 40), (255, 200, 80)])
                        d.polygon([(fx - 7, fy), (fx + 7, fy), (fx, fy - L)], fill=c + (215,))
                layer(img, flames)""")
R("""            if e[1] == 'shove':
                big = s['buff'] == 'cre'
                tx = 'POW!' if big else 'SHOVE!'; sz = 40 if big else 30
                items.append((clampx(s['x'], len(tx) * sz, yy), yy, tx, sz, (120, 180, 255) if big else (255, 220, 60), 6, a))
            elif e[1] == 'gum':
                tx = 'SPEED!' if e[3] == 'mush' else 'STRONG!'
                items.append((clampx(s['x'], len(tx) * 36, yy), yy, tx, 36, (255, 160, 40) if e[3] == 'mush' else (120, 170, 255), 7, a))
            elif e[1] == 'splash':
                yy = s['y'] - 80 - u * 40; items.append((clampx(s['x'], 7 * 32, yy), yy, 'SPLASH!', 32, (180, 230, 255), 6, a))""",
"""            if e[1] == 'shove' and s['buff'] == 'cre':     # rc10: only STRONG shoves get a pop: POW! 52px + orange impact burst (SHOVE! pops cut)
                v = FR[min(int(e[0] * FPS), len(FR) - 1)][0][e[3]]; ix, iy = (s['x'] + v['x']) / 2, (s['y'] + v['y']) / 2 - FOOT * 0.45
                if u < 0.35:
                    k_ = 1 - u / 0.35
                    def burst(d, ix=ix, iy=iy, k_=k_):
                        pts = []
                        for j in range(16):
                            rr_ = (95 if j % 2 == 0 else 42) * (0.6 + 0.6 * (1 - k_)); an = j * math.pi / 8
                            pts.append((ix + rr_ * math.cos(an), iy + rr_ * math.sin(an)))
                        d.polygon(pts, fill=(255, 150, 40, int(230 * k_)), outline=(255, 240, 160, int(255 * k_)))
                    layer(img, burst)
                items.append((clampx(s['x'], 4 * 52, yy), yy - 20, 'POW!', 52, (255, 120, 50), 8, a))""")
R("""        chips.append((sx + 10, CH0 + 40, 'OUT' if out else 'IN', 30, (255, 90, 80) if out else (140, 230, 120), 6, 255))
        if WIN and t >= T_WIN and n == WIN: layer(img, lambda d, sx=sx: d.ellipse([sx - 128, CH0 + 14, sx - 52, CH0 + 90], outline=(255, 214, 60, 255), width=6))""",
"""        chips.append((sx + 22, CH0 + 26, 'OUT' if out else 'IN', 44, (255, 90, 80) if out else (140, 230, 120), 7, 255))   # rc10: 30 -> 44px
        if WIN and t >= T_WIN and n == WIN: layer(img, lambda d, sx=sx: d.ellipse([sx - 130, CH0 + 12, sx - 50, CH0 + 92], outline=(255, 214, 60, 255), width=6))""")
R("""    if t < 2.6: text_layer(img, [(CX, CY - 40, 'PICK A PLAYER!', 54, (255, 255, 255), 8, 255)])
    for (n, to) in OUTS:
        u = t - to
        if 0 <= u < 1.6 and not (WIN and t >= T_WIN):
            text_layer(img, [(CX, CY + 210, LABEL[n] + ' IS OUT!', 44, (255, 110, 100), 7, int(255 * min(1, (1.6 - u) / 0.4)))])""",
"""    if t < 1.8:   # rc10: premise plate over the action (guides already shoving)
        layer(img, lambda d: d.rounded_rectangle([CX - 400, CY - 72, CX + 400, CY + 66], 20, fill=(14, 10, 24, 190), outline=(255, 214, 60, 255), width=5))
        text_layer(img, [(CX, CY - 52, 'PICK A PLAYER!', 56, (255, 255, 255), 8, 255), (CX, CY + 10, 'SHOVING ALLOWED', 44, (255, 214, 60), 7, 255)])
    for (t1, t2, txt, col) in STAMPS:
        if t1 <= t < t2 and t < T_WIN:
            sc = 1.0 + 0.25 * max(0, 0.12 - (t - t1)) / 0.12; fs_ = int((56 if 'OUT' in txt else 60) * sc)
            layer(img, lambda d: d.rounded_rectangle([78, SY, 1017, SY + 92], 18, fill=(14, 10, 24, 240), outline=col + (255,), width=6))
            text_layer(img, [(547, SY + 46 - fs_ // 2, txt, fs_, col, 9, 255)])""")
R("        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1150 - vf.height))",
  "        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (CX - vf.width // 2, 1170 - vf.height))")
R("        text_layer(img, [(CX, 1200, LABEL[WIN] + ' WINS!', 66, (255, 214, 60), 8, 255)])",
  "        layer(img, lambda d: d.rounded_rectangle([CX - 300, 1188, CX + 300, 1290], 20, fill=(14, 10, 24, 220), outline=(255, 214, 60, 255), width=6))\n        text_layer(img, [(CX, 1206, LABEL[WIN] + ' WINS!', int(66 * (1 + 0.3 * max(0, 0.12 - u) / 0.12)), (255, 214, 60), 9, 255)])")
R("""wr.close(); json.dump(out_ev, open('v89_ev.json', 'w')); print('done', round(END, 2))
mix('v89_noaudio.mp4', out_ev, 'magical_action.wav', 6, 'v89_mix.mp4')
print('LUFS', loudness('v89_mix.mp4'), '->', louder('v89_mix.mp4', 'v89_final.mp4'))""",
"""wr.close(); json.dump({'events': out_ev}, open('v89_ev.json', 'w')); print('done', round(END, 2))""")
open(p,'w').write(s); print('ok')
