p='r104c.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a[:100], s.count(a)); s=s.replace(a,b)
# (5) plain dig for Cyrus (cyrus_dig2 has a built-in fire slash that reads as STRENGTH)
R("'cyrus': seq('cyrus_dig2', KS * 2, 1, 9)","'cyrus': seq('cyrus_dig', KS * 2, 1, 9)")
R("if t - s['power'] < 1.6 and n == 'cleo':","if t - s['power'] < STR and n == 'cleo':")
R("if t - s['power'] < 1.6 and n == 'cyrus':","if t - s['power'] < SPD and n == 'cyrus':")
# (1) caught: the bubble lifts the greyed guide straight to her tracker icon and pops there within 0.5s
R("""        if s['caught'] is not None:
            u = t - s['caught']; by = max(TOP - 10, y - 60 - u * 260) + 8 * math.sin(t * 3)
            spr = PANIC[n][int(t * 10) % 8]; spr = ImageEnhance.Brightness(ImageEnhance.Color(spr).enhance(0.15)).enhance(0.7)   # rc12: OUT = greyed
            img.alpha_composite(spr, (int(x - spr.width / 2), int(by - FT + 25)))
            layer(img, lambda d: d.ellipse([x - 88, by - 188, x + 88, by + 12], fill=(170, 220, 255, 60), outline=(230, 245, 255, 220), width=6))
            layer(img, lambda d: d.ellipse([x - 65, by - 165, x - 45, by - 145], fill=(255, 255, 255, 220)))
            if n not in rise and not REW: rise[n] = t; oev((round(t, 3), 'poof'))
            continue""",
"""        if s['caught'] is not None:
            u = t - s['caught']
            if u < GH:
                k = u / GH; e = k * k * (3 - 2 * k); sc = 1 - 0.62 * e
                ix, iy = SX[n], ROSTER_Y + 34; cx0, cy0 = x, y - 100
                bxc = cx0 + (ix - cx0) * e; byc = cy0 + (iy - cy0) * e
                spr = PANIC[n][int(t * 10) % 8]; spr = ImageEnhance.Brightness(ImageEnhance.Color(spr).enhance(0.15)).enhance(0.7)   # OUT = greyed
                spr = spr.resize((max(1, int(spr.width * sc)), max(1, int(spr.height * sc))), Image.NEAREST)
                img.alpha_composite(spr, (int(bxc - spr.width / 2), int(byc + 100 * sc - FT * sc)))
                rb = 100 * sc
                layer(img, lambda d: (d.ellipse([bxc - rb, byc - rb, bxc + rb, byc + rb], fill=(170, 220, 255, 60), outline=(230, 245, 255, 220), width=6), d.ellipse([bxc - rb * 0.62, byc - rb * 0.72, bxc - rb * 0.42, byc - rb * 0.52], fill=(255, 255, 255, 220))))
            elif u < GH + 0.25:                          # pops into the crossed-out tracker icon
                k = (u - GH) / 0.25; ix, iy = SX[n], ROSTER_Y + 34; r0 = 34 + 40 * k; al_ = int(255 * (1 - k))
                layer(img, lambda d: [d.line([ix + r0 * math.cos(a_), iy + r0 * math.sin(a_), ix + (r0 + 14) * math.cos(a_), iy + (r0 + 14) * math.sin(a_)], fill=(230, 245, 255, al_), width=6) for a_ in [q * 0.785 for q in range(8)]])
            if n not in rise and not REW: rise[n] = t; oev((round(t, 3), 'poof')); oev((round(t + GH, 3), 'poofpops'))
            continue""")
R("        if s['caught'] is not None:\n            d.line([ix - 24,","        if s['caught'] is not None and t >= s['caught'] + GH:\n            d.line([ix - 24,")
R("        icc = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55) if s['caught'] is not None else ic",
  "        icc = ImageEnhance.Brightness(ImageEnhance.Color(ic).enhance(0.2)).enhance(0.55) if (s['caught'] is not None and t >= s['caught'] + GH) else ic")
R("yy_ = (max(TOP - 10, s_['y'] - 60 - (t - s_['caught']) * 260) - 150) if s_['caught'] is not None else s_['y'] - 300","yy_ = s_['y'] - 300")
# (3) shield: holds the water above her, cracks, pops, then the water rushes down her shaft (~0.9s) before she is out
R("""        if s['shield'] or (s['hold'] > 0 and 0 <= t - s['hold'] + 0.9 < 0.6):
            layer(img, lambda d: (d.ellipse([x - 98, y - 215, x + 98, y + 15], fill=(120, 230, 110, 55)), d.ellipse([x - 98, y - 215, x + 98, y + 15], outline=(170, 255, 150, 235), width=7), d.ellipse([x - 72, y - 190, x - 50, y - 168], fill=(255, 255, 255, 200))))
        if s['hold'] > 0 and 0 <= t - (s['hold'] - 0.3) < 0.3:      # n18: shield POP (ring bursts into shards)
            u_ = (t - (s['hold'] - 0.3)) / 0.3; al_ = int(255 * (1 - u_)); r0 = 100 + 70 * u_; cy_ = y - 100""",
"""        TBn = s['hold'] - HOLD if s['hold'] > 0 else -99
        if s['shield'] or (0 <= t - TBn < T_POP):
            layer(img, lambda d: (d.ellipse([x - 98, y - 215, x + 98, y + 15], fill=(120, 230, 110, 55)), d.ellipse([x - 98, y - 215, x + 98, y + 15], outline=(170, 255, 150, 235), width=7), d.ellipse([x - 72, y - 190, x - 50, y - 168], fill=(255, 255, 255, 200))))
            if T_CRK <= t - TBn < T_POP:                 # cracks spread across the bubble
                kc = (t - TBn - T_CRK) / (T_POP - T_CRK)
                CR = [[(0, -112), (-14, -80), (8, -52), (-6, -20)], [(-60, -150), (-36, -128), (-46, -100)], [(58, -146), (34, -118), (48, -86), (30, -60)]]
                layer(img, lambda d: [d.line([(x + px_, y - 100 + py_) for px_, py_ in cr[:max(2, int(len(cr) * min(1, kc * 1.6)))]], fill=(250, 255, 245, 245), width=5) for cr in CR[:1 + int(kc * 2.99)]])
                if abs(t - TBn - T_CRK) < 0.5 / 30: oev((round(t, 3), 'crunch_8bit'))
        if s['hold'] > 0 and 0 <= t - (TBn + T_POP) < 0.3:      # shield POP (ring bursts into shards)
            u_ = (t - (TBn + T_POP)) / 0.3; al_ = int(255 * (1 - u_)); r0 = 100 + 70 * u_; cy_ = y - 100""")
R("            if abs(t - (s['hold'] - 0.3)) < 0.5 / 30: oev((round(t, 3), 'poofpops'))","            if abs(t - (TBn + T_POP)) < 0.5 / 30: oev((round(t, 3), 'poofpops'))")
# water: held above the bubble, then rushing down after the pop; (2) pour into the chamber behind the winner
R("""        for n in NAMES:
            s = st[n]; floor = TOP + s['d'] * ROWH if s['phase'] == 'dig' else TUN_TOP
            bottom = min(wy, floor)""",
"""        for n in NAMES:
            s = st[n]; floor = TOP + s['d'] * ROWH if s['phase'] == 'dig' else TUN_TOP
            bottom = min(wy, floor)
            TBn = s['hold'] - HOLD if s['hold'] > 0 else -99
            if 0 <= t - TBn < HOLD and s['caught'] is None:
                btop = floor - 215
                if t - TBn < T_POP: bottom = min(bottom, btop)
                else: kk = min(1, (t - TBn - T_POP) / (HOLD - T_POP)); bottom = min(bottom, btop + (floor - 40 - btop) * kk * kk)""")
R("""        for q in range(26):
            bx = (q * 97 + t * 40) % W; by = TOP - ((t * 120 + q * 53) % 60)""",
"""        if T_POUR is not None and t >= T_POUR:          # the winner's shaft drains into the chamber behind him
            u = t - T_POUR; xw = SX[WIN]; fall_ = min(1, u / 0.18); floor_y = 1496
            d.rectangle([xw - CW + 10, TUN_TOP - 4, xw + CW - 10, TUN_TOP + (floor_y - TUN_TOP) * fall_], fill=(60, 150, 240, 190))
            for q in range(5):
                yy = TUN_TOP + ((u * 520 + q * 40) % max(1, (floor_y - TUN_TOP) * fall_))
                d.line([xw - CW + 20 + q * 30, yy, xw - CW + 20 + q * 30, yy + 26], fill=(210, 240, 255, 200), width=5)
            if fall_ >= 1:
                ph_ = min(80, 150 * (u - 0.18)); xl = max(80, xw - 360 * (u - 0.18)); xr_ = min(876, xw + 200 * (u - 0.18))
                d.rectangle([xl, floor_y - ph_, xr_, floor_y], fill=(60, 150, 240, 185))
                d.rectangle([xl, floor_y - ph_ - 5, xr_, floor_y - ph_ + 3], fill=(200, 235, 255, 210))
        for q in range(26):
            bx = (q * 97 + t * 40) % W; by = TOP - ((t * 120 + q * 53) % 60)""")
# (6) no '!' during the rewind
R("            if tp <= ta < tp + 0.7:","            if tp <= ta < tp + 0.7 and not REW:")
# constants
R("T_THR = [e[0] for e in EV if e[1] == 'through' and e[2] == WIN][0]",
  """T_THR = [e[0] for e in EV if e[1] == 'through' and e[2] == WIN][0]
GH = 0.5; T_CRK = 0.6; T_POP = 1.0          # n19: ghost-to-icon time; shield crack / pop times after BLOCKED
T_POUR = next((i / 30 for i, (_, wy_) in enumerate(FR) if i / 30 >= T_THR and wy_ >= TUN_TOP - 6), None)
print('T_THR', round(T_THR, 2), 'T_POUR', T_POUR and round(T_POUR, 2), 'T_WIN', round(T_WIN, 2))""")
open(p,'w').write(s); print('patched')
