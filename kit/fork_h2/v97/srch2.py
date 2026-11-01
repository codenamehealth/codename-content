import sys
src = open('r97.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv = ['r97.py', '0']
g = {'__name__': 'an'}; exec(compile(src, 'r97', 'exec'), g)
G4, T_END, OFF = g['G4'], g['T_END'], g['OFF']
def check(seed, verbose=False):
    fr, ev, fin, ld = g['sim'](seed)
    srt = sorted(fin.values(), reverse=True)
    if srt[0] - srt[1] != 1 or len(ld) < 4: return None
    win = max(G4, key=lambda k: fin[k])
    catches = sorted((te, k) for (te, k, kind, ix) in ev if kind != 'slime')
    slimes = sorted((te, k) for (te, k, kind, ix) in ev if kind == 'slime')
    wc = [te for te, k in catches if k == win][-1]
    if not (T_END - 1.0 <= wc <= T_END - 0.3): return None
    # no other catch within 0.35s of the deciding catch
    if any(abs(te - wc) < 0.35 for te, k in catches if not (te == wc and k == win)): return None
    sc = {k: 0 for k in G4}
    for te, k in catches:
        if te >= wc: break
        sc[k] += 1
    mo = max(v for k, v in sc.items() if k != win)
    if sc[win] != mo: return None            # tied for the lead right before the deciding catch
    sc1 = {k: 0 for k in G4}
    for te, k in catches:
        if te >= T_END - 1.0: break
        sc1[k] += 1
    m1 = max(sc1.values())
    if sum(1 for v in sc1.values() if v == m1) < 2: return None   # still tied going into the last second
    if not any(te < T_END - 2.0 for te, k in slimes): return None  # at least one slime stun on screen early
    return dict(seed=seed, fin=fin, win=win, catch_before_buzzer=round(T_END - wc, 2), sc_at_last_sec=sc1, leads=len(ld),
                slimes=[(round(te - OFF, 2), k) for te, k in slimes], last=[(round(te - OFF, 2), k) for te, k in catches if te > T_END - 2.0])
import os
lo, hi = int(os.environ['LO']), int(os.environ['HI'])
for seed in range(lo, hi):
    r = check(seed)
    if r: print(r, flush=True)
