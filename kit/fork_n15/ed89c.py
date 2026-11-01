p='r89.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("    gums = []; gsched = list(zip(GSCHED, GKINDS))", "    gums = []; gsched = list(zip(GSCHED, GKINDS)); G = {'next': 0.0}   # n15c: one action at a time (strikes >= ~1s apart, never right on a splash)")
R("        events.append((t, 'shove', n, v))\n", "        events.append((t, 'shove', n, v)); G['next'] = max(G['next'], t + 0.6)\n")
R("                            else: events.append((t, 'whiff', n, v))", "                            else: events.append((t, 'whiff', n, v)); G['next'] = max(G['next'], t + 0.6)")
R("            if abs(t - gt) < dt / 2 and len(alive) > 1:\n                gsched[gi_]", "            if False: pass\n            if due and len(alive) > 1:\n                gsched[gi_]") if False else None
R("                who = 'cyrus' if gk == 'mush' and 'cyrus' in cand else rnd.choice(cand)", "                who = 'cyrus' if gk == 'mush' and 'cyrus' in cand else ('ray' if gk == 'cre' and 'ray' in cand else rnd.choice(cand))   # n15c: Rayleigh opens with STRENGTH")
R("                    if s['buff'] == 'mush' and not s['dashed'] and tg and t - s['bt'] > 0.5:", "                    if s['buff'] == 'mush' and not s['dashed'] and tg and t - s['bt'] > 0.5 and t >= G['next'] and not any(0 <= t - ag[m]['atk'] < ATK_WIND + 0.1 for m in alive if m != n):")
R("                            s['dash'] = t; s['dashed'] = True;", "                            G['next'] = t + DASH_T + SKID_T + 0.3; s['dash'] = t; s['dashed'] = True;")
R("                    if tg and t > s['cd']:", "                    if tg and t > s['cd'] and t >= G['next'] and not any(0 <= t - ag[m]['atk'] < ATK_WIND + 0.1 for m in alive if m != n) and not any(0 <= t - ag[m]['dash'] < DASH_T for m in alive):")
R("                    s['out'] = t; outs.append((n, t)); events.append((t, 'splash', n, None))", "                    s['out'] = t; outs.append((n, t)); events.append((t, 'splash', n, None)); G['next'] = max(G['next'], t + 0.6)")
# score: opening beat
R("    if outs[-1][0] != 'cyrus': return None", """    if outs[-1][0] != 'cyrus': return None
    act = [e for e in ev if e[1] in ('wind', 'shove', 'whiff', 'dash')]   # n15c: the opener is one beat: Rayleigh eats STRENGTH, plants, strikes Cyrus
    g0 = [e for e in ev if e[1] == 'gum'][0]
    if g0[2] != 'ray' or g0[3] != 'cre' or not act or act[0][1] != 'wind' or act[0][2] != 'ray' or act[0][3] != 'cyrus' or act[0][0] < g0[0]: return None
    if len(act) < 2 or act[1][1] != 'shove' or act[1][2] != 'ray': return None
    if any(e[1] == 'whiff' for e in ev): return None""")
open(p,'w').write(s)
