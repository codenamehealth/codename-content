def idle_mask(vx, min_idle=10, min_gap=6, thr=25):
    """Per-frame idle flag with no short flickers: slow stretches shorter than min_idle stay in the run cycle,
    and run gaps shorter than min_gap between two idle stretches become idle."""
    n = len(vx); slow = [abs(v) < thr for v in vx]; m = [False] * n; i = 0
    while i < n:
        if slow[i]:
            j = i
            while j < n and slow[j]: j += 1
            if j - i >= min_idle:
                for k in range(i, j): m[k] = True
            i = j
        else: i += 1
    i = 0
    while i < n:
        if not m[i]:
            j = i
            while j < n and not m[j]: j += 1
            if i > 0 and j < n and j - i < min_gap:
                for k in range(i, j): m[k] = True
            i = j
        else: i += 1
    return m
def runs(m):
    out = []; c = 0; cur = None
    for v in m:
        if v == cur: c += 1
        else:
            if cur is not None: out.append((cur, c))
            cur, c = v, 1
    out.append((cur, c)); return out
