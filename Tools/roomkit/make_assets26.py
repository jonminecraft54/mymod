r"""Textures of the twenty-sixth batch, the outdoor expansion (original, drawn here or recoloured from SCP:CB's own):
     GFX\map\indev_o_moss.png       damp concrete with moss (from concretewall.jpg)
     GFX\map\indev_o_damp.png       a damp, water-stained painted wall (from whitewall.jpg)
     GFX\map\indev_o_rust.png       weathered metal (from metal.jpg)
     GFX\map\indev_o_mud.png        muddy ground with needles      indev_o_grass.png  wet grass and moss
     GFX\map\indev_o_asphalt.png    wet asphalt                    indev_o_road.png   wet asphalt with a yellow centre line
     GFX\map\indev_o_bark.png       bark                           indev_o_needles.png evergreen needles
     GFX\map\indev_o_rock.png       grey rock
     GFX\map\indev_o_forest.png     the tree line: layered evergreen silhouettes fading into fog (the edge of the map)
     GFX\map\indev_o_window.png     a rain-streaked window onto the forest
     GFX\map\indev_o_stripes.png    yellow-black floor marking  indev_o_sign.png  RESTRICTED AREA sign
     GFX\map\indev_o_screen.png     a terminal screen            indev_o_broken.png a cracked monitor
     GFX\map\indev_o_panel.png      an electrical panel          indev_o_rain.png   rain streaks (alpha) for the overlay
   No real place names appear anywhere in this batch.
   python make_assets26.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from make_assets5 import save_map, MAPDIR

FONT = r"C:\Windows\Fonts\arialbd.ttf"
R = random.Random(26)


def noise(size, base, amp, blur=1.0, seed=0):
    rnd = random.Random(seed)
    im = Image.new('RGB', size, base)
    px = im.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = rnd.randint(-amp, amp)
            px[x, y] = tuple(max(0, min(255, c + n)) for c in base)
    return im.filter(ImageFilter.GaussianBlur(blur))


def blotches(im, col, n, rmin, rmax, alpha, seed):
    rnd = random.Random(seed)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y, r = rnd.randint(0, im.size[0]), rnd.randint(0, im.size[1]), rnd.randint(rmin, rmax)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (alpha,))
    ov = ov.filter(ImageFilter.GaussianBlur(rmin / 2 + 2))
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')


def recolour(src, name, tint, moss=False, stains=False):
    im = Image.open(os.path.join(MAPDIR, src)).convert('RGB').resize((512, 512))
    im = ImageEnhance.Color(im).enhance(0.5)
    im = Image.blend(im, Image.new('RGB', im.size, tint), 0.25)
    if moss:
        im = blotches(im, (54, 86, 38), 70, 10, 40, 160, 1)
        d = ImageDraw.Draw(im)
        rnd = random.Random(2)
        for _ in range(900):                                   # a fuzz of moss at the bottom edge
            x = rnd.randint(0, 511)
            y = 511 - int(abs(rnd.gauss(0, 50)))
            d.point((x, y), fill=(60 + rnd.randint(0, 30), 100 + rnd.randint(0, 40), 40))
    if stains:
        d = ImageDraw.Draw(im)
        rnd = random.Random(3)
        for _ in range(26):                                    # water runs down from the top
            x = rnd.randint(0, 511)
            l = rnd.randint(80, 400)
            for y in range(l):
                d.point((x + int(3 * math.sin(y / 30.0)), y), fill=(120, 116, 100))
        im = im.filter(ImageFilter.GaussianBlur(0.8))
    save_map(im, name)


def ground(name, base, seed, needles=False):
    im = noise((256, 256), base, 22, 1.2, seed)
    im = blotches(im, tuple(max(0, c - 30) for c in base), 40, 6, 20, 120, seed + 1)
    if needles:
        d = ImageDraw.Draw(im)
        rnd = random.Random(seed + 2)
        for _ in range(500):
            x, y, a = rnd.randint(0, 255), rnd.randint(0, 255), rnd.uniform(0, math.pi)
            d.line([(x, y), (x + 6 * math.cos(a), y + 6 * math.sin(a))], fill=(96, 70, 40), width=1)
    save_map(im, name)


def road(name, line):
    im = noise((256, 256), (52, 54, 56), 16, 0.8, 9)
    im = blotches(im, (30, 32, 36), 20, 10, 30, 90, 10)               # puddles
    if line:
        d = ImageDraw.Draw(im)
        d.rectangle([122, 0, 133, 150], fill=(200, 170, 40))
    save_map(im, name)


def bark():
    im = noise((128, 256), (72, 52, 38), 18, 0.6, 11)
    d = ImageDraw.Draw(im)
    for x in range(0, 128, 9):
        d.line([(x + R.randint(-2, 2), 0), (x + R.randint(-2, 2), 255)], fill=(40, 28, 20), width=2)
    save_map(im, 'indev_o_bark.png')


def needles():
    im = noise((128, 128), (34, 60, 36), 22, 0.4, 12)
    d = ImageDraw.Draw(im)
    for _ in range(700):
        x, y = R.randint(0, 127), R.randint(0, 127)
        d.line([(x, y), (x + R.randint(-4, 4), y + 5)], fill=(R.randint(20, 50), R.randint(70, 100), R.randint(30, 50)))
    save_map(im, 'indev_o_needles.png')


def forest():
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (150, 156, 160))
    d = ImageDraw.Draw(im)
    for y in range(H):                                                 # overcast sky into fog
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(160 - 40 * t), int(166 - 40 * t), int(170 - 36 * t)))
    rnd = random.Random(13)
    for layer, (shade, base, hmin, hmax) in enumerate(((120, 330, 120, 200), (88, 380, 160, 260), (56, 430, 200, 320), (30, 470, 240, 380))):
        x = -30
        while x < W + 30:
            h = rnd.randint(hmin, hmax)
            w = h * rnd.uniform(0.28, 0.4)
            c = (shade - 10, shade + 4, shade - 6)
            d.polygon([(x, base), (x + w, base), (x + w / 2, base - h)], fill=c)
            x += rnd.randint(14, 34)
        d.rectangle([0, base, W, H], fill=(shade - 14, shade - 4, shade - 12))
    im = im.filter(ImageFilter.GaussianBlur(1.4))
    save_map(im, 'indev_o_forest.png')


def window():
    im = Image.open(os.path.join(MAPDIR, 'indev_o_forest.png')).resize((512, 256))
    d = ImageDraw.Draw(im)
    rnd = random.Random(14)
    for _ in range(120):
        x, y, l = rnd.randint(0, 511), rnd.randint(0, 255), rnd.randint(10, 60)
        d.line([(x, y), (x + rnd.randint(-2, 2), y + l)], fill=(200, 206, 210), width=1)
    d.rectangle([0, 0, 511, 255], outline=(60, 62, 64), width=14)
    d.line([(256, 0), (256, 255)], fill=(60, 62, 64), width=8)
    save_map(im.filter(ImageFilter.GaussianBlur(0.7)), 'indev_o_window.png')


def stripes():
    im = Image.new('RGB', (128, 128), (220, 180, 30))
    d = ImageDraw.Draw(im)
    for k in range(-128, 256, 40):
        d.polygon([(k, 0), (k + 20, 0), (k + 148, 128), (k + 128, 128)], fill=(24, 24, 24))
    save_map(im, 'indev_o_stripes.png')


def sign():
    im = Image.new('RGB', (512, 256), (235, 235, 230))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 511, 80], fill=(180, 30, 30))
    d.text((256, 40), 'RESTRICTED AREA', font=ImageFont.truetype(FONT, 44), fill=(255, 255, 255), anchor='mm')
    d.text((256, 130), 'AUTHORIZED PERSONNEL ONLY', font=ImageFont.truetype(FONT, 30), fill=(20, 20, 20), anchor='mm')
    d.text((256, 190), 'Use of deadly force authorized', font=ImageFont.truetype(FONT, 24), fill=(60, 60, 60), anchor='mm')
    d.rectangle([4, 4, 507, 251], outline=(30, 30, 30), width=6)
    save_map(im, 'indev_o_sign.png')


def screen(name, broken):
    im = Image.new('RGB', (256, 192), (14, 30, 22))
    d = ImageDraw.Draw(im)
    rnd = random.Random(15 + broken)
    for k in range(9):
        d.text((14, 14 + k * 18), ''.join(rnd.choice('0123456789ABCDEF:/- ') for _ in range(22)),
               font=ImageFont.truetype(FONT, 12), fill=(90, 220, 120))
    if broken:
        im = ImageEnhance.Brightness(im).enhance(0.4)
        d = ImageDraw.Draw(im)
        cx, cy = 150, 80
        for _ in range(14):
            a = rnd.uniform(0, 2 * math.pi)
            l = rnd.randint(40, 160)
            d.line([(cx, cy), (cx + l * math.cos(a), cy + l * math.sin(a))], fill=(220, 220, 220), width=2)
    d.rectangle([0, 0, 255, 191], outline=(30, 30, 30), width=12)
    save_map(im, name)


def panel():
    im = Image.new('RGB', (256, 256), (120, 126, 120))
    d = ImageDraw.Draw(im)
    for r in range(4):
        for c in range(3):
            x, y = 24 + c * 74, 30 + r * 52
            d.rectangle([x, y, x + 50, y + 34], fill=(40, 40, 40))
            d.rectangle([x + 18, y + 6, x + 32, y + 28], fill=(200, 200, 190))
    d.rectangle([0, 0, 255, 255], outline=(60, 60, 60), width=8)
    d.text((128, 240), 'DANGER 480V', font=ImageFont.truetype(FONT, 16), fill=(200, 30, 30), anchor='mm')
    save_map(im, 'indev_o_panel.png')


def rain():
    im = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rnd = random.Random(16)
    for _ in range(170):
        x, y, l = rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(12, 34)
        a = rnd.randint(50, 120)
        for k in range(2):                                             # drawn twice, wrapped, so it tiles
            d.line([(x, y - 256 * k), (x - 3, y + l - 256 * k)], fill=(200, 210, 220, a), width=1)
    im.save(os.path.join(MAPDIR, 'indev_o_rain.png'))


if __name__ == '__main__':
    recolour('concretewall.jpg', 'indev_o_moss.png', (70, 90, 70), moss=True)
    recolour('whitewall.jpg', 'indev_o_damp.png', (150, 150, 130), stains=True)
    recolour('metal.jpg', 'indev_o_rust.png', (120, 70, 40))
    ground('indev_o_mud.png', (78, 64, 46), 20, needles=True)
    ground('indev_o_grass.png', (58, 80, 44), 22)
    road('indev_o_asphalt.png', False)
    road('indev_o_road.png', True)
    bark()
    needles()
    im = noise((128, 128), (112, 114, 112), 26, 1.0, 17)
    save_map(blotches(im, (80, 100, 70), 10, 6, 16, 120, 18), 'indev_o_rock.png')
    forest()
    window()
    stripes()
    sign()
    screen('indev_o_screen.png', 0)
    screen('indev_o_broken.png', 1)
    panel()
    rain()
    print('batch 26 textures written')
