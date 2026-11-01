import sys,os; sys.argv=['x','search','0','0']
src=open('render_maze2.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
lo,hi=int(os.environ['LO']),int(os.environ['HI'])
for seed in range(lo,hi):
    r=score(seed)
    rc,fr,gt=sim(seed)
    print(os.environ['GC'],seed,'P' if r else '-',gt and (gt[0],round(gt[1],1)),{n:s['behind'] for n,s in rc.items() if s['behind'] is not None},{n:round(s['out'],1) for n,s in rc.items() if s['out']},r,flush=True)
