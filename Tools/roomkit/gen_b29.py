"""Build the six rooms of the twenty-ninth batch (SCP-820-JP, SCP-867, SCP-120) and write everything derived from them:
     GFX\\map\\<room>.rmesh + _lm1.png        (with --game, otherwise into out\\)
     IndevU29Data.bb                           generated: U29_* slot constants, FillRoom table, events
     b29_rooms.ini.txt / b29_names.txt         what wire18.py appends to Data\\rooms.ini and hooks into FillRoom
     previews\\annex_rooms_b29.jpg             one render + one plan per room
   python gen_b29.py --game            everything
   python gen_b29.py room2doorhall     one room into out\\ with a plan view

Lightmaps are capped at 2048 x 2048 (LM_MAX) so the new rooms stay inside the GPU memory budget."""
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import roomkit
import rooms_b29
from gen_b7 import blitz

LM_MAX = 2048


def ini(rooms):
    out = ['', ';INDEV TWENTY-NINTH BATCH - SCP-820-JP, SCP-867, SCP-120 / LUNAR AREA-32 (generated, Tools\\roomkit\\gen_b29.py, IndevU29.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = 2',
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=9000']
    open('b29_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b29_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b29.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        R = ret[0]
        assert R.name == fn.__name__, (R.name, fn.__name__)
        R.bake(verbose=False, max_size=LM_MAX)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b29_%s.png' % R.name, size=(768, 432))
        y = ret[5][0][1]
        R.topview('out/b29_%s_top.png' % R.name, y_cut=(y - 400, y + 100) if y < 0 or y > 600 else None)
        if R.name == 'room2b29pool':
            R.render((-250, rooms_b29.Y + 165, -350), (-80, rooms_b29.Y + 60, 300), 'out/b29_lunar_reception.png', size=(768, 432))
            R.render((-700, rooms_b29.Y + 170, 520), (-300, rooms_b29.Y + 150, 1000), 'out/b29_lunar_observatory.png', size=(768, 432))
            R.render((300, rooms_b29.Y + 170, -700), (900, rooms_b29.Y + 120, 500), 'out/b29_lunar_cargo.png', size=(768, 432))
            R.render((-300, rooms_b29.Y1 + 165, 0), (500, rooms_b29.Y1 + 120, 0), 'out/b29_lunar_sl1.png', size=(768, 432))
        built.append(ret)
        print('  %s  %d surfaces  lightmap %d  %.0fs' % (R.name, len(R.surfs), R.atlas_size, time.time() - t0))
    if not only:
        blitz(built, P='U29', FNAME='IndevU29Data.bb', EVENT='u29room', gen='gen_b29.py', src='rooms_b29.py',
              what='The three rooms of the twenty-ninth batch (SCP-820-JP, SCP-867, SCP-120)')
        ini(built)
        tw, th = 512, 288
        cols = 3
        rows = (len(built) + cols - 1) // cols
        sheet = Image.new('RGB', (tw * cols, (th + 22) * rows), (16, 16, 18))
        d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
        for i, (R, key, desc, zone, pos, view) in enumerate(built):
            x, y0 = (i % cols) * tw, (i // cols) * (th + 22)
            sheet.paste(Image.open('out/b29_%s.png' % R.name).resize((tw, th), Image.LANCZOS), (x, y0 + 22))
            d.text((x + 5, y0 + 3), '%s (zone %d)' % (R.name, zone), font=font, fill=(235, 220, 120))
        os.makedirs('previews', exist_ok=True)
        sheet.save('previews/annex_rooms_b29.jpg', quality=86)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))

