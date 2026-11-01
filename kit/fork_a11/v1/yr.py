import sys
sys.argv = ['x', '1', 'none']
src = open('render1s.py').read().split("def state(t)")[0]
exec(src)
ys = [motion(P, f / FPS)[1] + P['oy'] for f in range(NF)]
print('TY', TY, 'min y off', min(ys), 'potion top min', TY + min(ys) - POT.height // 2, 'hook top min', TY + min(ys) - POT.height // 2 - 40 - 10)
