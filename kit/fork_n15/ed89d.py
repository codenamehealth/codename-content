p='r89.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("END = T_WIN + float(os.environ.get('HOLD', '0.7'))", "END = T_WIN + float(os.environ.get('HOLD', '1.2'))   # n15c: JOY WINS! held 1.2s")
R("    if e[1] == 'gum' and e[3] != 'mush': SEV.append((e[0], 'gum', e[2], PWS[e[3]][0], PWS[e[3]][1], 0.9))\n    if e[1] == 'dash': SEV.append((e[0], 'gum', e[2], 'SPEED!', PWS['mush'][1], DASH_T + 0.35))   # SPEED fires on the first dash frame, held through it",
  "    if e[1] == 'gum' and e[3] != 'mush': SEV.append((e[0], 'gum', e[2], PWS[e[3]][0], PWS[e[3]][1], 0.9))\n    if e[1] == 'gum' and e[3] == 'mush':   # n15c: SPEED! on the pickup frame, held through the dash\n        dd_ = [x for x in EV if x[1] == 'dash' and x[2] == e[2]]\n        SEV.append((e[0], 'gum', e[2], 'SPEED!', PWS['mush'][1], (dd_[0][0] + DASH_T + 0.3 - e[0]) if dd_ else 0.9))")
R("""                sx_, sy_ = s['x'], max(SY + 140, min(s['y'], 1500 - 50)); sx_ = max(120, min((887 if sy_ + 50 > 1110 else 1025) - 50, sx_))
                s = dict(s, x=sx_, y=sy_)
                for k in range(3):""", """                if t - s['out'] > 1.2: continue   # n15c: ripples fade where they went in; no parked heads
                for k in range(3):""")
R("""                u = ((t - s['out']) * 0.8 + k / 3) % 1.0; rr_ = 20 + 60 * u
                    d.ellipse([s['x'] - rr_, s['y'] - rr_ * 0.5, s['x'] + rr_, s['y'] + rr_ * 0.5], outline=(230, 250, 255, int(200 * (1 - u))), width=3)""",
"""                u = ((t - s['out']) * 0.8 + k / 3) % 1.0; rr_ = 20 + 60 * u
                    d.ellipse([s['x'] - rr_, s['y'] - rr_ * 0.5, s['x'] + rr_, s['y'] + rr_ * 0.5], outline=(230, 250, 255, int(200 * (1 - u) * max(0.0, 1 - (t - s['out']) / 1.2))), width=3)""") if False else None
R("""            else:
                hd = HEAD[n]; bob = int(5 * math.sin(t * 4 + x))
                y = max(SY + 140, min(y, 1500 - 50)); x = max(70 + 50, min((887 if y + 50 > 1110 else 1025) - 50, x))   # rc10: never under the stamp slot   # bobbing heads stay in the zone
                img.alpha_composite(hd, (int(x - hd.width / 2), int(y - hd.height / 2 + bob)))
            continue""", """            continue   # n15c: no floating heads after they sink (the IN/OUT row shows OUT)""")
R("""    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if s['out'] is not None:""", """    for n in sorted(NAMES, key=lambda n: st[n]['y']):
        s = st[n]; x, y = s['x'], s['y']
        if WIN and t >= T_WIN and s['out'] is None: continue   # n15c: the win zoom replaces the in-game sprite (no second Joy)
        if s['out'] is not None:""")
open(p,'w').write(s)
