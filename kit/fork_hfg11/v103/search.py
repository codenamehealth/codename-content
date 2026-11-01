import os, sys, itertools, importlib
GT = [1.4, 3.4, 5.6, 7.8, 9.8, 11.6, 13.6]
KD = ['mush', 'cre', 'mel', 'cre', 'mush', 'cre', 'mel']
for gd, sp, strn in itertools.product([110], [1300], [25]):
    os.environ.update(GAPDEG=str(gd), SPD=str(sp), ALT='6', JIT='0.2', STRN=str(strn), OMV='0', SPX='1.5')
    import sim103; importlib.reload(sim103)
    ok = []
    for s in range(int(sys.argv[1]), int(sys.argv[2])):
        pre, fr, ev, cb, esc = sim103.place(s, GT, KD)
        if esc is None or not (13.0 <= esc <= 17.5): continue
        br = [e[0] for e in ev if e[1] in ('break', 'smash')]
        gaps = [b - a for a, b in zip([0.0] + br, br)]
        gum = [e for e in ev if e[1] == 'gum']
        delays = [round(e[0] - g['show'], 2) for e, g in zip(gum, pre)]
        if max(gaps) > 1.5 or len(gum) < 5 or min(delays) < 0.5: continue
        ok.append((s, round(esc, 1), round(max(gaps), 2), [(round(e[0], 1), e[2]) for e in gum], sum(e[1] == 'smash' for e in ev)))
    print(gd, sp, strn, len(ok), ok[:4], flush=True)
