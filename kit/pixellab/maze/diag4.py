import sys,os
src=open('render_maze4.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; exec(src)
for seed in range(int(os.environ.get('LO','0')),int(os.environ.get('HI','8'))):
    rc,fr,gt=sim(seed)
    print(seed,'gum',gt and (gt[0],round(gt[1],1)),'beh',{n:s['behind'] for n,s in rc.items() if s['behind'] is not None},'out',{n:round(s['out'],1) for n,s in rc.items() if s['out']},'caught',sorted(round(s['caught'],1) for s in rc.values() if s['caught']),flush=True)
