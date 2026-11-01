from PIL import Image, ImageDraw, ImageFont
import glob, os, numpy as np, colorsys
FONT='../npmfont/ps/package/files/PressStart2P.ttf'
src=[Image.open(f).convert('RGBA') for f in ['../syeda_src/char3/char7.png','../syeda_src/char3/char6.png']]
pal=set()
for s in src:
    a=np.array(s); m=a[:,:,3]>0
    for p in a[m][:,:3]: pal.add(tuple(int(x) for x in p))
PAL=np.array(sorted(pal),dtype=np.float32)
def lab(c):
    c=c/255.0; c=np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    xyz=c@M.T/np.array([0.9505,1.0,1.089])
    f=np.where(xyz>0.008856,np.cbrt(xyz),7.787*xyz+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
PLAB=lab(PAL)
def clean(im, extra=None):
    a=np.array(im).astype(np.float32); out=np.zeros_like(a)
    m=a[:,:,3]>=128
    px=lab(a[m][:,:3]); d=((px[:,None,:]-PLAB[None,:,:])**2).sum(-1); idx=d.argmin(1)
    out[m,:3]=PAL[idx]; out[m,3]=255
    o=out.astype(np.uint8)
    # drop isolated single pixels
    al=o[:,:,3]>0; nb=sum(np.roll(np.roll(al,dy,0),dx,1) for dy in (-1,0,1) for dx in (-1,0,1))-al
    o[al&(nb==0)]=0
    return Image.fromarray(o)
def frames(name):
    return [Image.open(f).convert('RGBA') for f in sorted(glob.glob(f'cleo/{name}/*.png'))]
def panel(action, models, fps, scale=3, hold_last=0):
    cols=[('SYEDA',None)]
    for m,label in models:
        if os.path.isdir(f'cleo/{action}_{m}'): cols+= [(label+' RAW',f'{action}_{m}'),(label+' CLEAN',f'{action}_{m}')]
    seqs=[]
    for lab_,key in cols:
        if key is None: continue
        fr=frames(key)
        if 'CLEAN' in lab_: fr=[clean(f) for f in fr]
        seqs.append(fr)
    n=max(len(s) for s in seqs)
    S=max(s[0].width for s in seqs); cw=S*scale; top=40
    W=cw*len(cols); H=cw+top
    f12=ImageFont.truetype(FONT,12)
    base=src[0]
    out=[]
    for i in range(n+hold_last):
        c=Image.new('RGBA',(W,H),(38,42,52,255)); d=ImageDraw.Draw(c)
        for j,(lab_,key) in enumerate(cols):
            d.text((j*cw+8,12),lab_,font=f12,fill=(230,230,230))
            if key is None:
                b=Image.new('RGBA',(S,S),(0,0,0,0)); 
                off=(S-92)//2 if S!=92 else 0
                # align same as input placement
                if S==128: b.alpha_composite(base,(-14,128-92-14+4))
                else: b.alpha_composite(base)
                c.alpha_composite(b.resize((cw,cw),Image.NEAREST),(j*cw,top))
            else:
                seq=seqs[j-1] if False else None
        k=0
        for j,(lab_,key) in enumerate(cols):
            if key is None: continue
            fr=seqs[k]; k+=1
            f=fr[min(i,len(fr)-1)]
            c.alpha_composite(f.resize((cw,cw),Image.NEAREST),(j*cw,top))
        out.append(c.convert('RGB'))
    out[0].save(f'cleo/compare_{action}.gif',save_all=True,append_images=out[1:],duration=int(1000/fps),loop=0)
    return len(cols)
if __name__=='__main__':
    import sys
    for action,fps in [('walk',10),('attack',12),('eat',8)]:
        print(action, panel(action,[('ai','TEXT'),('mm','MINIMAX')],fps))
