r"""Textures of the forty-fifth batch (the old SCP-939 chamber, the Morgue, the Off-Shoot Hall, the damaged wing).
Everything else reuses existing textures (concrete, metal panels, tiles, rust, glass, the dust sheets).
  indev_b45drawers.png  512  a wall of morgue cold-storage drawers: steel doors, handles, name-card slots
  indev_b45crack.png    256  a cracked window (alpha): spider cracks, a hole punched through
  indev_b45flame.png    128  small flames licking out of a door seam (alpha, emissive)
  indev_b45hole.png     256  a hole in the floor: broken concrete lip, black below (alpha)
  indev_b45panel.png    512  the old 939 chamber's dark ribbed wall panels with a rust band (ref. 225)
   python make_assets45.py"""
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


def drawers():
    rnd = random.Random(451)
    im = noise(512, 512, (150, 154, 156), 6, 452, 0.6)
    d = ImageDraw.Draw(im)
    for r in range(4):
        for c in range(4):
            x0, y0 = c * 128 + 6, r * 128 + 6
            d.rectangle((x0, y0, x0 + 116, y0 + 116), fill=(170, 174, 176), outline=(70, 72, 74), width=4)
            d.rectangle((x0 + 40, y0 + 70, x0 + 76, y0 + 82), fill=(60, 62, 64))
            d.rectangle((x0 + 34, y0 + 24, x0 + 82, y0 + 44), fill=(230, 226, 205), outline=(60, 60, 60))
            if rnd.random() < 0.6:
                d.text((x0 + 38, y0 + 26), rnd.choice(('D-1166', 'D-2903', 'J.DOE', 'D-4471', 'UNKNOWN', 'D-0815')), font=F(11), fill=(20, 20, 20))
    save(im, 'indev_b45drawers.png')


def crack():
    rnd = random.Random(453)
    im = Image.new('RGBA', (256, 256), (180, 200, 210, 60))
    d = ImageDraw.Draw(im)
    cx, cy = 150, 110
    d.ellipse((cx - 22, cy - 18, cx + 22, cy + 18), fill=(10, 10, 12, 230))
    for k in range(16):
        a = rnd.uniform(0, 6.28)
        x, y = cx, cy
        for _ in range(6):
            nx, ny = x + np.cos(a) * rnd.uniform(10, 30), y + np.sin(a) * rnd.uniform(10, 30)
            d.line((x, y, nx, ny), fill=(240, 245, 250, 220), width=2)
            x, y, a = nx, ny, a + rnd.uniform(-0.4, 0.4)
    for r in (40, 70, 100):
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), outline=(230, 236, 240, 120), width=1)
    save(im, 'indev_b45crack.png')


def flame():
    im = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rnd = random.Random(454)
    for _ in range(14):
        x = rnd.uniform(20, 108)
        h = rnd.uniform(30, 90)
        d.polygon(((x - 8, 128), (x + 8, 128), (x + rnd.uniform(-4, 4), 128 - h)), fill=(255, rnd.randint(110, 190), 30, 220))
    save(im.filter(ImageFilter.GaussianBlur(2)), 'indev_b45flame.png')


def hole():
    rnd = random.Random(455)
    im = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for k in range(18):
        a = k / 18 * 6.283
        r = rnd.uniform(90, 120)
        pts.append((128 + r * np.cos(a), 128 + r * np.sin(a)))
    d.polygon(pts, fill=(70, 70, 66, 255))
    pts2 = [(128 + (x - 128) * 0.8, 128 + (y - 128) * 0.8) for (x, y) in pts]
    d.polygon(pts2, fill=(2, 2, 2, 255))
    save(im, 'indev_b45hole.png')


def panel():
    im = noise(512, 512, (54, 52, 50), 8, 456, 0.8)
    d = ImageDraw.Draw(im)
    for x in range(0, 512, 64):
        d.line((x, 0, x, 512), fill=(30, 30, 30), width=5)
        d.line((x + 6, 0, x + 6, 512), fill=(80, 78, 74), width=2)
    for y in (128, 384):
        d.line((0, y, 512, y), fill=(32, 32, 32), width=4)
    d.rectangle((0, 440, 512, 512), fill=(110, 60, 40))                     # the rust band
    for x in range(0, 512, 32):
        d.line((x, 440, x, 512), fill=(80, 40, 28), width=2)
    save(im, 'indev_b45panel.png')


if __name__ == '__main__':
    for fn in (drawers, crack, flame, hole, panel):
        fn()
        print(fn.__name__)
