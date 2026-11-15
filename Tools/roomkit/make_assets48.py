"""Assets of the forty-eighth batch: SCP-806, the resurrection projector (all made here, nothing copied).

  GFX\\map\\indev_806metal.png    brushed dark gunmetal for the projector body (ref. image: the old projector)
  GFX\\map\\indev_806chrome.png   bright brushed steel for its plates and arms
  GFX\\map\\indev_806lens.png     the lens seen from the front: dozens of thin shaved-gemstone layers, glittering
  GFX\\map\\indev_806screen.png   the silver lenticular screen: fine vertical ribs
  GFX\\map\\indev_806f0..f5.png   six frames of monochrome footage (leader countdown, the cell (ref. image),
                                  the test card (ref. image), a person walking a corridor, a face, static)
  GFX\\map\\indev_806grey.png     the colourless skin every SCP-806-1 instance comes out with
  GFX\\map\\indev_806beam.png     a soft additive ray
  GFX\\map\\indev_806sign.png     CONTAINMENT LOCKER 8 / SCREENING ROOM signs
  GFX\\items\\filmreel.x + filmreel.png   the film reel item (a real disc with spokes, alpha-masked)
  GFX\\items\\INVreel806a..e.png  their inventory icons
  SFX\\Indev\\projector806.wav    the projector running: 24 fps gate clatter over the motor
"""
import math
import os
import random
import struct
import wave
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

ROOT = r"I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9"
MAP = os.path.join(ROOT, 'GFX', 'map')
ITEMS = os.path.join(ROOT, 'GFX', 'items')
R = random.Random(806)


def font(sz, bold=True):
    try:
        return ImageFont.truetype(r"C:\Windows\Fonts\%s" % ('arialbd.ttf' if bold else 'arial.ttf'), sz)
    except OSError:
        return ImageFont.load_default()


def grain(img, amt):
    n = Image.effect_noise(img.size, amt).convert('L')
    base = img.convert('L')
    return ImageChops.add(base, n, 2.0, -64).convert('RGB')


def brushed(size, base, var, streak):
    im = Image.new('L', size, base)
    px = im.load()
    for y in range(size[1]):
        row = base + R.randint(-var, var)
        for x in range(size[0]):
            px[x, y] = max(0, min(255, row + R.randint(-streak, streak)))
    return im.filter(ImageFilter.GaussianBlur((2.5, 0.3))).convert('RGB')


def metal():
    m = brushed((256, 256), 46, 6, 10)
    d = ImageDraw.Draw(m)
    for (x, y) in ((10, 10), (246, 10), (10, 246), (246, 246)):              # screw heads
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(88, 88, 90), outline=(20, 20, 20))
        d.line((x - 3, y, x + 3, y), fill=(30, 30, 30))
    d.rectangle((0, 0, 255, 255), outline=(18, 18, 18), width=3)
    m.save(os.path.join(MAP, 'indev_806metal.png'))
    c = brushed((256, 256), 168, 10, 16)
    ImageDraw.Draw(c).rectangle((0, 0, 255, 255), outline=(90, 90, 92), width=2)
    c.save(os.path.join(MAP, 'indev_806chrome.png'))


def lens():
    s = 256
    im = Image.new('RGB', (s, s), (8, 8, 10))
    d = ImageDraw.Draw(im)
    for k in range(40):                                                         # the shaved gem layers
        r = s / 2 - 4 - k * 2.9
        if r < 4:
            break
        g = 30 + int(70 * abs(math.sin(k * 1.7)))
        d.ellipse((s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r), outline=(g, g, g + 8), width=2)
    for _ in range(420):                                                        # glints
        a = R.uniform(0, 6.283)
        rr = R.uniform(0, s / 2 - 10) ** 0.9 * 1.1
        x, y = s / 2 + math.cos(a) * rr, s / 2 + math.sin(a) * rr
        v = R.randint(140, 255)
        d.point((x, y), fill=(v, v, v))
        if v > 235:
            d.line((x - 3, y, x + 3, y), fill=(v, v, v))
            d.line((x, y - 3, x, y + 3), fill=(v, v, v))
    d.ellipse((4, 4, s - 4, s - 4), outline=(120, 120, 124), width=6)          # the chrome bezel
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(os.path.join(MAP, 'indev_806lens.png'))


def screen():
    w, h = 512, 256
    im = Image.new('RGB', (w, h))
    px = im.load()
    for x in range(w):
        rib = 196 + int(22 * math.cos(x * 2 * math.pi / 4.0))
        for y in range(h):
            v = rib + R.randint(-5, 5)
            px[x, y] = (v, v, min(255, v + 4))
    ImageDraw.Draw(im).rectangle((0, 0, w - 1, h - 1), outline=(30, 30, 30), width=6)
    im.save(os.path.join(MAP, 'indev_806screen.png'))


def frame_base():
    return Image.new('RGB', (320, 240), (12, 12, 12))


def film_frames():
    """six monochrome frames - grain, scratches and a soft vignette on each"""
    frames = []
    # 0: the leader countdown
    im = frame_base()
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 319, 239), fill=(150, 150, 150))
    d.ellipse((70, 30, 250, 210), outline=(30, 30, 30), width=5)
    d.ellipse((95, 55, 225, 185), outline=(30, 30, 30), width=3)
    d.line((160, 10, 160, 230), fill=(30, 30, 30), width=3)
    d.line((20, 120, 300, 120), fill=(30, 30, 30), width=3)
    d.pieslice((70, 30, 250, 210), -90, 40, fill=(70, 70, 70))
    d.text((160, 120), '3', font=font(110), fill=(15, 15, 15), anchor='mm')
    frames.append(im)
    # 1: the cell from above (ref.: the trailer still) - tiles, the bed, the desk, the toilet, the lamp's pool of light
    im = frame_base()
    d = ImageDraw.Draw(im)
    d.polygon([(40, 230), (280, 230), (240, 40), (80, 40)], fill=(60, 60, 60))
    for k in range(9):
        t = k / 8.0
        xl, xr, yy = 80 - 40 * t, 240 + 40 * t, 40 + 190 * t
        d.line((xl, yy, xr, yy), fill=(25, 25, 25), width=2)
    for k in range(9):
        t = k / 8.0
        d.line((80 + 160 * t, 40, 40 + 240 * t, 230), fill=(25, 25, 25), width=2)
    d.polygon([(185, 60), (235, 60), (262, 175), (205, 175)], fill=(110, 110, 104), outline=(20, 20, 20))   # the bed
    d.polygon([(85, 55), (135, 55), (130, 95), (78, 95)], fill=(40, 40, 40))                                # the desk
    d.rectangle((92, 62, 118, 74), fill=(185, 185, 185))                                                     # papers
    d.ellipse((70, 160, 110, 200), fill=(45, 45, 45))                                                        # the toilet
    light = Image.new('L', im.size, 0)
    ImageDraw.Draw(light).ellipse((90, -60, 230, 120), fill=150)
    im = ImageChops.add(im, Image.merge('RGB', [light.filter(ImageFilter.GaussianBlur(40))] * 3))
    frames.append(im)
    # 2: the test card (ref.: the trailer's opening) - the motto smeared by tracking errors, no emblem
    im = frame_base()
    d = ImageDraw.Draw(im)
    d.rectangle((14, 30, 306, 210), fill=(70, 70, 70))
    d.text((160, 100), 'S C P', font=font(72), fill=(14, 14, 14), anchor='mm')
    d.text((160, 168), 'SECURE.  CONTAIN.  PROTECT.', font=font(17), fill=(14, 14, 14), anchor='mm')
    px = im.load()
    for y in range(240):                                                        # horizontal tearing
        if R.random() < 0.35:
            sh = R.randint(-9, 9)
            row = [px[x, y] for x in range(320)]
            for x in range(320):
                px[x, y] = row[(x - sh) % 320]
    frames.append(im)
    # 3: a person walking away down a corridor
    im = frame_base()
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (320, 0), (200, 90), (120, 90)], fill=(40, 40, 40))
    d.polygon([(0, 240), (320, 240), (200, 150), (120, 150)], fill=(75, 75, 75))
    d.polygon([(0, 0), (120, 90), (120, 150), (0, 240)], fill=(95, 95, 95))
    d.polygon([(320, 0), (200, 90), (200, 150), (320, 240)], fill=(85, 85, 85))
    d.rectangle((120, 90, 200, 150), fill=(150, 150, 150))
    d.ellipse((152, 98, 168, 114), fill=(20, 20, 20))
    d.rectangle((150, 113, 170, 150), fill=(20, 20, 20))
    frames.append(im)
    # 4: a face in three-quarter view, out of focus (generic, nobody in particular)
    im = frame_base()
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 319, 239), fill=(55, 55, 55))
    d.ellipse((105, 35, 225, 205), fill=(160, 160, 160))
    d.ellipse((115, 20, 235, 120), fill=(40, 40, 40))                           # hair
    d.ellipse((135, 105, 155, 117), fill=(40, 40, 40))
    d.ellipse((180, 105, 200, 117), fill=(40, 40, 40))
    d.line((168, 120, 160, 150), fill=(100, 100, 100), width=3)
    d.arc((140, 150, 190, 178), 10, 170, fill=(60, 60, 60), width=3)
    im = im.filter(ImageFilter.GaussianBlur(2.2))
    frames.append(im)
    # 5: static
    frames.append(Image.effect_noise((320, 240), 90).convert('RGB'))
    vig = Image.new('L', (320, 240), 0)
    ImageDraw.Draw(vig).ellipse((-60, -50, 380, 290), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(30))
    for k, im in enumerate(frames):
        im = grain(im, 40)
        d = ImageDraw.Draw(im)
        for _ in range(3):                                                      # scratches
            x = R.randint(0, 319)
            d.line((x, 0, x + R.randint(-6, 6), 239), fill=(200, 200, 200), width=1)
        for _ in range(12):                                                     # dust
            x, y = R.randint(0, 319), R.randint(0, 239)
            d.ellipse((x, y, x + R.randint(1, 3), y + R.randint(1, 3)), fill=(230, 230, 230) if R.random() < .5 else (0, 0, 0))
        im = Image.composite(im, Image.new('RGB', im.size, (0, 0, 0)), vig)
        im.resize((256, 192), Image.LANCZOS).save(os.path.join(MAP, 'indev_806f%d.png' % k))


def grey_skin():
    im = Image.new('L', (256, 256), 168)
    im = ImageChops.add(im, Image.effect_noise((256, 256), 30).convert('L'), 2.0, -64)
    im = im.filter(ImageFilter.GaussianBlur(1.2))
    Image.merge('RGB', [im] * 3).save(os.path.join(MAP, 'indev_806grey.png'))


def beam():
    im = Image.new('L', (64, 256), 0)
    d = ImageDraw.Draw(im)
    for x in range(64):
        v = int(255 * max(0, 1 - abs(x - 31.5) / 32) ** 2.2)
        d.line((x, 0, x, 255), fill=v)
    Image.merge('RGB', [im] * 3).save(os.path.join(MAP, 'indev_806beam.png'))


def signs():
    im = Image.new('RGB', (512, 256), (24, 24, 26))
    d = ImageDraw.Draw(im)
    for k, (t1, t2) in enumerate((('CONTAINMENT LOCKER 8', 'SCP-806  -  SAFE  -  FILM STORE'), ('SCREENING ROOM', 'A WATCHER MUST REMAIN AT ALL TIMES'))):
        y0 = k * 128
        d.rectangle((6, y0 + 6, 505, y0 + 121), outline=(200, 170, 40), width=4)
        d.text((256, y0 + 50), t1, font=font(40), fill=(225, 225, 225), anchor='mm')
        d.text((256, y0 + 95), t2, font=font(20, False), fill=(200, 170, 40), anchor='mm')
    im.save(os.path.join(MAP, 'indev_806sign.png'))


def reel_texture():
    s = 256
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = s / 2
    d.ellipse((4, 4, s - 4, s - 4), fill=(150, 150, 154, 255))                     # the flange
    d.ellipse((40, 40, s - 40, s - 40), fill=(34, 30, 26, 255))                    # the wound film
    for k in range(18):
        r = 40 + k * 2.6
        d.ellipse((c - (c - r), c - (c - r), c + (c - r), c + (c - r)), outline=(48, 42, 36, 255))
    for k in range(5):                                                         # the five windows
        a = k * 2 * math.pi / 5 - math.pi / 2
        pts = []
        for (ra, aa) in ((30, -0.42), (100, -0.28), (100, 0.28), (30, 0.42)):
            pts.append((c + math.cos(a + aa) * ra, c + math.sin(a + aa) * ra))
        d.polygon(pts, fill=(0, 0, 0, 0))
    d.ellipse((c - 26, c - 26, c + 26, c + 26), fill=(170, 170, 174, 255), outline=(60, 60, 60, 255), width=3)
    d.rectangle((c - 6, c - 6, c + 6, c + 6), fill=(0, 0, 0, 0))                 # the square hub hole
    im.save(os.path.join(ITEMS, 'filmreel.png'))
    return im


def reel_model():
    """GFX\\items\\filmreel.x: a flat disc (both faces) plus its rim, radius 1.5, 0.12 thick"""
    n = 32
    V, F, UV = [], [], []
    for side, y in ((0, 0.06), (1, -0.06)):
        ci = len(V)
        V.append((0, y, 0))
        UV.append((0.5, 0.5))
        for k in range(n):
            a = 2 * math.pi * k / n
            V.append((1.5 * math.cos(a), y, 1.5 * math.sin(a)))
            UV.append((0.5 + 0.49 * math.cos(a), 0.5 + 0.49 * math.sin(a)))
        for k in range(n):
            a, b = ci + 1 + k, ci + 1 + (k + 1) % n
            F.append((ci, b, a) if side == 0 else (ci, a, b))
    ri = len(V)
    for k in range(n):
        a = 2 * math.pi * k / n
        for y in (0.06, -0.06):
            V.append((1.5 * math.cos(a), y, 1.5 * math.sin(a)))
            UV.append((0.5 + 0.49 * math.cos(a), 0.5 + 0.49 * math.sin(a)))
    for k in range(n):
        a0, a1 = ri + 2 * k, ri + 2 * ((k + 1) % n)
        F.append((a0, a1, a0 + 1))
        F.append((a1, a1 + 1, a0 + 1))
    out = ['xof 0302txt 0032', 'Frame Reel {', 'Mesh ReelMesh {', '%d;' % len(V)]
    out += ['%f;%f;%f;%s' % (v[0], v[1], v[2], ',' if i < len(V) - 1 else ';') for i, v in enumerate(V)]
    out += ['%d;' % len(F)]
    out += ['3;%d,%d,%d;%s' % (f[0], f[1], f[2], ',' if i < len(F) - 1 else ';') for i, f in enumerate(F)]
    out += ['MeshMaterialList {', '1;', '%d;' % len(F)]
    out += ['0%s' % (',' if i < len(F) - 1 else ';') for i in range(len(F))]
    out += ['Material {', '1.0;1.0;1.0;1.0;;', '8.0;', '0.2;0.2;0.2;;', '0.0;0.0;0.0;;', 'TextureFilename { "filmreel.png"; }', '}', '}']
    out += ['MeshTextureCoords {', '%d;' % len(UV)]
    out += ['%f;%f;%s' % (u[0], u[1], ',' if i < len(UV) - 1 else ';') for i, u in enumerate(UV)]
    out += ['}', '}', '}']
    open(os.path.join(ITEMS, 'filmreel.x'), 'w').write('\n'.join(out) + '\n')


REELS = [('a', 'D', (200, 120, 40)), ('b', 'SEC', (60, 110, 200)), ('c', 'TOON', (190, 60, 160)),
         ('d', 'LIVE', (60, 170, 80)), ('e', '5.8s', (210, 40, 40))]


def reel_icons(tex):
    for key, label, col in REELS:
        im = Image.new('RGB', (64, 64), (40, 40, 40))
        r = tex.resize((58, 58), Image.LANCZOS)
        im.paste(r, (3, 3), r)
        d = ImageDraw.Draw(im)
        d.rectangle((2, 44, 61, 61), fill=col)
        d.text((32, 53), label, font=font(12), fill=(255, 255, 255), anchor='mm')
        im.save(os.path.join(ITEMS, 'INVreel806%s.png' % key))


def projector_sound():
    rate, secs = 22050, 4.0
    n = int(rate * secs)
    out = []
    for i in range(n):
        t = i / rate
        hum = 0.18 * math.sin(2 * math.pi * 60 * t) + 0.08 * math.sin(2 * math.pi * 120 * t + 0.4)
        ph = (t * 24.0) % 1.0                                                   # the gate, 24 times a second
        click = 0.0
        if ph < 0.06:
            click = (R.random() * 2 - 1) * 0.55 * (1 - ph / 0.06)
        whir = (R.random() * 2 - 1) * 0.05
        out.append(max(-1, min(1, hum + click + whir)))
    w = wave.open(os.path.join(ROOT, 'SFX', 'Indev', 'projector806.wav'), 'wb')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    w.writeframes(b''.join(struct.pack('<h', int(v * 26000)) for v in out))
    w.close()


if __name__ == '__main__':
    metal()
    lens()
    screen()
    film_frames()
    grey_skin()
    beam()
    signs()
    reel_model()
    reel_icons(reel_texture())
    projector_sound()
    print('ok')
