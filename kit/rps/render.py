import numpy as np, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
sys.path.insert(0,'.'); from sim import run
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
end,counts,hist=run(13)
HOLD=75; N=end+1+HOLD
g=Image.open(A+'scene_moon.png').convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
g=g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(10)); g=ImageEnhance.Brightness(g).enhance(0.45).convert('RGBA')
d=ImageDraw.Draw(g); d.rectangle((60,560,1020,1520),fill=None,outline=(201,162,74),width=5)
ov=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(ov).rectangle((62,562,1018,1518),fill=(10,8,25,90)); g.alpha_composite(ov)
d=ImageDraw.Draw(g); f=F(46); t='Who will win?'; w=d.textlength(t,font=f); d.text(((W-w)/2,250),t,font=f,fill=(255,255,255),stroke_width=5,stroke_fill=(20,15,35))
BG=g
NAMES=['Joy','Cleo','Cyrus','Rayleigh']; FILES=['idle_5.gif','idle_7.gif','idle_8.gif','idle_6.gif']
def bust(path,h):
    im=Image.open(A+path); im.seek(0); im=im.convert('RGBA'); im=im.crop(im.getbbox()); im=im.crop((0,0,im.width,int(im.height*0.56)))
    k=h/im.height; return im.resize((int(im.width*k),h),Image.NEAREST)
ICON=[bust(p,62) for p in FILES]; HUD=[bust(p,70) for p in FILES]
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
CX=[150,390,630,870]
for fr in range(N):
    k=min(fr,end); pos,typ=hist[k]; c=counts[k]
    img=BG.copy(); dr=ImageDraw.Draw(img)
    for i in range(4):
        ic=HUD[i]; x=CX[i]-60
        if c[i]==0: ic=ic.copy(); ic.putalpha(ic.split()[3].point(lambda v:v//3))
        img.alpha_composite(ic,(x,400)); dr.text((x+ic.width+10,425),str(c[i]),font=F(34),fill=(255,255,255) if c[i] else (120,120,130))
    for (x,y),t in zip(pos,typ):
        ic=ICON[t]; img.alpha_composite(ic,(int(x-ic.width/2),int(y-ic.height/2)))
    if fr>end:
        win=NAMES[int(np.argmax(c))]; t=f'{win} wins!'.upper(); fw=F(64); w=dr.textlength(t,font=fw)
        dr.text(((W-w)/2,1620),t,font=fw,fill=(255,214,90),stroke_width=6,stroke_fill=(20,15,35))
    ff.stdin.write(img.convert('RGB').tobytes())
    if fr in (5,600,1200,end+30): img.convert('RGB').resize((360,640)).save(f'p_{fr}.png')
ff.stdin.close(); ff.wait(); print('done',N/30)
