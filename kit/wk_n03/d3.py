import sys, os, collections
sys.argv=['n03b.py','x']
src=open('n03b.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
C_=collections.Counter(); wins=[]
for sd in range(1, int(os.environ.get('N','200'))):
    X, fr, ev, gum, B, wh = sim(sd)
    w=[e for e in ev if e[1]=='win']
    C_['win_'+(w[0][2] if w else 'none')]+=1
    if w: wins.append(round(w[0][0],1))
    C_['gum']+= gum['t'] is not None
    C_['exitbroke']+= B['exit']['broke'] is not None
print(C_, sorted(wins)[:30])
