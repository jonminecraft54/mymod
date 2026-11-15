"""Build the three rooms of the eleventh batch (photo rooms) and write everything derived from them:
     GFX\\map\\<room>.rmesh + _lm1.png        (with --game, otherwise into out\\)
     IndevT11Data.bb                           generated: T11_* slot constants, FillRoom table, fans, events
     b11_rooms.ini.txt / b11_names.txt         what wire11.py appends to Data\\rooms.ini and hooks into FillRoom
     previews\\annex_rooms_b11.jpg             one render + one plan per room
   python gen_b11.py --game            everything
   python gen_b11.py room2hoistoffice   one room into out\\ with a plan view

Lightmaps are capped at 2048 x 2048 (LM_MAX) so the new rooms stay inside the GPU memory budget."""
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import roomkit
import rooms_b11
from gen_b7 import blitz

LM_MAX = 2048


def ini(rooms):
    out = ['', ';INDEV ELEVENTH BATCH - 3 photo rooms (generated meshes, Tools\\roomkit\\gen_b11.py, IndevT11.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = 2',
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=9000']
    open('b11_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b11_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b11.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        R = ret[0]
        assert R.name == fn.__name__, (R.name, fn.__name__)
        R.bake(verbose=False, max_size=LM_MAX)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b11_%s.png' % R.name, size=(768, 432))
        y = ret[5][0][1]
        R.topview('out/b11_%s_top.png' % R.name, y_cut=(y - 400, y + 100) if y < 0 or y > 600 else None)
        built.append(ret)
        print('  %s  %d surfaces  lightmap %d  %.0fs' % (R.name, len(R.surfs), R.atlas_size, time.time() - t0))
    if not only:
        blitz(built, P='T11', FNAME='IndevT11Data.bb', EVENT='t11room', gen='gen_b11.py', src='rooms_b11.py',
              what='The three photo rooms of the eleventh batch')
        ini(built)
        tw, th = 512, 288
        cols = 3
        sheet = Image.new('RGB', (tw * cols, (th + 22) * 2), (16, 16, 18))
        d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
        for i, (R, key, desc, zone, pos, view) in enumerate(built):
            x = i * tw
            sheet.paste(Image.open('out/b11_%s.png' % R.name).resize((tw, th), Image.LANCZOS), (x, 22))
            top = Image.open('out/b11_%s_top.png' % R.name).convert('RGB')
            top.thumbnail((tw, th), Image.LANCZOS)
            sheet.paste(top, (x + (tw - top.width) // 2, th + 44))
            d.text((x + 5, 3), '%s (zone %d)' % (R.name, zone), font=font, fill=(235, 220, 120))
        os.makedirs('previews', exist_ok=True)
        sheet.save('previews/annex_rooms_b11.jpg', quality=86)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))
