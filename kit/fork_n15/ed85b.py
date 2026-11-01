p='r85.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}", """SRUNL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in SRUN.items()}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', SS, 1, 9) for g in NAMES}
ATK = {g: seq(PL + f'race/{g}_atk', SS, 0) for g in NAMES}      # n15b: Syeda/PixelLab attack frames (same sets as #89)
ATKL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in ATK.items()}
BCX = {'joy': 34.5, 'cyrus': 29.0, 'cleo': 31.0, 'ray': 29.5}
def atk_frame(a):
    if a < ATK_WIND: return 0 if a < ATK_WIND * 0.5 else 1
    if a < ATK_WIND + 0.3: return 2 + min(5, int((a - ATK_WIND) / 0.3 * 6))
    return 8 + min(4, int((a - ATK_WIND - 0.3) / (ATK_LEN - ATK_WIND - 0.3) * 5))""")
R("TW = float(os.environ.get('TW', '3.5')); END = T0 + DUR + TW", "HOLD = float(os.environ.get('HOLD', '0.7'))")
R("G_ = 6000.0; U_D0 = 0.5; H0 = LY + 300;", """QX, QY = 880, 700; QS = 5   # n15b: the covered '?' prize floats over the arena from frame 0
def cover(im):   # dark cloth silhouette of the prize with a white '?'
    a = im.getchannel('A'); c = Image.new('RGBA', im.size, (46, 30, 70, 255)); c.putalpha(a)
    d = ImageDraw.Draw(c); fq = F(int(im.height * 0.62)); w_ = d.textlength('?', font=fq)
    d.text((im.width / 2 - w_ / 2, im.height * 0.12), '?', font=fq, fill=(255, 255, 255), stroke_width=6, stroke_fill=(20, 10, 30)); return c
QPRIZE = cover(gummy('mel', QS)); QBIG = cover(PRIZE)
U_GL0, U_GL1 = 0.2, 0.6   # glides over beside the winner, growing to full size
G_ = 6000.0; U_D0 = 0.75; H0 = LY - QY; """)
R("U_SPLIT = U_LAND + T_B + 0.45; U_CATCH = U_SPLIT + 0.55", "U_SPLIT = U_LAND + T_B + 0.4; U_CATCH = U_SPLIT + 0.7; U_EAT = U_CATCH + 0.35   # n15b: pieces fly into hands, held a beat, eaten, then the nap\nEND = T0 + DUR + U_EAT + HOLD")
R("""    if U_D0 <= U_ < U_SPLIT: objs.append((LY - 40, 'g', None))   # drawn behind nearby guides""", """    if U_D0 <= U_ < U_SPLIT: objs.append((LY - 40, 'g', None))   # drawn behind nearby guides
    if U_ < U_D0:   # the covered prize: bobs over the arena, then glides beside the winner
        kq = 0.0 if U_ < U_GL0 else min(1.0, (U_ - U_GL0) / (U_GL1 - U_GL0)); kq = kq * kq * (3 - 2 * kq)
        qx = QX + (LX - QX) * kq; qb = QY + (0 if kq > 0 else 10 * math.sin(t * 3)); qi = QPRIZE if kq == 0 else QPRIZE.resize((int(QPRIZE.width + (QBIG.width - QPRIZE.width) * kq), int(QPRIZE.height + (QBIG.height - QPRIZE.height) * kq)), Image.NEAREST)
        layer(img, lambda d: d.ellipse([qx - qi.width * 0.75, qb - qi.height * 0.55 - 30, qx + qi.width * 0.75, qb + 30], fill=(255, 240, 200, 40 + int(25 * math.sin(t * 4)))))
        img.alpha_composite(qi, (int(qx - qi.width / 2), int(qb - qi.height)))
    if U_D0 <= U_ < U_D0 + 0.35:   # the cover pops off
        k3 = (U_ - U_D0) / 0.35
        layer(img, lambda d: [d.ellipse([LX + math.cos(j * 0.785) * (40 + 160 * k3) - 26, QY - PRIZE.height / 2 + math.sin(j * 0.785) * (40 + 160 * k3) - 26, LX + math.cos(j * 0.785) * (40 + 160 * k3) + 26, QY - PRIZE.height / 2 + math.sin(j * 0.785) * (40 + 160 * k3) + 26], fill=(70, 50, 100, int(220 * (1 - k3)))) for j in range(8)])""")
# guide sprite: stun / attack
R("""            if not live or tt < s['sleep']: spr = STAND[n]
            else:""", """            atk_a = tt - s['atk']; hop = 0
            if not live or tt < s['sleep']: spr = STAND[n]
            elif tt - s['stun'] < 0.6:
                spr = PANIC[n][int(t * 14) % 8]; u_ = tt - s['hit']
                if 0 <= u_ < 0.32: hop = int(46 * math.sin(math.pi * u_ / 0.32))   # knocked off their feet for a moment
                if math.hypot(s['vx'], s['vy']) > 80: layer(img, lambda d, x=x, y=y: [d.ellipse([x - 12 - 8 * k - s['vx'] * 0.05 * k, y - 10, x + 12 + 8 * k - s['vx'] * 0.05 * k, y + 6], fill=(230, 220, 200, 140 - 35 * k)) for k in range(3)])
            elif 0 <= atk_a < ATK_LEN: spr = None
            else:""")
R("""            img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
            if live and 0 <= tt - s['shield'] < 6.0:   # SHIELD bubble""", """            if live and 0 <= tt - s['strong'] < 4.0 and spr is not None or (live and 0 <= atk_a < ATK_WIND):   # STRENGTH: power flames rising off the body
                def flames(d, x=x, y=y):
                    r3 = random.Random(int(t * 15) + int(x))
                    for k in range(9):
                        fx = x + r3.uniform(-62, 62); fy = y - r3.uniform(20, FOOT - 20); L = r3.uniform(26, 54)
                        c = r3.choice([(255, 80, 40), (255, 140, 40), (255, 200, 80)])
                        d.polygon([(fx - 7, fy), (fx + 7, fy), (fx, fy - L)], fill=c + (215,))
                layer(img, flames)
            if spr is None:   # planted attack
                fi = atk_frame(atk_a)
                if s['face'] > 0: spr = ATK[n][fi]; ox = BCX[n] * SS
                else: spr = ATKL[n][fi]; ox = (128 - BCX[n]) * SS
                if atk_a < 0.2: layer(img, lambda d, x=x, y=y: [d.ellipse([x + q * 34 - 16, y - 8, x + q * 34 + 16, y + 6], fill=(230, 220, 200, int(150 * (1 - atk_a / 0.2)))) for q in (-1, 1)])
                img.alpha_composite(spr, (int(x - ox), int(y - 104 * SS)))
            else: img.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT - hop)))
            if live and 0 <= tt - s['shield'] < 6.0:   # SHIELD bubble""")
# nap Zzz from U_EAT; pieces into hands
R("""    if U_ >= U_CATCH:   # n15: everyone naps (melatonin), Zzz over every head""", """    if U_ >= U_EAT:   # n15: everyone naps (melatonin), Zzz over every head""")
R("""                u = ((U_ - U_CATCH) * 1.1 + q / 3) % 1.0
                over.append((x + 30 + 36 * u, y - FOOT + 30 - 80 * u, 'Z', 44 - 8 * q, (220, 200, 255), 7, int(255 * min(1, 2 * (1 - u), (U_ - U_CATCH) / 0.2 + q * 0))))""",
"""                u = ((U_ - U_EAT) * 1.1 + q / 3) % 1.0
                over.append((x + 30 + 36 * u, y - FOOT + 30 - 80 * u, 'Z', 44 - 8 * q, (220, 200, 255), 7, int(255 * min(1, 2 * (1 - u), (U_ - U_EAT) / 0.2 + q * 0))))""")
R("""    if U_SPLIT <= U_ < U_CATCH + 0.3:   # n15: the gummy pops into four, one piece arcs to each guide (gravity)""", """    if U_SPLIT <= U_ < U_EAT + 0.3:   # n15b: the gummy pops into four, a piece arcs into each guide's hands, held a beat, eaten""")
R("""        for n in NAMES:
            ax, ay = st['ag'][n]['x'], st['ag'][n]['y'] - FOOT * 0.55
            if U_ < U_CATCH:
                x0, y0 = LX, LY - PRIZE.height / 2
                px_ = x0 + (ax - x0) * k4; py_ = y0 + (ay - y0) * k4 - 260 * 4 * k4 * (1 - k4)
                img.alpha_composite(PIECE, (int(px_ - PIECE.width / 2), int(py_ - PIECE.height / 2)))
            else:
                k6 = (U_ - U_CATCH) / 0.3""", """        for n in NAMES:
            ax, ay = st['ag'][n]['x'] + (26 if st['ag'][n]['x'] < LX else -26), st['ag'][n]['y'] - FOOT * 0.42   # hands, on the side facing the prize
            if U_ < U_CATCH:
                x0, y0 = LX, LY - PRIZE.height / 2
                px_ = x0 + (ax - x0) * k4; py_ = y0 + (ay - y0) * k4 - 260 * 4 * k4 * (1 - k4)
                img.alpha_composite(PIECE, (int(px_ - PIECE.width / 2), int(py_ - PIECE.height / 2)))
            elif U_ < U_EAT:   # held in the hands, then lifted to the mouth
                ke = max(0.0, (U_ - U_CATCH - 0.18) / (U_EAT - U_CATCH - 0.18)); pc = PIECE if ke == 0 else PIECE.resize((max(2, int(PIECE.width * (1 - 0.8 * ke))), max(2, int(PIECE.height * (1 - 0.8 * ke)))), Image.NEAREST)
                hx_, hy_ = ax + ((st['ag'][n]['x'] - ax) * ke), ay - FOOT * 0.28 * ke
                img.alpha_composite(pc, (int(hx_ - pc.width / 2), int(hy_ - pc.height / 2)))
            else:
                k6 = (U_ - U_EAT) / 0.3; ay = st['ag'][n]['y'] - FOOT * 0.7""")
R("    if U_ >= U_CATCH and not any(e[1] == 'twinkle' for e in out_ev): out_ev += [(round(T0 + DUR + U_CATCH, 3), 'twinkle'), (round(T0 + DUR + U_CATCH + 0.15, 3), 'victory')]",
  "    if U_ >= U_CATCH and not any(e[1] == 'jump' for e in out_ev): out_ev.append((round(T0 + DUR + U_CATCH, 3), 'jump'))\n    if U_ >= U_D0 and not any(e[1] == 'poof' and e[0] > T0 + DUR for e in out_ev): out_ev.append((round(T0 + DUR + U_D0, 3), 'poof'))\n    if U_ >= U_EAT and not any(e[1] == 'twinkle' for e in out_ev): out_ev += [(round(T0 + DUR + U_EAT, 3), 'twinkle'), (round(T0 + DUR + U_EAT + 0.15, 3), 'victory')]")
R("    if U_ >= U_CATCH: img.alpha_composite(HOOK_END if U_ >= U_CATCH + 0.15 else Image.blend(HOOK, HOOK_END, (U_ - U_CATCH) / 0.15))", "    if U_ >= U_EAT: img.alpha_composite(HOOK_END if U_ >= U_EAT + 0.15 else Image.blend(HOOK, HOOK_END, (U_ - U_EAT) / 0.15))")
R("    if t < 1.4: img.alpha_composite(RULE)\n", "")
# locked scoreboard
R("    order = sorted(NAMES, key=lambda n: (-cnt[n], NAMES.index(n))); lead_ok = cnt[order[0]] > cnt[order[1]]",
  "    srt_ = sorted(NAMES, key=lambda n: -cnt[n]); lead_ok = cnt[srt_[0]] > cnt[srt_[1]]; order = NAMES   # n15b: order locked, only the leader is highlighted")
R("        if r == 0 and lead_ok: layer(", "        if n == srt_[0] and lead_ok: layer(")
# stale lead stamps
R("        if x_[0] <= t < min(x_[0] + 1.0, nxt) and live: cur = x_", "        if x_[0] <= t < min(x_[0] + 1.0, nxt) and live: cur = x_ if not (x_[1] == 'lead' and not (cnt[x_[2]] > max(cnt[m] for m in NAMES if m != x_[2]))) else None   # n15b: a lead stamp clears the frame the score changes")
# strike burst + POW + sounds
R("""        if e[1] == 'block' and 0 <= u < 0.6:""", """        if e[1] == 'shove' and 0 <= u < 0.35:   # STRENGTH strike: orange impact burst + POW!
            sa = FR[min(int(round(e[0] * FPS)), len(FR) - 1)]['ag']; ix, iy = (sa[e[2]]['x'] + sa[e[3]]['x']) / 2, (sa[e[2]]['y'] + sa[e[3]]['y']) / 2 - FOOT * 0.45; k_ = 1 - u / 0.35
            def burst(d, ix=ix, iy=iy, k_=k_):
                pts = [(ix + (95 if j % 2 == 0 else 42) * (0.6 + 0.6 * (1 - k_)) * math.cos(j * math.pi / 8), iy + (95 if j % 2 == 0 else 42) * (0.6 + 0.6 * (1 - k_)) * math.sin(j * math.pi / 8)) for j in range(16)]
                d.polygon(pts, fill=(255, 150, 40, int(230 * k_)), outline=(255, 240, 160, int(255 * k_)))
            layer(img, burst)
        if e[1] == 'shove' and 0 <= u < 0.8:
            sa = FR[min(int(round(e[0] * FPS)), len(FR) - 1)]['ag'][e[2]]
            text_layer(img, [(max(70 + 110, min(1025 - 110, sa['x'])), sa['y'] - FOOT - 60 - u * 40, 'POW!', 52, (255, 120, 50), 8, int(255 * min(1, (0.8 - u) / 0.3)))])
        if e[1] == 'block' and 0 <= u < 0.6:""")
R("            elif e[1] == 'block': out_ev.append((round(e[0], 3), 'poof'))", "            elif e[1] == 'block': out_ev.append((round(e[0], 3), 'poof'))\n            elif e[1] == 'shove': out_ev.append((round(e[0], 3), 'punch'))\n            elif e[1] == 'whiff': out_ev.append((round(e[0], 3), 'swish'))")
R("            if e[3] == 'cre':\n                rad = 60 + 330 * u", "            if False:\n                rad = 60 + 330 * u")
R("out_ev += [(round(e[0] + 0.05, 3), 'punch')] if e[3] == 'cre' else []", "out_ev += []")
open(p,'w').write(s)
