import numpy as np, math
from PIL import Image
A='../pause/assets/'
def native(n,i=0):
    im=Image.open(A+n); im.seek(i); return np.array(im.convert('RGBA'))[5::10,5::10].copy()
NF=6
BODY=[];
ARM_X0,ARM_Y0,ARM_Y1=57,46,64
for i in range(NF):
    a=native('idle_9.gif',i)
    b=a.copy(); b[ARM_Y0:ARM_Y1, ARM_X0:]=0
    BODY.append(b)
a0=native('idle_9.gif',0)
arm=np.zeros_like(a0); arm[ARM_Y0:ARM_Y1, ARM_X0:]=a0[ARM_Y0:ARM_Y1, ARM_X0:]
PIV=(59.5,48.0)        # shoulder pivot (x,y) native
HAND=(61.5,60.5)       # fist centre
c=native('vic_victoryPose.gif',0)
sword=c[1:22,62:70].copy()       # blade + guard, tip at top
# add a short grip below the guard (dark brown)
grip=np.zeros((3,8,4),np.uint8); grip[:,3:5]=(70,45,30,255); grip[:,2]=(20,12,8,255); grip[:,5]=(20,12,8,255)
sword=np.concatenate([sword,grip],0)   # 24 x 8, hilt bottom centre at (4,23)

def assembly(blade_rel_deg=-35):
    """arm hanging straight down (+y), sword gripped at HAND with blade rotated blade_rel_deg from the arm direction."""
    S=160; can=np.zeros((S,S,4),np.uint8); off=np.array([S//2-PIV[0], S//2-PIV[1]])
    # paste sword rotated: base orientation points up (-y); we want it along arm direction (+y) then rotate by blade_rel
    sw=Image.fromarray(sword)
    ang=180+blade_rel_deg
    sw_r=rot_pixel(sw, ang, (4,23))
    hx,hy=HAND[0]+off[0], HAND[1]+off[1]
    im=Image.fromarray(can)
    im.alpha_composite(sw_r[0], (int(round(hx-sw_r[1][0])), int(round(hy-sw_r[1][1]))))
    armimg=Image.fromarray(arm)
    im.alpha_composite(armimg,(int(off[0]),int(off[1])))
    return im, (S//2, S//2)

def rot_pixel(img, deg, pivot, k=8):
    """RotSprite-ish: upscale k, rotate nearest about pivot, sample back down. returns (img, new_pivot)."""
    w,h=img.size; big=img.resize((w*k,h*k),Image.NEAREST)
    pad=max(w,h)*k*2
    can=Image.new('RGBA',(pad,pad),(0,0,0,0)); px,py=pivot[0]*k+k//2, pivot[1]*k+k//2
    can.alpha_composite(big,(int(pad/2-px),int(pad/2-py)))
    r=can.rotate(-deg, resample=Image.NEAREST, center=(pad/2,pad/2))
    a=np.array(r)[k//2::k, k//2::k]
    out=Image.fromarray(a); return out, (pad/2/k, pad/2/k)
