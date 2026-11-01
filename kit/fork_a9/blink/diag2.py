import sys,os; sys.argv=['x','none']
src=open('render_blink.py').read().split("if __name__ == '__main__' and sys.argv[1] == 'search':")[0]
exec(src)
res=[]
for s in range(30):
    fr,ev,esc,g=sim(s,dur=60); res.append(esc[2] if esc else None)
print(os.environ.get('LIFE'),os.environ.get('SPD'),res)
