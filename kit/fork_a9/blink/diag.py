import sys; sys.argv=['x','none']
src=open('render_blink.py').read().split("if __name__ == '__main__' and sys.argv[1] == 'search':")[0]
exec(src)
for s in range(40):
    fr,ev,esc,g=sim(s); print(s, esc and (esc[0],round(esc[1],1),esc[2]), fr[-1]['att'])
