import pymunk, numpy as np, math, json, sys
from PIL import Image
from scipy.spatial import ConvexHull
FILES={'ACV':'acv_gummy_single.png','CREATINE':'cre_gummy_single.png','MUSHROOM':'mush_gummy_single.png','MELATONIN':'mel_gummy_red.png'}
GW=170
def load(name):
    im=Image.open('../gummy/'+FILES[name]).convert('RGBA'); im=im.crop(im.getbbox())
    im=im.resize((GW,int(im.height*GW/im.width)),Image.LANCZOS)
    a=np.array(im)[:,:,3]>120
    ys,xs=np.nonzero(a); pts=np.stack([xs,ys],1).astype(float)
    hull=ConvexHull(pts); v=pts[hull.vertices]
    # simplify to <= 16 points
    if len(v)>16: v=v[np.linspace(0,len(v)-1,16).astype(int)]
    v=v-np.array([im.width/2,im.height/2])
    h=im.height
    # squish: flatten the rounded top and bottom so gummies can stack
    v[:,1]=np.clip(v[:,1],-h/2+0.16*h,h/2-0.06*h)
    hull=ConvexHull(v); v=v[hull.vertices]
    return im,[tuple(p) for p in v]
SHAPES={n:load(n) for n in FILES}
PED_Y=1650; PED_L,PED_R=400,680
def run(seq,offs,drop_times,fatal_idx,fatal_hold,FPS=30,DUR=13.0,gravity=2200,fric=0.9,fv=0,fm=1.0):
    sp=pymunk.Space(); sp.gravity=(0,gravity); sp.iterations=40; sp.damping=0.7
    st=sp.static_body
    for a,b in [((PED_L,PED_Y),(PED_R,PED_Y)),((PED_L,PED_Y),(PED_L,PED_Y+260)),((PED_R,PED_Y),(PED_R,PED_Y+260)),((-200,1880),(1280,1880)),((1078,-400),(1078,1880)),((2,-400),(2,1880))]:
        s=pymunk.Segment(st,a,b,6); s.friction=0.9; s.elasticity=0.1; sp.add(s)
    bodies=[None]*len(seq); out=[]; spawned=[False]*len(seq)
    sub=10; dt=1/(FPS*sub)
    for f in range(int(DUR*FPS)):
        t=f/FPS
        for i,(name,tt) in enumerate(zip(seq,drop_times)):
            if not spawned[i] and t>=tt:
                im,verts=SHAPES[name]
                # spawn 260px above the current top of the stack
                top=min([b.position.y-90 for b in bodies if b is not None]+[PED_Y])
                m=1.0; mom=pymunk.moment_for_poly(m,verts)
                b=pymunk.Body(m,mom); b.position=(540+offs[i],top-150)
                s=pymunk.Poly(b,verts,radius=2); s.friction=fric; s.elasticity=0.15; sp.add(b,s)
                if i==fatal_idx: b.body_type=pymunk.Body.KINEMATIC
                bodies[i]=b; spawned[i]=True
        if fatal_idx is not None and bodies[fatal_idx] is not None and bodies[fatal_idx].body_type==pymunk.Body.KINEMATIC and t>=drop_times[fatal_idx]+fatal_hold:
            b=bodies[fatal_idx]; b.body_type=pymunk.Body.DYNAMIC; b.mass=fm; b.moment=pymunk.moment_for_poly(fm,SHAPES[seq[fatal_idx]][1]); b.velocity=(0,fv)
        if not getattr(sp,'_broke',False) and t>=(drop_times[-1]+fatal_hold) and any(b is not None and abs(b.angle)>math.radians(15) for b in bodies[:-1]):
            sp._broke=True
            for b in bodies:
                if b is None: continue
                for sh in b.shapes: sh.friction=0.25; sh.elasticity=0.35
        for _ in range(sub): sp.step(dt)
        out.append([(b.position.x,b.position.y,b.angle) if b is not None else None for b in bodies])
    return out
def fallen(fr): return sum(1 for p in fr if p is not None and p[1]>PED_Y+40)
if __name__=='__main__':
    seq=['ACV','CREATINE','MUSHROOM','MELATONIN','ACV','MUSHROOM','CREATINE','MELATONIN']
    import itertools
    lean=float(sys.argv[1]) if len(sys.argv)>1 else 10
    fat=float(sys.argv[2]) if len(sys.argv)>2 else 60
    offs=[0,lean,-lean*0.5,lean*1.2,-lean*0.3,lean*1.6,lean*1.2,fat]
    times=[0.6,1.5,2.4,3.3,4.2,5.1,6.0,6.9]
    out=run(seq,offs,times,7,1.6)
    for tt in [5.0,6.8,8.4,9.0,10.0,12.9]:
        fr=out[int(tt*30)]; print(tt,'fallen',fallen(fr),[ (int(p[0]),int(p[1]),round(math.degrees(p[2]))) for p in fr if p])
