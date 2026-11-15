r"""Textures of the thirty-eighth batch - only what the original SCP:CB textures cannot do (walls, floors, doors,
furniture all reuse the game's own: white.jpg, wood.jpg, dirtymetal.jpg, the ref96 white walls and tiles).
  indev_b38mirror.png   512  SCP-1148: a dark pane that shows only a dim reflection of a lit room
  indev_b38plaque.png   512  eight display placards (SCP-1039 and seven PENDING CLASSIFICATION objects)
  indev_b38garland.png  256  paper chains (alpha) for the party room
  indev_b38banner.png   512  HAPPY HOLIDAYS - D-BLOCK SOCIAL
  indev_b38frost.png    256  buttercream and sponge (SCP-1117's cake)
  indev_b38food.png     256  a crowded table: roasts, bread, fruit, dishes (SCP-1117-2)
  indev_b38doll.png     256  SCP-1039: woven fabric with a crude painted ribcage
  GFX\items\food1117.png   the ration model's texture override for a plate of SCP-1117-2
   python make_assets38.py"""
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F

ITEMS = os.path.join(os.path.dirname(MAPDIR), 'items')


def save(im, name, d=MAPDIR):
    im.save(os.path.join(d, name))


def noise(w, h, base, amp, seed, blur=1.0):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def mirror():
    y = np.linspace(0, 1, 512)[:, None]
    x = np.linspace(0, 1, 512)[None, :]
    v = 18 + 26 * np.exp(-((x - 0.5) ** 2) * 6) * (1 - y * 0.7) + np.random.default_rng(1148).normal(0, 2, (512, 512))
    rgb = np.stack([v * 0.95, v, v * 1.08], -1)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((150, 300, 362, 512), fill=(40, 40, 44, 60))                 # a dim reflected doorway
    for k in range(6):                                                    # faint streaks on the glass
        x0 = 60 + k * 80
        d.line((x0, 0, x0 + 120, 512), fill=(90, 90, 100, 18), width=10)
    save(im.filter(ImageFilter.GaussianBlur(1.5)), 'indev_b38mirror.png')


PLAQUES = [('SCP-1039', 'EUCLID', 'DO NOT CARRY ITEMS', 'WITHIN 40 METRES'),
           ('PENDING 38-01', 'SAFE (PROV.)', 'MUSIC BOX', 'PLAYS WHEN UNWATCHED'),
           ('PENDING 38-02', 'SAFE (PROV.)', 'SNOW GLOBE', 'ALWAYS SNOWING'),
           ('PENDING 38-03', 'SAFE (PROV.)', 'TYPEWRITER', 'TYPES ITS OWN LOG'),
           ('PENDING 38-04', 'SAFE (PROV.)', 'RUBBER DUCK', 'NEVER QUITE DRY'),
           ('PENDING 38-05', 'SAFE (PROV.)', 'CERAMIC MASK', 'WARM TO THE TOUCH'),
           ('PENDING 38-06', 'SAFE (PROV.)', 'TEAPOT', 'POURS COLD TEA'),
           ('PENDING 38-07', 'SAFE (PROV.)', 'POCKET WATCH', 'RUNS BACKWARDS')]


def plaques():
    im = Image.new('RGB', (512, 512), (20, 20, 22))
    d = ImageDraw.Draw(im)
    for i, (a, b, c, e) in enumerate(PLAQUES):
        x0, y0 = (i % 2) * 256, (i // 2) * 128
        d.rectangle((x0 + 4, y0 + 4, x0 + 251, y0 + 123), fill=(196, 184, 150), outline=(90, 80, 60), width=4)
        d.text((x0 + 16, y0 + 12), a, font=F(28), fill=(30, 26, 20))
        d.text((x0 + 16, y0 + 48), b, font=F(18), fill=(120, 30, 24))
        d.text((x0 + 16, y0 + 74), c, font=F(16), fill=(40, 36, 30))
        d.text((x0 + 16, y0 + 96), e, font=F(14), fill=(60, 56, 50))
    save(im, 'indev_b38plaque.png')


def garland():
    im = Image.new('RGBA', (256, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cols = ((200, 40, 40), (40, 150, 60), (230, 200, 60), (60, 90, 200))
    for k in range(11):
        x = k * 24
        y = 18 + 10 * np.sin(k / 10 * np.pi)
        d.ellipse((x, y, x + 26, y + 20), outline=cols[k % 4] + (255,), width=5)
    save(im, 'indev_b38garland.png')


def banner():
    im = Image.new('RGB', (512, 128), (180, 30, 30))
    d = ImageDraw.Draw(im)
    for k in range(0, 512, 32):
        d.polygon(((k, 0), (k + 16, 18), (k + 32, 0)), fill=(230, 210, 80))
    t = 'HAPPY HOLIDAYS'
    w = d.textlength(t, font=F(52))
    d.text((256 - w / 2, 26), t, font=F(52), fill=(250, 246, 236))
    t = 'D-BLOCK SOCIAL - ATTENDANCE MANDATORY'
    w = d.textlength(t, font=F(16))
    d.text((256 - w / 2, 96), t, font=F(16), fill=(250, 230, 200))
    save(im, 'indev_b38banner.png')


def frost():
    rnd = random.Random(1117)
    im = noise(256, 256, (246, 236, 224), 5, 11171, 1.2)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 150, 256, 256), fill=(206, 168, 112))                  # sponge on the lower half
    d.rectangle((0, 196, 256, 206), fill=(232, 120, 150))                  # a jam layer
    for _ in range(60):
        x, y = rnd.uniform(0, 256), rnd.uniform(0, 140)
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=rnd.choice(((240, 90, 120), (90, 170, 230), (250, 220, 80))))
    for x in range(0, 256, 32):
        d.ellipse((x, 132, x + 32, 160), fill=(250, 244, 236))
    save(im, 'indev_b38frost.png')


def food():
    rnd = random.Random(11172)
    im = noise(256, 256, (120, 70, 40), 10, 11173, 1.0)
    d = ImageDraw.Draw(im)
    for _ in range(40):
        x, y, r = rnd.uniform(0, 256), rnd.uniform(0, 256), rnd.uniform(10, 26)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(236, 232, 224))         # plates
        c = rnd.choice(((150, 80, 40), (200, 140, 60), (220, 60, 40), (90, 150, 60), (240, 200, 120)))
        d.ellipse((x - r * 0.65, y - r * 0.65, x + r * 0.65, y + r * 0.65), fill=c)
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    save(im, 'indev_b38food.png')
    save(im.resize((128, 128)), 'food1117.png', ITEMS)


def doll():
    im = noise(256, 256, (150, 128, 96), 12, 1039, 0.8)
    d = ImageDraw.Draw(im)
    for y in range(0, 256, 4):                                            # the weave
        d.line((0, y, 256, y), fill=(130, 110, 80), width=1)
    d.line((128, 30, 128, 220), fill=(40, 30, 24), width=6)               # the painted ribcage
    for k in range(6):
        y = 50 + k * 26
        d.arc((60, y - 10, 196, y + 30), 200, 340, fill=(40, 30, 24), width=5)
    save(im, 'indev_b38doll.png')


if __name__ == '__main__':
    for fn in (mirror, plaques, garland, banner, frost, food, doll):
        fn()
        print(fn.__name__)
