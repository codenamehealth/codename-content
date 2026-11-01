p='r85.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("U_GL0, U_GL1 = 0.15, 0.45", "U_GL0, U_GL1 = 0.1, 0.35")
R("G_ = 6000.0; U_D0 = 0.55;", "G_ = 6000.0; U_D0 = 0.4;")
R("U_SPLIT = U_LAND + T_B + 0.3; U_CATCH = U_SPLIT + 0.6; U_EAT = U_CATCH + 0.3", "U_SPLIT = U_LAND + T_B + 0.2; U_CATCH = U_SPLIT + 0.5; U_EAT = U_CATCH + 0.25   # n15c: tighter drop, NAP TIME held 1.6s")
R("HOLD = float(os.environ.get('HOLD', '0.7'))", "HOLD = float(os.environ.get('HOLD', '1.6')); V0 = float(os.environ.get('V0', '0.6'))   # n15c: opens 0.6s into the sim, guides already running")
# lead stamps clear POW
R("""STAMPS.sort(key=lambda x: x[0])   # n15: hidden 'final' slot removed (it delayed the real stamps)""", """SHV = [e[0] for e in EV if e[1] == 'shove']
STAMPS = [((max(x[0], sv + 0.6) if any(sv - 0.75 < x[0] < sv + 0.6 for sv in SHV) else x[0]), ) + x[1:] if x[1] == 'lead' else x for x in STAMPS]   # n15c: no LEADS! stamp under a POW!
sv_ = [sv for sv in SHV]
STAMPS = [((max(x[0], max([sv + 0.6 for sv in sv_ if sv - 0.75 < x[0] < sv + 0.6] or [x[0]])),) + x[1:]) if x[1] == 'lead' else x for x in STAMPS]
STAMPS.sort(key=lambda x: x[0])   # n15: hidden 'final' slot removed (it delayed the real stamps)""")
# clean 4-way split: no particle burst, a flash ring; pieces start quartered
R("""            layer(img, lambda d: [d.rectangle([px0 + math.cos(j * 0.524) * (60 + 160 * k5) - 8, py0 + math.sin(j * 0.524) * (60 + 160 * k5) - 8, px0 + math.cos(j * 0.524) * (60 + 160 * k5) + 8, py0 + math.sin(j * 0.524) * (60 + 160 * k5) + 8], fill=(220, 170, 255, int(255 * (1 - k5)))) for j in range(12)])""",
"""            layer(img, lambda d: d.ellipse([px0 - 90 - 120 * k5, py0 - 60 - 80 * k5, px0 + 90 + 120 * k5, py0 + 60 + 80 * k5], outline=(255, 255, 255, int(220 * (1 - k5))), width=8))   # n15c: one clean pop, exactly four pieces""")
R("""            if U_ < U_CATCH:
                x0, y0 = LX, LY - PRIZE.height / 2""", """            if U_ < U_CATCH:
                qi_ = NAMES.index(n); x0, y0 = LX + (-1 if qi_ % 2 == 0 else 1) * PIECE.width * 0.55, LY - PRIZE.height / 2 + (-1 if qi_ < 2 else 1) * PIECE.height * 0.45""")
# SLEEP! stamp at the eat
R("    if 0 <= t - T0 - DUR < 1.2: cur = (T0 + DUR, 'win', WIN)", "    if 0 <= t - T0 - DUR < 1.2: cur = (T0 + DUR, 'win', WIN)\n    if U_ >= U_EAT: cur = (T0 + DUR + U_EAT, 'sleep', None)   # n15c: names the melatonin as they eat it")
R("        elif cur[1] == 'block': ic, l1, l2, col = ICON[cur[2]], 'BLOCKED!', None, (110, 235, 110)", "        elif cur[1] == 'block': ic, l1, l2, col = ICON[cur[2]], 'BLOCKED!', None, (110, 235, 110)\n        elif cur[1] == 'sleep': ic, l1, l2, col = MELI, 'SLEEP!', None, PW['mel'][1]")
R("PRIZE = gummy('mel', 7); PIECE = gummy('mel', 3)", "PRIZE = gummy('mel', 7); PIECE = gummy('mel', 3); MELI = gummy('mel', 2)")
# hard-cut header
R("    if U_ >= U_EAT: img.alpha_composite(HOOK_END if U_ >= U_EAT + 0.15 else Image.blend(HOOK, HOOK_END, (U_ - U_EAT) / 0.15))", "    if U_ >= U_EAT: img.alpha_composite(HOOK_END)   # n15c: hard cut")
# pre-roll
R("for f in range(int(round(END * FPS))):", "for f in range(int(round(V0 * FPS)), int(round(END * FPS))):")
R("        if f == 0: out_ev.append((0.0, 'go_8bit'))", "        if f == int(round(V0 * FPS)): out_ev.append((round(t, 3), 'go_8bit'))")
R("wr.close(); json.dump({'events': sorted(out_ev)}, open('v85_ev.json', 'w')); print('done', round(END, 2))",
  "wr.close(); json.dump({'events': sorted((round(a - V0, 3), b) for a, b in out_ev if a >= V0 - 1e-6)}, open('v85_ev.json', 'w')); print('done', round(END - V0, 2))")
R("print('stamps', [(round(x[0], 2),) + x[1:] for x in STAMPS])", "print('stamps', [(round(x[0] - V0, 2),) + x[1:] for x in STAMPS])")
open(p,'w').write(s)
