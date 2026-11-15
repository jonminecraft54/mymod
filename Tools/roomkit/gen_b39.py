"""Build the five rooms of the thirty-seventh batch (SCP-028, reactor, archive, balcony hall, cells) and write:
     GFX\\map\\<room>.rmesh + _lm1.png        (with --game, otherwise into out\\)
     IndevU39Data.bb                           generated: U39_* slot constants, FillRoom table, events
     b39_rooms.ini.txt / b39_names.txt         what wire39.py appends to Data\\rooms.ini and hooks into FillRoom
     previews\\annex_rooms_b39.jpg             one render per room
   python gen_b39.py --game            everything
   python gen_b39.py room2b39hall      one room into out\\

Lightmaps are capped at 512 x 512 (LM_MAX) with coarse luxels: cheap on memory, still soft baked light."""
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import roomkit
import rooms_b39
from gen_b7 import blitz

LM_MAX = 512


def ini(rooms):
    out = ['', ';INDEV THIRTY-NINTH BATCH - RESEARCH, WAREHOUSE B, TEST CONTAINMENT (generated, Tools\\roomkit\\gen_b39.py, IndevU39.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = 2',
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=9000']
    open('b39_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b39_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b39.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        R = ret[0]
        assert R.name == fn.__name__, (R.name, fn.__name__)
        R.bake(verbose=False, max_size=LM_MAX)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b39_%s.png' % R.name, size=(768, 432))
        built.append(ret)
        print('  %s  %d surfaces  lightmap %d  %.0fs' % (R.name, len(R.surfs), R.atlas_size, time.time() - t0))
    if not only:
        blitz(built, P='U39', FNAME='IndevU39Data.bb', EVENT='u39room', gen='gen_b39.py', src='rooms_b39.py',
              what='The three very big rooms of the thirty-ninth batch (research department, Warehouse B, Test Containment 4)')
        ini(built)
        tw, th = 512, 288
        cols = 3
        rows = (len(built) + cols - 1) // cols
        sheet = Image.new('RGB', (tw * cols, (th + 22) * rows), (16, 16, 18))
        d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
        for i, (R, key, desc, zone, pos, view) in enumerate(built):
            x, y0 = (i % cols) * tw, (i // cols) * (th + 22)
            sheet.paste(Image.open('out/b39_%s.png' % R.name).resize((tw, th), Image.LANCZOS), (x, y0 + 22))
            d.text((x + 5, y0 + 3), '%s (zone %d)' % (R.name, zone), font=font, fill=(235, 220, 120))
        os.makedirs('previews', exist_ok=True)
        sheet.save('previews/annex_rooms_b39.jpg', quality=86)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))
