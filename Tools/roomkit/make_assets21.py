"""Textures of the twenty-first batch, original, drawn here:
     GFX\\map\\indev_b21green.png  leaves      indev_b21water.png  the pool's water
     GFX\\map\\indev_b21wave.png   SCP-151's painting of a wave      indev_b21tv.png  SCP-1981's static screen
   python make_assets21.py"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import save_map
from make_assets20 import flat


def wave():
    W, H = 512, 384
    im = Image.new('RGB', (W, H), (150, 170, 190))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(160 - 120 * t), int(180 - 110 * t), int(200 - 80 * t)))
    pts = [(x, 220 - 120 * math.exp(-((x - 300) / 90.0) ** 2) + 10 * math.sin(x / 18.0)) for x in range(0, W + 1, 4)]
    d.polygon(pts + [(W, H), (0, H)], fill=(20, 50, 80))
    d.line(pts, fill=(230, 240, 245), width=6)
    random.seed(151)
    for _ in range(300):
        x, y = random.randint(200, 420), random.randint(90, 240)
        d.ellipse([x, y, x + 3, y + 3], fill=(235, 245, 250))
    d.rectangle([0, 0, W - 1, H - 1], outline=(70, 50, 24), width=22)
    save_map(im.filter(ImageFilter.GaussianBlur(1.0)), 'indev_b21wave.png')


def tv():
    random.seed(1981)
    im = Image.new('RGB', (256, 192))
    px = im.load()
    for y in range(192):
        for x in range(256):
            v = random.randint(30, 200)
            px[x, y] = (v, v, v)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 255, 191], outline=(16, 16, 16), width=18)
    save_map(im, 'indev_b21tv.png')


if __name__ == '__main__':
    flat('indev_b21green.png', (40, 96, 36), 30, 128)
    flat('indev_b21water.png', (60, 140, 190), 12, 128)
    wave()
    tv()
    print('batch 21 textures written')
