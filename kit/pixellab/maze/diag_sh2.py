import sys,os
src=open('render_shadow15.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
sys.argv=['x']; __file__=os.path.abspath('render_shadow15.py'); exec(src)
print('GUM_XY',GUM_XY, 'er',er,'ec',ec)
rc,fr,gt=sim(0)
for f in range(0,len(fr),30):
    st=fr[f][0]; print(f//30, {n:(int(v['y']//C),int(v['x']//C)) for n,v in st.items()})
