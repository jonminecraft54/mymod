r"""Textures and the one sound of the thirtieth batch, Site-42 (original, drawn here):
  name plates (Site Director Dr. T. Sherman, Media Relations & Support, the Ethics Subcommittee, the Multi-U Dept.,
  Researcher M. Wickerford), wing signs (A4 / G14, B4 / Room 35), our own Site-42 plaque, public-relations posters of
  the post-reveal era, the SCP-3069 Atlantic map, thermal monitor screens, the Hume meter, Scranton field netting,
  the SCP-4434-A recreation (Figure A: non-anomalous, address redacted), the outpost camera feeds, corrugated
  container steel, the Lambda-14 soil and water board, the SCP-4427 contact counter, a whiteboard, traffic-cone paint.
  SFX\Indev\phonering.wav: a dual-tone telephone ring.
   python make_assets30.py"""
import math
import os
import random
import struct
import wave
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from make_assets5 import MAPDIR

ROOT = r'I:\MythicalC v1.2.7\v0.1\scpcb-dx9\scpcb-dx9'
FB = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
FM = r"C:\Windows\Fonts\courbd.ttf"
RND = random.Random(42)


def F(n, f=FB):
    return ImageFont.truetype(f, n)


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def plate(text, sub, w=512, h=128):
    im = Image.new('RGB', (w, h), (24, 24, 26))
    d = ImageDraw.Draw(im)
    d.rectangle([4, 4, w - 5, h - 5], outline=(190, 190, 190), width=3)
    d.text((w / 2, h * 0.4), text, font=F(int(h * 0.3)), fill=(235, 235, 235), anchor='mm')
    d.text((w / 2, h * 0.75), sub, font=F(int(h * 0.17), FR), fill=(190, 190, 190), anchor='mm')
    return im


def emblem(d, cx, cy, r, col):
    """our own Site-42 emblem: a ring, three inward arrows, '42' in the middle"""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=max(3, r // 9))
    for k in range(3):
        a = math.radians(90 + k * 120)
        x0, y0 = cx + math.cos(a) * r * 0.95, cy - math.sin(a) * r * 0.95
        x1, y1 = cx + math.cos(a) * r * 0.55, cy - math.sin(a) * r * 0.55
        d.line([(x0, y0), (x1, y1)], fill=col, width=max(3, r // 10))
        b1, b2 = a + 2.6, a - 2.6
        d.polygon([(x1, y1), (x1 + math.cos(b1) * r * 0.16, y1 - math.sin(b1) * r * 0.16),
                   (x1 + math.cos(b2) * r * 0.16, y1 - math.sin(b2) * r * 0.16)], fill=col)
    d.text((cx, cy), '42', font=F(int(r * 0.55)), fill=col, anchor='mm')


def plates():
    rows = [('DR. T. SHERMAN', 'SITE DIRECTOR'), ('MEDIA RELATIONS', '& SUPPORT'),
            ('ETHICS SUBCOMMITTEE', 'SENTIENT & SAPIENT ANOMALIES'), ('MULTI-U DEPT.', 'RESEARCHER M. WICKERFORD'),
            ('ROOM G14', 'SAFE-CLASS WING A4'), ('LOCKERS', 'SAFE-CLASS #2701-2799'),
            ('ROOM 35', 'EUCLID-LEVEL WING B4'), ('THERMAL WATCH', 'AC-27 RELAY'),
            ('SCP-3069', 'DEEP MONITORING'), ('GAMMA-6', 'EQUIPMENT'),
            ('OUTPOSTS 4433-A / 4434', 'REMOTE SURVEILLANCE'), ('EVIDENCE', 'SCP-4434'),
            ('SCP-2648', 'CONTAINER 1'), ('STORAGE', 'SITE-42 GENERAL')]
    sheet = Image.new('RGB', (1024, 896))
    for i, (a, b) in enumerate(rows):
        sheet.paste(plate(a, b), ((i % 2) * 512, (i // 2) * 128))
    save(sheet, 'indev_plates30.png')
    return rows


def plaque():
    im = Image.new('RGB', (512, 512), (36, 40, 48))
    d = ImageDraw.Draw(im)
    d.rectangle([10, 10, 501, 501], outline=(200, 170, 90), width=8)
    emblem(d, 256, 200, 130, (220, 200, 140))
    d.text((256, 380), 'SITE-42', font=F(64), fill=(230, 220, 190), anchor='mm')
    d.text((256, 440), 'SAPIENT OBJECT CONTAINMENT', font=F(24), fill=(200, 190, 160), anchor='mm')
    save(im, 'indev_s42plaque.png')


def posters():
    im = Image.new('RGB', (384, 512), (30, 70, 120))
    d = ImageDraw.Draw(im)
    emblem(d, 192, 170, 110, (255, 255, 255))
    d.text((192, 330), 'SITE-42', font=F(54), fill=(255, 255, 255), anchor='mm')
    d.text((192, 390), 'YOUR NEIGHBOURS', font=F(28), fill=(255, 220, 120), anchor='mm')
    d.text((192, 424), 'IN CONTAINMENT', font=F(28), fill=(255, 220, 120), anchor='mm')
    d.text((192, 476), 'Questions? Media Relations & Support', font=F(17, FR), fill=(220, 230, 240), anchor='mm')
    save(im, 'indev_s42poster1.png')
    im = Image.new('RGB', (384, 512), (236, 232, 222))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 384, 120], fill=(150, 30, 30))
    d.text((192, 60), 'OPEN HOUSE', font=F(50), fill=(255, 255, 255), anchor='mm')
    d.text((192, 170), 'Tours of the public wing', font=F(24), fill=(40, 40, 40), anchor='mm')
    d.text((192, 205), 'every Saturday', font=F(24), fill=(40, 40, 40), anchor='mm')
    for k, t in enumerate(('No photography past the', 'yellow line. Sapient residents', 'have a right to privacy.')):
        d.text((192, 290 + k * 34), t, font=F(22, FR), fill=(60, 60, 60), anchor='mm')
    emblem(d, 192, 440, 50, (150, 30, 30))
    save(im, 'indev_s42poster2.png')


def whiteboard():
    im = Image.new('RGB', (512, 256), (240, 242, 240))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 511, 255], outline=(150, 150, 150), width=8)
    lines = [('PUBLIC INQUIRIES TODAY: 1,204', (20, 40, 160)), ('- "is the hum normal?" (2648) x31', (40, 40, 40)),
             ('- I-40 lane closure (4427) x212', (40, 40, 40)), ('- "my mom keeps calling" -> 4433 team', (170, 30, 30)),
             ('PRESS 3PM: Dr. Sherman', (20, 120, 40))]
    for k, (t, c) in enumerate(lines):
        d.text((24, 26 + k * 44), t, font=F(24, FM), fill=c)
    save(im, 'indev_s42board.png')


def atlantic():
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (10, 30, 60))
    d = ImageDraw.Draw(im)
    for y in range(0, H, 32):
        d.line([(0, y), (W, y)], fill=(20, 50, 90))
    for x in range(0, W, 32):
        d.line([(x, 0), (x, H)], fill=(20, 50, 90))
    d.polygon([(0, 0), (180, 0), (210, 120), (160, 260), (190, 380), (120, H), (0, H)], fill=(60, 80, 60))   # America
    d.polygon([(W, 0), (860, 0), (820, 140), (870, 300), (840, H), (W, H)], fill=(70, 80, 60))                # Europe/Africa
    pts = [(520 + 40 * math.sin(y / 60.0), y) for y in range(0, H, 8)]
    d.line(pts, fill=(200, 120, 60), width=3)                                                                 # the ridge
    d.line([(200, 180), (820, 140)], fill=(220, 220, 220), width=2)                                           # TAT-14
    for k in range(14):                                                                                        # SCP-3069
        x = 260 + k * 40
        d.rectangle([x, 230 + 18 * math.sin(k), x + 30, 246 + 18 * math.sin(k)], fill=(170, 170, 190))
    for n, (x, y) in enumerate(((505, 170), (560, 300), (460, 380))):
        d.ellipse([x - 10, y - 10, x + 10, y + 10], outline=(255, 80, 60), width=4)
        d.text((x + 16, y - 12), 'AP %s' % ('I', 'II', 'III')[n], font=F(22), fill=(255, 120, 100))
    d.text((20, 20), 'SCP-3069 - KNOWN EXTENT (APPROX.)', font=F(26), fill=(230, 230, 240))
    d.text((20, 470), 'AP I 3500 m   AP II 3200 m (blocked)   AP III 4000 m (SCP-3069-A)', font=F(20, FR), fill=(200, 210, 230))
    save(im, 'indev_s42atlantic.png')


def screens():
    im = Image.new('RGB', (512, 256), (8, 8, 12))
    d = ImageDraw.Draw(im)
    for k in range(3):
        x0 = 10 + k * 168
        for y in range(10, 200, 2):
            for x in range(x0, x0 + 156, 4):
                h = 0.3 + 0.2 * math.sin(x / 20.0 + k) * math.cos(y / 17.0)
                if k == 1:
                    h += 0.7 * math.exp(-(((x - x0 - 78) ** 2 + (y - 100) ** 2) / 600.0))
                h = max(0, min(1, h))
                d.rectangle([x, y, x + 3, y + 1], fill=(int(255 * h), int(140 * h * h), int(120 * (1 - h))))
        d.text((x0 + 4, 212), ('LOBBY', 'B4 CORRIDOR', 'I-40 CAM 7')[k], font=F(18), fill=(220, 220, 220))
    d.text((180, 232), '37.8 C  SPHERE 60 cm', font=F(16), fill=(255, 200, 80))
    save(im, 'indev_s42thermal.png')
    im = Image.new('RGB', (256, 256), (16, 20, 16))
    d = ImageDraw.Draw(im)
    d.text((128, 40), 'HUME', font=F(30), fill=(120, 240, 140), anchor='mm')
    d.text((128, 120), '112 Hm', font=F(54), fill=(120, 240, 140), anchor='mm')
    d.text((128, 190), 'MIN 100  OK', font=F(24), fill=(120, 240, 140), anchor='mm')
    d.rectangle([20, 220, 236, 236], outline=(120, 240, 140), width=2)
    d.rectangle([20, 220, 200, 236], fill=(80, 200, 100))
    save(im, 'indev_s42hume.png')
    net = Image.new('RGB', (256, 256), (205, 208, 210))
    d = ImageDraw.Draw(net)
    for k in range(-256, 512, 24):
        d.line([(k, 0), (k + 256, 256)], fill=(120, 140, 150), width=2)
        d.line([(k, 256), (k + 256, 0)], fill=(120, 140, 150), width=2)
    d.rectangle([0, 0, 255, 255], outline=(150, 150, 155), width=6)
    d.text((128, 240), 'Mk. XIII SCRANTON NETTING', font=F(14), fill=(80, 90, 100), anchor='mm')
    save(net, 'indev_s42netting.png')


def feeds():
    """the outposts' camera feeds: the fire-damaged house (4433-A) and the valley with the hole (4434-D)"""
    W, H = 512, 256
    im = Image.new('RGB', (W, H), (12, 12, 12))
    d = ImageDraw.Draw(im)
    # feed 1: a burnt two-storey house behind a chain-link fence
    d.rectangle([4, 4, 252, 210], fill=(40, 44, 40))
    d.polygon([(60, 120), (60, 70), (128, 30), (196, 70), (196, 120)], fill=(46, 40, 36))
    d.rectangle([60, 120, 196, 200], fill=(56, 50, 44))
    for x, y in ((80, 140), (150, 140), (90, 85), (150, 85)):
        d.rectangle([x, y, x + 24, y + 24], fill=(10, 10, 10))
    for x in range(4, 252, 10):
        d.line([(x, 150), (x + 10, 210)], fill=(90, 90, 90))
        d.line([(x + 10, 150), (x, 210)], fill=(90, 90, 90))
    d.text((10, 220), 'OUTPOST 4433-A  CAM 2', font=F(16), fill=(220, 220, 220))
    # feed 2: the valley, trees, the hole
    d.rectangle([260, 4, 508, 210], fill=(36, 46, 36))
    d.polygon([(260, 60), (384, 170), (508, 60), (508, 210), (260, 210)], fill=(48, 60, 40))
    d.ellipse([360, 160, 408, 180], fill=(0, 0, 0))
    for x in range(266, 506, 18):
        d.polygon([(x, 70 + (x % 40)), (x + 8, 30 + (x % 40)), (x + 16, 70 + (x % 40))], fill=(24, 40, 24))
    d.text((266, 220), 'OUTPOST-4434  CAM 5  (AOE)', font=F(16), fill=(220, 220, 220))
    im = im.filter(ImageFilter.GaussianBlur(0.7))
    d = ImageDraw.Draw(im)
    for y in range(0, H, 3):
        d.line([(0, y), (W, y)], fill=(0, 0, 0))
    save(im, 'indev_s42feeds.png')
    ad = Image.new('RGB', (384, 512), (250, 248, 240))
    d = ImageDraw.Draw(ad)
    d.text((192, 60), 'FIGURE A', font=F(22), fill=(150, 30, 30), anchor='mm')
    d.text((192, 90), 'non-anomalous recreation', font=F(18, FR), fill=(150, 30, 30), anchor='mm')
    d.rectangle([30, 120, 354, 300], fill=(60, 90, 60))
    d.polygon([(30, 300), (192, 190), (354, 300)], fill=(40, 70, 40))
    d.text((192, 340), 'YOU ALREADY KNOW', font=F(30), fill=(30, 30, 30), anchor='mm')
    d.text((192, 380), 'WHERE TO FIND IT.', font=F(30), fill=(30, 30, 30), anchor='mm')
    d.rectangle([60, 420, 324, 460], fill=(0, 0, 0))
    d.text((192, 490), '[ADDRESS REDACTED]', font=F(18), fill=(80, 80, 80), anchor='mm')
    save(ad, 'indev_s42ad4434.png')


def misc():
    c = Image.new('RGB', (256, 256), (120, 70, 40))
    d = ImageDraw.Draw(c)
    for x in range(0, 256, 32):
        d.rectangle([x, 0, x + 14, 256], fill=(140, 84, 48))
        d.line([(x, 0), (x, 256)], fill=(90, 50, 30), width=2)
    for _ in range(200):
        x, y = RND.randrange(256), RND.randrange(256)
        d.ellipse([x, y, x + RND.randint(2, 8), y + RND.randint(2, 8)], fill=(100, 56, 30))
    save(c, 'indev_s42container.png')
    b = Image.new('RGB', (512, 256), (30, 34, 30))
    d = ImageDraw.Draw(b)
    d.text((256, 30), 'MTF LAMBDA-14 "DRUG-RUNNERS"', font=F(26), fill=(230, 230, 200), anchor='mm')
    rows = [('GROUNDWATER', 'PSILOCYBIN TRACE', 'FLAG'), ('SOIL  SE CORNER', 'HIGH', 'FLAG'), ('MASS GAIN', '+0.4 kg', 'OK'),
            ('HUM', '38 Hz', 'OK'), ('LAST FEED', 'NONE - DO NOT FEED', '')]
    for k, (a, v, f) in enumerate(rows):
        y = 70 + k * 36
        d.text((24, y), a, font=F(20, FM), fill=(200, 220, 200))
        d.text((260, y), v, font=F(20, FM), fill=(240, 220, 120))
        d.text((460, y), f, font=F(20, FM), fill=(240, 90, 80) if f == 'FLAG' else (120, 230, 120))
    save(b, 'indev_s42lambda.png')
    n = Image.new('RGB', (256, 256), (236, 236, 236))
    d = ImageDraw.Draw(n)
    d.rectangle([0, 0, 255, 255], outline=(20, 20, 20), width=10)
    d.text((128, 50), 'SCP-4427', font=F(30), fill=(20, 20, 20), anchor='mm')
    d.text((128, 100), 'CONTACTS', font=F(24), fill=(20, 20, 20), anchor='mm')
    d.text((128, 165), '44 / 45', font=F(54), fill=(180, 20, 20), anchor='mm')
    d.text((128, 225), 'DO NOT WALK THROUGH', font=F(18), fill=(20, 20, 20), anchor='mm')
    save(n, 'indev_s42count.png')
    cone = Image.new('RGB', (64, 128), (240, 100, 20))
    d = ImageDraw.Draw(cone)
    d.rectangle([0, 40, 64, 60], fill=(240, 240, 240))
    d.rectangle([0, 80, 64, 96], fill=(240, 240, 240))
    save(cone, 'indev_s42cone.png')


def ring():
    rate = 22050
    frames = []
    for burst in range(2):
        for i in range(int(rate * 0.4)):
            t = i / rate
            v = 0.32 * (math.sin(2 * math.pi * 440 * t) + math.sin(2 * math.pi * 480 * t))
            frames.append(int(max(-1, min(1, v)) * 30000))
        frames += [0] * int(rate * 0.2)
    frames += [0] * int(rate * 1.0)
    w = wave.open(os.path.join(ROOT, 'SFX', 'Indev', 'phonering.wav'), 'wb')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(rate)
    w.writeframes(b''.join(struct.pack('<h', f) for f in frames))
    w.close()


if __name__ == '__main__':
    plates()
    plaque()
    posters()
    whiteboard()
    atlantic()
    screens()
    feeds()
    misc()
    ring()
    print('batch 30 textures and the phone ring written')
