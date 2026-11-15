"""Textures of the twentieth batch (original, drawn here unless noted):
     GFX\\map\\indev_3008blue.png, indev_3008yellow.png, indev_3008fabric.png   the store's shelf trim, banner, sofa
     GFX\\map\\indev_261.png      the vending machine front     GFX\\map\\indev_458.png   the pizza box lid
     GFX\\map\\indev_poster20.png "HAVE YOU SEEN JOSIE?" over the user's image 20
     GFX\\npcs\\indev_3008staff.jpg   SCP-3008's staff: classd1.jpg recoloured to a yellow uniform, the face blanked
     GFX\\items\\INVcandy330.png     the sweet from SCP-330
   python make_assets20.py"""
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_assets5 import save_map
from make_assets19 import IMG

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
FONT = r"C:\Windows\Fonts\arialbd.ttf"


def flat(name, rgb, noise=10, size=256):
    random.seed(name)
    im = Image.new('RGB', (size, size), rgb)
    px = im.load()
    for y in range(size):
        for x in range(size):
            n = random.randint(-noise, noise)
            px[x, y] = tuple(max(0, min(255, c + n)) for c in rgb)
    save_map(im.filter(ImageFilter.GaussianBlur(0.7)), name)


def banner():
    im = Image.new('RGB', (256, 256), (250, 206, 30))
    d = ImageDraw.Draw(im)
    d.text((128, 128), 'OPEN', font=ImageFont.truetype(FONT, 80), fill=(20, 60, 150), anchor='mm')
    save_map(im, 'indev_3008yellow.png')


def vending():
    im = Image.new('RGB', (256, 256), (150, 22, 26))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 170, 230], fill=(30, 34, 40))
    for r in range(5):
        for c in range(3):
            d.rectangle([28 + c * 48, 28 + r * 40, 66 + c * 48, 56 + r * 40], fill=random.choice([(220, 180, 40), (40, 120, 200), (200, 60, 60)]))
    d.rectangle([186, 40, 236, 120], fill=(200, 200, 200))
    d.text((211, 160), '261', font=ImageFont.truetype(FONT, 26), fill=(255, 255, 255), anchor='mm')
    save_map(im, 'indev_261.png')


def pizza():
    im = Image.new('RGB', (128, 128), (206, 170, 120))
    d = ImageDraw.Draw(im)
    d.ellipse([24, 24, 104, 104], outline=(170, 30, 30), width=6)
    d.text((64, 64), 'HOT', font=ImageFont.truetype(FONT, 22), fill=(170, 30, 30), anchor='mm')
    save_map(im, 'indev_458.png')


def poster():
    im = Image.open(os.path.join(IMG, '20.png')).convert('RGB')
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((360, 360), Image.NEAREST)
    out = Image.new('RGB', (512, 512), (240, 238, 228))
    out.paste(im, (76, 96))
    d = ImageDraw.Draw(out)
    d.text((256, 50), 'HAVE YOU SEEN JOSIE?', font=ImageFont.truetype(FONT, 34), fill=(30, 30, 30), anchor='mm')
    d.text((256, 482), 'Half of her is always here.', font=ImageFont.truetype(FONT, 22), fill=(60, 60, 60), anchor='mm')
    save_map(out, 'indev_poster20.png')


def staff():
    im = Image.open(os.path.join(ROOT, 'GFX', 'npcs', 'classd1.jpg')).convert('RGB')
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b = px[x, y]
            if r > 120 and r > g * 1.25 and g > b:                 # the orange jumpsuit -> a yellow shirt
                v = (r + g) / 2
                px[x, y] = (int(v * 1.0), int(v * 0.86), 30)
            elif r > 90 and r > b * 1.2 and abs(r - g) < 70:      # skin -> the same flat pale grey, no features
                px[x, y] = (196, 190, 184)
    im.save(os.path.join(ROOT, 'GFX', 'npcs', 'indev_3008staff.jpg'), quality=92)


def candy():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(4, 22), (16, 32), (4, 42)], fill=(230, 60, 140))
    d.polygon([(60, 22), (48, 32), (60, 42)], fill=(230, 60, 140))
    d.ellipse([14, 18, 50, 46], fill=(240, 90, 160), outline=(255, 255, 255), width=2)
    im.save(os.path.join(ROOT, 'GFX', 'items', 'INVcandy330.png'))


if __name__ == '__main__':
    flat('indev_3008blue.png', (28, 70, 150))
    flat('indev_3008fabric.png', (90, 96, 110), 14, 128)
    banner()
    vending()
    pizza()
    poster()
    staff()
    candy()
    print('batch 20 textures written')
