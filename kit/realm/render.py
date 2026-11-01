import numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont
A='../pause/assets/'; FONT='../npmfont/ps/package/files/PressStart2P.ttf'
W,H,FPS=1080,1920,30
def F(s): return ImageFont.truetype(FONT,s)
SC=[('hub.gif','THE VILLAGE',(780,1150)),('found_hd.gif','THORNBERRY FOREST',(560,1000)),('sun_hd.gif','THE SUN TEMPLE',(820,1100)),('recov_hd.gif','THE MOON TEMPLE',(820,1100)),('vit_hd.gif','THE CASTLE',(700,1120))]
SEG=[110,105,110,109,110]   # cut points match the reference (3.67, 7.17, 10.83, 14.47, end)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','video_noaudio.mp4'],stdin=subprocess.PIPE)
cw=int(round(1080*W/H))  # source crop width for a 9:16 window at full source height
gf=0
for si,((fn,name,(x0,x1)),n) in enumerate(zip(SC,SEG)):
    im=Image.open(A+fn); frames=[]
    for i in range(im.n_frames): im.seek(i); frames.append(im.convert('RGB'))
    dur=im.info.get('duration',100)
    lab=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lab)
    f=F(64 if len(name)<14 else 56); words=name.split(' ')
    lines=[name] if d.textlength(name,font=f)<980 else [' '.join(words[:-1]),words[-1]]
    y=300
    if si==0:
        hf=F(76)
        for hy,ht in ((150,'CHOOSE YOUR'),(250,'REALM')):
            hw=d.textlength(ht,font=hf); d.text(((W-hw)/2,hy),ht,font=hf,fill=(255,214,90),stroke_width=8,stroke_fill=(20,15,35))
        y=380
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2,y),ln,font=f,fill=(255,255,255),stroke_width=8,stroke_fill=(20,15,35)); y+=90
    # number badge
    d.ellipse([60,1640,170,1750],fill=(255,255,255,215),outline=(20,15,35,255),width=5)
    nf=F(52); t=str(si+1); w=d.textlength(t,font=nf); d.text((115-w/2,1670),t,font=nf,fill=(20,15,35))
    for k in range(n):
        u=k/max(1,n-1); cx=x0+(x1-x0)*u
        sx=int(min(1920-cw,max(0,cx-cw/2)))
        src=frames[int((gf/FPS)*1000/dur)%len(frames)]
        img=src.crop((sx,0,sx+cw,1080)).resize((W,H),Image.NEAREST).convert('RGBA')
        img.alpha_composite(lab)
        ff.stdin.write(img.convert('RGB').tobytes())
        if k==n//2: img.convert('RGB').resize((270,480)).save(f'p_{si}.png')
        gf+=1
ff.stdin.close(); ff.wait(); print('done',gf/FPS)
