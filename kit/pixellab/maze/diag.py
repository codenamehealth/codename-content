import sys; sys.argv=['x','search','0','0']
src=open('render_maze2.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
for seed in range(12):
    rc,fr,gt=sim(seed)
    print(seed,'gum',gt,'beh',{n:s['behind'] for n,s in rc.items() if s['behind'] is not None},'out',{n:round(s['out'],1) for n,s in rc.items() if s['out']},'caught',sorted(round(s['caught'],1) for s in rc.values() if s['caught']))
