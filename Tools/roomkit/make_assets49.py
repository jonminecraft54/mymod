"""Assets of the forty-ninth batch: SCP-087-B (all made here).

  GFX\\map\\indev_087bnum.png    4 x 4 atlas of the stained metal number plates on the walls (1..16)
  GFX\\map\\indev_087blurk.png   the thing below: a tall dark shape, a pale smudge of a face (alpha)
  GFX\\map\\indev_087bsign.png   the plate over the stairwell: SCP-087-B / DO NOT DESCEND
"""
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
MAP = os.path.join(ROOT, 'GFX', 'map')
R = random.Random(87)


def font(sz, name='arialbd.ttf'):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\%s" % name, sz)
    except OSError:
        return ImageFont.load_default()


def plate(n):
    """a dented grey metal plate, a stencilled number (ref.: the plate with 7 on the brick wall)"""
    s = 128
    im = Image.new('L', (s, s), 150)
    im = ImageChops.add(im, Image.effect_noise((s, s), 26).convert('L'), 2.0, -64)
    d = ImageDraw.Draw(im)
    for _ in range(6):                                                         # stains
        x, y, r = R.randint(0, s), R.randint(0, s), R.randint(8, 30)
        d.ellipse((x - r, y - r, x + r, y + r), fill=R.randint(150, 172))
    im = im.filter(ImageFilter.GaussianBlur(2.0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, s - 1, s - 1), outline=110, width=3)
    d.text((s / 2, s / 2 + 4), str(n), font=font(30 if n < 10 else 26, 'times.ttf'), fill=20, anchor='mm')
    return Image.merge('RGB', [im] * 3)


def numbers():
    at = Image.new('RGB', (512, 512))
    for k in range(16):
        at.paste(plate(k + 1), ((k % 4) * 128, (k // 4) * 128))
    at.save(os.path.join(MAP, 'indev_087bnum.png'))


def lurker():
    w, h = 128, 256
    a = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(a)
    d.ellipse((40, 20, 88, 76), fill=255)                                      # head
    d.polygon([(30, 70), (98, 70), (112, 250), (16, 250)], fill=255)           # body, long
    d.polygon([(30, 80), (14, 200), (24, 202), (40, 100)], fill=255)           # arms hanging long
    d.polygon([(98, 80), (114, 200), (104, 202), (88, 100)], fill=255)
    a = a.filter(ImageFilter.GaussianBlur(5))
    rgb = Image.new('RGB', (w, h), (6, 6, 7))
    face = Image.new('L', (w, h), 0)
    fd = ImageDraw.Draw(face)
    fd.ellipse((48, 30, 80, 70), fill=120)
    fd.ellipse((54, 44, 62, 52), fill=0)
    fd.ellipse((66, 44, 74, 52), fill=0)
    fd.ellipse((60, 58, 68, 66), fill=0)
    face = face.filter(ImageFilter.GaussianBlur(2.5))
    rgb = ImageChops.add(rgb, Image.merge('RGB', [face] * 3))
    rgb.putalpha(a)
    rgb.save(os.path.join(MAP, 'indev_087blurk.png'))


def sign():
    im = Image.new('RGB', (512, 128), (30, 28, 26))
    d = ImageDraw.Draw(im)
    d.rectangle((4, 4, 507, 123), outline=(150, 140, 120), width=4)
    d.text((256, 46), 'SCP-087-B', font=font(48), fill=(215, 210, 200), anchor='mm')
    d.text((256, 96), 'DO NOT DESCEND', font=font(26), fill=(190, 60, 50), anchor='mm')
    im = ImageChops.multiply(im, Image.merge('RGB', [Image.effect_noise((512, 128), 30).convert('L').point(lambda v: 170 + v // 3)] * 3))
    im.save(os.path.join(MAP, 'indev_087bsign.png'))


def brick():
    """old, worn red brick (ref.: the stairwell screenshots): uneven bricks, dark sunken mortar, white salt stains"""
    W, H = 512, 512
    bw, bh, mort = 64, 32, 5
    im = Image.new('RGB', (W, H), (52, 48, 44))
    d = ImageDraw.Draw(im)
    for row in range(H // bh):
        off = (bw // 2) * (row % 2)
        for col in range(-1, W // bw + 1):
            x0 = col * bw + off + R.randint(-1, 1)
            y0 = row * bh + R.randint(-1, 1)
            base = R.choice([(118, 52, 38), (132, 62, 44), (104, 46, 36), (146, 74, 52), (96, 50, 42), (160, 86, 60)])
            v = R.randint(-14, 14)
            c = tuple(max(0, min(255, b + v)) for b in base)
            d.rounded_rectangle((x0 + mort // 2, y0 + mort // 2, x0 + bw - mort // 2, y0 + bh - mort // 2), radius=3, fill=c)
    n = Image.effect_noise((W, H), 40).convert('L')
    im = ImageChops.multiply(im, Image.merge('RGB', [n.point(lambda v: 150 + v // 3)] * 3))
    salt = Image.new('L', (W, H), 0)
    sd = ImageDraw.Draw(salt)
    for _ in range(26):                                                         # efflorescence
        x, y = R.randint(0, W), R.randint(0, H)
        for _ in range(R.randint(10, 40)):
            ex, ey = x + R.randint(-24, 24), y + R.randint(-10, 10)
            sd.ellipse((ex, ey, ex + R.randint(3, 9), ey + R.randint(2, 5)), fill=R.randint(90, 200))
    salt = salt.filter(ImageFilter.GaussianBlur(1.6))
    im = Image.composite(Image.new('RGB', (W, H), (206, 204, 196)), im, salt)
    grime = Image.new('L', (W, H), 0)
    gd = ImageDraw.Draw(grime)
    for _ in range(14):
        x = R.randint(0, W)
        gd.rectangle((x, 0, x + R.randint(10, 40), H), fill=R.randint(30, 70))
    grime = grime.filter(ImageFilter.GaussianBlur(14))
    im = Image.composite(Image.new('RGB', (W, H), (20, 18, 16)), im, grime)
    im.save(os.path.join(MAP, 'indev_087bbrick.png'))

if __name__ == '__main__':
    numbers()
    lurker()
    sign()
    brick()
    print('ok')
