import sys, os
sys.argv=['r81.py','181']
src=open('r81.py').read(); src=src[:src.index('# ---- static assets for render')]
exec(compile(src,'r81','exec'))
print('F_OUT', FR[-1][1], 'T_OUT', T_OUT)
FXB, FYB = EX_C[1] * C + C / 2, EX_R * C + 8
for r in range(15, 21):
    print(r, [round(DSL[r*FINE+2, c*FINE+2],1) if passable(r,c) else '#' for c in range(COLS)])
