import mido, subprocess, wave, numpy as np
TPB=480; BPM=192; spb=60/BPM; E=TPB//2
ev=[]
def note(ch,n,beat,durb,v):
    ev.append((int(beat*TPB),mido.Message('note_on',channel=ch,note=n,velocity=v)))
    ev.append((int((beat+durb)*TPB),mido.Message('note_off',channel=ch,note=n,velocity=0)))
r=None
mel=[[72,r,76,79,81,79,76,r],[77,r,76,r,74,72,74,r],[72,r,76,79,81,79,84,r],[83,81,79,77,76,74,72,r],
     [67,r,67,68,69,r,72,r],[74,r,72,r,69,r,67,r],[72,76,79,84,83,79,76,72],[74,r,67,r,72,r,r,r]]
chords=[(48,[60,64,67]),(53,[60,65,69]),(48,[60,64,67]),(43,[59,62,67]),(53,[60,65,69]),(50,[62,65,69]),(48,[60,64,67]),(43,[59,62,67])]
for bar in range(8):
    for i,n in enumerate(mel[bar]):
        b=bar*4+i*0.5
        if n: note(0,n-12,b,0.3,96); note(2,n,b,0.2,70)
    root,ch=chords[bar]
    for beat in range(4):
        b=bar*4+beat
        if beat%2==0: note(1,root-12 if beat==0 else root-5,b,0.45,100)
        else:
            for c in ch: note(3,c,b,0.2,62)
        note(9,76 if beat%2 else 77,b+0.5,0.1,55)
ev.sort(key=lambda e:(e[0],0 if e[1].type=='note_off' else 1))
mf=mido.MidiFile(ticks_per_beat=TPB); tr=mido.MidiTrack(); mf.tracks.append(tr)
tr.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(BPM)))
for ch,p in {0:70,1:58,2:13,3:45}.items(): tr.append(mido.Message('program_change',channel=ch,program=p))
last=0
for T,m in ev: m.time=T-last; last=T; tr.append(m)
mf.save('music2.mid')
subprocess.run(['fluidsynth','-ni','-q','-g','0.9','-r','44100','-F','music2.wav','/usr/share/sounds/sf2/TimGM6mb.sf2','music2.mid'],check=True)
with wave.open('music2.wav') as w:
    ch=w.getnchannels(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32).reshape(-1,ch)
SR=44100; L=SR*10; x=x[:L]
fade=int(SR*0.05); x[-fade:]*=np.linspace(1,0,fade)[:,None]
x=x/np.abs(x).max()*0.89*32767
with wave.open('audio2.wav','w') as w:
    w.setnchannels(ch);w.setsampwidth(2);w.setframerate(SR);w.writeframes(x.astype(np.int16).tobytes())
print('ok',len(x)/SR)
