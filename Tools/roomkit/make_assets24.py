"""Textures of the twenty-fourth batch (original, drawn here):
     GFX\\map\\indev_b24_<n>.png   a flat, lightly noisy colour for each SCP's object (scps_b24.py)
     GFX\\map\\indev_b24banner.png SECURE. CONTAIN. PROTECT. with the emblem, for Storage 6H
     GFX\\map\\indev_b24poster.png a red staff poster: WE ARE HERE TO PROTECT YOU
     GFX\\map\\indev_b24stair.png  SCP-087's stairwell, a flight going down into the dark
   python make_assets24.py"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_assets5 import save_map
from make_assets20 import flat
from scps_b24 import SCPS

FONT = r"C:\Windows\Fonts\arialbd.ttf"


def emblem(d, cx, cy, r, col, w):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], outline=col, width=w)
    for a in ((0, -1), (-0.87, 0.5), (0.87, 0.5)):
        d.line([(cx + a[0] * r * 0.2, cy + a[1] * r * 0.2), (cx + a[0] * r * 0.75, cy + a[1] * r * 0.75)], fill=col, width=w)


def banner():
    im = Image.new('RGB', (1024, 360), (236, 234, 228))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1023, 359], outline=(90, 90, 90), width=16)
    emblem(d, 860, 150, 110, (30, 30, 30), 12)
    d.text((70, 120), 'SCP', font=ImageFont.truetype(FONT, 150), fill=(28, 28, 28), anchor='lm')
    d.text((512, 300), 'Secure. Contain. Protect.', font=ImageFont.truetype(FONT, 60), fill=(28, 28, 28), anchor='mm')
    save_map(im.filter(ImageFilter.GaussianBlur(0.6)), 'indev_b24banner.png')


def poster():
    im = Image.new('RGB', (256, 352), (200, 30, 30))
    d = ImageDraw.Draw(im)
    d.text((128, 40), 'WE ARE HERE', font=ImageFont.truetype(FONT, 30), fill=(250, 250, 250), anchor='mm')
    d.ellipse([58, 90, 198, 230], fill=(245, 245, 245))
    emblem(d, 128, 160, 60, (30, 30, 30), 7)
    d.text((128, 300), 'TO PROTECT YOU', font=ImageFont.truetype(FONT, 26), fill=(250, 250, 250), anchor='mm')
    save_map(im, 'indev_b24poster.png')


def stairs():
    im = Image.new('RGB', (256, 256), (6, 6, 6))
    d = ImageDraw.Draw(im)
    for k in range(9):
        y = 250 - k * 16
        w = 120 - k * 11
        g = max(10, 90 - k * 10)
        d.rectangle([128 - w, y - 14, 128 + w, y], fill=(g, g, g))
    d.ellipse([122, 70, 134, 84], fill=(160, 160, 150))           # a pale face, far down
    save_map(im.filter(ImageFilter.GaussianBlur(1.2)), 'indev_b24stair.png')


if __name__ == '__main__':
    for n, cls, kind, col, *_ in SCPS:
        if kind == 'poster':
            im = Image.new('RGB', (128, 128), col)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, 127, 127], outline=(40, 30, 20), width=10)
            d.text((64, 64), 'SCP-' + n, font=ImageFont.truetype(FONT, 22), fill=(20, 20, 20), anchor='mm')
            save_map(im, 'indev_b24_%s.png' % n)
        else:
            flat('indev_b24_%s.png' % n, col, 12, 64)
    banner()
    poster()
    stairs()
    print('batch 24 textures written')
