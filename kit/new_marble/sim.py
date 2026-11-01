import pymunk, math, random, json, sys
W=1080; R=56
FIN=6200
def build(seed):
    rng=random.Random(seed)
    sp=pymunk.Space(); sp.gravity=(0,2600)
    st=sp.static_body; statics=[]
    def seg(a,b,r=12,el=0.4,kind='wall'):
        s=pymunk.Segment(st,a,b,r); s.elasticity=el; s.friction=0.5; sp.add(s); statics.append((kind,a,b,r))
    def peg(x,y,r=16,el=0.6,kind='peg'):
        c=pymunk.Circle(st,r,(x,y)); c.elasticity=el; c.friction=0.3; sp.add(c); statics.append((kind,(x,y),r))
    seg((40,0),(40,FIN+600),14); seg((1040,0),(1040,FIN+600),14)
    # start shelf (gate is a separate body removed at GO)
    seg((40,470),(1040,470),10,kind='shelf_hidden')
    # S1 pegboard
    for r_ in range(7):
        y=700+r_*160
        xs_=[240,440,640,840] if r_%2==0 else [340,540,740]
        for x in xs_: peg(x+rng.uniform(-8,8),y)
    # S2 zigzag ramps
    y=1950
    for k in range(4):
        if k%2==0: seg((40,y),(820,y+260),14,0.2,'ramp')
        else: seg((1040,y),(260,y+260),14,0.2,'ramp')
        y+=400
    # S3 gummy bumpers
    bumps=[]
    for (x,y_) in [(300,3450),(780,3450),(540,3700),(290,3950),(790,3950),(540,4200)]:
        peg(x,y_,62,1.05,'bump'); bumps.append((x,y_))
    # S4 spinners (kinematic)
    spin=[]
    for (x,y_,w_) in [(300,4600,2.6),(780,4600,-2.6),(540,4950,3.0)]:
        b=pymunk.Body(body_type=pymunk.Body.KINEMATIC); b.position=(x,y_); b.angular_velocity=w_
        s=pymunk.Segment(b,(-190,0),(190,0),16); s.elasticity=0.6; s.friction=0.5; sp.add(b,s); spin.append(b)
    # S5 pegs then funnel to the finish
    for r_ in range(5):
        y=5300+r_*130
        xs_=[240,440,640,840] if r_%2==0 else [340,540,740]
        for x in xs_: peg(x+rng.uniform(-10,10),y,14)
    seg((40,5900),(470,6080),14,0.2,'ramp'); seg((1040,5900),(610,6080),14,0.2,'ramp')
    seg((470,6080),(470,6150),14,0.2,'ramp'); seg((610,6080),(610,6150),14,0.2,'ramp')
    # catch floor after finish
    seg((40,6560),(1040,6560),14,0.1,'floor')
    marbles=[]
    xs=[200,420,640,860]; rng.shuffle(xs)
    for i in range(4):
        b=pymunk.Body(1,pymunk.moment_for_circle(1,0,R)); b.position=(xs[i],470-R-12)
        c=pymunk.Circle(b,R); c.elasticity=0.55; c.friction=0.5; sp.add(b,c); marbles.append(b)
    return sp,statics,spin,marbles,bumps,xs
def run(seed,T_GO=3.4,FPS=30,TMAX=30):
    sp,statics,spin,marbles,bumps,xs=build(seed)
    shelf=[s for s in sp.shapes if isinstance(s,pymunk.Segment) and s.body.body_type==pymunk.Body.STATIC and s.a==(40,470)][0]
    frames=[]; fin={}; stuck=[0]*4; rng=random.Random(seed*7+1)
    sub=8; dt=1/(FPS*sub); t=0.0
    removed=False
    nf=int(TMAX*FPS)
    for f in range(nf):
        t=f/FPS
        if t>=T_GO and not removed:
            sp.remove(shelf); removed=True
            for b in marbles: b.apply_impulse_at_local_point((rng.uniform(-60,60),0))
        for _ in range(sub):
            sp.step(dt)
        for i,b in enumerate(marbles):
            if b.position.y>FIN+20 and i not in fin: fin[i]=t
            if removed and i not in fin:
                if b.velocity.length<25: stuck[i]+=1
                else: stuck[i]=0
                if stuck[i]>15: print("RESCUE",i,round(t,2),int(b.position.x),int(b.position.y),file=sys.stderr); b.velocity=((540-b.position.x)*1.2+rng.uniform(-80,80),-300); stuck[i]=0
            # keep marbles inside track
            if b.position.x<40+R: b.position=(40+R+1,b.position.y)
            if b.position.x>1040-R: b.position=(1040-R-1,b.position.y)
        frames.append([(b.position.x,b.position.y,b.angle) for b in marbles]+[(s.angle,) for s in spin])
        if len(fin)==4 and t>max(fin.values())+1.0: break
    return frames,fin,statics,bumps,xs
if __name__=='__main__':
    best=None
    for seed in range(int(sys.argv[1]),int(sys.argv[2])):
        frames,fin,statics,bumps,xs=run(seed)
        if len(fin)<4: print(seed,'dnf',fin); continue
        # lead changes during the race
        lead=[];
        for fr in frames[int(3.4*30):int(min(fin.values())*30)]:
            ys=[p[1] for p in fr[:4]]; lead.append(max(range(4),key=lambda i:ys[i]))
        ch=sum(1 for a,b in zip(lead,lead[1:]) if a!=b)
        w=min(fin,key=fin.get); gap=sorted(fin.values())[1]-fin[w]
        print(seed,'win',w,'t',round(fin[w],2),'last',round(max(fin.values()),2),'changes',ch,'gap',round(gap,2))
