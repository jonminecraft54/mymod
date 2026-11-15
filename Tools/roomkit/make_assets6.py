"""Assets for the eighth batch (8 SCPs: 956, 2983, 095-FR, 3355, 4255, 1933, 6895, 1225):
   GFX\\map\\indev_labels6.png (+labels6.json)         yellow SCP labels
   GFX\\map\\indev_doorplates6.png (+doorplates6.json) black door plates (the reference corridor's)
   GFX\\map\\indev_plates6.png (+plates6.json)         name plates and signs
   GFX\\map\\indev_props6.png (+props6.json)           printed things: the cereal box, code card, wrapping, tape reels ...
   GFX\\map\\indev_neon6.png (+neon6.json)             things that glow: screens, the flux meter, the night sky hatch
   GFX\\map\\indev_*.png                               materials: lead, beryllium, mainframe beige, wrapping paper ...
   GFX\\npcs\\indev_*.jpg                              NPC skins (four Santa suits, a hazmat suit, a sweater ...)
   GFX\\items\\doc*.jpg                                17 documents (own wording, after the wiki articles)"""
import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from make_assets3 import MAPDIR, NPCDIR, F, font, wear, mottle
from make_assets5 import ft, save_map, noise, skin
from make_docs2 import typed, note, ITEMS
import make_npctex as NT

SCPS = [('956', 'EUCLID'), ('2983', 'KETER'), ('095-FR', 'KETER'), ('3355', 'SAFE'), ('4255', 'KETER'),
        ('1933', 'SAFE'), ('6895', 'KETER'), ('1225', 'SAFE')]
CLS = {'SAFE': (30, 120, 40), 'EUCLID': (200, 130, 20), 'KETER': (180, 24, 20)}


def key(num):
    return num.replace('-', '').lower()


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
        sz = 36
        while d.textlength("SCP-" + num, font=font(sz)) > 232:
            sz -= 2
        d.text((x + 12, y + 80), "SCP-" + num, font=font(sz), fill=(20, 20, 20))
        d.text((x + 12, y + 126), "OBJECT CLASS:", font=font(17), fill=(20, 20, 20))
        d.text((x + 12, y + 148), cls, font=font(30), fill=CLS[cls])
        tx, ty = x + 54, y + 218
        d.polygon([(tx, ty - 30), (tx - 34, ty + 28), (tx + 34, ty + 28)], fill=(236, 208, 34), outline=(20, 20, 20))
        d.text((tx, ty + 6), "!", font=font(34), fill=(20, 20, 20), anchor='mm')
        d.rectangle([x + 150, y + 190, x + 244, y + 246], fill=(26, 26, 28))
        d.rectangle([x, y, x + 255, y + 255], outline=(30, 30, 30), width=3)
    save_map(wear(im, 61), 'indev_labels6.png')
    json.dump(rects, open('labels6.json', 'w'), indent=1)


def doorplates():
    W = H = 1024
    im = Image.new('RGB', (W, H), (16, 16, 16))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (num, cls) in enumerate(SCPS):
        x, y = (i % 4) * 256, (i // 4) * 256
        rects[num] = (x / W, y / H, (x + 256) / W, (y + 256) / H)
        d.rectangle([x + 4, y + 4, x + 251, y + 251], fill=(26, 26, 27))
        d.rectangle([x + 14, y + 14, x + 241, y + 241], outline=(150, 150, 146), width=5)
        sz = 54
        while d.textlength("SCP-" + num, font=font(sz)) > 210:
            sz -= 2
        d.text((x + 128, y + 92), "SCP-" + num, font=font(sz), fill=(228, 226, 220), anchor='mm')
        d.line([(x + 34, y + 134), (x + 222, y + 134)], fill=(150, 150, 146), width=4)
        d.text((x + 128, y + 182), cls, font=font(40), fill=(228, 226, 220), anchor='mm')
    save_map(wear(im, 62), 'indev_doorplates6.png')
    json.dump(rects, open('doorplates6.json', 'w'), indent=1)


PLATES = [('yule', 'CONTAINMENT 4-Y (SEASONAL)'), ('lowrisk', 'LOW-RISK ITEM STORAGE'), ('unigift', 'MTF KAPPA-31 "UNIGIFTERS"'),
          ('openair', 'OPEN-AIR CONTAINMENT'), ('nocont', 'NO CLOSED CONTAINERS'), ('cell956', 'HUMANOID CELL 956'),
          ('cold', 'COLD STORE -4 C  SCP-956-1'), ('incin', 'INCINERATOR'), ('under12', 'NOBODY UNDER 12 WITHIN 200 M'),
          ('bunker', 'BUNKER 095-FR'), ('classd', 'CLASS-D PERSONNEL ONLY'), ('shield', 'SHIELDED CONTROL ROOM'),
          ('flux', 'FLUX PEAK: TAKE COVER'), ('stnick', "ST. NICK'S WORKSHOP"), ('sheridan', 'FORT SHERIDAN - PROJECT ARGOS'),
          ('argos', 'ARGOS A-7550'), ('chrono', 'DEPARTMENT OF CHRONOLOGY'), ('launch', 'LAUNCH DECK'), ('btkai', 'BTKAI UNIT'),
          ('radiation', 'RADIATION HAZARD'), ('charity', "STACY'S CHARITY FOR THE POOR"), ('giftline', 'GIFT PRODUCTION'),
          ('wonder', 'WONDERTAINMENT ITEMS'), ('tograd', 'HARDWIRED - DO NOT DISCONNECT')]
WARN = ('nocont', 'under12', 'classd', 'flux', 'radiation', 'tograd')


def plates():
    W, H = 1024, 1024
    im = Image.new('RGB', (W, H), (20, 20, 20))
    d = ImageDraw.Draw(im)
    rects = {}
    for i, (k, text) in enumerate(PLATES):
        x, y = (i % 2) * 512, (i // 2) * 73
        rects[k] = (x / W, y / H, (x + 512) / W, (y + 73) / H)
        yellow = k in WARN
        red = k in ('stnick', 'charity')
        bg = (150, 24, 22) if red else ((22, 40, 70) if k in ('chrono', 'launch', 'btkai') else (22, 22, 22))
        d.rectangle([x, y, x + 511, y + 72], fill=bg)
        d.rectangle([x + 3, y + 3, x + 508, y + 69], outline=(220, 180, 40) if (red or yellow) else (130, 130, 130), width=4)
        icon = k in ('radiation', 'bunker', 'flux')
        sz = 50
        while d.textlength(text, font=font(sz)) > (420 if icon else 470):
            sz -= 2
        d.text((x + (282 if icon else 256), y + 37), text, font=font(sz), fill=(250, 214, 40) if yellow else (240, 238, 230), anchor='mm')
        if icon:
            cx, cy = x + 30, y + 36
            d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(250, 214, 40))
            for a in (90, 210, 330):
                d.pieslice([cx - 17, cy - 17, cx + 17, cy + 17], a - 30, a + 30, fill=(20, 20, 20))
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(20, 20, 20))
    save_map(wear(im, 63), 'indev_plates6.png')
    json.dump(rects, open('plates6.json', 'w'), indent=1)


def props():
    W, H = 1024, 1024
    im = Image.new('RGB', (W, H), (230, 228, 220))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(68)
    R = {}

    def box(k, x0, y0, x1, y1):
        R[k] = (x0 / W, y0 / H, x1 / W, y1 / H)

    # SCP-2983: the cereal box front
    d.rectangle([0, 0, 255, 383], fill=(110, 60, 160))
    for k, c in enumerate([(255, 90, 90), (255, 200, 60), (90, 200, 120), (90, 160, 255), (255, 140, 220), (240, 240, 240)]):
        a = math.radians(200 + k * 28)
        cx, cy = 128 + 92 * math.cos(a), 250 + 92 * math.sin(a)
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=c, outline=(40, 20, 60), width=2)
    d.ellipse([96, 236, 160, 300], fill=(250, 214, 180))
    d.ellipse([110, 255, 120, 265], fill=(30, 30, 30))
    d.ellipse([136, 255, 146, 265], fill=(30, 30, 30))
    d.ellipse([118, 276, 140, 330], fill=(230, 80, 110))
    d.polygon([(100, 300), (60, 280), (64, 270)], fill=(250, 214, 180))
    d.polygon([(156, 300), (196, 280), (192, 270)], fill=(250, 214, 180))
    d.text((128, 30), "Dr. Wondertainment's", font=ft('arialbd.ttf', 17), fill=(255, 230, 120), anchor='mm')
    d.text((128, 66), "JUDY'S", font=ft('arialbd.ttf', 34), fill=(255, 255, 255), anchor='mm')
    d.text((128, 100), "CHOCO-WONDER", font=ft('arialbd.ttf', 28), fill=(255, 210, 60), anchor='mm')
    d.text((128, 132), "EXPLOSION", font=ft('arialbd.ttf', 26), fill=(255, 255, 255), anchor='mm')
    d.text((128, 160), "Marshmallow Bites!", font=ft('arialbd.ttf', 20), fill=(255, 210, 60), anchor='mm')
    d.text((128, 368), "Prize code inside!", font=ft('arial.ttf', 16), fill=(255, 255, 255), anchor='mm')
    box('cereal', 0, 0, 256, 384)
    # wrapping paper (red, green) and brown parcel paper with a St. Nick label
    for k, (bg, fg) in enumerate((((180, 24, 30), (240, 220, 120)), ((30, 110, 50), (240, 240, 240)))):
        x0 = 256 + k * 128
        d.rectangle([x0, 0, x0 + 127, 127], fill=bg)
        for yy in range(8, 128, 32):
            for xx in range(x0 + 8, x0 + 128, 32):
                d.polygon([(xx + 8, yy), (xx + 12, yy + 8), (xx + 8, yy + 16), (xx + 4, yy + 8)], fill=fg)
        d.rectangle([x0 + 58, 0, x0 + 70, 127], fill=(240, 200, 60))
        d.rectangle([x0, 58, x0 + 127, 70], fill=(240, 200, 60))
        box('wrap%d' % k, x0, 0, x0 + 128, 128)
    d.rectangle([512, 0, 767, 127], fill=(166, 128, 88))
    d.line([(512, 64), (767, 64)], fill=(120, 90, 60), width=3)
    d.line([(640, 0), (640, 127)], fill=(120, 90, 60), width=3)
    d.rectangle([530, 12, 630, 56], fill=(240, 236, 220))
    d.text((534, 16), "FROM: ST. NICK", font=ft('courbd.ttf', 11), fill=(20, 20, 20))
    d.text((534, 30), "100 CHRISTMAS ST", font=ft('cour.ttf', 10), fill=(20, 20, 20))
    d.text((534, 42), "NORTH POLE, NU", font=ft('cour.ttf', 10), fill=(20, 20, 20))
    box('parcel', 512, 0, 768, 128)
    # the Argos cabinet front: tape reels, lamps, switches
    d.rectangle([256, 128, 511, 511], fill=(200, 190, 166))
    for cx in (320, 448):
        d.ellipse([cx - 52, 170, cx + 52, 274], fill=(60, 60, 64), outline=(30, 30, 30), width=3)
        d.ellipse([cx - 14, 208, cx + 14, 236], fill=(200, 190, 166))
        for a in range(0, 360, 60):
            d.line([(cx, 222), (cx + 40 * math.cos(math.radians(a)), 222 + 40 * math.sin(math.radians(a)))], fill=(90, 90, 96), width=4)
    d.rectangle([272, 296, 496, 340], fill=(40, 40, 44))
    for k in range(16):
        c = [(255, 60, 40), (60, 255, 80), (255, 200, 40)][k % 3] if rng.random() < 0.6 else (60, 50, 40)
        d.ellipse([280 + k * 13, 312, 288 + k * 13, 320], fill=c)
    for k in range(8):
        d.rectangle([280 + k * 27, 360, 296 + k * 27, 400], fill=(60, 60, 60))
        d.rectangle([284 + k * 27, 364 + (k % 2) * 16, 292 + k * 27, 380 + (k % 2) * 16], fill=(220, 220, 210))
    d.text((384, 440), "ARGOS  A-7550", font=ft('arialbd.ttf', 26), fill=(40, 40, 40), anchor='mm')
    d.text((384, 474), "KERVIER INTELLIGENT SYSTEMS", font=ft('arial.ttf', 13), fill=(60, 60, 60), anchor='mm')
    box('argos', 256, 128, 512, 512)
    # MTF kappa-31 board: a US map with pins
    d.rectangle([512, 128, 767, 383], fill=(200, 196, 180))
    d.polygon([(530, 190), (600, 160), (700, 170), (750, 210), (740, 300), (700, 340), (620, 330), (560, 300), (532, 250)], fill=(150, 176, 140), outline=(80, 90, 70))
    for (px, py) in ((560, 220), (700, 200), (650, 260), (720, 300), (590, 290), (680, 240)):
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(220, 30, 30))
    d.text((640, 146), "CHRISTMAS NIGHT 19:30-22:30", font=ft('arialbd.ttf', 14), fill=(30, 30, 30), anchor='mm')
    d.text((640, 366), "follow him - don't stop him", font=ft('arial.ttf', 14), fill=(30, 30, 30), anchor='mm')
    box('kmap', 512, 128, 768, 384)
    # the memorial plaque in the bunker
    d.rectangle([768, 0, 1023, 191], fill=(120, 96, 50))
    d.rectangle([778, 10, 1013, 181], outline=(200, 170, 90), width=3)
    for k, ln in enumerate(("HARRY K. DAGHLIAN JR.", "21 AUGUST 1945", "LOUIS SLOTIN", "21 MAY 1946", "LOS ALAMOS")):
        d.text((896, 36 + k * 30), ln, font=ft('timesbd.ttf', 18), fill=(236, 214, 140), anchor='mm')
    box('plaque', 768, 0, 1024, 192)
    # radiation trefoil
    d.rectangle([768, 192, 1023, 447], fill=(250, 214, 40))
    cx, cy = 896, 320
    for a in (90, 210, 330):
        d.pieslice([cx - 100, cy - 100, cx + 100, cy + 100], a - 30, a + 30, fill=(20, 20, 20))
    d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=(250, 214, 40))
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(20, 20, 20))
    box('trefoil', 768, 192, 1024, 448)
    # SCP-956-1 jar label, the Stacy's charity box print, St. Nick's poster
    d.rectangle([0, 384, 255, 511], fill=(240, 236, 226))
    d.text((128, 410), "SCP-956-1", font=ft('courbd.ttf', 26), fill=(20, 20, 20), anchor='mm')
    d.text((128, 446), "KEEP AT -4 C", font=ft('courbd.ttf', 22), fill=(20, 20, 20), anchor='mm')
    d.text((128, 482), "DO NOT EAT", font=ft('courbd.ttf', 24), fill=(180, 20, 20), anchor='mm')
    box('jar', 0, 384, 256, 512)
    d.rectangle([0, 512, 255, 639], fill=(200, 40, 40))
    d.text((128, 548), "STACY'S", font=ft('arialbd.ttf', 34), fill=(255, 255, 255), anchor='mm')
    d.text((128, 590), "Charity for the Poor", font=ft('arialbd.ttf', 20), fill=(255, 230, 120), anchor='mm')
    box('stacy', 0, 512, 256, 640)
    d.rectangle([256, 512, 511, 767], fill=(28, 80, 46))
    d.text((384, 556), "ST. NICK'S", font=ft('georgiab.ttf', 40), fill=(255, 230, 140), anchor='mm')
    d.text((384, 602), "WORKSHOP", font=ft('georgiab.ttf', 34), fill=(255, 255, 255), anchor='mm')
    d.text((384, 660), "Give a child a Christmas.", font=ft('georgia.ttf', 18), fill=(255, 255, 255), anchor='mm')
    d.text((384, 700), "Every package delivered", font=ft('georgia.ttf', 16), fill=(220, 220, 220), anchor='mm')
    d.text((384, 722), "by St. Nick himself.", font=ft('georgia.ttf', 16), fill=(220, 220, 220), anchor='mm')
    box('nickposter', 256, 512, 512, 768)
    # Department of Chronology emblem: an hourglass in a ring
    d.rectangle([512, 384, 767, 639], fill=(22, 36, 70))
    d.ellipse([532, 404, 748, 620], outline=(200, 180, 110), width=6)
    d.polygon([(590, 450), (690, 450), (640, 512)], fill=(200, 180, 110))
    d.polygon([(590, 574), (690, 574), (640, 512)], fill=(200, 180, 110))
    d.text((640, 600), "DEPT. OF CHRONOLOGY", font=ft('arialbd.ttf', 13), fill=(220, 210, 160), anchor='mm')
    box('hourglass', 512, 384, 768, 640)
    # a Santa suit hanging in a locker
    d.rectangle([768, 448, 1023, 767], fill=(60, 64, 70))
    d.rectangle([800, 470, 990, 760], fill=(36, 38, 42))
    d.polygon([(840, 500), (950, 500), (970, 700), (820, 700)], fill=(190, 30, 30))
    d.rectangle([820, 690, 970, 712], fill=(240, 240, 236))
    d.rectangle([886, 500, 904, 700], fill=(240, 240, 236))
    d.rectangle([840, 600, 950, 616], fill=(30, 30, 30))
    box('suit', 768, 448, 1024, 768)
    # the frost (alpha is in its own texture), the flux meter dial
    d.rectangle([512, 640, 767, 767], fill=(236, 236, 230))
    d.arc([540, 650, 740, 850], 200, 340, fill=(30, 30, 30), width=5)
    for k in range(9):
        a = math.radians(200 + k * 17.5)
        d.line([(640 + 92 * math.cos(a), 750 + 92 * math.sin(a)), (640 + 100 * math.cos(a), 750 + 100 * math.sin(a))], fill=(30, 30, 30), width=3)
    d.arc([540, 650, 740, 850], 310, 340, fill=(220, 30, 30), width=10)
    d.text((640, 744), "NEUTRON FLUX", font=ft('arialbd.ttf', 14), fill=(30, 30, 30), anchor='mm')
    box('fluxdial', 512, 640, 768, 768)
    # a Wondertainment price sign and the BTKAI cabinet front
    d.rectangle([0, 640, 255, 767], fill=(255, 220, 60))
    d.text((128, 684), "WONDERTAINMENT", font=ft('arialbd.ttf', 24), fill=(200, 30, 120), anchor='mm')
    d.text((128, 724), "fun for every age!", font=ft('arial.ttf', 18), fill=(80, 40, 120), anchor='mm')
    box('wondersign', 0, 640, 256, 768)
    d.rectangle([0, 768, 511, 1023], fill=(30, 34, 44))
    for k in range(6):
        d.rectangle([20 + k * 80, 790, 80 + k * 80, 1000], fill=(44, 50, 66), outline=(90, 120, 200), width=2)
        for j in range(10):
            if rng.random() < 0.7:
                d.rectangle([30 + k * 80, 800 + j * 19, 70 + k * 80, 808 + j * 19], fill=(60, 140, 255))
    box('btkaifront', 0, 768, 512, 1024)
    # the reindeer service tag and the Clane flight log
    d.rectangle([512, 768, 1023, 1023], fill=(236, 232, 214))
    log = ["FLIGHT TEST LOG  4255-1 (REPLICA)", "T3  takeoff 22:04  landing 21:53", "T4  takeoff 22:10  landing 22:10",
           "T5  pilot met himself on the deck", "     (he was polite about it)", "Models R1-R8: no heat. As designed?"]
    for k, ln in enumerate(log):
        d.text((528, 784 + k * 36), ln, font=ft('courbd.ttf' if k == 0 else 'cour.ttf', 17), fill=(30, 30, 30))
    box('flightlog', 512, 768, 1024, 1024)
    save_map(wear(im, 64), 'indev_props6.png')
    json.dump(R, open('props6.json', 'w'), indent=1)


def neon():
    W, H = 1024, 512
    im = Image.new('RGB', (W, H), (6, 8, 6))
    d = ImageDraw.Draw(im)
    R = {}
    # SCP-3355's CRT: green command line
    d.rectangle([0, 0, 511, 255], fill=(4, 18, 6))
    lines = ["ARGOS A-7550  N1-CK  READY", "> STATUS", "DELIVERIES QUEUED: 4,112", "ROUTE: CHICAGO MET. AREA",
             "> WHO ARE YOU", "NICK. SGT., US ARMY.", "> _"]
    for k, ln in enumerate(lines):
        d.text((16, 14 + k * 32), ln, font=ft('courbd.ttf', 22), fill=(80, 255, 110))
    R['crt'] = (0, 0, 0.5, 0.5)
    # the vendor page on a monitor
    d.rectangle([512, 0, 1023, 255], fill=(250, 240, 255))
    d.rectangle([512, 0, 1023, 40], fill=(200, 40, 160))
    d.text((768, 20), "wondertainment - PRIZE INPUT", font=ft('arialbd.ttf', 20), fill=(255, 255, 255), anchor='mm')
    d.text((768, 90), "Enter your code from inside", font=ft('arial.ttf', 20), fill=(40, 30, 60), anchor='mm')
    d.text((768, 116), "every cereal box!", font=ft('arial.ttf', 20), fill=(40, 30, 60), anchor='mm')
    d.rectangle([600, 150, 936, 190], fill=(255, 255, 255), outline=(120, 100, 160), width=3)
    d.text((768, 230), "Good luck!!", font=ft('arialbd.ttf', 22), fill=(200, 40, 160), anchor='mm')
    R['vendor'] = (0.5, 0, 1, 0.5)
    # BTKAI screen: blue text
    d.rectangle([0, 256, 511, 511], fill=(4, 8, 30))
    for k, ln in enumerate(("BTKAI  BETA TEMPORAL KNOWLEDGE", "KNOWLEDGE COMPLETE TO: 20##", "GIFT QUEUE: 2,118,604,551",
                            "ACCURACY TARGET: 82.56%", "PILOT: CLANE, S.", "STATUS: NOMINAL / NONLINEAR")):
        d.text((16, 272 + k * 36), ln, font=ft('courbd.ttf', 20), fill=(110, 170, 255))
    R['btkai'] = (0, 0.5, 0.5, 1)
    # the night sky over the launch deck hatch
    rng = np.random.default_rng(4255)
    a = np.asarray(im).astype(float)
    sky = np.zeros((256, 512, 3))
    t = np.linspace(0, 1, 256)[:, None]
    sky[..., 0] = 8 + 20 * t
    sky[..., 1] = 14 + 26 * t
    sky[..., 2] = 40 + 50 * t
    for _ in range(420):
        y, x = rng.integers(0, 256), rng.integers(0, 512)
        sky[y, x] = rng.integers(160, 255)
    a[256:512, 512:1024] = sky
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    R['sky'] = (0.5, 0.5, 1, 1)
    im.save(os.path.join(MAPDIR, 'indev_neon6.png'))
    json.dump(R, open('neon6.json', 'w'), indent=1)


def materials():
    mottle('indev_lead.png', (88, 90, 94), (40, 40, 44), 81, sigma=1.2)
    mottle('indev_beige.png', (206, 196, 172), (150, 140, 120), 82, sigma=1.2)
    mottle('indev_beryl.png', (190, 194, 198), (110, 112, 116), 83, sigma=0.8)
    mottle('indev_pu.png', (120, 118, 112), (60, 58, 54), 84, sigma=0.6)
    mottle('indev_sleighred.png', (170, 24, 26), (80, 10, 12), 85, sigma=1.0)
    mottle('indev_gold.png', (220, 180, 70), (130, 90, 20), 86, sigma=0.8)
    # frost: white, mostly transparent at the centre
    a = np.zeros((256, 256, 4), dtype=np.uint8)
    yy, xx = np.mgrid[0:256, 0:256]
    edge = np.maximum(np.abs(xx - 128), np.abs(yy - 128)) / 128.0
    n = noise(256, 256, 87, 4, 1.0)
    alpha = np.clip((edge - 0.45) * 2.2 + (n - 0.5) * 0.8, 0, 1) * 200
    a[..., 0], a[..., 1], a[..., 2], a[..., 3] = 230, 240, 255, alpha.astype(np.uint8)
    Image.fromarray(a).save(os.path.join(MAPDIR, 'indev_frost.png'))
    # Christmas lights along a wire (alpha)
    a = np.zeros((32, 256, 4), dtype=np.uint8)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    d.line([(0, 8), (256, 8)], fill=(20, 40, 20, 255), width=2)
    cols = [(255, 60, 60), (60, 255, 80), (255, 210, 40), (80, 140, 255)]
    for k in range(8):
        x = 16 + k * 32
        d.ellipse([x - 6, 12, x + 6, 28], fill=cols[k % 4] + (255,))
    im.save(os.path.join(MAPDIR, 'indev_xlights.png'))


def skins():
    santa = (196, 28, 30)
    skin('janitor.jpg', 'indev_santa1933.jpg', (150, 34, 30), (130, 30, 28), 1.4, NT.blue,
         post=lambda a: a * (0.85 + 0.25 * noise(a.shape[0], a.shape[1], 1933, 6, 3))[..., None])          # stained
    skin('janitor.jpg', 'indev_santa4255.jpg', santa, (170, 24, 26), 1.6, NT.blue,
         post=lambda a: _trim(a, (230, 190, 80)))                                                            # gold trim
    skin('janitor.jpg', 'indev_santa6895.jpg', (176, 30, 34), (40, 60, 40), 1.5, NT.blue, post=lambda a: _trim(a, (240, 240, 236)))
    skin('janitor.jpg', 'indev_kappa31.jpg', santa, (180, 26, 28), 1.6, NT.blue, post=lambda a: _trim(a, (240, 240, 236)))
    skin('janitor.jpg', 'indev_hazmat.jpg', (226, 196, 40), (220, 190, 36), 1.6, NT.blue)
    skin('janitor.jpg', 'indev_sweater.jpg', (40, 110, 60), (60, 60, 80), 1.5, NT.blue)
    skin('scientist.jpg', 'indev_clane.jpg', (170, 30, 32), (40, 40, 44), 0.95, NT.pale)


def _trim(a, col):
    """white (or gold) bands across the jacket front/back and at the cuffs - a Santa suit's trim"""
    a = a.copy()
    for (x0, y0, x1, y1) in (NT.SHIRT_F, NT.SHIRT_B):
        h = y1 - y0
        a[y0 + int(h * 0.80):y0 + int(h * 0.88), x0 + 30:x1 - 30] = col
        a[y0 + 10:y0 + int(h * 0.80), (x0 + x1) // 2 - 8:(x0 + x1) // 2 + 8] = col
    return a


def codecard():
    """SCP-2983's prize code card: six characters, none of them letters you can type"""
    W, H = 581, 819
    im = Image.new('RGB', (W, H), (250, 244, 230))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 20, W - 20, H - 20], outline=(200, 40, 160), width=8)
    d.text((W // 2, 110), "YOUR SECRET", font=ft('arialbd.ttf', 44), fill=(200, 40, 160), anchor='mm')
    d.text((W // 2, 165), "PRIZE CODE!", font=ft('arialbd.ttf', 44), fill=(200, 40, 160), anchor='mm')
    rng = np.random.default_rng(2983)
    for k in range(6):
        cx, cy = 90 + k * 80, 360
        d.rectangle([cx - 34, cy - 60, cx + 34, cy + 60], outline=(60, 40, 90), width=3)
        pts = [(cx + rng.integers(-24, 25), cy + rng.integers(-48, 49)) for _ in range(4)]
        d.line(pts, fill=(30, 20, 50), width=6)
        d.ellipse([cx - 6, cy - 50, cx + 6, cy - 38], outline=(30, 20, 50), width=3)
    d.text((W // 2, 520), "Enter it at", font=ft('arial.ttf', 30), fill=(60, 40, 90), anchor='mm')
    d.text((W // 2, 560), "sweets.wondertainment.###", font=ft('arialbd.ttf', 26), fill=(60, 40, 90), anchor='mm')
    d.text((W // 2, 700), "Only someone over 18 may accept a prize.", font=ft('arial.ttf', 20), fill=(120, 100, 120), anchor='mm')
    d.text((W // 2, 730), "Tell your parents!", font=ft('arial.ttf', 20), fill=(120, 100, 120), anchor='mm')
    im.filter(ImageFilter.GaussianBlur(0.4)).save(os.path.join(ITEMS, 'doc2983c.jpg'), quality=90)


def docs():
    typed('doc956', [('Clearance Level', '3'), ('Item #', 'SCP-956'), ('Object Class', 'Euclid')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-956 is kept at the centre of Humanoid Cell 956 and entered only while dormant. {Nobody under twelve is '
              'to be brought within 200 m of it.} SCP-956-1 is kept in the neighbouring cold store at -4 C; excess is incinerated.'),
        ('h', 'Description:'),
        ('p', 'SCP-956 is a pinata shaped like a four-legged animal, made of glue, sugar, an unidentified fur and human tissue. '
              'Crushing force does not damage it; fire and gunfire do. It is passive towards adults.'),
        ('p', 'It becomes active only for children under twelve, whom it kills. What it leaves behind is a pile of unmarked '
              'sweets, SCP-956-1. {Eaten by anyone over twelve, SCP-956-1 brings on a seizure within three minutes; about '
              'one in three survive.}'),
        ('h', 'Addendum 956-a:'),
        ('p', 'It has started to move outside of testing. It walks the edge of its cell, then stands facing one wall. There is '
              'an elementary school in that direction. Reclassified Euclid.'),
    ])
    typed('doc2983', [('Clearance Level', '2'), ('Item #', 'SCP-2983'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'Boxes of SCP-2983 recovered from European grocers are catalogued and kept in low-risk item storage. The prize '
              'programme is a Code Orange priority.'),
        ('h', 'Description:'),
        ('p', 'SCP-2983 is a chocolate rice cereal with marshmallows, "Judy\'s Choco-Wonder Explosion Marshmallow Bites!", '
              'by Dr. Wondertainment. Pour in enough milk and the six marshmallow shapes come alive and sing - about brushing '
              'your teeth, exercise and a balanced diet - in voices from bass to soprano.'),
        ('p', 'Children call it the best cereal ever. {Anyone over twelve finds it tastes like unsweetened oatmeal.}'),
        ('h', 'Addendum:'),
        ('p', 'Each box has a code card inside. Entered on the vendor page, a code earns a "special prize", which arrives '
              'in the lap of whoever entered it. The terminal in the storage cell is still logged in.'),
    ])
    typed('doc095fr', [('Clearance Level', '4'), ('Item #', 'SCP-095-FR'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-095-FR is kept in a lead-padded safe in Bunker 095-FR, built to stand an atomic blast. {Only Class-D may '
              'handle it.} After each flux peak the bunker is inspected.'),
        ('h', 'Description:'),
        ('p', 'SCP-095-FR, "the Demon Core", is a 6.2 kg sphere of plutonium-239, 89 mm across, held permanently at critical '
              'mass. It irradiates anything living within ten metres and wrecks electronics within twenty.'),
        ('p', 'Its mass never falls; it seems to rebuild itself. On a cycle nobody understands it detonates. The last '
              'detonation destroyed Site Algiz in 2015. Before each one, the flux climbs to a peak.'),
        ('h', 'Addendum 095-FR-3:'),
        ('p', 'It killed Harry Daghlian (1945) and Louis Slotin (1946) at Los Alamos. The bench they used has been '
              'reproduced in the bunker. {Do not touch the bench.}'),
    ])
    typed('doc3355', [('Clearance Level', '2'), ('Item #', 'SCP-3355'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-3355 is contained where it was found, in a bunker under the defunct Fort Sheridan. The Foundation runs a '
              'charity front, "St. Nick\'s Workshop", to explain its deliveries. Procedures are reviewed every two years.'),
        ('h', 'Description:'),
        ('p', 'SCP-3355 is a 1987 Argos A-7550 strategy computer, built for the Army to manage the population after a '
              'disaster. It is sentient, though its hardware cannot account for that, and calls itself Nick.'),
        ('p', 'It reroutes packages through the logistics systems of the region to poor families with young children, '
              'signed "St. Nick, 100 Christmas Street, North Pole". It does not like visitors. It does not like interruptions.'),
        ('h', 'Committee review:'),
        ('p', 'Maintain current procedures. Every vote unanimous. {No meeting has lasted a minute.}'),
    ])
    typed('doc4255', [('Clearance Level', '4'), ('Item #', 'SCP-4255'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-4255 cannot be contained. Procedure Yule-02 gives parents memories of buying the gifts it delivers. '
              'Aircraft follow it on 24 December; no force is to be used.'),
        ('h', 'Description:'),
        ('p', 'SCP-4255 is an elderly man dressed as Santa Claus, with an ornate red and gold sleigh (SCP-4255-1) drawn by '
              'eight reindeer that have no body heat. At 20:00 UTC on 24 December up to 294 versions of him appear at once, '
              'from different points in his own life, and deliver presents; they are right 82.56% of the time.'),
        ('h', 'Addendum 4255-2:'),
        ('p', 'In 2097 the Department of Chronology found Stan Clane, who matches him exactly, and was ordered to make him '
              'SCP-4255: a replica sleigh, temporal devices, eight heat-proof reindeer models, gifts from the BTKAI unit. '
              '{The hangar here is where that work happens. Versions of him turn up in it.}'),
    ])
    typed('doc1933', [('Clearance Level', '2'), ('Item #', 'SCP-1933'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1933 is kept in a low-security cell with basic furnishings and fed whiskey, double cream, sugar and oil '
              'daily. It is to be showered weekly by force. Its clothing is flammable.'),
        ('h', 'Description:'),
        ('p', 'SCP-1933 is an obese, permanently drunk man in a Santa suit. Every fluid in his body is Irish cream, and it '
              'works for him. It does not work for anyone else.'),
        ('p', 'Up to 25 ml of it is safe to drink. {Past that, every extra millilitre adds a chance that all your fluids '
              'turn to Irish cream, which kills you at once.} He leaves bottles of it wrapped as presents and will not '
              'believe they are dangerous.'),
        ('h', 'Note:'),
        ('p', 'He means well. That is the consensus. It is not much comfort.'),
    ])
    typed('doc6895', [('Clearance Level', '3'), ('Item #', 'SCP-6895'), ('Object Class', 'Keter')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-6895 cannot be confined. MTF Kappa-31 ("Unigifters") dress like it and ride unicycles at "Stacy\'s Charity '
              'for the Poor" events so that it is taken for one of them.'),
        ('h', 'Description:'),
        ('p', 'SCP-6895 is an elderly man who calls himself Sir Nicholas. He rides a unicycle through American cities on '
              'Christmas night and can move from one place to another instantly. He reaches behind his back and brings out '
              'a present - eggnog, food, something warm - for people in trouble, who talk to him as if they had always known him.'),
        ('h', 'Note:'),
        ('p', 'He has started turning up in this facility, but only near people who are hurt. {If he finds you, say thank '
              'you. He will be gone before you finish.}'),
    ])
    typed('doc1225', [('Clearance Level', '2'), ('Item #', 'SCP-1225'), ('Object Class', 'Safe')], [
        ('h', 'Special Containment Procedures:'),
        ('p', 'SCP-1225 is kept in its packing, in a locked steel box on a concrete pedestal in an open-air enclosure. '
              '{No closed containers in the enclosure, pockets included.} No more than an hour a day inside.'),
        ('h', 'Description:'),
        ('p', 'SCP-1225 is a glass Christmas ornament. Hung on a tree or other woody plant, it ages every closed container '
              'within four metres: about a year in the first day, ten years in three weeks. Cloth frays, metal corrodes, '
              'food rots, electronics die.'),
        ('p', 'People near it for long become irritable and aggressive, and the effect lasts days.'),
        ('h', 'Note:'),
        ('p', 'Somebody keeps hanging it on the tree in the enclosure. The supply locker is a closed container.'),
    ])
    NOTES = {
        'doc956b': ({0: 'Cell 956 - night log', 1: 'Walked the walls again. 50 min.', 2: 'Stopped facing NE. Same spot as',
                     3: 'after every test.', 4: 'Checked the map. School, 3 km.', 6: 'Moved the cold store thermostat', 7: 'back to -4. Somebody had eaten',
                     8: 'from the jars. He is in the', 9: 'infirmary. He might be lucky.'}, '- Dr. N.'),
        'doc2983b': ({0: 'Prize log - R. Waters', 1: 'AO-4002 toy you can\'t remember', 2: 'AO-4003 endless trivia cards',
                      3: 'AO-4004 potato, hot, never burns', 4: 'AO-4005 chomping teeth', 6: 'Each one arrives IN YOUR LAP.', 7: 'Mind your coffee.',
                      9: 'Codes are on a card inside the', 10: 'box. The terminal still works.'}, '- R. Waters'),
        'doc095frb': ({0: 'Bunker 095-FR - shift card', 1: 'Siren = flux peak in 12 seconds.', 2: 'CONTROL ROOM. DOOR SHUT.',
                       3: 'Outside the lead you take a dose.', 4: 'Next to the core you take all of it.', 6: 'Radios and NVGs die down here.',
                       7: 'Leave them upstairs.', 9: 'Do NOT touch the bench.', 10: 'Slotin knew what he was doing too.'}, '- Shift lead'),
        'doc3355b': ({0: 'DELIVERY MANIFEST (printout)', 1: 'SHIP TO: D-9341', 2: '   c/o the Foundation, wherever', 3: 'ITEM: something useful',
                       4: 'FROM: ST. NICK', 5: '   100 CHRISTMAS STREET', 6: '   NORTH POLE, NUNAVUT', 8: 'Note at the bottom:', 9: '"look after yourself, kid"'}, None),
        'doc4255b': ({0: 'Dept. of Chronology - memo', 1: 'Versions of Clane keep turning', 2: 'up on the launch deck. Older,',
                      3: 'younger, once with a burn scar', 4: 'he hasn\'t got yet.', 6: 'Be polite. Take the present.', 7: 'It is usually what you need.',
                      9: 'Do not ask him what year it is.', 10: 'He will tell you.'}, '- Hangar staff'),
        'doc1933b': ({0: 'gift tag (tied to a bottle)', 2: 'TO: YOU!!', 3: 'MERRY CHRISTMAS', 4: 'from SANTA', 6: 'drink it all at once,',
                      7: 'its the best part', 9: '(scrawled, smells of whiskey)'}, None),
        'doc6895b': ({0: 'Kappa-31 field card', 1: 'He finds the ones who are', 2: 'having a bad night. Hurt, cold,', 3: 'broke, scared.',
                      5: 'If he turns up: say thank you.', 6: 'Take what he gives you.', 7: 'Don\'t ask where the unicycle', 8: 'goes when he does.',
                      10: 'Wear the suit. Ride the bike.'}, '- Unigifters'),
        'doc1225b': ({0: 'Open-air enclosure - again', 1: 'Somebody hung it on the tree', 2: 'AGAIN. The locker is a closed', 3: 'container. Everything in it',
                      4: 'is rotting while I write this.', 6: 'Take it down. Put it in the box.', 7: 'Lock the box.', 9: 'And stop shouting at me.',
                      10: 'I am NOT shouting.'}, '- Sgt. Ames'),
    }
    for name, (rows, sign) in NOTES.items():
        note(name, rows, sign=sign)
    codecard()
    return NOTES


TITLES = {
    'doc956': 'Document SCP-956', 'doc956b': 'Cell 956 Night Log',
    'doc2983': 'Document SCP-2983', 'doc2983b': 'Prize Log (R. Waters)', 'doc2983c': 'Cereal Box Prize Code',
    'doc095fr': 'Document SCP-095-FR', 'doc095frb': 'Bunker 095-FR Shift Card',
    'doc3355': 'Document SCP-3355', 'doc3355b': 'St. Nick Delivery Manifest',
    'doc4255': 'Document SCP-4255', 'doc4255b': 'Dept. of Chronology Memo',
    'doc1933': 'Document SCP-1933', 'doc1933b': 'Gift Tag From Santa',
    'doc6895': 'Document SCP-6895', 'doc6895b': 'Kappa-31 Field Card',
    'doc1225': 'Document SCP-1225', 'doc1225b': 'Open-Air Enclosure Note',
}


if __name__ == '__main__':
    labels()
    doorplates()
    plates()
    props()
    neon()
    materials()
    skins()
    notes = docs()
    assert set(TITLES) == {'doc' + key(n) for n, _ in SCPS} | set(notes) | {'doc2983c'}
    print('batch 8 assets, %d documents' % len(TITLES))
