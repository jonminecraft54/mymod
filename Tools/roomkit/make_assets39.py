r"""Textures of the thirty-ninth batch - only what the existing ones cannot do (concrete, crates, the red SCP
stencil, tiles, wood, metal, glass are all reused).
  indev_b39brick.png    512  red-brown brick (the staff lounge fireplace, after the user's reference photo)
  indev_b39carpet.png   256  worn oatmeal carpet (the lounge)
  indev_b39honey.png    256  golden honey with slow streaks (SCP-1176-1, the sarcophagus)
  indev_b39mummy.png    256  dark, dry, resin-stained wrappings (SCP-1176)
  indev_b39green.png    128  pale green smelted metal (SCP-586)
  indev_b39scales.png   256  grey-green reptile scales (SCP-1013)
  indev_b39meter.png    128  an upside-down voltmeter dial that reads as a smile (SCP-1370's head)
  GFX\items\honey1176.png  the ration model's texture override for a jar of SCP-1176-1
   python make_assets39.py"""
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F

ITEMS = os.path.join(os.path.dirname(MAPDIR), 'items')


def save(im, name, d=MAPDIR):
    im.save(os.path.join(d, name))


def noise(w, h, base, amp, seed, blur=1.0):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def brick():
    rnd = random.Random(39)
    im = Image.new('RGB', (512, 512), (150, 146, 140))
    d = ImageDraw.Draw(im)
    for row in range(16):
        off = 0 if row % 2 == 0 else 32
        for col in range(-1, 9):
            x0, y0 = col * 64 + off, row * 32
            c = rnd.choice(((122, 62, 46), (134, 70, 52), (110, 56, 44), (140, 78, 58)))
            d.rectangle((x0 + 3, y0 + 3, x0 + 61, y0 + 29), fill=c)
    im = Image.blend(im, noise(512, 512, (128, 128, 128), 20, 391, 0.8), 0.15)
    save(im, 'indev_b39brick.png')


def carpet():
    save(noise(256, 256, (178, 166, 146), 16, 392, 0.7), 'indev_b39carpet.png')


def honey():
    y = np.linspace(0, 6.28, 256)[:, None]
    x = np.linspace(0, 6.28, 256)[None, :]
    v = 0.5 + 0.25 * np.sin(x * 3 + np.sin(y * 2)) + 0.25 * np.sin(y * 5 + x)
    rgb = np.stack([200 + 50 * v, 130 + 60 * v, 20 + 30 * v], -1)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))
    save(im, 'indev_b39honey.png')
    save(im.resize((128, 128)), 'honey1176.png', ITEMS)


def mummy():
    im = noise(256, 256, (84, 64, 44), 14, 393, 1.0)
    d = ImageDraw.Draw(im, 'RGBA')
    for k in range(0, 256, 9):
        d.line((0, k, 256, k + 20), fill=(60, 44, 30, 140), width=3)
    for _ in range(30):
        x, y = random.uniform(0, 256), random.uniform(0, 256)
        d.ellipse((x - 9, y - 6, x + 9, y + 6), fill=(190, 130, 40, 70))
    save(im, 'indev_b39mummy.png')


def green():
    save(noise(128, 128, (150, 176, 150), 14, 394, 1.2), 'indev_b39green.png')


def scales():
    im = noise(256, 256, (96, 104, 86), 8, 395, 0.6)
    d = ImageDraw.Draw(im)
    for r in range(0, 256, 12):
        for c in range(0, 256, 14):
            x = c + (7 if (r // 12) % 2 else 0)
            d.arc((x - 8, r - 6, x + 8, r + 10), 0, 180, fill=(60, 66, 54), width=2)
    save(im, 'indev_b39scales.png')


def meter():
    im = Image.new('RGB', (128, 128), (226, 222, 206))
    d = ImageDraw.Draw(im)
    d.rectangle((2, 2, 125, 125), outline=(40, 40, 40), width=6)
    d.arc((24, 4, 104, 84), 20, 160, fill=(30, 30, 30), width=4)       # the scale, upside down: a smile
    for k in range(9):
        a = np.radians(20 + k * 17.5)
        d.line((64 + 34 * np.cos(a), 44 + 34 * np.sin(a), 64 + 40 * np.cos(a), 44 + 40 * np.sin(a)), fill=(30, 30, 30), width=2)
    d.line((64, 44, 82, 80), fill=(190, 30, 30), width=3)
    d.text((44, 96), 'V', font=F(22), fill=(30, 30, 30))
    save(im.rotate(180), 'indev_b39meter.png')


if __name__ == '__main__':
    random.seed(39)
    for fn in (brick, carpet, honey, mummy, green, scales, meter):
        fn()
        print(fn.__name__)
