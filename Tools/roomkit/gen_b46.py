"""Build the five rooms of the thirty-seventh batch (SCP-028, reactor, archive, balcony hall, cells) and write:
     GFX\\map\\<room>.rmesh + _lm1.png        (with --game, otherwise into out\\)
     IndevU46Data.bb                           generated: U45_* slot constants, FillRoom table, events
     b46_rooms.ini.txt / b46_names.txt         what wire45.py appends to Data\\rooms.ini and hooks into FillRoom
     previews\\annex_rooms_b46.jpg             one render per room
   python gen_b46.py --game            everything
   python gen_b46.py room2b39hall      one room into out\\

Lightmaps are capped at 512 x 512 (LM_MAX) with coarse luxels: cheap on memory, still soft baked light."""
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import roomkit
import rooms_b46
from gen_b7 import blitz

LM_MAX = 512
SHAPES = {}


def ini(rooms):
    out = ['', ';INDEV FORTY-SIXTH BATCH - ALTERNATE TIMELINE (generated, Tools\\roomkit\\gen_b46.py, IndevU46.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = %d' % SHAPES.get(R.name, 2),
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=9000']
    open('b46_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b46_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b46.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        if len(ret) > 6:
            SHAPES[ret[0].name] = ret[6]
            ret = ret[:6]
        R = ret[0]
        assert R.name == fn.__name__, (R.name, fn.__name__)
        R.bake(verbose=False, max_size=LM_MAX)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b46_%s.png' % R.name, size=(768, 432))
        built.append(ret)
        print('  %s  %d surfaces  lightmap %d  %.0fs' % (R.name, len(R.surfs), R.atlas_size, time.time() - t0))
    if not only:
        blitz(built, P='U46', FNAME='IndevU46Data.bb', EVENT='u46room', gen='gen_b46.py', src='rooms_b46.py',
              what='The four rooms of the forty-sixth batch (checkpoint 9, sector R, personnel lift, sealed wing)')
        ini(built)
        tw, th = 512, 288
        cols = 3
        rows = (len(built) + cols - 1) // cols
        sheet = Image.new('RGB', (tw * cols, (th + 22) * rows), (16, 16, 18))
        d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
        for i, (R, key, desc, zone, pos, view) in enumerate(built):
            x, y0 = (i % cols) * tw, (i // cols) * (th + 22)
            sheet.paste(Image.open('out/b46_%s.png' % R.name).resize((tw, th), Image.LANCZOS), (x, y0 + 22))
            d.text((x + 5, y0 + 3), '%s (zone %d)' % (R.name, zone), font=font, fill=(235, 220, 120))
        os.makedirs('previews', exist_ok=True)
        sheet.save('previews/annex_rooms_b46.jpg', quality=86)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))

