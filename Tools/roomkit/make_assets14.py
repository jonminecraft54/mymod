"""Assets of the fourteenth batch (SCP-4035 and SCP-3886):
     GFX\\map\\indev_stained4035.png     a stained-glass shade texture, made here (no photo is copied)
     GFX\\items\\INVbulb14.png           the inventory icon of the lightbulb
     GFX\\items\\photo3886.jpg           the 1900s circus train photograph, used as a readable photo item
   python make_assets14.py"""
import os
import numpy as np
from PIL import Image, ImageDraw
from make_assets5 import save_map

ITEMS = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9\GFX\items"
PHOTO = r"C:\Users\Computer\AppData\Local\Temp\claude\I--MythicalC-v1-2-7-v0-1-scpcb-dx9\bb8674a5-7deb-456c-b97b-7e5d757ed7a7\images\26.png"


def stained():
    """Voronoi panes in greens, olives and ambers, with dark lead lines where two panes meet."""
    N = 256
    rng = np.random.default_rng(4035)
    pts = rng.random((26, 2)) * N
    palette = np.array([(70, 170, 90), (40, 130, 70), (150, 190, 80), (200, 170, 60), (110, 150, 120),
                        (60, 140, 140), (170, 130, 50), (90, 180, 110)], dtype=np.float64)
    ys, xs = np.mgrid[0:N, 0:N]
    d = (xs[..., None] - pts[:, 0]) ** 2 + (ys[..., None] - pts[:, 1]) ** 2
    lab = d.argmin(axis=2)
    col = palette[rng.integers(0, len(palette), len(pts))][lab]
    # a little mottling, like the opalescent glass in the reference shade
    col = col * (0.85 + 0.3 * rng.random((N, N, 1)))
    lead = np.zeros((N, N), bool)
    lead[:, :-1] |= lab[:, :-1] != lab[:, 1:]
    lead[:-1, :] |= lab[:-1, :] != lab[1:, :]
    col[lead] = (28, 26, 22)
    save_map(Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), 'RGB'), 'indev_stained4035.png')


def bulb_icon():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([14, 6, 50, 42], fill=(236, 240, 220, 255), outline=(150, 150, 140, 255), width=2)
    d.ellipse([22, 14, 34, 26], fill=(255, 255, 255, 180))
    d.rectangle([22, 40, 42, 52], fill=(120, 120, 118, 255))
    d.rectangle([24, 52, 40, 58], fill=(70, 70, 70, 255))
    im.save(os.path.join(ITEMS, 'INVbulb14.png'))


def photo():
    Image.open(PHOTO).convert('RGB').save(os.path.join(ITEMS, 'photo3886.jpg'), quality=90)


if __name__ == '__main__':
    stained()
    bulb_icon()
    photo()
    print('batch 14 assets written')
