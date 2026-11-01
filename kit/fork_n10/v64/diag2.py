import collections
exec(open('r64.py').read().split("SEQ = None")[0])
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
        if min(math.hypot(q[2], q[3]) for q in path[-30:]) < 250: continue
        if any(h[0] == 'ball' and h[1] > t + TRY - 0.6 for h in hits): continue
        frozen.append(path[-1][:2]); t += TRY + GAP_T; break
print('frozen', len(frozen), t)
VR = vec_last(list(range(700000, 702000)), frozen, t)
C = collections.Counter()
for v in VR:
    if v is None: continue
    path, hits, popped = v; tesc = (popped + 1) / FPS
    if not (0.6 < tesc < 3.8): C['esc_time'] += 1; continue
    for j in range(popped + 1, len(path)):
        x, y, vx, vy = path[j]
        if x < 40 or x > 1040 or y < 260: C['off'] += 1; break
        if vy > 0 and y >= 1395:
            HX = x - GEM[0]; fl = (j - popped) / FPS
            C['HX%s fl%.1f' % ('ok' if 140 <= HX <= 870 else 'bad', fl)] += 1; break
    else: C['nocross'] += 1
print(sorted(C.items(), key=lambda kv: -kv[1])[:25])
