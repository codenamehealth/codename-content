# Oct 29 notes2 review fix (shared by #56 #59 #63 #80): stamps never stack.
# One stamp on screen at a time, >= GAP s of clear air between two stamps.
# items: (t_event, key, payload, must) ; must=True items wait their turn, others are dropped if they would wait > MAXWAIT.
GAP, DUR, MAXWAIT = 0.3, 0.8, 0.45

def schedule(items, gap=GAP, dur=DUR, maxwait=MAXWAIT, hard_end=None):
    out = []; free = -1e9
    for t, key, payload, must in sorted(items, key=lambda z: (z[0], not z[3])):
        st = max(t, free)
        if st - t > (1.2 if must else maxwait): continue
        en = st + dur
        if hard_end is not None and st >= hard_end: continue
        if hard_end is not None: en = min(en, hard_end)
        out.append((st, en, key, payload)); free = en + gap
    # a later must-item may be pushed past the next item's start: re-check order (already sequential by construction)
    return out

def active(sched, t):
    for st, en, key, payload in sched:
        if st <= t < en: return st, en, key, payload
    return None
