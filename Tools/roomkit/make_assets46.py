r"""Textures of the forty-sixth batch (the alternate timeline: the earlier breach).
Everything else reuses existing textures.
  indev_b49dust.png   256  decades of dust on a floor (alpha): grey drifts, footprint-free
  indev_b49map.png    512  a facility wall map with one whole sector struck out in black marker
  indev_b49sign.png   256  plain enamel signs: PERSONNEL LIFT / LOWER COMPLEX / CHECKPOINT (no logos)
   python make_assets46.py"""
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets45 import save, noise
from make_assets30 import F


def dust():
    a = np.random.default_rng(491).normal(0, 1, (256, 256)).astype(np.float32)
    im = Image.fromarray(((a - a.min()) / (a.max() - a.min()) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    al = np.asarray(im).astype(np.float32)
    al = np.clip((al - 90) * 1.6, 0, 170).astype(np.uint8)
    rgba = np.zeros((256, 256, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2], rgba[..., 3] = 150, 146, 138, al
    save(Image.fromarray(rgba, 'RGBA'), 'indev_b49dust.png')


def fmap():
    rnd = random.Random(492)
    im = noise(512, 512, (212, 206, 186), 5, 493, 0.7)
    d = ImageDraw.Draw(im)
    d.rectangle((8, 8, 504, 504), outline=(40, 40, 40), width=4)
    d.text((20, 16), 'SITE PLAN - LEVELS 1 TO 4', font=F(18), fill=(30, 30, 30))
    for _ in range(26):
        x, y = rnd.randint(30, 440), rnd.randint(60, 300)
        d.rectangle((x, y, x + rnd.randint(30, 70), y + rnd.randint(20, 50)), outline=(50, 50, 60), width=2)
    for _ in range(10):
        x, y = rnd.randint(30, 470), rnd.randint(60, 300)
        d.line((x, y, x + rnd.randint(-120, 120), y), fill=(70, 70, 80), width=3)
    d.rectangle((60, 330, 460, 480), fill=(18, 18, 18))                      # the sector struck out
    d.text((80, 340), 'SECTOR R - REMOVED', font=F(16), fill=(90, 90, 90))
    d.text((80, 450), 'by order, rev. 3', font=F(12), fill=(80, 80, 80))
    save(im, 'indev_b49map.png')


def sign():
    im = Image.new('RGB', (256, 256), (30, 34, 38))
    d = ImageDraw.Draw(im)
    for k, (txt, col) in enumerate((('PERSONNEL LIFT', (230, 200, 60)), ('LOWER COMPLEX', (210, 210, 210)),
                                    ('CHECKPOINT 9', (220, 70, 60)), ('SECTOR R', (120, 200, 140)))):
        y = k * 64
        d.rectangle((4, y + 4, 252, y + 60), outline=col, width=3)
        d.text((16, y + 20), txt, font=F(20), fill=col)
    save(im, 'indev_b49sign.png')


if __name__ == '__main__':
    for fn in (dust, fmap, sign):
        fn()
        print(fn.__name__)
