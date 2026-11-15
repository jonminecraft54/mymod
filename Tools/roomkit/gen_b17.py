"""Build the two rooms of the seventeenth batch (The Forgotten Hotel) and write everything derived from them:
     GFX\\map\\<room>.rmesh + _lm1.png        (with --game, otherwise into out\\)
     IndevU17Data.bb                           generated: U17_* slot constants, FillRoom table, events
     b17_rooms.ini.txt / b17_names.txt         what wire17.py appends to Data\\rooms.ini and hooks into FillRoom
     previews\\annex_rooms_b17.jpg             one render + one plan per room
   python gen_b17.py --game            everything
   python gen_b17.py room2doorhall     one room into out\\ with a plan view

Lightmaps are capped at 2048 x 2048 (LM_MAX) so the new rooms stay inside the GPU memory budget."""
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import roomkit
import rooms_b17
from gen_b7 import blitz

LM_MAX = 2048


def ini(rooms):
    out = ['', ';INDEV SEVENTEENTH BATCH - 2 rooms (The Forgotten Hotel) (generated, Tools\\roomkit\\gen_b17.py, IndevU17.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = 2',
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=9000']
    open('b17_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b17_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b17.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        R = ret[0]
        assert R.name == fn.__name__, (R.name, fn.__name__)
        R.bake(verbose=False, max_size=LM_MAX)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b17_%s.png' % R.name, size=(768, 432))
        y = ret[5][0][1]
        R.topview('out/b17_%s_top.png' % R.name, y_cut=(y - 400, y + 100) if y < 0 or y > 600 else None)
        built.append(ret)
        print('  %s  %d surfaces  lightmap %d  %.0fs' % (R.name, len(R.surfs), R.atlas_size, time.time() - t0))
    if not only:
        blitz(built, P='U17', FNAME='IndevU17Data.bb', EVENT='u17room', gen='gen_b17.py', src='rooms_b17.py',
              what='The two rooms of the seventeenth batch (The Forgotten Hotel)')
        ini(built)
        tw, th = 512, 288
        cols = 2
        rows = (len(built) + cols - 1) // cols
        sheet = Image.new('RGB', (tw * cols, (th + 22) * rows), (16, 16, 18))
        d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
        for i, (R, key, desc, zone, pos, view) in enumerate(built):
            x, y0 = (i % cols) * tw, (i // cols) * (th + 22)
            sheet.paste(Image.open('out/b17_%s.png' % R.name).resize((tw, th), Image.LANCZOS), (x, y0 + 22))
            d.text((x + 5, y0 + 3), '%s (zone %d)' % (R.name, zone), font=font, fill=(235, 220, 120))
        os.makedirs('previews', exist_ok=True)
        sheet.save('previews/annex_rooms_b17.jpg', quality=86)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))

