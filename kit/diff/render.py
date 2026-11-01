import numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30; N=int(9.0*FPS)
def F(s): return ImageFont.truetype(FONT,s)
hub=Image.open(A+'hub.gif'); FR=[]
for i in range(hub.n_frames): hub.seek(i); FR.append(np.array(hub.convert('RGB')))
def edit(a):
    a=a.copy()
    # 1) blank the TAVERN sign: cream letter pixels -> board brown
    s=a[430:468,1040:1175]; cream=(s[...,0]>200)&(s[...,1]>170); s[cream]=(150,82,42)
    # 2) tavern's left upper window shuttered
    a[260:356,1035:1106]=(157,87,45); a[260:356,1068:1073]=(84,32,32); a[260:264,1035:1106]=(84,32,32); a[352:356,1035:1106]=(84,32,32)
    # 3) attic window bricked over with plaster
    a[212:262,528:586]=(246,203,146)
    return a
CROP=(400,0,1840,1080); PW,PH=900,675
def panel(a): return Image.fromarray(a).crop(CROP).resize((PW,PH),Image.NEAREST)
TOPS=[panel(f) for f in FR]; BOTS=[panel(edit(f)) for f in FR]
bgsrc=Image.open(A+'vit_hd.gif'); bgsrc.seek(0); g=bgsrc.convert('RGB'); s=H/g.height; g=g.resize((int(g.width*s),H),Image.LANCZOS); ox=(g.width-W)//2
BG=ImageEnhance.Brightness(g.crop((ox,0,ox+W,H)).filter(ImageFilter.GaussianBlur(14))).enhance(0.55).convert('RGBA')
d=ImageDraw.Draw(BG); f=F(50); t='Find 3 differences'; w=d.textlength(t,font=f); d.text(((W-w)/2,250),t,font=f,fill=(255,255,255),stroke_width=6,stroke_fill=(20,15,35))
X=(W-PW)//2; Y1=360; Y2=Y1+PH+30
for y in (Y1,Y2): d.rectangle([X-8,y-8,X+PW+7,y+PH+7],fill=(201,162,74))
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
for fn in range(N):
    k=int(fn/FPS*1000/hub.info.get('duration',100))%len(FR)
    img=BG.copy(); img.paste(TOPS[k],(X,Y1)); img.paste(BOTS[k],(X,Y2))
    ff.stdin.write(img.convert('RGB').tobytes())
    if fn==0: img.convert('RGB').save('still.png')
ff.stdin.close(); ff.wait()
# answer key
key=Image.fromarray(edit(FR[0])).crop(CROP); dk=ImageDraw.Draw(key)
for b in [(1030,420,1185,478),(1025,250,1115,365),(518,202,596,272)]: dk.ellipse([b[0]-400-20,b[1]-20,b[2]-400+20,b[3]+20],outline=(255,40,40),width=8)
key.save('answer_key.png'); print('done')
