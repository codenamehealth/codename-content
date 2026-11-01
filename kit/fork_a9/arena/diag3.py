import sys
lo,hi=int(sys.argv[1]),int(sys.argv[2]); sys.argv=['x','none']
src=open('render_arena.py').read().split("if __name__ == '__main__' and sys.argv[1] == 'search':")[0]
exec(src)
for s in range(lo,hi):
    fr,ev,pts,ld=sim(s)
    late=[(round(e[0],1),e[2]) for e in ev if e[1]=='lead' and e[0]>T0+DUR-6]
    print(s, sorted(((v,n) for n,v in pts.items()),reverse=True), len(ld), 'late', late, flush=True)
