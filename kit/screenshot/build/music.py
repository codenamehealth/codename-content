import mido, random, json, numpy as np, subprocess, wave
random.seed(7)
TPB=480; BPM=150; spb=60/BPM
def tk(sec): return int(round(sec/spb*TPB))
ev=[]  # (time_sec, msg)
def note(ch,n,t,d,v=90):
    ev.append((t,mido.Message('note_on',channel=ch,note=n,velocity=v)))
    ev.append((t+d,mido.Message('note_off',channel=ch,note=n,velocity=0)))
prog={0:70,1:58,2:13,3:45}
E8=spb/2
mot=[[52,None,55,None,57,None,58,59],[52,None,55,None,58,None,57,55]]
def sneaky(t0,t1,vel=92):
    t=t0;i=0
    while t<t1-0.01:
        bar=mot[(i//8)%2]; n=bar[i%8]
        if n: note(0,n,t,E8*0.55,vel); note(3,n+12,t,E8*0.4,70)
        if i%2==0: note(1,(40 if (i//2)%2==0 else 47),t,E8*0.7,85)
        t+=E8;i+=1
def ticks(t0,t1,step):
    t=t0;k=0
    while t<t1-0.01:
        note(9,76 if k%2==0 else 77,t,0.05,100);t+=step;k+=1
def chaos(t0,t1):
    note(9,49,t0,0.5,110); note(9,57,t1-0.02 if t1<9.9 else t0,0.4,0)
    t=t0;sc=[76,79,81,83,86,88,91,93]
    while t<t1-0.01:
        note(2,random.choice(sc),t,0.09,100); t+=0.1
    t=t0;k=0
    while t<t1-0.01:
        note(1,40 if k%2==0 else 52,t,0.15,95); note(9,38 if k%2 else 36,t,0.1,90); t+=0.2;k+=1
sneaky(0.0,4.0); ticks(4.0,4.5,0.125)          # suspense right before the miss
chaos(4.5,5.25)
sneaky(5.25,7.9,85); ticks(7.9,8.7,0.2)         # near-miss: music drops out, only ticking
chaos(8.7,10.0)
ev.sort(key=lambda e:(e[0],0 if e[1].type=='note_off' else 1))
mf=mido.MidiFile(ticks_per_beat=TPB); tr=mido.MidiTrack(); mf.tracks.append(tr)
tr.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(BPM)))
for ch,p in prog.items(): tr.append(mido.Message('program_change',channel=ch,program=p))
last=0
for t,m in ev:
    T=tk(t); m.time=T-last; last=T; tr.append(m)
tr.append(mido.MetaMessage('end_of_track',time=tk(1.0)))
mf.save('music.mid')
subprocess.run(['fluidsynth','-ni','-q','-g','0.9','-r','44100','-F','music.wav','/usr/share/sounds/sf2/TimGM6mb.sf2','music.mid'],check=True)
# ---- SFX
SR=44100
def boing(dur=0.35,f0=180):
    t=np.arange(int(SR*dur))/SR
    f=f0*(1+0.9*np.exp(-t*10))*(1+0.25*np.exp(-t*6)*np.sin(2*np.pi*14*t))
    ph=2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)+0.3*np.sin(2*ph))*np.exp(-t*7)*0.5
def whistle(dur=0.45,a=700,b=2000):
    t=np.arange(int(SR*dur))/SR
    f=(a+(b-a)*(t/dur)**1.4)*(1+0.02*np.sin(2*np.pi*7*t))
    ph=2*np.pi*np.cumsum(f)/SR
    env=np.minimum(1,t/0.03)*np.minimum(1,(dur-t)/0.06)
    return (np.sin(ph)*0.35+np.random.randn(len(t))*0.02)*env
hits=json.load(open('hits.json'))
with wave.open('music.wav') as w:
    ch=w.getnchannels(); raw=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
mus=raw.reshape(-1,ch).mean(1) if ch>1 else raw
L=int(SR*10.0); out=np.zeros(L); out[:min(L,len(mus))]+=mus[:L]*1.0
def add(sig,t,g=1.0):
    i=int(t*SR); j=min(L,i+len(sig)); out[i:j]+=sig[:j-i]*g
random.seed(3)
for h in hits: add(boing(f0=random.choice([150,180,210,240])),h,0.8)
add(whistle(),4.47,0.9); add(whistle(),8.67,0.9)
out=out/ max(1e-6,np.abs(out).max())*0.89
pcm=(out*32767).astype(np.int16)
with wave.open('audio.wav','w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
print('ok',len(mus)/SR)
