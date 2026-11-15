r"""Textures of the thirty-third batch (original, drawn here), after the user's reference images 90-99:
  wall styles - the white shutter corridor (ref. 94/96: white plaster, a riveted steel trim at the top, black
  skirting), the dark buttressed corridor (ref. 99: white walls with a black band and skirting), the white floor
  tiles and the drop-ceiling grid (ref. 96), stone vault blocks with charred cuneiform (SCP-4612's vault);
  name plates; screens and boards for SCP-4876, -2394, -3419, -4612 (Akiva meter), -5079 (METATRON), -7284, -7042,
  -5267, -5512, the Little Misters checklist (SCP-3537), the "explained" plaque, the SCP-4712 vault door glyphs,
  the dark red pendant shade.
   python make_assets33.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from make_assets5 import MAPDIR
from make_assets30 import F, FR, FM, plate

RND = random.Random(33)
PLATES33 = [('SCP-1007 / 3537', 'HALL 8 - LITTLE MISTERS'), ('WONDERTAINMENT', 'RECOVERED PRODUCTS'),
            ('SITE-73 ARCHIVE', 'SECURE ARCHIVE ROOM'), ('DECOMMISSIONED', 'EXPLAINED / REMAINS'),
            ('SCP-1563', 'VIVARIUM 3'), ('SCP-2394', 'VETERINARY WING'), ('SCP-3419', 'OBSERVATION'),
            ('SITE-84 ARCHIVES', 'SCP-7042 / SCP-7284'), ('SITE-91 LIAISON', 'OPEN OFFICE'),
            ('DR. I. VARGA', 'DIRECTOR, PROV. SITE-91'), ('VAULT 4612', 'SUB-LEVEL 4 - STAIRS'),
            ('RESEARCH', 'SITE-73 OPEN OFFICE'), ('DR. N. TOLENTINO', 'SENIOR RESEARCHER')]
PLATE_KEYS = ['hall8', 'toys', 'site73', 'explained', 'viv1563', 'frog', 'colony', 'arch84', 'bullpen', 'varga', 'vault',
              'office73', 'tolentino']


def save(im, name):
    im.save(os.path.join(MAPDIR, name))


def noise(w, h, base, amp, seed, blur=0.8):
    a = np.random.default_rng(seed).normal(0, amp, (h, w, 1)).astype(np.float32) + np.array(base, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))


def grime(im, n, col, seed, rmax=40, alpha=40):
    """soft stains and streaks"""
    rnd = random.Random(seed)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rnd.randrange(im.size[0]), rnd.randrange(im.size[1])
        r = rnd.randint(6, rmax)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=col + (rnd.randint(alpha // 3, alpha),))
    ov = ov.filter(ImageFilter.GaussianBlur(10))
    return Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')


def wall96():
    """ref. 96: white plaster, a riveted steel trim at the top, black skirting (one repeat = the wall height)"""
    W, H = 512, 1024
    im = grime(noise(W, H, (226, 226, 222), 7, 3301, 1.0), 40, (120, 110, 96), 3302)
    d = ImageDraw.Draw(im)
    trim = noise(W, 70, (150, 150, 144), 10, 3303)
    im.paste(trim, (0, 0))
    d.line([(0, 70), (W, 70)], fill=(70, 70, 66), width=4)
    d.line([(0, 2), (W, 2)], fill=(200, 200, 194), width=3)
    for x in range(32, W, 64):
        d.ellipse([x - 6, 30, x + 6, 42], fill=(92, 92, 88))
        d.ellipse([x - 3, 32, x + 2, 37], fill=(196, 196, 190))
    im.paste((24, 24, 24), (0, H - 56, W, H))
    d.line([(0, H - 58), (W, H - 58)], fill=(60, 60, 60), width=3)
    for x in range(0, W, 3):                                                      # dirt kicked up the skirting
        if RND.random() < 0.3:
            d.line([(x, H - 58 - RND.randint(0, 20)), (x, H - 58)], fill=(170, 164, 150))
    save(im.filter(ImageFilter.GaussianBlur(0.4)), 'indev_b33wall96.png')


def wall99():
    """ref. 99: white walls, darker and grubbier, a black band a third of the way down, a black skirting with bolts"""
    W, H = 512, 1024
    im = grime(noise(W, H, (206, 204, 200), 8, 3304, 1.0), 70, (100, 90, 80), 3305, alpha=55)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 330, W, 352], fill=(18, 18, 18))
    d.line([(0, 353), (W, 353)], fill=(150, 150, 146), width=2)
    im.paste((30, 30, 30), (0, H - 70, W, H))
    d.rectangle([0, H - 70, W, H - 64], fill=(12, 12, 12))
    for x in range(40, W, 128):
        d.ellipse([x - 5, H - 40, x + 5, H - 30], fill=(80, 80, 76))
    save(im.filter(ImageFilter.GaussianBlur(0.4)), 'indev_b33wall99.png')


def floor_tiles():
    im = Image.new('RGB', (512, 512), (40, 40, 40))
    d = ImageDraw.Draw(im)
    for i in range(4):
        for j in range(4):
            t = noise(124, 124, (232 - RND.randint(0, 12),) * 3, 4, 3310 + i * 4 + j, 1.2)
            im.paste(t, (i * 128 + 2, j * 128 + 2))
    im = grime(im, 25, (140, 130, 110), 3311, 30, 30)
    save(im, 'indev_b33tile.png')


def drop_ceiling():
    im = noise(256, 256, (214, 214, 210), 6, 3312, 0.6)
    d = ImageDraw.Draw(im)
    for _ in range(900):                                                         # the fissured mineral fibre
        x, y = RND.randrange(256), RND.randrange(256)
        d.point((x, y), fill=(178, 178, 174))
    d.rectangle([0, 0, 255, 5], fill=(70, 70, 70))
    d.rectangle([0, 0, 5, 255], fill=(70, 70, 70))
    save(im, 'indev_b33ceil.png')


def stone():
    """SCP-4612's vault: stone blocks, many charred and warped, with cuneiform glyphs"""
    W = H = 512
    im = noise(W, H, (120, 112, 100), 14, 3320, 1.2)
    d = ImageDraw.Draw(im)
    rows = 6
    for r in range(rows):
        y0 = r * H // rows
        off = (r % 2) * 64
        x = -off
        while x < W:
            w = RND.choice((128, 160, 192))
            sh = RND.randint(-20, 14)
            col = (126 + sh, 116 + sh, 102 + sh)
            d.rectangle([x + 3, y0 + 3, x + w - 3, y0 + H // rows - 3], fill=col)
            if RND.random() < 0.35:                                               # charred
                for k in range(10):
                    cx, cy = x + RND.randint(10, w - 10), y0 + RND.randint(8, H // rows - 8)
                    d.ellipse([cx - 22, cy - 10, cx + 22, cy + 10], fill=(52 + k * 3, 46 + k * 3, 40 + k * 3))
            if RND.random() < 0.55:                                               # cuneiform wedges
                gy = y0 + 18
                for gx in range(x + 14, x + w - 14, 15):
                    for k in range(RND.randint(1, 3)):
                        yy = gy + k * 16
                        if RND.random() < 0.5:
                            d.polygon([(gx, yy), (gx + 10, yy + 3), (gx, yy + 6)], fill=(70, 62, 52))
                        else:
                            d.polygon([(gx + 2, yy), (gx + 8, yy), (gx + 5, yy + 12)], fill=(70, 62, 52))
            x += w
        d.line([(0, y0), (W, y0)], fill=(54, 50, 44), width=4)
    im = noise_overlay(im, 3321)
    save(im, 'indev_b33stone.png')


def noise_overlay(im, seed):
    n = noise(im.size[0], im.size[1], (128, 128, 128), 18, seed, 0.6)
    return Image.blend(im, Image.composite(n, im, Image.new('L', im.size, 60)), 0.35)


def screen(w, h, bg, title, lines, fg=(140, 240, 150), font=FM):
    im = Image.new('RGB', (w, h), bg)
    d = ImageDraw.Draw(im)
    d.rectangle([3, 3, w - 4, h - 4], outline=tuple(int(c * 0.6) for c in fg), width=3)
    d.text((14, 12), title, font=F(int(h * 0.075)), fill=fg)
    for k, l in enumerate(lines):
        d.text((16, int(h * 0.2) + k * int(h * 0.085)), l, font=F(int(h * 0.058), font), fill=fg)
    for y in range(0, h, 3):                                                     # scanlines
        d.line([(0, y), (w, y)], fill=tuple(max(0, c - 8) for c in bg))
    return im


def buddies():
    """SCP-4876: Sam (a green head), Terry (a purple six-armed cephalopod), Bo (a brown dog), Texty's speech blocks"""
    im = Image.new('RGB', (512, 320), (40, 90, 160))
    d = ImageDraw.Draw(im)
    for y in range(0, 320, 4):
        d.line([(0, y), (512, y)], fill=(30 + y // 8, 80 + y // 10, 150))
    px = lambda x, y, s, c: d.rectangle([x, y, x + s - 1, y + s - 1], fill=c)
    for (i, j) in [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
                   (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (1, 4), (2, 4), (3, 4)]:
        px(60 + i * 16, 150 + j * 16, 16, (70, 190, 70))
    px(76, 166, 16, (255, 255, 255)); px(108, 166, 16, (255, 255, 255)); px(84, 172, 8, (0, 0, 0)); px(116, 172, 8, (0, 0, 0))
    px(84, 198, 40, (30, 90, 30))
    for (i, j) in [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]:
        px(230 + i * 16, 140 + j * 16, 16, (150, 70, 190))
    for k in range(6):
        for j in range(3):
            px(226 + k * 14, 188 + j * 14, 10, (130, 60, 170))
    px(250, 160, 10, (255, 255, 255)); px(282, 160, 10, (255, 255, 255))
    for (i, j) in [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (2, 2), (3, 2), (4, 0), (5, 0), (1, 3), (4, 3)]:
        px(380 + i * 16, 170 + j * 16, 16, (150, 100, 50))
    d.rounded_rectangle([20, 20, 250, 110], 12, fill=(255, 255, 255))
    d.text((32, 34), "Hi!! I'm Sam! I think I'm", font=F(17, FR), fill=(0, 0, 0))
    d.text((32, 58), 'a snake. Maybe a lizard?', font=F(17, FR), fill=(0, 0, 0))
    d.rounded_rectangle([290, 20, 500, 110], 12, fill=(255, 255, 230))
    d.text((300, 34), 'BARK BARK!', font=F(18), fill=(0, 0, 0))
    d.text((300, 62), '(play with me!)', font=F(17, FR), fill=(60, 60, 60))
    d.text((256, 296), "Dr. Wondertainment's PIXEL BUDDIES", font=F(18), fill=(255, 240, 120), anchor='mm')
    save(im, 'indev_b33pixel.png')


def boards():
    save(screen(512, 320, (8, 16, 10), 'SCP-2394  FW800 NEURAL FEED', [
        'STATE ......... INDUCED DREAM', 'HEART (ARTIFICIAL) ..... 41 bpm',
        'DREAM LOC ..... "warm. rain. a gum tree."', 'TELEPORT ATTEMPTS ...... 0',
        'DRIP NP2394 ............ OK', 'LAST WAKE: 3 yrs ago', '> do not let it wake up']), 'indev_b33dream.png')
    save(screen(512, 320, (10, 10, 18), 'AKIVA RADIATION - VAULT 4612', [
        'BACKGROUND ............. 0.6 ak', 'CADAVER (body) ........ 214 ak', 'CADAVER (incision) .... 391 ak',
        'TREND ........... RISING (3 yrs)', 'BLOOD ............... UNCOAGULATED', '',
        'DO NOT TOUCH THE CRYSTALS'], fg=(130, 190, 255)), 'indev_b33akiva.png')
    save(screen(512, 320, (16, 6, 6), 'I/O METATRON  -  QUARANTINE', [
        'OBJECT: SCP-5079 (self-executing ritual)', 'STATUS: TEXT SCRUBBED (4,112 posts)',
        'THIS TERMINAL DOES NOT DISPLAY IT.', '', 'If you are lonely and someone online',
        'offers you a way to "connect" -', 'talk to a person. Not the text.'], fg=(255, 130, 120)), 'indev_b33metatron.png')
    # SCP-3419's vivarium seen through the observation glass: dirt, mounds, tunnels
    v = noise(512, 256, (98, 74, 50), 18, 3330, 1.5)
    d = ImageDraw.Draw(v)
    d.rectangle([0, 0, 512, 70], fill=(60, 66, 70))
    for k in range(7):
        cx, w = 40 + k * 72 + RND.randint(-10, 10), RND.randint(40, 80)
        d.polygon([(cx - w, 200), (cx, 120 - RND.randint(0, 50)), (cx + w, 200)], fill=(118, 90, 60))
        d.ellipse([cx - 8, 170, cx + 8, 186], fill=(30, 20, 14))
    d.rectangle([0, 200, 512, 256], fill=(84, 64, 44))
    save(v.filter(ImageFilter.GaussianBlur(1.0)), 'indev_b33colony.png')
    # SCP-7284: the transfer notice
    t = Image.new('RGB', (384, 512), (236, 232, 220))
    d = ImageDraw.Draw(t)
    d.text((192, 34), 'TRANSFER NOTICE', font=F(30), fill=(20, 20, 20), anchor='mm')
    d.text((192, 70), 'SCP-7284-1 and SCP-7284-2', font=F(20), fill=(40, 40, 40), anchor='mm')
    d.rectangle([40, 96, 344, 300], fill=(90, 120, 90))
    d.ellipse([90, 150, 250, 270], fill=(214, 170, 90))                          # "Goldie"
    d.ellipse([200, 120, 290, 200], fill=(222, 178, 96))
    d.ellipse([256, 150, 268, 162], fill=(30, 20, 10))
    d.polygon([(240, 120), (226, 160), (252, 150)], fill=(190, 140, 70))
    rows = ['Released to GOI-466 (Wilson\'s', 'Wildlife Solutions) - Site-84', 'transfer revoked. They are not',
            'to be separated again.', '', 'Goldie\'s bowl and ball stay here', 'until the paperwork is done.']
    for k, r in enumerate(rows):
        d.text((24, 318 + k * 26), r, font=F(18, FR), fill=(30, 30, 30))
    save(t, 'indev_b33transfer.png')
    # SCP-7042: the sketch wall
    s = Image.new('RGB', (512, 256), (120, 96, 70))
    d = ImageDraw.Draw(s)
    animals = ['ELEPHANT (pink)', 'OCTOPUS', 'WOLVERINE?', 'RHINO (old)', 'FIVE-EYED SHRIMP', 'CROCODILE']
    for k, a in enumerate(animals):
        x, y = 20 + (k % 3) * 166, 16 + (k // 3) * 120
        d.rectangle([x, y, x + 150, y + 104], fill=(242, 238, 226))
        for _ in range(9):
            pts = [(x + RND.randint(20, 130), y + RND.randint(14, 80)) for _ in range(3)]
            d.line(pts, fill=(80, 80, 80), width=2)
        d.text((x + 75, y + 92), a, font=F(13, FR), fill=(60, 60, 60), anchor='mm')
        d.ellipse([x + 70, y - 4, x + 80, y + 6], fill=(200, 40, 40))
    save(s, 'indev_b33sketches.png')
    # SCP-5267: photographs of the ruins (black and white, as the Way's photographs always are)
    r = Image.new('RGB', (512, 256), (40, 40, 40))
    d = ImageDraw.Draw(r)
    for k in range(3):
        x = 16 + k * 166
        ph = noise(150, 150, (150, 150, 150), 20, 3340 + k, 1.0)
        pd = ImageDraw.Draw(ph)
        pd.rectangle([0, 100, 150, 150], fill=(110, 110, 110))
        for b in range(4):
            bx = RND.randint(10, 120)
            pd.rectangle([bx, 60 + RND.randint(0, 30), bx + RND.randint(14, 30), 104], fill=(70, 70, 70))
        r.paste(ph, (x, 20))
        d.text((x + 75, 196), ('THE HILL', 'THE FORT', 'STORE-HOUSES')[k], font=F(16), fill=(220, 220, 220), anchor='mm')
    d.text((256, 232), 'SCP-5267  -  MONGOLIAN-MANCHURIAN STEPPE, 1993', font=F(15, FR), fill=(200, 200, 200), anchor='mm')
    save(r, 'indev_b33ruins.png')
    # SCP-5512: a pamphlet poster of the Second Haptic Assembly (our own drawing)
    p = Image.new('RGB', (384, 512), (232, 222, 196))
    d = ImageDraw.Draw(p)
    d.text((192, 40), 'THE SECOND', font=F(34), fill=(90, 40, 30), anchor='mm')
    d.text((192, 80), 'HAPTIC ASSEMBLY', font=F(34), fill=(90, 40, 30), anchor='mm')
    cx, cy = 192, 250
    d.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=(240, 200, 90))
    for k in range(24):                                                          # many hands round the sun
        a = math.radians(k * 15)
        x0, y0 = cx + math.cos(a) * 70, cy + math.sin(a) * 70
        x1, y1 = cx + math.cos(a) * 130, cy + math.sin(a) * 130
        d.line([(x0, y0), (x1, y1)], fill=(110, 60, 40), width=5)
        d.ellipse([x1 - 9, y1 - 9, x1 + 9, y1 + 9], fill=(150, 90, 60))
    d.text((192, 420), 'Meditation - introspection - ritual', font=F(18, FR), fill=(60, 40, 30), anchor='mm')
    d.text((192, 452), 'All are welcome. Free workshops.', font=F(18, FR), fill=(60, 40, 30), anchor='mm')
    d.text((192, 490), 'SEIZED - SCP-5512 EVIDENCE', font=F(16), fill=(170, 20, 20), anchor='mm')
    save(p, 'indev_b33assembly.png')
    # SCP-3537: the Little Misters checklist that appeared on its skin
    m = Image.new('RGB', (384, 512), (250, 236, 210))
    d = ImageDraw.Draw(m)
    d.text((192, 30), 'LITTLE MISTERS', font=F(30), fill=(200, 40, 120), anchor='mm')
    d.text((192, 60), 'find them all!', font=F(18, FR), fill=(60, 60, 200), anchor='mm')
    names = ['Chameleon', 'Headless', 'Laugh', 'Forgetful', 'Shapey', 'Soap', 'Hungry', 'Brass', 'Hot', 'Sweetie',
             'Life and Death', 'Fish', 'Moon', 'Redd', 'Money', 'Lost', 'Lie', 'Mad', 'Scary', 'Stripes']
    for k, n in enumerate(names):
        x, y = 22 + (k // 10) * 180, 90 + (k % 10) * 38
        tick = n in ('Shapey', 'Life and Death')
        d.rectangle([x, y + 4, x + 18, y + 22], outline=(60, 60, 60), width=2)
        if tick:
            d.line([(x + 3, y + 12), (x + 8, y + 19), (x + 17, y + 4)], fill=(30, 150, 30), width=3)
        d.text((x + 26, y + 2), '%02d %s' % (k + 1, n), font=F(17, FR), fill=(40, 40, 40))
    d.text((192, 488), 'COPIED FROM SCP-3537 (TRANSFORMATION #1)', font=F(13), fill=(150, 30, 30), anchor='mm')
    save(m, 'indev_b33misters.png')
    # the "explained" plaque
    e = Image.new('RGB', (384, 192), (30, 34, 40))
    d = ImageDraw.Draw(e)
    d.rectangle([5, 5, 378, 186], outline=(200, 200, 200), width=4)
    d.text((192, 50), 'EXPLAINED', font=F(40), fill=(240, 240, 240), anchor='mm')
    d.text((192, 100), 'no anomalous properties', font=F(20, FR), fill=(200, 200, 200), anchor='mm')
    d.text((192, 130), 'kept for archival purposes', font=F(20, FR), fill=(200, 200, 200), anchor='mm')
    d.text((192, 164), 'SITE-73 RECORDS', font=F(16), fill=(170, 170, 170), anchor='mm')
    save(e, 'indev_b33ex.png')
    # the glyphs round SCP-4712's vault door (Romanian stencil and the old cognitohazard ring, inactive)
    g = Image.new('RGB', (512, 512), (60, 64, 66))
    d = ImageDraw.Draw(g)
    d.ellipse([20, 20, 492, 492], outline=(170, 160, 120), width=10)
    for k in range(36):
        a = math.radians(k * 10)
        x, y = 256 + math.cos(a) * 220, 256 + math.sin(a) * 220
        d.polygon([(x - 6, y - 6), (x + 6, y - 2), (x - 2, y + 8)], fill=(190, 170, 110))
    d.text((256, 256), 'SCP-4712', font=F(54), fill=(230, 220, 190), anchor='mm')
    d.text((256, 318), 'PRESSURE SEAL - DO NOT OPEN', font=F(22), fill=(230, 80, 60), anchor='mm')
    save(noise_overlay(g, 3350), 'indev_b33glyph.png')
    # SCP-4890's open page (purple, with a pop-up W)
    h = Image.new('RGB', (512, 256), (90, 40, 140))
    d = ImageDraw.Draw(h)
    d.line([(256, 0), (256, 256)], fill=(50, 20, 80), width=6)
    d.text((128, 60), "DR. WONDERTAINMENT'S", font=F(18), fill=(255, 220, 120), anchor='mm')
    d.text((128, 100), 'GUIDE TO HISTORY', font=F(26), fill=(255, 255, 255), anchor='mm')
    d.text((384, 128), 'W', font=F(120), fill=(255, 200, 60), anchor='mm')
    save(h, 'indev_b33history.png')
    # SCP-1563's vivarium sign
    save(screen(384, 192, (30, 10, 10), 'VIVARIUM 3 - SCP-1563', [
        'DO NOT ENTER WITHOUT A NECK GUARD', 'FEEDING: 10 DEER / WEEK', 'IT LOOKS LIKE A MARKER.',
        'IT IS NOT A MARKER.'], fg=(255, 150, 150), font=FR), 'indev_b33viv.png')


def shade():
    save(noise(128, 128, (110, 30, 26), 8, 3360, 0.8), 'indev_b33shade.png')


if __name__ == '__main__':
    sheet = Image.new('RGB', (1024, 896))
    for i, (a, b) in enumerate(PLATES33):
        sheet.paste(plate(a, b), ((i % 2) * 512, (i // 2) * 128))
    save(sheet, 'indev_plates33.png')
    wall96()
    wall99()
    floor_tiles()
    drop_ceiling()
    stone()
    buddies()
    boards()
    shade()
    print('batch 33 textures written to', MAPDIR)
