"""Assets for the sixth batch (13 SCPs: 971, 1079-1083, 1145, 1200, 1879, 1916, 1921, 2789, 3182):
   GFX\\map\\indev_labels4.png (+labels4.json)     yellow SCP labels
   GFX\\map\\indev_doorplates.png (+doorplates.json) the black two-line plates beside containment doors
   GFX\\map\\indev_plates4.png (+plates4.json)     room name plates / hanging signs
   GFX\\map\\indev_props4.png (+props4.json)       packaging and paper: candy, gum, menu, labels
   GFX\\map\\indev_*.png                           room materials (restaurant, store, house, kiosk, tank)
   GFX\\npcs\\indev_*.jpg / .png                    NPC skins and the teddy's leather
   GFX\\items\\doc<n>.jpg, doc<n>b.jpg              two documents per SCP (own wording)"""
import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from make_assets3 import MAPDIR, NPCDIR, F, font, wear, mottle
from make_docs2 import typed, note
import make_npctex as NT

SCPS = [('971', 'SAFE'), ('1079', 'SAFE'), ('1080', 'SAFE'), ('1081', 'SAFE'), ('1082', 'EUCLID'), ('1083', 'SAFE'),
        ('1145', 'EUCLID'), ('1200', 'SAFE'), ('1879', 'KETER'), ('1916', 'SAFE'), ('1921', 'SAFE'), ('2789', 'EUCLID'),
        ('3182', 'SAFE')]
CLS = {'SAFE': (30, 120, 40), 'EUCLID': (200, 130, 20), 'KETER': (180, 24, 20)}


def ft(name, sz):
    return ImageFont.truetype(os.path.join(F, name), sz)


def labels():
    W = H = 1024
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (num, cls) in enumerate(SCPS):
        x, y = (i % 4) * 256, (i // 4) * 256
        rects[num] = (x / W, y / H, (x + 256) / W, (y + 256) / H)
        d.rectangle([x, y, x + 255, y + 255], fill=(238, 236, 228))
        d.rectangle([x, y, x + 255, y + 70], fill=(236, 208, 34))
        d.text((x + 12, y + 6), "SCP", font=font(46), fill=(20, 20, 20))
        cx, cy = x + 204, y + 36
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(20, 20, 20), width=4)
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=(20, 20, 20), width=3)
        for k in range(3):
            a = math.radians(90 + 120 * k)
            d.line([(cx + 11 * math.cos(a), cy - 11 * math.sin(a)), (cx + 28 * math.cos(a), cy - 28 * math.sin(a))], fill=(20, 20, 20), width=5)
        d.text((x + 12, y + 80), "SCP-" + num, font=font(36), fill=(20, 20, 20))
        d.text((x + 12, y + 126), "OBJECT CLASS:", font=font(17), fill=(20, 20, 20))
        d.text((x + 12, y + 148), cls, font=font(30), fill=CLS[cls])
        tx, ty = x + 54, y + 218
        d.polygon([(tx, ty - 30), (tx - 34, ty + 28), (tx + 34, ty + 28)], fill=(236, 208, 34), outline=(20, 20, 20))
        d.text((tx, ty + 6), "!", font=font(34), fill=(20, 20, 20), anchor='mm')
        d.rectangle([x + 150, y + 190, x + 244, y + 246], fill=(26, 26, 28))
        d.rectangle([x, y, x + 255, y + 255], outline=(30, 30, 30), width=3)
    wear(im, 41).save(os.path.join(MAPDIR, 'indev_labels4.png'))
    json.dump(rects, open('labels4.json', 'w'), indent=1)


def doorplates():
    """Black plates with white lettering, two lines, as beside the doors in the reference corridor."""
    W, H = 1024, 1024
    im = Image.new('RGB', (W, H), (16, 16, 16))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (num, cls) in enumerate(SCPS):
        x, y = (i % 4) * 256, (i // 4) * 256
        rects[num] = (x / W, y / H, (x + 256) / W, (y + 256) / H)
        d.rectangle([x + 4, y + 4, x + 251, y + 251], fill=(26, 26, 27))
        d.rectangle([x + 14, y + 14, x + 241, y + 241], outline=(150, 150, 146), width=5)
        d.text((x + 128, y + 92), "SCP-" + num, font=font(48 if len(num) == 4 else 54), fill=(228, 226, 220), anchor='mm')
        d.line([(x + 34, y + 134), (x + 222, y + 134)], fill=(150, 150, 146), width=4)
        d.text((x + 128, y + 182), cls, font=font(40), fill=(228, 226, 220), anchor='mm')
    wear(im, 42).save(os.path.join(MAPDIR, 'indev_doorplates.png'))
    json.dump(rects, open('doorplates.json', 'w'), indent=1)


def plates():
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    names = [('cont4l', 'CONTAINMENT 4-L'), ('storage13', 'STORAGE UNIT 13'), ('beefbelly', "BEEFBELLY BILL'S"),
             ('grocery', 'AISLE 3 - DO NOT ENTER'), ('testhouse', 'TEST HOUSE 1879'), ('chamber1145', 'CHAMBER 1145'),
             ('ltstorage', 'LONG-TERM STORAGE 6D'), ('aisle1', 'AISLE 1'), ('aisle2', 'AISLE 2'), ('aisle3', 'AISLE 3'),
             ('aisle4', 'AISLE 4'), ('noneat', 'NON-EDIBLE'), ('free', 'SPECIAL OFFER - FREE'), ('xenon', 'LAMP BREAKER')]
    for i, (key, text) in enumerate(names):
        x, y = (i % 2) * 512, (i // 2) * 73
        rects[key] = (x / W, y / H, (x + 512) / W, (y + 73) / H)
        yellow = key in ('grocery', 'chamber1145', 'noneat', 'xenon')
        red = key in ('beefbelly', 'free')
        bg = (176, 24, 22) if red else ((24, 64, 120) if key.startswith('aisle') else (22, 22, 22))
        d.rectangle([x, y, x + 511, y + 72], fill=bg)
        d.rectangle([x + 3, y + 3, x + 508, y + 69], outline=(220, 180, 40) if red else ((120, 110, 40) if yellow else (130, 130, 130)), width=4)
        sz = 50
        while d.textlength(text, font=font(sz)) > 480:
            sz -= 2
        fg = (250, 214, 40) if (yellow or red) else (238, 236, 228)
        d.text((x + 256, y + 37), text, font=font(sz), fill=fg, anchor='mm')
    wear(im, 43).save(os.path.join(MAPDIR, 'indev_plates4.png'))
    json.dump(rects, open('plates4.json', 'w'), indent=1)


def props():
    """One sheet of printed things: packaging, paper, labels."""
    W, H = 1024, 1024
    im = Image.new('RGB', (W, H), (230, 228, 220))
    d = ImageDraw.Draw(im)
    R = {}

    def box(key, x0, y0, x1, y1):
        R[key] = (x0 / W, y0 / H, x1 / W, y1 / H)
    # SCP-1079: a pink bonbon packet
    d.rectangle([0, 0, 255, 255], fill=(246, 150, 196))
    for k in range(9):
        d.ellipse([20 + (k % 3) * 74, 120 + (k // 3) * 42, 60 + (k % 3) * 74, 150 + (k // 3) * 42], fill=(255, 210, 232), outline=(200, 90, 150))
    d.text((128, 26), "Dr. Wondertainment's", font=ft('arialbd.ttf', 21), fill=(120, 30, 120), anchor='mm')
    d.text((128, 60), "BUBBLEBATH", font=ft('arialbd.ttf', 36), fill=(255, 255, 255), anchor='mm')
    d.text((128, 96), "BONBONS!", font=ft('arialbd.ttf', 34), fill=(255, 255, 255), anchor='mm')
    d.text((128, 246), "Only one sweet per sitting", font=ft('arial.ttf', 15), fill=(120, 30, 120), anchor='mm')
    box('bonbon', 0, 0, 256, 256)
    # SCP-1916: the moon rock box (child on a rocket in space)
    d.rectangle([256, 0, 511, 255], fill=(16, 18, 52))
    rng = np.random.default_rng(5)
    for _ in range(60):
        sx, sy = 256 + int(rng.integers(0, 255)), int(rng.integers(0, 255))
        d.point((sx, sy), fill=(255, 255, 220))
    d.ellipse([440, 30, 500, 90], fill=(220, 190, 120))
    d.polygon([(300, 210), (420, 110), (440, 130), (320, 230)], fill=(230, 230, 236))
    d.polygon([(420, 110), (452, 98), (440, 130)], fill=(220, 40, 40))
    d.ellipse([360, 128, 396, 164], outline=(200, 230, 255), width=3)
    d.text((384, 20), "ZERO-GEE-WHIZ!", font=ft('arialbd.ttf', 26), fill=(250, 214, 40), anchor='mm')
    d.text((384, 236), "MOON ROCKS", font=ft('arialbd.ttf', 30), fill=(250, 250, 250), anchor='mm')
    box('moonrocks', 256, 0, 512, 256)
    # SCP-1200: Tastes Like Chewing Gum, by The Factory
    d.rectangle([512, 0, 767, 127], fill=(46, 150, 92))
    d.text((640, 30), "TASTES LIKE", font=ft('arialbd.ttf', 26), fill=(255, 255, 255), anchor='mm')
    d.text((640, 66), "CHEWING GUM", font=ft('arialbd.ttf', 30), fill=(255, 250, 200), anchor='mm')
    d.text((640, 108), "THE FACTORY", font=ft('arial.ttf', 18), fill=(20, 40, 30), anchor='mm')
    box('gum', 512, 0, 768, 128)
    d.rectangle([512, 128, 767, 255], fill=(40, 70, 150))
    d.text((640, 192), "SECURE STORAGE", font=ft('arialbd.ttf', 24), fill=(240, 240, 240), anchor='mm')
    box('crate', 512, 128, 768, 256)
    # SCP-971: the worn delivery menu
    d.rectangle([768, 0, 1023, 330], fill=(236, 232, 214))
    d.text((896, 26), "QUIK 'N READY MEALZ", font=ft('arialbd.ttf', 20), fill=(30, 30, 30), anchor='mm')
    d.text((896, 52), "1-800-555-0971", font=ft('cour.ttf', 18), fill=(30, 30, 30), anchor='mm')
    items = ['A1  Hamburger', 'A2  Cheeseburger', 'B1  Chicken Sandwich', 'B4  Chicken Fingers', 'C1  Seasoned Fries',
             'C3  Curly Fries', 'D1  Soda (S/M/L)']
    for k, t in enumerate(items):
        d.text((786, 86 + k * 30), t, font=ft('cour.ttf', 17), fill=(40, 40, 40))
    box('menu', 768, 0, 1024, 330)
    # SCP-1921: arched sign and the reservoir label
    d.rectangle([0, 256, 511, 383], fill=(120, 40, 34))
    d.arc([20, 270, 490, 520], 200, 340, fill=(240, 200, 90), width=8)
    d.text((256, 318), "COTTON CANDY", font=ft('georgiab.ttf' if os.path.exists(os.path.join(F, 'georgiab.ttf')) else 'arialbd.ttf', 44), fill=(250, 226, 140), anchor='mm')
    d.text((256, 362), "- Free With Admission -", font=ft('georgia.ttf' if os.path.exists(os.path.join(F, 'georgia.ttf')) else 'arial.ttf', 22), fill=(250, 226, 140), anchor='mm')
    box('kiosksign', 0, 256, 512, 384)
    d.rectangle([512, 256, 767, 383], fill=(210, 206, 196))
    d.text((640, 300), "CLOWN", font=ft('arialbd.ttf', 40), fill=(150, 20, 20), anchor='mm')
    d.text((640, 346), "MILK", font=ft('arialbd.ttf', 40), fill=(150, 20, 20), anchor='mm')
    box('clownmilk', 512, 256, 768, 384)
    # SCP-2789: the free burger tray card
    d.rectangle([0, 384, 255, 511], fill=(220, 30, 30))
    d.text((128, 420), "TODAY ONLY", font=ft('arialbd.ttf', 26), fill=(255, 220, 40), anchor='mm')
    d.text((128, 470), "FREE BURGER", font=ft('arialbd.ttf', 32), fill=(255, 255, 255), anchor='mm')
    box('freecard', 0, 384, 256, 512)
    # SCP-1081 dials
    d.rectangle([256, 384, 511, 511], fill=(30, 30, 32))
    for k, t in enumerate(('DENSITY', 'RAPIDITY')):
        d.ellipse([280 + k * 110, 400, 340 + k * 110, 460], outline=(200, 200, 200), width=3)
        d.text((310 + k * 110, 480), t, font=ft('arial.ttf', 13), fill=(220, 220, 220), anchor='mm')
    box('dials', 256, 384, 512, 512)
    # SCP-1082: three dials on the safe door
    d.rectangle([512, 384, 767, 639], fill=(70, 74, 78))
    for k in range(3):
        cx, cy = 548 + k * 92, 512
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(40, 40, 42), outline=(170, 170, 170), width=4)
        d.line([(cx, cy), (cx + 18, cy - 18)], fill=(200, 200, 200), width=4)
    d.text((640, 600), "DO NOT OPEN", font=ft('arialbd.ttf', 24), fill=(220, 200, 60), anchor='mm')
    box('safedoor', 512, 384, 768, 640)
    # the 1879 house: a framed photo and the TV screen
    d.rectangle([768, 330, 1023, 520], fill=(90, 70, 50))
    d.rectangle([786, 348, 1005, 502], fill=(170, 190, 200))
    d.ellipse([850, 380, 940, 470], fill=(200, 170, 140))
    box('photo', 768, 330, 1024, 520)
    # the grocery store's faded wall advert
    d.rectangle([0, 640, 1023, 767], fill=(196, 60, 44))
    d.text((512, 690), "DENTON GROCERY", font=ft('arialbd.ttf', 64), fill=(250, 240, 220), anchor='mm')
    d.text((512, 745), "Fresh every day - since 1961", font=ft('arial.ttf', 26), fill=(250, 240, 220), anchor='mm')
    box('denton', 0, 640, 1024, 768)
    # a sheet of perforated calliope roll
    d.rectangle([0, 768, 511, 1023], fill=(226, 218, 190))
    for k in range(260):
        px, py = int(rng.integers(10, 500)), 780 + int(rng.integers(0, 230))
        d.rectangle([px, py, px + 6, py + 3], fill=(40, 34, 28))
    box('roll', 0, 768, 512, 1024)
    wear(im, 44).save(os.path.join(MAPDIR, 'indev_props4.png'))
    json.dump(R, open('props4.json', 'w'), indent=1)


def materials():
    mottle('indev_quartz.png', (150, 190, 226), (30, 30, 24), 51, sigma=2.0)
    mottle('indev_vinyl.png', (150, 26, 24), (24, 10, 10), 52, sigma=1.5)
    mottle('indev_kiosk.png', (126, 70, 40), (40, 24, 16), 53, sigma=1.4)
    mottle('indev_floss.png', (24, 22, 26), (14, 12, 14), 54, sigma=0.8)
    mottle('indev_teddy.png', (66, 46, 30), (18, 14, 10), 55, sigma=1.0, folder=NPCDIR)
    # red and white chequer for the restaurant
    a = np.zeros((128, 128, 3), dtype=np.uint8)
    yy, xx = np.mgrid[0:128, 0:128]
    chk = ((xx // 64) + (yy // 64)) % 2 == 0
    a[chk] = (196, 30, 28)
    a[~chk] = (236, 230, 220)
    Image.fromarray(a).filter(ImageFilter.GaussianBlur(0.6)).save(os.path.join(MAPDIR, 'indev_bbfloor.png'))
    # the Beefbelly Bill's board: logo and menu
    im = Image.new('RGB', (1024, 256), (30, 24, 20))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 12, 380, 244], 30, fill=(214, 34, 28), outline=(250, 210, 40), width=8)
    d.text((196, 92), "BEEFBELLY", font=ft('arialbd.ttf', 58), fill=(250, 214, 40), anchor='mm')
    d.text((196, 162), "BILL'S", font=ft('arialbd.ttf', 64), fill=(255, 255, 255), anchor='mm')
    menu = [('Bill Burger', '2.49'), ('Double Belly', '3.99'), ('Breakfast Biscuit', '1.89'), ('Fries', '1.29'), ('Shake', '1.79')]
    for k, (n, p) in enumerate(menu):
        d.text((420, 24 + k * 44), n, font=ft('arialbd.ttf', 30), fill=(244, 236, 220))
        d.text((990, 24 + k * 44), p, font=ft('arialbd.ttf', 30), fill=(250, 214, 40), anchor='ra')
    im.save(os.path.join(MAPDIR, 'indev_bbmenu.png'))
    # grocery shelf goods: four shelves of boxes and cans
    rng = np.random.default_rng(3182)
    im = Image.new('RGB', (512, 256), (60, 56, 52))
    d = ImageDraw.Draw(im)
    cols = [(196, 40, 36), (230, 190, 40), (40, 110, 180), (60, 150, 70), (220, 120, 30), (180, 180, 170), (120, 60, 140)]
    for s in range(4):
        y1 = 64 * s + 58
        d.rectangle([0, y1, 511, y1 + 6], fill=(150, 150, 146))
        x = 0
        while x < 512:
            w = int(rng.integers(16, 40))
            h = int(rng.integers(20, 50))
            if rng.random() < 0.18:
                x += w
                continue
            c = cols[int(rng.integers(0, len(cols)))]
            c = tuple(int(v * rng.uniform(0.55, 0.9)) for v in c)
            d.rectangle([x + 1, y1 - h, x + w - 1, y1], fill=c, outline=(30, 30, 30))
            d.rectangle([x + 3, y1 - h + 6, x + w - 3, y1 - h + 12], fill=(220, 214, 200))
            x += w
    im.save(os.path.join(MAPDIR, 'indev_goods.png'))
    # faded floral wallpaper for the test house
    im = Image.new('RGB', (256, 256), (196, 182, 150))
    d = ImageDraw.Draw(im)
    for x in range(0, 256, 64):
        d.rectangle([x, 0, x + 6, 255], fill=(172, 156, 124))
        for y in range(16, 256, 64):
            d.ellipse([x + 22, y, x + 46, y + 24], outline=(150, 96, 90), width=3)
            d.line([(x + 34, y + 24), (x + 34, y + 44)], fill=(96, 120, 80), width=2)
    wear(im, 45).save(os.path.join(MAPDIR, 'indev_wallpaper.png'))
    # red and white canopy stripes
    im = Image.new('RGB', (128, 128), (236, 230, 220))
    d = ImageDraw.Draw(im)
    for x in range(0, 128, 32):
        d.rectangle([x, 0, x + 15, 127], fill=(190, 30, 30))
    wear(im, 46).save(os.path.join(MAPDIR, 'indev_canopy.png'))
    # borosilicate water: blue, partly transparent
    a = np.zeros((64, 64, 4), dtype=np.uint8)
    a[..., 0], a[..., 1], a[..., 2], a[..., 3] = 90, 170, 255, 110
    Image.fromarray(a).save(os.path.join(MAPDIR, 'indev_water.png'))


def skins():
    """NPC skins on the Class-D body sheets."""
    a = np.asarray(Image.open(os.path.join(NPCDIR, 'scientist.jpg')).convert('RGB')).astype(float)
    NT.tint(a, NT.SHIRT_F, (126, 92, 58), 0.95, NT.pale)
    NT.tint(a, NT.SHIRT_B, (126, 92, 58), 0.95, NT.pale)
    NT.tint(a, NT.PANTS, (110, 82, 54), 1.0)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4)).save(os.path.join(NPCDIR, 'indev_salesman.jpg'), quality=92)
    a = np.asarray(Image.open(os.path.join(NPCDIR, 'scientist.jpg')).convert('RGB')).astype(float)
    NT.tint(a, NT.SHIRT_F, (44, 44, 48), 0.9, NT.pale)
    NT.tint(a, NT.SHIRT_B, (44, 44, 48), 0.9, NT.pale)
    NT.tint(a, NT.PANTS, (40, 40, 44), 1.0)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4)).save(os.path.join(NPCDIR, 'indev_ceo.jpg'), quality=92)
    a = np.asarray(Image.open(os.path.join(NPCDIR, 'janitor.jpg')).convert('RGB')).astype(float)
    NT.tint(a, NT.SHIRT_F, (214, 36, 30), 1.4, NT.blue)
    NT.tint(a, NT.SHIRT_B, (214, 36, 30), 1.4, NT.blue)
    NT.tint(a, NT.PANTS, (52, 52, 58), 1.4, NT.blue)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.rectangle([60, 120, 340, 140], fill=(250, 210, 40))
    im.filter(ImageFilter.GaussianBlur(0.4)).save(os.path.join(NPCDIR, 'indev_bbstaff.jpg'), quality=92)
    # SCP-1200-A: wrought iron under flaking layers of white, dim blue and yellow paint
    base = np.asarray(Image.open(os.path.join(NPCDIR, 'janitor.jpg')).convert('L')).astype(float) / 255.0
    Hh, Ww = base.shape
    rng = np.random.default_rng(1200)
    rust = np.array([112, 60, 34], dtype=float)
    out = np.zeros((Hh, Ww, 3))
    out[:] = rust
    for colour, cut in (((222, 222, 214), 0.55), ((96, 118, 150), 0.62), ((200, 180, 90), 0.7)):
        n = np.asarray(Image.fromarray((rng.random((Hh // 26, Ww // 26)) * 255).astype(np.uint8)).resize((Ww, Hh), Image.BICUBIC)
                       .filter(ImageFilter.GaussianBlur(2))).astype(float) / 255.0
        m = (n > cut)[..., None]
        out = np.where(m, np.array(colour, dtype=float), out)
    out *= (0.55 + 0.6 * base)[..., None]
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(os.path.join(NPCDIR, 'indev_paintiron.jpg'), quality=90)


def docs():
    typed('doc971', [('Clearance Level', '2'), ('Item #', 'SCP-971'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-971 is kept in its folder in file cabinet #26. Tests are limited to one a week, for the sake of the animals involved.'),
        ('h', 'Description:'),
        ('p', 'SCP-971 is a worn delivery menu for "Quik \'n Ready Mealz", a business that does not exist. Dialled '
              'by someone holding the menu, the number on it reaches an automated ordering line instead of the software '
              'help desk it belongs to. Some minutes later a paper bag of the order appears near the caller, always '
              'while nobody is looking at that spot.'),
        ('p', 'The food is ordinary fast food. The meat is from endangered species.'),
        ('h', 'Note:'),
        ('p', 'The menu and the phone are in the cell. {Hold the menu, then use the phone.} The bag will turn up '
              'wherever you are. Only one order is honoured per caller.'),
    ])
    typed('doc1079', [('Clearance Level', '1'), ('Item #', 'SCP-1079'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'All known packets are kept in Containment 4-L. Shipments found in shops are intercepted.'),
        ('h', 'Description:'),
        ('p', 'SCP-1079 are sweets in packets marked "Dr. Wondertainment\'s Bubblebath Bonbons!", with the warning '
              '"Only one sweet is to be taken per sitting". Seconds after eating one, the eater sweats a little of '
              'their own blood out through the skin as pink, bubblegum-scented foam. One sweet costs about a spoonful.'),
        ('p', 'The effect grows very fast with every further sweet. {Four in one sitting is fatal in nearly every case.}'),
        ('h', 'Note:'),
        ('p', 'Wait a few minutes between sweets and the count starts again. There is no reason to eat one at all.'),
    ])
    typed('doc1080', [('Clearance Level', '3'), ('Item #', 'SCP-1080'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1080 is kept in Storage Unit 13. No child under 13 is brought near it. SCP-1080-1 instances '
              'are housed with the object and answer to the number tattooed on the back of the left hand.'),
        ('h', 'Description:'),
        ('p', 'SCP-1080 is a windowless black chamber, 2 x 3 x 1.5 m, like a flotation tank without the water. It '
              'locks itself when a child is put inside. Days later the child comes out aged about twenty, with no '
              'personality and no speech. These are SCP-1080-1.'),
        ('p', 'An SCP-1080-1 obeys three commands only: "Come here", "Leave" and "Fix this" - the last only for a '
              'motor vehicle, which it repairs in minutes, better than any mechanic.'),
        ('h', 'Note:'),
        ('p', '{The tug that moved the pallets is broken, and a pallet is jammed against the store door.} The '
              'worker will follow you if you call him over.'),
    ])
    typed('doc1081', [('Clearance Level', '2'), ('Item #', 'SCP-1081'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1081 is kept in a lead-lined locker in Storage Unit 13, away from any electric current. Handlers wear noise-cancelling headphones.'),
        ('h', 'Description:'),
        ('p', 'SCP-1081 is a black speaker shaped like a small person, 30 cm tall, marked "Echus Projector Combine". '
              'A switch on its back reads INACTIVE, ACTIVE, SHUTDOWN and REACTIVATE. On SHUTDOWN it whistles and '
              'welcomes the listener to a performance, asking them not to talk. Everyone who hears it loses the '
              'ability to express anything at all.'),
        ('p', 'REACTIVATE thanks the audience and gives speech back - {but only if it is heard soon.} Left too '
              'long, the silence is permanent.'),
        ('h', 'Note:'),
        ('p', 'The test bench is still wired up. Leave the switch where it is.'),
    ])
    typed('doc1082', [('Clearance Level', '3'), ('Item #', 'SCP-1082'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1082 is kept in a triple-locked safe in Storage Unit 13. No test or access is authorised. '
              'Anyone who sees it is interviewed and given a Class-B amnestic, by force if necessary.'),
        ('h', 'Description:'),
        ('p', 'SCP-1082 is an object of a kind not recorded here. Seeing it, being near it, seeing a picture of it '
              'or talking to someone who has, makes a person unable to lie or say anything they do not literally '
              'mean, and intolerant of anyone who does.'),
        ('p', 'Untreated, this turns into the certainty that the Foundation exists to hide the object, and then '
              'into violence to get it out.'),
        ('h', 'Note:'),
        ('p', '{Document 1082-25 is kept on the safe. It was written by an exposed agent. Reading it is a risk.}'),
    ])
    typed('doc1083', [('Clearance Level', '2'), ('Item #', 'SCP-1083'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1083 is kept in a locker in Storage Unit 13, handled only with gloves. Anyone who touches it is sent for counselling.'),
        ('h', 'Description:'),
        ('p', 'SCP-1083 is a blue-tinted quartz skull, deformed, weighing 15 kg. Held in both hands it brings on '
              'one to three seconds of intense brain activity, felt as days or months in a dark void with a male '
              'voice that argues with the holder about every mistake of their life.'),
        ('p', 'Most come back thinking more clearly and knowing less. {Those who have hurt people come back broken.}'),
        ('h', 'Note:'),
        ('p', 'Operative 237 came back knowing things she had never been told. She is no longer with us.'),
    ])
    typed('doc1145', [('Clearance Level', '4'), ('Item #', 'SCP-1145'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1145 sits in a water-filled borosilicate tank in Chamber 1145, lit at all times. {It is never '
              'to be left unlit.} Two Class-D occupy the cells at the chamber walls in case it activates.'),
        ('h', 'Description:'),
        ('p', 'SCP-1145 is a 30 cm stuffed bear of tanned bear leather, stitched with an unknown tissue, recovered '
              'from Nagasaki. It is radioactive; the water absorbs it. Left without light for more than three '
              'seconds it becomes active and moves, through anything, to the nearest person.'),
        ('p', 'Then the radiation climbs every thirty seconds until that person picks it up. Held against bare '
              'skin it falls back to its resting level. Light makes it inactive again.'),
        ('h', 'Note:'),
        ('p', 'The lamp breaker is on the far wall of the chamber.'),
    ])
    typed('doc1200', [('Clearance Level', '2'), ('Item #', 'SCP-1200'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Packs of SCP-1200 seized in shops are kept in Containment 4-L. SCP-1200-A entities are held in '
              'individual reinforced containers.'),
        ('h', 'Description:'),
        ('p', 'SCP-1200 is chewing gum sold as "Tastes Like Chewing Gum" by "The Factory" - the maker of SCP-1125. '
              'Each flavour does something different when chewed: Lemons makes everything taste of lemon, Sunshine '
              'makes the chewer give off light, Rubik\'s Cube lets them rearrange their own body, and Moon\'s Shadow '
              'has killed.'),
        ('p', 'SCP-1200-A are figures of wrought iron under flaking paint, with a round hole where a face would be. '
              'They were found making one of the flavours, out of the dead.'),
        ('h', 'Note:'),
        ('p', 'The packs are not labelled with their flavour. {You find out by chewing.}'),
    ])
    typed('doc1879', [('Clearance Level', '3'), ('Item #', 'SCP-1879'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1879 cannot be contained. MTF Rho-4 ("Shoe Salesmen") deal with it at the lowest possible cost. '
              'Test House 1879 is a furnished mock-up used to draw it out.'),
        ('h', 'Description:'),
        ('p', 'SCP-1879 affects interior doors. Someone near an affected door hears knocking until they open it. '
              'Out steps a man of about 1.7 m who will not stop trying to sell them something. The price is '
              'rarely money and often harmful, and he will not explain it.'),
        ('p', 'Refused, he goes back through the door and comes out of another one later, pushier, with a higher '
              'price. Paid, he thanks you and leaves.'),
        ('h', 'Note:'),
        ('p', 'To buy, take his hand. To refuse, walk away. {He always comes back. The third time he is not polite.}'),
    ])
    typed('doc1916', [('Clearance Level', '1'), ('Item #', 'SCP-1916'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'All instances are kept in a sealed crate marked NON-EDIBLE in Containment 4-L.'),
        ('h', 'Description:'),
        ('p', 'SCP-1916 is a box of six gobstoppers sold as "Dr. Wondertainment\'s Zero-Gee-Whiz! Moon Rocks". '
              'Eaten, each one changes what the eater weighs for about ninety minutes, as if on another world: '
              'Martian Cherry, Venusian Berry, Lunar Lime, Jovian Jelly, Outer Space Strawberry, Planet X.'),
        ('p', 'The box says "Not for outdoors use" and "no more than one every four hours".'),
        ('h', 'Note:'),
        ('p', 'Lunar Lime makes running easy. Jovian Jelly makes standing hard. {Nobody knows what Planet X does.}'),
    ])
    typed('doc1921', [('Clearance Level', '2'), ('Item #', 'SCP-1921'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1921 is kept in Long-Term Storage 6D. The calliope rolls are stored apart from it.'),
        ('h', 'Description:'),
        ('p', 'SCP-1921 is a fire-damaged cotton candy kiosk from "Herman Fuller\'s Circus of the Disquieting". '
              'With the black fluid labelled "Clown Milk" in its reservoir, it spins black floss that vanishes on '
              'the tongue and settles round the brain. {The Clown Milk itself stops the heart.}'),
        ('p', 'A self-playing calliope at the back plays paper rolls. Anyone who has eaten the floss is changed by '
              'the tune: The Skater\'s Waltz makes nothing seem strange; When You\'re Smiling makes nothing seem bad.'),
        ('h', 'Note:'),
        ('p', 'The rolls are back in the calliope. Somebody has been playing them.'),
    ])
    typed('doc2789', [('Clearance Level', '3'), ('Item #', 'SCP-2789'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Instances of SCP-2789 are destroyed on discovery. The instance that has grown into this site\'s '
              'canteen is under review. Staff are not to eat there.'),
        ('h', 'Description:'),
        ('p', 'SCP-2789 is a fast food restaurant, "Beefbelly Bill\'s", staffed by people with no names who never '
              'leave. The food is ordinary. Thirty customers a year are offered a free burger. {Whoever eats it '
              'feels drawn somewhere new, and becomes the next restaurant.}'),
        ('p', 'SCP-2789-1 is an old man in formal clothes with a large moustache who calls himself the owner. He '
              'likes to ask how the menu could be better, and leaves business cards.'),
        ('h', 'Note:'),
        ('p', 'The building took in pipes and power from ours. Some of its insulation is skin.'),
    ])
    typed('doc3182', [('Clearance Level', '3'), ('Item #', 'SCP-3182'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The fixtures of Aisle 3 were moved here from the store in Denton, Missouri; the events came with '
              'them. {Nobody enters during a Deimos Event.} If you hear soft gurgling, leave Aisle 3 at once.'),
        ('h', 'Description:'),
        ('p', 'SCP-3182 is a closed grocery store. Each evening from 19:52 to 20:52, no light gets in and the '
              'people inside cannot find the way out, though the doors are where they always were. They feel '
              'sudden grief, remember the lives of old customers, and dread something on its way.'),
        ('p', 'Around Aisle 3 there is moaning, the sound of something heavy dragged, and shapes like people.'),
        ('h', 'Note:'),
        ('p', 'It has also started when somebody simply walks down Aisle 3.'),
    ])


NOTES = {
    'doc971b': ({0: 'Order log, cabinet #26', 1: 'Called 11:40 holding the menu.', 2: 'Ordered A1 and C1. The voice',
                 3: 'read my card number back to me.', 4: 'I have not got a card.', 6: 'The bag was on my chair when',
                 7: 'I turned round. It was hot.', 9: 'Burger tasted of nothing I know.'}, '- R. Tull'),
    'doc1079b': ({0: 'Stocktake - Wondertainment', 1: 'Bonbons: 3 packets short.', 2: 'Somebody ate them one at a',
                  3: 'time, a few minutes apart.', 5: 'Pink foam on the floor by the', 6: 'crate. Smells of bubblegum.',
                  8: 'It says ONE per sitting. It', 9: 'means it.'}, '- Stores, 4-L'),
    'doc1080b': ({0: 'Unit 13 - worker 0447', 1: 'Answers to his number only.', 2: '"Come here" - he follows you.',
                  3: '"Leave" - he goes back.', 4: '"Fix this" - only works on', 5: 'engines. He fixed the tug once',
                  6: 'in four minutes. It ran better', 7: 'than new.', 9: 'He does not look at you. Ever.'},
                 '- Unit 13 supervisor'),
    'doc1081b': ({0: 'Bench test 1081-2', 1: 'Do not set SHUTDOWN without', 2: 'headphones. We have none down',
                  3: 'here now.', 5: 'If somebody does: set it to', 6: 'REACTIVATE, quickly. A few', 7: 'minutes and it is too late.',
                  9: 'Kessler did not hurry. Kessler', 10: 'has not said a word since.'}, '- A. Vey'),
    'doc1082b': ({0: 'DOCUMENT 1082-25', 1: 'IT IS A [REDACTED]. IT IS NOT AN', 2: 'OBJECT. WHY DO YOU CALL IT AN',
                  3: 'OBJECT. YOU KNOW WHAT IT IS.', 5: 'THEY PUT IT IN A SAFE SO NOBODY', 6: 'WILL KNOW. I KNOW. I WILL NOT',
                  7: 'PRETEND. I WILL NOT SAY OBJECT.', 9: 'OPEN THE SAFE. EVERYONE SHOULD', 10: 'SEE IT. EVERYONE.'}, None),
    'doc1083b': ({0: 'Do not pick it up with both', 1: 'hands. One hand is safe.', 3: '237 held it 1.34 seconds. She',
                  4: 'said it took months. She came', 5: 'back knowing the office door', 6: 'code. Nobody had told her.',
                  8: 'D-class who held it said "he\'s', 9: 'right, I deserve it" and then', 10: 'hurt themselves.'}, '- Counselling, 38'),
    'doc1145b': ({0: 'Chamber 1145 - shift notes', 1: 'Breaker trips if the load spikes.', 2: 'Lamps out = 3 seconds.',
                  4: 'If it comes to you: PICK IT UP.', 5: 'Hold it. The counter drops. Then', 6: 'walk it to the breaker and get',
                  7: 'the lamps back on.', 9: 'Davis in cell 2 says it has', 10: 'never once come for him.'}, '- Dr. Okoye'),
    'doc1200b': ({0: 'Gum - flavours found so far', 1: 'Lemons - harmless.', 2: 'Sunshine - you glow. Nice.',
                  3: "Rubik's Cube - put yourself", 4: 'back the way you were. Try.', 5: "Moon's Shadow - you bleed",
                  6: 'later, with no wound.', 8: 'The iron one in the box watches', 9: 'whoever chews.'}, '- J. Ferro'),
    'doc1879b': ({0: 'Test House - Rho-4 debrief', 1: 'Knock on the closet. We opened.', 2: 'He sold Agent Ruiz a first',
                  3: 'aid kit for "a little blood".', 4: 'It was a little. Mostly.', 6: 'Refuse and he goes, and comes',
                  7: 'back out of another door with', 8: 'a worse price.', 10: 'The third time he hits you.'}, '- Rho-4'),
    'doc1916b': ({0: 'Moon Rocks - test summary', 1: 'Lunar Lime: weightless legs.', 2: 'Ran the length of the site.',
                  3: 'Jovian Jelly: could not stand', 4: 'for an hour.', 5: 'Outer Space Strawberry: hit the',
                  6: 'ceiling. Hard.', 7: 'Planet X: not authorised.', 9: 'One every four hours. Not two.'}, '- Xi-1964'),
    'doc1921b': ({0: 'Roll list (the ones we have)', 1: "B2-01 The Skater's Waltz", 2: '  nothing seems strange',
                  3: "B2-02 When You're Smiling", 4: '  nothing seems bad', 5: 'B2-03 Officer of the Year',
                  6: '  nothing seems wrong', 8: 'Only works if you ate the black', 9: 'floss first. Do NOT drink',
                  10: 'from the tank.'}, '- Storage 6D'),
    'doc2789b': ({0: "BEEFBELLY BILL'S", 1: 'Bill  -  Owner', 3: '"How would you make the', 4: 'menu better? Tell me.',
                  5: 'I listen to everyone."', 7: 'Ask about our special offer!'}, None),
    'doc3182b': ({0: 'Exploration log 3182-3 (copy)', 1: '19:52. Lights gone. Doors gone.', 2: 'I remembered buying bread here',
                  3: 'every Friday for thirty years.', 4: 'I have never been to Missouri.', 6: 'Something dragged in Aisle 3.',
                  7: 'Then a soft gurgle.', 9: 'We ran to the tills. It passed.', 10: 'Mills stayed in the aisle.'}, '- Team Deimos'),
}

TITLES = {
    'doc971': 'Document SCP-971', 'doc971b': 'Cabinet 26 Order Log', 'doc1079': 'Document SCP-1079', 'doc1079b': 'Wondertainment Stocktake',
    'doc1080': 'Document SCP-1080', 'doc1080b': 'Unit 13 Worker Card', 'doc1081': 'Document SCP-1081', 'doc1081b': 'Bench Test 1081-2',
    'doc1082': 'Document SCP-1082', 'doc1082b': 'Document 1082-25', 'doc1083': 'Document SCP-1083', 'doc1083b': 'Counselling Note',
    'doc1145': 'Document SCP-1145', 'doc1145b': 'Chamber 1145 Shift Notes', 'doc1200': 'Document SCP-1200', 'doc1200b': 'Gum Flavour List',
    'doc1879': 'Document SCP-1879', 'doc1879b': 'Rho-4 Debrief', 'doc1916': 'Document SCP-1916', 'doc1916b': 'Moon Rocks Test Summary',
    'doc1921': 'Document SCP-1921', 'doc1921b': 'Calliope Roll List', 'doc2789': 'Document SCP-2789', 'doc2789b': "Beefbelly Bill's Business Card",
    'doc3182': 'Document SCP-3182', 'doc3182b': 'Exploration Log 3182-3',
}


if __name__ == '__main__':
    labels()
    doorplates()
    plates()
    props()
    materials()
    skins()
    docs()
    for name, (rows, sign) in NOTES.items():
        note(name, rows, sign=sign)
    assert set(TITLES) == {'doc' + n for n, _ in SCPS} | {'doc%sb' % n for n, _ in SCPS}
    print('batch 6 assets, %d documents' % len(TITLES))
