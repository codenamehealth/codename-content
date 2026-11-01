import sys, os, collections
src = open('r64.py').read().split("SEQ = None")[0]
exec(src)
# tries 1-3 for base 1
frozen = []; t = T0
for i in range(3):
    for s in range(1000 + i * 100, 1000 + i * 100 + 99):
        res = run_attempt(s, frozen, t)
        if res is None: continue
        path, hits, popped = res
        bounces = [h[1] for h in hits if h[0] in ('wall', 'cap', 'ball')]
        near = [h[1] for h in hits if h[0] == 'cap' or (h[0] == 'wall' and h[2] < 0.10)]
        if popped is not None or not fail_ok(path, hits) or len(bounces) < 4: continue
        if i == 2 and not any(1.0 < x - t < 3.0 for x in near): continue
        if i < 2 and near: continue
        frozen.append(path[-1][:2]); t += TRY + GAP_T; break
print('frozen', frozen, t)
VR = vec_last(list(range(500000, 501000)), frozen, t)
C = collections.Counter(); ex = []
for v in VR:
    if v is None: C['noesc'] += 1; continue
    path, hits, popped = v; tesc = (popped + 1) / FPS
    if not (1.0 < tesc < 3.6): C['esc_time'] += 1; continue
    # catch diag
    reason = 'nocross'
    for j in range(popped + 1, len(path)):
        x, y, vx, vy = path[j]
        if x < 40 or x > 1040 or y < 260: reason = 'offscreen'; break
        if vy > 0 and y >= 1395:
            HX, HY = x - GEM[0], y - GEM[1]
            if not (140 <= HX <= 850): reason = 'hx %d' % (HX // 100 * 100); break
            if not (1440 <= HY <= 1510): reason = 'hy'; break
            if not (0.25 <= (j - popped) / FPS <= 1.3): reason = 'flight %.2f' % ((j - popped) / FPS); break
            reason = 'clearance'; ex.append((round(path[popped][0]), round(path[popped][1]), round(HX), round(HY))); break
    C[reason] += 1
print(C.most_common(20)); print(ex[:10])
