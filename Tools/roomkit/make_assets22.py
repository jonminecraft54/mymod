"""Textures of SCP-112-PT's room (original, drawn here):
     GFX\\map\\indev_112robe.png              the faded red bishop's robe with gold trim
     GFX\\map\\indev_112giftr.png, _giftg.png  wrapped presents
     GFX\\npcs\\indev_112spirit.jpg           SCP-112-PT-1: classd1.jpg recoloured to a red robe, white hair and beard tone
   python make_assets22.py"""
import os
from PIL import Image, ImageDraw
from make_assets5 import save_map
from make_assets20 import ROOT


def robe():
    im = Image.new('RGB', (128, 128), (120, 26, 24))
    d = ImageDraw.Draw(im)
    for x in (20, 64, 108):
        d.rectangle([x - 5, 0, x + 5, 127], fill=(190, 150, 60))
    d.line([(0, 64), (127, 64)], fill=(220, 210, 190), width=8)
    save_map(im, 'indev_112robe.png')


def gift(name, rgb):
    im = Image.new('RGB', (64, 64), rgb)
    d = ImageDraw.Draw(im)
    d.rectangle([28, 0, 36, 63], fill=(240, 220, 90))
    d.rectangle([0, 28, 63, 36], fill=(240, 220, 90))
    save_map(im, name)


def spirit():
    im = Image.open(os.path.join(ROOT, 'GFX', 'npcs', 'classd1.jpg')).convert('RGB')
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b = px[x, y]
            if r > 120 and r > g * 1.25 and g > b:               # the orange suit -> a deep red robe
                v = (r + g) / 2
                px[x, y] = (int(v * 0.8), int(v * 0.12), int(v * 0.1))
            elif r < 70 and g < 70 and b < 70:                    # dark hair and shoes -> white, like an old man's hair
                px[x, y] = (226, 224, 220)
    im.save(os.path.join(ROOT, 'GFX', 'npcs', 'indev_112spirit.jpg'), quality=92)


if __name__ == '__main__':
    robe()
    gift('indev_112giftr.png', (170, 30, 34))
    gift('indev_112giftg.png', (30, 120, 50))
    spirit()
    print('batch 22 textures written')
