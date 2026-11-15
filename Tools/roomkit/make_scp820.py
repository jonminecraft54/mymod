r"""SCP-820-JP, the Aztec-style stone knife (original model after scp-wiki.wikidot.com/scp-820-jp, CC BY-SA 3.0):
a leaf-shaped knapped flint blade, a carved turquoise-mosaic handle with a gold band, and a snake that coils up
from the handle round the blade to the tip. Plus the SCP-867 herbicide injector's icon.
     GFX\items\scp820jp.b3d + scp820jp.png + INVscp820jp.png
     GFX\items\INVherbicide867.png     (the injector reuses the game's syringe model)
   python make_scp820.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter
import make_scp983 as M

ITEMS = M.ITEMS
RND = random.Random(820)
M.ATLAS.update({'flint': (0, 0, .5, .5), 'mosaic': (.5, 0, 1, .5), 'snake': (0, .5, .5, 1), 'gold': (.5, .5, .75, .75),
                'eye820': (.75, .5, 1, .75)})


def texture():
    S = 512
    tex = Image.new('RGB', (S, S), (40, 40, 40))
    # knapped flint: dark grey-brown with pale conchoidal scars
    f = Image.new('RGB', (256, 256), (58, 52, 50))
    d = ImageDraw.Draw(f)
    for _ in range(90):
        x, y, r = RND.randrange(256), RND.randrange(256), RND.randint(10, 34)
        c = RND.randint(46, 96)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(c, c - 6, c - 8))
        d.arc([x - r, y - r * 0.6, x + r, y + r * 0.6], 180, 360, fill=(c + 40, c + 34, c + 30), width=2)
    tex.paste(f.filter(ImageFilter.GaussianBlur(0.8)), (0, 0))
    # the handle: turquoise and jet mosaic tesserae
    m = Image.new('RGB', (256, 256), (20, 20, 20))
    d = ImageDraw.Draw(m)
    for y in range(0, 256, 16):
        for x in range(0, 256, 16):
            k = RND.random()
            c = (30, 160, 150) if k < 0.6 else (20, 110, 130) if k < 0.85 else (200, 70, 50)
            j = RND.randint(-14, 14)
            d.rectangle([x + 1, y + 1, x + 14, y + 14], fill=tuple(max(0, min(255, v + j)) for v in c))
    tex.paste(m, (256, 0))
    # the snake: green-turquoise scales with a dark zigzag down its back
    s = Image.new('RGB', (256, 256), (40, 130, 90))
    d = ImageDraw.Draw(s)
    for y in range(0, 256, 10):
        for x in range(0, 256, 12):
            o = 6 if (y // 10) % 2 else 0
            d.ellipse([x + o - 6, y - 4, x + o + 6, y + 6], outline=(20, 80, 60), fill=(50 + RND.randint(0, 30), 150, 100))
    for y in range(0, 256, 16):
        d.polygon([(0, y), (12, y + 8), (0, y + 16)], fill=(20, 40, 30))
    tex.paste(s, (0, 256))
    g = Image.new('RGB', (128, 128), (190, 150, 50))
    d = ImageDraw.Draw(g)
    for x in range(0, 128, 8):
        d.line([(x, 0), (x, 128)], fill=(150, 110, 30), width=2)
    tex.paste(g, (256, 256))
    tex.paste(Image.new('RGB', (128, 128), (200, 20, 20)), (384, 256))
    tex.save(os.path.join(ITEMS, 'scp820jp.png'))


def knife():
    """lying along +y (tip up); units ~cm, 29 long"""
    m = M.Mesh()
    m.tube((0, 0, 0), (0, 8.5, 0), 1.25, 1.45, 'mosaic', 14)                      # the grip
    m.ellipsoid((0, -0.4, 0), (1.7, 1.0, 1.7), 'gold', 8, 12)                     # the pommel
    m.tube((0, 8.3, 0), (0, 9.3, 0), 1.9, 1.9, 'gold', 14)                        # the gold band at the guard
    m.ellipsoid((0, 18.5, 0), (3.1, 10.2, 0.75), 'flint', 10, 16)                # the leaf-shaped blade
    # the snake: from the pommel round the grip, then coiling up the blade to its head near the tip
    pts = []
    for i in range(70):
        t = i / 69.0
        y = -0.2 + t * 25.5
        ang = t * 2 * math.pi * 3.2
        if y < 9.0:
            wx = wz = 1.6
        else:
            k = max(0.0, 1 - ((y - 18.5) / 10.2) ** 2)
            wx, wz = 3.1 * math.sqrt(k) + 0.45, 0.75 * math.sqrt(k) + 0.5
        pts.append((wx * math.cos(ang), y, wz * math.sin(ang)))
    for i in range(len(pts) - 1):
        r = 0.55 if i < 60 else 0.55 - (i - 60) * 0.02
        m.tube(pts[i], pts[i + 1], r, r, 'snake', 8, caps=False)
    hx, hy, hz = pts[-1]
    m.ellipsoid((hx, hy + 0.5, hz), (0.8, 1.2, 0.7), 'snake', 8, 10)                # its head
    for s in (-1, 1):
        m.ellipsoid((hx + s * 0.55, hy + 0.9, hz + 0.3), (0.2, 0.2, 0.2), 'eye820', 4, 6)
    return m


def icons():
    ic = Image.new('RGB', (64, 64), (0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.polygon([(30, 4), (40, 14), (38, 34), (32, 38), (26, 34), (24, 14)], fill=(70, 64, 60), outline=(120, 112, 104))
    d.rectangle([28, 38, 36, 56], fill=(30, 160, 150))
    d.rectangle([26, 36, 38, 39], fill=(200, 160, 60))
    d.ellipse([27, 55, 37, 61], fill=(200, 160, 60))
    for y in range(40, 8, -6):
        d.arc([22, y - 4, 42, y + 4], 0, 180, fill=(50, 170, 100), width=2)
    d.ellipse([29, 6, 35, 11], fill=(50, 170, 100))
    ic.save(os.path.join(ITEMS, 'INVscp820jp.png'))
    src = os.path.join(ITEMS, 'Syringe', 'inv.png')
    if os.path.exists(src):
        h = Image.open(src).convert('RGB').resize((64, 64))
    else:
        h = Image.new('RGB', (64, 64), (0, 0, 0))
    d = ImageDraw.Draw(h)
    d.rectangle([2, 2, 61, 61], outline=(40, 200, 80), width=3)
    d.text((6, 46), 'HERB', fill=(60, 230, 100))
    h.save(os.path.join(ITEMS, 'INVherbicide867.png'))


if __name__ == '__main__':
    texture()
    k = knife()
    M.write_b3d(os.path.join(ITEMS, 'scp820jp.b3d'), k, 'scp820jp.png', shine=0.35)
    icons()
    print('scp820jp: %d vertices, %d triangles' % (len(k.V), len(k.T)))
