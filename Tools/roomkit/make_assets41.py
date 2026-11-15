r"""Textures of the forty-first batch (staff, medical, security and recreation rooms from the community room ideas).
Walls, tiles, doors, lockers, desks, chairs, monitors, the vending machine and whiteboards are the originals.
  indev_b41blood.png    256  dried blood smears and drag marks (alpha)
  indev_b41gym.png      512  a gym's wooden floor with court lines
  indev_b41screen.png   512  the theatre screen: a burnt-out projection - a face made of static
  indev_b41xray.png     256  a lightbox of x-ray films (one ribcage is not human)
   python make_assets41.py"""
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def blood():
    rnd = random.Random(41)
    im = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(18):
        x, y, r = rnd.uniform(40, 216), rnd.uniform(40, 216), rnd.uniform(8, 30)
        d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=(90, 10, 8, rnd.randint(150, 230)))
    for _ in range(4):
        x, y = rnd.uniform(60, 200), rnd.uniform(60, 120)
        d.line((x, y, x + rnd.uniform(-20, 20), y + rnd.uniform(60, 120)), fill=(80, 8, 6, 200), width=rnd.randint(6, 14))
    save(im.filter(ImageFilter.GaussianBlur(1.2)), 'indev_b41blood.png')


def gym():
    im = Image.new('RGB', (512, 512), (176, 132, 82))
    d = ImageDraw.Draw(im)
    rnd = random.Random(42)
    for y in range(0, 512, 16):
        off = rnd.randint(0, 120)
        for x in range(-off, 512, 128):
            d.rectangle((x, y, x + 126, y + 14), fill=tuple(c + rnd.randint(-14, 14) for c in (176, 132, 82)))
    d.rectangle((20, 20, 492, 492), outline=(240, 236, 220), width=6)
    d.line((256, 20, 256, 492), fill=(240, 236, 220), width=6)
    d.ellipse((196, 196, 316, 316), outline=(240, 236, 220), width=6)
    d.arc((-120, 140, 140, 372), 270, 90, fill=(180, 40, 40), width=6)
    save(im, 'indev_b41gym.png')


def screen():
    a = np.random.default_rng(411).integers(120, 255, (512, 512, 1)).astype(np.uint8)
    im = Image.fromarray(np.repeat(a, 3, 2)).filter(ImageFilter.GaussianBlur(1))
    d = ImageDraw.Draw(im)
    d.ellipse((150, 120, 362, 392), outline=(30, 30, 30), width=10)          # a face drawn by the static
    d.ellipse((200, 200, 240, 236), fill=(20, 20, 20))
    d.ellipse((272, 200, 312, 236), fill=(20, 20, 20))
    d.arc((210, 270, 302, 340), 200, 340, fill=(20, 20, 20), width=8)
    save(im, 'indev_b41screen.png')


def xray():
    im = Image.new('RGB', (256, 256), (210, 230, 240))
    d = ImageDraw.Draw(im)
    for k in range(3):
        x0 = 8 + k * 84
        d.rectangle((x0, 20, x0 + 76, 236), fill=(30, 40, 50))
        d.line((x0 + 38, 40, x0 + 38, 220), fill=(200, 210, 220), width=4)
        n = 7 if k != 2 else 12                                             # the third has too many ribs
        for i in range(n):
            y = 60 + i * (140 / n)
            d.arc((x0 + 8, y - 6, x0 + 68, y + 18), 200, 340, fill=(200, 210, 220), width=3)
    save(im, 'indev_b41xray.png')


if __name__ == '__main__':
    for fn in (blood, gym, screen, xray):
        fn()
        print(fn.__name__)
