# norm.py in.mp4 out.mp4 : two-pass loudnorm to -14 LUFS (video copied)
import sys, subprocess, json
i, o = sys.argv[1:3]
r = subprocess.run(['ffmpeg', '-i', i, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(r[r.rindex('{'):r.rindex('}') + 1])
af = f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', i, '-map', '0:v', '-map', '0:a', '-c:v', 'copy', '-af', af, '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', o], check=True)
r = subprocess.run(['ffmpeg', '-i', o, '-af', 'loudnorm=print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
print('LUFS', json.loads(r[r.rindex('{'):r.rindex('}') + 1])['input_i'])
