p='r104b.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a[:80], s.count(a)); s=s.replace(a,b)
# art 2x -> 2.5x
R("DIG = {'joy': seq('joy_dig', 2, 1, 9), 'cyrus': seq('cyrus_dig2', 2, 1, 9), 'cleo': seq('cleo_dig', 2, 1, 9), 'ray': seq('ray_dig', 2, 1, 9), 'hollow': seq('hollow_dig', 2, 1, 9)}",
  "DIG = {'joy': seq('joy_dig', KS * 2, 1, 9), 'cyrus': seq('cyrus_dig2', KS * 2, 1, 9), 'cleo': seq('cleo_dig', KS * 2, 1, 9), 'ray': seq('ray_dig', KS * 2, 1, 9)}")
R("STAND = {n: seq(f'../pixellab/maze/anim/{n}_frun', 2, 0, 1)[0] for n in NAMES}\nFRUN = {n: seq(f'../pixellab/maze/anim/{n}_frun', 2, 1, 9) for n in NAMES}\nSRUN = {n: seq(f'../pixellab/race/{n}_run', 2, 1, 9) for n in ['joy', 'cyrus', 'cleo', 'ray']}; SRUN['hollow'] = seq('../pixellab/maze/anim/hollow_srun', 2, 1, 9)\nPANIC = {n: seq(f'../pixellab/maze/anim/{n}_panic', 2, 1, 9) for n in NAMES}\nBLK = crop(Image.open('block/07.png').convert('RGBA')).resize((64, 64), Image.NEAREST)",
  "STAND = {n: seq(f'../pixellab/maze/anim/{n}_frun', KS * 2, 0, 1)[0] for n in NAMES}\nSRUN = {n: seq(f'../pixellab/race/{n}_run', KS * 2, 1, 9) for n in ['joy', 'cyrus', 'cleo', 'ray']}\nPANIC = {n: seq(f'../pixellab/maze/anim/{n}_panic', KS * 2, 1, 9) for n in NAMES}\nBLK = crop(Image.open('block/07.png').convert('RGBA')).resize((ROWH, ROWH), Image.NEAREST)\nFT = int(78 * 2 * KS)   # sprite foot offset")
R("GUM = {n: gummy(GK[n], 2) for n in NAMES}; GUM['joy'] = up(gummy_src('acv'), 2)","GUM = {n: gummy(GK[n], 2 * KS) for n in NAMES}; GUM['joy'] = up(gummy_src('acv'), 2 * KS)")
R("x = SX[n]; d.rectangle([x - 70, TOP - 20, x + 70, BOT + 6], fill=(22, 14, 12, 255)); d.rectangle([x - 70, TOP - 20, x + 70, BOT + 6], outline=(90, 62, 40, 255), width=5)",
  "x = SX[n]; d.rectangle([x - CW, TOP - 20, x + CW, BOT + 6], fill=(22, 14, 12, 255)); d.rectangle([x - CW, TOP - 20, x + CW, BOT + 6], outline=(90, 62, 40, 255), width=5)")
R("d.rectangle([SX[n] - 64, BOT, SX[n] + 64, TUN_TOP + 3], fill=(22, 14, 12, 255))","d.rectangle([SX[n] - ROWH, BOT, SX[n] + ROWH, TUN_TOP + 3], fill=(22, 14, 12, 255))")
R("img.alpha_composite(BLKC[n], (x - 64 + c * 64, y))","img.alpha_composite(BLKC[n], (x - ROWH + c * ROWH, y))")
R("gg = GUM[n]; img.alpha_composite(gg, (x - gg.width // 2, y + 32 - gg.height // 2))","gg = GUM[n]; img.alpha_composite(gg, (x - gg.width // 2, y + ROWH // 2 - gg.height // 2))")
R("d.line([x - 40 + q * 22, y + 8, x - 30 + q * 22, y + 56], fill=(40, 30, 30, 220), width=4)","d.line([x - 50 + q * 28, y + 10, x - 38 + q * 28, y + 70], fill=(40, 30, 30, 220), width=5)")
R("d.rectangle([SX[n] - 66, TOP - 20, SX[n] + 66, bottom], fill=(60, 150, 240, 175))\n                d.rectangle([SX[n] - 66, bottom - 6, SX[n] + 66, bottom], fill=(190, 230, 255, 200))",
  "d.rectangle([SX[n] - CW + 4, TOP - 20, SX[n] + CW - 4, bottom], fill=(60, 150, 240, 175))\n                d.rectangle([SX[n] - CW + 4, bottom - 6, SX[n] + CW - 4, bottom], fill=(190, 230, 255, 200))")
# frame-0 water front: bigger, already well into the street
R("fx = min(W + 40, 150 + 380 * ta); hh = 18 + 10 * ta; base = TOP - 4","fx = min(W + 40, 340 + 330 * ta); hh = 34 + 12 * ta; base = TOP - 4   # n18: a clear wave front on frame 0")
# guides: foot offsets and effect sizes x1.25
R("spr = PANIC[n][int(t * 10) % 8]; spr = ImageEnhance.Brightness(ImageEnhance.Color(spr).enhance(0.15)).enhance(0.7)   # rc12: OUT = greyed\n            img.alpha_composite(spr, (int(x - spr.width / 2), int(by - 156 + 20)))\n            layer(img, lambda d: d.ellipse([x - 70, by - 150, x + 70, by + 10], fill=(170, 220, 255, 60), outline=(230, 245, 255, 220), width=5))\n            layer(img, lambda d: d.ellipse([x - 52, by - 132, x - 36, by - 116], fill=(255, 255, 255, 220)))\n            if n not in rise: rise[n] = t; out_ev.append((round(t, 3), 'poof'))",
  "spr = PANIC[n][int(t * 10) % 8]; spr = ImageEnhance.Brightness(ImageEnhance.Color(spr).enhance(0.15)).enhance(0.7)   # rc12: OUT = greyed\n            img.alpha_composite(spr, (int(x - spr.width / 2), int(by - FT + 25)))\n            layer(img, lambda d: d.ellipse([x - 88, by - 188, x + 88, by + 12], fill=(170, 220, 255, 60), outline=(230, 245, 255, 220), width=6))\n            layer(img, lambda d: d.ellipse([x - 65, by - 165, x - 45, by - 145], fill=(255, 255, 255, 220)))\n            if n not in rise and not REW: rise[n] = t; oev((round(t, 3), 'poof'))")
R("text_layer(img, [(x + 74, y - 185 - 10 * min(1, u_ / 0.1), '!', int(64 * sc_), (255, 214, 60), 8, int(255 * min(1, (tp + 0.7 - ta) / 0.12)))])\n                if i_ == 0 and abs(ta - tp) < 0.5 / 30: out_ev.append((round(t, 3), 'boing'))",
  "text_layer(img, [(x + 70, y - 235 - 10 * min(1, u_ / 0.1), '!', int(72 * sc_), (255, 214, 60), 8, int(255 * min(1, (tp + 0.7 - ta) / 0.12)))])\n                if i_ == 0 and abs(ta - tp) < 0.5 / 30: oev((round(t, 3), 'boing'))")
R("bx, by_ = x + 80 * math.cos(a_), y - 80 + 95 * math.sin(a_)","bx, by_ = x + 100 * math.cos(a_), y - 100 + 118 * math.sin(a_)")
R("layer(img, lambda d: [d.line([x + sd * (70 + 10 * ((q + int(t * 15)) % 2)), y - 150 + q * 34, x + sd * (70 + 10 * ((q + int(t * 15)) % 2)), y - 110 + q * 34 + 20], fill=(255, 190, 90, 230), width=6) for sd in (-1, 1) for q in range(4)] + [d.rectangle([x - 50 + q * 22 + 6 * math.sin(t * 20 + q), y - 22 - ((t * 90 + q * 13) % 30), x - 38 + q * 22 + 6 * math.sin(t * 20 + q), y - 10 - ((t * 90 + q * 13) % 30)], fill=(210, 180, 140, 170)) for q in range(5)])",
  "layer(img, lambda d: [d.line([x + sd * (88 + 12 * ((q + int(t * 15)) % 2)), y - 188 + q * 42, x + sd * (88 + 12 * ((q + int(t * 15)) % 2)), y - 138 + q * 42 + 25], fill=(255, 190, 90, 230), width=7) for sd in (-1, 1) for q in range(4)] + [d.rectangle([x - 62 + q * 28 + 7 * math.sin(t * 20 + q), y - 28 - ((t * 90 + q * 13) % 38), x - 47 + q * 28 + 7 * math.sin(t * 20 + q), y - 13 - ((t * 90 + q * 13) % 38)], fill=(210, 180, 140, 170)) for q in range(5)])")
R("img.alpha_composite(spr, (int(x - spr.width / 2), int(y - 156)))","img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FT)))")
# shield: bubble holds, then pops 0.3s before she is out
R("        if s['shield'] or (s['hold'] > 0 and 0 <= t - s['hold'] + 0.9 < 0.9):\n            layer(img, lambda d: (d.ellipse([x - 78, y - 172, x + 78, y + 12], fill=(120, 230, 110, 55)), d.ellipse([x - 78, y - 172, x + 78, y + 12], outline=(170, 255, 150, 235), width=6), d.ellipse([x - 58, y - 152, x - 40, y - 134], fill=(255, 255, 255, 200))))",
  """        if s['shield'] or (s['hold'] > 0 and 0 <= t - s['hold'] + 0.9 < 0.6):
            layer(img, lambda d: (d.ellipse([x - 98, y - 215, x + 98, y + 15], fill=(120, 230, 110, 55)), d.ellipse([x - 98, y - 215, x + 98, y + 15], outline=(170, 255, 150, 235), width=7), d.ellipse([x - 72, y - 190, x - 50, y - 168], fill=(255, 255, 255, 200))))
        if s['hold'] > 0 and 0 <= t - (s['hold'] - 0.3) < 0.3:      # n18: shield POP (ring bursts into shards)
            u_ = (t - (s['hold'] - 0.3)) / 0.3; al_ = int(255 * (1 - u_)); r0 = 100 + 70 * u_; cy_ = y - 100
            layer(img, lambda d: [d.line([x + r0 * math.cos(a_), cy_ + r0 * math.sin(a_), x + (r0 + 26) * math.cos(a_), cy_ + (r0 + 26) * math.sin(a_)], fill=(170, 255, 150, al_), width=8) for a_ in [q * 0.785 + 0.3 for q in range(8)]]
                  + [d.ellipse([x + (r0 - 20) * math.cos(a_) - 7, cy_ + (r0 - 20) * math.sin(a_) - 7 + 60 * u_ * u_, x + (r0 - 20) * math.cos(a_) + 7, cy_ + (r0 - 20) * math.sin(a_) + 7 + 60 * u_ * u_], fill=(200, 255, 190, al_)) for a_ in [q * 0.785 for q in range(8)]])
            if abs(t - (s['hold'] - 0.3)) < 0.5 / 30: oev((round(t, 3), 'poofpops'))""")
R("text_layer(img, [(min(x + 40, 840), y - 190 - 40 * u, 'Z', 58, (220, 190, 255), 8, int(255 * (1 - u))), (min(x + 84, 860), y - 240 - 40 * u, 'z', 44, (220, 190, 255), 7, int(255 * (1 - u)))])",
  "text_layer(img, [(min(x + 50, 840), y - 238 - 40 * u, 'Z', 62, (220, 190, 255), 8, int(255 * (1 - u))), (min(x + 100, 860), y - 296 - 40 * u, 'z', 48, (220, 190, 255), 7, int(255 * (1 - u)))])")
R("layer(img, lambda d: [d.rectangle([x - 60 + q * 24, y - 10 - u * 40 + (q % 2) * 10, x - 48 + q * 24, y + 2 - u * 40 + (q % 2) * 10], fill=RING[n] + (int(255 * (1 - u)),)) for q in range(6)])",
  "layer(img, lambda d: [d.rectangle([x - 75 + q * 30, y - 12 - u * 50 + (q % 2) * 12, x - 60 + q * 30, y + 3 - u * 50 + (q % 2) * 12], fill=RING[n] + (int(255 * (1 - u)),)) for q in range(6)])")
# sounds + popups (skip during rewind)
R("            if snd: out_ev.append((round(te, 3), snd))","            if snd: oev((round(te, 3), snd))")
R("        if kind == 'gum' and 0 <= u < 1.0:","        if REW: continue\n        if kind == 'gum' and 0 <= u < 1.0:")
R("r_ = 60 + 900 * u; dd.ellipse([SX[n] - r_, st[n]['y'] - 80 - r_, SX[n] + r_, st[n]['y'] - 80 + r_], outline=(200, 140, 255, int(220 * (1 - u / 0.6))), width=14)",
  "r_ = 60 + 900 * u; dd.ellipse([SX[n] - r_, st[n]['y'] - 100 - r_, SX[n] + r_, st[n]['y'] - 100 + r_], outline=(200, 140, 255, int(220 * (1 - u / 0.6))), width=14)")
R("        if not any(e[1] == 'boom' for e in out_ev): out_ev.append((T_FLOOD, 'boom'))","        if not any(e[1] == 'boom' for e in out_ev): oev((T_FLOOD, 'boom'))")
# breakthrough beat
R("    # header\n","""    # n18: Rayleigh's breakthrough gets its own beat (flash + purple burst at the shaft floor)
    if not REW and 0 <= t - T_THR < 0.5:
        u = (t - T_THR) / 0.5; bxw = SX[WIN]; byw = BOT
        layer(img, lambda dd: dd.rectangle([0, 0, W, H], fill=(255, 255, 255, int(170 * max(0, 1 - u / 0.3)))))
        layer(img, lambda dd: [dd.ellipse([bxw - r_, byw - r_ * 0.6, bxw + r_, byw + r_ * 0.6], outline=(210, 150, 255, int(240 * (1 - u))), width=12) for r_ in (60 + 420 * u, 20 + 260 * u)]
              + [dd.rectangle([bxw + (q - 3.5) * 34 - 9, byw - 40 + 300 * u * u - 120 * u * (q % 3), bxw + (q - 3.5) * 34 + 9, byw - 22 + 300 * u * u - 120 * u * (q % 3)], fill=RING[WIN] + (int(255 * (1 - u)),)) for q in range(8)])
        if abs(t - T_THR) < 0.5 / 30: oev((round(t, 3), 'powerup1')); oev((round(t, 3), 'brick_8bit'))
    # header
""")
R("    for (a0, b0, tx, c0, n0, _, pr) in STAMPS:\n        if a0 <= t < b0 and t < T_WIN:","    for (a0, b0, tx, c0, n0, _, pr) in STAMPS:\n        if a0 <= t < b0 and t < T_WIN and not REW:")
R("                plate(img, EXIT_X, 1020, tx, 60, c0, al, scale=sc, border=(120, 200, 255))","                plate(img, EXIT_X, TOP - 95, tx, 64, c0, al, scale=sc, border=(120, 200, 255))   # n18: FLOOD! above the columns")
R("else s_['y'] - 250","else s_['y'] - 300")
R("        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(T_WIN + 0.05, 3), 'victory'))","        if not any(e[1] == 'victory' for e in out_ev): oev((round(T_WIN + 0.05, 3), 'victory'))")
R("SEV = [(T_FLOOD, 'THE DAM BROKE!', (120, 200, 255), 'center', 0, 3, 1.5)]   # with REACH THE PORTAL! under it","SEV = [(T_FLOOD, 'FLOOD!', (120, 200, 255), 'center', 0, 3, 1.2)]   # n18: was THE DAM BROKE!")
# render loop -> function, plus card + rewind ending
R("END = T_WIN + 1.5; NF = int(END * 30)","CARD = 1.1; END = T_WIN + CARD; NF = int(END * 30); NREW = 24   # n18: win card 1.1s, then a 0.8s rewind back to frame 0 (water drains)\nT_THR = [e[0] for e in EV if e[1] == 'through' and e[2] == WIN][0]\nREW = False\ndef oev(e):\n    if not REW: out_ev.append(e)")
R("for f in range(NF + PF):\n    ta = f / 30; t = ta - PRE; st, wy = FR[max(0, min(f - PF, len(FR) - 1))]\n    img = BOARD.copy()",
  "def render(ta):\n    t = ta - PRE; st, wy = FR[max(0, min(int(round(ta * 30)) - PF, len(FR) - 1))]\n    img = BOARD.copy()")
R("    img.alpha_composite(HOOK2 if t >= T_WIN else HOOK)\n    wr.write(img)\n    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')\nwr.close()",
  """    img.alpha_composite(HOOK2 if t >= T_WIN else HOOK)
    return img
for f in range(NF + PF):
    img = render(f / 30); wr.write(img)
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
REW = True; TA0 = PRE + T_WIN - 1 / 30; out_ev.append((round(T_WIN + CARD - 0.05, 3), 'rewind'))
for i in range(NREW):
    u = (i + 1) / NREW; ta = TA0 * (1 - u) ** 1.15
    img = render(ta)
    tint = Image.new('RGBA', (W, H), (40, 70, 140, int(70 * math.sin(math.pi * u)))); img.alpha_composite(tint)
    layer(img, lambda dd: [dd.rectangle([0, (yy + i * 53) % H, W, (yy + i * 53) % H + 6], fill=(230, 240, 255, 60)) for yy in (300, 900, 1400)])
    wr.write(img)
    if NF + PF + i in KEEP: img.convert('RGB').save(OUTD + f'/k_{NF + PF + i:04d}.png')
wr.close()""")
open(p,'w').write(s); print('ok')
