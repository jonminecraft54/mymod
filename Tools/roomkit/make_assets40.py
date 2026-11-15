r"""Textures of the fortieth batch - the Residential Sector. The facility parts reuse the original concrete,
tiles, lights and doors; these are only the household surfaces the game has nothing for.
  indev_b40paper1.png   512  faded floral wallpaper with a wainscot band
  indev_b40paper2.png   512  striped wallpaper, water-stained
  indev_b40door.png     256  a panelled wooden house door (decal: the residential hallway's many doors, 1197-1)
  indev_b40tv.png       256  a television showing static and a test card (emissive)
  indev_b40drawing.png  256  crayon drawings taped up (house, family, a bird, a man in a black uniform)
  indev_b40labels.png   512  storage box sides with strange inventory labels
  indev_b40sheet.png    256  dust sheets: off-white cloth, folds and dust
   python make_assets40.py"""
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def noise(w, h, base, amp, seed, blur=1.0):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def paper1():
    rnd = random.Random(401)
    im = noise(512, 512, (196, 184, 160), 6, 4011, 1.0)
    d = ImageDraw.Draw(im, 'RGBA')
    for y in range(0, 360, 60):
        for x in range(0, 512, 64):
            cx, cy = x + (32 if (y // 60) % 2 else 0), y + 30
            for a in range(5):
                v = np.radians(a * 72)
                d.ellipse((cx + 10 * np.cos(v) - 6, cy + 10 * np.sin(v) - 6, cx + 10 * np.cos(v) + 6, cy + 10 * np.sin(v) + 6), fill=(170, 110, 100, 150))
            d.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(200, 170, 80, 200))
            d.line((cx, cy + 10, cx - 8, cy + 26), fill=(110, 130, 90, 160), width=2)
    d.rectangle((0, 360, 512, 372), fill=(120, 90, 60, 255))                 # dado rail
    d.rectangle((0, 372, 512, 512), fill=(130, 140, 120, 255))               # painted wainscot
    for _ in range(12):
        x, y = rnd.uniform(0, 512), rnd.uniform(0, 512)
        d.ellipse((x - 40, y - 60, x + 40, y + 60), fill=(120, 100, 60, 18))
    save(im, 'indev_b40paper1.png')


def paper2():
    rnd = random.Random(402)
    im = Image.new('RGB', (512, 512), (178, 190, 196))
    d = ImageDraw.Draw(im, 'RGBA')
    for x in range(0, 512, 32):
        d.rectangle((x, 0, x + 10, 512), fill=(150, 166, 176, 255))
    for _ in range(6):
        x = rnd.uniform(0, 512)
        d.rectangle((x, 0, x + rnd.uniform(20, 60), rnd.uniform(100, 400)), fill=(130, 110, 70, 30))
    save(Image.blend(im, noise(512, 512, (170, 170, 170), 20, 4021), 0.12), 'indev_b40paper2.png')


def door():
    im = noise(256, 512, (120, 76, 44), 8, 403, 0.8)
    d = ImageDraw.Draw(im)
    for y in range(0, 512, 6):
        d.line((0, y, 256, y + 2), fill=(108, 68, 40), width=1)
    for (x0, y0, x1, y1) in ((30, 30, 120, 230), (136, 30, 226, 230), (30, 270, 120, 480), (136, 270, 226, 480)):
        d.rectangle((x0, y0, x1, y1), outline=(80, 50, 30), width=6)
    d.ellipse((200, 250, 220, 270), fill=(200, 170, 80))
    save(im, 'indev_b40door.png')


def tv():
    a = np.random.default_rng(404).integers(30, 230, (256, 256, 1)).astype(np.uint8)
    im = Image.fromarray(np.repeat(a, 3, 2))
    d = ImageDraw.Draw(im)
    for k, c in enumerate(((200, 200, 200), (200, 200, 40), (40, 200, 200), (40, 200, 40), (200, 40, 200), (200, 40, 40), (40, 40, 200))):
        d.rectangle((40 + k * 25, 70, 64 + k * 25, 160), fill=c)
    d.text((56, 176), 'PLEASE STAND BY', font=F(16), fill=(240, 240, 240))
    save(im.filter(ImageFilter.GaussianBlur(0.6)), 'indev_b40tv.png')


def drawing():
    im = Image.new('RGB', (256, 256), (230, 226, 210))
    d = ImageDraw.Draw(im)
    d.polygon(((30, 120), (80, 70), (130, 120)), outline=(200, 40, 40), width=4)   # a house
    d.rectangle((40, 120, 120, 190), outline=(60, 60, 200), width=4)
    for k, x in enumerate((160, 190, 220)):                                     # a family
        d.ellipse((x - 8, 120, x + 8, 136), outline=(30, 30, 30), width=3)
        d.line((x, 136, x, 180), fill=(30, 30, 30), width=3)
    d.ellipse((150, 30, 190, 60), outline=(120, 120, 120), width=4)             # a grey bird, red crest
    d.line((182, 34, 196, 20), fill=(220, 40, 40), width=5)
    d.text((24, 214), 'i wana go hom', font=F(18), fill=(40, 40, 160))
    save(im, 'indev_b40drawing.png')


LABELS = ['SPARE WINTER COATS (14)', 'TEXTBOOKS - DO NOT OPEN', 'XMAS LIGHTS (TANGLED)', 'PHOTOS 1987-1991',
          'THINGS THAT HUM', 'MOM\'S GOOD PLATES', 'TOYS (QUIET ONES)', 'DO NOT STACK - IT MINDS']


def labels():
    im = Image.new('RGB', (512, 512), (160, 120, 80))
    d = ImageDraw.Draw(im)
    for i, t in enumerate(LABELS):
        x0, y0 = (i % 2) * 256, (i // 2) * 128
        d.rectangle((x0 + 2, y0 + 2, x0 + 253, y0 + 125), fill=(170, 128, 84), outline=(110, 80, 50), width=3)
        d.line((x0 + 2, y0 + 62, x0 + 253, y0 + 62), fill=(140, 120, 90), width=8)   # packing tape
        d.text((x0 + 14, y0 + 82), t, font=F(15), fill=(20, 20, 20))
    save(im, 'indev_b40labels.png')


def sheet():
    im = noise(256, 256, (214, 208, 196), 6, 405, 1.4)
    d = ImageDraw.Draw(im, 'RGBA')
    for k in range(9):
        x = 20 + k * 28
        d.line((x, 0, x + 30, 256), fill=(170, 164, 150, 80), width=6)
    save(im, 'indev_b40sheet.png')


if __name__ == '__main__':
    for fn in (paper1, paper2, door, tv, drawing, labels, sheet):
        fn()
        print(fn.__name__)
