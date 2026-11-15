"""Preview sheet for the Indev-zone batch + a read-back check of the room files."""
import os
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import rmesh

G = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\map"
names = [('room2blockhall', 'room2blockhall - Containment Block D / SCP-017'),
         ('room1testcage', 'room1testcage - Test Chamber 4-A / SCP-131'),
         ('room2liftshaft', 'room2liftshaft - Maintenance Shaft 4'),
         ('room2cobserve', 'room2cobserve - Observation 4-C / SCP-999'),
         ('room1store4', 'room1store4 - Stores 4')]
for n, _ in names:
    m = rmesh.read_rmesh(os.path.join(G, n + '.rmesh'))
    print(n, m['header'], 'meshes', len(m['meshes']), 'hidden', len(m['hidden']), 'trailing', m['trailing'],
          dict(Counter(e['class'] for e in m['ents'])))
tw, th = 640, 360
sheet = Image.new('RGB', (tw * 4, (th + 28) * 3), (16, 16, 18))
d = ImageDraw.Draw(sheet)
f = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
for i, (n, label) in enumerate(names):
    col, row = (i % 2) * 2, i // 2
    for k in (1, 2):
        im = Image.open('out/final_%s_%d.png' % (n, k)).resize((tw, th), Image.LANCZOS)
        sheet.paste(im, ((col + k - 1) * tw, row * (th + 28) + 28))
    d.text((col * tw + 8, row * (th + 28) + 4), label, font=f, fill=(235, 220, 120))
os.makedirs('previews', exist_ok=True)
sheet.save('previews/annex_rooms_zone4.jpg', quality=88)
print('sheet written')
