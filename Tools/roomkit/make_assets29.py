r"""Textures of the twenty-ninth batch (original, drawn here or recoloured from the game's own):
     indev_867needle.png   SCP-867's needles: blue-spruce needles turned blood red       indev_867bark.png  dark red bark
     indev_867sign.png     BIO-CONTAINMENT SECTION E - full NBC + Kevlar                 indev_867decon.png herbicide shower
     indev_120pink.png     pastel pink paddling-pool plastic
     indev_120chart.png    the destination chart: the eleven configurations and their colours
     indev_120sign.png     SCP-120 - fortified outbuilding / armed guard
     indev_regolith.png    lunar regolith                     indev_lunarwall.png  white pressurised-module panels
     indev_earthview.png   the view from the observatory: black sky, stars, Earth over the grey plain of the mare
     indev_la32sign.png    LUNAR AREA-32 - SCP-120 RECEPTION (destination 9)
     indev_la32levels.png  the level directory (surface / sub-level 1 ...)
     indev_001door.png     the SCP-001 vault door plate        indev_l001screen.png the corrupted SCP-001 records terminal
     indev_2219label.png   "PORRIDGE": an unlicensed handheld cartridge label (our own drawing)
     indev_820stall.png    a souvenir-stall sign                indev_820pennant.png  a strip of pennants
     indev_820warn.png     SCP-820-JP - relocation every 2 hours
   python make_assets29.py"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from make_assets5 import MAPDIR

FB = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
FM = r"C:\Windows\Fonts\courbd.ttf"


def font(n, f=FB):
    return ImageFont.truetype(f, n)


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def noise(size, base, amp, blur=1.0, seed=0):
    rnd = random.Random(seed)
    im = Image.new('RGB', size, base)
    px = im.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = rnd.randint(-amp, amp)
            px[x, y] = tuple(max(0, min(255, c + n)) for c in base)
    return im.filter(ImageFilter.GaussianBlur(blur))


def plate(w, h, bg, lines, fg=(255, 255, 255), border=None, sizes=None):
    im = Image.new('RGB', (w, h), bg)
    d = ImageDraw.Draw(im)
    if border:
        d.rectangle([6, 6, w - 7, h - 7], outline=border, width=6)
    n = len(lines)
    sizes = sizes or [int(h / (n + 1.5))] * n
    tot = sum(sizes) * 1.25
    y = (h - tot) / 2 + sizes[0] * 0.6
    for t, s in zip(lines, sizes):
        d.text((w / 2, y), t, font=font(s), fill=fg, anchor='mm')
        y += s * 1.25
    return im


def needles():
    src = os.path.join(MAPDIR, 'indev_o_needles.png')
    im = Image.open(src).convert('RGB').resize((256, 256))
    g = ImageEnhance.Contrast(im.convert('L')).enhance(1.4)
    red = Image.merge('RGB', (g.point(lambda v: min(255, int(v * 1.25 + 40))), g.point(lambda v: int(v * 0.22)),
                              g.point(lambda v: int(v * 0.25))))
    save(red, 'indev_867needle.png')
    bark = Image.open(os.path.join(MAPDIR, 'indev_o_bark.png')).convert('RGB').resize((256, 256))
    bark = Image.blend(bark, Image.new('RGB', bark.size, (90, 20, 18)), 0.35)
    save(bark, 'indev_867bark.png')


def signs():
    save(plate(512, 256, (190, 160, 30), ['BIO-CONTAINMENT', 'SECTION E', 'FULL NBC + KEVLAR UNDERLAYER'],
               fg=(20, 20, 20), border=(20, 20, 20), sizes=[50, 56, 24]), 'indev_867sign.png')
    save(plate(384, 384, (30, 120, 60), ['HERBICIDAL', 'TREATMENT', 'ALL PERSONNEL', 'EXITING SECTION E', 'PUNCTURE MARKS?', '15 DAYS QUARANTINE'],
               border=(240, 240, 240), sizes=[40, 40, 22, 22, 26, 22]), 'indev_867decon.png')
    save(plate(512, 256, (60, 64, 70), ['SCP-120', 'AUTHORISED USE ONLY', 'DOCUMENT #120-23 REQUIRED'],
               border=(230, 190, 40), sizes=[70, 30, 24]), 'indev_120sign.png')
    save(plate(512, 256, (230, 232, 236), ['LUNAR AREA-32', 'SCP-120 RECEPTION', 'DESTINATION POINT 9 - MARE IMBRIUM'],
               fg=(30, 40, 70), border=(30, 40, 70), sizes=[62, 40, 22]), 'indev_la32sign.png')
    save(plate(384, 512, (34, 38, 46), ['LEVEL DIRECTORY', 'SURFACE', 'RECEPTION / OBSERVATORY', 'CARGO BAY / LANDER',
                                        'SUB-LEVEL 1', 'CONTAINMENT / STORAGE', 'SUB-LEVEL 2-4', 'RESTRICTED'],
               fg=(220, 230, 240), border=(120, 140, 170), sizes=[34, 30, 20, 20, 30, 20, 30, 20]), 'indev_la32levels.png')
    save(plate(512, 512, (70, 70, 74), ['SCP-001', 'LEVEL 5', 'O5 AUTHORISATION', 'FILE WITHHELD'],
               fg=(230, 40, 40), border=(200, 200, 200), sizes=[96, 60, 34, 34]), 'indev_001door.png')
    save(plate(384, 256, (150, 20, 20), ['SCP-820-JP', 'RELOCATE EVERY 2 HOURS', 'DO NOT LOOK AT THE BLADE'],
               border=(255, 255, 255), sizes=[54, 24, 22]), 'indev_820warn.png')


def chart():
    """the eleven configurations of SCP-120 and the colour of the liquid for each"""
    rows = [('1', 'PACIFIC (SCPS DEMETER)', (40, 110, 230)), ('2', 'GREENLAND', (245, 245, 250)),
            ('3', 'L3 - LOST', (6, 6, 8)), ('4', 'HIMALAYAS', (225, 228, 235)), ('5', 'L5 - LOST', (6, 6, 8)),
            ('6', 'SAHARA', (235, 205, 40)), ('7', 'GOBI', (130, 90, 50)), ('8', 'L2 - LOST', (6, 6, 8)),
            ('9', 'MARE IMBRIUM (AREA-32)', (140, 140, 145)), ('10', 'L4 - LOST', (6, 6, 8)), ('11', 'L1 - LOST', (6, 6, 8))]
    im = Image.new('RGB', (512, 640), (236, 236, 228))
    d = ImageDraw.Draw(im)
    d.text((256, 34), 'SCP-120 DESTINATIONS', font=font(34), fill=(20, 20, 20), anchor='mm')
    d.text((256, 66), 'cycle 1 -> 11 -> 1. One subject per use.', font=font(18, FR), fill=(40, 40, 40), anchor='mm')
    y = 96
    for n, t, c in rows:
        d.rectangle([24, y, 88, y + 40], fill=c, outline=(20, 20, 20), width=2)
        d.text((112, y + 20), n, font=font(24), fill=(20, 20, 20), anchor='lm')
        d.text((160, y + 20), t, font=font(20), fill=(170, 20, 20) if 'LOST' in t else (20, 20, 20), anchor='lm')
        y += 48
    save(im, 'indev_120chart.png')


def pink():
    im = noise((128, 128), (240, 170, 196), 6, 0.8, 120)
    d = ImageDraw.Draw(im)
    for y in range(0, 128, 32):                       # the welded seams of the inflatable rings
        d.line([(0, y), (128, y)], fill=(226, 150, 178), width=2)
    save(im, 'indev_120pink.png')


def lunar():
    im = noise((256, 256), (122, 122, 120), 26, 0.7, 32)
    d = ImageDraw.Draw(im)
    rnd = random.Random(32)
    for _ in range(40):                                # small craters and footprints in the dust
        x, y, r = rnd.randrange(256), rnd.randrange(256), rnd.randint(3, 14)
        d.ellipse([x - r, y - r, x + r, y + r], outline=(92, 92, 90), width=2)
        d.arc([x - r + 2, y - r + 2, x + r + 2, y + r + 2], 200, 340, fill=(160, 160, 156), width=1)
    save(im.filter(ImageFilter.GaussianBlur(0.6)), 'indev_regolith.png')
    w = noise((256, 256), (228, 230, 232), 5, 0.6, 33)
    d = ImageDraw.Draw(w)
    for k in range(0, 256, 128):
        d.rectangle([k + 2, 2, k + 125, 253], outline=(190, 194, 200), width=3)
        for y in (20, 236):
            for x in (k + 16, k + 112):
                d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(170, 174, 180))
    d.rectangle([0, 120, 256, 136], fill=(70, 90, 140))
    save(w, 'indev_lunarwall.png')
    # the view: stars, the Earth, the grey horizon of the mare
    W, H = 1024, 512
    v = Image.new('RGB', (W, H), (2, 2, 4))
    d = ImageDraw.Draw(v)
    for _ in range(700):
        x, y = rnd.randrange(W), rnd.randrange(int(H * 0.7))
        b = rnd.randint(90, 255)
        d.point((x, y), fill=(b, b, min(255, b + 10)))
    ex, ey, er = 690, 140, 74
    earth = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    e = ImageDraw.Draw(earth)
    e.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(30, 80, 170, 255))
    for _ in range(26):                                # continents and cloud bands
        x, y = ex + rnd.randint(-55, 55), ey + rnd.randint(-55, 55)
        r = rnd.randint(8, 22)
        if (x - ex) ** 2 + (y - ey) ** 2 < (er - 10) ** 2:
            e.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(60, 120, 60, 255) if rnd.random() < 0.5 else (235, 240, 245, 230))
    v = Image.alpha_composite(v.convert('RGBA'), earth).convert('RGB')
    # the night side: darken the right part of the disc with a soft terminator
    disc = Image.new('L', (W, H), 0)
    ImageDraw.Draw(disc).ellipse([ex - er, ey - er, ex + er, ey + er], fill=255)
    night = Image.new('L', (W, H), 0)
    ImageDraw.Draw(night).ellipse([ex - er + 40, ey - er - 20, ex + er + 90, ey + er + 20], fill=215)
    night = Image.composite(night.filter(ImageFilter.GaussianBlur(10)), Image.new('L', (W, H), 0), disc)
    v = Image.composite(Image.new('RGB', (W, H), (4, 6, 14)), v, night)
    d = ImageDraw.Draw(v)
    hz = int(H * 0.72)
    for y in range(hz, H):
        k = (y - hz) / (H - hz)
        g = int(70 + 70 * k)
        d.line([(0, y), (W, y)], fill=(g, g, g - 2))
    pts = [(0, hz)] + [(x, hz - int(18 * abs(math.sin(x / 90.0)) + rnd.randint(0, 6))) for x in range(0, W + 32, 32)] + [(W, hz)]
    d.polygon(pts, fill=(78, 78, 76))
    for _ in range(30):
        x, y = rnd.randrange(W), rnd.randint(hz + 10, H - 10)
        r = rnd.randint(6, 30)
        d.ellipse([x - r, y - r // 3, x + r, y + r // 3], outline=(60, 60, 58), width=2)
    save(v, 'indev_earthview.png')


def terminals():
    im = Image.new('RGB', (512, 384), (6, 14, 8))
    d = ImageDraw.Draw(im)
    lines = ['O5 COMMAND // LEVEL 6', 'SCP-001 INDEX ......... ', '  {$AUTH_PERSON}', '  {$PROTOCOL_CONTENT}',
             '  WARNING: {$WARNING_', '', '[ERROR]', '[ERROR]', '[ERROR]', 'MULTIPLE FAILURES REGISTERED.', 'CONTACT [hmcl-direct]']
    for i, t in enumerate(lines):
        d.text((24, 22 + i * 30), t, font=font(20, FM), fill=(230, 60, 50) if 'ERROR' in t or 'FAIL' in t else (90, 230, 120))
    save(im.filter(ImageFilter.GaussianBlur(0.5)), 'indev_l001screen.png')
    # PORRIDGE: our own cartridge label - a girl with yellow pigtails, a bowl, three bear silhouettes
    lab = Image.new('RGB', (256, 256), (70, 70, 80))
    d = ImageDraw.Draw(lab)
    d.rectangle([14, 14, 242, 242], fill=(240, 200, 60))
    d.text((128, 46), 'PORRIDGE', font=font(38), fill=(140, 30, 30), anchor='mm')
    d.ellipse([92, 90, 164, 162], fill=(250, 220, 190))
    d.ellipse([70, 96, 100, 150], fill=(250, 220, 40))
    d.ellipse([156, 96, 186, 150], fill=(250, 220, 40))
    for k, x in enumerate((40, 128, 216)):
        s = 18 + k * 4
        d.ellipse([x - s, 200 - s, x + s, 200 + s], fill=(90, 50, 20))
        d.ellipse([x - s, 196 - s * 2, x - s // 2, 196 - s - 4], fill=(90, 50, 20))
    d.text((128, 232), '5D EXPERIENTS!', font=font(16), fill=(30, 30, 30), anchor='mm')
    save(lab, 'indev_2219label.png')


def stall():
    im = Image.new('RGB', (512, 160), (200, 30, 40))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, 505, 153], outline=(255, 230, 120), width=6)
    d.text((256, 62), 'SOUVENIRS & SNACKS', font=font(42), fill=(255, 240, 210), anchor='mm')
    d.text((256, 118), 'free samples - famous local cookies!', font=font(24, FR), fill=(255, 230, 120), anchor='mm')
    save(im, 'indev_820stall.png')
    p = Image.new('RGBA', (512, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.line([(0, 10), (512, 10)], fill=(40, 40, 40, 255), width=4)
    cols = [(220, 40, 40), (240, 200, 40), (40, 160, 220), (60, 180, 80)]
    for i, x in enumerate(range(0, 512, 64)):
        d.polygon([(x + 4, 12), (x + 60, 12), (x + 32, 110)], fill=cols[i % 4] + (255,))
    save(p, 'indev_820pennant.png')


def registry():
    """Sub-Level 1's board: the anomalies under Lunar Area-32's jurisdiction as its facility dossier lists them,
    and what this sub-level holds itself"""
    rows = [('SCP-2493', 'EUCLID'), ('SCP-2651', 'SAFE'), ('SCP-2686', 'EUCLID'), ('SCP-2821', 'KETER'),
            ('SCP-3321', 'KETER'), ('EE-3570', 'N/A'), ('SCP-3609', 'EUCLID'), ('SCP-3655', 'SAFE'),
            ('SCP-4379', 'SAFE'), ('SCP-4731', 'SAFE'), ('SCP-4905', 'SAFE'), ('SCP-5775', 'EUCLID'),
            ('SCP-6981', 'SAFE'), ('SCP-7470', 'NEUTRALIZED'), ('SCP-7548', 'KETER'), ('SCP-8815', 'EUCLID'),
            ('SCP-9042', 'KETER')]
    im = Image.new('RGB', (512, 640), (28, 32, 40))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, 505, 633], outline=(120, 140, 170), width=4)
    d.text((256, 30), 'LUNAR AREA-32 - JURISDICTION', font=font(24), fill=(230, 235, 245), anchor='mm')
    col = {'SAFE': (90, 200, 110), 'EUCLID': (230, 190, 60), 'KETER': (230, 70, 60)}
    y = 64
    for i, (n, c) in enumerate(rows):
        x = 30 if i < 9 else 270
        yy = y + (i % 9) * 30
        d.text((x, yy), n, font=font(19), fill=(220, 225, 235))
        d.text((x + 120, yy), c, font=font(16), fill=col.get(c, (170, 170, 180)))
    d.line([(20, 350), (492, 350)], fill=(120, 140, 170), width=2)
    d.text((256, 374), 'HELD ON THIS SUB-LEVEL', font=font(22), fill=(230, 235, 245), anchor='mm')
    for k, (n, c, w) in enumerate((('SCP-001', 'EUCLID', 'vault - sealed, O5'), ('SCP-L001', 'EUCLID', 'records terminal'),
                                   ('SCP-2219', 'SAFE', 'test room, remote proxy'))):
        yy = 404 + k * 34
        d.text((30, yy), n, font=font(19), fill=(220, 225, 235))
        d.text((150, yy), c, font=font(16), fill=col[c])
        d.text((250, yy + 2), w, font=font(16, FR), fill=(180, 190, 205))
    d.text((256, 540), '(Former) SCP-2493 chamber: helium, 20 kPa,', font=font(16, FR), fill=(170, 180, 195), anchor='mm')
    d.text((256, 562), '270-285 K, rubber-padded. Kept in commission.', font=font(16, FR), fill=(170, 180, 195), anchor='mm')
    d.text((256, 600), 'All chambers can jettison their contents.', font=font(16), fill=(230, 120, 100), anchor='mm')
    save(im, 'indev_la32registry.png')


if __name__ == '__main__':
    registry()
    needles()
    signs()
    chart()
    pink()
    lunar()
    terminals()
    stall()
    print('batch 29 textures written')
