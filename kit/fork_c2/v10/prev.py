import sys; sys.path.insert(0, '..')
from common import *
sys.path.insert(0, PL + 'safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['SHAKE YOUR', 'PHONE'], accent=0, color=(255, 214, 60), sub='FOR A SURPRISE')
K=8; GY=int(sys.argv[3]); M=44
IDL = idle('hollow', K)
im = Image.open(A + sys.argv[1]); im.seek(0)
f = im.convert('RGB').resize((im.width*2, im.height*2), Image.NEAREST)
ox=int(sys.argv[2]); oy=f.height-(H+2*M)
bg=f.crop((ox,oy,ox+W+2*M,oy+H+2*M)).convert('RGBA').crop((M,M,M+W,M+H))
sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([540-150,GY-22,540+150,GY+16],fill=(0,0,0,90)); bg.alpha_composite(sh)
spr=IDL[0]; bg.alpha_composite(spr,(540-spr.width//2, GY-78*K))
bg.alpha_composite(HOOK); bg.convert('RGB').resize((540,960)).save(sys.argv[4])
