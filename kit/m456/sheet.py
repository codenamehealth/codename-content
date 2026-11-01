import sys,subprocess,os
from PIL import Image,ImageDraw,ImageFont
# usage: sheet.py video t0 t1 step out [w] [cols]   (frames at times t0..t1 by step, labeled)
V,t0,t1,st,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
w=int(sys.argv[6]) if len(sys.argv)>6 else 216; cols=int(sys.argv[7]) if len(sys.argv)>7 else 5
crop=os.environ.get('CROP')  # x,y,w,h in source px
h=int(w*16/9) if not crop else int(w*int(crop.split(',')[3])/int(crop.split(',')[2]))
ts=[];t=t0
while t<=t1+1e-6: ts.append(round(t,3)); t+=st
rows=(len(ts)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*(h+18)),(0,0,0)); d=ImageDraw.Draw(S)
cx=crop.split(',') if crop else None
vf=(f'crop={cx[2]}:{cx[3]}:{cx[0]}:{cx[1]},' if crop else '')+f'scale={w}:{h}'
for i,t in enumerate(ts):
    r=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',V,'-frames:v','1','-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True)
    if len(r.stdout)<w*h*3: continue
    im=Image.frombytes('RGB',(w,h),r.stdout[:w*h*3])
    x,y=(i%cols)*w,(i//cols)*(h+18); S.paste(im,(x,y+18)); d.text((x+3,y+3),f'{t:.2f}',fill=(255,255,0))
S.save(out,quality=85); print(out,len(ts))
