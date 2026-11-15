"""Textures of the seventeenth batch (The Forgotten Hotel, anomalous room H-17). Original designs, not copied from
any photograph: a teal lozenge carpet, a green-and-cream striped wallpaper, and a sheet of room-number plates.
   GFX\\map\\indev_hotelcarpet17.png, indev_hotelpaper17.png (512 x 512) and indev_hotelplates17.png (+ json)
   python make_assets17.py"""
import json
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from make_assets5 import save_map

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\arialbd.ttf"
rng = np.random.default_rng(17)


def carpet():
    """Lozenges in gold on deep teal, on a half-drop grid, with a slight wear mottle."""
    N = 512
    im = Image.new('RGB', (N, N), (18, 62, 66))
    d = ImageDraw.Draw(im)
    for row in range(8):
        for col in range(8):
            cx = col * 64 + (32 if row % 2 else 0)
            cy = row * 64 + 32
            d.polygon([(cx, cy - 22), (cx + 16, cy), (cx, cy + 22), (cx - 16, cy)], fill=(176, 132, 52))
            d.polygon([(cx, cy - 12), (cx + 8, cy), (cx, cy + 12), (cx - 8, cy)], fill=(60, 30, 30))
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(230, 200, 120))
    arr = np.asarray(im, dtype=np.float64) * (0.9 + 0.2 * rng.random((N, N, 1)))
    save_map(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB'), 'indev_hotelcarpet17.png')


def paper():
    """Vertical stripes: muted green and cream, with small dark dots every stripe."""
    N = 512
    im = Image.new('RGB', (N, N), (200, 190, 160))
    d = ImageDraw.Draw(im)
    for x in range(0, N, 64):
        d.rectangle([x, 0, x + 31, N], fill=(74, 98, 84))
        for y in range(16, N, 64):
            d.ellipse([x + 12, y, x + 20, y + 8], fill=(150, 120, 60))
    arr = np.asarray(im, dtype=np.float64) * (0.94 + 0.12 * rng.random((N, N, 1)))
    save_map(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB'), 'indev_hotelpaper17.png')


PLATES = [('h16', 'H-16'), ('h17', 'H-17'), ('h14', 'H-14'), ('lift', 'LIFT'), ('laundry', 'LAUNDRY'), ('stairs', 'STAIRS')]


def plates():
    W = H = 512
    im = Image.new('RGB', (W, H), (34, 34, 36))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (k, text) in enumerate(PLATES):
        x, y = (i % 3) * 170, (i // 3) * 256
        rects[k] = (x / W, y / H, min(x + 168, W) / W, min(y + 240, H) / H)
        d.rectangle([x + 4, y + 4, x + 164, y + 236], fill=(226, 218, 196), outline=(90, 74, 50), width=4)
        size = 56
        while d.textlength(text, font=ImageFont.truetype(FONT, size)) > 146:
            size -= 2
        d.text((x + 84, y + 120), text, font=ImageFont.truetype(FONT, size), fill=(60, 40, 26), anchor='mm')
    save_map(im, 'indev_hotelplates17.png')
    json.dump(rects, open(os.path.join(HERE, 'hotelplates17.json'), 'w'), indent=1)


def door_plate(text, name):
    """a landscape number plate over a door: the plate is a runtime quad (IndevU17.bb), so it is one texture"""
    im = Image.new('RGB', (256, 128), (226, 218, 196))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, 249, 121], outline=(90, 74, 50), width=6)
    size = 84
    while d.textlength(text, font=ImageFont.truetype(FONT, size)) > 220:
        size -= 2
    d.text((128, 64), text, font=ImageFont.truetype(FONT, size), fill=(60, 40, 26), anchor='mm')
    save_map(im, name)


if __name__ == '__main__':
    carpet()
    paper()
    plates()
    door_plate('H-17', 'indev_h17_door.png')
    door_plate('H-71', 'indev_h71_door.png')
    print('batch 17 textures and plates written')
