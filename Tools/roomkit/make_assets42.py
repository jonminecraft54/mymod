r"""Textures of the forty-second batch (the Panopticon, the Toy Box, the Vault, the Cellar). Walls, tiles,
glass, metal and doors reuse the existing ones; these are the pieces nothing else could do.
  indev_b42vault.png    512  a round vault door: spoked wheel, bolts, a numbered dial
  indev_b42charge.png   256  a demolition charge strapped to the tunnel wall: blocks, wires, a red tag
  indev_b42rack.png     512  backup server racks: drive bays, blinking LEDs (emissive)
  indev_b42fridge.png   256  SCP-4139's door: six crude magnet drawings and a combination lock
  indev_b42veins.jpg    256  SCP-466-2's skin: pale, crossed by swollen dark vessels (an NPC skin)
  indev_b42floor.png    512  the panopticon floor emblem (ring and arrows on worn concrete; not a real logo)
  GFX\items\flare1577.png, bracelets154.png   item texture overrides
   python make_assets42.py"""
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F

ITEMS = os.path.join(os.path.dirname(MAPDIR), 'items')
NPCS = os.path.join(os.path.dirname(MAPDIR), 'npcs')


def save(im, name, d=MAPDIR):
    im.save(os.path.join(d, name))


def noise(w, h, base, amp, seed, blur=1.0):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def vault():
    im = noise(512, 512, (60, 62, 66), 8, 421, 0.8)
    d = ImageDraw.Draw(im)
    d.ellipse((16, 16, 496, 496), fill=(120, 124, 128), outline=(40, 40, 44), width=14)
    d.ellipse((60, 60, 452, 452), outline=(80, 82, 86), width=8)
    for k in range(24):
        a = np.radians(k * 15)
        x, y = 256 + 215 * np.cos(a), 256 + 215 * np.sin(a)
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(70, 72, 76), outline=(30, 30, 30))
    d.ellipse((176, 176, 336, 336), outline=(50, 50, 54), width=12)
    for k in range(6):
        a = np.radians(k * 60)
        d.line((256, 256, 256 + 110 * np.cos(a), 256 + 110 * np.sin(a)), fill=(50, 50, 54), width=14)
    d.ellipse((236, 236, 276, 276), fill=(180, 160, 90))
    for k in range(10):
        a = np.radians(k * 36 - 90)
        d.text((256 + 60 * np.cos(a) - 6, 380 + 0 * np.sin(a) + k * 0), '', font=F(10))
    save(im, 'indev_b42vault.png')


def charge():
    im = Image.new('RGB', (256, 256), (70, 72, 70))
    d = ImageDraw.Draw(im)
    for k in range(3):
        d.rectangle((40 + k * 60, 70, 92 + k * 60, 190), fill=(190, 180, 140), outline=(80, 70, 50), width=3)
    d.rectangle((30, 120, 226, 136), fill=(40, 40, 40))                  # the strap
    for k in range(4):
        d.line((60 + k * 40, 70, 128, 20), fill=(200, 30, 30) if k % 2 else (230, 230, 230), width=3)
    d.rectangle((96, 200, 160, 236), fill=(200, 30, 30))
    d.text((100, 208), 'E-BLK', font=F(14), fill=(250, 250, 250))
    save(im, 'indev_b42charge.png')


def rack():
    rnd = random.Random(423)
    im = Image.new('RGB', (512, 512), (24, 26, 28))
    d = ImageDraw.Draw(im)
    for c in range(2):
        x0 = 10 + c * 252
        d.rectangle((x0, 10, x0 + 240, 502), fill=(40, 42, 46), outline=(70, 72, 76), width=4)
        for r in range(20):
            y = 24 + r * 24
            d.rectangle((x0 + 12, y, x0 + 228, y + 18), fill=(56, 58, 62))
            for k in range(4):
                col = rnd.choice(((60, 220, 90), (60, 220, 90), (240, 180, 40), (40, 40, 40)))
                d.ellipse((x0 + 190 + k * 8, y + 6, x0 + 195 + k * 8, y + 11), fill=col)
    save(im, 'indev_b42rack.png')


def fridge():
    im = Image.new('RGB', (256, 512), (232, 232, 226))
    d = ImageDraw.Draw(im)
    d.line((0, 190, 256, 190), fill=(150, 150, 150), width=4)
    d.rectangle((226, 230, 240, 330), fill=(180, 180, 180))
    for k, (x, y) in enumerate(((30, 30), (130, 40), (40, 240), (120, 230), (40, 370), (130, 380))):
        d.rectangle((x, y, x + 80, y + 90), fill=(250, 248, 236), outline=(200, 200, 190))
        d.ellipse((x + 30, y - 6, x + 46, y + 10), fill=(200, 40, 40))           # the magnet
        if k == 0:
            d.line((x + 10, y + 70, x + 70, y + 70), fill=(60, 160, 60), width=3)   # a picnic
            d.ellipse((x + 20, y + 30, x + 34, y + 44), outline=(30, 30, 30), width=2)
        elif k == 1:
            d.polygon(((x + 40, y + 15), (x + 55, y + 70), (x + 25, y + 70)), outline=(60, 60, 200), width=3)  # a rocket
        else:
            d.ellipse((x + 20, y + 20, x + 60, y + 60), outline=rnd_col(k), width=3)
    d.rectangle((100, 440, 156, 480), fill=(120, 120, 120))
    d.text((106, 450), '0-0-0', font=F(14), fill=(20, 20, 20))
    save(im, 'indev_b42fridge.png')


def rnd_col(k):
    return ((200, 60, 60), (60, 60, 200), (60, 160, 60), (160, 60, 160), (200, 140, 40), (30, 30, 30))[k % 6]


def veins():
    rnd = random.Random(466)
    im = noise(256, 256, (196, 170, 160), 8, 4661, 1.0)
    d = ImageDraw.Draw(im)
    for _ in range(40):
        x, y = rnd.uniform(0, 256), rnd.uniform(0, 256)
        w = rnd.randint(2, 6)
        for _ in range(rnd.randint(4, 10)):
            nx, ny = x + rnd.uniform(-20, 20), y + rnd.uniform(-20, 20)
            d.line((x, y, nx, ny), fill=(90, 20, 40), width=w)
            x, y = nx, ny
    os.makedirs(NPCS, exist_ok=True)
    im.convert('RGB').save(os.path.join(NPCS, 'indev_b42veins.jpg'), quality=90)


def floor():
    im = noise(512, 512, (176, 176, 170), 8, 424, 1.0)
    d = ImageDraw.Draw(im)
    d.ellipse((40, 40, 472, 472), outline=(50, 50, 52), width=22)
    d.ellipse((150, 150, 362, 362), outline=(50, 50, 52), width=16)
    for a in (90, 210, 330):
        v = np.radians(a)
        d.polygon(((256 + 100 * np.cos(v), 256 + 100 * np.sin(v)), (256 + 180 * np.cos(v - 0.2), 256 + 180 * np.sin(v - 0.2)),
                   (256 + 180 * np.cos(v + 0.2), 256 + 180 * np.sin(v + 0.2))), fill=(50, 50, 52))
    save(im, 'indev_b42floor.png')


def items():
    im = noise(128, 128, (220, 120, 30), 12, 425, 0.8)
    ImageDraw.Draw(im).rectangle((10, 50, 118, 78), fill=(40, 40, 40))
    save(im, 'flare1577.png', ITEMS)
    im = noise(128, 128, (170, 110, 50), 16, 426, 0.8)
    d = ImageDraw.Draw(im)
    for k in range(0, 128, 16):
        d.line((0, k, 128, k), fill=(120, 76, 30), width=3)
    save(im, 'bracelets154.png', ITEMS)


if __name__ == '__main__':
    for fn in (vault, charge, rack, fridge, veins, floor, items):
        fn()
        print(fn.__name__)
