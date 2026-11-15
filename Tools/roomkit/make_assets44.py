r"""Textures of the forty-fourth batch (the early SCP-1074 room and five distinctive sites). Concrete, metal, pipes,
tiles, rock (indev_b33stone), wood and glass are reused; new ones only where nothing else fits.
  indev_b44brick.png    512  old blue-grey painted brick, damp and stained (the prototype room, ref. 223)
  indev_b44cobble.png   512  worn stone setts, dark grout (ref. 223)
  indev_b44painting.png      SCP-1074's painting (a copy of GFX\map\Props\scp1074.png, so the rmesh can use it)
  indev_b44frost.png    256  frosted cryo-pod glass with a blue glow (emissive)
  indev_b44pad.png      512  padded wall panels of the gravity chamber
  indev_b44crystal.png  256  the geological anomaly's teal crystal (emissive)
  indev_b44marble.png   512  black marble with pale veins (the O5 vault)
  indev_b44hazard.png   256  yellow-black hazard floor stripes
  indev_b44signs.png    512  eight room signs: CRYO-1, THEATRE 2, GRAVITY LAB, GEO SITE 7, O5 RECORDS, ROOM 104,
                             AUTHORISED PERSONNEL ONLY, LN2 - COLD BURN HAZARD
   python make_assets44.py"""
import os
import random
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def noise(w, h, base, amp, seed, blur=1.0):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def brick():
    rnd = random.Random(441)
    im = Image.new('RGB', (512, 512), (40, 44, 52))
    d = ImageDraw.Draw(im, 'RGBA')
    for row in range(16):
        off = 0 if row % 2 == 0 else 32
        for col in range(-1, 9):
            x0, y0 = col * 64 + off, row * 32
            v = rnd.randint(-10, 10)
            d.rectangle((x0 + 2, y0 + 2, x0 + 62, y0 + 30), fill=(92 + v, 100 + v, 116 + v))
    for _ in range(14):
        x, y = rnd.uniform(0, 512), rnd.uniform(200, 512)
        d.ellipse((x - 60, y - 90, x + 60, y + 90), fill=(30, 34, 30, 40))
    save(Image.blend(im, noise(512, 512, (100, 100, 100), 20, 442), 0.18), 'indev_b44brick.png')


def cobble():
    rnd = random.Random(443)
    im = Image.new('RGB', (512, 512), (30, 32, 30))
    d = ImageDraw.Draw(im)
    for row in range(8):
        for col in range(8):
            x0, y0 = col * 64 + (32 if row % 2 else 0), row * 64
            v = rnd.randint(-14, 14)
            d.rectangle((x0 + 3, y0 + 3, x0 + 61, y0 + 61), fill=(70 + v, 78 + v, 74 + v))
    save(Image.blend(im, noise(512, 512, (90, 90, 90), 22, 444), 0.2), 'indev_b44cobble.png')


def painting():
    src = os.path.join(MAPDIR, 'Props', 'scp1074.png')
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(MAPDIR, 'indev_b44painting.png'))


def frost():
    im = noise(256, 256, (170, 210, 240), 16, 445, 2.0)
    d = ImageDraw.Draw(im, 'RGBA')
    rnd = random.Random(446)
    for _ in range(60):
        x, y = rnd.uniform(0, 256), rnd.uniform(0, 256)
        d.line((x, y, x + rnd.uniform(-20, 20), y + rnd.uniform(-20, 20)), fill=(255, 255, 255, 120), width=1)
    save(im, 'indev_b44frost.png')


def pad():
    im = noise(512, 512, (196, 190, 176), 6, 447, 1.0)
    d = ImageDraw.Draw(im)
    for y in range(0, 512, 128):
        for x in range(0, 512, 128):
            d.rectangle((x + 4, y + 4, x + 124, y + 124), outline=(150, 144, 130), width=4)
            d.ellipse((x + 60, y + 60, x + 68, y + 68), fill=(120, 116, 104))
    save(im, 'indev_b44pad.png')


def crystal():
    y = np.linspace(0, 6.28, 256)[:, None]
    x = np.linspace(0, 6.28, 256)[None, :]
    v = 0.5 + 0.5 * np.sin(x * 4 + np.cos(y * 3) * 2)
    rgb = np.stack([40 + 60 * v, 200 + 50 * v, 190 + 40 * v], -1)
    save(Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)), 'indev_b44crystal.png')


def marble():
    rnd = random.Random(448)
    im = noise(512, 512, (24, 24, 28), 6, 449, 1.5)
    d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(18):
        x, y = rnd.uniform(0, 512), rnd.uniform(0, 512)
        for _ in range(12):
            nx, ny = x + rnd.uniform(-40, 40), y + rnd.uniform(-20, 40)
            d.line((x, y, nx, ny), fill=(170, 170, 160, 90), width=2)
            x, y = nx, ny
    save(im, 'indev_b44marble.png')


def hazard():
    im = Image.new('RGB', (256, 256), (30, 30, 30))
    d = ImageDraw.Draw(im)
    for k in range(-256, 512, 64):
        d.polygon(((k, 0), (k + 32, 0), (k + 32 + 256, 256), (k + 256, 256)), fill=(220, 180, 30))
    save(im, 'indev_b44hazard.png')


SIGNS = ['CRYO-1', 'THEATRE 2', 'GRAVITY LAB', 'GEO SITE 7', 'O5 RECORDS', 'ROOM 104', 'AUTHORISED ONLY', 'LN2 - COLD BURN']


def signs():
    im = Image.new('RGB', (512, 512), (20, 20, 22))
    d = ImageDraw.Draw(im)
    for i, t in enumerate(SIGNS):
        x0, y0 = (i % 2) * 256, (i // 2) * 128
        bg = (200, 160, 30) if i >= 6 else (24, 24, 26)
        fg = (20, 20, 20) if i >= 6 else (236, 236, 230)
        d.rectangle((x0 + 4, y0 + 4, x0 + 251, y0 + 123), fill=bg, outline=(110, 110, 110), width=4)
        d.ellipse((x0 + 14, y0 + 34, x0 + 74, y0 + 94), outline=fg, width=5)
        w = d.textlength(t, font=F(26))
        d.text((x0 + 84 + (160 - w) / 2, y0 + 48), t, font=F(26), fill=fg)
    save(im, 'indev_b44signs.png')


if __name__ == '__main__':
    for fn in (brick, cobble, painting, frost, pad, crystal, marble, hazard, signs):
        fn()
        print(fn.__name__)
