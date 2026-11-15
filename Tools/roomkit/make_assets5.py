"""Assets for the seventh batch (10 SCPs: 052, 024, 482, 953, 1269, 1440, 2701, 3325, 4258, 6096):
   GFX\\map\\indev_labels5.png (+labels5.json)         yellow SCP labels
   GFX\\map\\indev_doorplates5.png (+doorplates5.json) black plates beside containment doors
   GFX\\map\\indev_plates5.png (+plates5.json)         room name plates and signs
   GFX\\map\\indev_props5.png (+props5.json)           printed things: tablets, clock, menu board, forms, posters
   GFX\\map\\indev_neon5.png (+neon5.json)             things that glow: neon signs, the scoreboard, screens
   GFX\\map\\indev_*.png                               room materials (subway tile, stage, diner, plaster ...)
   GFX\\map\\indev_view0..4.png                        what Freddy's windows look out on
   GFX\\npcs\\indev_*.jpg                              NPC skins on the Class-D body sheets
   GFX\\items\\doc<n>.jpg, doc<n>b.jpg (+ a few c)     documents (own wording, after the wiki articles)"""
import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_assets3 import MAPDIR, NPCDIR, F, font, wear, mottle
from make_docs2 import typed, note
import make_npctex as NT

SCPS = [('052', 'EUCLID'), ('024', 'EUCLID'), ('482', 'EUCLID'), ('953', 'KETER'), ('1269', 'EUCLID'),
        ('1440', 'KETER'), ('2701', 'SAFE'), ('3325', 'EUCLID'), ('4258', 'EUCLID'), ('6096', 'KETER')]
CLS = {'SAFE': (30, 120, 40), 'EUCLID': (200, 130, 20), 'KETER': (180, 24, 20)}


def ft(name, sz):
    p = os.path.join(F, name)
    if not os.path.exists(p):
        p = os.path.join(F, 'arialbd.ttf' if 'b' in name else 'arial.ttf')
    return ImageFont.truetype(p, sz)


def save_map(im, name):
    im.save(os.path.join(MAPDIR, name))


# ===================================================================== labels and plates
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
    save_map(wear(im, 51), 'indev_labels5.png')
    json.dump(rects, open('labels5.json', 'w'), indent=1)


def doorplates():
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
    save_map(wear(im, 52), 'indev_doorplates5.png')
    json.dump(rects, open('doorplates5.json', 'w'), indent=1)


PLATES = [('platform', '59 ST PLATFORM ACCESS'), ('closed', 'CLOSED SAT-SUN 11PM-1AM: TRACK WORK'), ('uptown', 'UPTOWN    A    D'),
          ('hall99', 'HALLWAY 99'), ('kennel', 'K-9 KENNELS'), ('alert', 'KENNEL ALERT'), ('stage', 'SOUND STAGE 024'),
          ('obs', 'REMOTE OBSERVATION LAB'), ('mail', 'MAIL'), ('diner', "FREDDY'S DINER"), ('decon', 'DECONTAMINATION'),
          ('ch6096', 'HUMANOID CHAMBER 6096'), ('holdb', 'HOLDING 6096-B'), ('hoist', 'FAN HOIST'), ('block15', 'CELL BLOCK 15'),
          ('c667', 'CELL 667'), ('intake', 'INTAKE'), ('prop1269', 'PROPERTY 1269'), ('locker482', 'CONTAINMENT LOCKER 482'),
          ('psych', 'PSYCHIATRIC OBSERVATION'), ('rci', 'REAL CHARACTERS INDUSTRIES'), ('labs', 'LG-1 LABORATORIES'),
          ('pens', 'HOLDING PENS'), ('int142', 'INTERVIEW ROOM 142'), ('observe', 'OBSERVATION'), ('onair', 'ON AIR'),
          ('gamma6', 'MTF GAMMA-6 POST'), ('cham', 'CONTAINMENT CHAMBER')]
WARN = ('closed', 'alert', 'hoist', 'c667', 'intake', 'cham')


def plates():
    W, H = 1024, 1024
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (key, text) in enumerate(PLATES):
        x, y = (i % 2) * 512, (i // 2) * 73
        rects[key] = (x / W, y / H, (x + 512) / W, (y + 73) / H)
        yellow = key in WARN
        red = key == 'onair'
        bg = (176, 24, 22) if red else ((236, 232, 222) if key == 'mail' else (22, 22, 22))
        d.rectangle([x, y, x + 511, y + 72], fill=bg)
        d.rectangle([x + 3, y + 3, x + 508, y + 69], outline=(220, 180, 40) if red else ((120, 110, 40) if yellow else (130, 130, 130)), width=4)
        sz = 50
        while d.textlength(text, font=font(sz)) > 480:
            sz -= 2
        fg = (250, 214, 40) if yellow else ((255, 255, 255) if red else ((30, 30, 30) if key == 'mail' else (238, 236, 228)))
        if key == 'uptown':
            d.text((x + 40, y + 37), 'UPTOWN', font=font(46), fill=fg, anchor='lm')
            for k, (cx, letter) in enumerate(((x + 330, 'A'), (x + 410, 'D'))):
                d.ellipse([cx - 28, y + 9, cx + 28, y + 65], fill=(0, 57, 166) if letter == 'A' else (255, 99, 25))
                d.text((cx, y + 37), letter, font=font(40), fill=(255, 255, 255), anchor='mm')
        else:
            d.text((x + 256, y + 37), text, font=font(sz), fill=fg, anchor='mm')
    save_map(wear(im, 53), 'indev_plates5.png')
    json.dump(rects, open('plates5.json', 'w'), indent=1)


# ===================================================================== printed things
def props():
    W, H = 1024, 1024
    im = Image.new('RGB', (W, H), (230, 228, 220))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(57)
    R = {}

    def box(key, x0, y0, x1, y1):
        R[key] = (x0 / W, y0 / H, x1 / W, y1 / H)

    # the 59 ST mosaic name tablet: a tile border round white tesserae with the name in black
    x0, y0, x1, y1 = 0, 0, 512, 192
    for yy in range(y0, y1, 8):
        for xx in range(x0, x1, 8):
            border = (xx < x0 + 40 or xx >= x1 - 40 or yy < y0 + 32 or yy >= y1 - 32)
            if border:
                c = [(150, 54, 40), (196, 150, 70), (40, 96, 70), (230, 220, 190)][((xx - x0) // 8 + (yy - y0) // 8 * 3) % 4 if (xx // 16 + yy // 16) % 2 else 3]
            else:
                c = (236, 232, 220)
            j = rng.integers(-12, 12)
            d.rectangle([xx, yy, xx + 7, yy + 7], fill=tuple(int(max(0, min(255, v + j))) for v in c), outline=(150, 146, 136))
    txt = Image.new('L', (432, 128), 0)
    ImageDraw.Draw(txt).text((216, 64), "59 ST", font=ft('timesbd.ttf', 104), fill=255, anchor='mm')
    t = np.asarray(txt)
    for yy in range(0, 128, 8):
        for xx in range(0, 432, 8):
            if t[yy:yy + 8, xx:xx + 8].mean() > 90:
                d.rectangle([x0 + 40 + xx, y0 + 32 + yy, x0 + 47 + xx, y0 + 39 + yy], fill=(26, 26, 30), outline=(70, 70, 70))
    box('59st', x0, y0, x1, y1)
    # the platform clock, stopped at 11:57
    d.rectangle([512, 0, 704, 192], fill=(30, 30, 30))
    d.ellipse([522, 10, 694, 182], fill=(238, 234, 222), outline=(10, 10, 10), width=6)
    cx, cy = 608, 96
    for k in range(12):
        a = math.radians(k * 30)
        d.line([(cx + 70 * math.sin(a), cy - 70 * math.cos(a)), (cx + 80 * math.sin(a), cy - 80 * math.cos(a))], fill=(20, 20, 20), width=4)
    for (ang, L, w) in (((11 + 57 / 60.0) * 30, 46, 7), (57 * 6, 72, 4)):
        a = math.radians(ang)
        d.line([(cx, cy), (cx + L * math.sin(a), cy - L * math.cos(a))], fill=(10, 10, 10), width=w)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(150, 20, 20))
    box('clock', 512, 0, 704, 192)
    # STAY / LEAVE buttons
    for (x, col, word) in ((704, (40, 170, 60), 'STAY'), (864, (200, 30, 30), 'LEAVE')):
        d.rectangle([x, 0, x + 159, 159], fill=(24, 24, 26))
        d.ellipse([x + 14, 14, x + 145, 145], fill=col, outline=(240, 240, 240), width=5)
        d.text((x + 80, 80), word, font=font(30), fill=(255, 255, 255), anchor='mm')
    box('stay', 704, 0, 864, 160)
    box('leave', 864, 0, 1024, 160)
    # Freddy's letter board menu
    d.rectangle([0, 192, 511, 447], fill=(24, 22, 22))
    for yy in range(200, 447, 6):
        d.line([(0, yy), (511, yy)], fill=(34, 32, 32))
    d.text((256, 220), "FREDDY'S", font=font(36), fill=(240, 240, 236), anchor='mm')
    menu = [('HAMBURGER', '35'), ('CHEESEBURGER', '40'), ('CHERRY PIE', '15'), ('COFFEE  (BOTTOMLESS)', '05'), ('MALTED', '20'), ('BLUE PLATE SPECIAL', '??')]
    for k, (n, p) in enumerate(menu):
        d.text((24, 256 + k * 30), n, font=ft('courbd.ttf', 22), fill=(236, 236, 230))
        d.text((488, 256 + k * 30), p + 'c', font=ft('courbd.ttf', 22), fill=(236, 236, 230), anchor='ra')
    box('menuboard', 0, 192, 512, 448)
    # jukebox front
    d.rectangle([512, 192, 767, 511], fill=(60, 30, 20))
    d.pieslice([522, 196, 758, 430], 180, 360, fill=(230, 170, 60))
    d.pieslice([540, 212, 740, 412], 180, 360, fill=(250, 220, 140))
    for k in range(6):
        d.rectangle([538 + k * 36, 330, 562 + k * 36, 400], fill=[(220, 40, 40), (40, 160, 220), (240, 200, 40)][k % 3])
    d.rectangle([540, 410, 740, 470], fill=(240, 236, 220), outline=(120, 90, 40), width=4)
    for r_ in range(3):
        for c_ in range(4):
            d.rectangle([548 + c_ * 48, 416 + r_ * 18, 590 + c_ * 48, 430 + r_ * 18], outline=(150, 40, 40))
    d.rectangle([512, 470, 767, 511], fill=(160, 120, 60))
    box('jukebox', 512, 192, 768, 512)
    # the INTAKE clipboard
    d.rectangle([768, 192, 1023, 511], fill=(120, 84, 50))
    d.rectangle([786, 214, 1006, 500], fill=(232, 226, 204))
    d.rectangle([856, 196, 936, 226], fill=(150, 150, 150))
    d.text((896, 242), "INTAKE", font=ft('courbd.ttf', 22), fill=(30, 30, 30), anchor='mm')
    d.text((796, 262), "NAME", font=ft('courbd.ttf', 13), fill=(30, 30, 30))
    d.text((920, 262), "RELEASE DATE", font=ft('courbd.ttf', 11), fill=(30, 30, 30))
    for k in range(12):
        yy = 284 + k * 18
        d.line([(792, yy + 14), (1000, yy + 14)], fill=(150, 150, 170))
        L = int(rng.integers(50, 110))
        pts = [(800 + i * 3, yy + 8 + int(4 * math.sin(i * 1.7 + k))) for i in range(L // 3)]
        d.line(pts, fill=(40, 40, 90), width=1)
        d.text((924, yy), '%02d/%02d/%d' % (rng.integers(1, 13), rng.integers(1, 29), rng.integers(2030, 3399)), font=ft('cour.ttf', 11), fill=(40, 40, 90))
    box('intake', 768, 192, 1024, 512)
    # an iron-banded cell door (for the cells nobody opens)
    d.rectangle([0, 448, 255, 767], fill=(70, 50, 34))
    for xx in range(0, 256, 32):
        d.line([(xx, 448), (xx, 767)], fill=(48, 34, 24), width=2)
    for yy in (480, 600, 720):
        d.rectangle([0, yy, 255, yy + 16], fill=(52, 52, 54))
        for xx in range(10, 256, 30):
            d.ellipse([xx, yy + 4, xx + 8, yy + 12], fill=(90, 90, 92))
    d.rectangle([96, 520, 160, 560], fill=(30, 26, 22), outline=(60, 60, 62), width=4)
    box('celldoor', 0, 448, 256, 768)
    # SCP-1440's playing cards, worn soft
    d.rectangle([256, 512, 511, 639], fill=(40, 70, 46))
    for k in range(5):
        cx = 300 + k * 42
        card = Image.new('RGBA', (60, 86), (236, 230, 214, 255))
        cd = ImageDraw.Draw(card)
        cd.rectangle([0, 0, 59, 85], outline=(120, 110, 90), width=2)
        cd.text((8, 6), 'AKQJ9'[k], font=font(18), fill=(160, 30, 30) if k % 2 else (20, 20, 20))
        card = card.rotate(-20 + k * 10, expand=True, fillcolor=(0, 0, 0, 0))
        im.paste(card, (cx - card.width // 2, 572 - card.height // 2), card)
    box('cards', 256, 512, 512, 640)
    # Real Characters poster
    d.rectangle([512, 512, 767, 767], fill=(250, 214, 60))
    d.ellipse([560, 560, 720, 720], fill=(240, 120, 30))
    for ex in (612, 668):
        d.ellipse([ex - 18, 602, ex + 18, 642], fill=(255, 255, 255))
        d.ellipse([ex - 7, 614, ex + 7, 630], fill=(10, 10, 10))
    d.chord([590, 640, 690, 700], 0, 180, fill=(150, 20, 30))
    d.text((640, 530), "REAL CHARACTERS!", font=font(24), fill=(200, 30, 40), anchor='mm')
    d.text((640, 748), "You can't get more real than that!", font=ft('arial.ttf', 15), fill=(40, 40, 40), anchor='mm')
    box('poster3325', 512, 512, 768, 768)
    # the straitjacket's tag
    d.rectangle([768, 512, 1023, 639], fill=(236, 230, 214))
    for k, ln in enumerate(("Made in Tsiao-yan, China", "Hand Wash Only", "No Aserejena Powder", "M")):
        d.text((896, 534 + k * 26), ln, font=ft('arial.ttf', 17), fill=(90, 90, 96), anchor='mm')
    box('tag482', 768, 512, 1024, 640)
    # the painted words on the replaced mailboxes
    d.rectangle([768, 640, 1023, 767], fill=(36, 36, 38))
    for (tx, ty, w_, rot) in ((800, 660, "MINE", -6), (880, 700, "SHE'S MINE", 4), (790, 730, "DON'T", 0)):
        layer = Image.new('RGBA', (220, 50), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((4, 4), w_, font=font(30), fill=(220, 30, 30, 255))
        layer = layer.rotate(rot, expand=True)
        im.paste(layer, (tx, ty), layer)
    box('painted', 768, 640, 1024, 768)
    # a hotel-room seascape
    d.rectangle([256, 640, 511, 767], fill=(110, 90, 50))
    d.rectangle([268, 652, 499, 755], fill=(150, 190, 214))
    d.rectangle([268, 712, 499, 755], fill=(60, 110, 140))
    d.polygon([(330, 712), (360, 670), (390, 712)], fill=(240, 240, 236))
    box('hotelart', 256, 640, 512, 768)
    # specimen label, kennel card, the subway strip map
    d.rectangle([0, 768, 255, 895], fill=(236, 236, 226))
    d.text((128, 792), "RCI  SPECIMEN 1b-07", font=ft('courbd.ttf', 18), fill=(20, 20, 20), anchor='mm')
    d.text((128, 830), "GESTATION WK 31", font=ft('cour.ttf', 18), fill=(20, 20, 20), anchor='mm')
    d.text((128, 866), "DO NOT DECANT", font=ft('courbd.ttf', 20), fill=(170, 20, 20), anchor='mm')
    box('specimen', 0, 768, 256, 896)
    d.rectangle([256, 768, 511, 895], fill=(240, 236, 220))
    for k, ln in enumerate(("KENNEL 3  JINDO  'MAEUM'", "KENNEL 4  FOXHOUND 'RUSTY'", "KEEP THEM AWAKE", "KEEP THEM LOUD")):
        d.text((270, 780 + k * 28), ln, font=ft('courbd.ttf', 15), fill=(30, 30, 30) if k < 2 else (170, 20, 20))
    box('kennelcard', 256, 768, 512, 896)
    d.rectangle([0, 896, 1023, 1023], fill=(240, 238, 230))
    d.line([(40, 960), (984, 960)], fill=(0, 57, 166), width=10)
    for k, st in enumerate(("207 ST", "168 ST", "125 ST", "59 ST", "42 ST", "W 4 ST", "CANAL", "HOYT")):
        xx = 60 + k * 128
        d.ellipse([xx - 12, 948, xx + 12, 972], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
        d.text((xx, 925), st, font=font(18), fill=(20, 20, 20), anchor='mm')
    d.ellipse([20, 984, 52, 1016], fill=(0, 57, 166))
    d.text((36, 1000), "A", font=font(22), fill=(255, 255, 255), anchor='mm')
    d.text((70, 1000), "8 AV EXPRESS", font=font(20), fill=(20, 20, 20), anchor='lm')
    box('stripmap', 0, 896, 1024, 1024)
    # a hotel TV cabinet front and a sink cabinet (doors only)
    d.rectangle([512, 768, 767, 895], fill=(110, 80, 52))
    for xx in (520, 642):
        d.rectangle([xx, 776, xx + 116, 887], outline=(70, 50, 30), width=4)
        d.ellipse([xx + 100, 826, xx + 108, 834], fill=(200, 180, 120))
    box('sinkcab', 512, 768, 768, 896)
    d.rectangle([768, 768, 1023, 895], fill=(200, 200, 196))
    d.text((896, 800), "NOTICE", font=font(26), fill=(170, 20, 20), anchor='mm')
    d.text((896, 840), "DO NOT TOUCH THE SHEET", font=ft('arialbd.ttf', 15), fill=(20, 20, 20), anchor='mm')
    d.text((896, 866), "(you can't anyway)", font=ft('arial.ttf', 14), fill=(60, 60, 60), anchor='mm')
    box('sheetnotice', 768, 768, 1024, 896)
    save_map(wear(im, 54), 'indev_props5.png')
    json.dump(R, open('props5.json', 'w'), indent=1)


def neon():
    """Things that glow (laid with an emissive material, so the lightmap leaves them bright)."""
    W, H = 1024, 640
    im = Image.new('RGB', (W, H), (8, 6, 10))
    d = ImageDraw.Draw(im)
    R = {}

    def glow_text(xy, text, f, core, halo):
        layer = Image.new('RGB', (W, H), (0, 0, 0))
        ImageDraw.Draw(layer).text(xy, text, font=f, fill=halo, anchor='mm')
        layer = layer.filter(ImageFilter.GaussianBlur(9))
        arr = np.asarray(im).astype(int) + np.asarray(layer).astype(int)
        im.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)))
        ImageDraw.Draw(im).text(xy, text, font=f, fill=core, anchor='mm')

    glow_text((512, 80), "TAKE THE PRIZE!", font(96), (255, 236, 250), (255, 40, 180))
    R['takeprize'] = (0, 0, 1, 160 / H)
    glow_text((256, 240), "Freddy's", ft('georgiaz.ttf', 92), (255, 230, 230), (255, 30, 30))
    R['freddys'] = (0, 160 / H, 0.5, 320 / H)
    d = ImageDraw.Draw(im)
    d.rectangle([520, 176, 760, 304], fill=(40, 6, 6))
    glow_text((640, 240), "APPLAUSE", font(44), (255, 220, 200), (255, 60, 20))
    R['applause'] = (512 / W, 160 / H, 768 / W, 320 / H)
    d = ImageDraw.Draw(im)
    d.rectangle([776, 170, 1016, 310], fill=(16, 10, 6), outline=(80, 60, 30), width=4)
    glow_text((896, 210), "ROUND", font(30), (255, 200, 90), (255, 120, 0))
    glow_text((896, 268), "1  2  3", ft('courbd.ttf', 44), (255, 200, 90), (255, 120, 0))
    R['score'] = (768 / W, 160 / H, 1, 320 / H)
    # TV static and a TV test card
    rng = np.random.default_rng(6096)
    a = np.asarray(im).copy()
    a[330:500, 10:246] = (rng.random((170, 236, 1)) * 200 + 30).astype(np.uint8)
    im = Image.fromarray(a)
    R['static'] = (0, 320 / H, 256 / W, 1)
    d = ImageDraw.Draw(im)
    bars = [(200, 200, 200), (200, 200, 0), (0, 200, 200), (0, 200, 0), (200, 0, 200), (200, 0, 0), (0, 0, 200)]
    for k, c in enumerate(bars):
        d.rectangle([266 + k * 33, 330, 298 + k * 33, 470], fill=c)
    d.rectangle([266, 470, 497, 500], fill=(20, 20, 30))
    R['testcard'] = (256 / W, 320 / H, 512 / W, 1)
    glow_text((768, 416), "DINER", font(110), (230, 250, 255), (30, 200, 255))
    R['dinersign'] = (512 / W, 320 / H, 1, 512 / H)
    # the final podium buttons, lit from inside
    d = ImageDraw.Draw(im)
    for k, (word, col, halo) in enumerate((("TAKE IT", (80, 230, 100), (20, 160, 40)), ("RISK IT", (255, 90, 80), (200, 20, 20)))):
        x = k * 160
        d.ellipse([x + 12, 524, x + 148, 636], fill=tuple(int(c * 0.6) for c in col), outline=(240, 240, 240), width=4)
        glow_text((x + 80, 580), word, font(26), (255, 255, 255), halo)
        R['take' if k == 0 else 'risk'] = (x / W, 512 / H, (x + 160) / W, 1)
    im.save(os.path.join(MAPDIR, 'indev_neon5.png'))
    json.dump(R, open('neon5.json', 'w'), indent=1)


# ===================================================================== materials
def noise(h, w, seed, scale=8, blur=2.0):
    rng = np.random.default_rng(seed)
    n = Image.fromarray((rng.random((max(2, h // scale), max(2, w // scale))) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(n.filter(ImageFilter.GaussianBlur(blur))).astype(float) / 255.0


def subtile():
    """White glazed subway tile, a coloured mosaic band, a brown base course. Mapped 512 units wide
    over the full 520-unit wall height (v = 0 at the ceiling)."""
    W, H = 512, 512
    im = Image.new('RGB', (W, H), (128, 126, 118))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(52)
    th, tw = 16, 32
    for r in range(H // th):
        off = (r % 2) * tw // 2
        for c in range(-1, W // tw + 1):
            x0 = c * tw + off
            y0 = r * th
            v = int(rng.integers(214, 236))
            d.rectangle([x0 + 1, y0 + 1, x0 + tw - 2, y0 + th - 2], fill=(v, v - 2, v - 8))
            d.line([(x0 + 3, y0 + 3), (x0 + tw - 6, y0 + 3)], fill=(250, 250, 246))
    y_band0, y_band1 = int((520 - 430) / 520 * H), int((520 - 380) / 520 * H)
    d.rectangle([0, y_band0, W, y_band1], fill=(60, 40, 30))
    for xx in range(0, W, 8):
        for yy in range(y_band0 + 2, y_band1 - 2, 8):
            k = (xx // 8 + (yy - y_band0) // 8) % 6
            c = [(170, 60, 44), (200, 160, 80), (46, 110, 80), (200, 160, 80), (170, 60, 44), (232, 222, 196)][k]
            d.rectangle([xx + 1, yy + 1, xx + 7, yy + 7], fill=c)
    y_base = int((520 - 56) / 520 * H)
    d.rectangle([0, y_base, W, H], fill=(96, 62, 40))
    for xx in range(0, W, 32):
        d.line([(xx, y_base), (xx, H)], fill=(70, 46, 30), width=2)
    d.rectangle([0, 0, W, int(30 / 520 * H)], fill=(70, 70, 66))
    a = np.asarray(im).astype(float)
    a *= (0.86 + 0.18 * noise(H, W, 521, 16, 6))[..., None]
    grime = noise(H, W, 522, 4, 1.5)
    a[grime > 0.78] *= 0.82
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_subtile.png'))


def simple_materials():
    rng = np.random.default_rng(55)
    # track ballast
    a = np.zeros((256, 256, 3))
    a[:] = 52
    for _ in range(900):
        x, y, r = rng.integers(0, 256), rng.integers(0, 256), rng.integers(3, 9)
        v = rng.integers(40, 110)
        yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
        m = (xx * xx + yy * yy) <= r * r
        ys, xs = (y + yy) % 256, (x + xx) % 256
        a[ys[m[:, 0]] if False else (y + np.nonzero(m)[0] - r) % 256, (x + np.nonzero(m)[1] - r) % 256] = (v, v - 4, v - 10)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)).save(os.path.join(MAPDIR, 'indev_ballast.png'))
    # platform edge: yellow with raised dots
    im = Image.new('RGB', (64, 64), (226, 186, 30))
    d = ImageDraw.Draw(im)
    for yy in range(4, 64, 16):
        for xx in range(4, 64, 16):
            d.ellipse([xx, yy, xx + 8, yy + 8], fill=(246, 210, 60), outline=(170, 140, 20))
    wear(im, 56).save(os.path.join(MAPDIR, 'indev_edge.png'))
    # green-painted steel with rivets (subway columns)
    im = Image.new('RGB', (128, 128), (46, 62, 46))
    d = ImageDraw.Draw(im)
    for yy in range(8, 128, 24):
        for xx in (10, 54, 98):
            d.ellipse([xx, yy, xx + 6, yy + 6], fill=(70, 88, 70), outline=(28, 36, 28))
    wear(im, 57).save(os.path.join(MAPDIR, 'indev_greenpaint.png'))
    # the stage: black gloss floor, velvet curtain, a light-up tile when off, blue bleachers
    a = np.zeros((256, 256, 3)) + 18
    a += 30 * noise(256, 256, 58, 32, 10)[..., None]
    for k in range(0, 256, 64):
        a[k:k + 2, :] = 60
        a[:, k:k + 2] = 60
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_stagefloor.png'))
    xx = np.arange(128)
    fold = 0.55 + 0.45 * np.sin(xx / 128 * 2 * np.pi * 4) ** 2
    a = np.zeros((512, 128, 3))
    a[..., 0] = 70 * fold
    a[..., 1] = 10 * fold
    a[..., 2] = 22 * fold
    a *= (0.85 + 0.2 * noise(512, 128, 59, 8, 2))[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_curtain.png'))
    im = Image.new('RGB', (128, 128), (20, 22, 30))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 127, 127], outline=(90, 90, 100), width=6)
    d.rectangle([10, 10, 117, 117], fill=(30, 34, 46))
    im.save(os.path.join(MAPDIR, 'indev_gstile.png'))
    im = Image.new('RGB', (128, 128), (30, 60, 140))
    d = ImageDraw.Draw(im)
    for yy in range(0, 128, 32):
        d.rectangle([0, yy, 127, yy + 4], fill=(20, 30, 70))
    wear(im, 60).save(os.path.join(MAPDIR, 'indev_bleach.png'))
    # the diner: black and white floor, two-tone wall (cream over red, a chrome strip), chrome
    a = np.zeros((128, 128, 3), dtype=np.uint8)
    yy, xx = np.mgrid[0:128, 0:128]
    chk = ((xx // 64) + (yy // 64)) % 2 == 0
    a[chk] = (24, 24, 26)
    a[~chk] = (232, 230, 222)
    wear(Image.fromarray(a), 61).save(os.path.join(MAPDIR, 'indev_dinerfloor.png'))
    H = 352
    im = Image.new('RGB', (256, H), (236, 226, 196))
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 140, 255, H - 1], fill=(170, 26, 30))
    d.rectangle([0, H - 152, 255, H - 140], fill=(206, 210, 214))
    d.line([(0, H - 150), (255, H - 150)], fill=(250, 250, 252), width=2)
    d.rectangle([0, H - 14, 255, H - 1], fill=(30, 30, 32))
    d.rectangle([0, 0, 255, 22], fill=(40, 150, 150))
    wear(im, 62).save(os.path.join(MAPDIR, 'indev_dinerwall.png'))
    yy = np.linspace(0, 1, 64)[:, None]
    a = np.zeros((64, 64, 3))
    a[:] = (150 + 90 * np.abs(np.sin(yy * 7.0)))[..., None]
    a[..., 2] += 10
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_chrome.png'))
    # the 6096 "hotel room": carpet, wallpaper
    im = Image.new('RGB', (256, 256), (92, 26, 34))
    d = ImageDraw.Draw(im)
    for yy in range(0, 256, 64):
        for xx in range(0, 256, 64):
            d.polygon([(xx + 32, yy + 6), (xx + 58, yy + 32), (xx + 32, yy + 58), (xx + 6, yy + 32)], outline=(170, 130, 60), width=3)
    wear(im, 63).save(os.path.join(MAPDIR, 'indev_carpet.png'))
    im = Image.new('RGB', (192, 192), (206, 192, 160))
    d = ImageDraw.Draw(im)
    for xx in range(0, 192, 48):
        d.rectangle([xx, 0, xx + 14, 191], fill=(192, 176, 140))
        d.line([(xx + 24, 0), (xx + 24, 191)], fill=(180, 160, 120), width=1)
    wear(im, 64).save(os.path.join(MAPDIR, 'indev_hotelwall.png'))
    # 1840s whitewash over stone, peeling
    W_, H_ = 512, 512
    stone = np.zeros((H_, W_, 3))
    stone[:] = (120, 110, 96)
    im = Image.fromarray(stone.astype(np.uint8))
    d = ImageDraw.Draw(im)
    for r in range(0, H_, 48):
        off = (r // 48 % 2) * 40
        for c in range(-1, W_ // 80 + 1):
            x0 = c * 80 + off
            v = int(rng.integers(90, 140))
            d.rectangle([x0 + 3, r + 3, x0 + 76, r + 45], fill=(v, v - 8, v - 20))
    st = np.asarray(im).astype(float)
    wash = np.zeros_like(st)
    wash[:] = (222, 218, 206)
    peel = noise(H_, W_, 65, 12, 2.5) * 0.6 + noise(H_, W_, 75, 48, 8) * 0.4
    m = (peel < 0.3)[..., None]
    a = np.where(m, st, wash * (0.85 + 0.15 * noise(H_, W_, 66, 8, 2))[..., None])
    stain = noise(H_, W_, 67, 64, 12)
    a *= (0.75 + 0.3 * stain)[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(os.path.join(MAPDIR, 'indev_plaster.png'))
    # Property 1269: artificial lawn, white siding, asphalt
    a = np.zeros((128, 128, 3))
    a[..., 1] = 110 + 60 * noise(128, 128, 68, 2, 0.6)
    a[..., 0] = 40 + 20 * noise(128, 128, 69, 4, 1)
    a[..., 2] = 34
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_lawn.png'))
    im = Image.new('RGB', (128, 128), (226, 224, 216))
    d = ImageDraw.Draw(im)
    for yy in range(0, 128, 16):
        d.rectangle([0, yy + 12, 127, yy + 15], fill=(170, 168, 160))
    wear(im, 70).save(os.path.join(MAPDIR, 'indev_siding.png'))
    a = np.zeros((256, 256, 3)) + 58
    a += 40 * noise(256, 256, 71, 2, 0.6)[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_asphalt.png'))
    # padded cell wall, ward lino
    im = Image.new('RGB', (128, 128), (226, 224, 214))
    a = np.asarray(im).astype(float)
    yy, xx = np.mgrid[0:128, 0:128]
    u, v = (xx + yy) % 64 / 64.0, (xx - yy) % 64 / 64.0
    puff = np.sin(u * np.pi) * np.sin(v * np.pi)
    a *= (0.72 + 0.32 * puff)[..., None]
    for (bx, by) in ((0, 0), (64, 0), (0, 64), (64, 64), (32, 32), (96, 32), (32, 96), (96, 96)):
        a[max(0, by - 2):by + 3, max(0, bx - 2):bx + 3] *= 0.6
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_padded.png'))
    a = np.zeros((128, 128, 3))
    a[:] = (170, 196, 176)
    fl = noise(128, 128, 72, 1, 0.3)
    a[fl > 0.8] = (130, 150, 136)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_lino.png'))
    # amniotic fluid: yellow-green, partly transparent
    a = np.zeros((64, 64, 4), dtype=np.uint8)
    a[..., 0], a[..., 1], a[..., 2], a[..., 3] = 200, 214, 110, 120
    Image.fromarray(a).save(os.path.join(MAPDIR, 'indev_fluid.png'))
    mottle('indev_oldwood.png', (96, 66, 40), (26, 16, 10), 73, sigma=1.4)
    # kennel straw
    im = Image.new('RGB', (128, 128), (150, 120, 60))
    d = ImageDraw.Draw(im)
    for _ in range(500):
        x, y = rng.integers(0, 128), rng.integers(0, 128)
        a = rng.uniform(0, math.pi)
        L = rng.integers(6, 20)
        v = int(rng.integers(160, 230))
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=(v, int(v * 0.82), int(v * 0.4)), width=1)
    im.save(os.path.join(MAPDIR, 'indev_straw.png'))
    # a shower curtain, white with blue stripes
    im = Image.new('RGB', (128, 128), (228, 232, 236))
    d = ImageDraw.Draw(im)
    for x in range(0, 128, 32):
        d.rectangle([x + 20, 0, x + 26, 127], fill=(120, 160, 210))
    a = np.asarray(im).astype(float) * (0.85 + 0.15 * np.sin(np.arange(128) / 128 * 2 * np.pi * 6) ** 2)[None, :, None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_curtain2.png'))
    # a futon cover
    im = Image.new('RGB', (128, 128), (52, 70, 120))
    d = ImageDraw.Draw(im)
    for x in range(0, 128, 32):
        for y in range(0, 128, 32):
            d.ellipse([x + 8, y + 8, x + 24, y + 24], outline=(220, 220, 230), width=2)
    wear(im, 76).save(os.path.join(MAPDIR, 'indev_futon.png'))
    # cracks and claw marks (alpha)
    for name, seed, claws in (('indev_crack.png', 77, False), ('indev_claws.png', 78, True)):
        a = np.zeros((256, 256, 4), dtype=np.uint8)
        im = Image.fromarray(a)
        d = ImageDraw.Draw(im)
        r2 = np.random.default_rng(seed)
        if claws:
            for k in range(4):
                x = 60 + k * 36
                d.line([(x, 30), (x + 18, 120), (x + 10, 226)], fill=(24, 16, 12, 230), width=5)
        else:
            def branch(x, y, ang, L, w):
                if L < 8 or w < 1:
                    return
                x2, y2 = x + L * math.cos(ang), y + L * math.sin(ang)
                d.line([(x, y), (x2, y2)], fill=(20, 18, 16, 235), width=int(w))
                branch(x2, y2, ang + r2.uniform(-0.6, 0.6), L * 0.8, w * 0.8)
                if r2.random() < 0.45:
                    branch(x2, y2, ang + r2.choice([-1, 1]) * r2.uniform(0.6, 1.2), L * 0.6, w * 0.6)
            branch(128, 250, -math.pi / 2, 40, 6)
        im.save(os.path.join(MAPDIR, name))


def backdrop():
    """The Real Characters studio set: a painted sky, a sun with a face, a rainbow, hills."""
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (120, 196, 240))
    d = ImageDraw.Draw(im)
    for k, c in enumerate([(230, 50, 50), (240, 140, 40), (240, 220, 50), (60, 180, 80), (50, 110, 220), (130, 60, 190)]):
        r_ = 420 - k * 26
        d.arc([512 - r_, 470 - r_, 512 + r_, 470 + r_], 180, 360, fill=c, width=26)
    d.ellipse([90, 40, 250, 200], fill=(255, 220, 60))
    for ex in (140, 200):
        d.ellipse([ex - 10, 94, ex + 10, 114], fill=(30, 30, 30))
    d.arc([130, 110, 210, 170], 20, 160, fill=(30, 30, 30), width=6)
    d.ellipse([-200, 380, 500, 700], fill=(90, 190, 80))
    d.ellipse([400, 400, 1200, 760], fill=(70, 170, 70))
    d.text((760, 110), "LET'S BE", font=font(64), fill=(255, 255, 255), anchor='mm')
    d.text((760, 190), "REAL!", font=font(96), fill=(255, 250, 120), anchor='mm')
    wear(im, 74).save(os.path.join(MAPDIR, 'indev_backdrop.png'))


def views():
    """Five things Freddy's windows look out on; the code swaps between them."""
    W, H = 512, 256
    rng = np.random.default_rng(4258)
    # 0: here - a concrete corridor in this facility
    im = Image.new('RGB', (W, H), (60, 60, 58))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (W, 0), (330, 100), (182, 100)], fill=(40, 40, 40))
    d.polygon([(0, H), (W, H), (330, 150), (182, 150)], fill=(84, 82, 76))
    d.rectangle([182, 100, 330, 150], fill=(30, 30, 30))
    d.rectangle([236, 106, 276, 146], fill=(70, 70, 76))
    d.ellipse([246, 40, 266, 50], fill=(255, 250, 220))
    im.save(os.path.join(MAPDIR, 'indev_view0.png'))
    # 1: a desert highway at dusk
    a = np.zeros((H, W, 3))
    t = np.linspace(0, 1, H)[:, None]
    a[..., 0] = 250 - 80 * t
    a[..., 1] = 130 + 40 * t
    a[..., 2] = 90 + 60 * t
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.ellipse([360, 120, 430, 190], fill=(255, 230, 150))
    d.rectangle([0, 160, W, H], fill=(170, 110, 70))
    d.polygon([(200, H), (312, H), (262, 160), (250, 160)], fill=(60, 56, 56))
    for k in range(5):
        d.polygon([(30 + k * 100, 160), (60 + k * 100, 110 - (k % 2) * 20), (90 + k * 100, 160)], fill=(130, 70, 50))
    im.save(os.path.join(MAPDIR, 'indev_view1.png'))
    # 2: a rainy neon city at night
    im = Image.new('RGB', (W, H), (14, 16, 30))
    d = ImageDraw.Draw(im)
    for k in range(14):
        x = k * 38 + int(rng.integers(-6, 6))
        h_ = int(rng.integers(60, 200))
        d.rectangle([x, H - h_, x + 34, H], fill=(24, 24, 40))
        for wy in range(H - h_ + 8, H - 10, 14):
            for wx in range(x + 4, x + 30, 9):
                if rng.random() < 0.4:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=tuple(int(v) for v in rng.choice([(255, 220, 120), (255, 80, 200), (80, 220, 255)])))
    a = np.asarray(im).astype(float)
    for _ in range(500):
        x, y = rng.integers(0, W), rng.integers(0, H - 12)
        a[y:y + 12, x] += 40
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(os.path.join(MAPDIR, 'indev_view2.png'))
    # 3: two suns over a violet plain
    a = np.zeros((H, W, 3))
    a[..., 0] = 120 + 60 * t
    a[..., 1] = 60 + 20 * t
    a[..., 2] = 160 - 30 * t
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.ellipse([90, 40, 170, 120], fill=(255, 240, 200))
    d.ellipse([300, 70, 340, 110], fill=(255, 160, 120))
    d.rectangle([0, 170, W, H], fill=(70, 40, 90))
    for k in range(8):
        x = int(rng.integers(0, W))
        d.polygon([(x, 172), (x + 8, 90 - k * 3), (x + 16, 172)], fill=(40, 26, 60))
    im.save(os.path.join(MAPDIR, 'indev_view3.png'))
    # 4: nothing at all, and far stars
    a = np.zeros((H, W, 3)) + 4
    for _ in range(220):
        a[rng.integers(0, H), rng.integers(0, W)] = rng.integers(120, 255)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.ellipse([360, 30, 470, 140], fill=(60, 90, 140))
    d.chord([360, 30, 470, 140], 90, 270, fill=(20, 30, 50))
    im.save(os.path.join(MAPDIR, 'indev_view4.png'))


# ===================================================================== NPC skins
def skin(base, out, shirt=None, pants=None, gain=1.0, mask=None, post=None):
    a = np.asarray(Image.open(os.path.join(NPCDIR, base)).convert('RGB')).astype(float)
    if shirt:
        NT.tint(a, NT.SHIRT_F, shirt, gain, mask)
        NT.tint(a, NT.SHIRT_B, shirt, gain, mask)
    if pants:
        NT.tint(a, NT.PANTS, pants, gain, mask)
    if post:
        a = post(a)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4)).save(os.path.join(NPCDIR, out), quality=92)


def skins():
    skin('scientist.jpg', 'indev_passenger.jpg', (122, 78, 40), (96, 62, 34), 0.95, NT.pale)       # a 1979 brown suit
    skin('scientist.jpg', 'indev_kumiho.jpg', (214, 210, 204), (34, 30, 32), 1.0, NT.pale)        # a researcher, as far as you know
    skin('janitor.jpg', 'indev_freddy.jpg', (240, 238, 232), (34, 34, 36), 1.6, NT.blue)          # white shirt and apron
    skin('janitor.jpg', 'indev_patron1.jpg', (196, 202, 214), (176, 182, 196), 1.7, NT.blue)      # a silver suit
    skin('janitor.jpg', 'indev_resident.jpg', (150, 40, 34), (60, 80, 130), 1.5, NT.blue)         # flannel and jeans
    skin('janitor.jpg', 'indev_attendant.jpg', (236, 236, 232), (230, 230, 226), 1.6, NT.blue)    # orderly whites
    skin('janitor.jpg', 'indev_patient.jpg', (170, 196, 222), (170, 196, 222), 1.5, NT.blue)      # a ward gown
    skin('janitor.jpg', 'indev_zeta.jpg', (78, 88, 60), (60, 66, 48), 1.5, NT.blue)               # off-duty fatigues
    skin('janitor.jpg', 'indev_prisoner.jpg', (128, 124, 112), (110, 106, 96), 1.5, NT.blue)      # penitentiary grey
    skin('scientist.jpg', 'indev_oldman.jpg', (92, 76, 58), (70, 64, 56), 0.9, NT.pale)           # a coat older than anyone

    def reptile(a):          # someone from somewhere else: every part of them green
        lum = a @ np.array([0.299, 0.587, 0.114])
        return np.stack([lum * 0.55, lum * 0.95, lum * 0.5], axis=-1) + 10
    skin('janitor.jpg', 'indev_patron2.jpg', (90, 120, 80), (60, 80, 60), 1.4, NT.blue, post=reptile)


# ===================================================================== documents
def docs():
    typed('doc052', [('Clearance Level', '3'), ('Item #', 'SCP-052'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-052 cannot be taken off the line it runs on. Its platform is closed to the public at the hours it '
              'appears, under a "track maintenance" notice, and held by MTF Gamma-6. {Nobody boards.} Anyone who '
              'steps off it is detained and sent to Site-21 for debriefing.'),
        ('h', 'Description:'),
        ('p', 'SCP-052 is a type R4 subway car, built in 1932 and scrapped in 1975, in perfect condition. It appears at '
              'the platform at 11:57 p.m., opens its doors for a few minutes, closes them and is gone. It is always '
              'empty except for whoever gets off.'),
        ('p', 'Those who get off say they boarded anywhere from 1976 to 2204. Most who get on are never recovered. '
              'One agent came back without his hands and with a note in his pocket.'),
        ('h', 'Note:'),
        ('p', 'The platform here is a copy of the 59th St. one, built round the point where it began to stop. '
              '{If you are on the tracks when it comes, you will not get the chance to board.} There are steps at the north end.'),
    ])
    typed('doc024', [('Clearance Level', '3'), ('Item #', 'SCP-024'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The sound stage is held behind sealed doors. Only test subjects enter; staff observe from the '
              'remote observation lab above it. If the true nature of the stage is compromised, the compound is to be demolished.'),
        ('h', 'Description:'),
        ('p', 'SCP-024 is an abandoned sound stage with a game show in it. An announcer greets whoever enters, '
              'promises fabulous prizes, warns that losers never leave, and asks whether they will play. {Those '
              'who refuse are put outside. Nobody gets a second invitation.}'),
        ('p', 'The game is an obstacle course that changes every time and gets worse as it goes. Breaking the '
              'rules brings out "studio guardians" - large masked shapes that take the offender away. Winners '
              'appear outside with a prize; losers are not seen again.'),
        ('p', 'After every game a tape of it turns up in the mailbox by the entrance, with a studio audience '
              'cheering that nobody inside ever saw.'),
    ])
    typed('doc482', [('Clearance Level', '2'), ('Item #', 'SCP-482'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-482 hangs in Containment Locker 482. Tests are logged. {Any subject still wearing it one hour '
              'after changes begin is terminated.} Remove the jacket from the body before disposal.'),
        ('h', 'Description:'),
        ('p', 'SCP-482 is a black leather straitjacket that fits anyone. While it is worn, every mental affliction '
              'the wearer has is simply gone - fear, grief, anything - for a period of one to six hours (Time Point Alpha).'),
        ('p', 'Taken off in time, it leaves the wearer as they were: everything comes back at once. Left on past '
              'that point (Time Point Beta), the body changes, shaped by whatever the mind was carrying. Those changes do not reverse.'),
        ('h', 'Note:'),
        ('p', 'Here the window is minutes, not hours. You cannot unbuckle it yourself. The attendant can.'),
    ])
    typed('doc953', [('Clearance Level', '4'), ('Item #', 'SCP-953'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-953 is kept in a Type 4 cell at the end of Hallway 99, fed liver daily by an automated cart. '
              'The approach is lined with open dog kennels: {it will not come within ten metres of a dog, least '
              'of all a barking one.} Direct contact is forbidden.'),
        ('h', 'Description:'),
        ('p', 'SCP-953 is a red fox with nine tails that can take other shapes, most often a young woman. Some fox '
              'feature always shows - ears, eyes, a tail. It can also suggest and persuade: those near it walk '
              'towards it, believing what it tells them.'),
        ('p', 'It kills by one blow to the abdomen and takes the liver.'),
        ('h', 'Addendum:'),
        ('p', 'Refer to it as "Kumiho". Staff are to follow the folkloric procedures, however odd. '
              '{The cell door has been found open. The dogs have not been quiet since.}'),
    ])
    typed('doc1269', [('Clearance Level', '2'), ('Item #', 'SCP-1269'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Property 1269 is a reconstruction of the house and yard the object was found at. One male researcher '
              'lives there as "the resident". {No women over 23 enter except for testing.}'),
        ('h', 'Description:'),
        ('p', 'SCP-1269 is a black curbside mailbox on a white post. When a woman lives alone on the property it '
              'begins to produce unaddressed love letters to her. They grow more obsessive and shorter until they '
              'are single sentences.'),
        ('p', 'Then it starts to move: when nobody is watching it is somewhere near her, facing her, half hidden - behind a '
              'window, a door, a shower curtain. In the dark it does not bother to hide.'),
        ('h', 'Note:'),
        ('p', 'A man moved in with the test occupant once. {He was found three weeks later in a garbage bag, '
              'with the replaced mailboxes.}'),
    ])
    typed('doc1440', [('Clearance Level', '4'), ('Item #', 'SCP-1440'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1440 cannot be contained without unacceptable losses. Track it, keep people away from its path, '
              'and do not try to hold it. {It will not resist you. That is the problem.}'),
        ('h', 'Description:'),
        ('p', 'SCP-1440 is an old man of no fixed origin who has not aged in fifty years. Anything human that stays '
              'near him - buildings, machines, people - begins to fail, slowly and then all at once, until it is '
              'destroyed. Only his own things are spared: a sack, a worn pack of cards, a small glass cup.'),
        ('p', 'He knows this, keeps away from people when he can, and asked us to destroy him. Every site that '
              'has held him has been lost.'),
        ('h', 'Note:'),
        ('p', 'Interview Room 142 is where he has stopped this time. Do not stay long.'),
    ])
    typed('doc2701', [('Clearance Level', '2'), ('Item #', 'SCP-2701'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Cell Block 15 is kept as found. A guard is posted with restraints. {Nobody is to write a name on '
              'the INTAKE form beside Cell 667.}'),
        ('h', 'Description:'),
        ('p', 'SCP-2701 is Cell 667 of a closed state penitentiary. If one person is locked inside it and a name '
              'and release date are written on the INTAKE form, thirteen seconds later they are gone. At midnight '
              'on the release date the door shuts by itself and they are back.'),
        ('p', 'In between there is nothing: no sight, sound, touch or sleep, and time runs three to four hundred times '
              'slower. A quarter of an hour feels like weeks. Long stays end in breakdown.'),
        ('h', 'Note:'),
        ('p', 'The warden put 137 men in there by himself. He said he had help. {Somebody still fills the form in.}'),
    ])
    typed('doc3325', [('Clearance Level', '3'), ('Item #', 'SCP-3325'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The Real Characters Industries facility is held as found. Captured SCP-3325-1 are fed raw meat '
              'twice a day and {tranquillised before anyone goes near them.}'),
        ('h', 'Description:'),
        ('p', 'SCP-3325-1 are living things grown to look like puppets and costume characters for children\'s '
              'television. They are carnivorous, aggressive, feel no pain and keep coming when hurt, but die like '
              'anything else. They repeat lines they were made to say.'),
        ('p', 'Below the recording studio are laboratories with specimens still growing in glass tubes, and pens '
              'of half-eaten livestock. Some instances are still in the vents.'),
        ('h', 'Note:'),
        ('p', 'One got out of its tube on LG-1. It will stop for meat. The glass chamber still locks.'),
    ])
    typed('doc4258', [('Clearance Level', '2'), ('Item #', 'SCP-4258'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'The diner is screened off. Staff leaving it use the decontamination shower by the door. Anything '
              'from another reality that walks out is to be stopped.'),
        ('h', 'Description:'),
        ('p', 'SCP-4258 is "Freddy\'s Diner", a 1950s diner that appeared one night with everyone nearby '
              'remembering it had always been there. Its one worker, Freddy, is an old man. Its customers come '
              'from other realities, some of them human. Everyone inside understands everyone else.'),
        ('p', 'The windows show wherever the last person to come in or go out came from. {Any battery-powered '
              'device brought inside goes flat, "to secure the privacy of our patrons".}'),
        ('h', 'Note:'),
        ('p', 'Freddy is kind. The coffee is good. The diner is the safest room in this zone. Do not get used to it.'),
    ])
    typed('doc6096', [('Clearance Level', '3'), ('Item #', 'SCP-6096'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-6096 is "contained" by MTF Zeta-29 in Humanoid Chamber 6096, and leaves whenever it wants. '
              'Its target is to be sedated ahead of it.'),
        ('h', 'Description:'),
        ('p', 'SCP-6096 is a small figure under a large cotton sheet. {Nobody can act to harm it, or try to, or make anything '
              'that would.} It is docile most of the time. Sometimes it gets up and walks, at walking pace, to a '
              'person chosen at random. Whoever sees it then knows who that person is and where, and must help it '
              'get there.'),
        ('p', 'When it reaches them it draws them under the sheet. They struggle for twenty to forty minutes and are gone.'),
        ('h', 'Note:'),
        ('p', 'The target alone can act against it. {So far no target has managed it.}'),
    ])


NOTES = {
    'doc052b': ({0: 'Statement, passenger 052-27', 1: 'Got on at 59th, Sat 9 June 1979,', 2: 'after the late show. Two stops.',
                 3: 'Doors opened on this platform', 4: 'and a man with a rifle said', 5: 'what year do you think it is.',
                 7: 'It was the same night. It was', 8: 'the same night when I got on.', 10: 'Can somebody call my mother.'}, '- 052-27'),
    'doc052c': ({1: 'SEND NO MORE.', 4: '(found in a pocket after a', 5: ' ride on SCP-052. The handwriting', 6: ' is the passenger\'s own.)'}, None),
    'doc024b': ({0: 'VHS - found in the stage mailbox', 1: 'Label: GAME 4,117 - ONE PLAYER', 2: 'Picture is good. Every camera',
                 3: 'angle there is. A full house in', 4: 'the bleachers, cheering.', 6: 'The bleachers were empty. I was',
                 7: 'there. I checked them myself.', 9: 'Put it in the box with the', 10: 'other 4,116.'}, '- Obs. lab'),
    'doc482b': ({0: 'Locker 482 - attendant card', 1: 'Wearer calm in under a minute.', 2: 'Alpha lasts 1.5 to 2.5 min here.',
                 3: 'Get them back to me before that.', 5: 'If it goes past: you have about', 6: 'a minute before the changes are',
                 7: 'too far. Protocol is protocol.', 9: 'They always say they feel fine.', 10: 'They do. That is the problem.'}, '- Orderly 3'),
    'doc953b': ({0: 'Hallway 99 - kennel rules', 1: 'Never let the dogs go quiet.', 2: 'KENNEL ALERT sets them off.',
                 3: 'Stand among the kennels if she', 4: 'calls you. She will call you.', 5: 'She will sound like somebody you',
                 6: 'want to help. Look for the', 7: 'ears, the eyes, a tail.', 9: 'Call her Kumiho. Never the', 10: 'other word.'}, '- Handler Seo'),
    'doc1269b': ({0: 'My dearest,', 1: 'I watch you water the plants on', 2: 'the sill every morning and I think',
                  3: 'there is nobody in the world as', 4: 'careful as you. I would be', 5: 'careful with you too. I would wait',
                  6: 'by the road for you forever.', 8: 'I am already by the road.', 9: 'I am always by the road.'}, None),
    'doc1269c': ({1: 'WHO IS HE', 3: 'WHO IS HE', 5: 'I SAW HIM IN THE HALL', 7: 'MAKE HIM LEAVE', 9: 'MINE MINE MINE'}, None),
    'doc1440b': ({0: 'To whoever has this room next -', 2: 'I am sorry about the lights, and', 3: 'the pipes, and the ceiling. It',
                  4: 'is always the same. I stay as', 5: 'short a time as I am let.', 7: 'I left the cards. They are the only',
                  8: 'things that never break near me.', 10: 'If you find a way, use it.'}, None),
    'doc2701b': ({0: 'Decard (transcript, part)', 1: '"You know how you break an', 2: 'animal? You take away its hope.', 3: 'Block every exit. Let the dread',
                  4: 'seep in."', 6: '"I didn\'t make it, son. I had', 7: 'help. Hate and grief are a', 8: 'currency to some."',
                  10: 'He filled in 137 forms.'}, '- Agent, 1970'),
    'doc3325b': ({0: 'REAL CHARACTERS! (brochure)', 1: 'Children are bored of puppets.', 2: 'They know it is all fake.',
                  3: 'We give them characters that are', 4: 'ALIVE - who teach them to manage', 5: 'their emotions and solve life',
                  6: 'problems, realistically.', 8: 'You can\'t get more real than', 9: 'that!'}, '- RCI'),
    'doc3325c': ({0: 'Tape found behind a prop', 1: 'Written on the case:', 2: '"we shouldn\'t have played God"', 4: 'Audio: something singing "let\'s',
                  5: 'be real today" in a voice that', 6: 'is too high, over and over,', 7: 'and under it somebody crying.'}, '- Recovery team'),
    'doc4258b': ({0: 'On a napkin:', 1: 'Best pie in eleven realities.', 2: 'Freddy says the windows show', 3: 'where the last one through came',
                  4: 'from. When you came in they', 5: 'showed a grey hall with lights.', 7: 'That is where you are from.', 8: 'I\'m sorry.'}, '- a regular'),
    'doc6096b': ({0: 'Welcome to Zeta-29.', 1: 'The booze is under the sink.', 3: 'You can\'t hurt it. You can\'t try.', 4: 'You can\'t even want to for long.',
                  6: 'If it picks somebody in the', 7: 'next room you WILL hold the door.', 9: 'If it picks you - only you can', 10: 'touch it. Get lucky.'}, '- C. Symanski'),
}

TITLES = {
    'doc052': 'Document SCP-052', 'doc052b': 'Passenger 052-27 Statement', 'doc052c': 'Send No More Note',
    'doc024': 'Document SCP-024', 'doc024b': 'Game 4,117 Tape Label',
    'doc482': 'Document SCP-482', 'doc482b': 'Locker 482 Attendant Card',
    'doc953': 'Document SCP-953', 'doc953b': 'Hallway 99 Kennel Rules',
    'doc1269': 'Document SCP-1269', 'doc1269b': 'Unaddressed Letter', 'doc1269c': 'Unaddressed Letter (Later)',
    'doc1440': 'Document SCP-1440', 'doc1440b': 'Note Left With the Cards',
    'doc2701': 'Document SCP-2701', 'doc2701b': 'Decard Interview (Part)',
    'doc3325': 'Document SCP-3325', 'doc3325b': 'Real Characters! Brochure', 'doc3325c': 'Tape Case Note',
    'doc4258': 'Document SCP-4258', 'doc4258b': "Napkin From Freddy's",
    'doc6096': 'Document SCP-6096', 'doc6096b': 'Zeta-29 Welcome Notice',
}


if __name__ == '__main__':
    labels()
    doorplates()
    plates()
    props()
    neon()
    subtile()
    simple_materials()
    backdrop()
    views()
    skins()
    docs()
    for name, (rows, sign) in NOTES.items():
        note(name, rows, sign=sign)
    assert set(TITLES) == {'doc' + n for n, _ in SCPS} | set(NOTES), set(TITLES) ^ ({'doc' + n for n, _ in SCPS} | set(NOTES))
    print('batch 7 assets, %d documents' % len(TITLES))
