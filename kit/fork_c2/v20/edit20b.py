p='r20.py'; s=open(p).read()
rep=[
("T_END = T0 + len(LOG) * TD_; DUR = T_END + 3.6",
"""HOLD_K = I_TRAP; HOLD = 1.1   # dramatic hold right after the Hollow gets 1 step from winning
def tstart(k): return T0 + k * TD_ + (HOLD if k >= HOLD_K else 0)
def kt(t):
    if t < T0: return -1, 0, False
    tt = t - T0
    if tt < HOLD_K * TD_: return int(tt // TD_), (tt % TD_) / TD_, False
    tt -= HOLD_K * TD_
    if tt < HOLD: return HOLD_K, 0, True
    tt -= HOLD; return HOLD_K + int(tt // TD_), (tt % TD_) / TD_, False
T_END = tstart(len(LOG)); DUR = T_END + 3.6"""),
("""    k = int((t - T0) // TD_) if t >= T0 else -1
    u = ((t - T0) % TD_) / TD_ if k >= 0 else 0""","""    k, u, holding = kt(t)"""),
("    elif k >= 0: st, ws, lf, ev = steps[k]","    elif k >= 0: st, ws, lf, ev = steps[k]\n    if holding: ev = None"),
("abs(x[0] - (T0 + k * TD_ + 0.3 * TD_)) < 0.01 for x in events)):\n            events.append((round(T0 + k * TD_ + 0.3 * TD_, 3), 'sword_hit'))",
 "abs(x[0] - (tstart(k) + 0.3 * TD_)) < 0.01 for x in events)):\n            events.append((round(tstart(k) + 0.3 * TD_, 3), 'sword_hit'))"),
("not any(abs(e[0] - (T0 + k * TD_)) < 0.01 for e in events):\n        events.append((round(T0 + k * TD_, 3), 'tick_8bit'))",
 "not any(abs(e[0] - tstart(k)) < 0.01 for e in events):\n        events.append((round(tstart(k), 3), 'tick_8bit'))"),
("    if I_LEAD <= k <= I_TRAP: return ('1 STEP FROM WINNING...', 30, (255, 214, 60))\n    if I_TRAP < k < I_CLUTCH:",
 "    if k == 'hold': return ('1 STEP FROM WINNING...', 34, (255, 214, 60))\n    if I_TRAP <= k < I_CLUTCH:"),
("        cap, csz, ccol = caption(k if k < len(LOG) else len(LOG) - 1)","        cap, csz, ccol = caption('hold' if holding else (k if k < len(LOG) else len(LOG) - 1))"),
("        pops.append((ox, oy - 150 - 30 * u, 'BLOCKED!', 30, (255, 90, 90), 5, a))\n        if ev[3] >= 2: pops.append((ox, oy - 110 - 30 * u, f'+{ev[3]} STEPS', 24, (255, 255, 255), 4, a))",
 "        py_ = max(Y0 + 4, oy - 150 - 30 * u)   # never up into the HUD\n        pops.append((ox, py_, 'BLOCKED!', 30, (255, 90, 90), 5, a))\n        if ev[3] >= 2: pops.append((ox, py_ + 40, f'+{ev[3]} STEPS', 24, (255, 255, 255), 4, a))"),
]
for a,b in rep:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w').write(s)
