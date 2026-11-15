r"""Textures of the thirty-fifth batch (original, drawn here), after the user's reference images 107-114:
  indev_b35plac.png / indev_b35scr.png   placards and record screens (the batch-34 drawing code, our table)
  indev_b35bars.png     the upper tier of barred cells (ref. 108): grey steel bars, the cell beyond dark
  indev_b35logo.png     the Foundation emblem painted on the cell block floor (ref. 108) - drawn as a plain ring with
                        three inward arrows (our own emblem, as on Site-42's plaque)
  indev_b35conc.png     board-marked bunker concrete with tie holes (ref. 111) for walls, pillars and the ceiling
  indev_b35lamp.png     the oval bulkhead wall lamp (ref. 111)
  indev_b35stone.png    old dark stone with damp and moss (ref. 110)
  indev_b35crate.png    cardboard boxes and pallet wood (ref. 109)
   python make_assets35.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
import make_assets34 as A
import data35

RND = random.Random(35)


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def renamed(fn, src, dst):
    fn()
    os.replace(os.path.join(MAPDIR, src), os.path.join(MAPDIR, dst))


def bars():
    im = Image.new('RGB', (512, 256), (14, 14, 16))
    d = ImageDraw.Draw(im)
    for cell in range(4):                                   # four cells: bars, a door frame, a slot, a bunk inside
        x0 = cell * 128
        d.rectangle([x0 + 10, 150, x0 + 118, 170], fill=(40, 40, 44))
        for x in range(x0 + 6, x0 + 128, 12):
            d.rectangle([x, 0, x + 4, 256], fill=(170, 172, 168))
        d.rectangle([x0, 0, x0 + 6, 256], fill=(150, 152, 150))
        d.rectangle([x0, 100, x0 + 128, 108], fill=(160, 162, 158))
        d.rectangle([x0 + 50, 110, x0 + 78, 122], fill=(90, 90, 92))
    d.rectangle([0, 0, 512, 10], fill=(150, 152, 150))
    d.rectangle([0, 246, 512, 256], fill=(150, 152, 150))
    save(im.filter(ImageFilter.GaussianBlur(0.4)), 'indev_b35bars.png')


def logo():
    im = Image.fromarray(np.clip(np.random.default_rng(351).normal(0, 6, (512, 512, 1)) + np.array((150, 148, 144)), 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    cx = cy = 256
    col = (40, 40, 44)
    d.ellipse([cx - 230, cy - 230, cx + 230, cy + 230], outline=col, width=26)
    d.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], outline=col, width=18)
    for k in range(3):
        a = math.radians(90 + k * 120)
        x0, y0 = cx + math.cos(a) * 225, cy - math.sin(a) * 225
        x1, y1 = cx + math.cos(a) * 60, cy - math.sin(a) * 60
        d.line([(x0, y0), (x1, y1)], fill=col, width=22)
        b1, b2 = a + 2.5, a - 2.5
        d.polygon([(x1, y1), (x1 + math.cos(b1) * 60, y1 - math.sin(b1) * 60), (x1 + math.cos(b2) * 60, y1 - math.sin(b2) * 60)], fill=col)
    save(im.filter(ImageFilter.GaussianBlur(1.0)), 'indev_b35logo.png')


def concrete():
    """ref. 111: board-marked concrete, horizontal formwork lines, rows of tie holes, damp streaks"""
    W = 512
    a = np.random.default_rng(352).normal(0, 9, (W, W, 1)) + np.array((138, 132, 118))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    d = ImageDraw.Draw(im)
    for y in range(0, W, 64):
        d.line([(0, y + RND.randint(-2, 2)), (W, y + RND.randint(-2, 2))], fill=(116, 110, 98), width=2)
        for x in range(32, W, 96):
            d.ellipse([x - 4, y + 28, x + 4, y + 36], fill=(70, 66, 58))
    for _ in range(25):
        x = RND.randrange(W)
        d.line([(x, 0), (x + RND.randint(-6, 6), RND.randint(60, 300))], fill=(118, 112, 100), width=RND.randint(2, 6))
    save(im.filter(ImageFilter.GaussianBlur(0.6)), 'indev_b35conc.png')


def lamp():
    im = Image.new('RGB', (128, 96), (40, 40, 38))
    d = ImageDraw.Draw(im)
    d.ellipse([8, 8, 120, 88], fill=(80, 78, 70))
    d.ellipse([18, 16, 110, 80], fill=(255, 244, 210))
    d.ellipse([34, 28, 94, 68], fill=(255, 255, 240))
    save(im, 'indev_b35lamp.png')


def stone():
    """ref. 110: old dark stone with damp streaks and black moss along the top"""
    W = 512
    a = np.random.default_rng(353).normal(0, 14, (W, W, 1)) + np.array((70, 74, 72))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.0))
    d = ImageDraw.Draw(im)
    for _ in range(40):
        x, y = RND.randrange(W), RND.randrange(W)
        d.line([(x, y), (x + RND.randint(-40, 40), y + RND.randint(-10, 30))], fill=(40, 44, 42), width=2)
    for _ in range(60):
        x = RND.randrange(W)
        d.ellipse([x - 20, -10, x + 20, RND.randint(30, 140)], fill=(18, 22, 18))
    for _ in range(18):
        x = RND.randrange(W)
        d.ellipse([x - 30, W - RND.randint(40, 90), x + 30, W + 10], fill=(70, 46, 36))
    save(im.filter(ImageFilter.GaussianBlur(1.4)), 'indev_b35stone.png')


def crate():
    im = Image.new('RGB', (256, 256), (150, 114, 70))
    d = ImageDraw.Draw(im)
    for _ in range(300):
        x, y = RND.randrange(256), RND.randrange(256)
        d.point((x, y), fill=(120, 90, 54))
    d.line([(0, 128), (256, 128)], fill=(196, 170, 120), width=10)                  # packing tape
    d.rectangle([20, 160, 110, 210], fill=(230, 226, 214))
    d.text((24, 168), 'DEEP STOR.', fill=(30, 30, 30))
    d.rectangle([0, 0, 255, 255], outline=(110, 82, 50), width=4)
    save(im, 'indev_b35crate.png')


def signs():
    """the batch-34 sign sheet with STORAGE AREA 10 and 11 in the two top cells"""
    from PIL import ImageFont
    sheet = Image.open(os.path.join(MAPDIR, 'indev_b34signs.png')).convert('RGB')
    for k, n in enumerate(('10', '11')):
        im = Image.new('RGB', (512, 128), (24, 24, 24))
        d = ImageDraw.Draw(im)
        d.rectangle([4, 4, 507, 123], outline=(200, 200, 200), width=3)
        d.text((256, 46), 'STORAGE AREA', font=A.F(44), fill=(235, 235, 235), anchor='mm')
        d.text((256, 96), n, font=A.F(36), fill=(235, 235, 235), anchor='mm')
        sheet.paste(im, (k * 512, 0))
    save(sheet, 'indev_b35signs.png')


if __name__ == '__main__':
    signs()
    A.U = data35.U
    A.SCREENS = [u for u in data35.U if u['unit'] == 'screen']
    renamed(A.placards, 'indev_b34plac.png', 'indev_b35plac.png')
    renamed(A.screens, 'indev_b34scr.png', 'indev_b35scr.png')
    import importlib
    importlib.reload(A)                                     # put batch 34's own atlases back exactly as they were
    A.placards()
    A.screens()
    bars()
    logo()
    concrete()
    lamp()
    stone()
    crate()
    print('batch 35 textures written')
