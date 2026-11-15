"""Textures of SCP-6483's quarters (original, drawn here):
     GFX\\map\\indev_6483mint.png   peppermint hard-candy wall (red and white diagonal stripes, glossy)
     GFX\\map\\indev_6483sra.png    the Scranton Reality Anchor monitor (ANCHOR: ACTIVE)
     GFX\\map\\indev_6483sraoff.png the same, switched off (ANCHOR: OFFLINE)
     GFX\\map\\indev_6483fire.png   the fire in the grate        GFX\\map\\indev_6483cloth.png  the tablecloth
   python make_assets23.py"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_assets5 import save_map

FONT = r"C:\Windows\Fonts\arialbd.ttf"


def mint():
    W = 256
    im = Image.new('RGB', (W, W), (246, 244, 240))
    d = ImageDraw.Draw(im)
    for k in range(-W, 2 * W, 64):
        d.polygon([(k, 0), (k + 28, 0), (k + 28 - W, W), (k - W, W)], fill=(196, 28, 36))
    im = im.filter(ImageFilter.GaussianBlur(1.2))
    d = ImageDraw.Draw(im)
    for y in range(0, W, 32):
        d.line([(0, y + 6), (W, y + 2)], fill=(255, 255, 255), width=1)   # a glossy sheen
    save_map(im, 'indev_6483mint.png')


def sra(on):
    im = Image.new('RGB', (256, 180), (22, 26, 24))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, 249, 173], outline=(90, 90, 86), width=6)
    d.text((128, 40), 'SRA-6483', font=ImageFont.truetype(FONT, 26), fill=(200, 200, 190), anchor='mm')
    d.text((128, 100), 'ANCHOR: ' + ('ACTIVE' if on else 'OFFLINE'), font=ImageFont.truetype(FONT, 24),
           fill=(80, 230, 90) if on else (240, 60, 50), anchor='mm')
    d.text((128, 145), 'Hume 1.00' if on else 'Hume 0.63', font=ImageFont.truetype(FONT, 20), fill=(150, 150, 140), anchor='mm')
    save_map(im, 'indev_6483sra.png' if on else 'indev_6483sraoff.png')


def fire():
    random.seed(6483)
    im = Image.new('RGB', (256, 160), (10, 6, 4))
    d = ImageDraw.Draw(im)
    for _ in range(90):
        x, h = random.randint(20, 236), random.randint(30, 120)
        c = random.choice([(255, 200, 60), (255, 140, 30), (230, 70, 20)])
        d.polygon([(x - 14, 160), (x + 14, 160), (x + random.randint(-8, 8), 160 - h)], fill=c)
    save_map(im.filter(ImageFilter.GaussianBlur(2.0)), 'indev_6483fire.png')


def cloth():
    im = Image.new('RGB', (128, 128), (150, 24, 30))
    d = ImageDraw.Draw(im)
    for k in range(0, 128, 32):
        d.rectangle([k, 0, k + 6, 127], fill=(30, 100, 50))
        d.rectangle([0, k, 127, k + 6], fill=(30, 100, 50))
    save_map(im, 'indev_6483cloth.png')


if __name__ == '__main__':
    mint()
    sra(True)
    sra(False)
    fire()
    cloth()
    print('batch 23 textures written')
