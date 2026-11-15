"""Build the six rooms of the thirty-sixth batch (confectionery, SCP-1479) and write everything derived from them:
     GFX\\map\\<room>.rmesh + _lm1.png        (with --game, otherwise into out\\)
     IndevU36Data.bb                           generated: U32_* slot constants, FillRoom table, events
     b36_rooms.ini.txt / b36_names.txt         what wire33.py appends to Data\\rooms.ini and hooks into FillRoom
     previews\\annex_rooms_b36.jpg             one render + one plan per room
   python gen_b36.py --game            everything
   python gen_b36.py room2doorhall     one room into out\\ with a plan view

Lightmaps are capped at 2048 x 2048 (LM_MAX) so the new rooms stay inside the GPU memory budget."""
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import roomkit
import rooms_b36
from gen_b7 import blitz

LM_MAX = 2048


def ini(rooms):
    out = ['', ';INDEV THIRTY-SIXTH BATCH - CONFECTIONERY AND SCP-1479 (generated, Tools\\roomkit\\gen_b36.py, IndevU36.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = 2',
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=9000']
    open('b36_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b36_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b36.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        R = ret[0]
        assert R.name == fn.__name__, (R.name, fn.__name__)
        R.bake(verbose=False, max_size=LM_MAX)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b36_%s.png' % R.name, size=(768, 432))
        y = ret[5][0][1]
        R.topview('out/b36_%s_top.png' % R.name, y_cut=(y - 400, y + 100) if y < 0 or y > 600 else None)
        built.append(ret)
        print('  %s  %d surfaces  lightmap %d  %.0fs' % (R.name, len(R.surfs), R.atlas_size, time.time() - t0))
    if not only:
        blitz(built, P='U36', FNAME='IndevU36Data.bb', EVENT='u36room', gen='gen_b36.py', src='rooms_b36.py',
              what='The six rooms of the thirty-sixth batch (confectionery, SCP-1479)')
        ini(built)
        tw, th = 512, 288
        cols = 3
        rows = (len(built) + cols - 1) // cols
        sheet = Image.new('RGB', (tw * cols, (th + 22) * rows), (16, 16, 18))
        d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
        for i, (R, key, desc, zone, pos, view) in enumerate(built):
            x, y0 = (i % cols) * tw, (i // cols) * (th + 22)
            sheet.paste(Image.open('out/b36_%s.png' % R.name).resize((tw, th), Image.LANCZOS), (x, y0 + 22))
            d.text((x + 5, y0 + 3), '%s (zone %d)' % (R.name, zone), font=font, fill=(235, 220, 120))
        os.makedirs('previews', exist_ok=True)
        sheet.save('previews/annex_rooms_b36.jpg', quality=86)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))

