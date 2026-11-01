import sys
from PIL import Image
out = sys.argv[1]; fs = sys.argv[2:]; tw, th = 360, 640
sh = Image.new('RGB', (tw * len(fs), th))
for i, f in enumerate(fs): sh.paste(Image.open(f).convert('RGB').resize((tw, th)), (i * tw, 0))
sh.save(out, quality=88)
