r"""Textures of the thirty-seventh batch (original, drawn here), after the user's reference images 132-138 and the
SCP-028 / reactor / archive brief. 512 where it is seen up close, 1024 only for the big courtyard ground.
  indev_b37yard.png    1024  SCP-028's yard: cracked, stained concrete slabs, weeds in the joints
  indev_b37leaves.png   256  dead leaves (alpha), scattered on the yard
  indev_b37poster.png   512  the red poster "WE ARE HERE TO PROTECT YOU" (ref. 132)
  indev_b37water.png    256  heavy water with the Cherenkov glow (scrolled at runtime)
  indev_b37reactor.png  512  reactor hall wall: riveted steel, a yellow-black band
  indev_b37files.png    512  the face of a motorised filing shelf: drawers, label slots, handles
  indev_b37plaster.png  512  a cell's cracked white plaster (ref. 138)
  indev_b37lift.png     512  service lift panel: call buttons, floor plate, LIFT stencil
   python make_assets37.py"""
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


def cracks(d, rnd, n, w, h, col, width=2):
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        for _ in range(rnd.randint(6, 18)):
            nx, ny = x + rnd.uniform(-22, 22), y + rnd.uniform(-22, 22)
            d.line((x, y, nx, ny), fill=col, width=width)
            x, y = nx, ny


def yard():
    rnd = random.Random(281)
    im = noise(1024, 1024, (128, 126, 120), 14, 2801, 1.2)
    d = ImageDraw.Draw(im, 'RGBA')
    for k in range(40):                                                    # water stains and oil
        x, y, r = rnd.uniform(0, 1024), rnd.uniform(0, 1024), rnd.uniform(30, 140)
        d.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=(60, 58, 50, rnd.randint(14, 40)))
    for i in range(0, 1025, 256):                                          # the slab joints, weeds in them
        d.line((i, 0, i, 1024), fill=(52, 50, 46, 255), width=5)
        d.line((0, i, 1024, i), fill=(52, 50, 46, 255), width=5)
        for _ in range(30):
            t = rnd.uniform(0, 1024)
            for (x, y) in ((i, t), (t, i)):
                d.line((x, y, x + rnd.uniform(-8, 8), y - rnd.uniform(4, 14)), fill=(70, 78, 44, 200), width=2)
    cracks(d, rnd, 70, 1024, 1024, (40, 38, 34, 220))
    save(im.filter(ImageFilter.SMOOTH), 'indev_b37yard.png')


def leaves():
    rnd = random.Random(282)
    im = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(46):
        x, y, s = rnd.uniform(10, 246), rnd.uniform(10, 246), rnd.uniform(6, 14)
        c = rnd.choice(((96, 66, 34), (120, 84, 40), (74, 52, 30), (110, 96, 52)))
        d.ellipse((x - s, y - s * 0.55, x + s, y + s * 0.55), fill=c + (235,))
        d.line((x - s, y, x + s, y), fill=(50, 34, 20, 255), width=1)
    save(im, 'indev_b37leaves.png')


def poster():
    im = Image.new('RGB', (512, 512), (176, 26, 22))
    d = ImageDraw.Draw(im)
    d.rectangle((14, 14, 497, 497), outline=(230, 220, 210), width=6)
    cx, cy = 256, 196                                                      # a plain ring emblem (not a real logo)
    d.ellipse((cx - 110, cy - 110, cx + 110, cy + 110), outline=(240, 236, 230), width=14)
    d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), outline=(240, 236, 230), width=10)
    for a in (0, 120, 240):
        v = np.radians(a - 90)
        d.line((cx + 60 * np.cos(v), cy + 60 * np.sin(v), cx + 120 * np.cos(v), cy + 120 * np.sin(v)), fill=(240, 236, 230), width=14)
    for i, (t, y, s) in enumerate((('WE ARE HERE', 352, 46), ('TO PROTECT YOU', 408, 46), ('SECURE . CONTAIN . PROTECT', 466, 20))):
        f = F(s)
        w = d.textlength(t, font=f)
        d.text((256 - w / 2, y), t, font=f, fill=(244, 240, 232))
    im = Image.blend(im, noise(512, 512, (176, 160, 150), 22, 2803, 0.6), 0.12)
    save(im, 'indev_b37poster.png')


def water():
    x = np.linspace(0, 6.283, 256)
    X, Y = np.meshgrid(x, x)
    v = (np.sin(X * 3 + np.sin(Y * 2) * 1.4) + np.sin(Y * 4 + np.cos(X * 3)) * 0.8 + np.sin((X + Y) * 5) * 0.4)
    v = (v - v.min()) / (v.max() - v.min())
    rgb = np.stack([40 + 90 * v ** 3, 120 + 120 * v ** 2, 220 + 35 * v], -1)
    save(Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), 'indev_b37water.png')


def reactor():
    rnd = random.Random(283)
    im = noise(512, 512, (104, 108, 110), 9, 2804, 0.8)
    d = ImageDraw.Draw(im, 'RGBA')
    for i in range(0, 513, 128):
        d.line((i, 0, i, 512), fill=(40, 42, 44, 255), width=4)
    d.line((0, 256, 512, 256), fill=(40, 42, 44, 255), width=4)
    for i in range(0, 512, 128):
        for j in (8, 248, 264, 504):
            for k in range(8, 128, 30):
                d.ellipse((i + k - 3, j - 3, i + k + 3, j + 3), fill=(150, 150, 150, 255), outline=(50, 50, 50, 255))
    for k in range(0, 512, 48):                                            # the hazard band
        d.polygon(((k, 400), (k + 24, 400), (k + 48, 440), (k + 24, 440)), fill=(30, 30, 30, 255))
        d.polygon(((k + 24, 400), (k + 48, 400), (k + 72, 440), (k + 48, 440)), fill=(214, 170, 30, 255))
    for _ in range(30):
        x, y = rnd.uniform(0, 512), rnd.uniform(0, 512)
        d.line((x, y, x + rnd.uniform(-3, 3), y + rnd.uniform(20, 70)), fill=(110, 70, 40, 60), width=3)
    save(im, 'indev_b37reactor.png')


def files():
    im = noise(512, 512, (150, 152, 148), 6, 2805, 0.6)
    d = ImageDraw.Draw(im)
    f = F(14)
    rnd = random.Random(284)
    for r in range(8):
        for c in range(4):
            x0, y0 = c * 128 + 6, r * 64 + 5
            d.rectangle((x0, y0, x0 + 116, y0 + 54), fill=(170, 172, 166), outline=(70, 72, 70), width=2)
            d.rectangle((x0 + 38, y0 + 8, x0 + 78, y0 + 22), fill=(230, 226, 205), outline=(60, 60, 60))
            d.text((x0 + 42, y0 + 8), '%s-%03d' % ('ABCDEFGH'[r], rnd.randint(1, 999)), font=F(10), fill=(30, 30, 30))
            d.rectangle((x0 + 44, y0 + 34, x0 + 72, y0 + 40), fill=(60, 62, 64))
    save(im, 'indev_b37files.png')


def plaster():
    rnd = random.Random(285)
    im = noise(512, 512, (214, 214, 210), 7, 2806, 1.0)
    d = ImageDraw.Draw(im, 'RGBA')
    cracks(d, rnd, 26, 512, 512, (120, 120, 116, 150), 1)
    for _ in range(12):
        x, y = rnd.uniform(0, 512), rnd.uniform(0, 512)
        d.ellipse((x - 40, y - 30, x + 40, y + 30), fill=(150, 146, 136, 18))
    save(im, 'indev_b37plaster.png')


def lift():
    im = noise(512, 512, (120, 124, 126), 8, 2807, 0.7)
    d = ImageDraw.Draw(im)
    d.rectangle((150, 60, 362, 452), fill=(60, 62, 66), outline=(30, 30, 30), width=6)
    for k, (t, c) in enumerate((('UP', (60, 200, 90)), ('DOWN', (220, 160, 40)))):
        y = 140 + k * 140
        d.ellipse((216, y - 40, 296, y + 40), fill=c, outline=(20, 20, 20), width=5)
        w = d.textlength(t, font=F(26))
        d.text((256 - w / 2, y + 48), t, font=F(26), fill=(230, 230, 230))
    d.text((176, 400), 'SERVICE LIFT', font=F(26), fill=(240, 200, 60))
    save(im, 'indev_b37lift.png')


if __name__ == '__main__':
    for fn in (yard, leaves, poster, water, reactor, files, plaster, lift):
        fn()
        print(fn.__name__)
