import json, math
J = json.load(open('plan.json')); CX, CY, RW, TH, r, RG, GAPW, OMEGA, FPS = 460, 930, 336, 18, 62, 25, 0.78, 1.35, 30
gc = lambda t: -math.pi / 2 + OMEGA * t
ad = lambda a, b: (a - b + math.pi) % (2 * math.pi) - math.pi
frozen = []; worst = {}
for k, t0, res, tend, path in J['seq']:
    prev = None; maxjump = 0; maxpen = 0; maxov = 0; maxacc = 0; pv = None
    for j, (x, y, vx, vy) in enumerate(path):
        t = t0 + (j + 1) / FPS; rad = r if (res == 'fail' or j <= J['POPF']) else RG
        d = math.hypot(x - CX, y - CY); a = math.atan2(y - CY, x - CX)
        if abs(ad(a, gc(t))) > GAPW / 2 + 0.05 and d < RW + 1: maxpen = max(maxpen, d + rad - RW)
        for fx, fy in frozen: maxov = max(maxov, 2 * r - math.hypot(x - fx, y - fy) if rad == r else 0)
        if prev:
            step = math.hypot(x - prev[0], y - prev[1]); exp = math.hypot(vx, vy) / FPS
            maxjump = max(maxjump, step / max(exp, 1))
        if pv: maxacc = max(maxacc, math.hypot(vx - pv[0], vy - pv[1] - 1500 / FPS))
        prev = (x, y); pv = (vx, vy)
    print(k, res, 'frames', len(path), 'max wall penetration px %.2f' % maxpen, 'max overlap with frozen px %.2f' % maxov, 'max step/(speed/fps) %.2f' % maxjump, 'max non-gravity dv per frame %.0f' % maxacc)
    if res == 'fail': frozen.append(path[-1][:2])
