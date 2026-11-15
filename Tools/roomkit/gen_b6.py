"""Build the seven rooms of the sixth batch (13 SCPs) and write everything derived from them:
     GFX\\map\\<room>.rmesh + _lm1.png        (with --game, otherwise into out\\)
     IndevS13Data.bb                           generated: S13_* slot constants, FillRoom table, fans, events
     b6_rooms.ini.txt / b6_names.txt           what wire6.py appends to Data\\rooms.ini and hooks into FillRoom
     previews\\annex_rooms_b6.jpg              one render + one plan per room
   python gen_b6.py --game            everything
   python gen_b6.py room2grocery      one room into out\\ with a plan view"""
import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import roomkit
import rooms_b6
from gen_s16 import blitz


def ini(rooms):
    out = ['', ';INDEV SIXTH BATCH - 13 SCPs (generated meshes, Tools\\roomkit\\gen_b6.py, IndevS13.bb)',
           ';=================================================']
    for R, key, desc, zone, pos, view in rooms:
        out += ['', '[%s]' % R.name, 'descr=%s' % desc, 'mesh path=GFX\\map\\%s.rmesh' % R.name, 'shape = 2',
                'commonness = 0', 'disabledecals = true', 'zone1=%d' % zone, 'set room=%s' % pos, 'set room priority=13000']
    open('b6_rooms.ini.txt', 'w').write('\n'.join(out) + '\n')
    open('b6_names.txt', 'w').write('\n'.join(R.name for R, *_ in rooms) + '\n')


if __name__ == '__main__':
    game = '--game' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    outdir = roomkit.MAPDIR if game else 'out'
    os.makedirs('out', exist_ok=True)
    t0 = time.time()
    built = []
    for fn in rooms_b6.ALL:
        if only and fn.__name__ not in only:
            continue
        ret = fn()
        R = ret[0]
        assert R.name == fn.__name__, (R.name, fn.__name__)
        R.bake(verbose=False)
        R.export(outdir)
        R.render(ret[5][0], ret[5][1], 'out/b6_%s.png' % R.name, size=(768, 432))
        R.topview('out/b6_%s_top.png' % R.name)
        built.append(ret)
        print('  %s  %d surfaces  %.0fs' % (R.name, len(R.surfs), time.time() - t0))
    if not only:
        blitz(built, P='S13', fname='IndevS13Data.bb', event='s13room', what='the seven rooms of the sixth batch (13 SCPs)',
              gen='gen_b6.py', src='rooms_b6.py')
        ini(built)
        tw, th = 512, 288
        cols = 4
        rows = (len(built) + cols - 1) // cols
        sheet = Image.new('RGB', (tw * cols, (th + 22) * 2 * rows), (16, 16, 18))
        d = ImageDraw.Draw(sheet)
        font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
        for i, (R, key, desc, zone, pos, view) in enumerate(built):
            x, y = (i % cols) * tw, (i // cols) * (th + 22) * 2
            sheet.paste(Image.open('out/b6_%s.png' % R.name).resize((tw, th), Image.LANCZOS), (x, y + 22))
            top = Image.open('out/b6_%s_top.png' % R.name).convert('RGB')
            top.thumbnail((tw, th), Image.LANCZOS)
            sheet.paste(top, (x + (tw - top.width) // 2, y + th + 44))
            d.text((x + 5, y + 3), '%s (zone %d)' % (R.name, zone), font=font, fill=(235, 220, 120))
        os.makedirs('previews', exist_ok=True)
        sheet.save('previews/annex_rooms_b6.jpg', quality=86)
    print('%d rooms in %.1fs -> %s' % (len(built), time.time() - t0, outdir))
