import mido, subprocess, wave, numpy as np
TPB=480; BPM=160
ev=[]
def note(ch,n,b,d,v):
    ev.append((int(b*TPB),mido.Message('note_on',channel=ch,note=n,velocity=v)))
    ev.append((int((b+d)*TPB),mido.Message('note_off',channel=ch,note=n,velocity=0)))
r=None
# 16th-note arpeggio lead over i-VI-III-VII in A minor: heroic chiptune feel
prog=[(57,[69,72,76]),(53,[69,72,77]),(48,[67,72,76]),(55,[67,71,74])]
mel=[[81,r,79,81,84,r,83,81],[77,r,76,77,81,r,79,77],[76,r,74,76,79,r,81,79],[74,r,76,79,83,81,79,76]]
for bar in range(8):
    root,ch=prog[bar%4]; b0=bar*4
    for i,n in enumerate(mel[bar%4]):
        if n: note(0,n,b0+i*0.5,0.42,92)
    for s in range(16): note(1,ch[s%3],b0+s*0.25,0.2,52)
    for q in range(8): note(2,root-12 if q%2==0 else root,b0+q*0.5,0.45,100)
    for q in range(4):
        note(9,36,b0+q,0.1,105)
        if q%2==1: note(9,38,b0+q,0.1,95)
    for e in range(8): note(9,42,b0+e*0.5+0.25,0.05,60)
ev.sort(key=lambda e:(e[0],0 if e[1].type=='note_off' else 1))
mf=mido.MidiFile(ticks_per_beat=TPB); tr=mido.MidiTrack(); mf.tracks.append(tr)
tr.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(BPM)))
for c,p in {0:80,1:81,2:38}.items(): tr.append(mido.Message('program_change',channel=c,program=p))
last=0
for T,m in ev: m.time=T-last; last=T; tr.append(m)
mf.save('music.mid')
subprocess.run(['fluidsynth','-ni','-q','-g','0.8','-r','44100','-F','music.wav','/usr/share/sounds/sf2/TimGM6mb.sf2','music.mid'],check=True)
with wave.open('music.wav') as w:
    c=w.getnchannels(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32).reshape(-1,c)
SR=44100; L=int(SR*289/30); x=x[:L].copy(); fd=int(SR*0.3); x[-fd:]*=np.linspace(1,0,fd)[:,None]
x=x/np.abs(x).max()*0.89*32767
with wave.open('audio.wav','w') as w:
    w.setnchannels(c); w.setsampwidth(2); w.setframerate(SR); w.writeframes(x.astype(np.int16).tobytes())
print('ok')
