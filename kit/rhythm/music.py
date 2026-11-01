import mido, subprocess, wave, json, numpy as np
C=json.load(open('chart.json')); SR=44100; DUR=27.6
BEAT=1.342/2; BPM=60/BEAT; T0=0.23; TPB=480
ev=[]
def note(ch,n,sec,dsec,v):
    b=lambda s: int(round(s/BEAT*TPB))
    ev.append((b(sec),mido.Message('note_on',channel=ch,note=n,velocity=v)))
    ev.append((b(sec+dsec),mido.Message('note_off',channel=ch,note=n,velocity=0)))
r=None
# original E-minor riff over the stomp-stomp-clap groove (2 beats per groove cycle)
prog=[40,40,36,38]  # E E C D (bass roots)
mel=[[64,r,67,r,71,r,69,67],[64,r,67,r,72,71,69,r],[60,r,64,r,67,r,69,71],[62,r,66,r,69,r,67,66]]
n_cyc=20
for k in range(n_cyc):
    t=T0+k*1.342; bar=k//2; root=prog[bar%4]
    note(1,root,t,0.28,100); note(1,root,t+0.31,0.25,90); note(1,root+7,t+0.61,0.3,85)
    if k>=2:
        m=mel[bar%4]; half=(k%2)*4
        for i in range(4):
            n=m[half+i]
            if n: note(0,n+12,t+i*BEAT/2,BEAT/2*0.8,88)
# bravo chord
for n in (64,67,71,76): note(0,n+12,C['end']+0.2,1.0,95)
ev.sort(key=lambda e:(e[0],0 if e[1].type=='note_off' else 1))
mf=mido.MidiFile(ticks_per_beat=TPB); tr=mido.MidiTrack(); mf.tracks.append(tr)
tr.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(BPM)))
for c,p in {0:80,1:38}.items(): tr.append(mido.Message('program_change',channel=c,program=p))
last=0
for T,m in ev: m.time=T-last; last=T; tr.append(m)
mf.save('music.mid')
subprocess.run(['fluidsynth','-ni','-q','-g','0.7','-r','44100','-F','music.wav','/usr/share/sounds/sf2/TimGM6mb.sf2','music.mid'],check=True)
with wave.open('music.wav') as w:
    ch=w.getnchannels(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32).reshape(-1,ch)/32768
mus=x.mean(1); L=int(SR*DUR); out=np.zeros(L); out[:min(L,len(mus))]+=mus[:L]*0.8
rng=np.random.default_rng(1)
def stomp():
    t=np.arange(int(SR*0.25))/SR; f=55+60*np.exp(-t*30)
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*14)*1.0 + rng.standard_normal(len(t))*np.exp(-t*80)*0.35)
def clap():
    t=np.arange(int(SR*0.22))/SR; n=rng.standard_normal(len(t))
    env=np.zeros_like(t)
    for d in (0,0.012,0.024): env+=np.exp(-np.clip(t-d,0,None)*60)*(t>=d)
    env+=np.exp(-t*18)*0.4
    s=n*env; s=np.convolve(s,[1,-0.9],mode='same')  # brighten
    return s*0.45
def add(sig,tt,g=1.0):
    i=int(tt*SR); j=min(L,i+len(sig)); out[i:j]+=sig[:j-i]*g
for tt in C['stomp']: add(stomp(),tt,0.9)
for tt in C['clap']: add(clap(),tt,1.0)
fd=int(SR*0.4); out[-fd:]*=np.linspace(1,0,fd)
out=out/np.abs(out).max()*0.89
with wave.open('audio.wav','w') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes())
print('ok',BPM)
