p='r104.py'; s=open(p).read()
def R(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, (s.count(a), a); s=s.replace(a,b)
R("PORTAL = crop(Image.open('portal/12.png').convert('RGBA')); PORTAL = up(PORTAL, 4)",
  "PORTAL = crop(Image.open('portal/12.png').convert('RGBA')); PORTAL = up(PORTAL, 4); print('portal', PORTAL.size)\nHOOK, HB = hook_layer(['WHO SURVIVES', 'THE FLOOD?'], accent=1, color=(120, 200, 255)); print('hook bottom', HB)\nROSTER_Y = HB + 10")
R("    d.rectangle([40, TUNNEL_Y - 170, W - 40, TUNNEL_Y + 40], fill=(26, 18, 14, 235)); d.rectangle([40, TUNNEL_Y - 170, W - 40, TUNNEL_Y + 40], outline=(90, 62, 40, 255), width=5)\n    for n in NAMES:\n        d.rectangle([SX[n] - 64, BOT, SX[n] + 64, TUNNEL_Y - 170], fill=(22, 14, 12, 255))",
  "    d.rectangle([76, TUN_TOP, 880, 1500], fill=(26, 18, 14, 235)); d.rectangle([76, TUN_TOP, 880, 1500], outline=(90, 62, 40, 255), width=5)\n    for n in NAMES:\n        d.rectangle([SX[n] - 64, BOT, SX[n] + 64, TUN_TOP + 3], fill=(22, 14, 12, 255))")
R("BOARD.alpha_composite(PORTAL, (EXIT_X - PORTAL.width // 2, TUNNEL_Y + 30 - PORTAL.height))",
  "BOARD.alpha_composite(PORTAL, (EXIT_X - PORTAL.width // 2, 1496 - PORTAL.height))")
R("END = T_WIN + 3.0; NF = int(END * 30); wr = Writer('flood_noaudio.mp4'); out_ev = []",
  "END = T_WIN + 3.0; NF = int(END * 30); wr = Writer(OUTD + '/noaudio.mp4'); out_ev = []\nKEEP = {int(x) for x in os.environ.get('KEEP', '').split(',') if x}")
R("img.alpha_composite(HUB[int(t * 5) % len(HUB)], (0, 330))","img.alpha_composite(HUB[int(t * 5) % len(HUB)], (0, TOP - 260))")
R("        d.rectangle([0, 560, W, TOP - 10], fill=(60, 150, 240, 170))","        d.rectangle([0, TOP - 110, W, TOP - 10], fill=(60, 150, 240, 170))")
R("floor = TOP + s['d'] * ROWH if s['phase'] == 'dig' else (TUNNEL_Y - 170 if s['phase'] != 'dig' else BOT)","floor = TOP + s['d'] * ROWH if s['phase'] == 'dig' else TUN_TOP")
R("                lv = min(TUNNEL_Y + 40, TUNNEL_Y - 170 + (wy - BOT))\n                d.rectangle([40, TUNNEL_Y - 170, W - 40, TUNNEL_Y + 40], fill=(0, 0, 0, 0))\n","")
R("bx = (q * 97 + t * 40) % W; by = 600 - ((t * 120 + q * 53) % 60)","bx = (q * 97 + t * 40) % W; by = TOP - ((t * 120 + q * 53) % 60)")
R("u = t - s['caught']; by = max(520, y - 60 - u * 260) + 8 * math.sin(t * 3)","u = t - s['caught']; by = max(TOP - 10, y - 60 - u * 260) + 8 * math.sin(t * 3)")
R("        elif s['phase'] == 'dig':\n            ph = int((1 - max(0, s['nxt'] - t) / 0.3) * 7.99); spr = DIG[n][max(0, min(7, ph))]\n            if t - s['power'] < 1.6:\n                layer(img, lambda d: d.ellipse([x - 80, y - 170, x + 80, y + 10], fill=(255, 220, 120, 60)))",
  "        elif s['phase'] == 'dig':\n            ph = int((1 - max(0, s['nxt'] - t) / 0.3) * 7.99); spr = DIG[n][max(0, min(7, ph))]\n            if t < s['sleep']: spr = DIG[n][0]\n            if t - s['power'] < 1.6 and n == 'cleo':\n                pul = 6 * math.sin(t * 18)\n                layer(img, lambda d: (d.ellipse([x - 84 - pul, y - 176 - pul, x + 84 + pul, y + 14 + pul], fill=(90, 150, 255, 70)), d.ellipse([x - 84 - pul, y - 176 - pul, x + 84 + pul, y + 14 + pul], outline=(160, 205, 255, 255), width=6)))\n            if t - s['power'] < 1.6 and n == 'cyrus':\n                layer(img, lambda d: [d.line([x + sd * (70 + 10 * ((q + int(t * 15)) % 2)), y - 150 + q * 34, x + sd * (70 + 10 * ((q + int(t * 15)) % 2)), y - 110 + q * 34 + 20], fill=(255, 190, 90, 230), width=6) for sd in (-1, 1) for q in range(4)] + [d.rectangle([x - 50 + q * 22 + 6 * math.sin(t * 20 + q), y - 22 - ((t * 90 + q * 13) % 30), x - 38 + q * 22 + 6 * math.sin(t * 20 + q), y - 10 - ((t * 90 + q * 13) % 30)], fill=(210, 180, 140, 170)) for q in range(5)])")
R("        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - 156)))\n",
  "        img.alpha_composite(spr, (int(x - spr.width / 2), int(y - 156)))\n        if s['shield'] or (s['hold'] > 0 and 0 <= t - s['hold'] + 0.9 < 0.9):\n            layer(img, lambda d: (d.ellipse([x - 78, y - 172, x + 78, y + 12], fill=(120, 230, 110, 55)), d.ellipse([x - 78, y - 172, x + 78, y + 12], outline=(170, 255, 150, 235), width=6), d.ellipse([x - 58, y - 152, x - 40, y - 134], fill=(255, 255, 255, 200))))\n        if t < s['sleep'] and s['phase'] == 'dig':\n            u = (t * 1.3) % 1\n            text_layer(img, [(x + 40, y - 190 - 40 * u, 'Z', 40, (220, 190, 255), 6, int(255 * (1 - u))), (x + 70, y - 230 - 40 * u, 'z', 28, (220, 190, 255), 5, int(255 * (1 - u)))])\n")
R("            snd = {'hit': 'stomp_8bit', 'break': 'brick_8bit', 'gum': 'powerup_8bit', 'out': 'vg02'}.get(kind)",
  "            snd = {'hit': 'stomp_8bit', 'break': 'brick_8bit', 'gum': 'powerup_8bit', 'out': 'vg02', 'blocked': 'sword_hit'}.get(kind)")
R("        if kind == 'gum' and 0 <= u < 1.0:\n            a = int(255 * min(1, (1 - u) / 0.3)); ctext(dd, SX[n], st[n]['y'] - 240 - u * 40, 'POWER DIG!', F(26), (255, 214, 60), 5, a)",
  "        if kind == 'gum' and 0 <= u < 1.0:\n            a = int(255 * min(1, (1 - u) / 0.3)); ctext(dd, min(max(SX[n], 70 + 4 * 34), 887 - 4 * 34), max(st[n]['y'] - 250 - u * 40, ROSTER_Y + 78), PLAB[n], F(34), PCOL[n], 7, a)\n            if n == 'ray' and u < 0.6:\n                r_ = 60 + 900 * u; dd.ellipse([SX[n] - r_, st[n]['y'] - 80 - r_, SX[n] + r_, st[n]['y'] - 80 + r_], outline=(200, 140, 255, int(220 * (1 - u / 0.6))), width=14)\n        if kind == 'blocked' and 0 <= u < 1.0:\n            a = int(255 * min(1, (1 - u) / 0.3)); ctext(dd, min(max(SX[n], 70 + 4 * 34), 887 - 4 * 34), max(st[n]['y'] - 250 - u * 40 + 50, ROSTER_Y + 120), 'BLOCKED!', F(34), (170, 255, 150), 7, a)")
R("        text_layer(img, [(W / 2, 470, 'THE DAM BROKE!', 56, (120, 200, 255), 8, a)])","        text_layer(img, [(EXIT_X, 1372, 'THE DAM BROKE!', 52, (120, 200, 255), 8, a)])")
R("    layer(img, lambda d: d.rectangle([0, 0, W, 330], fill=(10, 14, 30, 230)))\n    d = ImageDraw.Draw(img)\n    ctext(d, W / 2, 34, 'WHO SURVIVES', F(64)); ctext(d, W / 2, 118, 'THE FLOOD?', F(64), (120, 200, 255))\n",
  "    layer(img, lambda d: d.rounded_rectangle([96, ROSTER_Y - 4, 860, ROSTER_Y + 72], 16, fill=(10, 14, 30, 215)))\n")
R("img.alpha_composite(icc, (ix - ic.width // 2, 214))","img.alpha_composite(icc, (ix - ic.width // 2, ROSTER_Y))")
R("d.line([ix - 24, 224, ix + 24, 272], fill=(230, 50, 50), width=8); d.line([ix - 24, 272, ix + 24, 224], fill=(230, 50, 50), width=8)",
  "d.line([ix - 24, ROSTER_Y + 10, ix + 24, ROSTER_Y + 58], fill=(230, 50, 50), width=8); d.line([ix - 24, ROSTER_Y + 58, ix + 24, ROSTER_Y + 10], fill=(230, 50, 50), width=8)")
R("d.ellipse([ix - 40, 208, ix + 40, 288], outline=(255, 214, 60), width=6)","d.ellipse([ix - 40, ROSTER_Y - 6, ix + 40, ROSTER_Y + 74], outline=(255, 214, 60), width=6)")
R("        text_layer(img, [(W / 2, 1500, 'PICK ONE!', 60, (255, 255, 255), 8, 255)])","        text_layer(img, [(EXIT_X, 1360, 'PICK ONE!', 60, (255, 255, 255), 8, 255)])")
R("layer(img, lambda dd: dd.rectangle([0, 330, W, H], fill=(6, 8, 18, int(150 * a))))","layer(img, lambda dd: dd.rectangle([0, ROSTER_Y + 80, W, H], fill=(6, 8, 18, int(150 * a))))")
R("vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))","vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (EXIT_X - vf.width // 2, 1180 - vf.height))")
R("text_layer(img, [(W / 2, 1230, LABEL[WIN] + ' SURVIVED!', 44 if len(LABEL[WIN]) > 8 else 60, (255, 214, 60), 8, 255)])","text_layer(img, [(EXIT_X, 1230, LABEL[WIN] + ' SURVIVED!', 44 if len(LABEL[WIN]) > 8 else 56, (255, 214, 60), 8, 255)])")
R("    wr.write(img)\n    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/w_{f:04d}.png')",
  "    img.alpha_composite(HOOK)\n    wr.write(img)\n    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')")
R("json.dump({'events': out}, open('flood_events.json', 'w'))","json.dump({'events': out}, open(OUTD + '/ev.json', 'w'))")
open(p,'w').write(s); print('edited')
