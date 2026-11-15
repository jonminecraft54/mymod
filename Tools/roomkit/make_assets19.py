"""Textures of the nineteenth batch (from the reference images of 23 Oct 2026):
     GFX\\map\\indev_plates19.png (+ plates19.json)   room plates: OFFICE 19-A, HOIST CONTROL, STORAGE ...
     GFX\\map\\indev_shutter19.png                     a ribbed roll-up storage door (original, drawn here)
     GFX\\map\\indev_h09_0..2.png, indev_h09_x.png     SCP-H09's neon emblem frames (the user's images 15-18)
     GFX\\map\\indev_poster19.png                      the emblem poster in the cell block (the user's image 14)
     GFX\\map\\indev_river19a.png, _b.png              two framed photographs in the office (the user's images 10, 11)
   python make_assets19.py [image folder]"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_assets5 import save_map

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\arialbd.ttf"
IMG = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Computer\AppData\Local\Temp\claude\I--MythicalC-v1-2-7-v0-1-scpcb-dx9\bb8674a5-7deb-456c-b97b-7e5d757ed7a7\images"
PLATES = [('office', 'OFFICE 19-A'), ('hoist', 'HOIST CONTROL'), ('pit', 'HOIST PIT'), ('storage', 'STORAGE B'),
          ('h09', 'SCP-H09'), ('cells', 'CELL BLOCK D'), ('gallery', 'OBSERVATION'), ('cellA', 'D-19A'), ('cellB', 'D-19B')]


def plates():
    W = H = 512
    im = Image.new('RGB', (W, H), (30, 30, 32))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (k, text) in enumerate(PLATES):
        x, y = (i % 3) * 170, (i // 3) * 128
        rects[k] = (x / W, y / H, min(x + 168, W) / W, min(y + 124, H) / H)
        d.rectangle([x + 4, y + 4, x + 164, y + 120], fill=(24, 24, 24), outline=(150, 150, 150), width=4)
        size = 40
        while d.textlength(text, font=ImageFont.truetype(FONT, size)) > 146:
            size -= 2
        d.text((x + 84, y + 62), text, font=ImageFont.truetype(FONT, size), fill=(232, 232, 226), anchor='mm')
    save_map(im, 'indev_plates19.png')
    json.dump(rects, open(os.path.join(HERE, 'plates19.json'), 'w'), indent=1)


def shutter():
    im = Image.new('RGB', (256, 512), (96, 98, 96))
    d = ImageDraw.Draw(im)
    for y in range(0, 512, 24):
        d.rectangle([0, y, 255, y + 19], fill=(112, 114, 112))
        d.line([(0, y + 20), (255, y + 20)], fill=(58, 60, 58), width=3)
        d.line([(0, y + 1), (255, y + 1)], fill=(140, 142, 140), width=1)
    d.rectangle([0, 0, 255, 511], outline=(20, 20, 20), width=14)
    d.rectangle([20, 470, 236, 492], fill=(40, 40, 40))
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    save_map(im, 'indev_shutter19.png')


def photo(src, name, size=(512, 512), frame=True):
    im = Image.open(os.path.join(IMG, src)).convert('RGB')
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize(size, Image.LANCZOS)
    if frame:
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, size[0] - 1, size[1] - 1], outline=(46, 34, 24), width=24)
    save_map(im, name)


if __name__ == '__main__':
    plates()
    shutter()
    for i, src in enumerate(('15.png', '16.png', '17.png')):
        photo(src, 'indev_h09_%d.png' % i, frame=False)
    photo('18.png', 'indev_h09_x.png', frame=False)
    photo('14.png', 'indev_poster19.png')
    photo('10.jpg', 'indev_river19a.png')
    photo('11.jpg', 'indev_river19b.png')
    print('batch 19 textures written')
