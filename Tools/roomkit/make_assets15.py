"""Textures and inventory icons of the usable items of the fifteenth batch (SCP-377, 978, 3041, 1337):
     GFX\\items\\cookie377.jpg, camera978.jpg, knife3041.jpg, sweater1337.jpg    model textures (the paper model)
     GFX\\items\\INVcookie377.png, INVcamera978.png, INVknife3041.png, INVsweater1337.png    inventory icons
   python make_assets15.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ITEMS = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\items"
rng = np.random.default_rng(15)


def noisy(base, amp, size=256):
    n = rng.random((size, size, 1)) * amp - amp / 2
    return np.clip(np.array(base, dtype=np.float64) + n, 0, 255).astype(np.uint8)


def cookie():
    im = Image.fromarray(noisy((196, 150, 84), 40), 'RGB').filter(ImageFilter.GaussianBlur(1))
    d = ImageDraw.Draw(im)
    d.line([(60, 128), (196, 128)], fill=(120, 80, 40), width=5)          # the fold
    im.save(os.path.join(ITEMS, 'cookie377.jpg'), quality=90)
    icon = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    ImageDraw.Draw(icon).ellipse([8, 14, 56, 50], fill=(205, 160, 90, 255), outline=(120, 80, 40, 255), width=2)
    icon.save(os.path.join(ITEMS, 'INVcookie377.png'))


def camera():
    im = Image.fromarray(noisy((34, 34, 36), 20), 'RGB')
    d = ImageDraw.Draw(im)
    d.rectangle([40, 150, 216, 230], fill=(170, 40, 36))                  # the red body stripe
    d.ellipse([84, 60, 172, 148], fill=(18, 18, 20), outline=(90, 90, 92), width=6)
    im.save(os.path.join(ITEMS, 'camera978.jpg'), quality=90)
    icon = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    idr = ImageDraw.Draw(icon)
    idr.rectangle([6, 18, 58, 50], fill=(34, 34, 36, 255))
    idr.rectangle([8, 40, 56, 48], fill=(170, 40, 36, 255))
    idr.ellipse([22, 24, 42, 44], fill=(18, 18, 20, 255), outline=(90, 90, 92, 255), width=2)
    icon.save(os.path.join(ITEMS, 'INVcamera978.png'))


def knife():
    im = Image.fromarray(noisy((110, 104, 98), 50), 'RGB').filter(ImageFilter.GaussianBlur(1))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 256, 40], fill=(92, 40, 24))                       # rust along one edge
    im.save(os.path.join(ITEMS, 'knife3041.jpg'), quality=90)
    icon = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    idr = ImageDraw.Draw(icon)
    idr.polygon([(8, 44), (44, 22), (56, 14), (50, 30), (20, 50)], fill=(150, 150, 150, 255), outline=(60, 40, 30, 255))
    idr.rectangle([6, 42, 14, 52], fill=(100, 70, 50, 255))               # the braided hilt
    icon.save(os.path.join(ITEMS, 'INVknife3041.png'))


def sweater():
    im = Image.fromarray(noisy((160, 30, 34), 36), 'RGB').filter(ImageFilter.GaussianBlur(1))
    d = ImageDraw.Draw(im)
    for x in range(0, 256, 12):
        d.line([(x, 0), (x, 256)], fill=(120, 20, 24), width=1)           # knit
    im.save(os.path.join(ITEMS, 'sweater1337.jpg'), quality=90)
    icon = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    idr = ImageDraw.Draw(icon)
    idr.rounded_rectangle([12, 14, 52, 56], radius=6, fill=(160, 30, 34, 255), outline=(110, 20, 24, 255))
    idr.rectangle([22, 14, 42, 22], fill=(0, 0, 0, 0))                    # the neck
    icon.save(os.path.join(ITEMS, 'INVsweater1337.png'))


if __name__ == '__main__':
    cookie()
    camera()
    knife()
    sweater()
    print('4 usable items: textures and icons written')
