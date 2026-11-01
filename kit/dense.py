# usage: dense.py video out.jpg t0 t1 fps x0 y0 x1 y1 cols [scale]
import sys,subprocess,os,tempfile,glob
from PIL import Image,ImageDraw
v,out,t0,t1,fps=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5])
x0,y0,x1,y1,cols=map(int,sys.argv[6:11]); sc=float(sys.argv[11]) if len(sys.argv)>11 else 1.0
d=tempfile.mkdtemp(dir=os.path.dirname(out))
subprocess.run(['ffmpeg','-v','error','-ss',str(t0),'-i',v,'-t',str(t1-t0),'-vf',f'fps={fps},crop={x1-x0}:{y1-y0}:{x0}:{y0}','-q:v','3',d+'/f_%04d.jpg'],check=True)
fs=sorted(glob.glob(d+'/f_*.jpg')); ims=[Image.open(f).convert('RGB') for f in fs]
w,h=int((x1-x0)*sc),int((y1-y0)*sc); rows=(len(ims)+cols-1)//cols
G=Image.new('RGB',(cols*(w+4),rows*(h+22)),'white'); dr=ImageDraw.Draw(G)
for i,im in enumerate(ims):
    X,Y=(i%cols)*(w+4),(i//cols)*(h+22); G.paste(im.resize((w,h)),(X,Y+22)); dr.text((X+3,Y+5),f"t={t0+i/fps:.2f}",fill='black')
G.save(out,quality=85)
for f in fs: os.remove(f)
os.rmdir(d)
print(len(ims),G.size)
