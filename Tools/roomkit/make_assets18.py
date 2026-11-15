"""Textures and plates of The Hollowcrest (batch 18), original designs:
     GFX\map\indev_hollowplates18.png (+ hollowplates18.json)   room plates: RECEPTION, 117, BOILER, STAFF KITCHEN ...
     GFX\map\indev_svc_G.png, indev_svc_S.png                      the service lift's floor display (ground, service)
   python make_assets18.py"""
import json
import os
from PIL import Image, ImageDraw, ImageFont
from make_assets5 import save_map

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = r"C:\Windows\Fonts\arialbd.ttf"
PLATES = [('recep', 'RECEPTION'), ('r117', '117'), ('boiler', 'BOILER - HOT'), ('kitchen', 'STAFF KITCHEN'),
          ('ballroom', 'BALLROOM'), ('svc', 'SERVICE LIFT'), ('staff', 'STAFF ONLY'), ('quiet', 'QUIET, PLEASE')]


def plates():
    W = H = 512
    im = Image.new('RGB', (W, H), (34, 34, 36))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (k, text) in enumerate(PLATES):
        x, y = (i % 3) * 170, (i // 3) * 128
        rects[k] = (x / W, y / H, min(x + 168, W) / W, min(y + 124, H) / H)
        d.rectangle([x + 4, y + 4, x + 164, y + 120], fill=(230, 222, 200), outline=(96, 80, 56), width=4)
        size = 40
        while d.textlength(text, font=ImageFont.truetype(FONT, size)) > 146:
            size -= 2
        d.text((x + 84, y + 62), text, font=ImageFont.truetype(FONT, size), fill=(60, 42, 28), anchor='mm')
    save_map(im, 'indev_hollowplates18.png')
    json.dump(rects, open(os.path.join(HERE, 'hollowplates18.json'), 'w'), indent=1)


def display(letter, name):
    im = Image.new('RGB', (256, 256), (10, 12, 10))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 8, 247, 247], outline=(50, 50, 46), width=6)
    d.text((128, 128), letter, font=ImageFont.truetype(FONT, 190), fill=(255, 60, 40), anchor='mm')
    save_map(im, name)


if __name__ == '__main__':
    plates()
    display('G', 'indev_svc_G.png')
    display('S', 'indev_svc_S.png')
    print('batch 18 plates and display digits written')
