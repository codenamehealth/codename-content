import cv2, numpy as np, json, sys
d='n03'
f1=cv2.imread(f'{d}/f_0001.png')
T={'cyrus':(141,563),'ray':(289,567),'joy':(500,572),'cleo':(660,568)}
S=55; ins=8
tm={k:f1[y+ins:y+S-ins, x+ins:x+S-ins] for k,(x,y) in T.items()}
out={k:[] for k in T}
for i in range(1,544):
    f=cv2.imread(f'{d}/f_{i:04d}.png')
    reg=f[460:1440,20:1060]
    for k,t in tm.items():
        r=cv2.matchTemplate(reg,t,cv2.TM_CCOEFF_NORMED)
        _,mx,_,loc=cv2.minMaxLoc(r)
        out[k].append((loc[0]+20-ins,loc[1]+460-ins,round(mx,3)))
json.dump(out,open('track.json','w'))
