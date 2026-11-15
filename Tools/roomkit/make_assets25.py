r"""Textures of the twenty-fifth batch (original, drawn here):
     GFX\map\indev_b25_<n>.png    a colour (or framed picture) for each SCP's object (scps_b25.py)
     GFX\map\indev_b25console.png the control room's console wall: three screens, HOIST and DOOR panels
   python make_assets25.py"""
from PIL import Image, ImageDraw, ImageFont
from make_assets5 import save_map
from make_assets20 import flat
from scps_b25 import SCPS

FONT = r"C:\Windows\Fonts\arialbd.ttf"


def console():
    im = Image.new('RGB', (512, 256), (52, 54, 56))
    d = ImageDraw.Draw(im)
    for k in range(3):
        d.rectangle([20 + k * 110, 30, 120 + k * 110, 120], fill=(14, 16, 18), outline=(90, 90, 90), width=4)
    d.rectangle([28, 40, 110, 110], fill=(30, 60, 40))
    for k, t in enumerate(('HOIST', 'DOOR')):
        x = 360 + k * 76
        d.rectangle([x, 26, x + 68, 50], fill=(20, 20, 20))
        d.text((x + 34, 38), t, font=ImageFont.truetype(FONT, 16), fill=(230, 230, 230), anchor='mm')
        d.rectangle([x + 14, 70, x + 54, 150], fill=(200, 200, 190))
        d.ellipse([x + 22, 90, x + 46, 114], fill=(200, 40, 30) if k else (40, 160, 50))
    d.rectangle([160, 150, 280, 180], fill=(150, 20, 20))
    d.text((220, 165), 'CAUTION', font=ImageFont.truetype(FONT, 18), fill=(255, 220, 200), anchor='mm')
    save_map(im, 'indev_b25console.png')


if __name__ == '__main__':
    for n, cls, kind, col, *_ in SCPS:
        if kind == 'poster':
            im = Image.new('RGB', (128, 128), col)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, 127, 127], outline=(40, 30, 20), width=10)
            d.text((64, 64), 'SCP-' + n, font=ImageFont.truetype(FONT, 22), fill=(230, 230, 230), anchor='mm')
            save_map(im, 'indev_b25_%s.png' % n)
        else:
            flat('indev_b25_%s.png' % n, col, 12, 64)
    console()
    print('batch 25 textures written')
