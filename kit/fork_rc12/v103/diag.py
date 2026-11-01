import os, sys
os.environ.update(GAPDEG=sys.argv[1], SPD=sys.argv[2], ALT='6', JIT='0.2', STRN=sys.argv[3], OMV='0', SPX='1.5')
import sim103
GT = [1.4, 3.4, 5.6, 7.8, 9.8, 11.6, 13.6]; KD = ['mush', 'cre', 'mel', 'cre', 'mush', 'cre', 'mel']
for s in range(4):
    pre, fr, ev, cb, esc = sim103.place(s, GT, KD)
    br = [e[0] for e in ev if e[1] in ('break', 'smash')]
    gaps = [b - a for a, b in zip([0.0] + br, br)]
    gum = [e for e in ev if e[1] == 'gum']
    print(s, esc and round(esc, 1), 'k', fr[-1]['k'], 'maxgap', round(max(gaps), 2), 'at', round(br[gaps.index(max(gaps))], 1), [(round(e[0], 2), e[2]) for e in gum], [round(g['show'], 2) for g in pre])
