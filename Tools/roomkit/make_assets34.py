r"""Textures of the thirty-fourth batch (original, drawn here), after the user's reference images 100-106:
  indev_b34plac.png      a placard for every SCP (8 x 16 cells of 256 x 128): number, class band, title
  indev_b34scr.png       the record screens and photographs (4 x 8 cells of 512 x 256)
  indev_b34win.png       cell observation windows: three silhouettes behind frosted glass, papered over, a hive
  indev_b34door1619.png  SCP-1619: a graphite drawing of a door
  indev_b34signs.png     STORAGE AREA 06/07/08/09 and SURVEILLANCE ROOM / CAUTION (ref. 104, 106)
  indev_b34lock.png      the HEAVY CONTAINMENT ZONE LOCKDOWN switch panel (ref. 105)
  indev_b34console.png   the grey control console with its buttons and scope (ref. 102)
  indev_b34sulfur.png    the ring of sulfur on SCP-1913's floor
   python make_assets34.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F, FR, FM
from data34 import U

RND = random.Random(34)
CLASSCOL = {'Safe': (40, 150, 60), 'Euclid': (210, 160, 30), 'Keter': (190, 30, 30), 'Thaumiel': (20, 20, 20),
            'Apollyon': (90, 0, 0), 'Neutralized': (110, 110, 110), 'Explained': (60, 110, 200), 'Uncontained': (150, 40, 150),
            'N/A': (120, 90, 60)}
SCREENS = [u for u in U if u['unit'] == 'screen' and u['num'] != '1619']


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def noise(w, h, base, amp, seed, blur=0.8):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def placards():
    sheet = Image.new('RGB', (2048, 2048), (20, 20, 22))
    for i, u in enumerate(U):
        im = Image.new('RGB', (256, 128), (26, 27, 30))
        d = ImageDraw.Draw(im)
        d.rectangle([3, 3, 252, 124], outline=(170, 170, 170), width=2)
        col = CLASSCOL.get(u['cls'], (100, 100, 100))
        d.rectangle([3, 92, 252, 124], fill=col)
        num = 'SCP-' + u['num'] if u['num'] != 'L726' else 'SCP-L726'
        d.text((128, 30), num if u['num'] != 'L726' else 'SCP-L[   ]', font=F(30), fill=(240, 240, 240), anchor='mm')
        title = u['title'] if len(u['title']) < 24 else u['title'][:23] + '.'
        d.text((128, 66), title, font=F(17, FR), fill=(200, 200, 200), anchor='mm')
        d.text((128, 108), u['cls'].upper(), font=F(20), fill=(255, 255, 255) if u['cls'] != 'Safe' else (230, 255, 230), anchor='mm')
        sheet.paste(im, ((i % 8) * 256, (i // 8) * 128))
    save(sheet, 'indev_b34plac.png')


def screens():
    sheet = Image.new('RGB', (2048, 2048), (8, 8, 10))
    for i, u in enumerate(SCREENS):
        photo = u['num'] in ('1704', '1676', '3047', '1897-1', '2746', '7572', '6167')
        if photo:                                            # a pinned black-and-white photograph and its caption
            im = Image.new('RGB', (512, 256), (200, 196, 186))
            ph = noise(300, 200, (120, 120, 120), 22, 3400 + i, 1.2)
            pd = ImageDraw.Draw(ph)
            r = random.Random(i)
            if u['num'] == '3047':
                pd.rectangle([20, 70, 280, 160], fill=(60, 60, 60)); pd.rectangle([40, 50, 120, 70], fill=(70, 70, 70))
                for x in (60, 120, 200, 250):
                    pd.ellipse([x - 18, 150, x + 18, 186], fill=(30, 30, 30))
            elif u['num'] == '1676':
                pd.rectangle([40, 90, 260, 150], fill=(220, 220, 220)); pd.rectangle([80, 60, 220, 95], fill=(200, 200, 200))
                for x in (80, 220):
                    pd.ellipse([x - 22, 135, x + 22, 179], fill=(25, 25, 25))
            elif u['num'] == '1704':
                for k in range(140):
                    x, y = r.randint(20, 280), r.randint(40, 180)
                    pd.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(215, 210, 196)); pd.line([(x, y), (x + r.randint(-10, 10), y + 12)], fill=(200, 196, 180), width=3)
            elif u['num'] == '1897-1':
                pd.rectangle([0, 140, 300, 200], fill=(150, 140, 120))
                pd.rectangle([180, 20, 206, 150], fill=(30, 30, 30)); pd.ellipse([176, 4, 210, 34], fill=(30, 30, 30))
                pd.rectangle([60, 120, 66, 150], fill=(30, 30, 30))
            elif u['num'] == '7572':
                pd.rectangle([110, 10, 190, 190], fill=(90, 90, 90))
                for y in range(20, 190, 22):
                    pd.line([(110, y), (190, y)], fill=(70, 70, 70), width=2)
            elif u['num'] == '6167':
                pd.rectangle([0, 0, 300, 200], fill=(20, 20, 20)); pd.ellipse([90, 60, 210, 140], outline=(120, 120, 120), width=6)
                for y in range(60, 200, 18):
                    pd.line([(140, y), (160, y)], fill=(130, 110, 80), width=3)
            else:
                pd.polygon([(0, 200), (150, 60), (300, 200)], fill=(40, 40, 40)); pd.rectangle([120, 120, 180, 200], fill=(10, 10, 10))
            im.paste(ph, (16, 28))
            d = ImageDraw.Draw(im)
            d.ellipse([160, 18, 172, 30], fill=(200, 30, 30))
            d.text((330, 40), 'SCP-' + u['num'], font=F(30), fill=(30, 30, 30))
            words = u['title'].split()
            d.text((330, 84), ' '.join(words[:3]), font=F(18, FR), fill=(40, 40, 40))
            d.text((330, 108), ' '.join(words[3:]), font=F(18, FR), fill=(40, 40, 40))
            d.text((330, 200), u['cls'].upper(), font=F(22), fill=CLASSCOL.get(u['cls'], (0, 0, 0)))
        else:                                                # a terminal screen
            fg = {'579': (255, 80, 80), '785-2': (255, 220, 120), '5275': (120, 220, 255)}.get(u['num'], (140, 240, 150))
            im = Image.new('RGB', (512, 256), (8, 14, 10) if fg[1] > 200 else (16, 8, 8))
            d = ImageDraw.Draw(im)
            d.rectangle([3, 3, 508, 252], outline=tuple(c // 2 for c in fg), width=3)
            d.text((16, 12), 'SCP-%s  %s' % (u['num'], u['cls'].upper()), font=F(22), fill=fg)
            body = u['text']
            if u['num'] == '579':
                body = 'ACTION 10-ISRAFIL-A ... ACTION 10-ISRAFIL-B ... [DATA EXPUNGED] [DATA EXPUNGED] [DATA EXPUNGED]'
            if u['num'] == '785-2':
                body = 'MENU - UNCLE ####\'S #### ##### - DO NOT SAY THIS NAME IN A CROWD. Soup of the day. Pie. Coffee 25c.'
            line, y = '', 52
            for w in body.split():
                if len(line) + len(w) > 40:
                    d.text((16, y), line, font=F(17, FM), fill=fg); y += 24; line = ''
                line += w + ' '
            d.text((16, y), line, font=F(17, FM), fill=fg)
            for yy in range(0, 256, 3):
                d.line([(0, yy), (512, yy)], fill=(0, 0, 0))
        sheet.paste(im, ((i % 4) * 512, (i // 4) * 256))
    save(sheet, 'indev_b34scr.png')


def windows():
    """cell windows: frosted glass with a dark shape behind it (3 poses), papered over, a hive of comb"""
    sheet = Image.new('RGB', (1280, 256))
    for k in range(5):
        im = noise(256, 256, (150, 160, 166), 8, 3410 + k, 2.0)
        d = ImageDraw.Draw(im)
        if k < 3:
            cx = (90, 128, 170)[k]
            d.ellipse([cx - 20, 50, cx + 20, 96], fill=(40, 44, 48))
            d.polygon([(cx - 34, 100), (cx + 34, 100), (cx + 30 + k * 4, 256), (cx - 30, 256)], fill=(40, 44, 48))
            if k == 1:
                d.line([(cx + 34, 110), (cx + 60, 190)], fill=(40, 44, 48), width=14)
            im = im.filter(ImageFilter.GaussianBlur(5))
        elif k == 3:
            im = noise(256, 256, (226, 220, 200), 6, 3420, 1.0)
            d = ImageDraw.Draw(im)
            for y in range(0, 256, 64):
                d.line([(0, y), (256, y)], fill=(190, 180, 160), width=2)
            d.text((128, 100), 'DO NOT', font=F(36), fill=(170, 20, 20), anchor='mm')
            d.text((128, 150), 'LOOK', font=F(36), fill=(170, 20, 20), anchor='mm')
        else:
            im = Image.new('RGB', (256, 256), (120, 84, 20))
            d = ImageDraw.Draw(im)
            for j in range(9):
                for i in range(8):
                    x, y = i * 34 + (j % 2) * 17, j * 30
                    d.regular_polygon((x, y, 16), 6, fill=(220, 160, 40), outline=(120, 80, 10))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 255, 255], outline=(30, 30, 30), width=8)
        sheet.paste(im, (k * 256, 0))
    save(sheet, 'indev_b34win.png')


def door1619():
    im = noise(256, 512, (236, 234, 228), 4, 3430, 0.6)
    d = ImageDraw.Draw(im)
    g = (70, 70, 74)
    for k in range(3):                                       # a sketchy, hand-drawn door
        o = RND.uniform(-3, 3)
        d.line([(40 + o, 500), (44 + o, 40), (212 + o, 38), (216 + o, 500)], fill=g, width=3)
    d.rectangle([60, 70, 196, 230], outline=g, width=2)
    d.rectangle([60, 270, 196, 470], outline=g, width=2)
    d.ellipse([176, 270, 194, 288], outline=g, width=3)
    for y in range(80, 220, 9):
        d.line([(64, y), (192, y + 6)], fill=(170, 170, 172), width=1)
    save(im.filter(ImageFilter.GaussianBlur(0.5)), 'indev_b34door1619.png')


def signs():
    sheet = Image.new('RGB', (1024, 512), (0, 0, 0))
    for k, n in enumerate(('06', '07', '08', '09')):         # ref. 106: STORAGE AREA 06
        im = Image.new('RGB', (512, 128), (24, 24, 24))
        d = ImageDraw.Draw(im)
        d.rectangle([4, 4, 507, 123], outline=(200, 200, 200), width=3)
        d.text((256, 46), 'STORAGE AREA', font=F(44), fill=(235, 235, 235), anchor='mm')
        d.text((256, 96), n, font=F(36), fill=(235, 235, 235), anchor='mm')
        sheet.paste(im, ((k % 2) * 512, (k // 2) * 128))
    im = Image.new('RGB', (512, 256), (24, 24, 24))           # ref. 104: Surveillance Room / CAUTION
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 511, 70], fill=(30, 30, 34))
    d.text((256, 36), 'Surveillance Room', font=F(38), fill=(235, 235, 235), anchor='mm')
    d.rectangle([60, 80, 452, 250], fill=(240, 210, 20))
    d.rectangle([70, 88, 442, 140], fill=(20, 20, 20))
    d.text((256, 114), 'CAUTION', font=F(44), fill=(240, 210, 20), anchor='mm')
    d.text((256, 172), 'ADMITTANCE TO AUTHORIZED', font=F(24), fill=(20, 20, 20), anchor='mm')
    d.text((256, 208), 'PERSONNEL ONLY', font=F(24), fill=(20, 20, 20), anchor='mm')
    sheet.paste(im, (0, 256))
    im = Image.new('RGB', (512, 256), (24, 24, 24))
    d = ImageDraw.Draw(im)
    d.text((256, 80), 'SERVER ROOM', font=F(46), fill=(235, 235, 235), anchor='mm')
    d.text((256, 160), 'NO FOOD OR DRINK', font=F(28), fill=(240, 200, 60), anchor='mm')
    sheet.paste(im, (512, 256))
    save(sheet, 'indev_b34signs.png')


def lockpanel():
    """ref. 105: a grey steel panel - HEAVY CONTAINMENT ZONE LOCKDOWN, a big lever switch OFF/ON, a second breaker"""
    im = noise(512, 512, (118, 120, 122), 8, 3440, 0.8)
    d = ImageDraw.Draw(im)
    for (x, y, t) in ((60, 30, 'REMOTE DOOR CONTROL'), (280, 30, 'HEAVY CONTAINMENT ZONE LOCKDOWN')):
        d.rectangle([x, y, x + 200, y + 50], fill=(20, 20, 20))
        d.text((x + 100, y + 25), t, font=F(13), fill=(230, 230, 230), anchor='mm')
    for (x, lab) in ((100, 'OFF'), (330, 'OFF')):
        d.rectangle([x - 10, 110, x + 70, 150], fill=(20, 20, 20))
        d.text((x + 30, 130), lab, font=F(20), fill=(230, 230, 230), anchor='mm')
        d.rectangle([x - 20, 170, x + 80, 330], fill=(70, 72, 74), outline=(30, 30, 30), width=4)
        d.rectangle([x + 20, 180, x + 40, 260], fill=(30, 30, 30))
        d.rectangle([x - 10, 350, x + 70, 390], fill=(20, 20, 20))
        d.text((x + 30, 370), 'ON', font=F(20), fill=(230, 230, 230), anchor='mm')
    for x in range(40, 480, 40):
        d.rectangle([x, 430, x + 24, 470], fill=(40, 40, 42), outline=(20, 20, 20))
    save(im, 'indev_b34lock.png')


def console():
    """ref. 102: a grey control desk: two label plates, switches, a green scope screen"""
    im = noise(512, 256, (150, 152, 150), 6, 3450, 0.6)
    d = ImageDraw.Draw(im)
    for x in (40, 130):
        d.rectangle([x, 20, x + 70, 44], fill=(20, 20, 20))
        d.text((x + 35, 32), 'BYPASS', font=F(11), fill=(220, 220, 220), anchor='mm')
        for y in (70, 120, 170):
            d.rectangle([x + 20, y, x + 50, y + 30], fill=(40, 40, 40))
            d.ellipse([x + 28, y + 6, x + 42, y + 20], fill=(200, 30, 30) if y == 70 else (40, 180, 60))
    d.rectangle([250, 30, 480, 180], fill=(20, 24, 20), outline=(60, 60, 60), width=6)
    d.line([(365, 50), (365, 160)], fill=(60, 200, 80), width=2)
    d.line([(270, 105), (460, 105)], fill=(60, 200, 80), width=2)
    d.ellipse([355, 95, 375, 115], outline=(120, 255, 140), width=2)
    for x in range(250, 480, 30):
        d.rectangle([x, 200, x + 20, 230], fill=(50, 50, 52))
    save(im, 'indev_b34console.png')


def sulfur():
    im = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([10, 10, 246, 246], outline=(230, 210, 40, 255), width=18)
    bg = noise(256, 256, (90, 90, 90), 6, 3460, 1.0).convert('RGBA')
    save(Image.alpha_composite(bg, im).convert('RGB'), 'indev_b34sulfur.png')


if __name__ == '__main__':
    placards()
    screens()
    windows()
    door1619()
    signs()
    lockpanel()
    console()
    sulfur()
    print('batch 34 textures: %d placards, %d screens' % (len(U), len(SCREENS)))
