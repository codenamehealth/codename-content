# Guide battle sim, recut: 4 armies of guides (Hollow never in it), 2x units, charge from t=0,
# typed gummy powers (SPEC 12): mush SPEED, cre STRONG, mel SLEEP (everyone else stops ~1.2s), acv SHIELD. No gold.
import numpy as np, math, random, sys
NAMES = ['joy', 'ray', 'cleo', 'cyrus']            # i converts the next living army: joy>ray>cleo>cyrus>joy
NT = 4; FPS = 30
XMIN, XMAX, XNOTCH = 122, 972, 836                # unit centre bounds (2x sprite body ~90px wide)
YMIN, YMAX, YNOTCH = 740, 1492, 1110              # feet bounds (sprite ~130px tall above the feet)
POWDUR = {'mush': 2.5, 'cre': 2.5, 'acv': 2.5, 'mel': 1.2}
import os
R_CONV, R_STRONG = float(os.environ.get('RC', 38)), 84
PLAY = float(os.environ.get('PLAY', 1.45))      # n13b: render plays the sim at this speed; shove timings are in sim seconds so they read ~1s on screen
SHOVE_T, SHOVE_IMP, SHOVE_GAP, SHOVE_MAX, SHOVE_REACH = 1.0 * PLAY, 0.23 * PLAY, 0.6 * PLAY, 3, 150
BR = os.environ.get('BR'); BR = None if BR is None else int(BR); BRT = 10.6
CD2, RC2 = float(os.environ.get('CD2', 0.8)), float(os.environ.get('RC2', 46))   # after the creatine window: quicker conversions (more action, same running speed)   # n13b: creatine shoves (plant ~1s each, max 3)
CD = float(os.environ.get('CD', 1.5)); SPK = float(os.environ.get('SPK', 0.8))
def sim(seed, N=10, dur=34.0, gtimes=(3.2, 7.4, 11.6, 15.6)):
    rnd = random.Random(seed); rs = np.random.RandomState(seed)
    n = NT * N; T = np.repeat(np.arange(NT), N)
    cx = np.array([300, 800, 760, 300]); cy = np.array([860, 860, 1380, 1380])
    X = cx[T] + rs.uniform(-110, 110, n); Y = cy[T] + rs.uniform(-90, 90, n)
    VX = np.zeros(n); VY = np.zeros(n); SP = rs.uniform(150, 200, n) * SPK; PH = rs.uniform(0, 6.3, n)
    FL = np.full(n, -9.0); LC = np.full(n, -9.0); DIST = np.zeros(n)
    PLT = np.full(n, -9.0); PLJ = np.full(n, -1); PLD = np.zeros(n); KB = np.zeros((n, 2)); KT = np.full(n, -9.0); shoves = []; lastsh = -9.0; nsh = {}
    kinds = ['mush', 'acv', 'mel', 'cre']; rnd.shuffle(kinds)
    sched = [(gt + rnd.uniform(-0.4, 0.4), k) for gt, k in zip(gtimes, kinds)]
    eff = []                     # (team, kind, t0)
    gums = []; frames = []; events = []; leaders = []; end = None; outs = []
    brd = False
    for f in range(int(dur * FPS)):
        t = f / FPS; dt = 1 / FPS
        if BR is not None and not brd and t >= BRT: PH = PH + np.random.RandomState(BR).uniform(-1.2, 1.2, n); brd = True   # branch after the creatine window
        while sched and t >= sched[0][0]:
            gt, k = sched.pop(0)
            # drop it between the two biggest armies so it gets picked up
            cnt = np.bincount(T, minlength=NT); live = [a for a in range(NT) if cnt[a] > 0]
            mx_, my_ = X.mean(), Y.mean()
            gx = min(max(mx_ + rnd.uniform(-160, 160), XMIN + 40), XNOTCH - 40); gy = min(max(my_ + rnd.uniform(-140, 140), YMIN + 30), YMAX - 30)
            gums.append(dict(x=gx, y=gy, k=k, t0=t))
        cnt = np.bincount(T, minlength=NT); alive = cnt > 0
        def act(kind, dur_):
            return [(a, t0) for (a, k, t0) in eff if k == kind and 0 <= t - t0 < dur_]
        sh = np.zeros(NT, bool); spd = np.ones(NT); strong = np.zeros(NT, bool); asleep = np.zeros(NT, bool)
        for a, _ in act('acv', POWDUR['acv']): sh[a] = True
        for a, _ in act('mush', POWDUR['mush']): spd[a] = 1.9
        for a, _ in act('cre', POWDUR['cre']): strong[a] = True
        for a, _ in act('mel', POWDUR['mel']): asleep[np.arange(NT) != a] = True
        if end is None:
            nxt = [-1] * NT
            for a in range(NT):
                for s in range(1, NT):
                    if alive[(a + s) % NT]: nxt[a] = (a + s) % NT; break
            B = np.zeros((NT, NT), bool)
            for a in range(NT):
                b = nxt[a]
                if b >= 0 and b != a and alive[a]:
                    B[a, b] = (cnt[a] >= cnt[b]) if alive.sum() == 2 else True
            dx = X[None, :] - X[:, None]; dy = Y[None, :] - Y[:, None]; D = np.hypot(dx, dy) + 1e-6
            BM = B[T[:, None], T[None, :]]                       # i beats j
            prey = BM & ~sh[T][None, :]
            pd = np.where(prey, D, np.inf); pi = pd.argmin(1); pv = pd.min(1)
            qd = np.where(BM.T, D, np.inf); qi = qd.argmin(1); qv = qd.min(1)
            AX = np.zeros(n); AY = np.zeros(n)
            has = np.isfinite(pv); AX[has] += dx[has, pi[has]] / pv[has]; AY[has] += dy[has, pi[has]] / pv[has]
            fl = np.isfinite(qv) & (qv < 260) & ~sh[T]
            k_ = 1.3 * (1 - qv[fl] / 260); AX[fl] -= k_ * dx[fl, qi[fl]] / qv[fl]; AY[fl] -= k_ * dy[fl, qi[fl]] / qv[fl]
            for g in gums:
                gdx, gdy = g['x'] - X, g['y'] - Y; gd = np.hypot(gdx, gdy) + 1
                m = gd < 340; AX[m] += 1.1 * gdx[m] / gd[m]; AY[m] += 1.1 * gdy[m] / gd[m]
            a_ = t * 0.9 + PH; AX += 0.35 * np.cos(a_); AY += 0.35 * np.sin(a_ * 1.3)
            L = np.hypot(AX, AY) + 1e-6; sp = SP * spd[T]
            VX += (AX / L * sp - VX) * 0.12; VY += (AY / L * sp - VY) * 0.12
            mv = ~asleep[T] & ~(t - PLT < SHOVE_T)
            VX[~mv] = 0; VY[~mv] = 0
            kb = np.clip(1 - (t - KT) / 0.3, 0, 1)[:, None] * KB        # knocked-back victims slide away, easing out
            nx = X + VX * dt + kb[:, 0] * dt; ny = Y + VY * dt + kb[:, 1] * dt
            ny = np.clip(ny, YMIN, YMAX); nx = np.clip(nx, XMIN, np.where(ny > YNOTCH, XNOTCH, XMAX))
            DIST += np.hypot(nx - X, ny - Y); X, Y = nx, ny
            # separation within an army
            dx = X[None, :] - X[:, None]; dy = Y[None, :] - Y[:, None]; D = np.hypot(dx, dy) + 1e-6
            same = (T[:, None] == T[None, :]) & (D < 58) & ~np.eye(n, dtype=bool)
            p = np.where(same, (58 - D) / 2, 0)
            X -= (p * dx / D).sum(1) * 0.5; Y -= (p * dy / D).sum(1) * 0.5
            Y = np.clip(Y, YMIN, YMAX); X = np.clip(X, XMIN, np.where(Y > YNOTCH, XNOTCH, XMAX))
            # conversions
            D = np.hypot(X[None, :] - X[:, None], Y[None, :] - Y[:, None])
            R = np.where(strong[T], R_STRONG, R_CONV if t < BRT else RC2)
            # creatine (n13b): the strong army converts only by clear shoves, and can't be converted while strong
            for a in np.where(strong)[0]:
                for i in np.where((T == a) & (t - PLT >= SHOVE_T))[0]:
                    if nsh.get(a, 0) >= SHOVE_MAX or t - lastsh < SHOVE_GAP: break
                    busy = set(int(PLJ[k]) for k in range(n) if t - PLT[k] < SHOVE_T)
                    cand = [j for j in np.where(BM[i] & (D[i] < R_STRONG + 30) & ~sh[T])[0] if j not in busy and t - PLT[j] >= SHOVE_T]
                    if not cand: continue
                    j = min(cand, key=lambda j: D[i, j]); PLT[i] = t; PLJ[i] = j; PLD[i] = 1 if X[j] >= X[i] else -1
                    lastsh = t; nsh[a] = nsh.get(a, 0) + 1; shoves.append([round(t, 3), int(i), int(j), int(a), None])
            for sv in shoves:
                if sv[4] is None and t - sv[0] >= SHOVE_IMP:
                    i, j, a = sv[1], sv[2], sv[3]
                    if np.hypot(X[i] - X[j], Y[i] - Y[j]) < SHOVE_REACH and T[i] == a and T[j] != a:
                        ux, uy = X[j] - X[i], Y[j] - Y[i]; L_ = math.hypot(ux, uy) + 1e-6
                        KB[j] = (ux / L_ * 380, uy / L_ * 140); KT[j] = t
                        events.append((round(t, 3), 'conv', float(X[j]), float(Y[j]), a, True)); events.append((round(t, 3), 'shove', float(X[j]), float(Y[j]), a, int(i)))
                        T[j] = a; FL[j] = t; LC[j] = t; sv[4] = True
                    else: sv[4] = False
            C = BM & (D < R[:, None]) & ~strong[T][:, None] & ~strong[T][None, :] & ~sh[T][None, :] & ~asleep[T][:, None] & (t - LC > (CD if t < BRT else CD2))[:, None] & (t - PLT >= SHOVE_T)[:, None] & (t - PLT >= SHOVE_T)[None, :]
            for j in np.where(C.any(0) & (t - FL > 0.4))[0]:
                ii = np.where(C[:, j])[0]
                if len(ii) == 0: continue
                i = ii[0]
                if T[j] != T[i] and B[T[i], T[j]]:
                    events.append((round(t, 3), 'conv', float(X[j]), float(Y[j]), int(T[i]), bool(strong[T[i]])))
                    T[j] = T[i]; FL[j] = t; LC[i] = t; LC[j] = t; C[i, :] = False
            for g in list(gums):
                gd = np.hypot(g['x'] - X, g['y'] - Y); j = int(gd.argmin())
                if gd[j] < 52:
                    gums.remove(g); a = int(T[j]); eff.append((a, g['k'], t)); events.append((round(t, 3), 'gum', g['x'], g['y'], a, g['k']))
            cnt2 = np.bincount(T, minlength=NT)
            for a in range(NT):
                if cnt[a] > 0 and cnt2[a] == 0: outs.append((round(t, 3), a)); events.append((round(t, 3), 'out', 0, 0, a, None))
            mx = cnt2.max(); ld = [a for a in range(NT) if cnt2[a] == mx]
            if len(ld) == 1 and (not leaders or leaders[-1] != ld[0]): leaders.append(ld[0])
            if mx == n: end = (t, ld[0])
        frames.append(dict(PLT=PLT.copy(), PLD=PLD.copy(), T=T.copy(), X=X.copy(), Y=Y.copy(), VX=VX.copy(), VY=VY.copy(), D=DIST.copy(), FL=FL.copy(),
                           gums=[dict(g) for g in gums], sh=sh.copy(), spd=spd.copy(), strong=strong.copy(), asleep=asleep.copy()))
        if end and t > end[0] + 1.5: break
    return frames, events, end, leaders, outs
def score(seed):
    fr, ev, end, ld, outs = sim(seed)
    if not end or NAMES[end[1]] != 'ray': return None
    tw = end[0]; gpick = [e for e in ev if e[1] == 'gum']
    if not (20.0 < tw < 22.6) or len(gpick) < 4 or len(ld) < 4 or len(outs) != 3: return None
    ot = [o[0] for o in outs]
    if min(b - a for a, b in zip(ot, ot[1:])) < 1.8 or ot[0] < 7: return None
    return round(tw, 2), [(o[0], NAMES[o[1]]) for o in outs], [(e[0], NAMES[e[4]], e[5]) for e in gpick], [NAMES[k] for k in ld]
if __name__ == '__main__':
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        r = score(seed)
        if r: print(seed, r, flush=True)
